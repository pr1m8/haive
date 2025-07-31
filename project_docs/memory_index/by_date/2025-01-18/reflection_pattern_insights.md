# Reflection Pattern Insights - 2025-01-18

## Key Discovery: The Message-Only Challenge

When building reflection agents, we discovered a fundamental challenge:

- Agents only accept messages as input
- But we have structured outputs (like GradingResult) that need to flow between agents
- How do we bridge this gap?

## Solutions Discovered

### 1. Prompt Template Partials

Instead of trying to force structured data into messages, use ChatPromptTemplate features:

```python
REFLECTION_WITH_GRADE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a reflection specialist that improves responses."),
    ("human", """Please improve this response:

{response}

{grade_context}

Provide an enhanced version that addresses any feedback.""")
])

# Use partial to inject grade context
grade_text = f"Grade: {result.letter_grade} ({result.score}/100)..."
prompt = REFLECTION_WITH_GRADE_PROMPT.partial(grade_context=grade_text)
```

### 2. Optional Variables in Templates

```python
# Template with optional sections
ADAPTIVE_PROMPT = ChatPromptTemplate.from_messages([
    ("human", """{response}
{grade_feedback|Optional grade feedback:}
{previous_attempts|Previous attempts:}""")
])
```

### 3. The Right Prompt Pattern (from task_analysis example)

- Direct ChatPromptTemplate constants (no factory functions!)
- Multi-line strings with proper formatting
- Clear variable placeholders
- Structured sections with markdown

### 4. Generic Pre/Post Hook Pattern

Created three classes from generic pattern:

- `PrePostMultiAgent[TPreAgent, TMainAgent, TPostAgent]`
- `StructuredOutputMultiAgent` - for structured extraction
- `ReflectionMultiAgent` - for reflection with message transform
- `GradedReflectionMultiAgent` - grade → main → reflect

### 5. Message Transformation Role

The message transformer is crucial for reflection:

- Preserves first message (original query)
- Swaps AI ↔ Human roles
- Enables "conversation with self" pattern

## What We Learned

1. **Don't fight the message-only interface** - use prompt engineering instead
2. **Structured data can flow through prompt configuration** not messages
3. **Message transformation + prompt partials** = powerful combination
4. **No factories, no model_post_init** unless truly needed
5. **Direct class instantiation** is cleaner than factory functions

## The Flow Pattern

```
Main Agent → Response (AIMessage)
    ↓
Grading Agent → GradingResult (structured)
    ↓
Convert to prompt partial (not message!)
    ↓
Message Transform (AI → Human)
    ↓
Reflection Agent (with grade in prompt context)
```

## Related Files

- `/packages/haive-agents/src/haive/agents/reflection/` - Implementation
- `/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py` - Message transformer
- `/packages/haive-agents/src/haive/agents/task_analysis/context/prompts.py` - Good prompt example
