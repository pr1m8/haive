from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from haive.agents.document_modifiers.complex_extraction.agent import (
    ComplexExtractionAgent,
)
from haive.agents.document_modifiers.complex_extraction.config import (
    ComplexExtractionAgentConfig,
)


# Helper function to create an extraction agent
def create_complex_extraction_agent(
    extraction_model: type[BaseModel],
    system_prompt: str | None = None,
    model: str = "gpt-4o",
    max_retries: int = 3,
    force_tool_choice: bool = True,
    use_jsonpatch: bool = True,
    parse_pydantic: bool = False,
    **kwargs,
) -> ComplexExtractionAgent:
    """Create a complex extraction agent.

    Args:
        extraction_model: Pydantic model for extraction
        system_prompt: System prompt
        model: Model name
        max_retries: Maximum retry attempts
        force_tool_choice: Whether to force the tool choice
        use_jsonpatch: Whether to use JSONPatch for validation
        parse_pydantic: Whether to parse extracted data into a Pydantic object
        **kwargs: Additional arguments for agent configuration

    Returns:
        ComplexExtractionAgent instance
    """
    # Set up default system prompt
    if system_prompt is None:
        system_prompt = f"You are a precise data extraction assistant specialized in extracting {extraction_model.__name__} information from text. Extract all required fields accurately according to the schema."

    # Create prompt template with system prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), MessagesPlaceholder(variable_name="messages")]
    )

    # Set up LLM config
    llm_config = AzureLLMConfig(
        model=model, parameters={"temperature": 0.1}  # Lower temperature for extraction
    )

    # Create engine
    engine = AugLLMConfig(
        name=f"extract_{extraction_model.__name__}_engine",
        llm_config=llm_config,
        prompt_template=prompt_template,
    )

    # Create config
    config = ComplexExtractionAgentConfig(
        name=kwargs.pop("name", f"extract_{extraction_model.__name__}"),
        extraction_model=extraction_model,
        max_retries=max_retries,
        force_tool_choice=force_tool_choice,
        use_jsonpatch=use_jsonpatch,
        system_prompt=system_prompt,
        engine=engine,
        parse_pydantic=parse_pydantic,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()
