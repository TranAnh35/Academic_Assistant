# agents/search/agent.py
import logging
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools import google_search

from services.integrations.google_scholar import search_scholarly
from .prompts import return_instructions_search

logger = logging.getLogger(__name__)

GoogleSearchAgent = Agent(
    name="google_search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using Google Search.",
    instruction="You are an expert researcher. You always stick to the facts.",
    tools=[google_search]
)

ScholarAgent = Agent(
    name="scholar_agent",
    model="gemini-2.0-flash",
    description="A search agent that uses Google Scholar to find relevant papers.",
    instruction="You are an expert researcher. You always stick to the facts.",
    tools=[search_scholarly]
)

SearchAgent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description=(
        "A search agent that uses Google Search to search infomation general website and Google Scholar to find relevant papers."
    ),
    instruction=return_instructions_search('v1'),
    tools=[agent_tool.AgentTool(agent=GoogleSearchAgent), agent_tool.AgentTool(agent=ScholarAgent)]
)

logger.info("SearchAgent defined.")