"""Tests for schema integration with NodeFactory and NodeConfig."""

import logging
import os
import tempfile
from typing import List

import pytest
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.schema_composer import SchemaComposer

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Test Models ---


class QA(BaseModel):
    """Question and Answer model."""

    question: str = Field(description="The question asked")
    answer: str = Field(description="The answer to the question")


class QAs(BaseModel):
    """Container for multiple QA pairs."""

    qas: List[QA] = Field(description="List of QA pairs")


class DocumentSection(BaseModel):
    """A section in a document."""

    title: str = Field(description="Section title")
    content: str = Field(description="Section content")
    subsections: List["DocumentSection"] = Field(
        default_factory=list, description="Subsections"
    )


# Recursive model reference
DocumentSection.model_rebuild()


class DocumentHierarchy(BaseModel):
    """Hierarchical document structure."""

    title: str = Field(description="Document title")
    sections: List[DocumentSection] = Field(
        default_factory=list, description="Document sections"
    )


class DocumentAnalysis(BaseModel):
    """Structured analysis of a document."""

    topics: List[str] = Field(description="Main topics in the document")
    concepts: List[str] = Field(description="Key concepts in the document")
    dates: List[str] = Field(description="Important dates mentioned")
    summary: str = Field(description="Brief summary of the document")


# --- Test Fixtures ---


@pytest.fixture
def azure_llm_config():
    """Create AzureLLMConfig fixture."""
    return AzureLLMConfig(
        model="gpt-4o",
    )


@pytest.fixture
def sample_documents():
    """Create sample documents for vector store testing."""
    texts = [
        "Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming.",
        "Neural networks are computing systems inspired by the biological neural networks that constitute animal brains.",
        "Deep learning is part of a broader family of machine learning methods based on artificial neural networks.",
        "Natural language processing (NLP) is a field of AI that focuses on the interaction between computers and humans through natural language.",
        "Computer vision is an interdisciplinary field that deals with how computers can gain high-level understanding from digital images or videos.",
    ]

    return [
        Document(page_content=text, metadata={"source": f"doc{i}"})
        for i, text in enumerate(texts)
    ]


@pytest.fixture
def embedding_model():
    """Create a HuggingFace embedding model."""
    return HuggingFaceEmbeddingConfig(model="sentence-transformers/all-MiniLM-L6-v2")


@pytest.fixture
def vector_store(sample_documents, embedding_model):
    """Create a vector store with sample documents."""
    # Create temporary directory for vector store
    temp_dir = tempfile.mkdtemp()

    vs_config = VectorStoreConfig(
        name="test_vector_store",
        documents=sample_documents,
        vector_store_provider=VectorStoreProvider.FAISS,
        embedding_model=embedding_model,
        vector_store_path=os.path.join(temp_dir, "vector_store"),
        k=2,
    )

    return vs_config


@pytest.fixture
def retriever(vector_store):
    """Create a retriever from the vector store."""
    return VectorStoreRetrieverConfig(
        name="test_retriever", vector_store_config=vector_store, k=2
    )


# --- Tests ---


def test_summarizer_with_context_field(azure_llm_config):
    """Test a summarizer using context field instead of messages."""
    # Create prompt template
    summarizer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that summarizes text."),
            ("human", "Please summarize the following text:\n\n{context}"),
        ]
    )

    # Create AugLLM with output parser
    summarizer_llm = AugLLMConfig(
        name="summarizer_llm",
        prompt_template=summarizer_prompt,
        output_parser=StrOutputParser(),
        llm_config=azure_llm_config,
    )

    # Check that input schema has context field
    input_schema = summarizer_llm.derive_input_schema()
    assert hasattr(input_schema, "model_fields")
    assert "context" in input_schema.model_fields

    # Create NodeConfig with output mapping to summary field
    node_config = NodeConfig(
        name="summarize",
        engine=summarizer_llm,
        output_mapping={"text": "summary"},  # Map text output to summary field
        command_goto=END,
    )

    # Create node function
    node_func = NodeFactory.create_node_function(node_config)

    # Test with simple input - no messages field required
    test_input = {
        "context": "Paris is the capital of France. It is known for its art, culture, and the Eiffel Tower."
    }

    # Invoke node function
    result = node_func(test_input)

    # Verify result structure
    assert hasattr(result, "update")
    assert hasattr(result, "goto")
    assert result.goto == END

    # Check that summary field is in the update
    assert "summary" in result.update
    assert isinstance(result.update["summary"], str)
    assert len(result.update["summary"]) > 0


