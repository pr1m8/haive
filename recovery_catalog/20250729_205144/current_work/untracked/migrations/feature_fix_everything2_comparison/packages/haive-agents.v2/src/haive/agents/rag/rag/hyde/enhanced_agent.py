"""Enhanced HyDE RAG Agent using Structured Output Pattern.

from typing import Any, Dict
This demonstrates the new pattern where any agent can be enhanced with structured
output by appending a SimpleAgent. This approach is more modular and follows the
principle of separation of concerns.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.models import HyDEResult
from haive.agents.rag.utils.structured_output_enhancer import create_hyde_enhancer
from haive.agents.simple.agent import SimpleAgent

# Improved HyDE generation prompt based on LangChain best practices
ENHANCED_HYDE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at generating hypothetical documents for enhanced retrieval.

Your task is to create a detailed, authoritative document that would ideally contain
the complete answer to the given question. This hypothetical document will be used
to improve document retrieval by bridging the semantic gap between queries and documents.

Key principles:
- Write as if you are creating a comprehensive reference document
- Include specific details, examples, and technical information
- Use domain-appropriate terminology and structure
- Make the document substantial enough to answer the question thoroughly
- Write in a factual, authoritative tone without mentioning it's hypothetical

The document should be the type that would appear in:
- Academic papers or textbooks for research questions
- Technical documentation for technical questions
- News articles for current events questions
- How-to guides for procedural questions

{format_instructions}""",
        ),
        (
            "human",
            """Generate a comprehensive hypothetical document that would contain the ideal answer to this question:

Question: {query}

Consider what type of document would best answer this question and write accordingly.""",
        ),
    ]
)


class EnhancedHyDERAGAgent(SequentialAgent):
    """Enhanced HyDE RAG Agent using the structured output enhancement pattern.

    This agent demonstrates the new modular approach where:
    1. Base agents handle core functionality (generation, retrieval)
    2. Enhancement agents add structured output processing
    3. The pattern is reusable across different RAG types

    Benefits:
    - Separation of concerns between generation and structure
    - Reusable enhancement pattern
    - Easier testing and debugging
    - Better maintainability
    """

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        use_enhancement_pattern: bool = True,
        **kwargs
    ):
        """Create Enhanced HyDE RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            embedding_model: Optional embedding model for vector store
            use_enhancement_pattern: Whether to use the new enhancement pattern
            **kwargs: Additional arguments

        Returns:
            EnhancedHyDERAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        if use_enhancement_pattern:
            return cls._create_with_enhancement_pattern(
                documents, llm_config, embedding_model, **kwargs
            )
        return cls._create_traditional_pattern(
            documents, llm_config, embedding_model, **kwargs
        )

    @classmethod
    def _create_with_enhancement_pattern(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None = None,
        **kwargs
    ):
        """Create using the new structured output enhancement pattern."""
        # Step 1: Base HyDE generation (focused on content, not structure)
        base_hyde_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ENHANCED_HYDE_PROMPT,
                output_key="hypothetical_content",  # Raw content output
            ),
            name="Base HyDE Generator",
        )

        # Step 2: Create structured output enhancement
        hyde_enhancer = create_hyde_enhancer()
        structured_hyde_agent = hyde_enhancer.create_enhancement_agent(
            llm_config=llm_config,
            context_prompt="""Analyze the generated hypothetical content and structure it appropriately.

