from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.mixins import RetrieverMixin
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent


class BaseRAGAgent(RetrieverMixin, Agent):
    """Base RAG agent that performs retrieval.

    This agent inherits from RetrieverMixin which provides:
    - Automatic conversion of VectorStoreConfig to VectorStoreRetrieverConfig
    - Class methods for creating agents from various sources

    Examples:
        ```python
        # Create from vector store config directly
        agent = BaseRAGAgent(engine=vector_store_config)

        # Create from documents
        agent = BaseRAGAgent.from_documents(
            documents=[Document(page_content="...")],
            embedding_model=embedding_config,
            name="my_rag_agent"
        )

        # Create from existing vector store
        agent = BaseRAGAgent.from_vectorstore(
            vector_store_config=vs_config,
            name="my_rag_agent"
        )
        ```
    """

    name: str = "Base RAG Agent"
    engine: BaseRetrieverConfig | VectorStoreConfig = Field(
        ...,
        description="Retriever Engine (accepts BaseRetrieverConfig or VectorStoreConfig)",
    )

    def build_graph(self) -> BaseGraph:
        """Build the RAG agent graph."""
        # Create base graph with proper name
        graph = BaseGraph(name="BaseRAGAgent")

        # Add the retrieval node
        retrieval_node = EngineNodeConfig(engine=self.engine, name="retrieval_node")
        graph.add_node("retrieval_node", retrieval_node)

        # Set up proper flow: START -> retrieval_node -> END
        graph.add_edge(START, "retrieval_node")
        graph.add_edge("retrieval_node", END)

        return graph
