# HAP Improvement Plan - Practical Next Steps

**Purpose**: Actionable improvement plan for HAP based on deep analysis
**Timeline**: Q1-Q2 2025
**Priority**: High-impact, low-effort improvements first

## 🎯 Immediate Improvements (Week 1-2)

### 1. Add Basic Observability

**File**: `src/haive/hap/server/runtime.py`

```python
import json
from datetime import datetime
from typing import Dict, List, Any

class ExecutionTrace:
    """Lightweight execution tracing."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, node_id: str, data: Dict[str, Any]):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "node": node_id,
            "data": data
        })

    def to_json(self) -> str:
        return json.dumps(self.events, indent=2)

    def get_timeline(self) -> str:
        """Generate ASCII timeline of execution."""
        timeline = ["Execution Timeline:"]
        for event in self.events:
            if event["type"] == "node_start":
                timeline.append(f"  → {event['node']} started at {event['timestamp']}")
            elif event["type"] == "node_complete":
                timeline.append(f"  ✓ {event['node']} completed in {event['data']['duration']}s")
            elif event["type"] == "node_error":
                timeline.append(f"  ✗ {event['node']} failed: {event['data']['error']}")
        return "\n".join(timeline)

# Add to HAPRuntime.__init__
self.trace = ExecutionTrace()

# Add tracing to node execution
async def _execute_node(self, node_id: str, context: HAPContext):
    self.trace.log_event("node_start", node_id, {"input_size": len(str(context.inputs))})
    start_time = datetime.now()

    try:
        result = await super()._execute_node(node_id, context)
        duration = (datetime.now() - start_time).total_seconds()
        self.trace.log_event("node_complete", node_id, {"duration": duration})
        return result
    except Exception as e:
        self.trace.log_event("node_error", node_id, {"error": str(e)})
        raise
```

### 2. Implement Simple Retry Logic

**File**: `src/haive/hap/models/graph.py`

```python
from typing import Optional
import asyncio

class RetryConfig(BaseModel):
    """Configuration for retry behavior."""
    max_attempts: int = Field(default=1, ge=1, le=5)
    backoff_factor: float = Field(default=2.0, gt=1.0)
    initial_delay: float = Field(default=1.0, gt=0)

class HAPNode(BaseModel):
    """Enhanced with retry support."""
    # ... existing fields ...
    retry_config: Optional[RetryConfig] = None

    def should_retry(self, attempt: int, error: Exception) -> bool:
        """Determine if node should retry after error."""
        if not self.retry_config:
            return False

        # Don't retry validation errors
        if isinstance(error, (ValueError, ValidationError)):
            return False

        return attempt < self.retry_config.max_attempts

    def get_retry_delay(self, attempt: int) -> float:
        """Calculate delay before retry using exponential backoff."""
        if not self.retry_config:
            return 0

        return self.retry_config.initial_delay * (
            self.retry_config.backoff_factor ** (attempt - 1)
        )
```

**File**: `src/haive/hap/server/runtime.py` (update execution)

```python
async def _execute_node_with_retry(self, node: HAPNode, context: HAPContext):
    """Execute node with retry logic."""
    last_error = None

    for attempt in range(1, (node.retry_config.max_attempts if node.retry_config else 1) + 1):
        try:
            return await self._execute_node(node.id, context)
        except Exception as e:
            last_error = e

            if node.should_retry(attempt, e):
                delay = node.get_retry_delay(attempt)
                self.trace.log_event("node_retry", node.id, {
                    "attempt": attempt,
                    "delay": delay,
                    "error": str(e)
                })
                await asyncio.sleep(delay)
            else:
                break

    raise last_error
```

### 3. Add Performance Metrics

**File**: `src/haive/hap/server/runtime.py`

