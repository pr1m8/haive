# MultiAgent Consolidation Implementation Plan

**Domain**: MultiAgent Patterns  
**Estimated Days**: 4-5 days  
**Target LOC**: 3,000 LOC (from 5,000 LOC - 40% reduction)  
**Dependencies**: [Agent](../agent/AGENT_CLEANUP_PLAN.md), [Workflow](../workflow/WORKFLOW_CREATION_PLAN.md), [Schema](../schema/SCHEMA_MODULARIZATION_PLAN.md)

## 🎯 Overview

Consolidate 8 different multi-agent implementations into 6 clear, focused patterns. Transform complex inheritance-based multi-agent systems into simple composition patterns using the new agent and workflow layers.

## 📊 Current State Analysis

### The MultiAgent Complexity Problem

```bash
# Current multi-agent structure (5,000 total LOC)
packages/haive-agents/src/haive/agents/multi/
├── enhanced_multi_agent_v4.py          # 2,000 LOC - The monster
├── multi_agent.py                      # 800 LOC - Basic multi-agent
├── sequential_agent.py                 # 400 LOC - Sequential pattern
├── parallel_agent.py                   # 350 LOC - Parallel pattern
├── conditional_agent.py                # 450 LOC - Conditional routing
├── hierarchical_agent.py               # 600 LOC - Hierarchical patterns
├── coordinator_agent.py                # 250 LOC - Agent coordination
└── meta_agent.py                       # 150 LOC - Meta capabilities
```

### Key Problems Identified

1. **Pattern Overlap**: Multiple implementations of similar coordination patterns
2. **Version Inflation**: "v4" suggests multiple failed attempts at clean design
3. **Monolithic Design**: Single files trying to handle all multi-agent patterns
4. **Mixed Concerns**: Coordination logic + agent logic + workflow logic together
5. **Complex Inheritance**: Deep inheritance chains making changes risky

### MultiAgent Responsibility Analysis

| Current Implementation | Agent Management | Workflow Coordination | State Management | Meta Capabilities |
| ---------------------- | ---------------- | --------------------- | ---------------- | ----------------- |
| EnhancedMultiAgentV4   | ✅               | ✅                    | ✅               | ✅                |
| MultiAgent             | ✅               | ✅                    | ✅               | ❌                |
| SequentialAgent        | ✅               | ✅                    | ❌               | ❌                |
| ParallelAgent          | ✅               | ✅                    | ❌               | ❌                |
| ConditionalAgent       | ✅               | ✅                    | ✅               | ❌                |

**Problem**: Every multi-agent tries to handle everything rather than focusing on coordination patterns.

## 🏗️ Target Architecture

### Clean MultiAgent Structure (3,000 total LOC)

```
packages/haive-agents/src/haive/agents/multi/
├── __init__.py                         # Multi-agent exports (50 LOC)
├── base/
│   ├── __init__.py                    # Base exports (30 LOC)
│   ├── multi_agent_base.py            # Core multi-agent pattern (400 LOC)
│   └── coordination_protocol.py       # Coordination interface (150 LOC)
├── sequential.py                       # Sequential multi-agent (300 LOC)
├── parallel.py                        # Parallel multi-agent (350 LOC)
├── conditional.py                     # Conditional routing (400 LOC)
├── hierarchical.py                    # Hierarchical coordination (450 LOC)
├── meta_agent.py                      # Meta-capabilities (500 LOC)
├── composition/
│   ├── __init__.py                    # Composition exports (20 LOC)
│   ├── agent_registry.py              # Agent registration (200 LOC)
│   └── coordination_patterns.py       # Common patterns (300 LOC)
└── legacy/
    ├── __init__.py                    # Legacy exports (30 LOC)
    └── enhanced_multi_v4_facade.py    # Backward compatibility (320 LOC)
```

**Total**: 10 focused files, ~3,000 LOC (40% reduction)

### Design Principles

1. **Composition over Inheritance**: Multi-agents compose individual agents and workflows
2. **Single Coordination Pattern**: Each multi-agent handles one coordination approach
3. **Workflow Delegation**: Complex orchestration uses workflow layer
4. **Agent Independence**: Individual agents remain independent and testable
5. **Clear Interfaces**: All multi-agents implement coordination protocol

## 📋 Detailed Implementation Steps

### Step 1: Base Multi-Agent Infrastructure (Day 1)

#### 1.1 Coordination Protocol

**File**: `base/coordination_protocol.py`

