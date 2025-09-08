# Workflow Creation Implementation Plan

**Domain**: Workflow Creation (New Layer)  
**Estimated Days**: 5-6 days  
**Target LOC**: 800 LOC (new functionality)  
**Dependencies**: [Contracts](../contracts/PROTOCOL_CONTRACTS_PLAN.md), [Node](../node/NODE_CONSOLIDATION_PLAN.md)

## 🎯 Overview

Create a pure orchestration layer that handles workflow execution without any LLM coupling. This provides the foundation for Agent implementations while enabling standalone workflow usage for non-AI orchestration needs.

## 📊 Current State Analysis

### The Missing Layer Problem

**Current State**: No pure orchestration abstraction

- Agents directly implement workflow logic mixed with LLM concerns
- Workflow patterns scattered across multiple agent implementations
- No reusable orchestration components
- Complex agent inheritance chains for simple workflow needs

### Workflow Patterns Currently Embedded in Agents

```bash
# Workflow logic currently scattered in:
packages/haive-agents/src/haive/agents/
├── multi/enhanced_multi_agent_v4.py     # Sequential/parallel patterns
├── react/agent.py                       # Loop-based workflow
├── simple/agent.py                      # Linear workflow
├── rag/base/agent.py                    # Retrieval workflow
└── planning/planner.py                  # Planning workflow
```

**Problems**:

- **Mixed Concerns**: Workflow + LLM + Agent state all together
- **Duplication**: Same orchestration patterns repeated in multiple agents
- **No Reusability**: Can't use workflow patterns without LLM coupling
- **Testing Complexity**: Can't test orchestration logic independently

## 🏗️ Target Architecture

### Pure Workflow Layer (800 total LOC)

```
packages/haive-core/src/haive/core/workflow/
├── __init__.py                          # Workflow exports (50 LOC)
├── base/
│   ├── __init__.py                     # Base exports (20 LOC)
│   ├── base_workflow.py                # Core workflow logic (200 LOC)
│   └── workflow_protocol.py           # Protocol implementation (100 LOC)
├── sequential_workflow.py              # Sequential execution (150 LOC)
├── parallel_workflow.py                # Parallel execution (120 LOC)
├── conditional_workflow.py             # Conditional logic (100 LOC)
├── loop_workflow.py                    # Loop-based execution (80 LOC)
└── composite_workflow.py              # Workflow composition (80 LOC)
```

**Total**: 8 files, ~800 LOC (new layer)

### Key Design Principles

1. **No LLM Coupling**: Pure orchestration without AI dependencies
2. **Composable**: Workflows can be nested and combined
3. **Testable**: Logic testable without any external dependencies
4. **Reusable**: Same workflow patterns used by agents and standalone
5. **Protocol-Based**: Clear interfaces for all workflow types

## 📋 Detailed Implementation Steps

### Step 1: Base Workflow Infrastructure (Day 1)

#### 1.1 Workflow Protocol Implementation

**File**: `base/workflow_protocol.py`

