from google.adk.agents import Agent
from services.scholar import search
from .prompts import return_instructions_search

SearchAgent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description=(
        "A search agent that uses Google Scholar to find relevant papers."
    ),
    instruction=return_instructions_search(),
    tools=[search],
)