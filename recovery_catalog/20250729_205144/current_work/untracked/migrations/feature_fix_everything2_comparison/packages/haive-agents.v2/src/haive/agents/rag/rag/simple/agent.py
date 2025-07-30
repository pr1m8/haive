"""Simple RAG Agent - Dead Simple Pattern.

Literally just: BaseRAGAgent → SimpleAgent with RAG prompt template.
Uses EnhancedMultiAgent for sequential execution.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document

# Use EnhancedMultiAgent V3 for the pattern
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.answer_generators.prompts import RAG_ANSWER_STANDARD
from haive.agents.simple.agent import SimpleAgent


class SimpleRAGAgent(EnhancedMultiAgent):
    """Dead simple RAG: BaseRAGAgent → SimpleAgent with built-in RAG prompt.

    This is literally what the user wanted:
    SimpleRAGAgent = EnhancedMulti([BaseRAGAgent, SimpleAgent], mode=Sequential)

    Key features:
    - BaseRAGAgent handles document retrieval
    - SimpleAgent has RAG_ANSWER_STANDARD prompt with {query} and {retrieved_documents}
    - Sequential execution via EnhancedMultiAgent
    - Simple factory methods for easy creation
    """

    def __init__(
        self,
        documents: list[Document] | None = None,
        llm_config: LLMConfig | None = None,
        name: str = "simple_rag",
        **kwargs
    ):
        """Initialize SimpleRAG with documents and LLM config.

        Args:
            documents: Documents to use for retrieval (if None, must set later)
            llm_config: LLM configuration for answer generation
            name: Agent name
            **kwargs: Additional arguments passed to EnhancedMultiAgent
        """
        # Create the agents
        agents = []

        # Create retrieval agent
        if documents is not None:
            retrieval_agent = BaseRAGAgent.from_documents(
                documents=documents, name="retriever"
            )
            agents.append(retrieval_agent)

        # Create answer agent with RAG prompt template
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=RAG_ANSWER_STANDARD,  # Has {query} and {retrieved_documents}
            ),
            name="answer_generator",
        )
        agents.append(answer_agent)

        # Initialize as EnhancedMultiAgent with sequential execution
        super().__init__(
            name=name, agents=agents, execution_mode="sequential", **kwargs
        )

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        name: str = "simple_rag",
        **kwargs
    ) -> "SimpleRAGAgent":
        """Create SimpleRAG from documents - factory method."""
        return cls(documents=documents, llm_config=llm_config, name=name, **kwargs)

    @classmethod
    def create_enhanced(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        performance_mode: bool = True,
        debug_mode: bool = False,
        name: str = "enhanced_simple_rag",
        **kwargs
    ) -> "SimpleRAGAgent":
        """Create enhanced SimpleRAG with V3 features enabled."""
        return cls(
            documents=documents,
            llm_config=llm_config,
            name=name,
            performance_mode=performance_mode,
            debug_mode=debug_mode,
            **kwargs
        )


# Create the pattern the user literally asked for
def create_simple_rag_pattern(
    documents: list[Document], llm_config: LLMConfig | None = None
):
    """Literally: SimpleRAGAgent = EnhancedMulti([BaseRAGAgent, SimpleAgent], mode=Sequential)"""
    # Create the agents
    base_rag = BaseRAGAgent.from_documents(documents=documents, name="retriever")

    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    simple_agent = SimpleAgent(
        engine=AugLLMConfig(
            llm_config=llm_config,
            prompt_template=RAG_ANSWER_STANDARD,  # Built-in prompt with retrieved_documents key
        ),
        name="answer_generator",
    )

    # This is exactly what the user asked for:
    return EnhancedMultiAgent.create(
        agents=[base_rag, simple_agent],
        name="simple_rag_pattern",
        execution_mode="sequential",
    )


# For even more direct usage - alias pattern
def SimpleRAG(documents: list[Document], llm_config: LLMConfig | None = None, **kwargs):
    """Direct function pattern: SimpleRAG(documents) -> working RAG agent"""
    return create_simple_rag_pattern(documents, llm_config)
