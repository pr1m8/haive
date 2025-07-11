"""Debug the schema composition issue."""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.prompts import ChatPromptTemplate


def debug_schema_composition():
    """Debug how schemas are being composed."""
    # Create engine with prompt template
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant."), ("human", "{query}")]
    )

    engine = AugLLMConfig(name="test_engine", prompt_template=prompt)

    # Create schema composer
    composer = SchemaComposer(base_state_schema=LLMState)

    # Add the engine and extract fields from it
    composer.add_fields_from_engine(engine)

    # Compose the state schema
    state_schema = composer.build()


    # Check __input_fields__
    if hasattr(state_schema, "__input_fields__"):
        for engine_name, fields in state_schema.__input_fields__.items():
            pass
    else:
        pass

    # Check composer state

    # Debug engine input fields access
    if hasattr(engine, "prompt_template") and engine.prompt_template:

    # Check if engine can be called to get input fields some other way
    engine_attrs = [
        attr
        for attr in dir(engine)
        if "input" in attr.lower() and not attr.startswith("_")
    ]

    # Test calling get_input_fields directly
    try:
        input_fields = engine.get_input_fields()
        if hasattr(input_fields, "items"):
            pass

        # Check if query is wrongly in base class fields
        for field_name in input_fields:
            in_composer_fields = field_name in composer.fields
            in_base_class_fields = field_name in composer.base_class_fields

    except Exception as e:
        pass

    # Derive input schema
    input_schema = state_schema.derive_input_schema()

    # DEBUG: Check what derive_input_schema() actually uses for input_fields
    if hasattr(state_schema, "__input_fields__"):

        # Simulate what derive_input_schema does
        input_fields = []
        for engine_inputs in state_schema.__input_fields__.values():
            input_fields.extend(engine_inputs)

    if hasattr(state_schema, "__engine_io_mappings__"):
        pass

    # Test creating instances

    # Test input schema creation
    try:
        input_instance = input_schema(query="hello")
    except Exception as e:
        pass")

    # Test state schema creation with just input data
    try:
        # This should fail because engine is required
        state_instance = state_schema(query="hello")
    except Exception as e:
        pass")

    # Test state schema creation with engine
    try:
        state_instance = state_schema(query="hello", engine=engine)
    except Exception as e:
        pass")


if __name__ == "__main__":
    debug_schema_composition()