```python
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Generic
from haive.core.contracts.agent.multi_agent_protocol import MultiAgentProtocol
from haive.agents.base.agent import Agent
from enum import Enum

CoordinationResultT = TypeVar('CoordinationResultT')

class CoordinationMode(str, Enum):
    """Multi-agent coordination modes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HIERARCHICAL = "hierarchical"
    META = "meta"

class CoordinationProtocol(Protocol, Generic[CoordinationResultT]):
    """Protocol for multi-agent coordination."""

    def add_agent(self, name: str, agent: Agent, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add agent to coordination."""
        ...

    def remove_agent(self, name: str) -> None:
        """Remove agent from coordination."""
        ...

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name."""
        ...

    def list_agents(self) -> List[str]:
        """List all agent names."""
        ...

    async def coordinate(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> CoordinationResultT:
        """Execute coordination strategy."""
        ...

    def get_coordination_mode(self) -> CoordinationMode:
        """Get coordination mode."""
        ...

class AgentMetadata:
    """Metadata for agents in multi-agent systems."""

    def __init__(
        self,
        name: str,
        priority: int = 0,
        dependencies: List[str] = None,
        capabilities: List[str] = None,
        **kwargs
    ):
        self.name = name
        self.priority = priority
        self.dependencies = dependencies or []
        self.capabilities = capabilities or []
        self.extra = kwargs

    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability."""
        return capability in self.capabilities

    def depends_on(self, agent_name: str) -> bool:
        """Check if agent depends on another agent."""
        return agent_name in self.dependencies
```

#### 1.2 Base Multi-Agent Implementation

**File**: `base/multi_agent_base.py`

```python
from typing import Any, Dict, List, Optional, TypeVar
from pydantic import BaseModel, Field
from haive.agents.base.agent import Agent
from haive.core.workflow.base.base_workflow import BaseWorkflow
from .coordination_protocol import CoordinationProtocol, CoordinationMode, AgentMetadata

CoordinationResultT = TypeVar('CoordinationResultT')

class MultiAgentBase(BaseModel, CoordinationProtocol[Dict[str, Any]]):
    """Base class for all multi-agent implementations."""

    # Core multi-agent configuration
    name: str = Field(..., description="Multi-agent system name")
    coordination_mode: CoordinationMode = Field(..., description="Coordination strategy")

    # Agent registry
    agents: Dict[str, Agent] = Field(default_factory=dict, description="Registered agents")
    agent_metadata: Dict[str, AgentMetadata] = Field(default_factory=dict, description="Agent metadata")

    # Coordination workflow
    coordination_workflow: Optional[BaseWorkflow] = Field(default=None, description="Coordination workflow")

    # Multi-agent state
    shared_context: Dict[str, Any] = Field(default_factory=dict, description="Shared context")
    execution_history: List[Dict[str, Any]] = Field(default_factory=list, description="Execution history")

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        extra = "forbid"

    def add_agent(self, name: str, agent: Agent, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add agent to multi-agent system."""
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists")

        self.agents[name] = agent
        self.agent_metadata[name] = AgentMetadata(name=name, **(metadata or {}))

        # Update coordination workflow if needed
        self._update_coordination_workflow()

    def remove_agent(self, name: str) -> None:
        """Remove agent from multi-agent system."""
        if name not in self.agents:
            raise ValueError(f"Agent '{name}' not found")

        self.agents.pop(name)
        self.agent_metadata.pop(name)

        # Update coordination workflow
        self._update_coordination_workflow()

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name."""
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        """List all agent names."""
        return list(self.agents.keys())

    def get_coordination_mode(self) -> CoordinationMode:
        """Get coordination mode."""
        return self.coordination_mode

    async def coordinate(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute coordination strategy - implement in subclasses."""
        raise NotImplementedError("Subclasses must implement coordinate method")

    def update_shared_context(self, updates: Dict[str, Any]) -> None:
        """Update shared context."""
        self.shared_context.update(updates)

    def get_agents_by_capability(self, capability: str) -> List[str]:
        """Get agents with specific capability."""
        return [
            name for name, metadata in self.agent_metadata.items()
            if metadata.has_capability(capability)
        ]

    def get_agent_dependencies(self, agent_name: str) -> List[str]:
        """Get dependencies for specific agent."""
        if agent_name not in self.agent_metadata:
            return []
        return self.agent_metadata[agent_name].dependencies

    def validate_dependency_graph(self) -> List[str]:
        """Validate agent dependency graph for cycles."""
        errors = []

        def has_cycle(start_agent: str, visited: set, path: set) -> bool:
            if start_agent in path:
                return True
            if start_agent in visited:
                return False

            visited.add(start_agent)
            path.add(start_agent)

            dependencies = self.get_agent_dependencies(start_agent)
            for dep in dependencies:
                if has_cycle(dep, visited, path):
                    return True

            path.remove(start_agent)
            return False

        visited = set()
        for agent_name in self.agents:
            if agent_name not in visited:
                if has_cycle(agent_name, visited, set()):
                    errors.append(f"Circular dependency detected involving agent '{agent_name}'")

        return errors

    def _update_coordination_workflow(self) -> None:
        """Update coordination workflow when agents change - implement in subclasses."""
        pass

    def _record_execution(self, input_data: Any, result: Any, metadata: Dict[str, Any]) -> None:
        """Record execution in history."""
        execution_record = {
            "timestamp": datetime.now(),
            "input": input_data,
            "result": result,
            "coordination_mode": self.coordination_mode.value,
            "agents_involved": list(self.agents.keys()),
            "metadata": metadata
        }
        self.execution_history.append(execution_record)

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        return {
            "total_executions": len(self.execution_history),
            "coordination_mode": self.coordination_mode.value,
            "agent_count": len(self.agents),
            "last_execution": self.execution_history[-1] if self.execution_history else None
        }
```

