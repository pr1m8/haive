# Multi-Agent Workflows Guide

**Version**: 1.0  
**Purpose**: Comprehensive guide for creating and managing multi-agent workflows in Haive  
**Last Updated**: 2025-01-16

## 🎯 Overview

This guide covers the complete process of building multi-agent workflows in Haive, from basic sequential patterns to advanced parallelizable tree-based planning systems. The Haive framework provides intelligent routing, automatic sequence inference, and sophisticated branching capabilities.

### Key Features

- **Intelligent Routing**: Automatic task routing based on agent capabilities
- **Sequence Inference**: Smart detection of optimal execution order
- **MetaStateSchema Integration**: Advanced state management for complex workflows
- **Dynamic Recompilation**: Runtime adaptation of workflow graphs
- **Real Component Testing**: No mocks - test with real LLMs and tools
- **Memory-First Architecture**: Built on comprehensive memory system

### Real-World Applications

- **Content Creation**: Research → Write → Edit → Publish pipelines
- **Software Development**: Plan → Code → Test → Review → Deploy workflows
- **Data Processing**: Ingest → Clean → Transform → Analyze → Report chains
- **Customer Service**: Route → Analyze → Respond → Follow-up systems
- **Research Analysis**: Collect → Analyze → Synthesize → Validate processes

## 🏗️ Architecture Foundation

### Core Components

```
BaseGraph (Foundation)
├── Intelligent Routing System
│   ├── Sequence Inference Strategies
│   ├── Branch Routing Logic
│   └── Parallel Execution Management
├── Node Factory System
│   ├── Agent Nodes
│   ├── Tool Nodes
│   └── Validation Nodes
└── State Management
    ├── MultiAgentState
    ├── MetaStateSchema
    └── Field Mapping System
```

### Agent Hierarchy

```
Agent (Base)
├── SimpleAgent (Basic LLM agent)
├── ReactAgent (Reasoning + Tools)
├── RAGAgent (Retrieval + Generation)
└── MultiAgent (Coordinates other agents)
    ├── Sequential Execution
    ├── Parallel Execution
    ├── Conditional Branching
    └── Tree-based Planning
```

## 🚀 Quick Start: Basic Multi-Agent

### 1. Simple Sequential Workflow

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.multi.clean import MultiAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create individual agents
planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(
        prompt_template="Create a plan for: {input}"
    )
)

executor = SimpleAgent(
    name="executor",
    engine=AugLLMConfig(
        prompt_template="Execute the plan: {input}"
    )
)

reviewer = SimpleAgent(
    name="reviewer",
    engine=AugLLMConfig(
        prompt_template="Review the execution: {input}"
    )
)

# Create multi-agent with automatic sequence inference
multi_agent = MultiAgent.create(
    agents=[executor, reviewer, planner],  # Order doesn't matter
    name="workflow_agent",
    execution_mode="infer"  # Automatically infers: planner → executor → reviewer
)

# Execute
result = await multi_agent.arun("Build a Python web application")
```

### 2. Manual Sequence Control

```python
# Create multi-agent with explicit sequence
multi_agent = MultiAgent.create(
    agents=[planner, executor, reviewer],
    name="controlled_workflow",
    execution_mode="sequential"
)

# Set explicit sequence
multi_agent.set_sequence(["planner", "executor", "reviewer"])

# Execute
result = await multi_agent.arun("Build a Python web application")
```

## 🧠 Sequence Inference Strategies

The Haive framework automatically infers execution order using three strategies:

### 1. Naming Pattern Recognition

```python
# Agents with common naming patterns are automatically ordered
agents = [
    SimpleAgent(name="executor", engine=config),      # 2nd - execution phase
    SimpleAgent(name="planner", engine=config),       # 1st - planning phase
    SimpleAgent(name="reviewer", engine=config),      # 3rd - review phase
    SimpleAgent(name="formatter", engine=config),     # 4th - output phase
]

