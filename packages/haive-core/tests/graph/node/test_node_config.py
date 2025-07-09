import logging

from langgraph.graph import END

from haive.core.engine.base import EngineType
from haive.core.graph.node.config import NodeConfig

# from conftest import real_llm_engine

# Configure logging for this test file
logger = logging.getLogger(__name__)

# Define tests for NodeConfig


def test_node_config_init_basic():
    """Test basic NodeConfig initialization."""
    logger.debug("--- Starting test_node_config_init_basic ---")
    node_config = NodeConfig(name="test_node", engine="test_engine")
    logger.debug(f"Created NodeConfig: {node_config}")

    assert node_config.name == "test_node"
    logger.debug(f"Asserted name: {node_config.name}")
    assert node_config.engine == "test_engine"
    logger.debug(f"Asserted engine ref: {node_config.engine}")
    assert node_config.command_goto is None
    logger.debug(f"Asserted command_goto: {node_config.command_goto}")
    assert node_config.input_mapping is None
    logger.debug(f"Asserted input_mapping: {node_config.input_mapping}")
    assert node_config.output_mapping is None
    logger.debug(f"Asserted output_mapping: {node_config.output_mapping}")
    assert isinstance(node_config.config_overrides, dict)
    logger.debug(
        f"Asserted config_overrides type: {type(node_config.config_overrides)}"
    )
    assert isinstance(node_config.metadata, dict)
    logger.debug(f"Asserted metadata type: {type(node_config.metadata)}")
    logger.debug("--- Finished test_node_config_init_basic ---")


def test_node_config_with_end():
    """Test NodeConfig with END as command_goto."""
    logger.debug("--- Starting test_node_config_with_end ---")
    # Test with string "END"
    logger.debug("Testing with command_goto='END'")
    node_config_str = NodeConfig(
        name="test_node_str", engine="test_engine", command_goto="END"
    )
    logger.debug(f"Created NodeConfig (str): {node_config_str}")
    assert node_config_str.command_goto is END
    logger.debug(f"Asserted command_goto (str): {node_config_str.command_goto}")

    # Test with END constant
    logger.debug("Testing with command_goto=END")
    node_config_const = NodeConfig(
        name="test_node_const", engine="test_engine", command_goto=END
    )
    logger.debug(f"Created NodeConfig (const): {node_config_const}")
    assert node_config_const.command_goto is END
    logger.debug(f"Asserted command_goto (const): {node_config_const.command_goto}")
    logger.debug("--- Finished test_node_config_with_end ---")


def test_node_config_with_engine_object(real_llm_engine):
    """Test NodeConfig with an Engine object."""
    logger.debug("--- Starting test_node_config_with_engine_object ---")
    logger.debug(f"Using real_llm_engine: {real_llm_engine}")
    node_config = NodeConfig(name="test_node_engine_obj", engine=real_llm_engine)
    logger.debug(f"Created NodeConfig: {node_config}")

    assert node_config.engine is real_llm_engine
    logger.debug(f"Asserted engine object: {node_config.engine}")
    assert node_config.engine_id == real_llm_engine.id
    logger.debug(f"Asserted engine_id: {node_config.engine_id}")
    logger.debug("--- Finished test_node_config_with_engine_object ---")


def test_node_config_with_mappings():
    """Test NodeConfig with input and output mappings."""
    logger.debug("--- Starting test_node_config_with_mappings ---")
    input_mapping = {"state_key": "input_key"}
    output_mapping = {"output_key": "state_key"}
    logger.debug(f"Input mapping: {input_mapping}")
    logger.debug(f"Output mapping: {output_mapping}")

    node_config = NodeConfig(
        name="test_node_mappings",
        engine="test_engine",
        input_mapping=input_mapping,
        output_mapping=output_mapping,
    )
    logger.debug(f"Created NodeConfig: {node_config}")

    assert node_config.input_mapping == input_mapping
    logger.debug(f"Asserted input_mapping: {node_config.input_mapping}")
    assert node_config.output_mapping == output_mapping
    logger.debug(f"Asserted output_mapping: {node_config.output_mapping}")
    logger.debug("--- Finished test_node_config_with_mappings ---")