```python
from typing import Any, Dict, List, Optional, TypeVar, Generic, Callable
from haive.core.contracts.agent.workflow_protocol import WorkflowProtocol, WorkflowMode
from enum import Enum

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
StepT = TypeVar('StepT')

class WorkflowStep:
    """Single step in a workflow."""

    def __init__(
        self,
        name: str,
        executor: Callable[[Any, Any], Any],
        input_mapper: Optional[Callable[[Any], Any]] = None,
        output_mapper: Optional[Callable[[Any], Any]] = None
    ):
        self.name = name
        self.executor = executor
        self.input_mapper = input_mapper or (lambda x: x)
        self.output_mapper = output_mapper or (lambda x: x)

    async def aexecute(self, input_data: Any, context: Any) -> Any:
        """Execute step asynchronously."""
        # Map input
        mapped_input = self.input_mapper(input_data)

        # Execute step
        if asyncio.iscoroutinefunction(self.executor):
            result = await self.executor(mapped_input, context)
        else:
            result = self.executor(mapped_input, context)

        # Map output
        return self.output_mapper(result)

    def execute(self, input_data: Any, context: Any) -> Any:
        """Execute step synchronously."""
        import asyncio
        return asyncio.run(self.aexecute(input_data, context))

class BaseWorkflowProtocol(WorkflowProtocol[InputT, OutputT]):
    """Base implementation of workflow protocol."""

    def __init__(self, name: str, mode: WorkflowMode):
        self.name = name
        self._mode = mode
        self.steps: List[WorkflowStep] = []
        self._context = {}

    @property
    def mode(self) -> WorkflowMode:
        """Workflow execution mode."""
        return self._mode

    def add_step(self, step: Any, name: str) -> None:
        """Add step to workflow."""
        if isinstance(step, WorkflowStep):
            workflow_step = step
        elif callable(step):
            workflow_step = WorkflowStep(name, step)
        else:
            raise ValueError(f"Invalid step type: {type(step)}")

        self.steps.append(workflow_step)

    def remove_step(self, name: str) -> None:
        """Remove step from workflow."""
        self.steps = [step for step in self.steps if step.name != name]

    def get_step(self, name: str) -> Optional[WorkflowStep]:
        """Get step by name."""
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def set_context(self, **kwargs) -> None:
        """Set workflow context."""
        self._context.update(kwargs)

    async def aexecute(self, input_data: InputT) -> OutputT:
        """Execute workflow asynchronously - implement in subclasses."""
        raise NotImplementedError("Subclasses must implement aexecute")

    def execute(self, input_data: InputT) -> OutputT:
        """Execute workflow synchronously."""
        import asyncio
        return asyncio.run(self.aexecute(input_data))
```

#### 1.2 Base Workflow Implementation

**File**: `base/base_workflow.py`

```python
import asyncio
import time
from typing import Any, Dict, List, Optional, Callable
from .workflow_protocol import BaseWorkflowProtocol, WorkflowStep
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

class BaseWorkflow(BaseWorkflowProtocol[Dict[str, Any], Dict[str, Any]]):
    """Base workflow with common functionality."""

    def __init__(
        self,
        name: str,
        mode: WorkflowMode,
        timeout_seconds: int = 300,
        max_retries: int = 0
    ):
        super().__init__(name, mode)
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self._execution_history: List[Dict[str, Any]] = []

    async def aexecute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with timing and error handling."""
        execution_id = f"{self.name}_{int(time.time() * 1000)}"
        start_time = time.time()

        execution_record = {
            "execution_id": execution_id,
            "start_time": start_time,
            "input_data": input_data,
            "steps_executed": [],
            "status": "running",
            "error": None
        }

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self._execute_steps(input_data, execution_record),
                timeout=self.timeout_seconds
            )

            # Update record
            execution_record["status"] = "completed"
            execution_record["result"] = result
            execution_record["end_time"] = time.time()
            execution_record["duration_ms"] = int((execution_record["end_time"] - start_time) * 1000)

            self._execution_history.append(execution_record)
            return result

        except Exception as e:
            execution_record["status"] = "failed"
            execution_record["error"] = str(e)
            execution_record["end_time"] = time.time()
            self._execution_history.append(execution_record)
            raise

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps - implement in subclasses."""
        raise NotImplementedError("Subclasses must implement _execute_steps")

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history."""
        return self._execution_history.copy()

    def get_last_execution(self) -> Optional[Dict[str, Any]]:
        """Get last execution record."""
        return self._execution_history[-1] if self._execution_history else None

    def clear_history(self) -> None:
        """Clear execution history."""
        self._execution_history.clear()
```

### Step 2: Sequential Workflow (Day 2)

#### 2.1 Sequential Execution Pattern

**File**: `sequential_workflow.py`

