"""Step-Back Prompting RAG Agents.

from typing import Any
Implementation of step-back prompting for abstract reasoning.
Generates broader conceptual queries for enhanced context retrieval.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class StepBackQuery(BaseModel):
    """Step-back query generation result."""

    original_query: str = Field(description="Original specific query")
    step_back_query: str = Field(description="Abstract/general step-back query")

    abstraction_level: str = Field(description="Level of abstraction applied")
    conceptual_focus: str = Field(description="Main conceptual focus")
    broader_context: str = Field(description="Broader context to explore")

    reasoning: str = Field(description="Why this step-back query was generated")
    expected_benefit: str = Field(
        description="Expected benefit from step-back approach"
    )


class StepBackResult(BaseModel):
    """Combined results from step-back retrieval."""

    original_documents: list[str] = Field(description="Documents from original query")
    step_back_documents: list[str] = Field(description="Documents from step-back query")

    conceptual_coverage: float = Field(
        ge=0.0, le=1.0, description="Conceptual coverage score"
    )
    context_enhancement: float = Field(
        ge=0.0, le=1.0, description="Context enhancement score"
    )

    integration_strategy: str = Field(description="How to integrate the contexts")
    synthesis_approach: str = Field(description="Recommended synthesis approach")


# Enhanced prompts for step-back reasoning
STEP_BACK_GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at step-back prompting for enhanced reasoning and retrieval.

Step-back prompting involves taking a specific question and generating a more general,
abstract question that explores the underlying principles, concepts, or broader context.

**STEP-BACK PRINCIPLES:**
1. **Abstraction**: Move from specific to general concepts
2. **Conceptual Focus**: Identify underlying principles
3. **Broader Context**: Explore related domains and background
4. **Enhanced Understanding**: Build foundational knowledge first

**EXAMPLES:**
- Specific: "Why does my LangGraph agent return error X?"
  Step-back: "How does error handling work in LangGraph agents?"

- Specific: "What was Apple's revenue in Q3 2023?"
  Step-back: "What are Apple's financial performance metrics and reporting patterns?"

- Specific: "How do I fix this Python import error?"
  Step-back: "How does Python's import system work and what are common import issues?"

The step-back query should provide conceptual foundation for better understanding the specific question.""",
        ),
        (
            "human",
            """Generate a step-back query for enhanced reasoning:

**Specific Query:** {query}

**Context (if available):** {context}

Create a step-back query that:
1. Abstracts to underlying concepts and principles
2. Provides broader context and background
3. Enables better foundational understanding
4. Enhances the ability to answer the specific query

Provide the step-back query with detailed reasoning.""",
        ),
    ]
)


STEP_BACK_SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at synthesizing information from step-back prompting results.

You have access to:
1. **Original Context**: Documents retrieved for the specific query
2. **Step-Back Context**: Documents retrieved for the broader/abstract query

Use the step-back context to provide foundational understanding, then apply that
knowledge to give a comprehensive answer to the original specific query.

**SYNTHESIS STRATEGY:**
1. Start with foundational concepts from step-back context
2. Build understanding of underlying principles
3. Apply this foundation to the specific question
4. Provide a comprehensive, well-grounded answer""",
        ),
        (
            "human",
            """Answer the specific query using step-back enhanced context:

**Original Query:** {query}
**Step-Back Query:** {step_back_query}

**Original Context (specific):**
{original_documents}

**Step-Back Context (foundational):**
{step_back_documents}

**Integration Guidance:**
- Conceptual Coverage: {conceptual_coverage}
- Context Enhancement: {context_enhancement}
- Integration Strategy: {integration_strategy}

