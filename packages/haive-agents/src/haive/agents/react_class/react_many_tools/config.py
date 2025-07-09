from typing import Literal

from agents.rag.base.config import BaseRAGConfig
from agents.react.react.config import ReactAgentConfig
from agents.react.react_many_tools.state import ReactManyToolsState
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig, VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from langchain_core.embeddings import Embeddings
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, model_validator


class ReactManyToolsConfig(ReactAgentConfig):
    """Configuration for React Agent with many tools.

    Extends ReactAgentConfig with features for handling large numbers of tools
    and integrates with RAG capabilities.
    """

    # Override state schema
    state_schema: type[BaseModel] = Field(default=ReactManyToolsState)

    # Tool filtering configuration
    max_tools_per_request: int = Field(
        default=10,
        description="Maximum number of tools to expose to the agent per request",
    )

    # Tool categorization
    tool_categories: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Mapping of category names to lists of tool names",
    )

    # Embedding model for semantic tool search
    embeddings_model: Embeddings | None = Field(
        default=None, description="Embedding model for semantic tool filtering"
    )

    # Tool selection approach
    tool_selection_mode: Literal["semantic", "categorical", "keyword", "auto"] = Field(
        default="auto", description="Method for selecting relevant tools"
    )

    # Tool filtering prompt
    tool_filter_prompt: str | None = Field(
        default=None, description="Prompt for the filtering LLM to select tools"
    )

    # RAG integration
    rag_config: BaseRAGConfig | None = Field(
        default=None, description="Optional RAG configuration for document retrieval"
    )

    # Retriever configuration
    retriever_config: BaseRetrieverConfig | VectorStoreConfig | None = Field(
        default=None, description="Configuration for the retriever component"
    )

    # Answer generation engine
    answer_generator: AugLLMConfig | None = Field(
        default=None, description="Configuration for the answer generator"
    )

    # Integration modes
    use_rag: bool = Field(
        default=True, description="Whether to enable RAG capabilities"
    )

    @model_validator(mode="after")
    def ensure_valid_configuration(self):
        """Validate the configuration."""
        # Call parent validator
        super().ensure_valid_configuration()

        # Ensure categories are valid if specified
        if self.tool_categories:
            tool_names = {
                tool.name for tool in self.tools if isinstance(tool, BaseTool)
            }
            for category, tools in self.tool_categories.items():
                unknown_tools = [t for t in tools if t not in tool_names]
                if unknown_tools:
                    import logging

                    logging.warning(
                        f"Unknown tools in category {category}: {unknown_tools}"
                    )

        # Set default tool filter prompt if not provided
        if not self.tool_filter_prompt:
            self.tool_filter_prompt = """You are a tool selection assistant.
Given a user query and available tools, select the most relevant tools that would help answer the query.
Choose no more than {max_tools} tools.

Available tools:
{tool_descriptions}

User query: {query}

Selected tools (tool names only, one per line):"""

        # Validate RAG configuration
        if self.use_rag:
            if not self.rag_config and not self.retriever_config:
                import logging

                logging.warning(
                    "RAG is enabled but no retriever_config or rag_config provided"
                )

            # Convert VectorStoreConfig to RetrieverConfig if needed
            if isinstance(self.retriever_config, VectorStoreConfig):
                self.retriever_config = VectorStoreRetrieverConfig(
                    name=f"retriever_for_{self.name}",
                    vector_store_config=self.retriever_config,
                )

        return self
