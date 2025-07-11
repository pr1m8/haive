"""Test the exact notebook scenario with SimpleAgent v2."""

import logging

logging.basicConfig(level=logging.DEBUG)

# Test creating and running SimpleAgent v2 exactly as in notebook

try:
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    from langchain_core.prompts import ChatPromptTemplate

    # Create agent exactly as in notebook
    agent = SimpleAgentV2(
        name="test_agent",
        prompt_template=ChatPromptTemplate.from_template("{query}"),
        temperature=0.5,
    )


    # Check state schema
    state_schema = agent.state_schema

    # Check input schema
    input_schema = agent.input_schema

    # Try to create runnable
    runnable = agent.create_runnable()

    # Try to run
    import asyncio

    async def test_run():
        result = await agent.arun("hello")
        return result

    result = asyncio.run(test_run())

except Exception as e:
    import traceback

    traceback.print_exc()

# Now test the specific issue with schema composition

try:
    from haive.core.schema.prebuilt.llm_state import LLMState
    from langgraph.graph import StateGraph

    # Test using LLMState directly
    try:
        graph = StateGraph(LLMState)
    except Exception as e:
        pass

    # Test creating a custom state that inherits from LLMState
    try:

        class CustomState(LLMState):
            custom_field: str = ""

        graph = StateGraph(CustomState)
    except Exception as e:
        pass

    # Test what SimpleAgent v2 actually creates
    try:
        agent = SimpleAgentV2(name="test")
        graph = StateGraph(agent.state_schema)
    except Exception as e:
        pass

except Exception as e:
    import traceback

    traceback.print_exc()