def test_node_config_resolve_engine(real_llm_engine, monkeypatch):
    """Test resolving engine reference."""
    logger.debug("--- Starting test_node_config_resolve_engine ---")

    # Test with engine object
    logger.debug("Testing resolve_engine with direct engine object")
    node_config_obj = NodeConfig(name="test_node_resolve_obj", engine=real_llm_engine)
    logger.debug(f"Created NodeConfig: {node_config_obj}")
    resolved_engine_obj, engine_id_obj = node_config_obj.resolve_engine()
    logger.debug(f"Resolved engine: {resolved_engine_obj}, engine_id: {engine_id_obj}")
    assert resolved_engine_obj is real_llm_engine
    assert engine_id_obj == real_llm_engine.id
    logger.debug("Assertions passed for engine object case.")

    # Test with string (mock the registry lookup)
    logger.debug("Testing resolve_engine with string reference (mocking registry)")
    from haive.core.engine.base import EngineRegistry

    # Create a mock registry class for testing
    class MockRegistry:
        def find(self, name_or_id):
            logger.debug(f"MockRegistry.find called with: {name_or_id}")
            if name_or_id == "test_engine" or name_or_id == real_llm_engine.id:
                logger.debug(f"MockRegistry returning: {real_llm_engine}")
                return real_llm_engine
            logger.debug("MockRegistry returning None")
            return None

        # Add the 'engines' attribute needed by the first loop in resolve_engine
        @property
        def engines(self):
            # Provide a minimal structure that allows the loop to run
            # In a real scenario, this would contain actual engines
            logger.debug("MockRegistry.engines accessed")
            # We need to return something compatible with `for engine_type in registry.engines:`
            # The original code iterates keys (EngineType), then calls get(type, name)
            # Let's just return the necessary structure to pass the loop, assuming find() will work later.
            # Returning an empty dict or a dict with a dummy type should suffice for the loop structure.
            return {EngineType.LLM: {}}  # Allow iteration over engine types

        def get(self, engine_type, name):
            # Add the 'get' method used inside the loop in resolve_engine
            logger.debug(
                f"MockRegistry.get called with type: {engine_type}, name: {name}"
            )
            if engine_type == EngineType.LLM and name == "test_engine":
                logger.debug(f"MockRegistry.get returning: {real_llm_engine}")
                return real_llm_engine
            logger.debug("MockRegistry.get returning None")
            return None

    # Patch the get_instance method to return our mock
    mock_registry = MockRegistry()
    logger.debug("Patching EngineRegistry.get_instance")
    monkeypatch.setattr(EngineRegistry, "get_instance", lambda: mock_registry)

    # Create config with string reference
    node_config_str = NodeConfig(name="test_node_resolve_str", engine="test_engine")
    logger.debug(f"Created NodeConfig with string engine ref: {node_config_str}")

    # Resolve engine
    resolved_engine_str, engine_id_str = node_config_str.resolve_engine()
    logger.debug(f"Resolved engine: {resolved_engine_str}, engine_id: {engine_id_str}")
    assert resolved_engine_str is real_llm_engine
    assert engine_id_str == real_llm_engine.id
    logger.debug("Assertions passed for string reference case.")
    logger.debug("--- Finished test_node_config_resolve_engine ---")


def test_node_config_serialization(real_llm_engine, monkeypatch):
    """Test NodeConfig serialization to/from dict."""
    logger.debug("--- Starting test_node_config_serialization ---")

    # Create a config with various fields
    logger.debug("Creating NodeConfig for serialization")
    node_config = NodeConfig(
        name="test_node_serialize",
        engine=real_llm_engine,
        command_goto=END,
        input_mapping={"state_key": "input_key"},
        output_mapping={"output_key": "state_key"},
        config_overrides={"temperature": 0.7},
        metadata={"description": "Test node"},
    )
    logger.debug(f"Original NodeConfig: {node_config}")

    # Convert to dict
    logger.debug("Converting NodeConfig to dict using to_dict()")
    config_dict = node_config.to_dict()
    logger.debug(f"Serialized dict: {config_dict}")

    # Check serialization details
    assert config_dict["name"] == "test_node_serialize"
    assert config_dict["engine_ref"]["id"] == real_llm_engine.id
    assert config_dict["engine_ref"]["name"] == real_llm_engine.name
    assert config_dict["command_goto"] == "END"
    assert config_dict["input_mapping"] == {"state_key": "input_key"}
    assert config_dict["output_mapping"] == {"output_key": "state_key"}
    assert config_dict["config_overrides"] == {"temperature": 0.7}
    assert config_dict["metadata"] == {"description": "Test node"}
    logger.debug("Serialization assertions passed.")

    # Mock the registry for deserialization
    logger.debug("Setting up mock registry for deserialization")
    from haive.core.engine.base import EngineRegistry

    class MockRegistry:
        def find(self, name_or_id):
            logger.debug(
                f"MockRegistry.find called with: {name_or_id} during deserialization"
            )
            if name_or_id == real_llm_engine.id or name_or_id == real_llm_engine.name:
                logger.debug(f"MockRegistry returning engine: {real_llm_engine}")
                return real_llm_engine
            logger.debug("MockRegistry returning None")
            return None

    mock_registry = MockRegistry()
    logger.debug("Patching EngineRegistry.get_instance for deserialization")
    monkeypatch.setattr(EngineRegistry, "get_instance", lambda: mock_registry)

    # Deserialize using from_dict
    logger.debug("Deserializing dict using NodeConfig.from_dict()")
    new_config = NodeConfig.from_dict(config_dict)
    logger.debug(f"Deserialized NodeConfig: {new_config}")

    # Check fields match
    assert new_config.name == node_config.name
    assert new_config.engine_id == real_llm_engine.id
    assert new_config.engine == real_llm_engine  # Check if engine object was resolved
    assert new_config.command_goto is END
    assert new_config.input_mapping == node_config.input_mapping
    assert new_config.output_mapping == node_config.output_mapping
    assert new_config.config_overrides == node_config.config_overrides
    assert new_config.metadata == node_config.metadata
    logger.debug("Deserialization assertions passed.")
    logger.debug("--- Finished test_node_config_serialization ---")
