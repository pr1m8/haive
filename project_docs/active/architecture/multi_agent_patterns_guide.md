# Multi-Agent Patterns Guide

**Version**: 1.0  
**Purpose**: Comprehensive guide to building multi-agent systems in Haive  
**Last Updated**: 2025-01-16

## 🎯 Overview

Multi-agent systems in Haive coordinate multiple AI agents to solve complex problems that would be difficult for a single agent. This guide covers the fundamental patterns, implementation approaches, and best practices for building robust multi-agent systems.

## 🏗️ Core Architecture

### Foundation Components

```
Multi-Agent System Architecture
├── ProperMultiAgent (Base Class)
│   ├── Agent management (engines dict pattern)
│   ├── Execution modes (sequential, parallel, conditional, branch)
│   └── State schema composition
├── MultiAgentState (State Management)
│   ├── Hierarchical state management
│   ├── Execution tracking
│   └── Recompilation support
└── AgentNodeV3 (Graph Integration)
    ├── Agent execution nodes
    ├── State projection
    └── Tool routing
```

### Key Principles

1. **No Schema Flattening**: Each agent maintains its own schema
2. **Hierarchical State**: Agents have isolated state within shared context
3. **Engines Dict Pattern**: Agents managed like engines (list/dict → dict)
4. **Execution Modes**: Sequential, parallel, conditional, and branching patterns
5. **Recompilation Support**: Dynamic agent updates and graph rebuilding

## 🎨 Multi-Agent Patterns

### 1. Sequential Pattern (Chain)

Agents execute in order, each building on the previous agent's output.

```python
from haive.agents.multi.proper_base import ProperMultiAgent
from haive.agents.simple.agent import SimpleAgent

class SequentialMultiAgent(ProperMultiAgent):
    """Sequential execution: Agent1 → Agent2 → Agent3"""

    @classmethod
    def create_default(cls, **kwargs):
        # Create agents in execution order
        analyzer = SimpleAgent(name="analyzer")
        processor = SimpleAgent(name="processor")
        formatter = SimpleAgent(name="formatter")

        return cls(
            name="sequential_agent",
            agents=[analyzer, processor, formatter],
            execution_mode="sequential",
            **kwargs
        )
```

**Use Cases**:

- Document processing pipeline
- Research → Analysis → Summary
- Data extraction → Transformation → Formatting

### 2. Parallel Pattern (Fan-Out)

Agents execute simultaneously, processing different aspects of the same input.

```python
class ParallelMultiAgent(ProperMultiAgent):
    """Parallel execution: All agents run simultaneously"""

    @classmethod
    def create_default(cls, **kwargs):
        # Create specialized agents
        content_analyzer = SimpleAgent(name="content_analyzer")
        sentiment_analyzer = SimpleAgent(name="sentiment_analyzer")
        fact_checker = SimpleAgent(name="fact_checker")

        return cls(
            name="parallel_agent",
            agents=[content_analyzer, sentiment_analyzer, fact_checker],
            execution_mode="parallel",
            parallel_wait_for_all=True,  # Wait for all to complete
            **kwargs
        )
```

**Use Cases**:

- Multi-aspect analysis
- Content validation (multiple checks)
- Competitive research (multiple sources)

### 3. Conditional Pattern (Decision-Based)

Agents execute based on conditions or previous results.

```python
class ConditionalMultiAgent(ProperMultiAgent):
    """Conditional execution based on state"""

    @classmethod
    def create_default(cls, **kwargs):
        classifier = SimpleAgent(name="classifier")
        text_processor = SimpleAgent(name="text_processor")
        image_processor = SimpleAgent(name="image_processor")

        return cls(
            name="conditional_agent",
            agents=[classifier, text_processor, image_processor],
            execution_mode="conditional",
            **kwargs
        )

    def get_next_agent(self, state) -> str:
        """Determine next agent based on classification"""
        if state.get_agent_output("classifier"):
            result = state.get_agent_output("classifier")
            if "text" in result.lower():
                return "text_processor"
            elif "image" in result.lower():
                return "image_processor"
        return "classifier"
```

**Use Cases**:

- Content type routing
- Error handling workflows
- Adaptive processing pipelines

### 4. Branch Pattern (Tree-Like)

Agents execute in branching patterns based on complex decision trees.