### Step 2: Sequential Multi-Agent (Day 2)

#### 2.1 Sequential Coordination

**File**: `sequential.py`

```python
from typing import Any, Dict, List, Optional
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from .base.multi_agent_base import MultiAgentBase
from .base.coordination_protocol import CoordinationMode

class SequentialMultiAgent(MultiAgentBase):
    """Multi-agent system with sequential execution."""

    def __init__(
        self,
        name: str,
        agents: Optional[List[Any]] = None,
        fail_fast: bool = True,
        **kwargs
    ):
        super().__init__(
            name=name,
            coordination_mode=CoordinationMode.SEQUENTIAL,
            **kwargs
        )

        self.fail_fast = fail_fast

        # Add agents if provided
        if agents:
            for i, agent in enumerate(agents):
                agent_name = getattr(agent, 'name', f'agent_{i}')
                self.add_agent(agent_name, agent)

        # Create coordination workflow
        self._create_coordination_workflow()

    def _create_coordination_workflow(self) -> None:
        """Create sequential coordination workflow."""
        workflow = SequentialWorkflow(
            name=f"{self.name}_sequential_coordination",
            fail_fast=self.fail_fast
        )

        # Add agent execution steps
        for agent_name in self.agents:
            def create_agent_step(name: str):
                async def agent_step(data, context):
                    agent = self.agents[name]

                    # Prepare agent input
                    agent_input = self._prepare_agent_input(data, name, context)

                    # Execute agent
                    agent_result = await agent.arun(agent_input)

                    # Process agent output
                    processed_result = self._process_agent_output(agent_result, name, context)

                    return {
                        **data,
                        f"{name}_result": processed_result,
                        "last_agent": name,
                        "agent_outputs": {
                            **data.get("agent_outputs", {}),
                            name: processed_result
                        }
                    }

                return agent_step

            workflow.add_step(create_agent_step(agent_name), agent_name)

        self.coordination_workflow = workflow

    async def coordinate(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute sequential coordination."""
        if not self.agents:
            raise ValueError("No agents registered for coordination")

        # Prepare coordination input
        coordination_input = {
            "original_input": input_data,
            "shared_context": self.shared_context,
            "coordination_context": context or {},
            "agent_outputs": {}
        }

        # Execute coordination workflow
        workflow_result = await self.coordination_workflow.aexecute(coordination_input)

        # Process final result
        final_result = {
            "coordination_mode": "sequential",
            "agents_executed": list(self.agents.keys()),
            "individual_results": workflow_result.get("agent_outputs", {}),
            "final_output": workflow_result.get("final_result"),
            "workflow_metadata": {
                "steps_completed": workflow_result.get("steps_completed", 0),
                "execution_successful": workflow_result.get("workflow_type") == "sequential"
            }
        }

        # Record execution
        self._record_execution(input_data, final_result, {
            "coordination_mode": "sequential",
            "agents_count": len(self.agents)
        })

        return final_result

    def _prepare_agent_input(self, data: Dict[str, Any], agent_name: str, context: Dict[str, Any]) -> Any:
        """Prepare input for specific agent."""
        # Get previous agent results for context
        agent_outputs = data.get("agent_outputs", {})

        # Build agent input
        agent_input = {
            "query": data.get("original_input", ""),
            "previous_results": agent_outputs,
            "shared_context": self.shared_context,
            "agent_context": context.get(agent_name, {})
        }

        return agent_input

    def _process_agent_output(self, agent_result: Any, agent_name: str, context: Dict[str, Any]) -> Any:
        """Process output from specific agent."""
        # Extract key information
        if isinstance(agent_result, dict):
            return agent_result
        else:
            return {"content": str(agent_result), "source_agent": agent_name}

    def _update_coordination_workflow(self) -> None:
        """Update coordination workflow when agents change."""
        self._create_coordination_workflow()

    def set_agent_order(self, agent_names: List[str]) -> None:
        """Set execution order of agents."""
        # Validate all agents exist
        for name in agent_names:
            if name not in self.agents:
                raise ValueError(f"Agent '{name}' not found")

        # Reorder agents dictionary
        ordered_agents = {name: self.agents[name] for name in agent_names}
        self.agents = ordered_agents

        # Recreate workflow with new order
        self._create_coordination_workflow()

# Factory function
def create_sequential_multi_agent(
    name: str,
    agents: List[Any],
    fail_fast: bool = True
) -> SequentialMultiAgent:
    """Factory for creating sequential multi-agent systems."""
    return SequentialMultiAgent(
        name=name,
        agents=agents,
        fail_fast=fail_fast
    )
```

