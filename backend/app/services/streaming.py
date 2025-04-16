import os
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.agents import LiveRequestQueue, Agent
from google.adk.agents.run_config import RunConfig
from google.adk.sessions.in_memory_session_service import InMemorySessionService


# Load Gemini API Key
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Gemini")
session_service = InMemorySessionService()

def _create_session(session_id: str):
    """Create a new session."""
    return session_service.create_session(
        app_name=APP_NAME,
        user_id=session_id,
        session_id=session_id,
    )

def _create_runner(agent: Agent):
    """Create a new runner."""
    return Runner(
        app_name=APP_NAME,
        agent=agent,
        session_service=session_service,
    )

def _create_run_config():
    """Create a new run config."""
    return RunConfig(response_modalities=["TEXT"])

def _create_live_request_queue():
    """Create a new live request queue."""
    return LiveRequestQueue()

def start_agent_session(session_id: str, agent: Agent):
    """Starts an agent session"""
    
    session = _create_session(session_id)
    runner = _create_runner(agent)
    run_config = _create_run_config()
    live_request_queue = _create_live_request_queue()
    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    
    return live_events, live_request_queue