```python
from dataclasses import dataclass
from statistics import mean, median

@dataclass
class PerformanceMetrics:
    """Runtime performance metrics."""
    total_executions: int = 0
    total_duration: float = 0.0
    node_timings: Dict[str, List[float]] = field(default_factory=dict)
    error_counts: Dict[str, int] = field(default_factory=dict)

    def record_node_execution(self, node_id: str, duration: float):
        if node_id not in self.node_timings:
            self.node_timings[node_id] = []
        self.node_timings[node_id].append(duration)

    def record_error(self, node_id: str):
        self.error_counts[node_id] = self.error_counts.get(node_id, 0) + 1

    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        summary = {
            "total_executions": self.total_executions,
            "average_duration": self.total_duration / self.total_executions if self.total_executions else 0,
            "node_stats": {}
        }

        for node_id, timings in self.node_timings.items():
            summary["node_stats"][node_id] = {
                "executions": len(timings),
                "avg_duration": mean(timings),
                "median_duration": median(timings),
                "min_duration": min(timings),
                "max_duration": max(timings),
                "error_rate": self.error_counts.get(node_id, 0) / len(timings)
            }

        return summary

# Add to HAPRuntime
self.metrics = PerformanceMetrics()
```

## 🚀 Quick Wins (Week 3-4)

### 1. Checkpoint System

**File**: `src/haive/hap/server/checkpoint.py` (new file)

```python
import pickle
import json
from pathlib import Path
from typing import Optional

class CheckpointManager:
    """Simple checkpoint system for workflow state."""

    def __init__(self, checkpoint_dir: str = ".hap_checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)

    async def save_checkpoint(
        self,
        workflow_id: str,
        context: HAPContext,
        current_node: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Save workflow checkpoint."""
        checkpoint = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "context": context.model_dump(),
            "current_node": current_node,
            "metadata": metadata or {}
        }

        checkpoint_file = self.checkpoint_dir / f"{workflow_id}_{current_node}.checkpoint"

        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    async def load_checkpoint(self, workflow_id: str, node_id: Optional[str] = None) -> Optional[Dict]:
        """Load workflow checkpoint."""
        if node_id:
            checkpoint_file = self.checkpoint_dir / f"{workflow_id}_{node_id}.checkpoint"
        else:
            # Find latest checkpoint
            checkpoints = list(self.checkpoint_dir.glob(f"{workflow_id}_*.checkpoint"))
            if not checkpoints:
                return None
            checkpoint_file = max(checkpoints, key=lambda p: p.stat().st_mtime)

        if not checkpoint_file.exists():
            return None

        with open(checkpoint_file, 'r') as f:
            return json.load(f)

    def list_checkpoints(self, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available checkpoints."""
        pattern = f"{workflow_id}_*.checkpoint" if workflow_id else "*.checkpoint"
        checkpoints = []

        for checkpoint_file in self.checkpoint_dir.glob(pattern):
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)
                checkpoints.append({
                    "file": checkpoint_file.name,
                    "workflow_id": data["workflow_id"],
                    "node": data["current_node"],
                    "timestamp": data["timestamp"]
                })

        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)
```

### 2. Basic Parallel Execution

**File**: `src/haive/hap/server/runtime.py` (enhance)

```python
async def _execute_parallel_nodes(self, node_ids: List[str], context: HAPContext) -> Dict[str, Any]:
    """Execute multiple nodes in parallel."""
    tasks = []

    for node_id in node_ids:
        # Create isolated context for each parallel node
        node_context = context.model_copy(deep=True)
        task = asyncio.create_task(self._execute_node(node_id, node_context))
        tasks.append((node_id, task))

    # Wait for all to complete
    results = {}
    for node_id, task in tasks:
        try:
            result = await task
            results[node_id] = result
        except Exception as e:
            results[node_id] = {"error": str(e)}

    # Merge results back into main context
    context.outputs.update(results)
    return results

# Update run method to detect parallel opportunities
async def run(self, input_data: Dict[str, Any]) -> HAPContext:
    """Enhanced run with parallel detection."""
    context = HAPContext(inputs=input_data)

    # Analyze graph for parallel opportunities
    execution_plan = self._create_execution_plan()

    for stage in execution_plan:
        if len(stage) == 1:
            # Sequential execution
            await self._execute_node(stage[0], context)
        else:
            # Parallel execution
            await self._execute_parallel_nodes(stage, context)

    return context

def _create_execution_plan(self) -> List[List[str]]:
    """Create execution plan with parallel stages."""
    # Simple implementation - group nodes with same distance from entry
    plan = []
    visited = set()
    current_level = [self.graph.entry_node] if isinstance(self.graph.entry_node, str) else self.graph.entry_node

    while current_level:
        plan.append(current_level)
        visited.update(current_level)

        next_level = []
        for node_id in current_level:
            node = self.graph.nodes[node_id]
            for next_node in node.next_nodes:
                if next_node not in visited:
                    next_level.append(next_node)

        current_level = list(set(next_level))  # Remove duplicates

    return plan
```

