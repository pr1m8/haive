import logging

from langgraph.graph import END
from langgraph.types import Command, Send

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory

# Configure logging for this test file
logger = logging.getLogger(__name__)

# Simple tests for NodeFactory that don't try to mock or patch anything


def test_create_node_function_with_real_engine(real_llm_engine):
    """Test creating a node function from a real engine."""
    logger.debug("--- Starting test_create_node_function_with_real_engine ---")
    logger.debug(f"Using real_llm_engine: {real_llm_engine}")

    # Create node function
    logger.debug("Calling NodeFactory.create_node_function with engine and END")
    node_function = NodeFactory.create_node_function(real_llm_engine, command_goto=END)
    logger.debug(f"Created node function: {node_function}")

    # Verify it's callable
    assert callable(node_function)
    logger.debug("Asserted node function is callable.")

    # Verify metadata is attached
    assert hasattr(node_function, "__node_config__")
    logger.debug("Asserted node function has __node_config__ attribute.")
    assert node_function.__node_config__.engine is real_llm_engine
    logger.debug(
        f"Asserted __node_config__.engine is the original engine: {node_function.__node_config__.engine}"
    )
    assert hasattr(node_function, "__engine_id__")
    logger.debug("Asserted node function has __engine_id__ attribute.")
    assert node_function.__engine_id__ == real_llm_engine.id
    logger.debug(
        f"Asserted __engine_id__ matches engine.id: {node_function.__engine_id__}"
    )
    logger.debug("--- Finished test_create_node_function_with_real_engine ---")


def test_node_config_with_engine_id(real_llm_engine):
    """Test NodeConfig correctly stores engine ID."""
    logger.debug("--- Starting test_node_config_with_engine_id ---")
    logger.debug(f"Using real_llm_engine: {real_llm_engine}")

    # Create a config
    logger.debug("Creating NodeConfig instance")
    node_config = NodeConfig(
        name="test_node_engine_id", engine=real_llm_engine, command_goto=END
    )
    logger.debug(f"Created NodeConfig: {node_config}")

    # Check engine and engine_id
    assert node_config.engine is real_llm_engine
    logger.debug(f"Asserted NodeConfig.engine: {node_config.engine}")
    assert node_config.engine_id == real_llm_engine.id
    logger.debug(f"Asserted NodeConfig.engine_id: {node_config.engine_id}")

    # Verify engine is properly resolved
    logger.debug("Calling NodeConfig.resolve_engine()")
    resolved_engine, engine_id = node_config.resolve_engine()
    logger.debug(f"Resolved engine: {resolved_engine}, engine_id: {engine_id}")
    assert resolved_engine is real_llm_engine
    assert engine_id == real_llm_engine.id
    logger.debug("Assertions for resolved engine passed.")
    logger.debug("--- Finished test_node_config_with_engine_id ---")


def test_node_function_with_mappings(real_llm_engine):
    """Test a node function with input/output mappings."""
    logger.debug("--- Starting test_node_function_with_mappings ---")
    input_mapping = {"state_key": "engine_input"}
    output_mapping = {"engine_output": "result_key"}
    logger.debug(f"Input mapping: {input_mapping}")
    logger.debug(f"Output mapping: {output_mapping}")

    # Create node function with mappings
    logger.debug("Calling NodeFactory.create_node_function with mappings")
    node_function = NodeFactory.create_node_function(
        real_llm_engine,
        command_goto=END,
        input_mapping=input_mapping,
        output_mapping=output_mapping,
    )
    logger.debug(f"Created node function: {node_function}")

    # Check the mappings in node_config attached to the function
    assert hasattr(node_function, "__node_config__")
    logger.debug(
        f"Checking mappings on attached __node_config__: {node_function.__node_config__}"
    )
    assert node_function.__node_config__.input_mapping == input_mapping
    logger.debug(
        f"Asserted input_mapping on node_config: {node_function.__node_config__.input_mapping}"
    )
    assert node_function.__node_config__.output_mapping == output_mapping
    logger.debug(
        f"Asserted output_mapping on node_config: {node_function.__node_config__.output_mapping}"
    )
    logger.debug("--- Finished test_node_function_with_mappings ---")