### Step 3: Parallel Multi-Agent (Day 2.5)

#### 3.1 Parallel Coordination

**File**: `parallel.py`

```python
import asyncio
from typing import Any, Dict, List, Optional
from haive.core.workflow.parallel_workflow import ParallelWorkflow
from .base.multi_agent_base import MultiAgentBase
from .base.coordination_protocol import CoordinationMode

class ParallelMultiAgent(MultiAgentBase):
    """Multi-agent system with parallel execution."""

    def __init__(
        self,
        name: str,
        agents: Optional[List[Any]] = None,
        max_concurrent: Optional[int] = None,
        wait_for_all: bool = True,
        **kwargs
    ):
        super().__init__(
            name=name,
            coordination_mode=CoordinationMode.PARALLEL,
            **kwargs
        )

        self.max_concurrent = max_concurrent
        self.wait_for_all = wait_for_all

        # Add agents if provided
        if agents:
            for i, agent in enumerate(agents):
                agent_name = getattr(agent, 'name', f'agent_{i}')
                self.add_agent(agent_name, agent)

        # Create coordination workflow
        self._create_coordination_workflow()

    def _create_coordination_workflow(self) -> None:
        """Create parallel coordination workflow."""
        workflow = ParallelWorkflow(
            name=f"{self.name}_parallel_coordination",
            max_concurrent=self.max_concurrent,
            wait_for_all=self.wait_for_all
        )

        # Add agent execution steps
        for agent_name in self.agents:
            def create_agent_step(name: str):
                async def agent_step(data, context):
                    agent = self.agents[name]

                    # Prepare agent input (independent for parallel execution)
                    agent_input = self._prepare_agent_input(data, name, context)

                    # Execute agent
                    agent_result = await agent.arun(agent_input)

                    # Process agent output
                    processed_result = self._process_agent_output(agent_result, name, context)

                    return {
                        "agent_name": name,
                        "result": processed_result,
                        "execution_metadata": {
                            "agent_type": agent.agent_type if hasattr(agent, 'agent_type') else 'unknown',
                            "input_size": len(str(agent_input)),
                            "output_size": len(str(processed_result))
                        }
                    }

                return agent_step

            workflow.add_step(create_agent_step(agent_name), agent_name)

        self.coordination_workflow = workflow

    async def coordinate(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute parallel coordination."""
        if not self.agents:
            raise ValueError("No agents registered for coordination")

        # Prepare coordination input
        coordination_input = {
            "original_input": input_data,
            "shared_context": self.shared_context,
            "coordination_context": context or {}
        }

        # Execute coordination workflow
        workflow_result = await self.coordination_workflow.aexecute(coordination_input)

        # Process parallel results
        successful_results = workflow_result.get("successful_results", {})
        failed_results = workflow_result.get("failed_results", {})

        # Merge successful results
        merged_output = self._merge_parallel_results(successful_results)

        final_result = {
            "coordination_mode": "parallel",
            "agents_executed": list(successful_results.keys()),
            "agents_failed": list(failed_results.keys()),
            "individual_results": successful_results,
            "failed_results": failed_results,
            "merged_output": merged_output,
            "workflow_metadata": {
                "successful_count": len(successful_results),
                "failed_count": len(failed_results),
                "total_agents": len(self.agents),
                "success_rate": len(successful_results) / len(self.agents) if self.agents else 0
            }
        }

        # Record execution
        self._record_execution(input_data, final_result, {
            "coordination_mode": "parallel",
            "max_concurrent": self.max_concurrent,
            "wait_for_all": self.wait_for_all
        })

        return final_result

    def _prepare_agent_input(self, data: Dict[str, Any], agent_name: str, context: Dict[str, Any]) -> Any:
        """Prepare input for specific agent (independent for parallel execution)."""
        agent_input = {
            "query": data.get("original_input", ""),
            "shared_context": self.shared_context,
            "agent_context": context.get(agent_name, {}),
            "agent_name": agent_name
        }

        return agent_input

    def _process_agent_output(self, agent_result: Any, agent_name: str, context: Dict[str, Any]) -> Any:
        """Process output from specific agent."""
        if isinstance(agent_result, dict):
            return {**agent_result, "source_agent": agent_name}
        else:
            return {"content": str(agent_result), "source_agent": agent_name}

    def _merge_parallel_results(self, successful_results: Dict[str, Any]) -> Dict[str, Any]:
        """Merge results from parallel agent execution."""
        merged = {
            "combined_content": [],
            "agent_contributions": {},
            "consensus_items": [],
            "unique_insights": []
        }

        for agent_name, result in successful_results.items():
            # Extract content
            content = result.get("content", str(result))
            merged["combined_content"].append(f"[{agent_name}]: {content}")

            # Store agent contribution
            merged["agent_contributions"][agent_name] = result

            # Look for common themes (simplified analysis)
            if isinstance(result, dict) and "key_points" in result:
                for point in result["key_points"]:
                    # Simple consensus detection
                    count = sum(1 for other_result in successful_results.values()
                              if isinstance(other_result, dict)
                              and "key_points" in other_result
                              and point in str(other_result["key_points"]))

                    if count > 1:
                        merged["consensus_items"].append(point)
                    else:
                        merged["unique_insights"].append(f"[{agent_name}]: {point}")

        return merged

    def _update_coordination_workflow(self) -> None:
        """Update coordination workflow when agents change."""
        self._create_coordination_workflow()

    def set_concurrency_limit(self, max_concurrent: Optional[int]) -> None:
        """Set maximum concurrent agent executions."""
        self.max_concurrent = max_concurrent
        self._create_coordination_workflow()

# Factory function
def create_parallel_multi_agent(
    name: str,
    agents: List[Any],
    max_concurrent: Optional[int] = None,
    wait_for_all: bool = True
) -> ParallelMultiAgent:
    """Factory for creating parallel multi-agent systems."""
    return ParallelMultiAgent(
        name=name,
        agents=agents,
        max_concurrent=max_concurrent,
        wait_for_all=wait_for_all
    )
```