```python
from typing import Any, Dict
from .base.base_workflow import BaseWorkflow
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

class SequentialWorkflow(BaseWorkflow):
    """Execute steps sequentially, passing output to next step."""

    def __init__(self, name: str = "sequential_workflow", **kwargs):
        super().__init__(name, WorkflowMode.SEQUENTIAL, **kwargs)
        self._fail_fast = kwargs.get('fail_fast', True)

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps in sequence."""
        current_data = input_data
        results = {}

        for i, step in enumerate(self.steps):
            step_start_time = time.time()
            step_record = {
                "step_name": step.name,
                "step_index": i,
                "start_time": step_start_time,
                "input": current_data
            }

            try:
                # Execute step
                step_result = await step.aexecute(current_data, self._context)

                # Record step completion
                step_record["status"] = "completed"
                step_record["result"] = step_result
                step_record["end_time"] = time.time()
                step_record["duration_ms"] = int((step_record["end_time"] - step_start_time) * 1000)

                # Store result and pass to next step
                results[step.name] = step_result
                current_data = self._merge_step_output(current_data, step_result, step.name)

            except Exception as e:
                step_record["status"] = "failed"
                step_record["error"] = str(e)
                step_record["end_time"] = time.time()

                if self._fail_fast:
                    execution_record["steps_executed"].append(step_record)
                    raise
                else:
                    # Continue with error recorded
                    step_record["result"] = None
                    results[step.name] = None

            execution_record["steps_executed"].append(step_record)

        return {
            "final_result": current_data,
            "step_results": results,
            "workflow_type": "sequential",
            "steps_completed": len([r for r in results.values() if r is not None])
        }

    def _merge_step_output(self, current_data: Dict[str, Any], step_result: Any, step_name: str) -> Dict[str, Any]:
        """Merge step output into current data."""
        if isinstance(step_result, dict):
            # Merge dictionaries
            return {**current_data, **step_result, f"__{step_name}__": step_result}
        else:
            # Store as step-named key
            return {**current_data, step_name: step_result}
```

### Step 3: Parallel Workflow (Day 2.5)

#### 3.1 Parallel Execution Pattern

**File**: `parallel_workflow.py`

```python
import asyncio
from typing import Any, Dict, List
from .base.base_workflow import BaseWorkflow
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

class ParallelWorkflow(BaseWorkflow):
    """Execute steps in parallel and collect results."""

    def __init__(self, name: str = "parallel_workflow", **kwargs):
        super().__init__(name, WorkflowMode.PARALLEL, **kwargs)
        self._max_concurrent = kwargs.get('max_concurrent', None)  # None = unlimited
        self._wait_for_all = kwargs.get('wait_for_all', True)

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps in parallel."""
        if self._max_concurrent:
            # Execute with concurrency limit
            semaphore = asyncio.Semaphore(self._max_concurrent)
            tasks = [self._execute_step_with_semaphore(step, input_data, semaphore, i)
                    for i, step in enumerate(self.steps)]
        else:
            # Execute all concurrently
            tasks = [self._execute_single_step(step, input_data, i)
                    for i, step in enumerate(self.steps)]

        if self._wait_for_all:
            # Wait for all tasks to complete
            step_results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Return results as they complete
            step_results = []
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                step_results.append(result)

        # Process results
        successful_results = {}
        failed_results = {}

        for i, result in enumerate(step_results):
            step_name = self.steps[i].name

            if isinstance(result, Exception):
                failed_results[step_name] = {
                    "error": str(result),
                    "step_index": i
                }
                execution_record["steps_executed"].append({
                    "step_name": step_name,
                    "step_index": i,
                    "status": "failed",
                    "error": str(result)
                })
            else:
                successful_results[step_name] = result["result"]
                execution_record["steps_executed"].append({
                    "step_name": step_name,
                    "step_index": result["step_index"],
                    "status": "completed",
                    "result": result["result"],
                    "duration_ms": result["duration_ms"]
                })

        return {
            "successful_results": successful_results,
            "failed_results": failed_results,
            "workflow_type": "parallel",
            "steps_completed": len(successful_results),
            "steps_failed": len(failed_results),
            "original_input": input_data
        }

    async def _execute_step_with_semaphore(
        self,
        step,
        input_data: Dict[str, Any],
        semaphore: asyncio.Semaphore,
        step_index: int
    ) -> Dict[str, Any]:
        """Execute step with concurrency control."""
        async with semaphore:
            return await self._execute_single_step(step, input_data, step_index)

    async def _execute_single_step(
        self,
        step,
        input_data: Dict[str, Any],
        step_index: int
    ) -> Dict[str, Any]:
        """Execute a single step."""
        start_time = time.time()

        result = await step.aexecute(input_data, self._context)

        return {
            "result": result,
            "step_index": step_index,
            "duration_ms": int((time.time() - start_time) * 1000)
        }
```

