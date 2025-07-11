"""Configuration for the open_perplexity research agent.

This module defines the configuration class and factory methods for creating
research agent configurations. It includes settings for LLM engines, tools,
vector stores, and research parameters.
"""

from datetime import datetime
from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.models.vectorstore.base import VectorStoreConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from haive.agents.research.open_perplexity.engines import create_research_engines
from haive.agents.research.open_perplexity.prompts import MAIN_SYSTEM_PROMPT
from haive.agents.research.open_perplexity.react_agent_config import (
    create_research_rag_engine,
    create_research_react_agent_config,
)

# Import agent-specific modules
from haive.agents.research.open_perplexity.state import (
    ResearchInputState,
    ResearchOutputState,
    ResearchState,
)
from haive.agents.research.open_perplexity.structured_tools import RESEARCH_TOOLS


class ResearchAgentConfig(AgentConfig):
    """Configuration for open_perplexity research agent.

    Defines all configuration parameters for the research agent, including
    state schemas, engines, tools, and research parameters.

    Attributes:
        state_schema: Schema for the agent state
        input_schema: Schema for input to the agent
        output_schema: Schema for agent output
        engines: Dictionary of AugLLM engines for different tasks
        tools: Tools for research and analysis
        vectorstore_config: Vector store configuration for document storage
        react_agent_name: Name of the configured ReAct agent
        rag_agent_name: Name of the configured RAG agent
        report_format: Format for the final report
        research_depth: Depth of research (1-5, higher means more thorough)
        max_sources_per_query: Maximum number of sources to use per query
        concurrent_searches: Number of concurrent searches to perform
        default_report_sections: Default sections for the research report
    """

    # Override state schema to use our custom state
    state_schema: type[BaseModel] = Field(
        default=ResearchState, description="Schema for the agent state"
    )

    # Input and output schemas
    input_schema: type[BaseModel] = Field(
        default=ResearchInputState, description="Schema for input to the agent"
    )

    output_schema: type[BaseModel] = Field(
        default=ResearchOutputState, description="Schema for agent output"
    )

    # Engines dictionary
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="Dictionary of AugLLM engines for different tasks",
    )

    # Tool configurations
    tools: list[BaseTool] = Field(
        default_factory=lambda: RESEARCH_TOOLS,
        description="Tools for research and analysis",
    )

    # Vector store configuration
    vectorstore_config: VectorStoreConfig | None = Field(
        default=None, description="Vector store configuration for document storage"
    )

    # Agent configurations
    react_agent_name: str | None = Field(
        default=None, description="Name of the configured ReAct agent"
    )

    rag_agent_name: str | None = Field(
        default=None, description="Name of the configured RAG agent"
    )

    # Report generation settings
    report_format: str = Field(
        default="markdown",
        description="Format for the final report (markdown, html, etc.)",
    )

    # Research parameters
    research_depth: int = Field(
        default=3, description="Depth of research (1-5, higher means more thorough)"
    )

    max_sources_per_query: int = Field(
        default=5, description="Maximum number of sources to use per query"
    )

    concurrent_searches: int = Field(
        default=3, description="Number of concurrent searches to perform"
    )

    default_report_sections: list[dict[str, Any]] = Field(
        default_factory=lambda: [
            {
                "name": "Executive Summary",
                "description": "Brief overview of the research topic and key findings",
                "requires_research": False,
            },
            {
                "name": "Research Methodology",
                "description": "Description of the research approach, sources, and methods",
                "requires_research": False,
            },
            {
                "name": "Key Findings",
                "description": "Main findings and insights from the research",
                "requires_research": True,
            },
            {
                "name": "Analysis",
                "description": "In-depth analysis of the research findings",
                "requires_research": True,
            },
            {
                "name": "Evidence and Support",
                "description": "Supporting evidence and sources for the findings",
                "requires_research": True,
            },
            {
                "name": "Alternative Perspectives",
                "description": "Alternative viewpoints and contradictory evidence",
                "requires_research": True,
            },
            {
                "name": "Conclusions",
                "description": "Final conclusions from the research",
                "requires_research": False,
            },
            {
                "name": "References",
                "description": "List of sources used in the research",
                "requires_research": False,
            },
        ],
        description="Default report sections",
    )

    @classmethod
    def from_scratch(cls, name: str | None = None, llm_model: str = "gpt-4o", **kwargs):
        """Create a research agent configuration from scratch.

        Factory method to create a fully configured research agent with all
        necessary engines, tools, and settings.

        Args:
            name: Optional name for the agent (defaults to timestamped name)
            llm_model: Model to use for the agent (default: "gpt-4o")
            **kwargs: Additional configuration parameters

        Returns:
            ResearchAgentConfig: A fully configured research agent configuration
        """
        # Create a name if not provided
        if not name:
            name = f"open_perplexity_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create LLM configuration
        llm_config = AzureLLMConfig(
            model=llm_model,
            parameters={
                "temperature": 0.2
            },  # Lower temperature for more accurate research
        )

        # Create main AugLLM engine
        main_engine = AugLLMConfig(
            name="research_main",
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=MAIN_SYSTEM_PROMPT),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            ),
        )

        # Get all specialized engines
        engines = create_research_engines(llm_model)

        # Add main engine to engines dictionary
        engines["main"] = main_engine

        # Create ReAct agent config for research
        react_agent_config = create_research_react_agent_config(
            name=f"{name}_research", llm_model=llm_model, temperature=0.2
        )

        # Create RAG engine (but not the full config yet since we need loaded documents)
        rag_engine_name = f"{name}_retrieval_engine"
        rag_engine = create_research_rag_engine(
            name=rag_engine_name, llm_model=llm_model, temperature=0.2
        )

        # Store the engine in the engines dictionary
        engines["rag_engine"] = rag_engine

        # No rag_agent_name yet - will be set up after vector store is populated
        rag_agent_name = None

        # Create the research agent config
        return cls(
            name=name,
            engine=main_engine,  # Set main engine as primary
            engines=engines,  # Set all engines in dictionary
            react_agent_name=react_agent_config.name,
            rag_agent_name=rag_agent_name,  # This will be set later after documents are loaded
            tools=RESEARCH_TOOLS,
            **kwargs,
        )