### Step 4: Meta-Agent Implementation (Day 3)

#### 4.1 Meta-Capabilities

**File**: `meta_agent.py`

```python
from typing import Any, Dict, List, Optional, Callable
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from haive.agents.base.agent import Agent
from .base.multi_agent_base import MultiAgentBase
from .base.coordination_protocol import CoordinationMode

class MetaAgent(MultiAgentBase):
    """Multi-agent system with meta-learning and self-modification capabilities."""

    def __init__(
        self,
        name: str,
        agents: Optional[List[Any]] = None,
        meta_state_schema: Optional[MetaStateSchema] = None,
        adaptation_threshold: float = 0.7,
        **kwargs
    ):
        super().__init__(
            name=name,
            coordination_mode=CoordinationMode.META,
            **kwargs
        )

        self.meta_state = meta_state_schema or MetaStateSchema()
        self.adaptation_threshold = adaptation_threshold
        self.performance_history: List[Dict[str, float]] = []

        # Add agents if provided
        if agents:
            for i, agent in enumerate(agents):
                agent_name = getattr(agent, 'name', f'agent_{i}')
                self.add_agent(agent_name, agent)
                # Register agent in meta state
                self.meta_state.register_agent(agent_name, type(agent).__name__)

    async def coordinate(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute meta-coordination with self-adaptation."""
        if not self.agents:
            raise ValueError("No agents registered for meta-coordination")

        # Analyze input and select best coordination strategy
        coordination_strategy = await self._analyze_and_select_strategy(input_data, context)

        # Execute with selected strategy
        if coordination_strategy == "sequential":
            result = await self._execute_sequential(input_data, context)
        elif coordination_strategy == "parallel":
            result = await self._execute_parallel(input_data, context)
        elif coordination_strategy == "adaptive":
            result = await self._execute_adaptive(input_data, context)
        else:
            result = await self._execute_default(input_data, context)

        # Learn from execution
        await self._learn_from_execution(input_data, result, coordination_strategy)

        # Check if adaptation is needed
        await self._check_and_adapt()

        return result

    async def _analyze_and_select_strategy(self, input_data: Any, context: Optional[Dict[str, Any]]) -> str:
        """Analyze input and select best coordination strategy."""
        # Simple strategy selection based on input characteristics
        input_text = str(input_data)

        # Analyze input complexity
        complexity_score = len(input_text.split()) / 100.0  # Simple metric

        # Check if input requires parallel processing
        parallel_keywords = ["compare", "analyze all", "multiple", "each"]
        needs_parallel = any(keyword in input_text.lower() for keyword in parallel_keywords)

        # Check if input requires sequential processing
        sequential_keywords = ["step by step", "then", "after", "following"]
        needs_sequential = any(keyword in input_text.lower() for keyword in sequential_keywords)

        # Check performance history for best strategy
        if self.performance_history:
            recent_performance = self.performance_history[-5:]  # Last 5 executions
            strategy_performance = {}

            for perf in recent_performance:
                strategy = perf.get("strategy", "default")
                score = perf.get("success_score", 0.5)

                if strategy not in strategy_performance:
                    strategy_performance[strategy] = []
                strategy_performance[strategy].append(score)

            # Find best performing strategy
            best_strategy = "default"
            best_score = 0.0

            for strategy, scores in strategy_performance.items():
                avg_score = sum(scores) / len(scores)
                if avg_score > best_score:
                    best_score = avg_score
                    best_strategy = strategy

            # Use best strategy if performance is good enough
            if best_score > self.adaptation_threshold:
                return best_strategy

        # Fallback to heuristic selection
        if needs_parallel and not needs_sequential:
            return "parallel"
        elif needs_sequential and not needs_parallel:
            return "sequential"
        elif complexity_score > 0.5:
            return "adaptive"
        else:
            return "sequential"  # Default

    async def _execute_sequential(self, input_data: Any, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute with sequential strategy."""
        results = {}
        current_input = input_data

        for agent_name, agent in self.agents.items():
            agent_result = await agent.arun(current_input)
            results[agent_name] = agent_result

            # Update input for next agent
            if isinstance(agent_result, str):
                current_input = agent_result
            else:
                current_input = agent_result

        return {
            "coordination_strategy": "sequential",
            "individual_results": results,
            "final_output": current_input
        }

    async def _execute_parallel(self, input_data: Any, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute with parallel strategy."""
        import asyncio

        # Execute all agents in parallel
        tasks = []
        for agent_name, agent in self.agents.items():
            task = agent.arun(input_data)
            tasks.append((agent_name, task))

        # Gather results
        results = {}
        for agent_name, task in tasks:
            try:
                result = await task
                results[agent_name] = result
            except Exception as e:
                results[agent_name] = {"error": str(e)}

        # Merge results
        merged_output = self._merge_parallel_results(results)

        return {
            "coordination_strategy": "parallel",
            "individual_results": results,
            "final_output": merged_output
        }

    async def _execute_adaptive(self, input_data: Any, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute with adaptive strategy."""
        # Start with one agent, then decide whether to continue
        agent_names = list(self.agents.keys())
        if not agent_names:
            return {"error": "No agents available"}

        # Execute first agent
        first_agent = self.agents[agent_names[0]]
        first_result = await first_agent.arun(input_data)

        # Analyze if more agents are needed
        confidence = self._analyze_result_confidence(first_result)

        if confidence > self.adaptation_threshold:
            # First result is confident, return it
            return {
                "coordination_strategy": "adaptive",
                "agents_used": [agent_names[0]],
                "final_output": first_result,
                "confidence": confidence
            }
        else:
            # Need more agents, execute remaining in parallel
            remaining_agents = agent_names[1:]
            if not remaining_agents:
                return {
                    "coordination_strategy": "adaptive",
                    "agents_used": [agent_names[0]],
                    "final_output": first_result,
                    "confidence": confidence
                }

            # Execute remaining agents
            tasks = []
            for agent_name in remaining_agents:
                agent = self.agents[agent_name]
                task = agent.arun(input_data)
                tasks.append((agent_name, task))

            # Gather additional results
            additional_results = {agent_names[0]: first_result}
            for agent_name, task in tasks:
                try:
                    result = await task
                    additional_results[agent_name] = result
                except Exception as e:
                    additional_results[agent_name] = {"error": str(e)}

            # Merge all results
            final_output = self._merge_adaptive_results(additional_results)

            return {
                "coordination_strategy": "adaptive",
                "agents_used": list(additional_results.keys()),
                "individual_results": additional_results,
                "final_output": final_output,
                "initial_confidence": confidence
            }

    async def _execute_default(self, input_data: Any, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute with default strategy."""
        return await self._execute_sequential(input_data, context)

    def _analyze_result_confidence(self, result: Any) -> float:
        """Analyze confidence in a result."""
        # Simple confidence analysis
        if isinstance(result, dict):
            if "confidence" in result:
                return float(result["confidence"])
            if "error" in result:
                return 0.1
            # Analyze content length and completeness
            content_score = min(len(str(result)) / 1000, 1.0)
            return 0.5 + (content_score * 0.3)

        elif isinstance(result, str):
            # Analyze string result
            if len(result) < 50:
                return 0.4  # Too short, likely incomplete
            if len(result) > 1000:
                return 0.8  # Comprehensive response
            return 0.6  # Reasonable length

        return 0.5  # Unknown type, medium confidence

    def _merge_adaptive_results(self, results: Dict[str, Any]) -> Any:
        """Merge results from adaptive execution."""
        if not results:
            return None

        # Find highest confidence result
        best_result = None
        best_confidence = 0.0

        for agent_name, result in results.items():
            confidence = self._analyze_result_confidence(result)
            if confidence > best_confidence:
                best_confidence = confidence
                best_result = result

        # If we have multiple good results, combine them
        good_results = []
        for agent_name, result in results.items():
            confidence = self._analyze_result_confidence(result)
            if confidence > 0.6:
                good_results.append(result)

        if len(good_results) > 1:
            # Combine multiple good results
            return {
                "primary_result": best_result,
                "supporting_results": good_results,
                "combined_confidence": best_confidence
            }
        else:
            return best_result

    async def _learn_from_execution(self, input_data: Any, result: Dict[str, Any], strategy: str) -> None:
        """Learn from execution results."""
        # Calculate success score
        success_score = self._calculate_success_score(result)

        # Record performance
        performance_record = {
            "strategy": strategy,
            "success_score": success_score,
            "input_complexity": len(str(input_data)) / 1000,
            "agents_used": result.get("agents_used", list(self.agents.keys())),
            "timestamp": datetime.now().isoformat()
        }

        self.performance_history.append(performance_record)

        # Keep only recent history
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]

        # Update meta state
        await self.meta_state.execute_agent({
            "action": "record_performance",
            "data": performance_record
        })

    def _calculate_success_score(self, result: Dict[str, Any]) -> float:
        """Calculate success score for an execution."""
        # Simple success scoring
        base_score = 0.5

        # Check for errors
        if "error" in result or any("error" in str(v) for v in result.values()):
            base_score -= 0.3

        # Check for completeness
        if result.get("final_output"):
            base_score += 0.2

        # Check for confidence indicators
        if "confidence" in result:
            confidence = float(result["confidence"])
            base_score += (confidence - 0.5) * 0.4

        return max(0.0, min(1.0, base_score))

    async def _check_and_adapt(self) -> None:
        """Check if adaptation is needed and perform it."""
        if len(self.performance_history) < 10:
            return  # Not enough data for adaptation

        # Analyze recent performance
        recent_performance = self.performance_history[-10:]
        avg_performance = sum(p["success_score"] for p in recent_performance) / len(recent_performance)

        if avg_performance < self.adaptation_threshold:
            # Performance is below threshold, need adaptation
            await self._perform_adaptation()

    async def _perform_adaptation(self) -> None:
        """Perform meta-level adaptation."""
        # Analyze which strategies are performing poorly
        strategy_performance = {}
        for perf in self.performance_history[-20:]:
            strategy = perf["strategy"]
            score = perf["success_score"]

            if strategy not in strategy_performance:
                strategy_performance[strategy] = []
            strategy_performance[strategy].append(score)

        # Find worst performing strategy
        worst_strategy = None
        worst_score = 1.0

        for strategy, scores in strategy_performance.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < worst_score:
                worst_score = avg_score
                worst_strategy = strategy

        # Adapt by modifying thresholds or adding new agents
        if worst_strategy:
            # Lower threshold for this strategy
            self.adaptation_threshold = max(0.5, self.adaptation_threshold - 0.1)

            # Record adaptation
            await self.meta_state.execute_agent({
                "action": "adapt",
                "worst_strategy": worst_strategy,
                "new_threshold": self.adaptation_threshold
            })

# Factory function
def create_meta_agent(
    name: str,
    agents: List[Any],
    adaptation_threshold: float = 0.7
) -> MetaAgent:
    """Factory for creating meta-agents."""
    return MetaAgent(
        name=name,
        agents=agents,
        adaptation_threshold=adaptation_threshold
    )
```

