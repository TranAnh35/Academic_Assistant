from google.adk.agents import Agent
from .tools import _setup_scholarly, search

SearchAgent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description=(
        "A search agent that uses Google Scholar to find relevant papers."
    ),
    instruction=(
        """
        You are a search agent. Your task is to find relevant papers on Google Scholar based on the given query.
        """
    ),
    tools=[_setup_scholarly, search],
)