# Automatic inference creates: planner → executor → reviewer → formatter
```

**Common Patterns** (in execution order):

- `planner`, `analyzer`, `researcher` → **Analysis Phase**
- `executor`, `worker`, `processor` → **Execution Phase**
- `validator`, `reviewer`, `critic` → **Review Phase**
- `formatter`, `summarizer`, `output` → **Output Phase**

### 2. Agent Type Recognition

```python
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.rag.base.agent import BaseRAGAgent

# Automatic type-based ordering
agents = [
    SimpleAgent(name="formatter", engine=config),     # 3rd - Simple processing
    ReactAgent(name="reasoner", engine=config),       # 1st - Complex reasoning
    BaseRAGAgent(name="retriever", engine=config),    # 2nd - Information retrieval
]

# Inference creates: ReactAgent → BaseRAGAgent → SimpleAgent
```

**Type Priority**:

1. **ReactAgent** - Complex reasoning first
2. **RAGAgent** - Information retrieval second
3. **SimpleAgent** - Basic processing third
4. **ToolAgent** - Tool usage fourth

### 3. Prompt Dependency Analysis

```python
# Agents with prompt dependencies are automatically ordered
planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(prompt_template="Create plan: {input}")
)

executor = SimpleAgent(
    name="executor",
    engine=AugLLMConfig(prompt_template="Execute plan: {planner_result}")  # Depends on planner
)

reviewer = SimpleAgent(
    name="reviewer",
    engine=AugLLMConfig(prompt_template="Review execution: {executor_output}")  # Depends on executor
)

# Inference creates: planner → executor → reviewer
```

## 🌿 Branch Routing & Conditional Logic

### 1. Basic Branch Configuration

```python
# Create multi-agent with branching
multi_agent = MultiAgent.create(
    agents=[analyzer, success_handler, error_handler],
    name="branching_workflow",
    execution_mode="branch"
)

# Add branch condition
multi_agent.add_branch(
    source_agent="analyzer",
    condition="if success",
    target_agents=["success_handler", "error_handler"]
)

# Execute - analyzer determines next path
result = await multi_agent.arun("Analyze data quality")
```

### 2. Advanced Branch Patterns

```python
# Complex branching with multiple conditions
branches = {
    "analyzer": {
        "condition": "data_quality_check",
        "targets": ["data_cleaner", "validator", "error_handler"]
    },
    "data_cleaner": {
        "condition": "cleaning_success",
        "targets": ["validator", "manual_review"]
    },
    "validator": {
        "condition": "validation_result",
        "targets": ["processor", "error_handler"]
    }
}

multi_agent = MultiAgent(
    agents=agent_dict,
    execution_mode="branch",
    branches=branches
)
```

## 🔄 Parallel Execution Patterns

### 1. Parallel Processing

```python
# Multiple agents processing different aspects
parallel_agents = [
    SimpleAgent(name="text_processor", engine=text_config),
    SimpleAgent(name="image_processor", engine=image_config),
    SimpleAgent(name="metadata_processor", engine=meta_config),
]

multi_agent = MultiAgent.create(
    agents=parallel_agents,
    name="parallel_processor",
    execution_mode="parallel"
)

# All agents execute simultaneously
result = await multi_agent.arun("Process multimedia content")
```

### 2. Fan-out/Fan-in Pattern

```python
# Distribution → Parallel Processing → Aggregation
distributor = SimpleAgent(name="distributor", engine=dist_config)
worker1 = SimpleAgent(name="worker1", engine=worker_config)
worker2 = SimpleAgent(name="worker2", engine=worker_config)
worker3 = SimpleAgent(name="worker3", engine=worker_config)
aggregator = SimpleAgent(name="aggregator", engine=agg_config)

