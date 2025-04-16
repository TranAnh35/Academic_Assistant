from agents.agent import root_agent
from agents.sub_agent.search.agent import SearchAgent

from google.adk.agents import Agent

def get_agent(agent_name: str) -> Agent:
    """Get the agent based on the agent name."""
    if agent_name == "root_agent" or agent_name == "root":
        return root_agent
    elif agent_name == "search_agent" or agent_name == "search":
        return SearchAgent
    else:
        raise ValueError(f"Unknown agent name: {agent_name}")