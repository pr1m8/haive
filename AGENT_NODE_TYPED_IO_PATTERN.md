# Agent Node Typed I/O Pattern - Using Agent Schemas

**Date**: 2025-01-18
**Key Insight**: Agent nodes can use the agent's input/output schemas as type parameters!

## 🎯 The Pattern from LangGraph

From the LangGraph docs on private state:

```python
# Node 1 outputs its specific schema
def node_1(state: OverallState) -> Node1Output:
    return {"private_data": "set by node_1"}

# Node 2 accepts specific input schema
def node_2(state: Node2Input) -> OverallState:
    return {"a": "set by node_2"}
```

## 🔥 Applied to Agent Nodes

We can use the agent's schemas directly:

```python
# Agent has input/output schemas
class SelectorAgent(Agent):
    input_schema = SelectorInput    # What it expects
    output_schema = SelectedModules # What it returns
    state_schema = SelectorAgentState # Its working state

# Agent node can use these as type hints!
def agent_node(state: MultiAgentState) -> Command[dict]:
    agent = get_agent("selector")

    # Agent handles its own input extraction based on input_schema
    result = agent.invoke(state)  # Returns SelectedModules instance

    # Clean typed update
    return Command(
        update={
            # The output schema field becomes the update key!
            "selected_modules": result.model_dump() if hasattr(result, 'model_dump') else result
        }
    )
```

## 📚 Key Insights from Docs

### 1. Messages with add_messages Reducer

```python
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

This is why MultiAgentState.messages works - it has the reducer!

### 2. Input/Output Schema Pattern

```python
# Define distinct schemas
builder = StateGraph(
    OverallState,
    input_schema=InputState,    # What node expects
    output_schema=OutputState   # What node returns
)
```

### 3. Private State Between Nodes

The exact pattern we need for agents:

- Each agent has its own input/output schemas
- Nodes pass specific data between them
- Not everything is in the overall state

## 🎯 The Complete Pattern

### Agent Definition

```python
class MyAgent(Agent):
    # Agent declares its schemas
    input_schema = MyAgentInput     # e.g., task_description, context
    output_schema = MyAgentOutput   # e.g., SelectedModules
    state_schema = MyAgentState     # Internal working state

    def invoke(self, state: Any) -> MyAgentOutput:
        # Extract inputs based on input_schema
        if self.input_schema:
            inputs = self.extract_inputs_from_state(state)
        else:
            inputs = state

        # Process and return output_schema instance
        return MyAgentOutput(...)
```

### Agent Node Pattern

```python
class AgentNodeV3Config:
    def __call__(self, state: MultiAgentState) -> Command:
        # Get agent with its schemas
        agent = self._get_agent(state)

        # Pass full state - agent extracts based on input_schema
        result = agent.invoke(state)

        # Update based on output_schema
        if hasattr(agent, 'output_schema') and agent.output_schema:
            # Use schema name as field
            field_name = self._get_output_field_name(agent)
            update = {field_name: result}
        else:
            # Default to agent_outputs
            update = {
                "agent_outputs": {
                    self.agent_name: result
                }
            }

        return Command(update=update)
```

## 📊 Examples

### Simple Agent (Messages)

```python
# No output_schema - defaults to messages
simple_agent = SimpleAgent(name="chat")
# Updates: {"messages": [...]}
```

### Structured Agent (Schema)

```python
# Has output_schema
select_agent = SelectorAgent(name="select_modules")
# Updates: {"selected_modules": SelectedModules(...)}
```

### With Prompt Template

```python
# Agent with prompt template needing extra inputs
class AnalysisAgent(Agent):
    input_schema = AnalysisInput  # has: document, analysis_type, context
    output_schema = AnalysisResult
    prompt_template = ChatPromptTemplate.from_template(
        "Analyze {document} for {analysis_type} considering {context}"
    )
```

## 🔑 Key Benefits

1. **Type Safety**: Full typing from agent schemas
2. **Clean Updates**: Output schema → state field mapping
3. **Flexibility**: Agents can have complex input needs
4. **No Projection**: Agent handles extraction internally
5. **LangGraph Native**: Follows the framework patterns

## 📝 Implementation Notes

1. **Agent must handle input extraction** based on its input_schema
2. **Output can be schema instance or dict** - node handles conversion
3. **Field naming convention**:
   - Schema-based: `selected_modules`, `adapted_modules`
   - Default: `agent_outputs[agent_name]`
4. **Messages use reducer**: Annotated[list[BaseMessage], add_messages]

---

**This is the way!** Agents declare their I/O, nodes just orchestrate!
