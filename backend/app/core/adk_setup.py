# core/adk_setup.py
from google.adk.runners import Runner
from google.adk.agents import LiveRequestQueue, Agent
from google.adk.agents.run_config import RunConfig
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from .config import settings

session_service = InMemorySessionService()

def create_session(session_id: str):
    """Tạo hoặc lấy session ADK."""
    return session_service.create_session(
        app_name=settings.APP_NAME,
        user_id=session_id,
        session_id=session_id,
    )

def create_runner(agent: Agent):
    """Tạo ADK Runner."""
    return Runner(
        app_name=settings.APP_NAME,
        agent=agent,
        session_service=session_service,
    )

def create_run_config():
    """Tạo cấu hình chạy ADK."""
    return RunConfig(response_modalities=["TEXT"])

def create_live_request_queue():
    """Tạo hàng đợi request cho live run."""
    return LiveRequestQueue()

def start_agent_session(session_id: str, agent: Agent):
    """Bắt đầu một phiên làm việc live của agent."""
    session = create_session(session_id)
    runner = create_runner(agent)
    run_config = create_run_config()
    live_request_queue = create_live_request_queue()
    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    return live_events, live_request_queue