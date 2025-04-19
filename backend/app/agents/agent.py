# agents/coordinator.py
import logging
from google.adk.agents import Agent

from agents.sub_agent.search.agent import SearchAgent

logger = logging.getLogger(__name__)

root_agent = Agent(
    name="Coordinator_Agent",
    model="gemini-2.0-flash",
    sub_agents=[SearchAgent],
)

logger.info("CoordinatorAgent defined.")