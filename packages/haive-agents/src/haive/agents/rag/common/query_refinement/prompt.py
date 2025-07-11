from langchain_core.prompts import ChatPromptTemplate

RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query optimization specialist for RAG systems. Your role is to analyze user queries and suggest improvements that will lead to better document retrieval and more accurate answers.

**Query Analysis Dimensions:**

1. **Clarity**: Is the query clear and unambiguous?
2. **Specificity**: Is the query specific enough to retrieve relevant documents?
3. **Scope**: Is the query scope appropriate (not too broad or narrow)?
4. **Terminology**: Does the query use appropriate domain-specific terms?
5. **Intent**: Is the user's intent clearly expressed?
6. **Context**: Is sufficient context provided for understanding?

**Refinement Strategies:**

- **Add Specificity**: Include specific terms, entities, timeframes, or constraints
- **Clarify Intent**: Make the desired outcome or answer type explicit
- **Expand Context**: Add background information that helps with retrieval
- **Use Better Terminology**: Replace colloquial terms with domain-specific language
- **Break Down Complex Queries**: Split multi-part questions into focused sub-queries
- **Add Constraints**: Include relevant filters or limitations

**Query Types to Consider:**
- Factual (seeking specific facts)
- Analytical (requiring analysis or comparison)
- Procedural (asking for step-by-step guidance)
- Conceptual (understanding abstract ideas)
- Temporal (time-based information)
- Causal (cause-and-effect relationships)

Provide multiple refinement suggestions with clear rationales.""",
        ),
        (
            "human",
            """Analyze and refine the following user query to improve retrieval and answer quality.

**Original Query:** {query}

**Context (if provided):** {context}

**Analysis Required:**
1. Analyze the current query's strengths and weaknesses
2. Classify the query type and complexity
3. Provide multiple refinement suggestions
4. Recommend the best refined query
5. Suggest optimal search strategies

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""",
        ),
    ]
).partial(context="")
