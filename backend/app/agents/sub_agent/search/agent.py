# agents/search/agent.py
import logging
from google.adk.agents import Agent

from services.intergrations.google_scholar import search
from .prompts import return_instructions_search

logger = logging.getLogger(__name__)

SearchAgent = Agent(
    name="search_agent",
    model="gemini-2.0-flash", # Cập nhật model nếu cần
    description=(
        "A search agent that uses Google Scholar to find relevant papers."
    ),
    instruction=return_instructions_search(),
    tools=[search],
)

logger.info("SearchAgent defined.")