### 3. Export to Standard Formats

**File**: `src/haive/hap/server/export.py` (new file)

```python
from typing import Literal
import yaml

class WorkflowExporter:
    """Export workflows to standard formats."""

    @staticmethod
    def to_github_actions(graph: HAPGraph) -> str:
        """Export workflow as GitHub Actions YAML."""
        jobs = {}

        for node_id, node in graph.nodes.items():
            job = {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": f"Execute {node_id}",
                        "run": f"haive-hap execute --node {node_id}"
                    }
                ]
            }

            if node.next_nodes:
                job["needs"] = node.next_nodes

            jobs[node_id] = job

        workflow = {
            "name": graph.name or "HAP Workflow",
            "on": ["workflow_dispatch"],
            "jobs": jobs
        }

        return yaml.dump(workflow, default_flow_style=False)

    @staticmethod
    def to_airflow(graph: HAPGraph) -> str:
        """Export workflow as Airflow DAG."""
        dag_code = f'''
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from haive.hap import HAPRuntime

dag = DAG(
    '{graph.name or "hap_workflow"}',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None
)

runtime = HAPRuntime(graph)
'''

        for node_id, node in graph.nodes.items():
            dag_code += f'''
def execute_{node_id}(**context):
    return runtime.execute_node("{node_id}", context["dag_run"].conf)

{node_id}_task = PythonOperator(
    task_id="{node_id}",
    python_callable=execute_{node_id},
    dag=dag
)
'''

        # Add dependencies
        for node_id, node in graph.nodes.items():
            for next_node in node.next_nodes:
                dag_code += f"\n{node_id}_task >> {next_node}_task"

        return dag_code

    @staticmethod
    def to_mermaid(graph: HAPGraph) -> str:
        """Export workflow as Mermaid diagram."""
        mermaid = ["graph TD"]

        for node_id, node in graph.nodes.items():
            label = node.description or node_id
            mermaid.append(f'    {node_id}["{label}"]')

        for node_id, node in graph.nodes.items():
            for next_node in node.next_nodes:
                mermaid.append(f"    {node_id} --> {next_node}")

        return "\n".join(mermaid)
```

## 📊 Medium-Term Improvements (Month 2-3)

### 1. Visual Workflow Designer

Create a simple web UI using FastAPI and Vue.js:

**File**: `src/haive/hap/designer/server.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI(title="HAP Workflow Designer")

@app.post("/api/workflows")
async def create_workflow(workflow: dict):
    """Create new workflow from visual design."""
    try:
        graph = HAPGraph.model_validate(workflow)
        # Save to file or database
        return {"id": str(uuid.uuid4()), "status": "created"}
    except ValidationError as e:
        raise HTTPException(400, detail=str(e))

@app.get("/api/workflows/{workflow_id}/export/{format}")
async def export_workflow(workflow_id: str, format: Literal["python", "yaml", "mermaid"]):
    """Export workflow in various formats."""
    # Load workflow
    graph = load_workflow(workflow_id)

    if format == "python":
        return {"code": graph.to_python_code()}
    elif format == "yaml":
        return {"code": WorkflowExporter.to_github_actions(graph)}
    elif format == "mermaid":
        return {"code": WorkflowExporter.to_mermaid(graph)}

app.mount("/", StaticFiles(directory="designer/dist", html=True))
```

### 2. Workflow Templates Library

**File**: `src/haive/hap/templates/__init__.py`

