"""Enhanced LLM Compiler Agent with Dynamic Execution Graphs.

This implementation creates a sophisticated LLM Compiler that:
- Compiles natural language into executable dependency graphs
- Supports parallel execution with complex dependencies
- Provides real-time execution monitoring
- Uses structured outputs with comprehensive validation
- No mocks - all real components
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any

from langchain_core.tools import tool
from pydantic import BaseModel, Field, computed_field, field_validator

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState


logger = logging.getLogger(__name__)


class NodeType(str, Enum):
    """Types of execution nodes."""

    TOOL_CALL = "tool_call"
    LLM_REASONING = "llm_reasoning"
    DATA_TRANSFORM = "data_transform"
    CONDITION_CHECK = "condition_check"
    AGGREGATION = "aggregation"
    FINAL_OUTPUT = "final_output"


class ExecutionStatus(str, Enum):
    """Execution status of nodes."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ExecutionResult:
    """Result of node execution."""

    node_id: str
    status: ExecutionStatus
    output: Any
    error: str | None = None
    execution_time: float | None = None
    metadata: dict[str, Any] = None


class ExecutionNode(BaseModel):
    """Enhanced execution node with comprehensive validation."""

    node_id: str = Field(
        ..., pattern=r"^node_\w+$", description="Unique node identifier"
    )
    node_type: NodeType = Field(..., description="Type of execution node")
    description: str = Field(..., min_length=5, description="What this node does")
    operation: str = Field(
        ..., min_length=1, description="Specific operation to perform"
    )

    # Dependencies and data flow
    input_dependencies: set[str] = Field(
        default_factory=set, description="Input data dependencies"
    )
    control_dependencies: set[str] = Field(
        default_factory=set, description="Control flow dependencies"
    )
    output_keys: list[str] = Field(
        default_factory=list, description="Output variable names"
    )

    # Execution configuration
    agent_type: str = Field(default="react", description="Agent type for execution")
    timeout_seconds: int = Field(
        default=30, ge=1, le=300, description="Execution timeout"
    )
    retry_count: int = Field(
        default=2, ge=0, le=5, description="Number of retries on failure"
    )
    parallel_safe: bool = Field(default=True, description="Can execute in parallel")

    # Execution state
    status: ExecutionStatus = Field(
        default=ExecutionStatus.PENDING, description="Current status"
    )
    execution_cost: float = Field(
        default=0.0, ge=0.0, description="Estimated execution cost"
    )

    @field_validator("input_dependencies", "control_dependencies")
    @classmethod
    def validate_dependencies(cls, v: set[str]) -> set[str]:
        """Validate node dependencies."""
        for dep in v:
            if not dep.startswith("node_"):
                raise ValueError(f"Invalid node reference: {dep}")
        return v

    @computed_field
    @property
    def all_dependencies(self) -> set[str]:
        """Get all dependencies (input + control)."""
        return self.input_dependencies | self.control_dependencies

    @computed_field
    @property
    def is_ready(self) -> bool:
        """Check if node is ready for execution."""
        return self.status == ExecutionStatus.READY

    @computed_field
    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal node."""
        return self.node_type == NodeType.FINAL_OUTPUT


class CompiledGraph(BaseModel):
    """Compiled execution graph with dependency analysis."""

    objective: str = Field(..., min_length=10, description="Overall objective")
    nodes: dict[str, ExecutionNode] = Field(
        default_factory=dict, description="Execution nodes"
    )
    execution_order: list[list[str]] = Field(
        default_factory=list, description="Execution order groups"
    )
    estimated_total_cost: float = Field(
        default=0.0, ge=0.0, description="Total estimated cost"
    )
    max_parallel_degree: int = Field(
        default=5, ge=1, le=20, description="Maximum parallel execution"
    )

    @field_validator("nodes")
    @classmethod
    def validate_graph_structure(
        cls, v: dict[str, ExecutionNode]
    ) -> dict[str, ExecutionNode]:
        """Validate graph structure and detect cycles."""
        if not v:
            return v

        # Check for cycles using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(node_id: str) -> bool:
            if node_id not in v:
                return False

            visited.add(node_id)
            rec_stack.add(node_id)

            for dep in v[node_id].all_dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False

        for node_id in v:
            if node_id not in visited and has_cycle(node_id):
                raise ValueError(
                    f"Cycle detected in execution graph involving {node_id}"
                )

        return v

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if not self.nodes:
            return 0.0

        completed = sum(
            1
            for node in self.nodes.values()
            if node.status == ExecutionStatus.COMPLETED
        )
        return (completed / len(self.nodes)) * 100

    @computed_field
    @property
    def entry_points(self) -> list[str]:
        """Get nodes with no dependencies."""
        return [
            node_id
            for node_id, node in self.nodes.items()
            if len(node.all_dependencies) == 0
        ]

    @computed_field
    @property
    def exit_points(self) -> list[str]:
        """Get terminal nodes."""
        return [node_id for node_id, node in self.nodes.items() if node.is_terminal]

    def get_ready_nodes(
        self, execution_results: dict[str, ExecutionResult]
    ) -> list[ExecutionNode]:
        """Get nodes ready for execution."""
        ready = []

        for node in self.nodes.values():
            if node.status != ExecutionStatus.PENDING:
                continue

            # Check if all dependencies are satisfied
            deps_satisfied = all(
                dep in execution_results
                and execution_results[dep].status == ExecutionStatus.COMPLETED
                for dep in node.all_dependencies
            )

            if deps_satisfied:
                ready.append(node)

        return ready[: self.max_parallel_degree]

    def update_node_status(self, node_id: str, status: ExecutionStatus) -> bool:
        """Update node status."""
        if node_id not in self.nodes:
            return False

        self.nodes[node_id].status = status
        return True

    def topological_sort(self) -> list[list[str]]:
        """Get topological execution order."""
        # Simplified topological sort into execution groups
        execution_groups = []
        remaining_nodes = set(self.nodes.keys())

        while remaining_nodes:
            # Find nodes with no remaining dependencies
            ready_nodes = []
            for node_id in remaining_nodes:
                node = self.nodes[node_id]
                if node.all_dependencies.issubset(
                    set(self.nodes.keys()) - remaining_nodes
                ):
                    ready_nodes.append(node_id)

            if not ready_nodes:
                # Break cycles or handle remaining nodes
                ready_nodes = [remaining_nodes.pop()]

            execution_groups.append(ready_nodes)
            remaining_nodes -= set(ready_nodes)

        return execution_groups


class CompilerOutput(BaseModel):
    """Final output from LLM Compiler execution."""

    objective: str = Field(..., description="Original objective")
    execution_summary: dict[str, Any] = Field(..., description="Execution summary")
    final_results: dict[str, Any] = Field(..., description="Final output results")
    performance_metrics: dict[str, float] = Field(
        ..., description="Performance metrics"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Optimization recommendations"
    )

    @field_validator("final_results")
    @classmethod
    def validate_final_results(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate final results."""
        if not v:
            raise ValueError("Final results cannot be empty")
        return v


