# tests/core/engine/retriever/test_retriever.py

import logging

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableConfig

from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
)
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
            # cache_folder is now handled by the default in HuggingFaceEmbeddingConfig
        ),
    )

    return VectorStoreRetrieverConfig(
        name="retriever_test", vector_store_config=vectorstore
    )


def test_instantiate_returns_base_retriever():
    config = make_retriever_config()
    retriever = config.instantiate()
    logger.info(f"✅ Instantiated retriever: {type(retriever).__name__}")
    print(f"✅ Instantiated retriever: {type(retriever).__name__}")
    assert isinstance(retriever, BaseRetriever)


def test_get_relevant_documents_returns_results():
    config = make_retriever_config()
    docs = config.invoke("Where is the Eiffel Tower?")
    logger.info(f"✅ Retrieved {len(docs)} documents")
    print(f"✅ Retrieved {len(docs)} documents:")
    for i, doc in enumerate(docs):
        print(f"[Result {i}] {doc.page_content}")
    assert isinstance(docs, list)
    assert all(isinstance(d, Document) for d in docs)
    assert len(docs) > 0


def test_retriever_input_schema_fields():
    config = make_retriever_config()
    input_schema = config.derive_input_schema()
    fields = list(input_schema.model_fields.keys())
    logger.info(f"✅ Input schema fields: {fields}")
    print(f"✅ Input schema fields: {fields}")
    assert "query" in fields
    assert "k" in fields


def test_retriever_output_schema_fields():
    config = make_retriever_config()
    output_schema = config.derive_output_schema()
    fields = list(output_schema.model_fields.keys())
    logger.info(f"✅ Output schema fields: {fields}")
    print(f"✅ Output schema fields: {fields}")
    assert "documents" in fields


def test_apply_runnable_config_overrides_k():
    config = make_retriever_config()
    rcfg = RunnableConfig(configurable={"k": 2})
    applied = config.apply_runnable_config(rcfg)
    logger.info(f"✅ Applied k override: {applied.get('k')}")
    print(f"✅ Applied k override: {applied.get('k')}")
    assert applied.get("k") == 2