def test_config_overrides_in_node_config(real_llm_engine):
    """Test config overrides are stored correctly in NodeConfig."""
    logger.debug("--- Starting test_config_overrides_in_node_config ---")
    config_overrides = {"temperature": 0.5, "max_tokens": 100}
    logger.debug(f"Config overrides to test: {config_overrides}")

    # Create a node config with config overrides
    logger.debug("Creating NodeConfig with overrides")
    node_config = NodeConfig(
        name="test_node_overrides",
        engine=real_llm_engine,
        command_goto=END,
        config_overrides=config_overrides,
    )
    logger.debug(f"Created NodeConfig: {node_config}")

    # Check config overrides on NodeConfig object
    assert node_config.config_overrides == config_overrides
    logger.debug(
        f"Asserted config_overrides on NodeConfig object: {node_config.config_overrides}"
    )

    # Create node function and check the overrides are passed through
    logger.debug("Creating node function from NodeConfig")
    node_function = NodeFactory.create_node_function(node_config)
    logger.debug(f"Created node function: {node_function}")
    assert hasattr(node_function, "__node_config__")
    logger.debug(
        f"Checking overrides on attached __node_config__: {node_function.__node_config__}"
    )
    assert node_function.__node_config__.config_overrides == config_overrides
    logger.debug(
        f"Asserted config_overrides on attached node_config: {node_function.__node_config__.config_overrides}"
    )
    logger.debug("--- Finished test_config_overrides_in_node_config ---")


def test_node_function_with_callable():
    """Test creating a node function from a callable."""
    logger.debug("--- Starting test_node_function_with_callable ---")

    # Define a test callable
    def test_callable(state):
        logger.debug(f"Inside test_callable with state: {state}")
        result = {"processed": True, **state}
        logger.debug(f"test_callable returning: {result}")
        return result

    logger.debug(f"Defined test_callable: {test_callable}")

    # Create node function
    logger.debug("Calling NodeFactory.create_node_function with callable")
    node_function = NodeFactory.create_node_function(test_callable, command_goto=END)
    logger.debug(f"Created node function: {node_function}")

    # Verify it's callable
    assert callable(node_function)
    logger.debug("Asserted node function is callable.")

    # Test invoking the function
    test_state = {"test": "data"}
    logger.debug(f"Invoking node_function with state: {test_state}")
    result_cmd = node_function(test_state)
    logger.debug(f"Result from node_function invocation: {result_cmd}")

    # Verify result is a Command with the right structure
    assert isinstance(result_cmd, Command)
    logger.debug(f"Asserted result type is Command: {isinstance(result_cmd, Command)}")
    assert result_cmd.goto is END
    logger.debug(f"Asserted result.goto is END: {result_cmd.goto is END}")
    assert "processed" in result_cmd.update
    assert result_cmd.update["processed"] is True
    assert "test" in result_cmd.update
    assert result_cmd.update["test"] == "data"
    logger.debug(f"Asserted result.update content: {result_cmd.update}")
    logger.debug("--- Finished test_node_function_with_callable ---")


def test_extract_input():
    """Test extracting input based on mapping."""
    logger.debug("--- Starting test_extract_input ---")
    state = {
        "key1": "value1",
        "key2": "value2",
        "runnable_config": {"config_key": "config_val"},
    }
    logger.debug(f"Test state: {state}")

    # Test with no mapping (should return state excluding runnable_config)
    logger.debug("Testing _extract_input with no mapping")
    result_no_map = NodeFactory._extract_input(state, None)
    logger.debug(f"Result (no mapping): {result_no_map}")
    expected_no_map = {
        "key1": "value1",
        "key2": "value2",
    }  # runnable_config should be excluded
    assert result_no_map == expected_no_map

    # Test with mapping
    mapping_multi = {"key1": "input1", "key3": "input3"}  # key3 doesn't exist
    logger.debug(f"Testing _extract_input with multi-key mapping: {mapping_multi}")
    result_multi_map = NodeFactory._extract_input(state, mapping_multi)
    logger.debug(f"Result (multi-key mapping): {result_multi_map}")
    assert result_multi_map == {"input1": "value1"}  # Only key1 mapped

    # Test with single field mapping
    mapping_single = {"key2": "input2"}
    logger.debug(f"Testing _extract_input with single-key mapping: {mapping_single}")
    result_single_map = NodeFactory._extract_input(state, mapping_single)
    logger.debug(f"Result (single-key mapping): {result_single_map}")
    assert result_single_map == "value2"  # Returns value directly
    logger.debug("--- Finished test_extract_input ---")