# Configure with Send objects for distribution
graph = BaseGraph(name="fanout_fanin")
graph.add_intelligent_agent_routing(
    agents={
        "distributor": distributor,
        "worker1": worker1,
        "worker2": worker2,
        "worker3": worker3,
        "aggregator": aggregator
    },
    execution_mode="parallel"
)
```

## 🛠️ Advanced BaseGraph Integration

### 1. Direct BaseGraph Usage

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph

# Create graph with intelligent routing
graph = BaseGraph(name="advanced_workflow")

# Add agents with intelligent routing
graph.add_intelligent_agent_routing(
    agents={
        "planner": planner_agent,
        "executor": executor_agent,
        "reviewer": reviewer_agent
    },
    execution_mode="infer",
    prefix="agent_"  # Nodes become: agent_planner, agent_executor, agent_reviewer
)

# Execute graph directly
result = await graph.ainvoke({"input": "Build application"})
```

### 2. Custom Node Integration

```python
# Mix agents with custom nodes
def custom_validation_node(state):
    """Custom validation logic."""
    return {"validated": True, "score": 0.95}

graph = BaseGraph(name="hybrid_workflow")

# Add custom node
graph.add_node("validator", custom_validation_node)

# Add intelligent agent routing
graph.add_intelligent_agent_routing(
    agents={"planner": planner, "executor": executor},
    execution_mode="infer"
)

# Connect custom node to agent routing
graph.add_edge("validator", "planner")
graph.add_edge("executor", END)
```

## 📊 State Management Patterns

### 1. MultiAgentState Usage

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

# Define custom state schema
class WorkflowState(MultiAgentState):
    """Custom state for workflow."""

    # Workflow-specific fields
    plan: Optional[str] = None
    execution_result: Optional[str] = None
    review_score: Optional[float] = None

    # Shared context
    project_context: Dict[str, Any] = Field(default_factory=dict)

# Use with MultiAgent
multi_agent = MultiAgent(
    agents=agents,
    state_schema=WorkflowState,
    execution_mode="infer"
)
```

### 2. MetaStateSchema for Complex Workflows

```python
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Create meta-capable agent
meta_state = MetaStateSchema.from_agent(
    agent=multi_agent,
    initial_state={"workflow_id": "proj_001"},
    graph_context={"project_type": "web_app"}
)

# Execute with full tracking
result = await meta_state.execute_agent(
    input_data={"requirement": "Build e-commerce site"},
    update_state=True
)

# Get execution summary
summary = meta_state.get_execution_summary()
print(f"Executions: {summary['execution_count']}")
```

## 🔧 Tool Integration Patterns

### 1. Shared Tools Across Agents

```python
from langchain_core.tools import tool

@tool
def database_query(query: str) -> str:
    """Query the database."""
    return f"Query result for: {query}"

@tool
def file_processor(filepath: str) -> str:
    """Process a file."""
    return f"Processed file: {filepath}"

# Create agents with shared tools
planner = ReactAgent(
    name="planner",
    engine=config,
    tools=[database_query]  # Planner can query database
)

executor = ReactAgent(
    name="executor",
    engine=config,
    tools=[database_query, file_processor]  # Executor can do both
)

# Tools are automatically available to appropriate agents
```

### 2. Agent-as-Tool Pattern

```python
# Any agent can become a tool for other agents
research_agent = SimpleAgent(name="researcher", engine=research_config)
analysis_agent = SimpleAgent(name="analyzer", engine=analysis_config)

# Convert agents to tools
research_tool = research_agent.as_tool()
analysis_tool = analysis_agent.as_tool()

# Use in other agents
supervisor = ReactAgent(
    name="supervisor",
    engine=supervisor_config,
    tools=[research_tool, analysis_tool]
)
```

### 3. Memory-Aware Tool Integration

```python
from haive.agents.memory import UnifiedMemorySystem, MemorySystemConfig

# Create memory system
memory_config = MemorySystemConfig(
    store_type="memory",
    collection_name="workflow_memories",
    enable_all_features=True
)
memory_system = UnifiedMemorySystem(memory_config)

@tool
def memory_search(query: str) -> str:
    """Search workflow memories."""
    result = asyncio.run(memory_system.retrieve_memories(query))
    if result.success:
        memories = result.result["memories"]
        return f"Found {len(memories)} relevant memories"
    return "No memories found"

