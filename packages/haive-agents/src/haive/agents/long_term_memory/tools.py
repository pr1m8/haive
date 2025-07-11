import uuid

from agents.long_term_memory.models import KnowledgeTriple
from haive.core.models.vectorstore.base import VectorStoreConfig
from haive.core.utils.runnable_config_utils import get_user_id
from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel


@tool
def save_recall_memory(
    memory: str, config: RunnableConfig, vs_config: VectorStoreConfig
) -> str:
    """Save memory to vectorstore for later semantic retrieval."""
    user_id = get_user_id(config)
    document = Document(
        page_content=memory, id=str(uuid.uuid4()), metadata={"user_id": user_id}
    )
    vs_config.add_documents([document])
    return memory


@tool
def save_structured_recall_memory(
    config: RunnableConfig,
    vs_config: VectorStoreConfig,
    memories: list[BaseModel] = None,
) -> str:
    """Save memory to vectorstore for later semantic retrieval."""
    if memories is None:
        memories = [KnowledgeTriple]
    if memories is None:
        memories = [KnowledgeTriple]
    if memories is None:
        memories = [KnowledgeTriple]
    if memories is None:
        memories = [KnowledgeTriple]
    if memories is None:
        memories = [KnowledgeTriple]
    user_id = get_user_id(config)
    for memory in memories:
        serialized = " ".join(memory.values())
        document = Document(
            serialized,
            id=str(uuid.uuid4()),
            metadata={
                "user_id": user_id,
                **memory,
            },
        )
        vs_config.add_documents([document])
    return memories


@tool
def search_recall_memories(
    query: str, config: RunnableConfig, vs_config: VectorStoreConfig
) -> list[str]:
    """Search for relevant memories."""
    user_id = get_user_id(config)

    def _filter_function(doc: Document) -> bool:
        return doc.metadata.get("user_id") == user_id

    documents = vs_config.create_vectorstore().similarity_search(
        query, k=3, filter=_filter_function
    )
    return [document.page_content for document in documents]