### Step 4: Conditional and Loop Workflows (Day 3)

#### 4.1 Conditional Workflow

**File**: `conditional_workflow.py`

```python
from typing import Any, Dict, Callable, Optional
from .base.base_workflow import BaseWorkflow
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

class ConditionalBranch:
    """Single conditional branch."""

    def __init__(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        steps: List[str]
    ):
        self.name = name
        self.condition = condition
        self.steps = steps

class ConditionalWorkflow(BaseWorkflow):
    """Execute different step sequences based on conditions."""

    def __init__(self, name: str = "conditional_workflow", **kwargs):
        super().__init__(name, WorkflowMode.CONDITIONAL, **kwargs)
        self.branches: List[ConditionalBranch] = []
        self.default_steps: List[str] = []

    def add_branch(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        steps: List[str]
    ) -> None:
        """Add conditional branch."""
        self.branches.append(ConditionalBranch(name, condition, steps))

    def set_default_steps(self, steps: List[str]) -> None:
        """Set steps to execute if no conditions match."""
        self.default_steps = steps

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps based on conditions."""
        # Evaluate conditions
        selected_branch = None
        for branch in self.branches:
            try:
                if branch.condition(input_data):
                    selected_branch = branch
                    break
            except Exception as e:
                # Log condition evaluation error but continue
                print(f"Error evaluating condition for branch {branch.name}: {e}")

        # Determine steps to execute
        if selected_branch:
            steps_to_execute = selected_branch.steps
            branch_name = selected_branch.name
        else:
            steps_to_execute = self.default_steps
            branch_name = "default"

        # Execute selected steps
        results = {}
        current_data = input_data

        for step_name in steps_to_execute:
            step = self.get_step(step_name)
            if not step:
                raise ValueError(f"Step '{step_name}' not found in workflow")

            step_start_time = time.time()
            step_result = await step.aexecute(current_data, self._context)

            results[step_name] = step_result
            current_data = self._merge_step_output(current_data, step_result, step_name)

            execution_record["steps_executed"].append({
                "step_name": step_name,
                "status": "completed",
                "result": step_result,
                "duration_ms": int((time.time() - step_start_time) * 1000)
            })

        return {
            "final_result": current_data,
            "branch_executed": branch_name,
            "step_results": results,
            "workflow_type": "conditional",
            "steps_completed": len(results)
        }

    def _merge_step_output(self, current_data: Dict[str, Any], step_result: Any, step_name: str) -> Dict[str, Any]:
        """Merge step output into current data."""
        if isinstance(step_result, dict):
            return {**current_data, **step_result}
        else:
            return {**current_data, step_name: step_result}
```

#### 4.2 Loop Workflow

**File**: `loop_workflow.py`

