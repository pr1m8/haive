import asyncio

from langchain_core.documents import Document

from haive.agents.document_modifiers.summarizer.iterative_refinement.agent import (
    IterativeSummarizer,
)
from haive.agents.document_modifiers.summarizer.iterative_refinement.config import (
    IterativeSummarizerConfig,
)

test_docs = [
    Document(page_content="This is a test document about machine learning."),
    Document(page_content="This document expands on deep learning architectures."),
    Document(page_content="It also discusses how transformers are used in NLP."),
    Document(page_content="Finally, it provides an overview of applications of AI."),
]

config = IterativeSummarizerConfig(
    contents=test_docs,
    # aug_llm_configs=aug_llm_configs
)

agent = IterativeSummarizer(config)


async def main():
    result = await agent.arun({"contents": test_docs}, debug=True)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
