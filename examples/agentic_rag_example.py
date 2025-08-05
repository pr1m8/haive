"""Agentic RAG Example - Simple and Clean Implementation.

This example shows how to use SimpleAgent with structured output for agentic RAG.
"""

import asyncio
from typing import Any

from langchain_core.tools import tool

from haive.agents.rag.common.document_graders.models import DocumentBinaryResponse
from haive.agents.rag.common.query_refinement.models import QueryRefinementResponse
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Document grader using SimpleAgent
document_grader = SimpleAgent(
    name="document_grader",
    engine=AugLLMConfig(
        prompt_template="""You are a document relevance grader. Evaluate whether documents are relevant to a given query.

For each document:
1. Carefully read the query and document content
2. Decide if the document contains information that helps answer the query
3. Grade as 'pass' if relevant, 'fail' if not relevant
4. Provide clear justification for your decision
5. Assign a confidence score (0-1)

Be strict but fair - documents should directly relate to the query to pass.

Query: {query}

Documents to grade:
{documents}""",
        structured_output_model=DocumentBinaryResponse,
        structured_output_version="v2",
        temperature=0.0,
    ),
)

# Query rewriter using SimpleAgent
query_rewriter = SimpleAgent(
    name="query_rewriter",
    engine=AugLLMConfig(
        prompt_template="""You are a query optimization specialist for RAG systems. Your role is to analyze queries and suggest improvements for better retrieval.

Guidelines:
1. Make queries more specific and clear
2. Add relevant context or constraints
3. Use appropriate technical terminology
4. Consider different phrasings that might yield better results
5. Break down complex queries if needed

Provide multiple suggestions with clear rationales and select the best one.

Original query: {query}

Context: {context}""",
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
        temperature=0.7,
    ),
)


@tool
def grade_documents(query: str, documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Grade documents for relevance to a query."""
    result = asyncio.run(document_grader.arun({"query": query, "documents": documents}))
    return result.model_dump()


@tool
def rewrite_query(query: str, context: str = "") -> dict[str, Any]:
    """Rewrite a query to improve retrieval."""
    result = asyncio.run(query_rewriter.arun({"query": query, "context": context}))
    return result.model_dump()


# Main agentic RAG agent using ReactAgent with tools
agentic_rag = ReactAgent(
    name="agentic_rag",
    engine=AugLLMConfig(
        system_message="""You are an agentic RAG system that helps users find relevant information.

Your workflow:
1. When given a query, first try to retrieve relevant documents
2. Grade the documents for relevance using the grade_documents tool
3. If documents are not relevant enough, rewrite the query using rewrite_query tool
4. Continue until you have good documents or reach max attempts
5. Generate a final answer based on the relevant documents

Use the tools available to you to provide the best possible answer.""",
        temperature=0.3,
    ),
    tools=[grade_documents, rewrite_query],
)


async def main():
    """Example usage of the agentic RAG system."""

    # Example documents
    documents = [
        {
            "id": "doc1",
            "content": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to perform computations. Unlike classical computers that use bits, quantum computers use quantum bits (qubits).",
        },
        {
            "id": "doc2",
            "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data without being explicitly programmed.",
        },
        {
            "id": "doc3",
            "content": "Python is a high-level programming language known for its simplicity and readability. It's widely used in data science and web development.",
        },
    ]

    # Test document grading
    print("=== Document Grading Example ===")
    grading_result = await document_grader.arun(
        {"query": "What is quantum computing?", "documents": documents},
    )

    print(f"Grading result: {grading_result}")

    # Test query rewriting
    print("\n=== Query Rewriting Example ===")
    rewrite_result = await query_rewriter.arun(
        {
            "query": "quantum stuff",
            "context": "User is asking about quantum computing basics",
        },
    )

    print(f"Rewrite result: {rewrite_result}")

    # Test full agentic RAG
    print("\n=== Full Agentic RAG Example ===")
    rag_result = await agentic_rag.arun(
        f"I have these documents: {documents}. "
        "My query is: 'quantum stuff'. "
        "Please grade them for relevance and rewrite my query if needed, then provide an answer.",
    )

    print(f"RAG result: {rag_result}")


async def demonstrate_components():
    """Demonstrate individual components of the Agentic RAG system."""
    print("\n\n🧩 Individual Components Demo\n")

    # Document Grader
    from haive.agents.rag.agentic import DocumentGraderAgent

    print("1️⃣ Document Grader Agent:")
    grader = DocumentGraderAgent.create_default()

    grading_input = {
        "query": "What is machine learning?",
        "documents": [
            {
                "id": "doc1",
                "content": "Machine learning is a type of artificial intelligence that allows systems to learn from data.",
            },
            {
                "id": "doc2",
                "content": "The weather today is sunny with a chance of rain in the evening.",
            },
        ],
    }

    grading_result = await grader.arun(grading_input)
    print(f"   Graded {len(grading_result.document_decisions)} documents")
    for decision in grading_result.document_decisions:
        print(
            f"   - {decision.document_id}: {decision.decision} ({decision.justification[:50]}...)",
        )

    # Query Rewriter
    from haive.agents.rag.agentic import QueryRewriterAgent

    print("\n2️⃣ Query Rewriter Agent:")
    rewriter = QueryRewriterAgent.create_default()

    rewrite_input = {
        "query": "ML applications",
        "context": "User is looking for practical applications of machine learning",
    }

    rewrite_result = await rewriter.arun(rewrite_input)
    print(f"   Original: {rewrite_result.original_query}")
    print(f"   Best Rewrite: {rewrite_result.best_refined_query}")
    print("   Other Suggestions:")
    for suggestion in rewrite_result.refinement_suggestions[:3]:
        print(f"   - {suggestion.refined_query} ({suggestion.improvement_type})")


async def main():
    """Run all demonstrations."""
    # Run the main Agentic RAG demo
    await demonstrate_agentic_rag()

    # Run component demos
    await demonstrate_components()

    print("\n\n✅ Demo completed!")


if __name__ == "__main__":
    # Note: This example requires:
    # 1. OpenAI API key set in environment
    # 2. Vector store setup (or mock data)
    # 3. Optional: Web search API for full functionality

    print("Note: This is a demonstration example.")
    print("In production, you would:")
    print("- Use a real vector store with your documents")
    print("- Configure actual web search API")
    print("- Add proper error handling and logging")
    print("- Optimize prompts for your use case\n")

    asyncio.run(main())