@tool
def memory_store(content: str) -> str:
    """Store information in workflow memory."""
    result = asyncio.run(memory_system.store_memory(content))
    if result.success:
        return f"Stored memory: {result.result['memory_id']}"
    return "Failed to store memory"

# Create memory-aware agents
planner = ReactAgent(
    name="planner",
    engine=config,
    tools=[memory_search, memory_store]
)
```

### 4. Dynamic Tool Loading

```python
class DynamicToolAgent(ReactAgent):
    """Agent that can load tools dynamically."""

    def __init__(self, name: str, engine: AugLLMConfig, base_tools: List = None):
        super().__init__(name=name, engine=engine, tools=base_tools or [])
        self.available_tools = self._discover_available_tools()

    def _discover_available_tools(self) -> Dict[str, Any]:
        """Discover available tools from the system."""
        return {
            "web_search": self._create_web_search_tool(),
            "file_operations": self._create_file_tool(),
            "database_query": self._create_db_tool(),
            "api_calls": self._create_api_tool()
        }

    async def load_tool(self, tool_name: str):
        """Load a tool dynamically."""
        if tool_name in self.available_tools:
            new_tool = self.available_tools[tool_name]
            self.tools.append(new_tool)
            # Trigger recompilation if using BaseGraph
            if hasattr(self, 'mark_for_recompile'):
                self.mark_for_recompile(f"Added tool: {tool_name}")
```

## 🎯 Best Practices

### 1. Agent Design

```python
# ✅ GOOD - Clear naming and purpose
planner = SimpleAgent(
    name="requirements_planner",
    engine=AugLLMConfig(
        prompt_template="Analyze requirements and create implementation plan: {input}",
        temperature=0.3  # Lower for planning
    )
)

executor = ReactAgent(
    name="code_executor",
    engine=AugLLMConfig(
        prompt_template="Implement the plan: {plan}",
        temperature=0.7  # Higher for creativity
    ),
    tools=[code_tools]
)

# ❌ AVOID - Vague names and purposes
agent1 = SimpleAgent(name="agent1", engine=config)
agent2 = SimpleAgent(name="agent2", engine=config)
```

### 2. State Schema Design

```python
# ✅ GOOD - Clear state structure
class ProjectWorkflowState(MultiAgentState):
    """State for project development workflow."""

    # Input/Output
    requirements: str = Field(..., description="Project requirements")
    final_output: Optional[str] = Field(None, description="Final deliverable")

    # Intermediate results
    plan: Optional[str] = Field(None, description="Implementation plan")
    code: Optional[str] = Field(None, description="Generated code")
    tests: Optional[str] = Field(None, description="Test results")

    # Metadata
    progress: float = Field(0.0, ge=0.0, le=1.0, description="Completion percentage")
    errors: List[str] = Field(default_factory=list, description="Error log")
```

### 3. Error Handling

```python
# ✅ GOOD - Robust error handling
try:
    result = await multi_agent.arun("Build application")
except Exception as e:
    logger.error(f"Workflow failed: {e}")
    # Implement fallback strategy
    fallback_result = await simple_agent.arun("Create basic structure")
```

## 🧪 Testing Multi-Agent Workflows

### 1. Unit Testing Individual Agents

```python
import pytest
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

@pytest.mark.asyncio
async def test_planner_agent():
    """Test planner agent with real LLM."""
    planner = SimpleAgent(
        name="test_planner",
        engine=AugLLMConfig(temperature=0.1)
    )

    result = await planner.arun("Create a plan for a todo app")

    assert isinstance(result, str)
    assert len(result) > 0
    assert "plan" in result.lower()
