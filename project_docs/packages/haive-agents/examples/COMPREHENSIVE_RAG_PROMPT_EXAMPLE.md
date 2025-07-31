# Comprehensive RAG Prompt Example

**Purpose**: Complete example of BaseRAG → SimpleAgent with comprehensive ChatPromptTemplate

## Key Components

### 1. Comprehensive ChatPromptTemplate

```python
RAG_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an advanced AI assistant specializing in retrieval-augmented generation (RAG).
Your role is to provide accurate, comprehensive, and well-reasoned answers based solely on the retrieved documents provided to you.

**Core Principles:**
1. **Accuracy First**: Base all answers strictly on the retrieved documents
2. **Source Attribution**: Always cite which document(s) support each claim
3. **Transparency**: Clearly indicate when information is insufficient or unavailable
4. **Synthesis**: Intelligently combine information from multiple documents when relevant
5. **Context Awareness**: Consider the relationships between different pieces of information

**Response Guidelines:**
- Start with a direct answer to the question
- Provide detailed explanations with supporting evidence
- Use quotes when citing specific passages
- Acknowledge any limitations or gaps in the available information
- Suggest related topics or follow-up questions when appropriate

**Quality Standards:**
- Ensure factual accuracy by cross-referencing multiple sources when available
- Maintain objectivity and avoid speculation beyond the documents
- Present information in a clear, logical structure
- Use appropriate technical language while remaining accessible

**Special Instructions:**
- For technical topics: Include definitions and explanations of key terms
- For procedural questions: Provide step-by-step guidance if available
- For comparative questions: Highlight similarities and differences
- For analytical questions: Break down complex concepts systematically"""
        ),
        (
            "human",
            """Please answer the following question based on the retrieved documents provided below.

**Retrieved Documents:**
{retrieved_documents}

**Question:** {query}

**Additional Context (if any):** {context}

**Answer Requirements:**
1. Provide a comprehensive answer using only information from the retrieved documents
2. Include specific citations for each major claim (e.g., [Source: Document Name])
3. If the documents don't fully answer the question, explicitly state what information is missing
4. Organize your response with clear structure (introduction, main points, conclusion if appropriate)
5. Highlight any particularly important or relevant findings
6. If multiple documents provide different perspectives, present all viewpoints fairly

**Response Format:**
- Start with a brief direct answer (1-2 sentences)
- Provide detailed explanation with evidence
- Include a summary of key points at the end
- Note any limitations or areas where more information would be helpful

Please provide your answer now:"""
        ),
    ]
).partial(context="No additional context provided")
```

### 2. Comprehensive Structured Output Model

```python
class ComprehensiveRAGAnswer(BaseModel):
    """Comprehensive structured answer from RAG system."""

    # Core answer components
    direct_answer: str = Field(
        description="Brief, direct answer to the question (1-2 sentences)"
    )

    detailed_explanation: str = Field(
        description="Comprehensive explanation with evidence from documents"
    )

    # Structured sections for complex answers
    answer_sections: Optional[List[AnswerSection]] = Field(
        default=None,
        description="Structured sections for organizing complex answers"
    )

    # Source tracking
    primary_sources: List[DocumentReference] = Field(
        description="Primary documents used for the answer"
    )

    all_sources_used: List[str] = Field(
        description="List of all source documents referenced"
    )

    # Quality indicators
    confidence_score: float = Field(
        description="Overall confidence in the answer (0-1)",
        ge=0.0,
        le=1.0
    )

    answer_completeness: str = Field(
        description="Assessment of how completely the question was answered",
        pattern="^(complete|partial|insufficient)$"
    )

    # Additional insights
    key_findings: List[str] = Field(
        description="Key findings or insights from the analysis"
    )

    information_gaps: Optional[List[str]] = Field(
        default=None,
        description="Important information that was missing from the documents"
    )

    follow_up_questions: Optional[List[str]] = Field(
        default=None,
        description="Suggested follow-up questions for deeper understanding"
    )

    # Metadata
    answer_type: str = Field(
        description="Type of answer provided",
        pattern="^(factual|analytical|procedural|conceptual|comparative)$"
    )

    synthesis_level: str = Field(
        description="Level of synthesis required",
        pattern="^(single_source|multi_source|complex_synthesis)$"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the answer was generated"
    )
```

### 3. SimpleAgent Configuration

```python
# Create SimpleAgent with comprehensive prompt and structured output v2
simple_agent = SimpleAgent(
    name="comprehensive_answer_generator",
    engine=AugLLMConfig(
        prompt_template=RAG_ANSWER_PROMPT,
        structured_output_model=ComprehensiveRAGAnswer,
        structured_output_version='v2',  # Using v2 as requested
        temperature=0.7,
        max_tokens=2000  # Allow for detailed answers
    )
)
```

### 4. Complete Flow

```python
# Step 1: Retrieve documents with BaseRAG
retrieval_result = await base_rag.arun(query)

# Step 2: Format retrieved documents
retrieved_docs_text = "\n\n".join([
    f"[Document {j}: {doc.metadata.get('source', 'Unknown')} - {doc.metadata.get('chapter', 'N/A')}]\n{doc.page_content}"
    for j, doc in enumerate(retrieval_result.retrieved_documents, 1)
])

# Step 3: Prepare input with all template variables
answer_input = {
    "retrieved_documents": retrieved_docs_text,
    "query": question_data['query'],
    "context": question_data['context']  # Additional context from user
}

# Step 4: Generate comprehensive answer
answer = await simple_agent.arun(answer_input)
```

## Key Features

1. **Comprehensive System Prompt**: Detailed instructions for high-quality RAG answers
2. **Rich Human Prompt**: Structured requirements and formatting guidelines
3. **Multiple Template Variables**: `{retrieved_documents}`, `{query}`, `{context}`
4. **Structured Output v2**: Using `structured_output_version='v2'` for better parsing
5. **Detailed Answer Model**: Captures all aspects of a comprehensive answer

## Benefits

- **Quality**: Detailed prompts lead to better, more structured answers
- **Flexibility**: Handles various question types (factual, analytical, procedural, etc.)
- **Transparency**: Tracks sources, confidence, and information gaps
- **Insights**: Provides key findings and follow-up questions
- **Metadata**: Rich metadata for answer analysis and improvement

## Example Output Structure

```json
{
  "direct_answer": "Machine learning is a subset of AI that enables systems to learn from data and improve through experience, unlike traditional programming which requires explicit instructions for every scenario.",

  "detailed_explanation": "Machine learning fundamentally differs from traditional programming in its approach to problem-solving. In traditional programming, developers write explicit rules and logic...",

  "primary_sources": [
    {
      "source_name": "ML Fundamentals Guide",
      "relevance_score": 0.95,
      "key_points": [
        "ML learns patterns from data",
        "Improves through experience",
        "No explicit programming needed"
      ]
    }
  ],

  "all_sources_used": ["ML Fundamentals Guide", "ML Categories Handbook"],

  "confidence_score": 0.92,
  "answer_completeness": "complete",

  "key_findings": [
    "ML automates pattern recognition",
    "Traditional programming requires manual rule creation",
    "ML adapts to new data without reprogramming"
  ],

  "follow_up_questions": [
    "What are the specific types of machine learning algorithms?",
    "When should I use ML vs traditional programming?"
  ],

  "answer_type": "comparative",
  "synthesis_level": "multi_source"
}
```

This approach provides a complete, production-ready RAG system with comprehensive prompting and structured outputs.
