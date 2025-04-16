from fastapi import APIRouter

from services.http_handler import run_agent

router = APIRouter()

@router.get("/search/{session_id}")
async def search(session_id: str, prompt: str):
    """Search endpoint"""
    response = await run_agent(prompt, session_id, agent_name="search_agent")
    return {"response": response}