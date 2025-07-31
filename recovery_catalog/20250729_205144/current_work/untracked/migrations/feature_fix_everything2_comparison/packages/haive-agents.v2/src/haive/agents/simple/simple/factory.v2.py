"""Utility functions for creating and using SimpleAgent.

This module provides helper functions for easily creating SimpleAgent instances
with various configurations.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from haive.agents.simple.agent import SimpleAgent
from haive.agents.simple.config import SimpleAgentConfig
from haive.agents.simple.state import SimpleAgentState


# =============================================
# Factory Functions
# =============================================
def create_simple_agent(
    name: str = "simple_agent",
    engine: AugLLMConfig | None = None,
    state_schema: type[BaseModel] = SimpleAgentState,
    system_prompt: str = "You are a helpful assistant.",
    prompt_template: str | ChatPromptTemplate | None = None,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
    model: str = "gpt-4o",
    debug: bool = False,
    preserve_model: bool = True,
) -> SimpleAgent:
    """Create a SimpleAgent with the specified configuration.

    Args:
        name: Name of the agent
        engine: LLM engine to use (created if not provided)
        state_schema: Schema for agent state (default: SimpleAgentState)
        system_prompt: System prompt for the LLM
        prompt_template: Custom prompt template (string or ChatPromptTemplate)
        input_mapping: Mapping from state to engine inputs
        output_mapping: Mapping from engine outputs to state
        model: Model to use if creating engine
        debug: Enable debug mode
        preserve_model: Whether to preserve BaseModel instances

    Returns:
        Configured SimpleAgent instance
    """
    # Create config
    config = SimpleAgentConfig(
        name=name,
        engine=engine,
        state_schema=state_schema,
        system_prompt=system_prompt,
        prompt_template=prompt_template,
        input_mapping=input_mapping,
        output_mapping=output_mapping,
        model=model,
        debug=debug,
        preserve_model=preserve_model,
    )

    # Create and return agent
    return SimpleAgent(config)