```python
class BranchMultiAgent(ProperMultiAgent):
    """Branch execution with multiple paths"""

    @classmethod
    def create_default(cls, **kwargs):
        coordinator = SimpleAgent(name="coordinator")
        branch_a = SimpleAgent(name="branch_a")
        branch_b = SimpleAgent(name="branch_b")
        merger = SimpleAgent(name="merger")

        return cls(
            name="branch_agent",
            agents=[coordinator, branch_a, branch_b, merger],
            execution_mode="branch",
            branch_condition="if complexity > 0.5",
            **kwargs
        )
```

**Use Cases**:

- Complex decision workflows
- Multi-path processing
- Scenario-based analysis

### 5. Hierarchical Pattern (Nested)

Multi-agents containing other multi-agents for complex orchestration.

```python
class HierarchicalMultiAgent(ProperMultiAgent):
    """Hierarchical multi-agent with nested agents"""

    @classmethod
    def create_default(cls, **kwargs):
        # Create sub-multi-agents
        research_team = SequentialMultiAgent.create_default(name="research_team")
        analysis_team = ParallelMultiAgent.create_default(name="analysis_team")
        reporting_agent = SimpleAgent(name="reporting")

        return cls(
            name="hierarchical_agent",
            agents=[research_team, analysis_team, reporting_agent],
            execution_mode="sequential",
            **kwargs
        )
```

**Use Cases**:

- Large-scale workflows
- Department-like organization
- Complex business processes

## 🔧 Implementation Guide

### Step 1: Define Your Pattern

```python
# 1. Identify the pattern type
pattern_type = "sequential"  # sequential, parallel, conditional, branch, hierarchical

# 2. Define agent roles
agent_roles = {
    "planner": "Creates plans and strategies",
    "executor": "Executes tasks using tools",
    "validator": "Validates and verifies results"
}

# 3. Determine execution flow
execution_flow = "planner → executor → validator"
```

### Step 2: Create State Schema

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

class MyMultiAgentState(MultiAgentState):
    """Custom state for your multi-agent system."""

    # Add domain-specific fields
    task_type: str = Field(..., description="Type of task being processed")
    complexity_score: float = Field(default=0.0, description="Task complexity")
    validation_status: str = Field(default="pending", description="Validation status")

    # Add custom methods
    def get_complexity_level(self) -> str:
        """Get complexity level based on score."""
        if self.complexity_score < 0.3:
            return "low"
        elif self.complexity_score < 0.7:
            return "medium"
        else:
            return "high"

    def is_validated(self) -> bool:
        """Check if task is validated."""
        return self.validation_status == "validated"
```

### Step 3: Create Individual Agents

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create specialized agents
def create_planner_agent() -> SimpleAgent:
    return SimpleAgent(
        name="planner",
        engine=AugLLMConfig(
            name="planner",
            prompt_template=PLANNER_PROMPT,
            structured_output_model=PlanModel,
            temperature=0.7
        )
    )

def create_executor_agent(tools: list) -> ReactAgent:
    return ReactAgent(
        name="executor",
        engine=AugLLMConfig(
            name="executor",
            prompt_template=EXECUTOR_PROMPT,
            structured_output_model=ExecutionResult,
            temperature=0.3
        ),
        tools=tools
    )

def create_validator_agent() -> SimpleAgent:
    return SimpleAgent(
        name="validator",
        engine=AugLLMConfig(
            name="validator",
            prompt_template=VALIDATOR_PROMPT,
            structured_output_model=ValidationResult,
            temperature=0.1
        )
    )
```

### Step 4: Build Multi-Agent Class

```python
class MyMultiAgent(ProperMultiAgent):
    """Custom multi-agent implementation."""

    @classmethod
    def create_default(cls, tools: list = None, **kwargs):
        """Create multi-agent with default configuration."""

        # Create agents
        planner = create_planner_agent()
        executor = create_executor_agent(tools or [])
        validator = create_validator_agent()

        # Extract name to avoid conflicts
        name = kwargs.pop("name", "MyMultiAgent")

        return cls(
            name=name,
            agents=[planner, executor, validator],
            execution_mode="sequential",
            state_schema=MyMultiAgentState,
            **kwargs
        )

    def should_continue_execution(self, state: MyMultiAgentState) -> bool:
        """Determine if execution should continue."""
        # Custom logic based on state
        if state.complexity_score > 0.8:
            return True  # High complexity needs more processing
        return state.is_validated()

    def get_next_agent(self, state: MyMultiAgentState) -> str:
        """Determine next agent based on state."""
        if not state.get_agent_output("planner"):
            return "planner"
        elif not state.get_agent_output("executor"):
            return "executor"
        elif not state.is_validated():
            return "validator"
        else:
            return "end"
```

