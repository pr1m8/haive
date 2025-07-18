# Implementation Plan - Three Agent Supervisor Test

## Agent ID: claude_agent_20250107_165800

## Implementation Steps

### Step 1: Create Three Specialized Agents

#### Research Agent (ReactAgent + tavily_search)

```python
from haive.tools.tools.search_tools import tavily_search

research_engine = AugLLMConfig(
    name="research_engine",
    tools=[tavily_search],
    system_message="You are a research specialist. Use tavily_search to find information."
)
research_agent = ReactAgent(name="research_agent", engine=research_engine)
```

#### Math Agent (ReactAgent + add/multiply) - Already exists ✅

#### Essay Writer Agent (SimpleAgent + structured output)

```python
class Essay(BaseModel):
    title: str = Field(description="Essay title")
    introduction: str = Field(description="Introduction paragraph")
    body_paragraphs: List[str] = Field(description="Main body paragraphs")
    conclusion: str = Field(description="Conclusion paragraph")

essay_engine = AugLLMConfig(
    name="essay_engine",
    structured_output_model=Essay,
    structured_output_version='v2',
    system_message="You are an essay writer. Create well-structured essays."
)
essay_writer_agent = SimpleAgent(name="essay_writer_agent", engine=essay_engine)
```

### Step 2: Register All Agents

```python
registry.register("research_agent", research_agent, "Searches for information using Tavily")
registry.register("math_agent", math_agent, "Performs mathematical calculations")
registry.register("essay_writer_agent", essay_writer_agent, "Writes structured essays")
```

### Step 3: Test Multi-Step Task

```python
# Complex task requiring all 3 agents
result = supervisor.invoke({
    "messages": [HumanMessage(
        "Research the current costs of implementing AI in small businesses, "
        "calculate the ROI over 5 years assuming 20% efficiency gain, "
        "and write a brief essay about the findings."
    )]
})
```

### Expected Flow

1. Supervisor analyzes task
2. Routes to research_agent for cost data
3. Routes to math_agent for ROI calculation
4. Routes to essay_writer_agent for final essay
5. Returns comprehensive result

### Success Criteria

- [ ] All 3 agents registered and accessible
- [ ] Supervisor correctly identifies which agent for each subtask
- [ ] Proper handoff between agents
- [ ] State/results flow between agents
- [ ] Final result incorporates all agent outputs
- [ ] No infinite loops or stuck states
