# Multi-Agent Understanding Notes - Complete Pattern Analysis

**Version**: 1.0
**Purpose**: Complete understanding of Haive multi-agent patterns from reading guides and clean.py
**Last Updated**: 2025-01-20

## 🎯 What I'm Learning from the Code

### Two Different Patterns Discovered

Based on reading the guides and files, there are **TWO distinct patterns**:

#### Pattern 1: MultiAgent Class (from clean.py)

- **Class**: `MultiAgent(Agent)` - inherits from Agent
- **Usage**: `MultiAgent(agents=[agent1, agent2])`
- **Purpose**: Coordinates multiple agents using routing logic
- **State**: Uses `MultiAgentState` by default (line 239 in clean.py)
- **Execution**: Has its own execution logic via BaseGraph

#### Pattern 2: MultiAgentState Container (from guides)

- **State Container**: `MultiAgentState(agents=[agent1, agent2])`
- **Usage**: Direct state management with `create_agent_node_v3`
- **Purpose**: State container for multi-agent workflows
- **Execution**: Uses agent nodes: `create_agent_node_v3("agent_name")`

## 📋 Key Insights from clean.py (MultiAgent Class)

### Line-by-Line Analysis

**Lines 152-155**: MultiAgent has `agents: dict[str, Agent]` field

```python
agents: dict[str, Agent] = Field(
    default_factory=dict,
    description="Dictionary of agents this multi-agent coordinates",
)
```

**Lines 185-231**: `normalize_agents_and_name` validator converts list to dict

```python
if isinstance(agents, list):
    # Convert list to dict using agent names
    agent_dict = {}
    for i, agent in enumerate(agents):
        if hasattr(agent, "name") and agent.name:
            agent_dict[agent.name] = agent
        else:
            agent_dict[f"agent_{i}"] = agent
    values["agents"] = agent_dict
```

**Lines 233-239**: MultiAgent automatically uses MultiAgentState

```python
def setup_agent(self) -> None:
    """Setup multi-agent - use MultiAgentState by default."""
    super().setup_agent()

    # Set default state schema if none provided
    if self.state_schema is None:
        self.state_schema = MultiAgentState
```

**Lines 241-247**: MultiAgent builds its own BaseGraph

```python
def build_graph(self) -> BaseGraph:
    """Build the BaseGraph for this multi-agent."""
    # Create BaseGraph with state schema
    graph = BaseGraph(name=f"{self.name}_graph", state_schema=self.state_schema)
```

## 📋 Key Insights from guides (MultiAgentState Pattern)

### From basic_sequential.py

**Lines 137-141**: MultiAgentState constructor takes agents list

```python
state = WorkflowState(
    agents=[planner, executor, reviewer],
    task_description=task_description,
    deadline=deadline,
)
```

**Lines 144-146**: Create agent nodes from agent names

```python
plan_node = create_agent_node_v3("planner")
exec_node = create_agent_node_v3("executor")
review_node = create_agent_node_v3("reviewer")
```

**Lines 158, 165, 172**: Direct node execution

```python
result1 = plan_node(state, config)  # Planning
result2 = exec_node(state, config)   # Execution
result3 = review_node(state, config) # Review
```

**Lines 50-74**: Custom state schema extends MultiAgentState

```python
class WorkflowState(MultiAgentState):
    """State schema for the sequential workflow."""

    # Input fields
    task_description: str = ""
    deadline: str = ""

    # Planning agent outputs
    plan: List[str] = Field(default_factory=list)
    priority: str = ""
    # ... more fields for each agent's outputs
```

### From MultiAgentState.py

**Lines 52**: MultiAgentState constructor

```python
state = MultiAgentState(agents=[planner, executor])
```

**Lines 64-72**: Sequential execution pattern

```python
result1 = plan_node(state, config)  # Updates planning_result field

# Apply updates
for key, value in result1.update.items():
    if hasattr(state, key):
        setattr(state, key, value)

result2 = exec_node(state, config)  # Reads planning_result, outputs execution_result
```

**Lines 78-90**: LangGraph integration

```python
graph = StateGraph(MultiAgentState)
graph.add_node("plan", create_agent_node_v3("planner"))
graph.add_node("execute", create_agent_node_v3("executor"))
```

## 🎯 CORRECT PATTERN IDENTIFIED

After reading the existing `multi_agent_simple_rag.py`, I now understand the CORRECT pattern:

### SimpleRAG Inherits from MultiAgent (CORRECT)

```python
class SimpleRAG(MultiAgent):
    """SimpleRAG inheriting from MultiAgent."""

    # Pydantic fields for configuration
    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(...)
    llm_config: AugLLMConfig = Field(...)

    @model_validator(mode="after")
    def create_agents(self) -> "SimpleRAG":
        """Create the retriever and generator agents."""
        # Create agents
        retriever = BaseRAGAgent(name=f"{self.name}_retriever", engine=self.retriever_config)
        generator = SimpleAgent(name=f"{self.name}_generator", engine=self.llm_config)

        # Set agents dictionary (required by MultiAgent)
        self.agents = {"retriever": retriever, "generator": generator}

        # Set execution mode to sequential
        self.execution_mode = "sequential"

        return self
```

**Key Points from Existing Implementation**:

1. **Line 56**: `class SimpleRAG(MultiAgent):` - inherits from MultiAgent
2. **Lines 118-161**: Pydantic Field definitions for configuration
3. **Line 181**: `@model_validator(mode="after")` - sets up agents AFTER validation
4. **Line 201**: `self.agents = {"retriever": retriever_agent, "generator": generator_agent}` - sets agents dict
5. **Line 204**: `self.execution_mode = "sequence"` - sets execution mode

### Why This Pattern Works

1. **SimpleRAG IS a MultiAgent** - it inherits all MultiAgent functionality
2. **Pydantic Fields** - clean configuration with validation
3. **model_validator(mode="after")** - proper setup timing, no **init** override
4. **self.agents = {...}** - sets the agents dictionary that MultiAgent expects
5. **self.execution_mode = "sequential"** - tells MultiAgent how to execute

## 🎯 What I Still Need to Understand

1. **Which pattern does the user want for SimpleRAG?**
   - Inheriting from MultiAgent (Option A)?
   - Function returning MultiAgent (Option B)?
   - Function returning MultiAgentState (Option C)?

2. **How do the patterns work together?**
   - Does MultiAgent internally use MultiAgentState?
   - When would you use each pattern?

3. **What does "inheriting" mean in this context?**
   - The user said "it is a class inheriting" - inheriting from what?
   - MultiAgent? Agent? MultiAgentState?

## 🔄 Next Steps to Complete Understanding

1. **Ask for clarification** on which specific pattern is wanted
2. **Read more examples** to see how they're actually used
3. **Look at existing RAG implementations** to see the patterns
4. **Test understanding** with simple examples

---

**Status**: Still learning - need to understand which specific pattern the user wants for SimpleRAG.