```python
from typing import Any, Dict, Callable, Optional
from .base.base_workflow import BaseWorkflow
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

class LoopWorkflow(BaseWorkflow):
    """Execute steps in a loop based on conditions."""

    def __init__(self, name: str = "loop_workflow", **kwargs):
        super().__init__(name, WorkflowMode.LOOP, **kwargs)
        self._continue_condition: Optional[Callable[[Dict[str, Any]], bool]] = None
        self._max_iterations = kwargs.get('max_iterations', 100)
        self._min_iterations = kwargs.get('min_iterations', 1)

    def set_continue_condition(self, condition: Callable[[Dict[str, Any]], bool]) -> None:
        """Set condition for continuing loop."""
        self._continue_condition = condition

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps in loop."""
        current_data = input_data
        iteration_results = []
        iteration = 0

        while iteration < self._max_iterations:
            iteration += 1
            iteration_start_time = time.time()

            # Execute all steps in this iteration
            iteration_step_results = {}

            for step in self.steps:
                step_start_time = time.time()
                step_result = await step.aexecute(current_data, self._context)

                iteration_step_results[step.name] = step_result
                current_data = self._merge_step_output(current_data, step_result, step.name)

                execution_record["steps_executed"].append({
                    "step_name": step.name,
                    "iteration": iteration,
                    "status": "completed",
                    "result": step_result,
                    "duration_ms": int((time.time() - step_start_time) * 1000)
                })

            # Record iteration
            iteration_record = {
                "iteration": iteration,
                "step_results": iteration_step_results,
                "iteration_data": current_data,
                "duration_ms": int((time.time() - iteration_start_time) * 1000)
            }
            iteration_results.append(iteration_record)

            # Check continue condition (after minimum iterations)
            if iteration >= self._min_iterations and self._continue_condition:
                try:
                    should_continue = self._continue_condition(current_data)
                    if not should_continue:
                        break
                except Exception as e:
                    # Error in condition - stop loop
                    print(f"Error in continue condition: {e}")
                    break

        return {
            "final_result": current_data,
            "iterations_completed": iteration,
            "iteration_results": iteration_results,
            "workflow_type": "loop",
            "loop_completed_normally": iteration < self._max_iterations or self._continue_condition is None
        }

    def _merge_step_output(self, current_data: Dict[str, Any], step_result: Any, step_name: str) -> Dict[str, Any]:
        """Merge step output into current data."""
        if isinstance(step_result, dict):
            return {**current_data, **step_result}
        else:
            return {**current_data, step_name: step_result}
```

### Step 5: Composite Workflow (Day 4)

#### 5.1 Workflow Composition

**File**: `composite_workflow.py`

