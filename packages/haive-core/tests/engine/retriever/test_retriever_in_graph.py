# tests/core/engine/retriever/test_retriever_in_graph.py

import logging
from typing import List, Optional

# Import Document at the top level
from langchain_core.documents import Document
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def make_retriever_config(docs=None) -> VectorStoreRetrieverConfig:
    docs = docs or [Document(page_content="The Eiffel Tower is in Paris.")]
    logger.info(f"[make_retriever_config] Using {len(docs)} document(s)")
    for i, doc in enumerate(docs):
        logger.info(f" - Doc {i}: {doc.page_content}")
        print(f"📄 Doc {i}: {doc.page_content}")

    vectorstore = VectorStoreConfig(
        name="vs_test",
        documents=docs,
        vector_store_provider=VectorStoreProvider.IN_MEMORY,
        embedding_model=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-MiniLM-L6-v2"
        ),
    )

    return VectorStoreRetrieverConfig(
        name="retriever_test", vector_store_config=vectorstore
    )


# Define state classes at the top level
class RetrievalState(BaseModel):
    search_text: str = Field(default="")
    query: Optional[str] = Field(default=None)
    documents: Optional[List[Document]] = Field(default=None)


class QueryState(BaseModel):
    query: str = Field(default="")
    documents: Optional[List[Document]] = Field(default=None)


# Add this test to verify the retriever works in isolation
def test_retriever_works_directly():
    """Verify that the retriever works correctly in isolation."""
    docs = [Document(page_content="The Eiffel Tower is in Paris.")]
    retriever_config = make_retriever_config(docs)

    # Test direct invocation
    results = retriever_config.invoke("Eiffel Tower")

    # Print results for debugging
    print(f"Direct retriever results: {results}")
    logger.info(f"Direct retriever results: {results}")

    # Verify results
    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], Document)
    assert "Eiffel Tower" in results[0].page_content


def test_retriever_with_different_input_mappings():
    """Test that retriever works with different input mappings in the graph."""
    docs = [Document(page_content="The Eiffel Tower is in Paris.")]
    retriever_config = make_retriever_config(docs)

    # Create graph with state schema
    from typing import List, Optional

    from pydantic import BaseModel, Field

    class RetrievalState(BaseModel):
        search_text: str = Field(default="")
        query: Optional[str] = Field(default=None)
        documents: Optional[List[Document]] = Field(default=None)

    # Create graph with explicit state schema
    graph = DynamicGraph(
        name="retriever_mapping_test",
        components=[retriever_config],
        state_schema=RetrievalState,
    )

    # Add preprocessing node that explicitly sets the query
    def log_input(state):
        print(f"🔍 Input state: {state}")

        # Access state fields correctly based on type
        if isinstance(state, dict):
            search_text = state.get("search_text", "")
            return {"query": search_text}  # Set query to search_text
        else:
            search_text = getattr(state, "search_text", "")
            return {"query": search_text}  # Set query to search_text

    # Add post-processing node to handle documents
    def process_results(state):
        print(f"📝 Processing state: {state}")

        # Create a Command to handle the response
        from langgraph.types import Command

        # Extract documents if they exist
        documents = None
        if hasattr(state, "result") and state.result:
            documents = state.result

        # Return with Command for control flow
        return Command(update={"documents": documents}, goto="END")

    # Add nodes
    graph.add_node("preprocess", log_input)
    graph.add_node("retrieve", retriever_config)
    graph.add_node("process", process_results)

    # Connect nodes
    graph.add_edge("START", "preprocess")
    graph.add_edge("preprocess", "retrieve")
    graph.add_edge("retrieve", "process")

    # Compile the graph
    app = graph.compile()

    # Use input with search_text
    input_data = {"search_text": "Eiffel Tower"}

    # Run the graph
    result = app.invoke(input_data)

    # Validate the results
    logger.info(f"✅ Graph with custom mapping result: {result}")
    print(f"✅ Graph with custom mapping result: {result}")

    # Basic validation
    assert result is not None


def test_retriever_with_runtime_config():
    """Test that retriever works with runtime configuration in the graph."""
    docs = [
        Document(page_content="The Eiffel Tower is in Paris."),
        Document(page_content="The Louvre Museum houses the Mona Lisa."),
    ]
    retriever_config = make_retriever_config(docs)

    # Create a graph with explicit state schema
    graph = DynamicGraph(
        name="retriever_config_test",
        components=[retriever_config],
        state_schema=QueryState,
    )

    # Add node and set up connections
    graph.add_node("retrieve", retriever_config, command_goto=END)
    graph.add_edge(START, "retrieve")

    # Set default runtime config
    graph.set_default_runnable_config({"configurable": {"k": 1}})  # Only get 1 result

    # Compile the graph
    app = graph.compile()

    # Run the graph with explicit query
    result = app.invoke({"query": "museum"})

    # Validate the results
    logger.info(f"✅ Graph with runtime config result: {result}")
    print(f"✅ Graph with runtime config result: {result}")

    assert isinstance(result, dict)
    assert "documents" in result or "result" in result

    # Get documents from the result
    docs_result = result.get("documents", result.get("result", []))
    assert isinstance(docs_result, list)
    # Should only get 1 result due to k=1 config
    assert len(docs_result) == 1


def test_retriever_in_dynamic_graph():
    """Test that retriever works correctly within DynamicGraph."""
    docs = [
        Document(page_content="The Eiffel Tower is in Paris."),
        Document(page_content="The Louvre Museum houses the Mona Lisa."),
    ]
    retriever_config = make_retriever_config(docs)

    # Create a state schema explicitly
    class SimpleQueryState(BaseModel):
        query: str = Field(default="")
        documents: Optional[List[Document]] = Field(default=None)
        text_contents: Optional[List[str]] = Field(default=None)

    # Create a simple graph with just the retriever
    graph = DynamicGraph(
        name="retriever_test_graph",
        components=[retriever_config],
        state_schema=SimpleQueryState,
    )

    # Create a custom post-processing node to handle the Document objects
    def process_docs(state):
        # Check for documents in several possible locations
        docs = []
        if hasattr(state, "documents") and state.documents:
            docs = state.documents
        elif hasattr(state, "result") and state.result:
            docs = state.result

        # Extract text contents
        texts = [doc.page_content for doc in docs]

        # Return with Command
        return Command(update={"documents": docs, "text_contents": texts}, goto=END)

    # Add nodes to the graph
    graph.add_node("retrieve", retriever_config)
    graph.add_node("process", process_docs, command_goto=END)

    # Connect nodes
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "process")

    # Compile the graph
    app = graph.compile()

    # Create input according to the expected schema
    input_data = {"query": "Where is the Eiffel Tower?"}

    # Run the graph
    result = app.invoke(input_data)

    # Validate the results
    logger.info(f"✅ Graph result: {result}")
    print(f"✅ Graph result: {result}")

    # Check if documents were returned correctly
    assert "documents" in result
    assert isinstance(result["documents"], list)
    assert len(result["documents"]) > 0
    assert all(isinstance(d, Document) for d in result["documents"])

    # Check if text contents were extracted
    assert "text_contents" in result
    assert isinstance(result["text_contents"], list)
    assert "Eiffel Tower" in " ".join(result["text_contents"])


if __name__ == "__main__":
    # Run all tests
    print("\n📊 Testing retriever in dynamic graph")
    test_retriever_in_dynamic_graph()
    test_retriever_with_different_input_mappings()
    test_retriever_with_runtime_config()

    print("\n✅ All tests passed!")