def test_structured_output_model_fields(azure_llm_config):
    """Test that structured output model fields appear in schema."""
    # Create prompt template for QA generation
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI assistant that generates questions and answers from text.",
            ),
            ("human", "Generate questions and answers from this text:\n\n{contents}"),
        ]
    )

    # Create AugLLM with structured output model
    qa_llm = AugLLMConfig(
        name="qa_generator",
        prompt_template=qa_prompt,
        structured_output_model=QAs,
        llm_config=azure_llm_config,
    )

    # Schema composition should include the structured output model fields
    schema = SchemaComposer.compose_schema(components=[qa_llm], name="QASchema")

    # Verify schema includes the structured output model fields
    assert hasattr(schema, "model_fields")
    assert "qas" in schema.model_fields  # Field from QAs model
    assert "contents" in schema.model_fields  # Field from prompt template

    # Create node config
    node_config = NodeConfig(name="generate_qa", engine=qa_llm, command_goto=END)

    # Create node function
    node_func = NodeFactory.create_node_function(node_config)

    # Test with basic input
    test_input = {
        "contents": "Marie Curie was a Polish-born physicist and chemist known for her pioneering research on radioactivity."
    }

    # Invoke node function
    result = node_func(test_input)

    # Verify result structure
    assert hasattr(result, "update")
    assert "qas" in result.update
    assert isinstance(result.update["qas"], list)

    # Check that qas list contains QA objects
    if len(result.update["qas"]) > 0:
        qa_item = result.update["qas"][0]
        assert isinstance(qa_item, QA)
        assert hasattr(qa_item, "question")
        assert hasattr(qa_item, "answer")


def test_implicit_schema_from_engines(azure_llm_config, retriever):
    """Test that schema is implicitly derived from engines in a graph."""
    # Create answer generation LLM
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that answers questions based on provided context.",
            ),
            (
                "human",
                """
        Question: {query}
        
        Context:
        {context}
        
        Answer:""",
            ),
        ]
    )

    answer_llm = AugLLMConfig(
        name="answer_generator",
        prompt_template=answer_prompt,
        llm_config=azure_llm_config,
    )

    # Create graph without explicit schema
    graph = DynamicGraph(name="rag_workflow", components=[retriever, answer_llm])

    # Get the implicitly derived schema
    derived_schema = graph.state_schema

    # Verify schema includes fields from both components
    assert hasattr(derived_schema, "model_fields")
    assert "query" in derived_schema.model_fields  # From retriever input
    assert "context" in derived_schema.model_fields  # From LLM prompt

    # Add nodes with mapping
    graph.add_node(
        "retrieve",
        retriever,
        input_mapping={"query": "query"},
        output_mapping={"documents": "context"},
    )

    graph.add_node("generate_answer", answer_llm, command_goto=END)

    # Connect nodes
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate_answer")

    # Compile graph
    compiled_graph = graph.compile()

    # Test with query
    test_input = {"query": "What is machine learning?"}

    # Invoke graph
    result = compiled_graph.invoke(test_input)

    # Check result structure
    assert isinstance(result, dict)
    assert "context" in result  # Should contain retrieved documents
    assert isinstance(result["context"], list)
    assert len(result["context"]) > 0  # Should have at least one retrieved document
    assert "content" in result  # Should contain generated answer


