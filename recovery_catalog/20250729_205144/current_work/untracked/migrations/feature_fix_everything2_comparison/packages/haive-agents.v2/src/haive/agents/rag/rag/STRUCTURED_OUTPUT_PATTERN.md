# Structured Output Pattern for RAG Agents

This document demonstrates the proper pattern for implementing structured output parsing in RAG agents, following the haive-core engine architecture.

## Key Principles

1. **Prompts focus on generation, not structure** - The prompt should instruct the LLM what to generate, not how to format it
2. **Output parsers handle structure** - Use `structured_output_model` with Pydantic models for parsing
3. **Use `output_key` for state management** - Store structured results in specific state keys
4. **Include format instructions** - Add `{format_instructions}` placeholder in prompts

## Pattern Implementation

### 1. Define Pydantic Models

```python
from pydantic import BaseModel, Field

class HyDEResult(BaseModel):
    """Structured output for HyDE generation."""
    hypothetical_doc: str = Field(description="Generated hypothetical document")
    refined_query: str = Field(description="Refined query for retrieval")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in hypothesis")
```

### 2. Create Prompt Template

```python
HYDE_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at generating hypothetical documents.

Guidelines:
- Write as if creating an authoritative reference document
- Include specific details and explanations
- Use clear, factual language

Please provide your response in the following format:
{format_instructions}"""),
    ("human", """Generate a hypothetical document for: {query}""")
])
```

### 3. Configure AugLLMConfig with Structured Output

```python
# V1 Approach (Parser-based) - Recommended for complex models
hyde_generator = SimpleAgent(
    engine=AugLLMConfig(
        llm_config=llm_config,
        prompt_template=HYDE_GENERATION_PROMPT,
        structured_output_model=HyDEResult,
        structured_output_version="v1",  # Uses PydanticOutputParser
        output_key="hyde_result"
    ),
    name="HyDE Generator"
)

# V2 Approach (Tool-based) - For simpler models
hyde_generator = SimpleAgent(
    engine=AugLLMConfig(
        llm_config=llm_config,
        prompt_template=HYDE_GENERATION_PROMPT,
        structured_output_model=HyDEResult,
        structured_output_version="v2",  # Uses tool forcing
        output_key="hyde_result"
    ),
    name="HyDE Generator"
)
```

### 4. Handle Structured Output in Downstream Nodes

```python
def transform_to_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """Use structured HyDE result for retrieval."""
    hyde_result = state.get("hyde_result", {})

    # Handle both dict and object forms
    if isinstance(hyde_result, dict):
        hyp_doc = hyde_result.get("hypothetical_doc", "")
    else:
        hyp_doc = getattr(hyde_result, "hypothetical_doc", "")

    return {
        "query": hyp_doc,
        "original_query": state.get("query", ""),
        "hyde_result": hyde_result
    }
```

## Complete Example: HyDE Agent

```python
class HyDERAGAgentV2(SequentialAgent):
    """HyDE RAG with proper structured output."""

    @classmethod
    def from_documents(cls, documents: List[Document], llm_config: LLMConfig, **kwargs):
        # Step 1: Generate structured hypothetical document
        hyde_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=HYDE_GENERATION_PROMPT,
                structured_output_model=HyDEResult,
                structured_output_version="v1",
                output_key="hyde_result"
            ),
            name="HyDE Generator"
        )

        # Step 2: Use structured output for retrieval
        hyde_retriever = HyDERetrieverAgent(
            base_retriever=BaseRAGAgent.from_documents(documents),
            name="HyDE Retriever"
        )

        # Step 3: Generate final answer
        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator"
        )

        return cls(
            agents=[hyde_generator, hyde_retriever, answer_agent],
            name=kwargs.get('name', 'HyDE RAG Agent V2'),
            **kwargs
        )
```

## Other RAG Patterns

### Fusion RAG

```python
# Query expansion with structured variations
query_expander = SimpleAgent(
    engine=AugLLMConfig(
        llm_config=llm_config,
        prompt_template=QUERY_EXPANSION_FUSION_PROMPT,
        structured_output_model=QueryVariationsFusion,
        output_key="query_variations_fusion"
    )
)

# Answer generation with fusion metadata
fusion_answerer = SimpleAgent(
    engine=AugLLMConfig(
        llm_config=llm_config,
        prompt_template=FUSION_ANSWER_PROMPT,
        structured_output_model=FusionResult,
        output_key="fusion_answer_result"
    )
)
```

### Speculative RAG

```python
# Hypothesis generation
hypothesis_gen = SimpleAgent(
    engine=AugLLMConfig(
        llm_config=llm_config,
        prompt_template=SPECULATIVE_PROMPT,
        structured_output_model=SpeculativeResult,
        output_key="speculative_result"
    )
)
```

## Benefits of This Pattern

1. **Separation of Concerns**: Prompts focus on content, parsers handle structure
2. **Type Safety**: Pydantic models provide validation and type hints
3. **Reusability**: Models can be reused across different agents
4. **Debugging**: Structured outputs are easier to inspect and debug
5. **Integration**: Works seamlessly with the haive-core engine system

## Common Pitfalls to Avoid

1. **Don't embed JSON in prompts** - Use structured output instead
2. **Don't parse responses manually** - Let the engine handle parsing
3. **Don't forget format instructions** - Include `{format_instructions}` placeholder
4. **Don't ignore output_key** - Use specific keys for state management
5. **Don't mix approaches** - Choose either v1 (parser) or v2 (tool) consistently

## Testing Structured Output

```python
def test_structured_output():
    """Test that structured output works correctly."""
    agent = HyDERAGAgentV2.from_documents(documents, llm_config)
    result = agent.invoke({"query": "What is machine learning?"})

    # Verify structured output is present
    assert "hyde_result" in result
    hyde_result = result["hyde_result"]

    # Verify structure
    assert isinstance(hyde_result, HyDEResult)
    assert hasattr(hyde_result, "hypothetical_doc")
    assert hasattr(hyde_result, "refined_query")
    assert hasattr(hyde_result, "confidence")
```

This pattern ensures consistent, maintainable, and properly structured RAG implementations across all agent types.
