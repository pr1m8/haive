import inspect
import json
import logging
import traceback

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, ConfigDict, Field

from haive.haive.agents.simple.factory import create_simple_agent
from haive.haive.core.engine.aug_llm import AugLLMConfig
from haive.haive.core.models.llm.base import AzureLLMConfig

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def debug_print_schema(schema):
    """Provide a comprehensive debug print of a schema"""
    logger.debug("Schema Details:")
    logger.debug(f"Schema Name: {schema.__name__}")
    logger.debug("Schema Fields:")

    # Access model_fields for Pydantic v2
    if hasattr(schema, "model_fields"):
        for field_name, field_info in schema.model_fields.items():
            logger.debug(
                f"- {field_name}: Type={field_info.annotation}, Default={field_info.default}"
            )
    # Fallback for Pydantic v1 or other models
    elif hasattr(schema, "__fields__"):
        for field_name, field_info in schema.__fields__.items():
            logger.debug(
                f"- {field_name}: Type={field_info.type_}, Default={field_info.default}"
            )


def inspect_module_members(module):
    """Inspect module members and print relevant details"""
    logger.debug(f"Inspecting module: {module.__name__}")
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, BaseModel):
            logger.debug(f"Found BaseModel: {name}")
            debug_print_schema(obj)


def test_simple_agent_schema_validation():
    """Test that SimpleAgent correctly derives schema from AugLLMConfig with structured output model"""

    # Define a custom structured model for demonstration
    class PersonInfo(BaseModel):
        name: str = Field(description="Person's name")
        age: int | None = Field(default=None, description="Person's age")
        interests: list[str] = Field(
            default_factory=list, description="List of interests"
        )

        model_config = ConfigDict(extra="allow")  # Allow extra fields

    # Create a prompt template that will generate PersonInfo
    person_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Generate a detailed person profile based on the input."),
            ("human", "Tell me about the person: {person_description}"),
        ]
    )

    # Create an AugLLMConfig with structured output
    person_aug_llm = AugLLMConfig(
        name="person_profile_generator",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=person_prompt,
        structured_output_model=PersonInfo,
    )

    # Log engine details for debugging
    logger.debug("AugLLMConfig Details:")
    logger.debug(f"Name: {person_aug_llm.name}")
    logger.debug(
        f"Prompt Template Input Variables: {person_aug_llm.prompt_template.input_variables}"
    )
    logger.debug(f"Structured Output Model: {person_aug_llm.structured_output_model}")

    # Log derived schemas from engine
    try:
        input_schema = person_aug_llm.derive_input_schema()
        logger.debug("Input Schema:")
        debug_print_schema(input_schema)

        output_schema = person_aug_llm.derive_output_schema()
        logger.debug("Output Schema:")
        debug_print_schema(output_schema)
    except Exception as e:
        logger.exception(f"Error deriving schemas: {e}")

    # Create a simple agent with the structured output model
    try:
        agent = create_simple_agent(
            engine=person_aug_llm, name="person_profile_agent", visualize=False
        )
    except Exception as e:
        logger.exception(f"Error creating agent: {e}")
        logger.exception(f"Full traceback: {traceback.format_exc()}")
        raise

    # Validate state schema creation
    assert hasattr(agent, "state_schema"), "Agent should have a state schema"
    state_schema = agent.state_schema

    # Debug the schema
    debug_print_schema(state_schema)

    # Verify essential fields exist
    logger.debug("Checking schema fields:")
    for field_name in state_schema.model_fields:
        logger.debug(f"Found field: {field_name}")

    expected_fields = ["messages", "runnable_config", "person_description"]
    for field in expected_fields:
        assert (
            field in state_schema.model_fields
        ), f"{field} field should exist in state schema"

    # Verify structured output field exists (using lowercase name convention)
    model_name = person_aug_llm.structured_output_model.__name__.lower()
    assert (
        model_name in state_schema.model_fields
    ), f"Structured output field '{model_name}' should exist in schema"

    # Test creating a state instance
    try:
        state_instance = state_schema(
            messages=[HumanMessage(content="Test message")],
            person_description="A creative artist in their 30s",
            personinfo=PersonInfo(name="Test", age=30, interests=["Testing"]),
        )
        assert (
            state_instance.personinfo.name == "Test"
        ), "Failed to access structured output field"
        logger.debug("Successfully created and validated state instance")
    except Exception as e:
        logger.exception(f"Error creating state instance: {e}")
        raise


def test_agent_with_output_parsing():
    """Test that SimpleAgent correctly derives input fields from prompt template"""
    # Create a simple output parser
    output_parser = StrOutputParser()

    # Create prompt template with explicit text variable
    simple_prompt = ChatPromptTemplate.from_messages(
        [("system", "Summarize the input text concisely."), ("human", "{text}")]
    )

    # Log prompt details
    logger.debug(f"Prompt template input variables: {simple_prompt.input_variables}")

    # Create AugLLMConfig with output parser
    summary_aug_llm = AugLLMConfig(
        name="text_summarizer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=simple_prompt,
        output_parser=output_parser,
    )

    # Log derived input schema
    try:
        input_schema = summary_aug_llm.derive_input_schema()
        logger.debug("Input Schema from AugLLMConfig:")
        debug_print_schema(input_schema)
    except Exception as e:
        logger.exception(f"Error deriving input schema: {e}")

    # Create agent
    try:
        summary_agent = create_simple_agent(
            engine=summary_aug_llm, name="summary_agent", visualize=False
        )
    except Exception as e:
        logger.exception(f"Error creating summary agent: {e}")
        logger.exception(f"Full traceback: {traceback.format_exc()}")
        raise

    # Debug state schema
    debug_print_schema(summary_agent.state_schema)

    # Verify required fields from prompt template are present
    assert (
        "text" in summary_agent.state_schema.model_fields
    ), "Input variable 'text' should be in schema"
    assert (
        "messages" in summary_agent.state_schema.model_fields
    ), "Messages field should be in schema"
    assert (
        "runnable_config" in summary_agent.state_schema.model_fields
    ), "runnable_config field should be in schema"
    # assert 'output' in summary_agent.state_schema.model_fields, "output field should be in schema"

    # Test agent functionality with simple input
    try:
        input_data = {
            "text": "Artificial intelligence is transforming industries through automation, enhanced decision-making, and innovative solutions to complex problems."
        }
        result = summary_agent.run(input_data)

        # Validate result structure
        assert "messages" in result, "Result should contain messages"
        # assert 'output' in result, "Result should contain output field"

        # Log result for inspection
        logger.debug("Agent Run Result:")
        logger.debug(json.dumps({k: str(v) for k, v in result.items()}, indent=2))
    except Exception as e:
        logger.exception(f"Error running agent: {e}")
        logger.exception(f"Full traceback: {traceback.format_exc()}")
        raise
