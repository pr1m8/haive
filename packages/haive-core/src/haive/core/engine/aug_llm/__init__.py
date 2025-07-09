"""
AugLLM module for creating enhanced LLM chains.

This module provides a comprehensive configuration and factory system for building
enhanced LLM chains with prompts, tools, output parsers, and structured output models.
The AugLLM system is designed to streamline the creation of complex LLM interactions
while providing extensive validation, debugging, and customization capabilities.

Key components:
- AugLLMConfig: Central configuration class for defining LLM chain behavior
- AugLLMFactory: Factory for transforming configurations into executable runnables
- Utility functions: Tools for composing, chaining, and managing runnables

The AugLLM system integrates tightly with LangChain runnables while adding
significant enhancements for tool integration, structured output handling, and
comprehensive configuration management. It supports both traditional parser-based
approaches (v1) and modern tool-based approaches (v2) to structured output.

Examples:
    >>> from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
    >>> from pydantic import BaseModel, Field
    >>>
    >>> # Define a structured output model
    >>> class Answer(BaseModel):
    >>>     response: str = Field(description="The answer to the question")
    >>>     confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    >>>
    >>> # Create a configuration
    >>> config = AugLLMConfig(
    >>>     name="qa_agent",
    >>>     system_message="You are a helpful assistant that answers questions accurately.",
    >>>     structured_output_model=Answer,
    >>>     temperature=0.3
    >>> )
    >>>
    >>> # Create a runnable
    >>> qa_chain = compose_runnable(config)
    >>>
    >>> # Use the runnable
    >>> result = qa_chain.invoke("What is the capital of France?")
"""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.engine.aug_llm.factory import AugLLMFactory
from haive.core.engine.aug_llm.mcp_config import (
    MCPAugLLMConfig,
    create_mcp_aug_llm_config,
)
from haive.core.engine.aug_llm.utils import (
    chain_runnables,
    compose_runnable,
    compose_runnables_from_dict,
    create_runnables_dict,
    merge_configs,
)

__all__ = [
    "AugLLMConfig",
    "MCPAugLLMConfig",
    "AugLLMFactory",
    "compose_runnable",
    "create_runnables_dict",
    "compose_runnables_from_dict",
    "chain_runnables",
    "merge_configs",
    "create_mcp_aug_llm_config",
]
