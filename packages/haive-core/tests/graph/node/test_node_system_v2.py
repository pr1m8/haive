import logging
from typing import List

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.types import NodeType
from haive.core.schema.schema_composer import SchemaComposer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_node_factory")


# Define a proper BaseModel for structured output
class Plan(BaseModel):
    steps: list[str] = Field(description="A list of steps to complete the task")


def test_node_creation_with_schema_composer():
    """Test node creation using SchemaComposer integration with a structured output model."""
    logger.info("Starting test_node_creation_with_schema_composer")

    # Create an AugLLMConfig instance with a proper BaseModel structured output
    logger.debug("Creating AugLLMConfig instance with Plan structured output model")
    aug_llm = AugLLMConfig(
        name="test_llm",
        id="llm_12345",
        model="gpt-4o",
        temperature=0.0,
        system_prompt="You are a helpful assistant that can help me plan my day.",
        structured_output_model=Plan,  # Using the BaseModel class directly
    )

    # Use SchemaComposer to dynamically generate schemas
    logger.debug("Using SchemaComposer to generate schemas from engine")
    schema_composer = SchemaComposer.from_components([aug_llm])

    # Display generated schema information for debugging
    logger.debug(f"Generated schema class: {schema_composer}")
    logger.debug(f"Schema Python code:\n{schema_composer.to_python_code()}")

    # Create input/output schemas
    input_schema = schema_composer.create_input_schema()
    output_schema = schema_composer.create_output_schema()
    state_schema = schema_composer  # .build()

    logger.debug(f"Input schema fields: {getattr(input_schema, 'model_fields', {})}")
    logger.debug(f"Output schema fields: {getattr(output_schema, 'model_fields', {})}")
    logger.debug(f"State schema fields: {getattr(state_schema, 'model_fields', {})}")

    # Verify engine I/O mappings were detected
    assert hasattr(
        state_schema, "__engine_io_mappings__"
    ), "Schema missing engine I/O mappings"
    logger.debug(f"Engine I/O mappings: {state_schema.__engine_io_mappings__}")

    # Check for structured model tracking
    assert hasattr(
        state_schema, "__structured_models__"
    ), "Schema missing structured model tracking"
    logger.debug(f"Structured models: {state_schema.__structured_models__}")

    # Create a NodeConfig with explicit schema settings for clarity
    logger.debug("Creating NodeConfig with AugLLMConfig engine and explicit schemas")
    node_config = NodeConfig(
        id="test_node_1",
        name="test_llm_node",
        engine=aug_llm,
        command_goto="END",
        state_schema=state_schema,
        input_schema=input_schema,
        output_schema=output_schema,
    )

    # Verify that node configuration is correct
    assert (
        node_config.node_type == NodeType.ENGINE
    ), f"Expected ENGINE node type but got {node_config.node_type}"
    assert node_config.engine == aug_llm, "Engine not correctly assigned"
    assert node_config.command_goto == "END", "command_goto not correctly assigned"

    # Use NodeFactory to create a node function
    logger.debug("Creating node function with NodeFactory")
    node_function = NodeFactory.create_node_function(node_config)

    # Create a test state using the state schema directly
    logger.debug("Creating test state using the state schema")
    test_messages = [
        HumanMessage(content="Help me plan a birthday party for my daughter")
    ]
    test_state = state_schema(messages=test_messages)

    logger.debug(f"Test state created: {test_state}")

    # Test the node function configuration - we won't actually invoke it
    # since we don't want to make real API calls in tests
    assert hasattr(
        node_function, "__node_config__"
    ), "Node function missing __node_config__ attribute"
    assert hasattr(
        node_function, "__engine_id__"
    ), "Node function missing __engine_id__ attribute"
    assert (
        node_function.__engine_id__ == "llm_12345"
    ), f"Expected engine_id=llm_12345 but got {node_function.__engine_id__}"

    logger.info("Test node creation completed successfully")