### Step 5: Add Custom Logic

```python
# Add result processing methods
def process_planning_result(self, state: MyMultiAgentState, result: PlanModel) -> MyMultiAgentState:
    """Process planning result and update state."""
    state.complexity_score = result.complexity_score
    state.task_type = result.task_type
    return state

def process_execution_result(self, state: MyMultiAgentState, result: ExecutionResult) -> MyMultiAgentState:
    """Process execution result and update state."""
    if result.success:
        state.validation_status = "ready_for_validation"
    else:
        state.validation_status = "needs_revision"
    return state

def process_validation_result(self, state: MyMultiAgentState, result: ValidationResult) -> MyMultiAgentState:
    """Process validation result and update state."""
    state.validation_status = "validated" if result.is_valid else "failed"
    return state
```

## 🔄 Execution Modes

### Sequential Mode

```python
class SequentialAgent(ProperMultiAgent):
    """Sequential execution pattern."""

    def __init__(self, **kwargs):
        super().__init__(
            execution_mode="sequential",
            **kwargs
        )

    # Agents execute in order: agents[0] → agents[1] → agents[2]
    # Each agent receives output from previous agent
    # State is shared and updated by each agent
```

### Parallel Mode

```python
class ParallelAgent(ProperMultiAgent):
    """Parallel execution pattern."""

    def __init__(self, **kwargs):
        super().__init__(
            execution_mode="parallel",
            parallel_wait_for_all=True,  # Wait for all agents
            **kwargs
        )

    # All agents execute simultaneously
    # Each agent receives the same input
    # Results are collected and merged
```

### Conditional Mode

```python
class ConditionalAgent(ProperMultiAgent):
    """Conditional execution pattern."""

    def __init__(self, **kwargs):
        super().__init__(
            execution_mode="conditional",
            **kwargs
        )

    def get_next_agent(self, state) -> str:
        """Override to provide conditional logic."""
        # Custom logic to determine next agent
        if condition_a(state):
            return "agent_a"
        elif condition_b(state):
            return "agent_b"
        else:
            return "default_agent"
```

### Branch Mode

```python
class BranchAgent(ProperMultiAgent):
    """Branch execution pattern."""

    def __init__(self, **kwargs):
        super().__init__(
            execution_mode="branch",
            branch_condition="complexity > 0.5",
            **kwargs
        )

    # Complex branching logic with multiple paths
    # Can split and merge execution flows
    # Supports conditional branching
```

## 🎯 Design Patterns

### 1. Producer-Consumer Pattern

```python
class ProducerConsumerAgent(ProperMultiAgent):
    """Producer creates data, consumer processes it."""

    @classmethod
    def create_default(cls, **kwargs):
        producer = SimpleAgent(name="producer")  # Generates data
        consumer = SimpleAgent(name="consumer")  # Processes data

        return cls(
            name="producer_consumer",
            agents=[producer, consumer],
            execution_mode="sequential",
            **kwargs
        )
```

### 2. Map-Reduce Pattern

```python
class MapReduceAgent(ProperMultiAgent):
    """Map phase processes data, reduce phase aggregates results."""

    @classmethod
    def create_default(cls, **kwargs):
        mapper = SimpleAgent(name="mapper")      # Processes individual items
        reducer = SimpleAgent(name="reducer")    # Aggregates results

        return cls(
            name="map_reduce",
            agents=[mapper, reducer],
            execution_mode="sequential",
            **kwargs
        )
```

### 3. Pipeline Pattern

```python
class PipelineAgent(ProperMultiAgent):
    """Processing pipeline with multiple stages."""

    @classmethod
    def create_default(cls, **kwargs):
        ingester = SimpleAgent(name="ingester")    # Stage 1: Ingest data
        processor = SimpleAgent(name="processor")  # Stage 2: Process data
        transformer = SimpleAgent(name="transformer")  # Stage 3: Transform
        outputter = SimpleAgent(name="outputter")  # Stage 4: Output results

        return cls(
            name="pipeline",
            agents=[ingester, processor, transformer, outputter],
            execution_mode="sequential",
            **kwargs
        )
```

### 4. Supervisor Pattern

