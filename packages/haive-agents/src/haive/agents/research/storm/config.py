# src/haive/agents/research/storm/config.py

# NOTE: The following imports are placeholders - these modules are not yet implemented

from typing import Any

from pydantic import BaseModel, Field


# Placeholder config classes until the actual implementations are ready
class SequenceAgentConfig(BaseModel):
    """Placeholder for SequenceAgentConfig."""

    name: str = "sequence_agent"
    default_agent_configs: bool = True
    agent_configs: list = Field(default_factory=list)


class ResearchAgentConfig(BaseModel):
    """Placeholder for ResearchAgentConfig."""

    name: str = "research_agent"
    llm_config: Any | None = None
    topic: str = ""

    def build_agent(self):
        """Placeholder build method."""
        return type("Agent", (), {"config": self})()


class InterviewAgentConfig(BaseModel):
    """Placeholder for InterviewAgentConfig."""

    name: str = "interview_agent"
    llm_config: Any | None = None
    max_turns: int = 5
    num_perspectives: int = 3

    def build_agent(self):
        """Placeholder build method."""
        return type("Agent", (), {"config": self})()


class WritingAgentConfig(BaseModel):
    """Placeholder for WritingAgentConfig."""

    name: str = "writing_agent"
    llm_config: Any | None = None
    retriever_config: Any | None = None

    def build_agent(self):
        """Placeholder build method."""
        return type("Agent", (), {"config": self})()


# Placeholder LLM config until we can import the real one
class AzureLLMConfig(BaseModel):
    """Placeholder for AzureLLMConfig."""

    model: str = "gpt-4o"


# Placeholder retriever configs
class BaseRetrieverConfig(BaseModel):
    """Placeholder for BaseRetrieverConfig."""

    name: str = "retriever"


class VectorStoreRetrieverConfig(BaseRetrieverConfig):
    """Placeholder for VectorStoreRetrieverConfig."""

    vector_store_config: Any | None = None
    k: int = 4
    search_type: str = "similarity"


class VectorStoreConfig(BaseModel):
    """Placeholder for VectorStoreConfig."""

    name: str = "vector_store"
    vector_store_provider: str = "InMemory"
    embedding_model: Any | None = None


class STORMAgentConfig(SequenceAgentConfig):
    """Configuration for the STORM agent - an orchestrator that coordinates research,
    interviews, and writing to generate comprehensive Wikipedia-style articles.

    STORM follows these stages:
    1. Research: Generate initial outline and identify perspectives
    2. Interview: Conduct expert interviews for diverse insights
    3. Writing: Refine outline, write sections, and assemble final article
    """

    # Topic for research
    topic: str = Field(
        default="", description="The topic to research and generate an article about"
    )

    # LLM configurations for different components
    fast_llm_config: AzureLLMConfig = Field(
        default=AzureLLMConfig(model="gpt-4o-mini"),
        description="Configuration for the faster LLM used for research and interviews",
    )

    long_context_llm_config: AzureLLMConfig = Field(
        default=AzureLLMConfig(model="gpt-4o"),
        description="Configuration for the long-context LLM used for writing",
    )

    # Knowledge storage configuration
    vector_store_config: VectorStoreConfig = Field(
        default=None,
        description="Configuration for the vector store used to index references",
    )

    retriever_config: BaseRetrieverConfig = Field(
        default=None,
        description="Configuration for the retriever used to access references",
    )

    # Sub-agent configurations
    research_agent_config: ResearchAgentConfig = Field(
        default=None, description="Configuration for the research agent"
    )

    interview_agent_config: InterviewAgentConfig = Field(
        default=None, description="Configuration for the interview agent"
    )

    writing_agent_config: WritingAgentConfig = Field(
        default=None, description="Configuration for the writing agent"
    )

    # Control parameters
    num_perspectives: int = Field(
        default=3, description="Number of perspectives to use (N parameter)"
    )

    max_interview_turns: int = Field(
        default=5,
        description="Maximum number of conversation turns per interview (M parameter)",
    )

    def __init__(self, **data):
        # Initialize with parent class
        super().__init__(**data)

        # Don't use default sequence configurations
        self.default_agent_configs = False

        # Set up vector store config if not provided
        if not self.vector_store_config:
            self._create_default_vector_store_config()

        # Set up retriever config if not provided
        if not self.retriever_config:
            self._create_default_retriever_config()

        # Create sub-agent configs if not provided
        if not self.research_agent_config:
            self._create_research_agent_config()

        if not self.interview_agent_config:
            self._create_interview_agent_config()

        if not self.writing_agent_config:
            self._create_writing_agent_config()

        # Create the agent configs for the sequence
        self._create_storm_agent_sequence()

    def _create_default_vector_store_config(self):
        """Create the default vector store configuration."""
        from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

        self.vector_store_config = VectorStoreConfig(
            name="storm_references",
            vector_store_provider="InMemory",
            embedding_model=OpenAIEmbeddingConfig(model="text-embedding-3-small"),
        )

    def _create_default_retriever_config(self):
        """Create the default retriever configuration."""
        self.retriever_config = VectorStoreRetrieverConfig(
            name="storm_retriever",
            vector_store_config=self.vector_store_config,
            k=4,
            search_type="similarity",
        )

    def _create_research_agent_config(self):
        """Create the research agent configuration."""
        self.research_agent_config = ResearchAgentConfig(
            name="storm_research", llm_config=self.fast_llm_config, topic=self.topic
        )

    def _create_interview_agent_config(self):
        """Create the interview agent configuration."""
        self.interview_agent_config = InterviewAgentConfig(
            name="storm_interview",
            llm_config=self.fast_llm_config,
            max_turns=self.max_interview_turns,
            num_perspectives=self.num_perspectives,
        )

    def _create_writing_agent_config(self):
        """Create the writing agent configuration."""
        self.writing_agent_config = WritingAgentConfig(
            name="storm_writing",
            llm_config=self.long_context_llm_config,
            retriever_config=self.retriever_config,
        )

    def _create_storm_agent_sequence(self):
        """Create the sequence of agents for the STORM workflow."""
        # Build the subagents
        research_agent = self.research_agent_config.build_agent()
        interview_agent = self.interview_agent_config.build_agent()
        writing_agent = self.writing_agent_config.build_agent()

        # Set the agent_configs for the sequence
        self.agent_configs = [
            research_agent.config,
            interview_agent.config,
            writing_agent.config,
        ]