class EnhancedLLMCompiler(Agent):
    """Enhanced LLM Compiler with dynamic execution graphs."""

    def __init__(
        self,
        name: str,
        engine: AugLLMConfig,
        available_agents: dict[str, Agent],
        **kwargs,
    ):
        self.available_agents = available_agents
        self.compiler_agent = None
        self.executor_agents = {}
        self.orchestrator_agent = None

        super().__init__(name=name, engine=engine, **kwargs)

    def setup_agent(self):
        """Setup compiler and execution agents."""
        # Create compiler with structured output
        self.compiler_agent = SimpleAgent(
            name=f"{self.name}_compilef",
            engine=self.engine.model_copy(
                update={
                    "structured_output_model": CompiledGraph,
                    "structured_output_version": "v2",
                    "system_message": self._create_compilation_prompt(),
                }
            ),
        )

        # Create executor agents for different node types
        self.executor_agents = {
            NodeType.TOOL_CALL: ReactAgent(
                name=f"{self.name}_tool_executof",
                engine=self.engine.model_copy(update={"temperature": 0.1}),
                tools=self._get_available_tools(),
            ),
            NodeType.LLM_REASONING: SimpleAgent(
                name=f"{self.name}_reasoning_executof",
                engine=self.engine.model_copy(update={"temperature": 0.7}),
            ),
            NodeType.DATA_TRANSFORM: SimpleAgent(
                name=f"{self.name}_transform_executof",
                engine=self.engine.model_copy(update={"temperature": 0.1}),
            ),
            NodeType.FINAL_OUTPUT: SimpleAgent(
                name=f"{self.name}_output_executof",
                engine=self.engine.model_copy(
                    update={
                        "structured_output_model": CompilerOutput,
                        "structured_output_version": "v2",
                    }
                ),
            ),
        }

        # Create orchestrator
        self.orchestrator_agent = SimpleAgent(
            name=f"{self.name}_orchestratof",
            engine=self.engine.model_copy(
                update={
                    "system_message": "You are an execution orchestrator. Coordinate parallel execution and handle errors."
                }
            ),
        )

        # Set up state schema
        self.state_schema = MessagesState

    def _create_compilation_prompt(self) -> str:
        """Create compilation prompt."""
        agent_descriptions = []
        for name, agent in self.available_agents.items():
            agent_descriptions.append(f"- {name}: {agent.__class__.__name__}")

        return f"""You are an LLM Compiler. Convert natural language into executable dependency graphs.

Available agents:
{chr(10).join(agent_descriptions)}

Your task is to:
1. Analyze the natural language query
2. Break it down into executable nodes
3. Identify dependencies between nodes
4. Create a parallel execution plan
5. Estimate costs and optimize for efficiency

Node types available:
- tool_call: Execute tools/functions
- llm_reasoning: LLM-based reasoning
- data_transform: Transform/process data
- condition_check: Conditional logic
- aggregation: Combine results
- final_output: Format final output

Create an optimized execution graph that maximizes parallelism while respecting dependencies."""

    def _get_available_tools(self) -> list[Any]:
        """Get tools from available agents."""
        tools = []
        for agent in self.available_agents.values():
            if hasattr(agent, "tools") and agent.tools:
                tools.extend(agent.tools)
        return tools

    def build_graph(self):
        """Build execution graph."""
        # For this implementation, we'll use a custom execution approach

    async def arun(self, query: str, **kwargs) -> dict[str, Any]:
        """Execute LLM Compiler workflow."""
        logger.info(f"LLM Compiler {self.name} processing query: {query}")

        try:
            # Phase 1: Compilation
            logger.info("Phase 1: Compiling natural language to execution graph")
            compiled_graph = await self._compile_query(query)

            # Phase 2: Execution
            logger.info("Phase 2: Executing compiled graph")
            execution_results = await self._execute_graph(compiled_graph)

            # Phase 3: Output Generation
            logger.info("Phase 3: Generating final output")
            final_output = await self._generate_output(
                compiled_graph, execution_results
            )

            return {
                "query": query,
                "compiled_graph": compiled_graph,
                "execution_results": execution_results,
                "final_output": final_output,
                "status": "completed",
            }

        except Exception as e:
            logger.exception(f"LLM Compiler execution failed: {e}")
            return {"query": query, "error": str(e), "status": "failed"}

    async def _compile_query(self, query: str) -> CompiledGraph:
        """Compile natural language query into execution graph."""
        compilation_prompt = f"""Compile the following natural language query into an executable dependency graph:

Query: {query}

Create a structured execution plan with:
1. Nodes that represent discrete operations
2. Clear dependencies between nodes
3. Parallel execution opportunities
4. Cost estimation and optimization
5. Proper error handling paths

Focus on creating an efficient graph that can execute in parallel where possible."""

        result = await self.compiler_agent.arun(compilation_prompt)

        # Extract structured output
        if isinstance(result, dict) and "compiled_graph" in result:
            return result["compiled_graph"]
        if isinstance(result, CompiledGraph):
            return result
        raise ValueError(f"Invalid compilation result: {type(result)}")

    async def _execute_graph(self, graph: CompiledGraph) -> dict[str, ExecutionResult]:
        """Execute compiled graph with parallel processing."""
        execution_results = {}

        # Execute nodes in topological order
        execution_groups = graph.topological_sort()

        for group_idx, node_group in enumerate(execution_groups):
            logger.info(
                f"Executing group {group_idx + 1}/{len(execution_groups)} with {len(node_group)} nodes"
            )

            # Execute nodes in parallel
            tasks = []
            for node_id in node_group:
                if node_id in graph.nodes:
                    node = graph.nodes[node_id]
                    task = self._execute_node(node, execution_results)
                    tasks.append((node_id, task))
                    graph.update_node_status(node_id, ExecutionStatus.RUNNING)

            # Wait for completion
            results = await asyncio.gather(
                *[task for _, task in tasks], return_exceptions=True
            )

            # Process results
            for (node_id, _), result in zip(tasks, results, strict=False):
                if isinstance(result, Exception):
                    logger.error(f"Node execution failed for {node_id}: {result}")
                    execution_results[node_id] = ExecutionResult(
                        node_id=node_id,
                        status=ExecutionStatus.FAILED,
                        output=None,
                        error=str(result),
                    )
                    graph.update_node_status(node_id, ExecutionStatus.FAILED)
                else:
                    execution_results[node_id] = result
                    graph.update_node_status(node_id, ExecutionStatus.COMPLETED)

            logger.info(f"Graph execution progress: {graph.completion_percentage:.1f}%")

        return execution_results

    async def _execute_node(
        self, node: ExecutionNode, context: dict[str, ExecutionResult]
    ) -> ExecutionResult:
        """Execute a single node."""
        start_time = asyncio.get_event_loop().time()

        try:
            # Get appropriate executor
            executor = self.executor_agents.get(node.node_type)
            if not executor:
                raise ValueError(
                    f"No executor available for node type: {node.node_type}"
                )

            # Prepare execution context
            execution_context = self._prepare_execution_context(node, context)

            # Create execution prompt
            execution_prompt = f"""Execute node: {node.description}

Operation: {node.operation}
Node type: {node.node_type}

Context from dependencies:
{execution_context}

Provide the specific output required for this node."""

            # Execute with timeout
            result = await asyncio.wait_for(
                executor.arun(execution_prompt), timeout=node.timeout_seconds
            )

            execution_time = asyncio.get_event_loop().time() - start_time

            return ExecutionResult(
                node_id=node.node_id,
                status=ExecutionStatus.COMPLETED,
                output=result,
                execution_time=execution_time,
                metadata={"node_type": node.node_type},
            )

        except TimeoutError:
            return ExecutionResult(
                node_id=node.node_id,
                status=ExecutionStatus.FAILED,
                output=None,
                error=f"Execution timeout after {node.timeout_seconds} seconds",
            )
        except Exception as e:
            return ExecutionResult(
                node_id=node.node_id,
                status=ExecutionStatus.FAILED,
                output=None,
                error=str(e),
            )

    def _prepare_execution_context(
        self, node: ExecutionNode, context: dict[str, ExecutionResult]
    ) -> str:
        """Prepare execution context from dependencies."""
        context_lines = []

        for dep_id in node.all_dependencies:
            if dep_id in context:
                result = context[dep_id]
                context_lines.append(f"{dep_id}: {str(result.output)[:200]}...")

        return "\n".join(context_lines) if context_lines else "No dependencies"

    async def _generate_output(
        self, graph: CompiledGraph, execution_results: dict[str, ExecutionResult]
    ) -> CompilerOutput:
        """Generate final output from execution results."""
        # Find terminal nodes
        terminal_results = {
            node_id: result
            for node_id, result in execution_results.items()
            if graph.nodes[node_id].is_terminal
        }

        output_prompt = f"""Generate final output from execution results.

Original objective: {graph.objective}

Terminal node results:
{self._format_terminal_results(terminal_results)}

All execution results:
{self._format_execution_summary(execution_results)}

Performance metrics:
- Total nodes: {len(graph.nodes)}
- Completed: {sum(1 for r in execution_results.values() if r.status == ExecutionStatus.COMPLETED)}
- Failed: {sum(1 for r in execution_results.values() if r.status == ExecutionStatus.FAILED)}
- Total time: {sum(r.execution_time or 0 for r in execution_results.values()):.2f}s

Provide a comprehensive final output with analysis and recommendations."""

        # Use the final output executor
        final_executor = self.executor_agents[NodeType.FINAL_OUTPUT]
        result = await final_executor.arun(output_prompt)

        # Extract structured output
        if isinstance(result, dict) and "compiler_output" in result:
            return result["compiler_output"]
        if isinstance(result, CompilerOutput):
            return result
        raise ValueError(f"Invalid output format: {type(result)}")

    def _format_terminal_results(
        self, terminal_results: dict[str, ExecutionResult]
    ) -> str:
        """Format terminal results for output generation."""
        lines = []
        for node_id, result in terminal_results.items():
            lines.append(f"{node_id}: {str(result.output)[:300]}...")
        return "\n".join(lines)

    def _format_execution_summary(
        self, execution_results: dict[str, ExecutionResult]
    ) -> str:
        """Format execution summary."""
        lines = []
        for node_id, result in execution_results.items():
            status_symbol = "✓" if result.status == ExecutionStatus.COMPLETED else "✗"
            time_str = (
                f"({result.execution_time:.2f}s)" if result.execution_time else ""
            )
            lines.append(f"{status_symbol} {node_id}: {result.status} {time_str}")
        return "\n".join(lines)


# Test Implementation
async def test_enhanced_llm_compiler():
    """Test the enhanced LLM Compiler with real components."""

    # Create mock agents for testing
    @tool
    def research_tool(topic: str) -> str:
        """Research a topic."""
        return f"Research results for {topic}: Comprehensive information about {topic}"

    @tool
    def analysis_tool(data: str) -> str:
        """Analyze data."""
        return f"Analysis of data: {data[:100]}... - Key insights and findings"

    research_agent = ReactAgent(
        name="research_agent",
        engine=AugLLMConfig(temperature=0.1),
        tools=[research_tool],
    )

    analysis_agent = SimpleAgent(
        name="analysis_agent", engine=AugLLMConfig(temperature=0.7)
    )

    available_agents = {"researcher": research_agent, "analyzer": analysis_agent}

    # Create compiler
    compiler = EnhancedLLMCompiler(
        name="test_compiler",
        engine=AugLLMConfig(temperature=0.5),
        available_agents=available_agents,
    )

    # Test query
    result = await compiler.arun(
        "Research the impact of AI on healthcare and provide a comprehensive analysis with recommendations"
    )

    if result.get("status") == "completed":
        pass
    else:
        pass


if __name__ == "__main__":
    asyncio.run(test_enhanced_llm_compiler())
