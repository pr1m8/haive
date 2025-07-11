# tests/core/engine/vectorstore/test_vectorstore.py

import logging

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
)
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def make_default_config(docs: list[Document] | None = None) -> VectorStoreConfig:
    used_docs = (
        docs
        if docs is not None
        else [Document(page_content="The capital of France is Paris.")]
    )
    logger.info(f"[make_default_config] Initializing with {len(used_docs)} document(s)")
    for i, doc in enumerate(used_docs):
        logger.info(f" - Doc {i}: {doc.page_content}")

    return VectorStoreConfig(
        name="test_vs",
        documents=used_docs,
        vector_store_provider=VectorStoreProvider.IN_MEMORY,
        embedding_model=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-MiniLM-L6-v2"
        ),
    )


def test_create_vectorstore_returns_inmemory():
    config = make_default_config()
    vs = config.instantiate()
    logger.info(f"✅ Created vector store: {vs.__class__.__name__}")
    assert isinstance(vs, InMemoryVectorStore)


def test_similarity_search_returns_results():
    config = make_default_config()
    results = config.similarity_search("What is the capital of France?")
    logger.info(f"✅ Retrieved {len(results)} results from similarity_search")
    for i, doc in enumerate(results):
        logger.info(f" - Result {i}: {doc.page_content}")
    assert isinstance(results, list)
    assert all(isinstance(doc, Document) for doc in results)
    assert len(results) > 0


def test_invoke_returns_documents():
    config = make_default_config()
    results = config.invoke("Paris")
    logger.info(f"✅ Retrieved {len(results)} documents from invoke")
    assert isinstance(results, list)
    assert all(isinstance(doc, Document) for doc in results)


def test_input_output_schemas():
    config = make_default_config()
    input_schema = config.derive_input_schema()
    output_schema = config.derive_output_schema()
    logger.info(f"✅ Input schema fields: {list(input_schema.model_fields.keys())}")
    logger.info(f"✅ Output schema fields: {list(output_schema.model_fields.keys())}")
    assert "query" in input_schema.model_fields
    assert "documents" in output_schema.model_fields


def test_add_documents():
    config = make_default_config(docs=[])
    logger.info(f"🔄 Initial document count: {len(config.documents)}")
    assert len(config.documents) == 0

    doc1 = Document(page_content="Rome is the capital of Italy.")
    config.add_document(doc1)
    logger.info(f"✅ After add_document: {len(config.documents)}")
    assert len(config.documents) == 1

    doc2 = Document(page_content="Berlin is the capital of Germany.")
    config.add_documents([doc2])
    logger.info(f"✅ After add_documents: {len(config.documents)}")
    assert len(config.documents) == 2

    for i, doc in enumerate(config.documents):
        print(f"[Doc {i}] {doc.page_content}")