Extract the hypothetical document, create a refined query for retrieval, and assess confidence.
Consider how well the hypothetical document would serve for semantic retrieval.""",
            agent_name="HyDE Structure Enhancer",
            include_state_context=True,
        )

        # Step 3: Enhanced retrieval using structured output
        enhanced_retriever = EnhancedHyDERetriever(
            documents=documents,
            embedding_model=embedding_model,
            name="Enhanced HyDE Retriever",
        )

        # Step 4: Final answer generation
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )

        return cls(
            agents=[
                base_hyde_generator,
                structured_hyde_agent,
                enhanced_retriever,
                answer_agent,
            ],
            name=kwargs.get("name", "Enhanced HyDE RAG Agent"),
            **kwargs
        )

    @classmethod
    def _create_traditional_pattern(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None = None,
        **kwargs
    ):
        """Create using traditional pattern for comparison."""
        # Traditional: structured output embedded in initial generation
        hyde_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ENHANCED_HYDE_PROMPT,
                structured_output_model=HyDEResult,
                structured_output_version="v1",
                output_key="hyde_result",
            ),
            name="Traditional HyDE Generator",
        )

        retriever = EnhancedHyDERetriever(
            documents=documents, embedding_model=embedding_model, name="HyDE Retriever"
        )

        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )

        return cls(
            agents=[hyde_generator, retriever, answer_agent],
            name=kwargs.get("name", "Traditional HyDE RAG Agent"),
            **kwargs
        )


class EnhancedHyDERetriever(Agent):
    """Enhanced retriever that handles both enhancement pattern and traditional outputs."""

    # Define as Pydantic fields
    documents: list[Document] = Field(
        default_factory=list, description="Documents for retrieval"
    )
    embedding_model: str | None = Field(
        default=None, description="Embedding model to use"
    )

    def __init__(
        self, documents: list[Document], embedding_model: str | None = None, **kwargs
    ):
        super().__init__(documents=documents, embedding_model=embedding_model, **kwargs)

    def build_graph(self) -> Any:
        """Build graph that adapts to both enhancement and traditional patterns."""
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from langgraph.graph import END, START

        graph = BaseGraph(name="EnhancedHyDERetriever")

        def adaptive_retrieval(state: dict[str, Any]) -> dict[str, Any]:
            """Adaptively retrieve based on available state information."""
            # Try to get structured HyDE result first (traditional pattern)
            hyde_result = state.get("hyderesult_result") or state.get("hyde_result")

            if hyde_result:
                # Use structured output
                if isinstance(hyde_result, dict):
                    hyp_doc = hyde_result.get("hypothetical_doc", "")
                    refined_query = hyde_result.get("refined_query", "")
                else:
                    hyp_doc = getattr(hyde_result, "hypothetical_doc", "")
                    refined_query = getattr(hyde_result, "refined_query", "")

                # Use refined query if available, otherwise hypothetical doc
                retrieval_query = refined_query or hyp_doc
            else:
                # Fall back to raw hypothetical content (enhancement pattern)
                retrieval_query = state.get(
                    "hypothetical_content", state.get("query", "")
                )

            # Create base retriever on-demand
            base_retriever = BaseRAGAgent.from_documents(
                documents=self.documents,
                embedding_model=self.embedding_model,
                name="On-Demand Base Retrievef",
            )

            # Perform retrieval
            try:
                result = base_retriever.run({"query": retrieval_query})
                docs = []

                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]

                return {
                    "retrieved_documents": docs,
                    "retrieval_query_used": retrieval_query,
                    "retrieval_method": "hyde_enhanced",
                    "num_retrieved": len(docs),
                }

            except Exception as e:
                # Fallback to original query
                result = base_retriever.run({"query": state.get("query", "")})
                docs = []

                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]

                return {
                    "retrieved_documents": docs,
                    "retrieval_query_used": state.get("query", ""),
                    "retrieval_method": "fallback",
                    "num_retrieved": len(docs),
                    "retrieval_error": str(e),
                }

        graph.add_node("adaptive_retrieve", adaptive_retrieval)
        graph.add_edge(START, "adaptive_retrieve")
        graph.add_edge("adaptive_retrieve", END)

        return graph


# Factory functions for easy creation
def create_enhanced_hyde_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    use_enhancement_pattern: bool = True,
    **kwargs
) -> EnhancedHyDERAGAgent:
    """Create an Enhanced HyDE RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        use_enhancement_pattern: Whether to use the new enhancement pattern
        **kwargs: Additional arguments

    Returns:
        Configured Enhanced HyDE RAG agent
    """
    return EnhancedHyDERAGAgent.from_documents(
        documents=documents,
        llm_config=llm_config,
        use_enhancement_pattern=use_enhancement_pattern,
        **kwargs
    )


# Demonstration of the pattern
def demonstrate_enhancement_vs_traditional() -> Dict[str, Any]:
    """Demonstrate the difference between enhancement and traditional patterns."""
    from langchain_core.documents import Document

    # Sample documents
    docs = [
        Document(
            page_content="Machine learning uses algorithms to learn patterns from data."
        ),
        Document(
            page_content="Neural networks are inspired by biological neural networks."
        ),
        Document(
            page_content="Deep learning uses multiple layers for complex pattern recognition."
        ),
    ]

    # Enhanced pattern (separation of concerns)
    enhanced_agent = create_enhanced_hyde_agent(
        documents=docs, use_enhancement_pattern=True, name="Enhancement Pattern HyDE"
    )

    # Traditional pattern (embedded structure)
    traditional_agent = create_enhanced_hyde_agent(
        documents=docs, use_enhancement_pattern=False, name="Traditional Pattern HyDE"
    )

    return {
        "enhanced": enhanced_agent,
        "traditional": traditional_agent,
        "pattern_benefits": [
            "Modular design with reusable enhancement components",
            "Clearer separation between generation and structure",
            "Easier to test individual components",
            "More flexible prompt engineering",
            "Better error handling and debugging",
        ],
    }
