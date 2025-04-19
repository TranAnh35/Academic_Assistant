# services/websocket_handler.py
import json
import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect

from google.genai.types import Part, Content
from google.adk.agents import LiveRequestQueue

logger = logging.getLogger(__name__)

async def agent_to_client_messaging(websocket: WebSocket, live_events, session_id: str):
    """Gửi tin nhắn từ Agent Events đến Client qua WebSocket."""
    try:
        async for event in live_events:
            message_to_send = None
            log_message = None

            if event.turn_complete:
                message_to_send = {"turn_complete": True}
                log_message = "[TURN COMPLETE]"
            elif event.interrupted:
                message_to_send = {"interrupted": True}
                log_message = "[INTERRUPTED]"
            elif event.error:
                error_detail = str(event.error)
                message_to_send = {"error": error_detail}
                log_message = f"[AGENT ERROR]: {error_detail}"
                logger.error(f"Agent error event (Session: {session_id}): {error_detail}", exc_info=event.error)
            elif event.is_partial_response() or event.is_final_response():
                part: Part | None = (
                    event.content and event.content.parts and event.content.parts[0]
                )
                if part and part.text:
                    text = part.text
                    message_to_send = {"message": text}
                    log_message = f"[AGENT TO CLIENT]: {text}"
                else:
                    logger.debug(f"Received response event without text (Session: {session_id})")

            if message_to_send:
                try:
                    await websocket.send_text(json.dumps(message_to_send))
                    if log_message:
                        logger.info(f"{log_message} (Session: {session_id})")
                except WebSocketDisconnect:
                    logger.warning(f"WebSocket disconnected while sending message (Session: {session_id}).")
                    break
                except Exception as e:
                    logger.error(f"Error sending message via WebSocket (Session: {session_id}): {e}", exc_info=True)
                    

            await asyncio.sleep(0)

    except asyncio.CancelledError:
         logger.info(f"Agent-to-client task cancelled (Session: {session_id}).")
    except Exception as e:
         logger.error(f"Unexpected error in agent_to_client_messaging (Session: {session_id}): {e}", exc_info=True)
    finally:
         logger.info(f"Agent-to-client messaging loop finished (Session: {session_id}).")


async def client_to_agent_messaging(websocket: WebSocket, live_request_queue: LiveRequestQueue, session_id: str):
    """Nhận tin nhắn từ Client qua WebSocket và gửi đến Agent Queue."""
    try:
        while True:
            text = await websocket.receive_text()
            logger.info(f"[CLIENT TO AGENT]: {text} (Session: {session_id})")
            try:
                content = Content(role="user", parts=[Part.from_text(text=text)])
                live_request_queue.send_content(content=content)
            except Exception as e:
                logger.error(f"Error sending content to live request queue (Session: {session_id}): {e}", exc_info=True)
                await websocket.send_text(json.dumps({"error": "Failed to process your message."}))

            await asyncio.sleep(0) # Yield control
    except WebSocketDisconnect:
        logger.info(f"Client disconnected (Session: {session_id}).")
        live_request_queue.end_request()
    except asyncio.CancelledError:
         logger.info(f"Client-to-agent task cancelled (Session: {session_id}).")
    except Exception as e:
        logger.error(f"Unexpected error in client_to_agent_messaging (Session: {session_id}): {e}", exc_info=True)
    finally:
        logger.info(f"Client-to-agent messaging loop finished (Session: {session_id}).")
        live_request_queue.end_request()
        