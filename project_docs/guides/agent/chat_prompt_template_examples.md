# ChatPromptTemplate Examples - Haive Framework

**Purpose**: Examples of using ChatPromptTemplate with SimpleAgent and structured output
**Last Updated**: 2025-01-20

## Query Refinement Example

This example shows how to use ChatPromptTemplate with SimpleAgent for query refinement:

```python
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Define the chat prompt template
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
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
]).partial(context="")

# Define structured output models
class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(
        description="Type of improvement made (clarity, specificity, scope, etc.)"
    )
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(
        description="Expected improvement in retrieval or answering"
    )

class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(
        description="Analysis of the original query's strengths and weaknesses"
    )
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(
        description="List of suggested query improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: list[str] = Field(
        description="Recommendations for search strategy"
    )

# Create the agent with prompt template and structured output
query_refinement_agent = SimpleAgent(
    engine=AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version='v2'
    )
)

# Compile and use
query_refinement_agent.compile()

# Usage
result = await query_refinement_agent.arun({
    "query": "How does AI work?",
    "context": "Machine learning context"
})
```

## Key Patterns

### 1. ChatPromptTemplate Structure

```python
ChatPromptTemplate.from_messages([
    ("system", "System instructions..."),
    ("human", "User message with {variables}...")
])
```

### 2. Using with SimpleAgent

```python
agent = SimpleAgent(
    engine=AugLLMConfig(
        prompt_template=your_chat_template,
        structured_output_model=YourModel,
        structured_output_version='v2'
    )
)
```

### 3. Partial Templates

```python
# Set default values for some variables
template = ChatPromptTemplate.from_messages([...]).partial(context="")
```

### 4. Variable Substitution

The human message can include variables like `{query}` and `{context}` that get filled in when the agent runs.

## RAG Answer Generation Example

```python
RAG_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful assistant that answers questions based on provided context.

Instructions:
- Use ONLY the information in the provided context to answer the question
- If the context doesn't contain enough information, say so clearly
- Provide source references when possible"""
    ),
    (
        "human",
        """Context:
{context}

Question: {query}

Please provide a structured answer based on the context above."""
    )
])
```

This gets used in SimpleRAG to format retrieved documents and the user query as a proper chat conversation.