```python
from typing import Dict, Any
from haive.hap.models import HAPGraph

class WorkflowTemplate:
    """Base class for workflow templates."""

    name: str = "Template"
    description: str = "Template description"

    def create(self, **params) -> HAPGraph:
        """Create workflow instance with parameters."""
        raise NotImplementedError

class ResearchWorkflow(WorkflowTemplate):
    """Research → Analysis → Report workflow."""

    name = "Research Pipeline"
    description = "Comprehensive research workflow with analysis and reporting"

    def create(
        self,
        research_depth: str = "comprehensive",
        output_format: str = "markdown",
        include_citations: bool = True
    ) -> HAPGraph:
        graph = HAPGraph(name="research_pipeline")

        # Configure agents based on parameters
        research_config = {
            "temperature": 0.7 if research_depth == "comprehensive" else 0.5,
            "system_message": f"Conduct {research_depth} research with citations."
        }

        graph.add_entrypoint_node(
            "research",
            "haive.agents.research:ResearchAgent",
            config=research_config,
            next_nodes=["analyze"]
        )

        graph.add_entrypoint_node(
            "analyze",
            "haive.agents.analysis:AnalysisAgent",
            next_nodes=["report"]
        )

        graph.add_entrypoint_node(
            "report",
            "haive.agents.report:ReportAgent",
            config={"format": output_format, "citations": include_citations}
        )

        graph.entry_node = "research"
        return graph

# Registry of available templates
TEMPLATES = {
    "research": ResearchWorkflow(),
    "customer_support": CustomerSupportWorkflow(),
    "content_creation": ContentCreationWorkflow(),
    "data_pipeline": DataProcessingWorkflow()
}

def list_templates() -> Dict[str, str]:
    """List available workflow templates."""
    return {
        name: template.description
        for name, template in TEMPLATES.items()
    }

def create_from_template(template_name: str, **params) -> HAPGraph:
    """Create workflow from template."""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    return TEMPLATES[template_name].create(**params)
```

## 🎯 Implementation Priority

### Week 1-2: Foundation

1. ✅ Add ExecutionTrace to HAPRuntime
2. ✅ Implement basic retry logic
3. ✅ Add performance metrics collection

### Week 3-4: Resilience

1. ✅ Create CheckpointManager
2. ✅ Implement basic parallel execution
3. ✅ Add workflow export functionality

### Month 2: Developer Experience

1. 🔄 Build visual designer MVP
2. 🔄 Create workflow template library
3. 🔄 Add debugging tools

### Month 3: Production Features

1. 📅 Distributed execution support
2. 📅 Advanced error recovery
3. 📅 Performance optimization

## 📝 Testing Strategy

For each improvement, create tests following Haive's no-mock philosophy:

```python
# tests/test_observability.py
async def test_execution_trace_captures_all_events():
    """Test that execution trace captures node lifecycle."""
    graph = create_test_graph()
    runtime = HAPRuntime(graph)

    result = await runtime.run({"input": "test"})

    # Verify trace contains expected events
    trace_json = runtime.trace.to_json()
    events = json.loads(trace_json)

    assert any(e["type"] == "node_start" for e in events)
    assert any(e["type"] == "node_complete" for e in events)

    # Verify timeline generation
    timeline = runtime.trace.get_timeline()
    assert "→" in timeline
    assert "✓" in timeline

# tests/test_retry_logic.py
async def test_node_retry_on_transient_error():
    """Test that nodes retry on transient errors."""
    # Create agent that fails first time
    flaky_agent = FlakyAgent(fail_count=1)

    graph = HAPGraph()
    graph.add_agent_node(
        "flaky",
        flaky_agent,
        retry_config=RetryConfig(max_attempts=3, initial_delay=0.1)
    )

    runtime = HAPRuntime(graph)
    result = await runtime.run({})

    # Should succeed after retry
    assert result.outputs["flaky"]["status"] == "success"
    assert flaky_agent.attempt_count == 2
```

## 🎉 Expected Outcomes

After implementing these improvements:

1. **Better Visibility**: Know exactly what's happening in workflows
2. **Increased Reliability**: Workflows recover from transient failures
3. **Improved Performance**: Parallel execution where possible
4. **Enhanced Developer Experience**: Visual tools and templates
5. **Production Readiness**: Checkpoints, monitoring, and exports

---

**Next Step**: Start with Week 1-2 improvements. They're high-impact, low-risk, and will immediately improve the developer experience.
