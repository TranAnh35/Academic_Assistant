# api/websocket_router.py
import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path, HTTPException

from services.websocket_handler import (
    agent_to_client_messaging,
    client_to_agent_messaging,
)
from agents.registry import get_agent, list_available_agents
from core.adk_setup import start_agent_session

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/{agent_name}/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    agent_name: str = Path(..., description=f"Name of the agent to connect to. Available: {', '.join(list_available_agents())}"),
    session_id: str = Path(..., description="Unique session identifier")
    ):
    """WebSocket endpoint for real-time agent interaction."""

    try:
        agent = get_agent(agent_name)
        logger.info(f"Agent '{agent_name}' found for WebSocket connection.")
    except ValueError as e:
        logger.error(f"WebSocket connection failed: {e}")
        await websocket.close(code=1008, reason=str(e))
        return

    await websocket.accept()
    logger.info(f"WebSocket Client connected: Agent='{agent_name}', Session='{session_id}'")

    agent_to_client_task = None
    client_to_agent_task = None

    try:
        live_events, live_request_queue = start_agent_session(session_id, agent)
        logger.info(f"ADK live session started for Agent='{agent_name}', Session='{session_id}'")

        agent_to_client_task = asyncio.create_task(
            agent_to_client_messaging(websocket, live_events, session_id)
        )
        client_to_agent_task = asyncio.create_task(
            client_to_agent_messaging(websocket, live_request_queue, session_id)
        )

        
        done, pending = await asyncio.wait(
            {agent_to_client_task, client_to_agent_task},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            logger.debug(f"Cancelling pending task: {task.get_name()} for Session='{session_id}'")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e_cancel:
                logger.error(f"Error during task cancellation for Session='{session_id}': {e_cancel}", exc_info=True)


        for task in done:
            if task.exception():
                logger.error(f"WebSocket handling task failed for Session='{session_id}': {task.exception()}", exc_info=task.exception())


    except WebSocketDisconnect:
        logger.info(f"WebSocket Client disconnected gracefully: Agent='{agent_name}', Session='{session_id}'")
    except Exception as e:
        logger.error(f"Error during WebSocket connection handling for Agent='{agent_name}', Session='{session_id}': {e}", exc_info=True)
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except Exception:
            pass
    finally:
        if agent_to_client_task and not agent_to_client_task.done():
            agent_to_client_task.cancel()
        if client_to_agent_task and not client_to_agent_task.done():
            client_to_agent_task.cancel()

        try:
            if websocket.client_state != websocket.client_state.DISCONNECTED:
                 await websocket.close()
                 logger.info(f"WebSocket connection closed for Session='{session_id}'.")
        except Exception as e_close:
             logger.warning(f"Error trying to close WebSocket for Session='{session_id}': {e_close}")

        logger.info(f"Finished handling WebSocket connection for Agent='{agent_name}', Session='{session_id}'")