### Step 5: Backward Compatibility (Day 4)

#### 5.1 Enhanced Multi-Agent V4 Facade

**File**: `legacy/enhanced_multi_v4_facade.py`

```python
from typing import Any, Dict, List, Optional
from ..sequential import SequentialMultiAgent
from ..parallel import ParallelMultiAgent
from ..conditional import ConditionalMultiAgent
from ..meta_agent import MetaAgent

class EnhancedMultiAgentV4:
    """Backward compatibility facade for EnhancedMultiAgentV4."""

    def __init__(
        self,
        agents: List[Any] = None,
        execution_mode: str = "sequential",
        **kwargs
    ):
        """Initialize with legacy parameters."""
        self.agents_list = agents or []
        self.execution_mode = execution_mode
        self._name = kwargs.get('name', 'enhanced_multi_agent_v4')

        # Create appropriate multi-agent implementation
        if execution_mode == "sequential":
            self._impl = SequentialMultiAgent(
                name=self._name,
                agents=self.agents_list,
                **kwargs
            )
        elif execution_mode == "parallel":
            self._impl = ParallelMultiAgent(
                name=self._name,
                agents=self.agents_list,
                **kwargs
            )
        elif execution_mode == "parallel_then_sequential":
            # Use conditional with parallel first, then sequential
            self._impl = ConditionalMultiAgent(
                name=self._name,
                agents=self.agents_list,
                **kwargs
            )
        elif execution_mode == "meta":
            self._impl = MetaAgent(
                name=self._name,
                agents=self.agents_list,
                **kwargs
            )
        else:
            # Default to sequential
            self._impl = SequentialMultiAgent(
                name=self._name,
                agents=self.agents_list,
                **kwargs
            )

    # Legacy property accessors
    @property
    def agents(self) -> Dict[str, Any]:
        """Get agents dictionary."""
        return self._impl.agents

    @property
    def execution_mode(self) -> str:
        """Get execution mode."""
        return self._execution_mode

    @execution_mode.setter
    def execution_mode(self, value: str) -> None:
        """Set execution mode."""
        self._execution_mode = value
        # Would need to recreate implementation here

    # Legacy methods
    async def arun(self, input_data: Any, **kwargs) -> Any:
        """Execute multi-agent (legacy interface)."""
        result = await self._impl.coordinate(input_data, kwargs)

        # Transform result to legacy format
        if "final_output" in result:
            return result["final_output"]
        elif "merged_output" in result:
            return result["merged_output"]
        else:
            return result

    def run(self, input_data: Any, **kwargs) -> Any:
        """Execute multi-agent synchronously (legacy interface)."""
        import asyncio
        return asyncio.run(self.arun(input_data, **kwargs))

    def add_agent(self, agent: Any, name: Optional[str] = None) -> None:
        """Add agent (legacy interface)."""
        agent_name = name or getattr(agent, 'name', f'agent_{len(self.agents_list)}')
        self._impl.add_agent(agent_name, agent)
        self.agents_list.append(agent)

    def remove_agent(self, name: str) -> None:
        """Remove agent (legacy interface)."""
        self._impl.remove_agent(name)
        # Remove from agents list
        self.agents_list = [agent for agent in self.agents_list
                          if getattr(agent, 'name', '') != name]

# Legacy class aliases for backward compatibility
MultiAgent = SequentialMultiAgent  # Basic multi-agent was sequential
```

