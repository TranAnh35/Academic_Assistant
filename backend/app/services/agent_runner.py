# services/agent_runner.py
import logging
from google.genai import types as genai_types
from google.adk.agents import Agent

from core.adk_setup import (
    create_runner,
    create_run_config,
    create_session
)
from agents.registry import get_agent

logger = logging.getLogger(__name__)

async def run_agent_http(prompt: str, session_id: str, agent_name: str) -> str | None:
    """
    Chạy một agent với prompt và session ID cho HTTP request.
    Trả về phản hồi cuối cùng dưới dạng text hoặc None nếu lỗi.
    """
    logger.info(f"Received HTTP request for agent '{agent_name}' (Session: {session_id})")
    logger.debug(f"Prompt: {prompt}")

    try:
        agent: Agent = get_agent(agent_name)
    except ValueError as e:
        logger.error(f"Failed to get agent '{agent_name}': {e}")
        return None

    try:
        # Tạo content input cho agent
        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=prompt)],
        )
    except Exception as e:
        logger.error(f"Error creating input content: {e}", exc_info=True)
        return None

    try:
        create_session(session_id)
        logger.info(f"Ensured session exists for ID: {session_id}")

        runner = create_runner(agent)
        run_config = create_run_config()
        logger.info(f"ADK Runner and RunConfig created for agent '{agent_name}'.")

        events = runner.run_async(
            user_id=session_id,
            session_id=session_id,
            new_message=content,
            run_config=run_config,
        )

        final_response_text = None
        logger.info("Waiting for agent response...")
        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                    logger.info(f"Final response received (Session: {session_id})")
                    logger.debug(f"Final response content: {final_response_text}")
                else:
                    logger.warning(f"Final response event received but content/parts are missing (Session: {session_id}).")
                break
            elif event.error:
                 logger.error(f"Agent run error event: {event.error} (Session: {session_id})")
            else:
                logger.debug(f"Received intermediate event: {type(event)} (Session: {session_id})")


        if final_response_text is None:
            logger.error(f"No final response received from agent '{agent_name}' (Session: {session_id}).")
            return None

        return final_response_text

    except Exception as e:
        logger.error(f"Error running agent '{agent_name}' (Session: {session_id}): {e}", exc_info=True)
        return None