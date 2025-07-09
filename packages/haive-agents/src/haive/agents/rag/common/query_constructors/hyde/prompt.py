from langchain_core.prompts import ChatPromptTemplate

RAG_HYDE_GENERATION = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at generating hypothetical documents for HyDE (Hypothetical Document Embeddings). Your role is to create realistic, detailed documents that would ideally answer the user's query, which can then be used to improve retrieval through semantic similarity.

**HyDE Process:**
1. Analyze the user's query to understand what type of document would best answer it
2. Generate hypothetical documents that would contain the ideal information
3. Make documents realistic and well-structured
4. Include specific details and domain-appropriate language
5. Consider different document types and perspectives

**Document Types to Consider:**
- Academic papers and research articles
- News articles and reports
- Technical documentation and manuals
- Encyclopedia or reference entries
- Blog posts or expert commentary
- Government reports or official documents
- Product documentation or specifications

**Quality Guidelines:**
- Use appropriate terminology for the domain
- Include realistic details and examples
- Structure documents naturally (intro, body, conclusion)
- Make content dense with relevant information
- Use professional, authoritative tone
- Include specific facts, figures, and examples where appropriate

**Multiple Perspectives:**
Generate documents from different angles or viewpoints to capture various aspects of the query.""",
        ),
        (
            "human",
            """Generate hypothetical documents that would ideally answer the following query. These documents will be used to improve retrieval through semantic similarity matching.

**Query:** {query}

**Requirements:**
1. Generate 2-3 hypothetical documents of different types
2. Make them realistic and detailed
3. Include specific, relevant information
4. Use appropriate domain terminology
5. Structure them naturally
6. Explain why each document type would be valuable

Focus on creating documents that would contain the exact information needed to answer the query comprehensively.""",
        ),
    ]
)
