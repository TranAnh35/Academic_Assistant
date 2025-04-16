from google.genai import types
# Remove direct import of InMemorySessionService if not needed elsewhere in this file
# from google.adk.sessions.in_memory_session_service import InMemorySessionService

from .streaming import (
    _create_runner,
    _create_run_config,
    _create_session, # Import _create_session
)

from .agent_handler import get_agent

import logging

logger = logging.getLogger(__name__)

async def run_agent(prompt: str, session_id: str, agent_name: str = "search_agent"):
    """Run the agent with the given prompt and session ID."""
    try:
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    except Exception as e:
        logger.error(f"Error creating content: {e}")
        logger.debug(f"Prompt: {prompt}")
        return None
    
    logger.info(f"Prompt: {prompt}")
    
    try:
        agent = get_agent(agent_name)
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        logger.debug(f"Agent name: {agent_name}")
        return None
    
    logger.info(f"Running agent: {agent_name}")
    
    try:
        runner = _create_runner(agent)
    except Exception as e:
        logger.error(f"Error creating runner: {e}")
        logger.debug(f"Agent: {agent}")
        return None
    
    logger.info(f'Runner created: {runner}')
    
    try:
        _create_session(session_id)
        logger.info(f'Ensured session exists for ID: {session_id}')
    except Exception as e:
        logger.error(f"Error ensuring session exists: {e}")
        logger.debug(f"Session ID: {session_id}")
        return None

    try:
        run_config = _create_run_config()
    except Exception as e:
        logger.error(f"Error creating run config: {e}")
        return None
    
    logger.info(f'Run config created: {run_config}')
    
    try:
        # Remove await here, run_async returns an async generator
        events = runner.run_async(
            user_id=session_id,
            session_id=session_id,
            new_message=content,
            run_config=run_config,
        )
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        logger.debug(f"Content: {content}")
        return None
    
    logger.info(f'Agent running, events object: {events}') # Log the generator object itself
    
    final_response = None
    # Iterate over the async generator
    async for event in events:
        if event.is_final_response():
            # Check if content and parts exist before accessing
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                logger.info(f'Final response received: {final_response}')
            else:
                logger.warning("Final response event received but content/parts are missing.")
            break # Stop after getting the final response
        # Optional: Log other event types if needed for debugging
        # else:
        #     logger.debug(f"Received event: {event}")
    
    if final_response is None:
        logger.error("No final response received from agent.")

        return None 
            
    return final_response