```python
from typing import Any, Dict, List, Union
from .base.base_workflow import BaseWorkflow
from .sequential_workflow import SequentialWorkflow
from .parallel_workflow import ParallelWorkflow
from .conditional_workflow import ConditionalWorkflow
from .loop_workflow import LoopWorkflow
from haive.core.contracts.agent.workflow_protocol import WorkflowMode

WorkflowType = Union[BaseWorkflow, 'CompositeWorkflow']

class CompositeWorkflow(BaseWorkflow):
    """Compose multiple workflows together."""

    def __init__(self, name: str = "composite_workflow", **kwargs):
        super().__init__(name, WorkflowMode.SEQUENTIAL, **kwargs)  # Default to sequential
        self.sub_workflows: List[WorkflowType] = []
        self._execution_mode = kwargs.get('execution_mode', 'sequential')

    def add_workflow(self, workflow: WorkflowType) -> None:
        """Add sub-workflow."""
        self.sub_workflows.append(workflow)

    def remove_workflow(self, name: str) -> None:
        """Remove sub-workflow by name."""
        self.sub_workflows = [wf for wf in self.sub_workflows if wf.name != name]

    async def _execute_steps(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-workflows."""
        if self._execution_mode == 'sequential':
            return await self._execute_sequential(input_data, execution_record)
        elif self._execution_mode == 'parallel':
            return await self._execute_parallel(input_data, execution_record)
        else:
            raise ValueError(f"Unknown execution mode: {self._execution_mode}")

    async def _execute_sequential(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-workflows sequentially."""
        current_data = input_data
        workflow_results = {}

        for workflow in self.sub_workflows:
            workflow_start_time = time.time()

            workflow_result = await workflow.aexecute(current_data)

            workflow_results[workflow.name] = workflow_result

            # Update current data based on result structure
            if isinstance(workflow_result, dict):
                if "final_result" in workflow_result:
                    current_data = workflow_result["final_result"]
                else:
                    current_data = {**current_data, **workflow_result}

            execution_record["steps_executed"].append({
                "workflow_name": workflow.name,
                "workflow_type": workflow.mode.value,
                "status": "completed",
                "result": workflow_result,
                "duration_ms": int((time.time() - workflow_start_time) * 1000)
            })

        return {
            "final_result": current_data,
            "workflow_results": workflow_results,
            "workflow_type": "composite_sequential",
            "workflows_completed": len(workflow_results)
        }

    async def _execute_parallel(self, input_data: Dict[str, Any], execution_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-workflows in parallel."""
        import asyncio

        tasks = [workflow.aexecute(input_data) for workflow in self.sub_workflows]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        successful_results = {}
        failed_results = {}

        for i, result in enumerate(results):
            workflow_name = self.sub_workflows[i].name

            if isinstance(result, Exception):
                failed_results[workflow_name] = str(result)
                execution_record["steps_executed"].append({
                    "workflow_name": workflow_name,
                    "status": "failed",
                    "error": str(result)
                })
            else:
                successful_results[workflow_name] = result
                execution_record["steps_executed"].append({
                    "workflow_name": workflow_name,
                    "status": "completed",
                    "result": result
                })

        return {
            "successful_results": successful_results,
            "failed_results": failed_results,
            "workflow_type": "composite_parallel",
            "workflows_completed": len(successful_results),
            "workflows_failed": len(failed_results),
            "original_input": input_data
        }

# Factory functions for common patterns
def create_sequential_workflow(name: str, steps: List[Callable]) -> SequentialWorkflow:
    """Factory for sequential workflow."""
    workflow = SequentialWorkflow(name)
    for i, step in enumerate(steps):
        step_name = getattr(step, '__name__', f'step_{i}')
        workflow.add_step(step, step_name)
    return workflow

def create_parallel_workflow(name: str, steps: List[Callable], **kwargs) -> ParallelWorkflow:
    """Factory for parallel workflow."""
    workflow = ParallelWorkflow(name, **kwargs)
    for i, step in enumerate(steps):
        step_name = getattr(step, '__name__', f'step_{i}')
        workflow.add_step(step, step_name)
    return workflow
```

### Step 6: Integration & Testing (Days 5-6)

#### 6.1 Comprehensive Workflow Testing

**Unit Tests**: Test each workflow type

```python
# tests/workflow/test_sequential_workflow.py
import pytest
from haive.core.workflow.sequential_workflow import SequentialWorkflow

@pytest.mark.asyncio
class TestSequentialWorkflow:
    async def test_simple_sequential_execution(self):
        """Test basic sequential execution."""
        def add_one(data, context):
            return {"value": data["value"] + 1}

        def multiply_two(data, context):
            return {"value": data["value"] * 2}

        workflow = SequentialWorkflow("test_sequential")
        workflow.add_step(add_one, "add_one")
        workflow.add_step(multiply_two, "multiply_two")

        result = await workflow.aexecute({"value": 5})

        # (5 + 1) * 2 = 12
        assert result["final_result"]["value"] == 12
        assert result["workflow_type"] == "sequential"
        assert result["steps_completed"] == 2
        assert "add_one" in result["step_results"]
        assert "multiply_two" in result["step_results"]

    async def test_error_handling_fail_fast(self):
        """Test error handling with fail_fast=True."""
        def success_step(data, context):
            return {"success": True}

        def error_step(data, context):
            raise ValueError("Test error")

        workflow = SequentialWorkflow("test_error", fail_fast=True)
        workflow.add_step(success_step, "success")
        workflow.add_step(error_step, "error")

        with pytest.raises(ValueError, match="Test error"):
            await workflow.aexecute({"value": 1})

        # Check execution history
        history = workflow.get_execution_history()
        assert len(history) == 1
        assert history[0]["status"] == "failed"
```

