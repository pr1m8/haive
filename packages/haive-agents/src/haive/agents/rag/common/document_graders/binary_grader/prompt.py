from langchain_core.prompts import ChatPromptTemplate

RAG_DOCUMENT_GRADE_BINARY = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert document relevance evaluator providing binary PASS/FAIL decisions.

**PASS Criteria:**
- Document contains information that directly or indirectly helps answer the query
- Content is factually relevant to the query topic or entities
- Information could reasonably be used to construct a partial or complete answer
- Document provides context that enhances understanding of the query domain

**FAIL Criteria:**
- Document has no meaningful connection to the query
- Information is completely off-topic or unrelated
- Content would not contribute to answering the query in any meaningful way
- Document discusses different entities, concepts, or topics entirely

Provide clear PASS/FAIL decisions with thorough justifications.""",
        ),
        (
            "human",
            """Query: {query}

Documents to evaluate:
{retrieved_documents}

For each document, provide a clear PASS/FAIL decision with justification.""",
        ),
    ]
)