```python
class SupervisorAgent(ProperMultiAgent):
    """Supervisor coordinates worker agents."""

    @classmethod
    def create_default(cls, **kwargs):
        supervisor = SimpleAgent(name="supervisor")  # Coordinates work
        worker_1 = SimpleAgent(name="worker_1")      # Specialized worker
        worker_2 = SimpleAgent(name="worker_2")      # Specialized worker

        return cls(
            name="supervisor",
            agents=[supervisor, worker_1, worker_2],
            execution_mode="conditional",  # Supervisor decides next worker
            **kwargs
        )
```

### 5. Validator Pattern

```python
class ValidatorAgent(ProperMultiAgent):
    """Multiple validators ensure quality."""

    @classmethod
    def create_default(cls, **kwargs):
        processor = SimpleAgent(name="processor")     # Main processing
        validator_1 = SimpleAgent(name="validator_1") # Accuracy check
        validator_2 = SimpleAgent(name="validator_2") # Quality check

        return cls(
            name="validator",
            agents=[processor, validator_1, validator_2],
            execution_mode="sequential",
            **kwargs
        )
```

## 🧪 Testing Multi-Agent Systems

### Unit Testing

```python
def test_multi_agent_creation():
    """Test multi-agent creation and configuration."""
    agent = MyMultiAgent.create_default(
        tools=[search_tool],
        name="test_agent"
    )

    # Test basic properties
    assert agent.name == "test_agent"
    assert agent.execution_mode == "sequential"
    assert len(agent.agents) == 3

    # Test agent composition
    assert "planner" in agent.agents
    assert "executor" in agent.agents
    assert "validator" in agent.agents
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_multi_agent_execution():
    """Test multi-agent execution with real LLMs."""
    agent = MyMultiAgent.create_default(
        tools=[calculator_tool],
        name="test_execution"
    )

    # Execute with real input
    result = await agent.arun("Calculate 15 * 23 and validate the result")

    # Verify result
    assert isinstance(result, str)
    assert "345" in result

    # Verify state
    final_state = agent.get_final_state()
    assert final_state.is_validated()
```

### State Testing

```python
def test_multi_agent_state():
    """Test multi-agent state management."""
    agent = MyMultiAgent.create_default(name="test_state")

    # Create test state
    state = agent.state_schema(
        task_type="calculation",
        complexity_score=0.5,
        agents=agent.agents
    )

    # Test state methods
    assert state.get_complexity_level() == "medium"
    assert not state.is_validated()

    # Test state updates
    state.validation_status = "validated"
    assert state.is_validated()
```

## 📊 Performance Considerations

### Execution Efficiency

```python
# ✅ EFFICIENT - Parallel execution for independent tasks
parallel_agent = ParallelAgent(
    agents=[analyzer_1, analyzer_2, analyzer_3],
    execution_mode="parallel",
    parallel_wait_for_all=True
)

# ✅ EFFICIENT - Sequential execution for dependent tasks
sequential_agent = SequentialAgent(
    agents=[preprocessor, processor, postprocessor],
    execution_mode="sequential"
)
```

### Memory Management

```python
# ✅ GOOD - Isolated agent states
state.update_agent_state("planner", {"plan": plan_data})
state.update_agent_state("executor", {"results": execution_data})

# ❌ BAD - Shared mutable state
state.shared_data = {"plan": plan_data, "results": execution_data}  # Risky
```

### Scalability

```python
# ✅ SCALABLE - Dynamic agent creation
def create_processing_agents(num_agents: int) -> List[Agent]:
    return [
        SimpleAgent(name=f"processor_{i}")
        for i in range(num_agents)
    ]

# ✅ SCALABLE - Conditional execution
def get_next_agent(self, state) -> str:
    if state.complexity_score > 0.8:
        return "high_complexity_agent"
    else:
        return "standard_agent"
```

## 🚨 Common Pitfalls

### 1. Schema Flattening

```python
# ❌ WRONG - Flattening agent schemas
class BadMultiAgentState(MultiAgentState):
    planner_step: int = Field(...)  # Don't flatten!
    executor_result: str = Field(...)

# ✅ CORRECT - Use hierarchical state
class GoodMultiAgentState(MultiAgentState):
    task_complexity: float = Field(...)  # Shared state only

    def get_planner_step(self) -> int:
        return self.get_agent_state("planner").get("step", 0)
```

### 2. Agent Coupling