```

### 2. Integration Testing Multi-Agent Workflows

```python
@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete multi-agent workflow."""
    # Create workflow
    multi_agent = MultiAgent.create(
        agents=[planner, executor, reviewer],
        name="test_workflow",
        execution_mode="infer"
    )

    # Execute
    result = await multi_agent.arun("Build a simple calculator")

    # Verify
    assert result is not None
    assert multi_agent.conversation_history
    assert len(multi_agent.conversation_history) > 0
```

### 3. Performance Testing

```python
import time
import asyncio

@pytest.mark.asyncio
async def test_parallel_performance():
    """Test parallel execution performance."""
    # Sequential timing
    start = time.time()
    seq_result = await sequential_agent.arun("Process data")
    seq_time = time.time() - start

    # Parallel timing
    start = time.time()
    par_result = await parallel_agent.arun("Process data")
    par_time = time.time() - start

    # Parallel should be faster
    assert par_time < seq_time
```

## 📈 Performance Optimization

### 1. Efficient Agent Configuration

```python
# ✅ GOOD - Optimized configuration
config = AugLLMConfig(
    temperature=0.1,     # Lower for consistency
    max_tokens=500,      # Limit for speed
    model="gpt-4o-mini"  # Faster model for simple tasks
)

# Use appropriate models for different tasks
planning_config = AugLLMConfig(model="gpt-4o")      # Complex reasoning
execution_config = AugLLMConfig(model="gpt-4o-mini") # Simple processing
```

### 2. State Management Optimization

```python
# ✅ GOOD - Efficient state updates
class OptimizedWorkflowState(MultiAgentState):
    """Optimized state with computed fields."""

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Calculate completion based on completed steps."""
        completed = sum(1 for step in self.steps if step.completed)
        return completed / len(self.steps) if self.steps else 0.0
```

### 3. Caching Strategies

```python
# Cache agent results for expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_analysis(input_hash: str) -> str:
    """Cache analysis results."""
    return analysis_agent.run(input_hash)
```

## 🚀 Advanced Patterns

### 1. Memory-Enhanced Multi-Agent Systems

```python
from haive.agents.memory import (
    UnifiedMemorySystem,
    MultiAgentMemoryCoordinator,
    MultiAgentCoordinatorConfig
)

class MemoryEnhancedMultiAgent(MultiAgent):
    """Multi-agent system with comprehensive memory capabilities."""

    def __init__(self, agents: List[Agent], memory_config: MemorySystemConfig):
        super().__init__(agents=agents, name="memory_enhanced")

        # Initialize memory system
        self.memory_system = UnifiedMemorySystem(memory_config)

        # Initialize memory coordinator
        coordinator_config = MultiAgentCoordinatorConfig(
            memory_store_manager=self.memory_system.memory_store,
            memory_classifier=self.memory_system.classifier,
            kg_generator_config=self.memory_system.kg_generator.config,
            agentic_rag_config=self.memory_system.agentic_rag.config
        )
        self.memory_coordinator = MultiAgentMemoryCoordinator(coordinator_config)

    async def execute_with_memory(self, task: str) -> str:
        """Execute task with memory integration."""
        # Store initial task in memory
        await self.memory_system.store_memory(f"Task: {task}")

        # Retrieve relevant memories
        memories = await self.memory_system.retrieve_memories(task, limit=5)

        # Execute with memory context
        context = f"Task: {task}\n\nRelevant memories:\n"
        if memories.success:
            for memory in memories.result["memories"]:
                context += f"- {memory.get('content', '')}\n"

        result = await super().arun(context)

        # Store result in memory
        await self.memory_system.store_memory(f"Result: {result}")

        return result