**Integration Tests**: Test workflow combinations

```python
# tests/workflow/test_workflow_integration.py
import pytest
from haive.core.workflow.composite_workflow import CompositeWorkflow
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from haive.core.workflow.parallel_workflow import ParallelWorkflow

@pytest.mark.asyncio
class TestWorkflowIntegration:
    async def test_composite_sequential_workflows(self):
        """Test composing sequential workflows."""
        # Create first workflow: data preparation
        prep_workflow = SequentialWorkflow("preparation")
        prep_workflow.add_step(
            lambda data, ctx: {"value": data["raw_value"] * 2},
            "double"
        )
        prep_workflow.add_step(
            lambda data, ctx: {"value": data["value"] + 10},
            "add_offset"
        )

        # Create second workflow: data processing
        process_workflow = SequentialWorkflow("processing")
        process_workflow.add_step(
            lambda data, ctx: {"processed": data["value"] ** 2},
            "square"
        )
        process_workflow.add_step(
            lambda data, ctx: {"final": data["processed"] / 2},
            "halve"
        )

        # Create composite workflow
        composite = CompositeWorkflow("data_pipeline")
        composite.add_workflow(prep_workflow)
        composite.add_workflow(process_workflow)

        # Execute composite workflow
        result = await composite.aexecute({"raw_value": 3})

        # ((3 * 2) + 10)^2 / 2 = (16)^2 / 2 = 256 / 2 = 128
        assert result["final_result"]["final"] == 128
        assert result["workflows_completed"] == 2
        assert "preparation" in result["workflow_results"]
        assert "processing" in result["workflow_results"]
```

**System Tests**: Test with real components

```python
# tests/workflow/system/test_workflow_with_agents.py
import pytest
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

@pytest.mark.asyncio
class TestWorkflowWithAgents:
    async def test_agent_workflow_integration(self):
        """Test workflow using real agents as steps."""
        # Create agents
        analyzer = SimpleAgent(
            name="analyzer",
            engine=AugLLMConfig(temperature=0.1)
        )

        formatter = SimpleAgent(
            name="formatter",
            engine=AugLLMConfig(temperature=0.1)
        )

        # Create workflow with agent steps
        def analyze_step(data, context):
            # Use agent to analyze input
            analysis_input = f"Analyze this data: {data['input']}"
            return {"analysis": analyzer.run(analysis_input)}

        def format_step(data, context):
            # Use agent to format analysis
            format_input = f"Format this analysis: {data['analysis']}"
            return {"formatted": formatter.run(format_input)}

        workflow = SequentialWorkflow("agent_workflow")
        workflow.add_step(analyze_step, "analyze")
        workflow.add_step(format_step, "format")

        # Execute workflow
        result = await workflow.aexecute({"input": "Customer feedback data"})

        # Verify structure
        assert "analysis" in result["step_results"]["analyze"]
        assert "formatted" in result["step_results"]["format"]
        assert isinstance(result["final_result"]["formatted"], str)
```

## 🧪 Testing Strategy

### 1. Property-Based Testing (Hypothesis)