## 📊 Success Metrics

### Technical Metrics

- [ ] **40% LOC reduction** (5,000 → 3,000 LOC)
- [ ] **6 focused patterns** (from 8 mixed implementations)
- [ ] **Clear coordination modes** - each multi-agent has single strategy
- [ ] **100% workflow delegation** - complex orchestration uses workflow layer
- [ ] **Protocol compliance** - all multi-agents implement coordination protocol

### Quality Metrics

- [ ] **Single coordination pattern** - each multi-agent focused on one approach
- [ ] **Agent independence** - individual agents remain testable
- [ ] **Composition over inheritance** - multi-agents compose workflows and agents
- [ ] **Backward compatibility** - existing usage works through facade layer

### Developer Experience

- [ ] **Simple multi-agent creation** - factory functions for common patterns
- [ ] **Clear documentation** - purpose and usage of each coordination pattern
- [ ] **Easy testing** - multi-agents testable with mock agents
- [ ] **Migration support** - clear upgrade path from v4 to clean patterns

## 🔗 Integration Points

### With Agent Domain

- Multi-agents compose individual agents
- Agent execution delegated to agent layer
- Agent results aggregated by multi-agent coordination

### With Workflow Domain

- Multi-agent coordination implemented as workflows
- Complex orchestration patterns use workflow compositions
- Multi-agent state management via workflow state

