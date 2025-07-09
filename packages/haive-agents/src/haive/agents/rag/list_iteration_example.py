"""Example of using ListIterationNode with RAG agents

Shows how to use the list iteration pattern for processing multiple queries
or documents through RAG agents.
"""

from typing import Any, Dict, List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.list_iteration_node import (
    ListIterationNodeConfig,
    create_engine_callable,
    create_list_iteration_node,
)
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.rag.simple.agent import SimpleRAGAgent


# Example 1: Process multiple queries through a RAG agent
def create_multi_query_processor(documents: List[Document]):
    """Create a list iteration node that processes multiple queries."""

    # Create a RAG agent
    rag_agent = SimpleRAGAgent.from_documents(
        documents=documents,
        llm_config=AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        ),
    )

    # Create callable that uses the RAG agent
    def process_query(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single query through RAG."""
        result = rag_agent.run({"query": query})
        return {
            "query": query,
            "response": result.get("response", ""),
            "query_index": context["index"],
        }

    # Create list iteration node
    return create_list_iteration_node(
        name="MultiQueryProcessor",
        list_key="queries",  # Expects state.queries to be a list
        callable_func=process_query,
        output_key="query_results",
    )


# Example 2: Process documents through summarization
def create_document_summarizer():
    """Create a list iteration node that summarizes multiple documents."""

    # Create summarization engine
    summarize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert at summarizing documents concisely."),
            ("human", "Summarize this document in 2-3 sentences:\n\n{document}"),
        ]
    )

    summarize_engine = AugLLMConfig(
        llm_config=AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        ),
        prompt_template=summarize_prompt,
        output_key="summary",
    )

    # Create engine callable
    def summarize_document(doc: Document, context: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize a single document."""
        result = summarize_engine.invoke({"document": doc.page_content})
        return {
            "document_index": context["index"],
            "source": doc.metadata.get("source", "unknown"),
            "summary": result.get("summary", ""),
            "original_length": len(doc.page_content),
        }

    # Create list iteration node
    return create_list_iteration_node(
        name="DocumentSummarizer",
        list_key="documents",  # Expects state.documents to be a list
        callable_func=summarize_document,
        output_key="summaries",
    )


# Example 3: Batch entity extraction
def create_entity_extractor():
    """Create a list iteration node for entity extraction."""

    from pydantic import BaseModel, Field

    class ExtractedEntities(BaseModel):
        """Entities extracted from text."""

        people: List[str] = Field(default_factory=list, description="Names of people")
        organizations: List[str] = Field(
            default_factory=list, description="Organization names"
        )
        locations: List[str] = Field(default_factory=list, description="Location names")
        dates: List[str] = Field(default_factory=list, description="Dates mentioned")

    extract_prompt = ChatPromptTemplate.from_messages(
        [("system", "Extract entities from the following text."), ("human", "{text}")]
    )

    extract_engine = AugLLMConfig(
        llm_config=AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        ),
        prompt_template=extract_prompt,
        structured_output_model=ExtractedEntities,
        output_key="entities",
    )

    # Use the create_engine_callable helper
    engine_callable = create_engine_callable(extract_engine)

    return create_list_iteration_node(
        name="EntityExtractor",
        list_key="texts",  # Expects state.texts to be a list
        callable_func=engine_callable,
        output_key="extracted_entities",
    )


# Example 4: Parallel document grading with Send pattern
def create_parallel_document_grader():
    """Create a list iteration node that grades documents in parallel."""

    def grade_document(doc: Document, context: Dict[str, Any]) -> Dict[str, Any]:
        """Grade a single document - this would be processed in parallel."""
        # In real usage, this would be a separate node that receives the Send
        return {
            "document": doc.page_content[:100] + "...",
            "relevance_score": 0.85,  # Placeholder
            "quality_score": 0.90,  # Placeholder
            "index": context["index"],
        }

    return create_list_iteration_node(
        name="ParallelDocumentGrader",
        list_key="documents_to_grade",
        callable_func=grade_document,
        output_key="grading_results",
        use_send=True,  # Enable parallel processing
        send_node_name="grade_single_document",
        parallel=True,
    )


# Example usage in a graph
def example_graph_usage():
    """Example of how to use list iteration nodes in a graph."""

    from haive.core.graph.state_graph.base_graph2 import BaseGraph
    from langgraph.graph import END, START

    # Create graph
    graph = BaseGraph(name="ListIterationExample")

    # Create nodes
    query_processor = create_multi_query_processor(
        documents=[
            Document(page_content="Example document about AI"),
            Document(page_content="Another document about ML"),
        ]
    )

    summarizer = create_document_summarizer()

    # Add nodes to graph
    graph.add_node("process_queries", query_processor)
    graph.add_node("summarize_docs", summarizer)

    # Add edges
    graph.add_edge(START, "process_queries")
    graph.add_edge("process_queries", "summarize_docs")
    graph.add_edge("summarize_docs", END)

    # Example state
    example_state = {
        "queries": ["What is AI?", "How does ML work?", "What are neural networks?"],
        "documents": [
            Document(page_content="Long document about AI..."),
            Document(page_content="Long document about ML..."),
        ],
    }

    # The graph would process all queries and summarize all documents
    return graph