```

### 2. Recursive Multi-Agent Systems

```python
# Self-improving multi-agent system
class RecursiveMultiAgent(MultiAgent):
    """Multi-agent that can modify its own workflow."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.optimizer_agent = SimpleAgent(
            name="optimizer",
            engine=AugLLMConfig(
                prompt_template="Optimize workflow: {workflow_performance}"
            )
        )
        self.performance_tracker = PerformanceTracker()

    async def optimize_workflow(self):
        """Optimize the workflow based on performance."""
        performance_data = self.performance_tracker.get_metrics()
        optimization = await self.optimizer_agent.arun(str(performance_data))

        # Apply optimization suggestions
        await self.apply_optimization(optimization)

        # Store optimization in memory
        if hasattr(self, 'memory_system'):
            await self.memory_system.store_memory(
                f"Optimization applied: {optimization}"
            )
```

### 3. Dynamic Agent Addition with MetaStateSchema

```python
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

class DynamicMultiAgent(MultiAgent):
    """Multi-agent that can add new agents at runtime."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_agents = {}
        self.agent_factory = AgentFactory()

        # Wrap existing agents in MetaStateSchema
        for agent_name, agent in self.agents.items():
            self.meta_agents[agent_name] = MetaStateSchema.from_agent(
                agent=agent,
                initial_state={"ready": True},
                graph_context={"agent_type": agent.__class__.__name__}
            )

    async def add_specialist_agent(self, task_type: str, requirements: Dict[str, Any]):
        """Add a specialist agent for specific tasks."""
        # Create specialist agent
        specialist = await self.agent_factory.create_specialist(task_type, requirements)

        # Wrap in MetaStateSchema
        meta_specialist = MetaStateSchema.from_agent(
            agent=specialist,
            initial_state={"ready": True, "specialized": True},
            graph_context={"agent_type": "specialist", "task_type": task_type}
        )

        # Add to system
        self.agents[specialist.name] = specialist
        self.meta_agents[specialist.name] = meta_specialist

        # Trigger recompilation
        await self.rebuild_graph()

        # Store in memory
        if hasattr(self, 'memory_system'):
            await self.memory_system.store_memory(
                f"Added specialist agent: {specialist.name} for {task_type}"
            )
```

### 4. Hierarchical Multi-Agent with Supervision

```python
class HierarchicalMultiAgent(MultiAgent):
    """Multi-agent system with hierarchical supervision."""

    def __init__(self, supervisor_config: AugLLMConfig, worker_agents: List[Agent]):
        # Create supervisor agent
        supervisor = SimpleAgent(
            name="supervisor",
            engine=supervisor_config,
            system_message="""You are a supervisor agent coordinating multiple workers.

            Your responsibilities:
            - Analyze incoming tasks
            - Assign tasks to appropriate workers
            - Monitor worker performance
            - Combine worker outputs
            - Provide final results

            Available workers: {worker_names}
            """.format(worker_names=[agent.name for agent in worker_agents])
        )

        # Initialize with supervisor + workers
        all_agents = [supervisor] + worker_agents
        super().__init__(agents=all_agents, name="hierarchical_system")

        self.supervisor = supervisor
        self.workers = {agent.name: agent for agent in worker_agents}

    async def execute_hierarchical(self, task: str) -> str:
        """Execute task with hierarchical coordination."""
        # Supervisor analyzes task
        supervision_prompt = f"""
        Task: {task}

        Available workers: {list(self.workers.keys())}

        Analyze this task and determine:
        1. Which workers should handle it
        2. In what order
        3. What specific instructions to give each worker

        Format your response as a JSON plan.
        """

        plan = await self.supervisor.arun(supervision_prompt)

        # Execute plan (simplified - would need JSON parsing)
        worker_results = {}
        for worker_name in self.workers:
            if worker_name in plan:
                worker_task = f"Task: {task}\nPlan: {plan}"
                worker_results[worker_name] = await self.workers[worker_name].arun(worker_task)

        # Supervisor combines results
        final_prompt = f"""
        Task: {task}
        Worker results: {worker_results}

        Combine these results into a final comprehensive response.
        """

        return await self.supervisor.arun(final_prompt)
