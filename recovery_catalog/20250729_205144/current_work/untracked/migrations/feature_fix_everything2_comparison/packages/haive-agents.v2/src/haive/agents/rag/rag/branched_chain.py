"""Branched RAG using ChainAgent.

RAG system that branches into multiple specialized retrieval paths based on query type,
then merges results for comprehensive answers.
"""

from enum import Enum
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain import ChainAgent, flow_with_edges


class QueryType(str, Enum):
    """Types of queries for branching."""

    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PROCEDURAL = "procedural"


class QueryClassification(BaseModel):
    """Query classification result."""

    primary_type: QueryType = Field(description="Primary query type")
    secondary_type: QueryType | None = Field(
        default=None, description="Secondary type if applicable"
    )
    complexity: Literal["simple", "medium", "complex"] = Field(
        description="Query complexity"
    )
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence")


class BranchResult(BaseModel):
    """Result from a retrieval branch."""

    branch_type: str = Field(description="Type of branch")
    retrieved_docs: list[str] = Field(description="Retrieved documents")
    branch_answer: str = Field(description="Answer from this branch")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score")


class MergedResult(BaseModel):
    """Final merged result."""

    primary_answer: str = Field(description="Primary answer")
    supporting_evidence: list[str] = Field(
        description="Supporting evidence from branches"
    )
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")
    sources_used: list[str] = Field(description="Sources used")


