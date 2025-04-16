import asyncio

from fastapi import APIRouter, WebSocket

from services.websocket_handler import (
    agent_to_client_messaging,
    client_to_agent_messaging,
)
from services.agent_handler import get_agent
from services.streaming import start_agent_session

router = APIRouter()

@router.websocket("{agent_name}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str, session_id: int):
    """Client websocket endpoint"""
    
    await websocket.accept()
    print(f"Client #{session_id} connected")
    
    agent = get_agent(agent_name)
    session_id_str = str(session_id)
    
    live_events, live_request_queue = start_agent_session(session_id_str, agent)
    agent_to_client_task = asyncio.create_task(
        agent_to_client_messaging(websocket, live_events)
    )
    client_to_agent_task = asyncio.create_task(
        client_to_agent_messaging(websocket, live_request_queue)
    )
    await asyncio.gather(agent_to_client_task, client_to_agent_task)
    
    print(f"Client #{session_id} disconnected")
    
    await websocket.close()