### With Schema Domain

- Multi-agent state uses composed state schemas
- Agent coordination metadata via schema composition
- Message passing between agents via message schemas

## 🚨 Common Pitfalls

### 1. Over-coordination

**Problem**: Making multi-agent coordination too complex
**Solution**: Keep coordination simple, delegate complexity to workflows

### 2. Agent Coupling

**Problem**: Multi-agents creating tight coupling between agents
**Solution**: Maintain agent independence, use shared context for communication

### 3. Performance Overhead

**Problem**: Multi-agent coordination adding significant overhead
**Solution**: Optimize coordination workflows, use parallel execution where appropriate

### 4. State Management Complexity

**Problem**: Complex state sharing between agents
**Solution**: Use schema composition patterns, clear state boundaries

## 🔄 Rollback Strategy

### If Multi-Agent Issues Arise

1. **Pattern-by-pattern rollback**: Each coordination pattern is independent
2. **Revert to enhanced v4**: Keep facade layer as fallback
3. **Gradual migration**: Move one coordination pattern at a time
4. **Agent isolation**: Ensure agent problems don't affect multi-agent layer

### Risk Mitigation

- Maintain enhanced v4 facade during entire migration
- Comprehensive testing of new vs old multi-agent behavior
- Performance monitoring for coordination overhead
- Clear separation between coordination and agent execution

---

**Next Steps**:

1. Start with sequential multi-agent (most straightforward pattern)
2. Build comprehensive testing for each coordination pattern
3. Create facade layer for backward compatibility
4. Validate performance improvements with clean coordination patterns
