"""Test file for diagnosing agent serialization issues.

This script attempts to serialize and deserialize different types of agents
to identify exactly what's causing the msgpack serialization error.
"""

import json
import logging
import pickle
import traceback
from typing import Any

from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.multi.agent import MultiAgent, MultiAgentState
from haive.agents.react.agent import ReactAgent

# Import necessary components
from haive.agents.simple.agent import SimpleAgent


# Define a test tool and model for structured output
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


def try_pickle_serialization(obj: Any, name: str) -> bool:
    """Try to serialize an object with pickle."""
    logger.info(f"Testing pickle serialization for {name}")
    try:
        # Try to pickle the object
        pickled_data = pickle.dumps(obj)
        logger.info(f"✓ Successfully pickled {name} ({len(pickled_data)} bytes)")

        # Try to unpickle
        unpickled_obj = pickle.loads(pickled_data)
        logger.info(f"✓ Successfully unpickled {name}")

        # Basic verification
        logger.info(
            f"Original type: {type(obj).__name__}, Unpickled type: {type(unpickled_obj).__name__}"
        )
        return True
    except Exception as e:
        logger.exception(f"✗ Failed to pickle {name}: {type(e).__name__}: {e}")
        logger.exception(traceback.format_exc())
        return False


def try_json_serialization(obj: Any, name: str) -> bool:
    """Try to serialize an object with JSON."""
    logger.info(f"Testing JSON serialization for {name}")
    try:
        # For pydantic models, use model_dump_json
        if hasattr(obj, "model_dump_json"):
            json_data = obj.model_dump_json()
            logger.info(
                f"✓ Successfully serialized {name} using model_dump_json ({len(json_data)} bytes)"
            )
            return True

        # For objects with to_dict/dict methods
        if hasattr(obj, "to_dict"):
            dict_data = obj.to_dict()
            json_data = json.dumps(dict_data)
            logger.info(
                f"✓ Successfully serialized {name} using to_dict ({len(json_data)} bytes)"
            )
            return True
        if hasattr(obj, "dict"):
            dict_data = obj.dict()
            json_data = json.dumps(dict_data)
            logger.info(
                f"✓ Successfully serialized {name} using dict method ({len(json_data)} bytes)"
            )
            return True

        # Try direct JSON serialization (likely to fail for complex objects)
        json_data = json.dumps(obj)
        logger.info(
            f"✓ Successfully serialized {name} directly to JSON ({len(json_data)} bytes)"
        )
        return True
    except Exception as e:
        logger.exception(
            f"✗ Failed to serialize {name} to JSON: {type(e).__name__}: {e}"
        )
        return False


def try_model_dump(obj: Any, name: str) -> bool:
    """Try to use model_dump on an object."""
    logger.info(f"Testing model_dump for {name}")
    try:
        if hasattr(obj, "model_dump"):
            dump_data = obj.model_dump()
            logger.info(f"✓ Successfully dumped {name} using model_dump")

            # Check for problematic fields
            check_problematic_fields(dump_data, name)
            return True
        logger.warning(f"Object {name} doesn't have model_dump method")
        return False
    except Exception as e:
        logger.exception(f"✗ Failed to dump {name}: {type(e).__name__}: {e}")
        return False


def check_problematic_fields(data: dict[str, Any], name: str, path: str = "") -> None:
    """Recursively check for problematic fields in a dictionary."""
    if not isinstance(data, dict):
        return

    for key, value in data.items():
        current_path = f"{path}.{key}" if path else key

        # Check for problematic types
        if callable(value):
            logger.warning(f"Problematic field in {name}: {current_path} is callable")
        elif isinstance(value, type | type(None).__class__):
            logger.warning(f"Problematic field in {name}: {current_path} is a type")
        elif hasattr(value, "__class__") and value.__class__.__module__ not in [
            "builtins",
            "datetime",
        ]:
            logger.warning(
                f"Potential complex object in {name}: {current_path} is {type(value).__name__}"
            )

        # Recurse into dictionaries
        if isinstance(value, dict):
            check_problematic_fields(value, name, current_path)
        # Recurse into lists
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    check_problematic_fields(item, name, f"{current_path}[{i}]")


def test_simple_agent_serialization():
    """Test serialization of SimpleAgent."""
    logger.info("===== Testing SimpleAgent Serialization =====")

    # Create a SimpleAgent
    engine = AugLLMConfig(tools=[add])
    agent = SimpleAgent(engine=engine, name="Test Simple Agent")

    # Test serialization methods
    pickle_success = try_pickle_serialization(agent, "SimpleAgent")
    json_success = try_json_serialization(agent, "SimpleAgent")
    dump_success = try_model_dump(agent, "SimpleAgent")

    logger.info(
        f"SimpleAgent serialization results: Pickle: {pickle_success}, JSON: {json_success}, Dump: {dump_success}"
    )


def test_react_agent_serialization():
    """Test serialization of ReactAgent."""
    logger.info("===== Testing ReactAgent Serialization =====")

    # Create a ReactAgent
    engine = AugLLMConfig(tools=[add])
    agent = ReactAgent(engine=engine, name="Test React Agent")

    # Test serialization methods
    pickle_success = try_pickle_serialization(agent, "ReactAgent")
    json_success = try_json_serialization(agent, "ReactAgent")
    dump_success = try_model_dump(agent, "ReactAgent")

    logger.info(
        f"ReactAgent serialization results: Pickle: {pickle_success}, JSON: {json_success}, Dump: {dump_success}"
    )


