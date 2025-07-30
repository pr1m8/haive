"""Document Grading Agent for Agentic RAG.

This agent evaluates retrieved documents for relevance using existing models from common.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.rag.common.document_graders.models import (
    DocumentBinaryResponse,
)
from haive.agents.simple import SimpleAgent


def create_document_grader_agent(
    name: str = "document_grader", temperature: float = 0.0, **kwargs
) -> SimpleAgent:
    """Create a document grader agent using direct SimpleAgent instantiation.

    Args:
        name: Agent name (default: "document_grader")
        temperature: LLM temperature (default: 0.0 for consistency)
        **kwargs: Additional configuration options

    Returns:
        SimpleAgent configured for document grading

    Example:
        .. code-block:: python

            # Create grader agent
            grader = create_document_grader_agent(
            name="doc_grader",
            temperature=0.0
            )

            # Grade documents
            result = await grader.arun({
            "query": "What is quantum computing?",
            "documents": [
            {"content": "Quantum computing uses quantum mechanics...", "id": "doc1"},
            {"content": "Classical computing uses binary digits...", "id": "doc2"}
            ]
            })

            # Access results
            for decision in result.document_decisions:
            print(f"Document {decision.document_id}: {decision.decision}")
            print(f"Reason: {decision.justification}")

    """
    prompt_template = (
        "You are a document relevance grader. Evaluate whether documents are relevant to a given query.\n\n"
        "For each document:\n"
        "1. Carefully read the query and document content\n"
        "2. Decide if the document contains information that helps answer the query\n"
        "3. Grade as 'pass' if relevant, 'fail' if not relevant\n"
        "4. Provide clear justification for your decision\n"
        "5. Assign a confidence score (0-1)\n\n"
        "Be strict but fair - documents should directly relate to the query to pass.\n\n"
        "Query: {query}\n\n"
        "Documents to grade:\n{documents}"
    )

    return SimpleAgent(
        name=name,
        engine=AugLLMConfig(
            temperature=temperature,
            prompt_template=prompt_template,
            structured_output_model=DocumentBinaryResponse,
            structured_output_version="v2",
        ),
        **kwargs
    )


async def grade_documents(
    agent: SimpleAgent, query: str, documents: list[dict[str, Any]]
) -> DocumentBinaryResponse:
    """Grade documents for relevance to a query.

    Args:
        agent: The document grader agent
        query: The user query
        documents: List of documents with 'content' and 'id' fields

    Returns:
        DocumentBinaryResponse with grading results
    """
    # Format the input for the agent
    input_data = {"query": query, "documents": documents}

    # Run the agent
    result = await agent.arun(input_data)

    # Return the structured result
    return result
