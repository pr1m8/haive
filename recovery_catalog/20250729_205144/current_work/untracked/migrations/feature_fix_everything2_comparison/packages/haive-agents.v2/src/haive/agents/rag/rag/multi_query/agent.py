"""Multi-Query RAG Agent.

Improves recall through query diversification.
Generates multiple query variations and retrieves from all.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent


class QueryVariations(BaseModel):
    """Structured output for query variations."""

    specific_query: str = Field(description="More specific version of the query")
    broader_query: str = Field(description="Broader conceptual version")
    alternative_query: str = Field(description="Alternative phrasing of the query")


QUERY_EXPANSION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at query expansion for improved information retrieval.
Generate diverse query variations that capture different aspects and phrasings.""",
        ),
        (
            "human",
            """Generate 3 different versions of this query to improve search coverage:

Original Query: {query}

Create:
1. A more specific version that narrows the focus
2. A broader version that captures related concepts
3. An alternative phrasing that might match different documents

Return the three query variations.""",
        ),
    ]
)


class MultiRetrievalAgent(Agent):
    """Agent that performs parallel retrieval with multiple queries."""

    name: str = "Multi-Query Retriever"
    base_retriever: BaseRAGAgent = Field(..., description="Base retriever to use")

    def build_graph(self) -> BaseGraph:
        """Build graph that retrieves with multiple queries in parallel."""
        graph = BaseGraph(name="MultiRetriever")

        def expand_and_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            """Retrieve documents for all query variations."""
            # Get query variations
            variations = state.get("query_variations", {})
            original_query = state.get("query", "")

            # Collect all queries
            all_queries = [original_query]
            if isinstance(variations, dict):
                all_queries.extend(
                    [
                        variations.get("specific_query", ""),
                        variations.get("broader_query", ""),
                        variations.get("alternative_query", ""),
                    ]
                )

            # Remove empty queries
            all_queries = [q for q in all_queries if q.strip()]

            # Retrieve for each query
            doc_scores = {}  # Track document scores across queries

            for query in all_queries:
                # Use the base retriever's engine
                result = self.base_retriever.engine.invoke({"query": query})

                # Extract documents from result
                docs = result.get("retrieved_documents", [])

                # Track document occurrences for ranking
                for i, doc in enumerate(docs):
                    doc_id = hash(doc.page_content)
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = {"doc": doc, "score": 0, "positions": []}
                    # Higher score for documents appearing in multiple queries
                    doc_scores[doc_id]["score"] += 1
                    # Bonus for higher ranking positions
                    doc_scores[doc_id]["positions"].append(1 / (i + 1))

            # Rank documents by combined score
            ranked_docs = sorted(
                doc_scores.values(),
                key=lambda x: x["score"] + sum(x["positions"]),
                reverse=True,
            )

            # Extract unique documents
            unique_docs = [item["doc"] for item in ranked_docs]

            return {
                "retrieved_documents": unique_docs[:10],  # Top 10 documents
                "retrieval_queries": all_queries,
                "retrieval_stats": {
                    "total_queries": len(all_queries),
                    "unique_documents": len(unique_docs),
                    "top_score": ranked_docs[0]["score"] if ranked_docs else 0,
                },
            }

        # Add retrieval node
        graph.add_node("multi_retrieve", expand_and_retrieve)

        # Connect: START -> multi_retrieve -> END
        graph.add_edge(START, "multi_retrieve")
        graph.add_edge("multi_retrieve", END)

        return graph


class MultiQueryRAGAgent(SequentialAgent):
    """Multi-Query RAG with query expansion for improved recall."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        **kwargs
    ):
        """Create Multi-Query RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            embedding_model: Optional embedding model for vector store
            **kwargs: Additional arguments

        Returns:
            MultiQueryRAGAgent instance
        """
        # Step 1: Query expansion agent
        query_expander = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=QUERY_EXPANSION_PROMPT,
                structured_output_model=QueryVariations,
                output_key="query_variations",
            ),
            name="Query Expander",
        )

        # Step 2: Create base retriever
        base_retriever = BaseRAGAgent.from_documents(
            documents=documents, embedding_model=embedding_model, name="Base Retriever"
        )

        # Step 3: Multi-query retriever
        multi_retriever = MultiRetrievalAgent(
            base_retriever=base_retriever, name="Multi-Query Retriever"
        )

        # Step 4: Answer generation
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
            agents=[query_expander, multi_retriever, answer_agent],
            name=kwargs.get("name", "Multi-Query RAG Agent"),
            **kwargs
        )