Provide a comprehensive answer that leverages both the foundational step-back context
and the specific context to thoroughly address the original query.""",
        ),
    ]
)


class StepBackQueryGeneratorAgent(Agent):
    """Agent that generates step-back queries for abstract reasoning."""

    name: str = "Step-Back Query Generator"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        abstraction_level: str = "moderate",
        **kwargs,
    ):
        """Initialize step-back query generator.

        Args:
            llm_config: LLM configuration
            abstraction_level: Level of abstraction ("low", "moderate", "high")
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.abstraction_level = abstraction_level
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build step-back query generation graph."""
        graph = BaseGraph(name="StepBackQueryGenerator")

        # Create step-back generation engine
        generation_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=STEP_BACK_GENERATOR_PROMPT,
            structured_output_model=StepBackQuery,
            output_key="step_back_query_result",
        )

        def generate_step_back_query(state: dict[str, Any]) -> dict[str, Any]:
            """Generate step-back query for broader context."""
            query = getattr(state, "query", "")
            context = getattr(state, "context", "") or getattr(
                state, "retrieved_documents", ""
            )

            # Format context
            if isinstance(context, list):
                context_str = (
                    "\n".join(
                        [
                            f"Doc {i+1}: {doc.page_content[:200]}..."
                            for i, doc in enumerate(context[:3])
                        ]
                    )
                    if context
                    else "No context available"
                )
            else:
                context_str = (
                    str(context)[:500] + "..."
                    if len(str(context)) > 500
                    else str(context)
                )

            # Generate step-back query
            step_back_result = generation_engine.invoke(
                {"query": query, "context": context_str}
            )

            return {
                "step_back_query_result": step_back_result,
                "step_back_query": step_back_result.step_back_query,
                "original_query": step_back_result.original_query,
                "abstraction_level": step_back_result.abstraction_level,
                "conceptual_focus": step_back_result.conceptual_focus,
                "broader_context": step_back_result.broader_context,
                "step_back_reasoning": step_back_result.reasoning,
            }

        graph.add_node("generate_step_back", generate_step_back_query)
        graph.add_edge(START, "generate_step_back")
        graph.add_edge("generate_step_back", END)

        return graph


class DualRetrievalAgent(Agent):
    """Agent that performs both original and step-back retrieval."""

    name: str = "Dual Retrieval"

    def __init__(
        self,
        documents: list[Document],
        embedding_model: str | None = None,
        max_docs_each: int = 5,
        **kwargs,
    ):
        """Initialize dual retrieval agent.

        Args:
            documents: Documents for retrieval
            embedding_model: Embedding model
            max_docs_each: Max docs to retrieve for each query
            **kwargs: Additional arguments
        """
        self.documents = documents
        self.embedding_model = embedding_model
        self.max_docs_each = max_docs_each
        super().__init__(**kwargs)

        # Create base retriever
        self.base_retriever = BaseRAGAgent.from_documents(
            documents=documents, embedding_model=embedding_model, name="Base Retriever"
        )

    def build_graph(self) -> BaseGraph:
        """Build dual retrieval graph."""
        graph = BaseGraph(name="DualRetrieval")

        def dual_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            """Retrieve for both original and step-back queries."""
            original_query = getattr(state, "original_query", "") or getattr(
                state, "query", ""
            )
            step_back_query = getattr(state, "step_back_query", "")

            # Retrieve for original query
            original_docs = []
            if original_query:
                try:
                    result = self.base_retriever.run({"query": original_query})
                    if hasattr(result, "retrieved_documents"):
                        original_docs = result.retrieved_documents[: self.max_docs_each]
                    elif isinstance(result, dict) and "retrieved_documents" in result:
                        original_docs = result["retrieved_documents"][
                            : self.max_docs_each
                        ]
                except Exception as e:
                    logger.warning(f"Original retrieval failed: {e}")

            # Retrieve for step-back query
            step_back_docs = []
            if step_back_query:
                try:
                    result = self.base_retriever.run({"query": step_back_query})
                    if hasattr(result, "retrieved_documents"):
                        step_back_docs = result.retrieved_documents[
                            : self.max_docs_each
                        ]
                    elif isinstance(result, dict) and "retrieved_documents" in result:
                        step_back_docs = result["retrieved_documents"][
                            : self.max_docs_each
                        ]
                except Exception as e:
                    logger.warning(f"Step-back retrieval failed: {e}")

            # Combine documents (step-back first for foundational context)
            combined_docs = step_back_docs + original_docs

            # Calculate coverage metrics
            original_content = {doc.page_content[:100] for doc in original_docs}
            step_back_content = {doc.page_content[:100] for doc in step_back_docs}

            overlap = len(original_content.intersection(step_back_content))
            total_unique = len(original_content.union(step_back_content))

            conceptual_coverage = len(step_back_docs) / max(self.max_docs_each, 1)
            context_enhancement = (total_unique - overlap) / max(total_unique, 1)

            # Build step-back result
            step_back_result = StepBackResult(
                original_documents=[
                    doc.page_content[:200] + "..." for doc in original_docs
                ],
                step_back_documents=[
                    doc.page_content[:200] + "..." for doc in step_back_docs
                ],
                conceptual_coverage=conceptual_coverage,
                context_enhancement=context_enhancement,
                integration_strategy=(
                    "foundational_first" if step_back_docs else "direct"
                ),
                synthesis_approach=(
                    "step_back_enhanced" if step_back_docs else "standard"
                ),
            )

            return {
                "original_documents": original_docs,
                "step_back_documents": step_back_docs,
                "retrieved_documents": combined_docs,
                "step_back_result": step_back_result,
                "conceptual_coverage": conceptual_coverage,
                "context_enhancement": context_enhancement,
                "has_step_back_context": len(step_back_docs) > 0,
            }

        graph.add_node("dual_retrieve", dual_retrieve)
        graph.add_edge(START, "dual_retrieve")
        graph.add_edge("dual_retrieve", END)

        return graph


class StepBackRAGAgent(SequentialAgent):
    """Complete Step-Back RAG agent with abstract reasoning."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        abstraction_level: str = "moderate",
        max_docs_each: int = 5,
        **kwargs,
    ):
        """Create Step-Back RAG agent from documents.

        Args:
            documents: Documents to index
            llm_config: LLM configuration
            embedding_model: Embedding model for retrieval
            abstraction_level: Level of abstraction for step-back queries
            max_docs_each: Max docs to retrieve for each query type
            **kwargs: Additional arguments

        Returns:
            StepBackRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: Generate step-back query
        step_back_generator = StepBackQueryGeneratorAgent(
            llm_config=llm_config,
            abstraction_level=abstraction_level,
            name="Step-Back Generator",
        )

        # Step 2: Dual retrieval (original + step-back)
        dual_retriever = DualRetrievalAgent(
            documents=documents,
            embedding_model=embedding_model,
            max_docs_each=max_docs_each,
            name="Dual Retriever",
        )

        # Step 3: Step-back synthesis
        synthesis_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=STEP_BACK_SYNTHESIS_PROMPT
            ),
            name="Step-Back Synthesizer",
        )

        return cls(
            agents=[step_back_generator, dual_retriever, synthesis_agent],
            name=kwargs.get("name", "Step-Back RAG Agent"),
            **kwargs,
        )


# Factory function
def create_step_back_rag_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    reasoning_depth: str = "moderate",
    **kwargs,
) -> StepBackRAGAgent:
    """Create a Step-Back RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        reasoning_depth: Depth of reasoning ("shallow", "moderate", "deep")
        **kwargs: Additional arguments

    Returns:
        Configured Step-Back RAG agent
    """
    # Adjust parameters based on reasoning depth
    if reasoning_depth == "shallow":
        kwargs.setdefault("abstraction_level", "low")
        kwargs.setdefault("max_docs_each", 3)
    elif reasoning_depth == "deep":
        kwargs.setdefault("abstraction_level", "high")
        kwargs.setdefault("max_docs_each", 7)
    else:  # moderate
        kwargs.setdefault("abstraction_level", "moderate")
        kwargs.setdefault("max_docs_each", 5)

    return StepBackRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_step_back_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Step-Back RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "step_back_query_result",
            "step_back_query",
            "original_query",
            "abstraction_level",
            "conceptual_focus",
            "broader_context",
            "step_back_reasoning",
            "original_documents",
            "step_back_documents",
            "retrieved_documents",
            "step_back_result",
            "conceptual_coverage",
            "context_enhancement",
            "has_step_back_context",
            "response",
            "messages",
        ],
    }
