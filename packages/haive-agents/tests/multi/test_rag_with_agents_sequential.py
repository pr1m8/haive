"""Test RAG with multiple agents in sequential execution.

This test demonstrates:
1. BaseRAGAgent for retrieval from documents
2. SimpleAgent for answering based on retrieved context
3. Sequential execution with MultiAgentState and AgentNodeV3
"""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
)
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config, create_agent_node_v3
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

# Fix forward reference issue
MultiAgentState.model_rebuild()
AgentNodeV3Config.model_rebuild()


class RAGState(StateSchema):
    """State for RAG agent."""

    messages: list = Field(default_factory=list)
    query: str = Field(default="")
    context: list[str] = Field(default_factory=list)
    retrieved_documents: list[Document] = Field(default_factory=list)


class AnswerState(StateSchema):
    """State for answer agent."""

    messages: list = Field(default_factory=list)
    context: list[str] = Field(default_factory=list)
    answer: str = Field(default="")


# Create test documents
def create_test_documents():
    """Create sample documents for testing."""
    return [
        Document(
            page_content="The Haive framework is a powerful AI agent system built on top of LangGraph.",
            metadata={"source": "haive_intro.txt", "page": 1},
        ),
        Document(
            page_content="Haive agents can be composed hierarchically without schema flattening. Each agent maintains its own state schema independently.",
            metadata={"source": "haive_architecture.txt", "page": 1},
        ),
        Document(
            page_content="The MultiAgentState pattern allows agents to be stored as first-class fields, enabling proper type safety and hierarchical access.",
            metadata={"source": "haive_patterns.txt", "page": 1},
        ),
        Document(
            page_content="RAG (Retrieval Augmented Generation) agents in Haive can retrieve relevant documents and use them as context for generation.",
            metadata={"source": "haive_rag.txt", "page": 1},
        ),
        Document(
            page_content="The AgentNodeV3 system provides state projection, ensuring each agent only sees its expected schema without global state pollution.",
            metadata={"source": "haive_nodes.txt", "page": 1},
        ),
    ]


async def test_rag_with_agents_sequential():
    """Test RAG agent retrieving documents followed by answer agent."""

    # Step 1: Create test documents
    documents = create_test_documents()

    # Step 2: Create embedding model configuration

    # Create HuggingFace embedding configuration
    embedding_config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )


    # Step 3: Create vector store config with documents
    vector_store_config = VectorStoreConfig(
        name="test_vectorstore",
        documents=documents,
        embedding_model=embedding_config,  # Still use config, VectorStoreConfig handles instantiation
        vector_store_provider=VectorStoreProvider.FAISS,
    )

    # Step 4: Create agents

    # RAG agent for retrieval
    rag_agent = BaseRAGAgent(
        name="retriever",
        engine=vector_store_config,
        state_schema=RAGState,
        use_prebuilt_base=True,
        debug=True,
    )

    # Simple agent for answering
    answer_agent = SimpleAgent(
        name="answerer",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a helpful assistant. Answer questions based on the provided context. If the context doesn't contain relevant information, say so.",
        ),
        state_schema=AnswerState,
        use_prebuilt_base=True,
        debug=True,
    )

    # Step 5: Create MultiAgentState

    # Initial query
    query = "What is the MultiAgentState pattern in Haive?"

    state = MultiAgentState(
        agents=[rag_agent, answer_agent], messages=[HumanMessage(content=query)]
    )

    # Set the query in RAG agent's state
    state.update_agent_state("retriever", {"query": query})


    # Step 6: Create AgentNodeV3 configurations

    retriever_node = create_agent_node_v3(
        agent_name="retriever",
        name="retrieve_context",
        command_goto="answer_question",
        shared_fields=["messages", "query"],  # Share query with retriever
    )

    answerer_node = create_agent_node_v3(
        agent_name="answerer",
        name="answer_question",
        command_goto=None,  # End of sequence
        shared_fields=["messages", "context"],  # Share context with answerer
    )


    # Step 7: Execute retriever node
    state.display_debug_info("Before Retrieval")

    try:
        # Execute with debug config
        debug_config = {"debug": True}
        retriever_result = retriever_node(state, config=debug_config)


        # Apply retriever updates to state
        if hasattr(retriever_result, "update") and retriever_result.update:
            for key, value in retriever_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)

        # Extract context from retrieved documents
        retriever_state = state.get_agent_state("retriever")
        if "retrieved_documents" in retriever_state:
            # Convert Document objects to strings for the answerer
            context_strings = []
            for doc in retriever_state["retrieved_documents"]:
                if hasattr(doc, "page_content"):
                    context_strings.append(doc.page_content)
                else:
                    context_strings.append(str(doc))

            # Share context with answerer
            state.update_agent_state("answerer", {"context": context_strings})

            # Also update the retriever's context field for consistency
            state.update_agent_state("retriever", {"context": context_strings})

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False

    # Step 8: Execute answerer node
    state.display_debug_info("Before Answer Generation")

    try:
        # Execute with debug config
        answerer_result = answerer_node(state, config=debug_config)


        # Apply answerer updates to state
        if hasattr(answerer_result, "update") and answerer_result.update:
            for key, value in answerer_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)


    except Exception as e:
        import traceback

        traceback.print_exc()
        return False

    # Step 9: Display results
    state.display_debug_info("Final State After RAG")

    # Display the answer
    answerer_state = state.get_agent_state("answerer")
    retriever_state = state.get_agent_state("retriever")

    if "context" in retriever_state:
        for i, ctx in enumerate(retriever_state["context"][:3]):  # Show first 3
            pass

    if "messages" in answerer_state and len(answerer_state["messages"]) > 1:
        # Get the AI response (should be the last message)
        for msg in answerer_state["messages"]:
            if hasattr(msg, "type") and msg.type == "ai":
                break


    # Display agent table
    state.display_agent_table()

    return True


if __name__ == "__main__":
    result = asyncio.run(test_rag_with_agents_sequential())
    if result:
        pass!")
    else:
        pass!")
