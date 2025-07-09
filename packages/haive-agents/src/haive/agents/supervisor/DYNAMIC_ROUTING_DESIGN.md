# Dynamic Routing Design for Haive Supervisor

## Overview

This document details the design for implementing dynamic agent routing in the Haive Supervisor using the `DynamicChoiceModel` and a single intelligent routing node, providing advantages over LangGraph's traditional multi-tool handoff approach.

## Core Concept: Single Node Dynamic Routing

### Traditional LangGraph Approach (Multi-Tool)

```python
# Multiple handoff tools - one per agent
tools = [
    create_handoff_tool("research_agent"),
    create_handoff_tool("math_agent"),
    create_handoff_tool("writer_agent"),
    # ... N tools for N agents
]

# LLM must choose among many tools
supervisor = create_react_agent(model=llm, tools=tools)
```

**Limitations**:

- Linear scaling: N agents = N tools
- Static agent list requires recompilation
- Tool pollution in LLM context
- Complex handoff logic scattered across tools

### Haive Approach (Single Routing Node)

```python
# Single routing decision with dynamic choices
routing_model = DynamicChoiceModel[str](
    options=["research_agent", "math_agent", "writer_agent"],
    model_name="AgentRouter"
)

# Single routing node handles all decisions
routing_node = NodeFactory.create_node_function(
    config=DynamicRoutingEngine(
        routing_model=routing_model,
        decision_prompt="Select the best agent for: {task}"
    )
)
```

**Advantages**:

- O(1) complexity regardless of agent count
- Runtime agent addition/removal
- Clean separation of routing logic
- Simplified LLM decision space

## DynamicChoiceModel Integration

### Agent Registration Flow

```python
class SupervisorAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize empty routing model
        self.routing_model = DynamicChoiceModel[str](
            options=[],
            model_name="AgentChoice",
            include_end=True
        )

        # Registry for agent instances
        self.agent_registry = {}

    def register_agent(self, agent: Agent) -> None:
        """Register agent and update routing model."""
        agent_name = agent.name

        # Add to registry
        self.agent_registry[agent_name] = agent

        # Update routing model (triggers schema regeneration)
        self.routing_model.add_option(agent_name)

        # Rebuild graph with new routing options
        self._rebuild_graph()

        logger.info(f"Registered agent: {agent_name}")
        logger.debug(f"Available routes: {self.routing_model.option_names}")
```

### Runtime Agent Updates

```python
def unregister_agent(self, agent_name: str) -> bool:
    """Remove agent and update routing model."""
    if agent_name not in self.agent_registry:
        return False

    # Remove from registry
    del self.agent_registry[agent_name]

    # Update routing model
    self.routing_model.remove_option_by_name(agent_name)

    # Rebuild graph
    self._rebuild_graph()

    return True

def list_available_agents(self) -> list[str]:
    """Get current available agents."""
    return self.routing_model.option_names
```

## Routing Engine Design

### Core Routing Logic

```python
class DynamicRoutingEngine:
    """Intelligent routing engine using DynamicChoiceModel + LLM."""

    def __init__(self,
                 routing_model: DynamicChoiceModel[str],
                 decision_engine: AugLLMConfig,
                 routing_prompt: str | None = None):
        self.routing_model = routing_model
        self.decision_engine = decision_engine
        self.routing_prompt = routing_prompt or self._default_prompt()

    async def route_request(self, state: Any, config: RunnableConfig) -> Command:
        """Main routing logic."""

        # Extract context from current state
        context = self._extract_context(state)

        # Get available agents
        available_agents = self.routing_model.option_names

        # Generate routing prompt
        prompt = self._build_routing_prompt(context, available_agents)

        # Get LLM decision
        choice_schema = self.routing_model.current_model
        decision = await self._get_llm_decision(prompt, choice_schema, config)

        # Validate choice
        if not self.routing_model.validate_choice(decision.choice):
            raise ValueError(f"Invalid routing choice: {decision.choice}")

        # Execute routing
        return self._execute_routing(decision.choice, state)

    def _execute_routing(self, choice: str, state: Any) -> Command:
        """Execute the routing decision."""
        if choice == "END":
            return Command(goto="__end__")

        # Route to selected agent
        return Command(
            goto=choice,
            update={"routing_decision": choice, "routing_timestamp": time.time()}
        )
```

### Intelligent Prompt Generation

```python
def _build_routing_prompt(self, context: dict, available_agents: list[str]) -> str:
    """Build context-aware routing prompt."""

    # Extract key information
    last_message = context.get("last_message", "")
    task_type = self._classify_task(last_message)

    # Get agent capabilities (if available)
    agent_capabilities = self._get_agent_capabilities(available_agents)

    prompt = f"""
    You are an intelligent task router. Analyze the following request and select
    the most appropriate agent to handle it.

    Current Request: {last_message}
    Task Type: {task_type}

    Available Agents:
    {self._format_agent_list(available_agents, agent_capabilities)}

    Select the agent best suited for this task. If the task is complete, select END.

    Response Format: Provide only the agent name or END.
    """

    return prompt
```

## Graph Building Strategy

### Dynamic Graph Construction