def test_handle_result():
    """Test handling different result types."""
    logger.debug("--- Starting test_handle_result ---")

    # Test with dict result
    result_dict = {"key": "value"}
    logger.debug(f"Testing _handle_result with dict: {result_dict}")
    handled_dict = NodeFactory._handle_result(result_dict, END, None)
    logger.debug(f"Handled dict result: {handled_dict}")
    assert isinstance(handled_dict, Command)
    assert handled_dict.goto is END
    # Check that the original key-value pairs are present, allowing for additional metadata
    assert all(handled_dict.update.get(k) == v for k, v in result_dict.items())

    # Test with Command result
    cmd = Command(update={"test": True}, goto="next_node")
    logger.debug(f"Testing _handle_result with Command: {cmd}")
    handled_cmd = NodeFactory._handle_result(cmd, END, None)
    logger.debug(f"Handled Command result: {handled_cmd}")
    assert handled_cmd is cmd  # Should return the Command unchanged

    # Test with Send result
    send = Send("target_node", {"sent_data": True})
    logger.debug(f"Testing _handle_result with Send: {send}")
    handled_send = NodeFactory._handle_result(send, END, None)
    logger.debug(f"Handled Send result: {handled_send}")
    assert handled_send is send  # Should return the Send unchanged

    # Test with output mapping
    result_map = {"source_key": "value"}
    output_mapping = {"source_key": "target_key"}
    logger.debug(
        f"Testing _handle_result with dict and output mapping: {result_map}, {output_mapping}"
    )
    handled_map = NodeFactory._handle_result(result_map, END, output_mapping)
    logger.debug(f"Handled mapped result: {handled_map}")
    assert isinstance(handled_map, Command)
    assert handled_map.goto is END
    assert "target_key" in handled_map.update
    assert handled_map.update["target_key"] == "value"
    logger.debug("--- Finished test_handle_result ---")


def test_process_output():
    """Test processing output with mapping."""
    logger.debug("--- Starting test_process_output ---")

    # Test with no mapping (should return output as-is)
    output_dict = {"key1": "value1", "key2": "value2"}
    logger.debug(f"Testing _process_output with dict and no mapping: {output_dict}")
    result_no_map = NodeFactory._process_output(output_dict, None)
    logger.debug(f"Result (no mapping): {result_no_map}")
    assert result_no_map == output_dict

    # Test with mapping
    mapping = {"key1": "state1", "key3": "state3"}  # key3 doesn't exist in output
    logger.debug(
        f"Testing _process_output with dict and mapping: {output_dict}, {mapping}"
    )
    result_map = NodeFactory._process_output(output_dict, mapping)
    logger.debug(f"Result (mapping): {result_map}")
    assert result_map == {"state1": "value1"}  # Only key1 mapped

    # Test with non-dict output and no mapping
    output_str = "string output"
    logger.debug(f"Testing _process_output with non-dict and no mapping: {output_str}")
    result_non_dict = NodeFactory._process_output(output_str, None)
    logger.debug(f"Result (non-dict, no mapping): {result_non_dict}")
    assert result_non_dict == {"result": output_str}

    # Test with non-dict output and mapping (mapping should be ignored)
    logger.debug(
        f"Testing _process_output with non-dict and mapping: {output_str}, {mapping}"
    )
    result_non_dict_map = NodeFactory._process_output(output_str, mapping)
    logger.debug(f"Result (non-dict, mapping): {result_non_dict_map}")
    assert result_non_dict_map == {"result": output_str}  # Mapping ignored for non-dict
    logger.debug("--- Finished test_process_output ---")
