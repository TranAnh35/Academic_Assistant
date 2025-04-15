# Định nghĩa CoordinatorAgent

from agents.sub_agent.search.agent import SearchAgent
from google.adk.agents import Agent

root_agent = Agent(
    name="Coordinator_Agent",
    model="gemini-2.0-flash",
    sub_agents=[SearchAgent],
)