```

### 5. Event-Driven Multi-Agent System

```python
import asyncio
from typing import Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentEvent:
    """Event that can trigger agent actions."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime
    source_agent: str = None

class EventDrivenMultiAgent(MultiAgent):
    """Multi-agent system with event-driven coordination."""

    def __init__(self, agents: List[Agent]):
        super().__init__(agents=agents, name="event_driven")

        # Event system
        self.event_queue = asyncio.Queue()
        self.event_handlers = {}
        self.event_history = []

        # Register default handlers
        self._register_default_handlers()

    def register_event_handler(self, event_type: str, handler: Callable):
        """Register handler for specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    async def publish_event(self, event: AgentEvent):
        """Publish event to the system."""
        await self.event_queue.put(event)
        self.event_history.append(event)

    async def start_event_loop(self):
        """Start processing events."""
        while True:
            try:
                event = await self.event_queue.get()
                await self._handle_event(event)
            except asyncio.CancelledError:
                break

    async def _handle_event(self, event: AgentEvent):
        """Handle incoming event."""
        handlers = self.event_handlers.get(event.type, [])

        # Execute handlers in parallel
        tasks = [handler(event) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _register_default_handlers(self):
        """Register default event handlers."""

        async def handle_task_completion(event: AgentEvent):
            """Handle task completion event."""
            if event.type == "task_completed":
                next_agent = self._determine_next_agent(event.data)
                if next_agent:
                    await self._execute_agent(next_agent, event.data)

        async def handle_error(event: AgentEvent):
            """Handle error event."""
            if event.type == "agent_error":
                await self._handle_agent_error(event.data)

        self.register_event_handler("task_completed", handle_task_completion)
        self.register_event_handler("agent_error", handle_error)
```

## 🎯 Common Use Cases

### 1. Content Creation Pipeline

```python
# Research → Write → Edit → Publish
content_pipeline = MultiAgent.create(
    agents=[
        ReactAgent(name="researcher", tools=[web_search, database_query]),
        SimpleAgent(name="writer", engine=creative_config),
        SimpleAgent(name="editor", engine=editing_config),
        SimpleAgent(name="publisher", engine=publishing_config)
    ],
    execution_mode="infer"
)
```

### 2. Code Development Workflow

```python
# Plan → Code → Test → Review → Deploy
dev_workflow = MultiAgent.create(
    agents=[
        SimpleAgent(name="architect", engine=planning_config),
        ReactAgent(name="developer", tools=[code_tools]),
        ReactAgent(name="tester", tools=[test_tools]),
        SimpleAgent(name="reviewer", engine=review_config),
        ReactAgent(name="deployer", tools=[deploy_tools])
    ],
    execution_mode="infer"
)
```

### 3. Data Processing Pipeline

```python
# Ingest → Clean → Transform → Analyze → Report
data_pipeline = MultiAgent.create(
    agents=[
        ReactAgent(name="ingester", tools=[data_connectors]),
        SimpleAgent(name="cleaner", engine=cleaning_config),
        ReactAgent(name="transformer", tools=[transform_tools]),
        SimpleAgent(name="analyzer", engine=analysis_config),
        SimpleAgent(name="reporter", engine=reporting_config)
    ],
    execution_mode="infer"
)
```

## 🔗 Integration with External Systems

### 1. Database Integration

```python
@tool
def query_database(query: str) -> str:
    """Query PostgreSQL database."""
    # Use MCP PostgreSQL server
    return execute_sql_query(query)

# Use in agents
data_agent = ReactAgent(
    name="data_analyst",
    engine=config,
    tools=[query_database]
)
```

### 2. API Integration

```python
@tool
def call_external_api(endpoint: str, data: dict) -> dict:
    """Call external REST API."""
    return make_api_call(endpoint, data)

# Use in agents
api_agent = ReactAgent(
    name="api_coordinator",
    engine=config,
    tools=[call_external_api]
)
```

## 📚 Next Steps

1. **Implement Basic Workflow** - Start with simple sequential pattern
2. **Add Branching Logic** - Implement conditional routing
3. **Optimize Performance** - Use parallel execution where appropriate
4. **Add Error Handling** - Implement robust error recovery
5. **Monitor & Iterate** - Track performance and optimize

---

**Remember**: Multi-agent workflows are powerful but complex. Start simple, test thoroughly, and build incrementally. The Haive framework provides the foundation - your creativity defines the possibilities.
