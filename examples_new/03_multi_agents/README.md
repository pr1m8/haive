# Multi-Agent Examples

Learn to coordinate multiple agents for complex workflows and specialized tasks. These examples demonstrate agent collaboration, orchestration, and emergent behaviors.

## Purpose

Multi-agent systems allow you to combine specialized agents to solve complex problems that would be difficult for a single agent. Learn coordination patterns, state management, and workflow orchestration.

## Prerequisites

- Solid understanding of single agents from [previous examples](../02_single_agents/)
- Familiarity with async/await patterns
- Basic understanding of workflow concepts
- Knowledge of Pydantic models for state management

## Examples

### Basic Coordination

#### `sequential_agents.py`

**Chain agents in sequence**

- Agent A passes results to Agent B
- Linear workflow execution
- State transfer between agents
- Error propagation handling

#### `parallel_agents.py`

**Run agents concurrently**

- Multiple agents work simultaneously
- Result aggregation patterns
- Performance optimization
- Race condition handling

#### `hierarchical_agents.py`

**Supervisor-worker pattern**

- Manager agent coordinates workers
- Task delegation and monitoring
- Result compilation
- Dynamic work assignment

### Advanced Orchestration

#### `dynamic_routing.py`

**Route tasks based on content**

- Intelligent task classification
- Agent selection strategies
- Fallback mechanisms
- Performance monitoring

#### `consensus_agents.py`

**Multiple agents reach consensus**

- Voting and agreement patterns
- Conflict resolution
- Quality assurance through redundancy
- Byzantine fault tolerance concepts

#### `iterative_refinement.py`

**Agents improve each other's work**

- Critique and revision cycles
- Quality improvement loops
- Convergence detection
- Diminishing returns handling

### State Management

#### `shared_state.py`

**Agents share common state**

- Centralized state management
- State synchronization
- Conflict resolution
- Atomic operations

#### `message_passing.py`

**Agents communicate via messages**

- Asynchronous message queues
- Event-driven coordination
- Loose coupling patterns
- Message routing and filtering

## Key Patterns

### Sequential Execution

```python
from haive.agents.multi import EnhancedMultiAgentV4

# Create sequential workflow
workflow = EnhancedMultiAgentV4([
    planner_agent,
    executor_agent,
    validator_agent
], mode="sequential")

result = await workflow.arun("Complex task")
```

### Parallel Execution

```python
# Run agents in parallel, then combine results
workflow = EnhancedMultiAgentV4([
    researcher_agent,
    analyst_agent,
    reviewer_agent
], mode="parallel")

results = await workflow.arun("Research topic")
```

### Hierarchical Coordination

```python
# Supervisor coordinates multiple workers
supervisor = SupervisorAgent(
    name="coordinator",
    workers=[
        specialist_1,
        specialist_2,
        specialist_3
    ]
)
```

### Dynamic Routing

```python
router = RoutingAgent(
    name="router",
    agents={
        "technical": technical_agent,
        "creative": creative_agent,
        "analytical": analytical_agent
    },
    routing_strategy="content_based"
)
```

## Running Examples

```bash
# Basic coordination patterns
poetry run python examples_new/03_multi_agents/sequential_agents.py
poetry run python examples_new/03_multi_agents/parallel_agents.py

# Advanced orchestration
poetry run python examples_new/03_multi_agents/dynamic_routing.py
poetry run python examples_new/03_multi_agents/consensus_agents.py

# State management
poetry run python examples_new/03_multi_agents/shared_state.py
poetry run python examples_new/03_multi_agents/message_passing.py
```

## Skill Level

**Advanced** - Requires understanding of:

- Single agent patterns and capabilities
- Async/await and concurrent programming
- State management concepts
- Workflow design principles

## Architecture Patterns

### Coordination Strategies

1. **Sequential (Pipeline)**
   - Linear workflow
   - Each agent processes previous output
   - Good for refinement workflows

2. **Parallel (Fan-out/Fan-in)**
   - Concurrent execution
   - Results aggregated
   - Good for analysis tasks

3. **Hierarchical (Tree)**
   - Manager-worker relationships
   - Delegation and supervision
   - Good for complex projects

4. **Mesh (Peer-to-peer)**
   - Agents communicate directly
   - Decentralized coordination
   - Good for collaborative tasks

### State Management

