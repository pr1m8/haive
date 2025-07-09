import asyncio

from haive.core.utils.doc_utils import clean_and_format_text
from langchain_core.documents import Document

from haive.agents.document_modifiers.summarizer.map_branch.agent import SummarizerAgent
from haive.agents.document_modifiers.summarizer.map_branch.config import (
    SummarizerAgentConfig,
)


async def main():
    summarizer = SummarizerAgent(SummarizerAgentConfig())
    # summarizer.setup_workflow()
    from langchain_community.document_loaders import WebBaseLoader

    documents = WebBaseLoader(
        "https://en.wikipedia.org/wiki/Differential_geometry"
    ).load()

    print(summarizer.length_function(documents))
    documents = [
        Document(
            page_content=clean_and_format_text(d.page_content), metadata=d.metadata
        )
        for d in documents
    ]
    await summarizer.arun({"contents": documents}, debug=True)
    # print(documents)
    # from langchain_community.document_transformers import Html2TextTransformer,MarkdownifyTransformer,BeautifulSoupTransformer,\
    # DoctranQATransformer,DoctranPropertyExtractor,OpenAIMetadataTagger,LongContextReorder,NucliaTextTransformer


if __name__ == "__main__":
    asyncio.run(main())
