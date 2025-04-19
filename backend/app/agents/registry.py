# agents/registry.py
import logging
from google.adk.agents import Agent

from agents.agent import root_agent
from agents.sub_agent.search.agent import SearchAgent

logger = logging.getLogger(__name__)

# Sử dụng dictionary để đăng ký agent, dễ mở rộng (OCP)
_agent_registry = {
    "coordinator": root_agent,
    "search": SearchAgent,
    # Thêm các agent khác vào đây
}

# Có thể thêm alias
_agent_registry["root"] = root_agent
_agent_registry["search_agent"] = SearchAgent


def get_agent(agent_name: str) -> Agent:
    """Lấy instance agent dựa trên tên đã đăng ký."""
    agent = _agent_registry.get(agent_name.lower()) # Chuẩn hóa tên về chữ thường
    if agent is None:
        logger.error(f"Unknown agent name requested: {agent_name}")
        raise ValueError(f"Unknown agent name: {agent_name}")
    logger.debug(f"Retrieved agent: {agent_name}")
    return agent

def list_available_agents() -> list[str]:
    """Liệt kê tên các agent có sẵn."""
    return list(_agent_registry.keys())