```python
# ❌ WRONG - Tight coupling between agents
class BadAgent(ProperMultiAgent):
    def execute(self, state):
        # Agent A directly calls Agent B
        result_a = self.agents["agent_a"].run(input)
        result_b = self.agents["agent_b"].run(result_a)  # Too coupled!

# ✅ CORRECT - Loose coupling through state
class GoodAgent(ProperMultiAgent):
    def execute(self, state):
        # Agents communicate through state
        state.record_agent_output("agent_a", result_a)
        # Agent B reads from state when it executes
```

### 3. Synchronization Issues

```python
# ❌ WRONG - Race conditions in parallel execution
class BadParallelAgent(ProperMultiAgent):
    def process_parallel_results(self, results):
        # All agents modify same shared resource
        for result in results:
            self.shared_resource.update(result)  # Race condition!

# ✅ CORRECT - Proper synchronization
class GoodParallelAgent(ProperMultiAgent):
    def process_parallel_results(self, results):
        # Collect results first, then merge
        merged_results = {}
        for agent_name, result in results.items():
            merged_results[agent_name] = result
        return merged_results
```

## 🎯 Best Practices

### 1. Agent Specialization

```python
# ✅ GOOD - Specialized agents with clear roles
research_agent = SimpleAgent(
    name="researcher",
    engine=AugLLMConfig(
        prompt_template="You are a research specialist...",
        temperature=0.3  # Factual research
    )
)

creative_agent = SimpleAgent(
    name="creative",
    engine=AugLLMConfig(
        prompt_template="You are a creative writing assistant...",
        temperature=0.9  # Creative generation
    )
)
```

### 2. State Management

```python
# ✅ GOOD - Clear state boundaries
class WellDesignedState(MultiAgentState):
    # Shared context
    task_id: str = Field(...)
    priority: int = Field(default=1)

    # Agent-specific state accessed via methods
    def get_research_progress(self) -> float:
        return self.get_agent_state("researcher").get("progress", 0.0)

    def set_research_progress(self, progress: float):
        self.update_agent_state("researcher", {"progress": progress})
```

### 3. Error Handling

```python
# ✅ GOOD - Comprehensive error handling
class RobustMultiAgent(ProperMultiAgent):
    async def execute_agent(self, agent_name: str, state):
        try:
            result = await self.agents[agent_name].arun(state)
            state.record_agent_output(agent_name, result)
            return result
        except Exception as e:
            # Record error and attempt recovery
            error_result = {"error": str(e), "agent": agent_name}
            state.record_agent_output(agent_name, error_result)

            # Attempt recovery or fallback
            if self.has_fallback_agent(agent_name):
                return await self.execute_fallback(agent_name, state)
            else:
                raise
```

### 4. Monitoring and Debugging

```python
# ✅ GOOD - Rich monitoring support
class MonitoredMultiAgent(ProperMultiAgent):
    def execute(self, input_data):
        # Log execution start
        logger.info(f"Starting multi-agent execution: {self.name}")

        # Display debug info
        if self.debug:
            self.state.display_debug_info("Execution Start")

        # Execute with monitoring
        result = super().execute(input_data)

        # Log completion
        logger.info(f"Multi-agent execution completed: {self.name}")

        return result
```

## 🔗 Related Documentation

- [MultiAgentState Documentation](multiagent_state_documentation.md)
- [ProperMultiAgent Documentation](proper_multi_agent_documentation.md)
- [Plan and Execute Agent v2](../../haive-agents/PLAN_AND_EXECUTE_V2_DOCUMENTATION.md)
- [Agent-as-Tool Pattern](agent_as_tool_pattern.md)

## 📝 Summary

Multi-agent systems in Haive provide:

1. **Flexible Patterns**: Sequential, parallel, conditional, branch, and hierarchical execution
2. **State Management**: Hierarchical state without schema flattening
3. **Agent Specialization**: Each agent focused on specific tasks
4. **Execution Control**: Fine-grained control over agent coordination
5. **Scalability**: Support for complex, large-scale workflows
6. **Monitoring**: Rich debugging and monitoring capabilities

The key to successful multi-agent systems is proper agent specialization, clear state boundaries, and choosing the right execution pattern for your use case.

---

**Quick Start Template**:

```python
class MyMultiAgent(ProperMultiAgent):
    @classmethod
    def create_default(cls, tools=None, **kwargs):
        agents = [
            create_agent_1(),
            create_agent_2(),
            create_agent_3()
        ]
        return cls(
            name="my_multi_agent",
            agents=agents,
            execution_mode="sequential",
            state_schema=MyMultiAgentState,
            **kwargs
        )
```