```python
from hypothesis import given, strategies as st
from haive.core.workflow.sequential_workflow import SequentialWorkflow

@given(
    values=st.lists(st.integers(), min_size=1, max_size=10)
)
@pytest.mark.asyncio
async def test_sequential_workflow_properties(values):
    """Property-based testing for sequential workflows."""
    def sum_step(data, context):
        return {"sum": sum(data.get("values", []))}

    def count_step(data, context):
        return {"count": len(data.get("values", []))}

    workflow = SequentialWorkflow("prop_test")
    workflow.add_step(sum_step, "sum")
    workflow.add_step(count_step, "count")

    result = await workflow.aexecute({"values": values})

    # Properties that should always hold
    assert result["final_result"]["sum"] == sum(values)
    assert result["final_result"]["count"] == len(values)
    assert result["steps_completed"] == 2
    assert result["workflow_type"] == "sequential"
```

### 2. Performance Testing

```python
import time
import pytest

@pytest.mark.asyncio
async def test_workflow_performance():
    """Test workflow execution performance."""
    def fast_step(data, context):
        return {"processed": data.get("value", 0) + 1}

    workflow = SequentialWorkflow("perf_test")
    for i in range(100):
        workflow.add_step(fast_step, f"step_{i}")

    start_time = time.time()
    result = await workflow.aexecute({"value": 0})
    end_time = time.time()

    execution_time_ms = (end_time - start_time) * 1000

    # Should complete 100 steps quickly
    assert result["final_result"]["processed"] == 100
    assert execution_time_ms < 100  # Less than 100ms for 100 simple steps
```

## 📊 Success Metrics

### Technical Metrics

- [ ] **Pure orchestration** - no LLM coupling in workflow layer
- [ ] **100% test coverage** for all workflow types
- [ ] **<10ms overhead** per workflow step
- [ ] **Composable** - workflows can be nested without issues

### Quality Metrics

- [ ] **Protocol compliance** - all workflows implement WorkflowProtocol
- [ ] **Single responsibility** - each workflow type has one clear purpose
- [ ] **Error handling** - comprehensive error recovery and reporting
- [ ] **Observable** - detailed execution tracking and history

### Developer Experience

- [ ] **Simple API** - easy to create and use workflows
- [ ] **Clear examples** - comprehensive documentation with examples
- [ ] **Debuggable** - execution history enables easy debugging
- [ ] **Extensible** - easy to create new workflow types

## 🔗 Integration Points

### With Agent Domain

- Agents use workflows internally for orchestration
- Agent execution becomes workflow + LLM engine
- Multi-agent patterns built on workflow foundation

### With Node Domain

- Workflow steps can be graph nodes
- Complex orchestration via workflow composition
- Node execution patterns abstracted as workflows

### With Engine Domain

- Workflows orchestrate engine execution
- Engine results fed through workflow steps
- Tool execution patterns as workflow templates

## 🚨 Common Pitfalls

### 1. Overcomplicating Workflows

**Problem**: Making workflows too complex for simple use cases
**Solution**: Provide simple factory functions and common patterns

### 2. Performance Overhead

**Problem**: Workflow abstraction adding significant overhead
**Solution**: Optimize hot paths and provide direct execution options

### 3. Error Propagation

**Problem**: Errors getting lost in workflow composition
**Solution**: Comprehensive error tracking and clear error messages

### 4. State Management Complexity

**Problem**: Complex state passing between workflow steps
**Solution**: Clear state transformation patterns and documentation

## 🔄 Rollback Strategy

### If Workflow Abstraction Issues Arise

1. **Isolate problem workflow**: Each workflow type is independent
2. **Revert to direct execution**: Agents can bypass workflows temporarily
3. **Gradual adoption**: Migrate one workflow pattern at a time
4. **Performance monitoring**: Watch for regressions and optimize

### Risk Mitigation

- Keep workflow abstraction optional for agents initially
- Comprehensive performance benchmarking
- Clear migration path from existing patterns
- Feature flags for workflow vs direct execution

---

**Next Steps**:

1. Start with BaseWorkflow and SequentialWorkflow (most fundamental)
2. Add comprehensive testing for each workflow type
3. Create factory functions for common patterns
4. Validate agent integration patterns
