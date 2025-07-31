"""Base_Agent core module.

This module provides base agent functionality for the Haive framework.

Classes:
    BaseRAGAgent: BaseRAGAgent implementation.

Functions:
    retrieve: Retrieve functionality.
    generate_answer: Generate Answer functionality.
    setup_workflow: Setup Workflow functionality.
"""

import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.types import Command

from haive.agents.rag.base.config import BaseRAGConfig

logging.basicConfig(level=logging.DEBUG)


@register_agent(BaseRAGConfig)
class BaseRAGAgent(Agent[BaseRAGConfig]):
    """Simple base RAG agent with retrieve and generate functionality."""

    def retrieve(self, state: dict[str, Any]):
        """Retrieve documents based on the query."""
        query = state.query
        documents = self.config.retriever_engine.create_retriever().invoke(query)
        return Command(update={"retrieved_documents": documents})

    def generate_answer(self, state: dict[str, Any]):
        """Generate an answer based on retrieved documents."""
        query = state.query
        documents = state.retrieved_documents
        if not documents:
            return {
                "answer": "I couldn't find any relevant documents to answer your query."
            }
        context = "\n\n".join([doc.page_content for doc in documents])
        answer = self.config.engine.create_runnable().invoke(
            {"query": query, "context": context}
        )
        return Command(update={"answer": answer})

    def setup_workflow(self) -> None:
        """Set up the RAG workflow for this agent."""
        gb = DynamicGraph(state_schema=self.state_schema)
        gb.add_node("retrieve", self.retrieve)
        self.graph = gb.build()


"""
def test_base_rag_agent():
    # Initialize the WebBaseLoader with the URL for a Wiki page
    loader = WebBaseLoader("https://en.wikipedia.org/wiki/OpenAI")
    documents = loader.load()

    # Create the vector store config from the documents
    vector_store_config = VectorStoreConfig.create_vs_config_from_documents(documents)

    # Set up the retriever engine (this would ideally be provided in the RAG configuration)
    retriever = vector_store_config.create_retriever()

    # Set up the test configuration for the BaseRAGAgent (for example, using mock configurations)
    base_rag_config = BaseRAGConfig(
        name="test_agent",
        retriever_engine=retriever,
        engine=AugLLMConfig(),
    )

    # Initialize the agent with the configuration
    agent = BaseRAGAgent(config=base_rag_config)

    # Define a simple query (such as querying OpenAI)
    query = "What is OpenAI?"

    # Create a mock state object (you may have to define this based on your actual system)
    state = {
        "query": query,
    }

    # Run the agent to retrieve and generate an answer
    result = agent.run(input_data=query)

    # Print or log the result for verification
    logging.info(f"Result: {result}")

    assert "answer" in result, "Answer not found in the result"

# Run the test
test_base_rag_agent()
"""