def create_branched_rag_chain(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    name: str = "Branched RAG",
) -> ChainAgent:
    """Create a branched RAG system using ChainAgent."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Step 1: Query classifier
    classifier = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Classify the query type and complexity:
            - factual: Seeking specific facts or information
            - analytical: Requiring analysis, comparison, or reasoning
            - creative: Seeking ideas, brainstorming, or creative solutions
            - procedural: Looking for step-by-step instructions or processes

            Complexity: simple (direct lookup), medium (some analysis), complex (multi-step reasoning)""",
                ),
                ("human", "Query: {query}"),
            ]
        ),
        structured_output_model=QueryClassification,
        output_key="classification",
    )

    # Step 2: Factual retrieval branch
    def factual_branch(state: dict[str, Any]) -> dict[str, Any]:
        """Factual information retrieval branch."""
        state.get("classification", {})
        query = state.get("query", "")

        # Focus on exact facts and specific information
        relevant_docs = [
            doc
            for doc in documents
            if any(
                word.lower() in doc.page_content.lower() for word in query.split()[:5]
            )
        ][:3]

        # Extract precise facts
        facts = [doc.page_content for doc in relevant_docs]
        answer = f"Based on the documents: {'; '.join(facts[:2])}"

        return {
            "factual_result": BranchResult(
                branch_type="factual",
                retrieved_docs=facts,
                branch_answer=answer,
                relevance_score=0.9 if relevant_docs else 0.3,
            )
        }

    # Step 3: Analytical retrieval branch
    analytical_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Analyze and synthesize information for deeper insights"),
                (
                    "human",
                    """Query: {query}
            Available context: {documents_context}

            Provide analytical insights and reasoning.""",
                ),
            ]
        ),
        output_key="analytical_answer",
    )

    def analytical_processor(state: dict[str, Any]) -> dict[str, Any]:
        """Process analytical branch results."""
        analytical_answer = state.get("analytical_answer", "")

        return {
            "analytical_result": BranchResult(
                branch_type="analytical",
                retrieved_docs=[doc.page_content for doc in documents[:2]],
                branch_answer=analytical_answer,
                relevance_score=0.8,
            )
        }

    # Step 4: Creative retrieval branch
    creative_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Generate creative solutions and innovative ideas"),
                (
                    "human",
                    """Query: {query}
            Context for inspiration: {documents_context}

            Provide creative and innovative responses.""",
                ),
            ]
        ),
        output_key="creative_answer",
    )

    def creative_processor(state: dict[str, Any]) -> dict[str, Any]:
        """Process creative branch results."""
        creative_answer = state.get("creative_answer", "")

        return {
            "creative_result": BranchResult(
                branch_type="creative",
                retrieved_docs=[doc.page_content for doc in documents[:2]],
                branch_answer=creative_answer,
                relevance_score=0.7,
            )
        }

    # Step 5: Procedural retrieval branch
    procedural_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Extract step-by-step procedures and processes"),
                (
                    "human",
                    """Query: {query}
            Available procedures: {documents_context}

            Provide clear, step-by-step instructions.""",
                ),
            ]
        ),
        output_key="procedural_answer",
    )

    def procedural_processor(state: dict[str, Any]) -> dict[str, Any]:
        """Process procedural branch results."""
        procedural_answer = state.get("procedural_answer", "")

        return {
            "procedural_result": BranchResult(
                branch_type="procedural",
                retrieved_docs=[doc.page_content for doc in documents[:2]],
                branch_answer=procedural_answer,
                relevance_score=0.85,
            )
        }

    # Step 6: Context preparation for branches
    def prepare_context(state: dict[str, Any]) -> dict[str, Any]:
        """Prepare document context for branches."""
        context = "\n\n".join([doc.page_content for doc in documents[:5]])
        return {"documents_context": context}

    # Step 7: Results merger
    merger = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Merge results from multiple retrieval branches into a comprehensive answer.
            Prioritize based on query type and relevance scores.""",
                ),
                (
                    "human",
                    """Original Query: {query}
            Query Classification: {classification}

            Branch Results:
            - Factual: {factual_result}
            - Analytical: {analytical_result}
            - Creative: {creative_result}
            - Procedural: {procedural_result}

            Create a comprehensive, well-structured response.""",
                ),
            ]
        ),
        structured_output_model=MergedResult,
        output_key="merged_result",
    )

    # Step 8: Final response generator
    final_generator = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Generate the final user-facing response"),
                (
                    "human",
                    """Query: {query}
            Merged Analysis: {merged_result}

            Provide a clear, comprehensive response.""",
                ),
            ]
        ),
        output_key="response",
    )

    # Build the branched chain
    return flow_with_edges(
        [
            classifier,  # 0: Classify query
            prepare_context,  # 1: Prepare context
            factual_branch,  # 2: Factual branch
            analytical_branch,  # 3: Analytical branch
            analytical_processor,  # 4: Process analytical
            creative_branch,  # 5: Creative branch
            creative_processor,  # 6: Process creative
            procedural_branch,  # 7: Procedural branch
            procedural_processor,  # 8: Process procedural
            merger,  # 9: Merge all results
            final_generator,  # 10: Final response
        ],
        # Sequential flow through classifier and context prep
        "0->1",
        # Branch out to all retrieval strategies
        "1->2",
        "1->3",
        "1->5",
        "1->7",
        # Process branch results
        "3->4",
        "5->6",
        "7->8",
        # All branches flow to merger
        "2->9",
        "4->9",
        "6->9",
        "8->9",
        # Merger flows to final generator
        "9->10",
    )


def create_adaptive_branched_rag(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Create an adaptive branched RAG that selects branches based on query type."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Classifier
    classifier = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Classify query type: factual, analytical, creative, or procedural",
                ),
                ("human", "{query}"),
            ]
        ),
        output_key="query_type",
    )

    # Branch-specific processors
    factual_processor = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Extract precise factual information"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="response",
    )

    analytical_processor = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Provide analytical insights and reasoning"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="response",
    )

    creative_processor = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Generate creative solutions and ideas"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="response",
    )

    procedural_processor = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Provide step-by-step procedures"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="response",
    )

    # Context preparation
    def add_context(state: dict[str, Any]) -> dict[str, Any]:
        context = "\n\n".join([doc.page_content for doc in documents[:3]])
        return {"context": context}

    # Conditional routing based on query type
    return flow_with_edges(
        [
            classifier,  # 0
            add_context,  # 1
            factual_processor,  # 2
            analytical_processor,  # 3
            creative_processor,  # 4
            procedural_processor,  # 5
        ],
        "0->1",  # Always prepare context
        (
            1,
            {  # Route based on query type
                "factual": 2,
                "analytical": 3,
                "creative": 4,
                "procedural": 5,
            },
            lambda s: s.get("query_type", "factual").lower(),
        ),
    )


def create_parallel_branched_rag(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Create a parallel branched RAG that runs all branches simultaneously."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Context preparation
    def prepare_context(state: dict[str, Any]) -> dict[str, Any]:
        context = "\n\n".join([doc.page_content for doc in documents[:5]])
        return {"context": context}

    # All branches run in parallel
    factual_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Extract factual information"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="factual_response",
    )

    analytical_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Provide analytical insights"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="analytical_response",
    )

    creative_branch = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Generate creative ideas"),
                ("human", "Query: {query}\nContext: {context}"),
            ]
        ),
        output_key="creative_response",
    )

    # Final synthesizer
    synthesizer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Synthesize all branch responses into a comprehensive answer",
                ),
                (
                    "human",
                    """Query: {query}
            Factual: {factual_response}
            Analytical: {analytical_response}
            Creative: {creative_response}

            Create final response.""",
                ),
            ]
        ),
        output_key="response",
    )

    # Parallel execution
    return flow_with_edges(
        [
            prepare_context,  # 0
            factual_branch,  # 1
            analytical_branch,  # 2
            creative_branch,  # 3
            synthesizer,  # 4
        ],
        # All branches run in parallel from context
        "0->1",
        "0->2",
        "0->3",
        # All flow to synthesizer
        "1->4",
        "2->4",
        "3->4",
    )


# I/O schema
def get_branched_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for branched RAG."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "classification",
            "factual_result",
            "analytical_result",
            "creative_result",
            "procedural_result",
            "merged_result",
            "response",
            "messages",
        ],
    }