def test_multi_agent_serialization():
    """Test serialization of MultiAgent."""
    logger.info("===== Testing MultiAgent Serialization =====")

    # Create a MultiAgent
    simple_engine = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    react_engine = AugLLMConfig(tools=[add])

    simple_agent = SimpleAgent(engine=simple_engine, name="Test Simple Agent")
    react_agent = ReactAgent(engine=react_engine, name="Test React Agent")

    multi_agent = MultiAgent(
        agents=[simple_agent, react_agent], name="Test Multi Agent"
    )

    # Test serialization methods
    pickle_success = try_pickle_serialization(multi_agent, "MultiAgent")
    json_success = try_json_serialization(multi_agent, "MultiAgent")
    dump_success = try_model_dump(multi_agent, "MultiAgent")

    logger.info(
        f"MultiAgent serialization results: Pickle: {pickle_success}, JSON: {json_success}, Dump: {dump_success}"
    )

    # Test serialization of the state
    state_instance = multi_agent._state_instance
    if state_instance:
        logger.info("===== Testing MultiAgentState Serialization =====")
        pickle_success = try_pickle_serialization(state_instance, "MultiAgentState")
        json_success = try_json_serialization(state_instance, "MultiAgentState")
        dump_success = try_model_dump(state_instance, "MultiAgentState")

        logger.info(
            f"MultiAgentState serialization results: Pickle: {pickle_success}, JSON: {json_success}, Dump: {dump_success}"
        )


def test_state_with_agents_serialization():
    """Test serializing a state with agents directly."""
    logger.info("===== Testing State With Agents Serialization =====")

    # Create a state with agents
    state = MultiAgentState()

    # Add agents to state
    simple_engine = AugLLMConfig()
    react_engine = AugLLMConfig(tools=[add])

    simple_agent = SimpleAgent(engine=simple_engine, name="Simple Agent In State")
    react_agent = ReactAgent(engine=react_engine, name="React Agent In State")

    state.add_agent(simple_agent)
    state.add_agent(react_agent)

    # Test serialization
    pickle_success = try_pickle_serialization(state, "State with agents")
    json_success = try_json_serialization(state, "State with agents")
    dump_success = try_model_dump(state, "State with agents")

    logger.info(
        f"State with agents serialization results: Pickle: {pickle_success}, JSON: {json_success}, Dump: {dump_success}"
    )


def test_specific_problematic_fields():
    """Test specific fields that might be causing serialization issues."""
    logger.info("===== Testing Specific Problematic Fields =====")

    # Create a SimpleAgent
    simple_engine = AugLLMConfig()
    simple_agent = SimpleAgent(engine=simple_engine)

    # Test graph field
    if hasattr(simple_agent, "graph"):
        logger.info("Testing graph field")
        try:
            pickle.dumps(simple_agent.graph)
            logger.info("✓ Graph is picklable")
        except Exception as e:
            logger.exception(f"✗ Graph is not picklable: {type(e).__name__}: {e}")

    # Test _state_instance field
    if hasattr(simple_agent, "_state_instance"):
        logger.info("Testing _state_instance field")
        try:
            pickle.dumps(simple_agent._state_instance)
            logger.info("✓ _state_instance is picklable")
        except Exception as e:
            logger.exception(
                f"✗ _state_instance is not picklable: {type(e).__name__}: {e}"
            )

    # Test structured_output_model field
    if hasattr(simple_agent, "structured_output_model"):
        logger.info("Testing structured_output_model field")
        try:
            pickle.dumps(simple_agent.structured_output_model)
            logger.info("✓ structured_output_model is picklable")
        except Exception as e:
            logger.exception(
                f"✗ structured_output_model is not picklable: {type(e).__name__}: {e}"
            )


def test_langgraph_serialization():
    """Test how LangGraph handles serialization."""
    logger.info("===== Testing LangGraph Serialization =====")

    try:
        from langgraph.checkpoint.base import BaseCheckpointSaver

        logger.info("Successfully imported LangGraph checkpoint components")

        # Try to inspect how LangGraph handles serialization
        if hasattr(BaseCheckpointSaver, "serialize"):
            logger.info(
                "LangGraph uses BaseCheckpointSaver.serialize for serialization"
            )

        # Look for msgpack usage
        import inspect

        import langgraph.checkpoint.memory as memory_checkpoint

        memory_source = inspect.getsource(memory_checkpoint)
        if "msgpack" in memory_source:
            logger.info("LangGraph memory checkpointer uses msgpack")

    except ImportError:
        logger.exception("Could not import LangGraph checkpoint components")


if __name__ == "__main__":
    logger.info("Starting agent serialization tests")

    # Run individual tests
    test_simple_agent_serialization()
    test_react_agent_serialization()
    test_multi_agent_serialization()
    test_state_with_agents_serialization()
    test_specific_problematic_fields()
    test_langgraph_serialization()

    logger.info("All serialization tests completed")