def test_complex_field_mapping(azure_llm_config):
    """Test complex mapping from nested structured output fields."""
    # Create document analysis prompt
    analysis_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You analyze documents and extract key information."),
            (
                "human",
                """
        Please analyze this document and extract:
        1. Main topics
        2. Key concepts
        3. Important dates
        
        Document: {document}
        """,
            ),
        ]
    )

    # Create AugLLM with structured output
    analysis_llm = AugLLMConfig(
        name="document_analyzer",
        prompt_template=analysis_prompt,
        structured_output_model=DocumentAnalysis,
        llm_config=azure_llm_config,
    )

    # Create NodeConfig with complex mapping
    node_config = NodeConfig(
        name="analyze_document",
        engine=analysis_llm,
        input_mapping={"content": "document"},  # Map state.content to engine.document
        output_mapping={
            "documentanalysis.topics": "extracted_topics",  # Map model's topics to state.extracted_topics
            "documentanalysis.concepts": "extracted_concepts",  # Map model's concepts to state.extracted_concepts
            "documentanalysis.summary": "document_summary",  # Map model's summary to state.document_summary
        },
        command_goto=END,
    )

    # Create node function
    node_func = NodeFactory.create_node_function(node_config)

    # Test with basic input
    test_input = {
        "content": "The Industrial Revolution was a period of major industrialization and innovation that took place during the late 1700s and early 1800s. The Industrial Revolution began in Great Britain and quickly spread throughout the world."
    }

    # Invoke node function
    result = node_func(test_input)

    # Verify result structure
    assert hasattr(result, "update")

    # Check mapped output fields
    assert "extracted_topics" in result.update
    assert isinstance(result.update["extracted_topics"], list)

    assert "extracted_concepts" in result.update
    assert isinstance(result.update["extracted_concepts"], list)

    assert "document_summary" in result.update
    assert isinstance(result.update["document_summary"], str)

    # Full model should be available too
    assert "documentanalysis" in result.update
    assert hasattr(result.update["documentanalysis"], "topics")
    assert hasattr(result.update["documentanalysis"], "concepts")
    assert hasattr(result.update["documentanalysis"], "summary")
    assert hasattr(result.update["documentanalysis"], "dates")


def test_schema_composer_includes_all_fields(azure_llm_config, retriever):
    """Test that SchemaComposer includes fields from all engines."""
    # Create a document structure prompt
    doc_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You analyze document structure."),
            (
                "human",
                "Analyze this document and create a structured outline:\n\n{contents}",
            ),
        ]
    )

    # Create AugLLM with structured output
    doc_llm = AugLLMConfig(
        name="doc_structure_analyzer",
        prompt_template=doc_prompt,
        structured_output_model=DocumentHierarchy,
        llm_config=azure_llm_config,
    )

    # Use SchemaComposer to generate a schema from multiple components
    schema = SchemaComposer.compose_schema(
        components=[retriever, doc_llm], name="CombinedSchema"
    )

    # Verify schema includes fields from all components
    assert hasattr(schema, "model_fields")

    # From retriever
    assert "query" in schema.model_fields
    assert "documents" in schema.model_fields

    # From document LLM
    assert "contents" in schema.model_fields
    assert "documenthierarchy" in schema.model_fields

    # Check field types
    assert schema.model_fields["query"].annotation == str
    assert schema.model_fields["documenthierarchy"].annotation == DocumentHierarchy


def test_node_factory_detects_engine_type(azure_llm_config):
    """Test that NodeFactory correctly detects engine type."""
    # Create simple prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant."), ("human", "{input}")]
    )

    # Create AugLLM
    llm = AugLLMConfig(name="llm", prompt_template=prompt, llm_config=azure_llm_config)

    # Create NodeConfig with auto-detection of message usage
    node_config = NodeConfig(name="process", engine=llm, command_goto=END)

    # Verify that node config correctly auto-detects uses_messages
    assert node_config.use_direct_messages is True

    # Create NodeConfig with explicit uses_messages=False
    node_config_no_msgs = NodeConfig(
        name="process_no_msgs", engine=llm, use_direct_messages=False, command_goto=END
    )

    # Create node functions
    node_func = NodeFactory.create_node_function(node_config)
    node_func_no_msgs = NodeFactory.create_node_function(node_config_no_msgs)

    # Test with messages
    test_with_msgs = {"messages": [HumanMessage(content="Hello")]}

    # Test with direct input
    test_with_input = {"input": "Hello"}

    # Invoke both node functions with both inputs
    result_msgs = node_func(test_with_msgs)
    result_input = node_func_no_msgs(test_with_input)

    # Both should work
    assert hasattr(result_msgs, "update")
    assert hasattr(result_input, "update")