def test_node_with_engine_specific_config():
    """Test node configuration handling with engine-specific settings."""
    logger.info("Starting test_node_with_engine_specific_config")

    # Create an AugLLMConfig instance
    logger.debug("Creating AugLLMConfig instance")
    aug_llm = AugLLMConfig(
        name="test_llm",
        id="llm_config_test",
        model="gpt-4o",
        temperature=0.7,  # Default temperature
        system_prompt="You are a helpful assistant.",
    )

    # Use SchemaComposer to dynamically generate schema
    schema_composer = SchemaComposer.from_components([aug_llm])
    state_schema = schema_composer

    # Create a NodeConfig with config overrides
    logger.debug("Creating NodeConfig with config overrides")
    node_config = NodeConfig(
        id="test_node_config",
        name="config_test_node",
        engine=aug_llm,
        command_goto="END",
        state_schema=state_schema,
        config_overrides={
            "temperature": 0.0,  # Override default temperature
            "max_tokens": 500,
        },
    )

    # Create node function
    NodeFactory().create_node_function(node_config)

    # Verify that config overrides were properly set
    assert (
        "temperature" in node_config.config_overrides
    ), "Temperature not found in config_overrides"
    assert (
        node_config.config_overrides["temperature"] == 0.0
    ), "Temperature override not set correctly"

    # Create test state
    state_schema(messages=[HumanMessage(content="What is the capital of France?")])

    # Create a config with engine-specific settings
    test_config = {
        "configurable": {
            "engine_configs": {
                "llm_config_test": {
                    "temperature": 0.3  # This should override the node's config_overrides
                }
            }
        }
    }

    logger.debug(f"Created test config: {test_config}")

    # We're not actually invoking the function here, just verifying the config is properly structured
    logger.info("Engine configuration test completed successfully")


def test_node_schema_integration():
    """Test integration between node system and schema system."""
    logger.info("Starting test_node_schema_integration")

    # Create an AugLLMConfig with Plan output model
    logger.debug("Creating AugLLMConfig with Plan model")
    aug_llm = AugLLMConfig(
        name="integration_test_llm",
        id="llm_integration",
        model="gpt-4o",
        temperature=0.0,
        system_prompt="You are a helpful planning assistant.",
        structured_output_model=Plan,
    )

    # Generate schema using SchemaComposer
    logger.debug("Generating schema with SchemaComposer")
    schema = SchemaComposer.from_components([aug_llm])
    state_schema = schema

    # Verify that the schema has proper field tracking
    assert "messages" in state_schema.model_fields, "Schema missing messages field"
    assert "plan" in state_schema.model_fields, "Schema missing plan field"

    # Verify engine I/O mappings were detected
    assert hasattr(
        state_schema, "__engine_io_mappings__"
    ), "Schema missing engine I/O mappings"
    engine_mappings = state_schema.__engine_io_mappings__

    logger.debug(f"Engine I/O mappings: {engine_mappings}")
    assert (
        "llm_integration" in engine_mappings
    ), "Engine mapping missing for llm_integration"
    assert (
        "inputs" in engine_mappings["llm_integration"]
    ), "Engine mapping missing inputs"
    assert (
        "outputs" in engine_mappings["llm_integration"]
    ), "Engine mapping missing outputs"

    # Create a NodeConfig with auto-extracted I/O mappings
    logger.debug("Creating NodeConfig with auto-extracted mappings")
    node_config = NodeConfig(
        id="integration_node",
        name="integration_test_node",
        engine=aug_llm,
        state_schema=state_schema,
        command_goto="END",
    )

    # Extract input/output mappings from schema __engine_io_mappings__
    input_mappings = {}
    output_mappings = {}

    if "llm_integration" in engine_mappings:
        for input_field in engine_mappings["llm_integration"].get("inputs", []):
            input_mappings[input_field] = input_field

        for output_field in engine_mappings["llm_integration"].get("outputs", []):
            output_mappings[output_field] = output_field

    # Set mappings on node config
    node_config.input_fields = input_mappings
    node_config.output_fields = output_mappings

    logger.debug(f"Auto-extracted input mappings: {input_mappings}")
    logger.debug(f"Auto-extracted output mappings: {output_mappings}")

    # Create node function
    NodeFactory.create_node_function(node_config)

    # Verify mappings are correct
    assert (
        "messages" in node_config.get_input_mapping()
    ), "Input mapping missing messages field"
    assert (
        "plan" in node_config.get_output_mapping()
    ), "Output mapping missing plan field"

    logger.info("Schema integration test completed successfully")
