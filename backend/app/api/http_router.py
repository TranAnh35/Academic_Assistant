# api/http_router.py
import logging
from fastapi import APIRouter, HTTPException, Query

from services.agent_runner import run_agent_http

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search/{session_id}")
async def search_endpoint(
    session_id: str,
    prompt: str = Query(..., min_length=1, description="User query for searching papers")
    ):
    """
    HTTP endpoint to interact with the search agent.
    """
    logger.info(f"Received search request for session: {session_id}")

    response_text = await run_agent_http(
        prompt=prompt,
        session_id=session_id,
        agent_name="search"
    )

    if response_text is None:
        logger.error(f"Agent run failed for session {session_id}")
        raise HTTPException(status_code=500, detail="Agent execution failed or produced no response.")

    logger.info(f"Successfully processed search request for session: {session_id}")
    return {"response": response_text}