```python
class WorkflowState(StateSchema):
    """Shared state across all agents."""
    messages: List[BaseMessage]
    shared_context: Dict[str, Any]
    agent_results: Dict[str, Any]
    workflow_status: str

    def update_from_agent(self, agent_name: str, result: Any):
        """Update state with agent result."""
        self.agent_results[agent_name] = result
```

### Error Handling

```python
class RobustWorkflow:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    async def execute_with_fallback(self, task: str):
        """Execute with fallback strategies."""
        for agent in self.agents:
            try:
                return await agent.arun(task)
            except Exception as e:
                logger.warning(f"Agent {agent.name} failed: {e}")
                continue
        raise WorkflowError("All agents failed")
```

## Common Use Cases

### Content Creation Pipeline

```python
# Research → Write → Review → Publish
content_pipeline = EnhancedMultiAgentV4([
    ResearchAgent(tools=[web_search, document_loader]),
    WriterAgent(style="professional"),
    EditorAgent(focus="quality"),
    PublisherAgent(platforms=["blog", "social"])
], mode="sequential")
```

### Data Analysis Workflow

```python
# Collect → Clean → Analyze → Visualize
analysis_workflow = EnhancedMultiAgentV4([
    DataCollectorAgent(sources=["api", "files"]),
    DataCleanerAgent(strategies=["outliers", "missing"]),
    AnalystAgent(methods=["stats", "ml"]),
    VisualizationAgent(charts=["plots", "dashboards"])
], mode="sequential")
```

### Decision Support System

```python
# Multiple perspectives → Consensus → Recommendation
decision_system = ConsensusWorkflow([
    FinancialAnalystAgent(),
    RiskAssessmentAgent(),
    StrategicPlanningAgent(),
    StakeholderAgent()
], consensus_threshold=0.75)
```

## Performance Considerations

1. **Parallelization**: Use parallel execution when agents are independent
2. **Resource Management**: Monitor memory and API usage across agents
3. **Failure Isolation**: Don't let one agent failure break entire workflow
4. **State Size**: Keep shared state minimal to reduce overhead
5. **Communication Overhead**: Minimize data transfer between agents

## Best Practices

### Agent Design

- **Single Responsibility**: Each agent has a clear, focused role
- **Loose Coupling**: Agents should be independently testable
- **Clear Interfaces**: Well-defined input/output contracts
- **Error Handling**: Graceful degradation on failures

### Workflow Design

- **Idempotent Operations**: Agents should be safely restartable
- **Progress Tracking**: Monitor workflow execution status
- **Checkpointing**: Save state at critical points
- **Rollback Capability**: Handle partial failures gracefully

### Testing Strategies

```python
# Test individual agents in isolation
def test_individual_agents():
    agent = ResearchAgent()
    result = await agent.arun("test query")
    assert result is not None

# Test agent interactions
def test_agent_coordination():
    workflow = create_test_workflow()
    result = await workflow.execute_test_case()
    assert_workflow_completed_successfully(result)
```

## Common Challenges

### State Synchronization

- **Problem**: Agents modifying shared state concurrently
- **Solution**: Use locks, atomic operations, or message passing

### Error Propagation

- **Problem**: One agent failure breaks entire workflow
- **Solution**: Implement circuit breakers and fallback strategies

### Performance Bottlenecks

- **Problem**: Sequential workflows are slow
- **Solution**: Identify parallelizable steps and optimize accordingly

### Complexity Management

- **Problem**: Complex multi-agent systems are hard to debug
- **Solution**: Comprehensive logging, monitoring, and visualization

## Next Steps

Ready for specialized applications?

1. **[RAG Systems](../04_specialized/rag/)** - Multi-agent document processing
2. **[Planning Agents](../04_specialized/planning/)** - Complex task planning
3. **[Game Environments](../04_specialized/games/)** - Multi-agent games
4. **[Advanced Patterns](../05_advanced/)** - Custom multi-agent architectures

## Troubleshooting

### Workflow Hangs

- Check for deadlocks in agent communication
- Verify all async operations are properly awaited
- Monitor resource usage and API rate limits

### Inconsistent Results

- Ensure proper state synchronization
- Validate agent execution order
- Check for race conditions in parallel execution

### Memory Issues

- Monitor shared state size growth
- Implement state cleanup strategies
- Use weak references for large objects

## Resources

- [Multi-Agent Architecture Guide](../../docs/architecture/multi_agents.md)
- [State Management Patterns](../../docs/patterns/state_management.md)
- [Workflow Orchestration](../../docs/guides/workflows.md)