```python
def build_graph(self) -> BaseGraph:
    """Build supervisor graph with dynamic routing."""

    # Create base graph with composed schema
    combined_schema = self._compose_schemas()
    graph = BaseGraph(combined_schema)

    # Add supervisor routing node
    routing_engine = DynamicRoutingEngine(
        routing_model=self.routing_model,
        decision_engine=self.main_engine
    )

    supervisor_node = NodeFactory.create_node_function(
        config=routing_engine,
        command_goto="route_decision"
    )

    graph.add_node("supervisor", supervisor_node)
    graph.add_edge(START, "supervisor")

    # Add registered agents as nodes
    for agent_name, agent in self.agent_registry.items():
        # Wrap agent to return to supervisor
        agent_wrapper = self._create_agent_wrapper(agent)
        graph.add_node(agent_name, agent_wrapper)

        # Agent returns to supervisor after execution
        graph.add_edge(agent_name, "supervisor")

    # Dynamic conditional edges from supervisor
    graph.add_conditional_edges(
        "supervisor",
        self._routing_condition,
        self.routing_model.option_names + ["__end__"]
    )

    return graph

def _routing_condition(self, state: Any) -> str:
    """Extract routing decision from state."""
    return state.get("routing_decision", "END")
```

### Agent Wrapper Pattern

```python
def _create_agent_wrapper(self, agent: Agent) -> Callable:
    """Wrap agent to handle state coordination."""

    async def agent_wrapper(state: Any, config: RunnableConfig) -> dict:
        """Execute agent and prepare return to supervisor."""

        # Execute agent
        result = await agent.ainvoke(state, config)

        # Add routing metadata
        result.update({
            "last_agent": agent.name,
            "agent_execution_time": time.time(),
            "routing_decision": None  # Clear for next routing
        })

        return result

    return agent_wrapper
```

## Schema Composition

### Automatic Schema Merging

```python
def _compose_schemas(self) -> type[BaseModel]:
    """Compose schemas from all registered agents."""

    if not self.agent_registry:
        # Default schema if no agents
        return self.state_schema

    composer = SchemaComposer()

    # Add base supervisor schema
    composer.add_schema(self.state_schema)

    # Add routing fields
    routing_fields = {
        "routing_decision": (str | None, None),
        "routing_timestamp": (float | None, None),
        "last_agent": (str | None, None),
        "agent_execution_time": (float | None, None),
    }
    composer.add_fields(routing_fields)

    # Add schemas from registered agents
    for agent in self.agent_registry.values():
        if hasattr(agent, 'state_schema'):
            composer.add_schema(agent.state_schema)

    return composer.compose()
```

## Performance Optimizations

### 1. Lazy Graph Rebuilding

```python
def _rebuild_graph(self) -> None:
    """Rebuild graph only when necessary."""
    if not self._graph_needs_rebuild:
        return

    self._compiled_graph = None  # Clear cached graph
    self._graph_needs_rebuild = False
```

### 2. Choice Model Caching

```python
def _get_cached_choice_model(self) -> type[BaseModel]:
    """Cache choice model to avoid regeneration."""
    current_options = tuple(self.routing_model.option_names)

    if (self._cached_choice_key != current_options or
        self._cached_choice_model is None):

        self._cached_choice_model = self.routing_model.current_model
        self._cached_choice_key = current_options

    return self._cached_choice_model
```

### 3. Agent Capability Caching

```python
def _get_agent_capabilities(self, agent_names: list[str]) -> dict[str, str]:
    """Cache agent capability descriptions."""
    capabilities = {}

    for name in agent_names:
        if name in self._capability_cache:
            capabilities[name] = self._capability_cache[name]
        else:
            agent = self.agent_registry.get(name)
            if agent and hasattr(agent, 'description'):
                capability = agent.description
                self._capability_cache[name] = capability
                capabilities[name] = capability

    return capabilities
```

## Integration with Haive Patterns

### 1. Mixin Integration

```python
class SupervisorAgent(Agent):
    """Inherits all Haive Agent capabilities."""

    # ExecutionMixin provides:
    # - run(), arun() methods
    # - Error handling
    # - Timeout management

    # StateMixin provides:
    # - State validation
    # - State transformation
    # - History management

    # PersistenceMixin provides:
    # - Checkpointing
    # - State persistence
    # - Recovery mechanisms
```

### 2. Configuration Integration

```python
class SupervisorConfig(BaseModel):
    """Supervisor-specific configuration."""

    routing_prompt: str | None = None
    output_mode: Literal["full_history", "last_message"] = "last_message"
    max_agents: int = 10
    routing_timeout: float = 30.0
    enable_parallel_routing: bool = False

    # Inherit base agent config
    class Config:
        extra = "allow"  # Allow additional agent configs
```

## Usage Examples

### Basic Supervisor Setup

```python
# Create supervisor
supervisor = SupervisorAgent(
    name="TaskCoordinator",
    engine=AugLLMConfig(model="gpt-4"),
    routing_prompt="Route tasks to the most suitable specialist agent."
)

# Register specialized agents
supervisor.register_agent(research_agent)
supervisor.register_agent(math_agent)
supervisor.register_agent(writer_agent)

# Execute task
result = await supervisor.arun({
    "messages": [HumanMessage(content="Research quantum computing and write a summary")]
})
```

### Runtime Agent Management

```python
# Add new agent during runtime
code_agent = ReactAgent(name="code_specialist", engine=code_engine)
supervisor.register_agent(code_agent)

# Remove agent
supervisor.unregister_agent("math_agent")

# Check available agents
print(supervisor.list_available_agents())
# Output: ["research_agent", "writer_agent", "code_specialist", "END"]
```

This dynamic routing design provides a scalable, maintainable approach to multi-agent coordination while leveraging Haive's existing infrastructure and the flexibility of `DynamicChoiceModel`.
