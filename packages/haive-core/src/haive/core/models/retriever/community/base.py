from enum import Enum
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.retrievers import BaseRetriever
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv(".env")


class BaseRetrieverConfig(BaseModel):
    """Abstract base class for retriever configuration."""

    def create(self) -> BaseRetriever:
        raise NotImplementedError("Must implement create method.")


# --- Community Retriever Support ---


class CommunityRetrieverType(str, Enum):
    WikipediaRetriever = "WikipediaRetriever"
    TavilySearchAPIRetriever = "TavilySearchAPIRetriever"
    PubMedRetriever = "PubMedRetriever"
    AskNewsRetriever = "AskNewsRetriever"
    WebResearchRetriever = "WebResearchRetriever"
    ZepRetriever = "ZepRetriever"
    ZillizRetriever = "ZillizRetriever"
    ArxivRetriever = "ArxivRetriever"


class CommunityRetrieverConfig(BaseRetrieverConfig):
    retriever_type: CommunityRetrieverType
    retriever_kwargs: dict[str, Any] = Field(default_factory=dict)

    def create(self) -> BaseRetriever:
        from langchain_community.retrievers import __getattr__

        retriever_cls = __getattr__(self.retriever_type.value)
        return retriever_cls(**self.retriever_kwargs)


sample_queries = {
    "WikipediaRetriever": "Large language models",
    "TavilySearchAPIRetriever": "latest advancements in generative AI",
    "PubMedRetriever": "CRISPR gene editing technology",
    "AskNewsRetriever": "current state of global inflation",
    "WebResearchRetriever": "open source vector databases",
    "ZepRetriever": "user behavior analysis",
    "ZillizRetriever": "embedding optimization techniques",
    "ArxivRetriever": "transformer models in NLP",
}

for retriever_name, query in sample_queries.items():

    try:
        config = CommunityRetrieverConfig(
            retriever_type=CommunityRetrieverType(retriever_name),
            retriever_kwargs={"search_type": "similarity"},  # Optional per retriever
        )
        retriever = config.create()
        docs = retriever.invoke(query)

        if docs:
            pass
        else:
            passd.")
    except Exception as e:
        pass")
