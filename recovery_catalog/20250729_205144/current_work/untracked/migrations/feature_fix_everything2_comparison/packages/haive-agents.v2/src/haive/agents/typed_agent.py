"""Typed agent base classes with clear separation of concerns.

This module provides a cleaner agent hierarchy that matches the state schema
hierarchy, with better separation between different types of agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
)

from haive.core.schema.base_state_schemas import (
    AgentState,
    DataProcessingState,
    EngineState,
    MetaAgentState,
    ToolExecutorState,
    WorkflowState,
)

if TYPE_CHECKING:
    from haive.core.engine.base import Engine


# Type variables for state schemas
TState = TypeVar("TState", bound=EngineState)


# ============================================================================
# BASE EXECUTOR (NOT AGENT)
# ============================================================================


class BaseExecutor(ABC, Generic[TState]):
    """Base class for all executors (not necessarily agents).

    Executors are components that process state but don't necessarily
    have LLM capabilities. This includes tool executors, data processors,
    routers, validators, etc.
    """

    def __init__(self, name: str, state_schema: type[TState], **kwargs):
        self.name = name
        self.state_schema = state_schema
        self.config = kwargs

    @abstractmethod
    async def execute(self, state: TState) -> TState:
        """Execute the processing logic."""

    def get_required_engines(self) -> list[str]:
        """Get list of required engine names."""
        return []

    def validate_state(self, state: TState) -> bool:
        """Validate that state has required components."""
        # Check required engines
        return all(
            state.get_engine(engine_name) for engine_name in self.get_required_engines()
        )


class ToolExecutor(BaseExecutor[ToolExecutorState]):
    """Executor for tool-based workflows without LLM.

    Executes tools based on predefined plans or rules.
    """

    def __init__(self, name: str, execution_strategy: str = "sequential", **kwargs):
        super().__init__(name, ToolExecutorState, **kwargs)
        self.execution_strategy = execution_strategy

    async def execute(self, state: ToolExecutorState) -> ToolExecutorState:
        """Execute tools according to plan."""
        while state.current_step < len(state.execution_plan):
            step = state.execution_plan[state.current_step]

            if step["status"] == "pending":
                # Execute tool
                tool_name = step["tool"]
                inputs = step["inputs"]

                # Find tool
                tool = self._find_tool(state, tool_name)
                if tool:
                    result = await self._execute_tool(tool, inputs)
                    state.mark_step_complete(result)
                else:
                    state.mark_step_complete({"error": f"Tool {tool_name} not found"})

        return state

    def _find_tool(self, state: ToolExecutorState, tool_name: str) -> Any | None:
        """Find a tool by name."""
        for tool in state.tools:
            if hasattr(tool, "name") and tool.name == tool_name:
                return tool
        return None

    async def _execute_tool(self, tool: Any, inputs: dict[str, Any]) -> Any:
        """Execute a single tool."""
        # Tool execution logic
        if hasattr(tool, "ainvoke"):
            return await tool.ainvoke(inputs)
        if hasattr(tool, "invoke"):
            return tool.invoke(inputs)
        return {"error": "Tool not executable"}


class DataProcessor(BaseExecutor[DataProcessingState]):
    """Executor for data processing workflows.

    Processes data through various transformation engines.
    """

    def __init__(self, name: str, required_engines: list[str], **kwargs):
        super().__init__(name, DataProcessingState, **kwargs)
        self.required_engines = required_engines

    def get_required_engines(self) -> list[str]:
        """Get list of required engine names."""
        return self.required_engines

    async def execute(self, state: DataProcessingState) -> DataProcessingState:
        """Process data through stages."""
        current_data = state.input_data

        for stage in state.processing_stages:
            # Get engine for this stage
            engine = state.get_engine(stage)
            if engine:
                # Process data
                result = await self._process_with_engine(engine, current_data)
                state.stage_results[stage] = result
                current_data = result
            else:
                state.stage_results[stage] = {"error": f"Engine {stage} not found"}

        state.processed_data = current_data
        return state

    async def _process_with_engine(self, engine: Engine, data: Any) -> Any:
        """Process data with a specific engine."""
        # Engine-specific processing
        if hasattr(engine, "process"):
            return await engine.process(data)
        return data


# ============================================================================
# AGENT CLASSES (WITH LLM/DECISION MAKING)
# ============================================================================


class BaseAgent(BaseExecutor[AgentState]):
    """Base class for agents with primary decision-making engine.

    Agents are executors that have a primary engine (usually LLM)
    for making decisions.
    """

    def __init__(
        self,
        name: str,
        primary_engine: Engine | None = None,
        state_schema: type[AgentState] = AgentState,
        **kwargs,
    ):
        super().__init__(name, state_schema, **kwargs)
        self.primary_engine = primary_engine

    async def execute(self, state: AgentState) -> AgentState:
        """Execute agent logic."""
        # Ensure primary engine is available
        if self.primary_engine and not state.engine:
            state.engine = self.primary_engine

        # Get the engine
        engine = state.primary_engine
        if not engine:
            raise ValueError(
                f"No primary engine available for agent {
                    self.name}"
            )

        # Execute main agent logic
        result = await self.run_engine(engine, state)

        # Update state with results
        state = self.update_state_with_result(state, result)

        return state

    @abstractmethod
    async def run_engine(self, engine: Engine, state: AgentState) -> Any:
        """Run the primary engine with state."""

    def update_state_with_result(self, state: AgentState, result: Any) -> AgentState:
        """Update state with engine result."""
        # Default: just return state
        # Subclasses should override
        return state


class LLMAgent(BaseAgent):
    """Standard LLM-based agent.

    Uses an LLM engine for conversation and decision making.
    """

    async def run_engine(self, engine: Engine, state: AgentState) -> Any:
        """Run LLM engine."""
        # Prepare input from state
        messages = getattr(state, "messages", [])

        # Run engine
        if hasattr(engine, "ainvoke"):
            return await engine.ainvoke({"messages": messages})
        return engine.invoke({"messages": messages})

    def update_state_with_result(self, state: AgentState, result: Any) -> AgentState:
        """Update state with LLM result."""
        if isinstance(result, dict) and "messages" in result:
            state.messages.extend(result["messages"])
        elif hasattr(result, "content"):
            # Single message response
            state.add_message(result)

        return state


class WorkflowAgent(BaseAgent):
    """Agent that can modify its own workflow graph.

    This agent can inspect results and dynamically modify its
    execution graph.
    """

    def __init__(
        self,
        name: str,
        primary_engine: Engine | None = None,
        initial_graph: dict[str, Any] | None = None,
        **kwargs,
    ):
        super().__init__(name, primary_engine, WorkflowState, **kwargs)
        self.initial_graph = initial_graph

    async def execute(self, state: WorkflowState) -> WorkflowState:
        """Execute with potential graph modification."""
        # Initialize graph if needed
        if state.graph is None and self.initial_graph:
            state.graph = self.initial_graph

        # Run normal agent logic
        state = await super().execute(state)

        # Check if we should modify graph
        if self.should_modify_graph(state):
            modifications = await self.determine_graph_modifications(state)
            state.modify_graph(modifications)

        return state

    def should_modify_graph(self, state: WorkflowState) -> bool:
        """Determine if graph should be modified."""
        # Override in subclasses
        return False

    async def determine_graph_modifications(
        self, state: WorkflowState
    ) -> dict[str, Any]:
        """Determine what graph modifications to make."""
        # Override in subclasses
        return {}


class MetaAgent(WorkflowAgent):
    """Agent that can spawn and manage other agents.

    This is for advanced scenarios where agents need to dynamically
    create and coordinate other agents.
    """

    def __init__(
        self,
        name: str,
        primary_engine: Engine | None = None,
        agent_factory: dict[str, type[BaseAgent]] | None = None,
        **kwargs,
    ):
        super().__init__(name, primary_engine, **kwargs)
        self.agent_factory = agent_factory or {}
        self.state_schema = MetaAgentState

    async def execute(self, state: MetaAgentState) -> MetaAgentState:
        """Execute meta-agent logic."""
        # Run main logic
        state = await super().execute(state)

        # Check if we need to spawn agents
        if self.should_spawn_agents(state):
            await self.spawn_agents(state)

        # Execute active sub-agents
        if state.active_sub_agents:
            await self.execute_sub_agents(state)

        # Aggregate results if needed
        if self.should_aggregate(state):
            self.aggregate_results(state)

        return state

    def should_spawn_agents(self, state: MetaAgentState) -> bool:
        """Determine if new agents should be spawned."""
        # Override in subclasses
        return False

    async def spawn_agents(self, state: MetaAgentState) -> None:
        """Spawn new sub-agents."""
        # Override in subclasses

    async def execute_sub_agents(self, state: MetaAgentState) -> None:
        """Execute active sub-agents."""
        for agent_name in state.active_sub_agents:
            if agent_name in state.sub_agents:
                agent_data = state.sub_agents[agent_name]
                agent_type = agent_data.get("agent_type", "base")

                # Create agent instance
                if agent_type in self.agent_factory:
                    agent_class = self.agent_factory[agent_type]
                    agent = agent_class(name=agent_name)

                    # Execute with sub-agent state
                    # This is simplified - real implementation would handle
                    # state isolation
                    result = await agent.execute(state)
                    state.update_sub_agent_result(agent_name, result)

    def should_aggregate(self, state: MetaAgentState) -> bool:
        """Determine if results should be aggregated."""
        return len(state.sub_agent_results) > 0

    def aggregate_results(self, state: MetaAgentState) -> None:
        """Aggregate sub-agent results."""
        # Default: merge all results
        aggregated = {}
        for result in state.sub_agent_results.values():
            if isinstance(result, dict):
                aggregated.update(result)

        state.metadata["aggregated_results"] = aggregated


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================


class ReactiveAgent(LLMAgent):
    """Agent that reacts to specific patterns or triggers.

    Useful for monitoring, alerting, or event-driven workflows.
    """

    def __init__(self, name: str, triggers: list[dict[str, Any]], **kwargs):
        super().__init__(name, **kwargs)
        self.triggers = triggers

    async def execute(self, state: AgentState) -> AgentState:
        """Check triggers before normal execution."""
        triggered = self.check_triggers(state)

        if triggered:
            # Modify behavior based on trigger
            state.metadata["triggered"] = triggered

        return await super().execute(state)

    def check_triggers(self, state: AgentState) -> list[str]:
        """Check which triggers are activated."""
        triggered = []

        for trigger in self.triggers:
            if self.evaluate_trigger(trigger, state):
                triggered.append(trigger.get("name", "unnamed"))

        return triggered

    def evaluate_trigger(self, trigger: dict[str, Any], state: AgentState) -> bool:
        """Evaluate a single trigger."""
        # Simple pattern matching on messages
        pattern = trigger.get("pattern")
        if pattern and hasattr(state, "messages"):
            last_message = state.get_last_message()
            if last_message and pattern in str(last_message.content):
                return True

        return False


class AdaptiveAgent(WorkflowAgent):
    """Agent that adapts its behavior based on performance.

    Tracks its own performance and modifies strategy accordingly.
    """

    def __init__(
        self,
        name: str,
        performance_metrics: list[str],
        adaptation_threshold: float = 0.7,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.performance_metrics = performance_metrics
        self.adaptation_threshold = adaptation_threshold
        self.performance_history: list[dict[str, float]] = []

    async def execute(self, state: WorkflowState) -> WorkflowState:
        """Execute with performance tracking."""
        # Execute normally
        state = await super().execute(state)

        # Track performance
        metrics = self.calculate_performance(state)
        self.performance_history.append(metrics)

        # Check if adaptation needed
        if self.needs_adaptation(metrics):
            await self.adapt_strategy(state)

        return state

    def calculate_performance(self, state: WorkflowState) -> dict[str, float]:
        """Calculate performance metrics."""
        # Override in subclasses
        return {}

    def needs_adaptation(self, metrics: dict[str, float]) -> bool:
        """Check if adaptation is needed."""
        # Simple threshold check
        avg_performance = sum(metrics.values()) / len(metrics) if metrics else 0
        return avg_performance < self.adaptation_threshold

    async def adapt_strategy(self, state: WorkflowState) -> None:
        """Adapt the agent's strategy."""
        # Override in subclasses


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_executor(executor_type: str, name: str, **kwargs) -> BaseExecutor:
    """Factory to create appropriate executor.

    Args:
        executor_type: Type of executor
        name: Name for the executor
        **kwargs: Additional arguments

    Returns:
        Executor instance
    """
    if executor_type == "tool":
        return ToolExecutor(name, **kwargs)
    if executor_type == "data":
        return DataProcessor(name, **kwargs)
    raise ValueError(f"Unknown executor type: {executor_type}")


def create_agent(
    agent_type: str, name: str, engine: Engine | None = None, **kwargs
) -> BaseAgent:
    """Factory to create appropriate agent.

    Args:
        agent_type: Type of agent
        name: Name for the agent
        engine: Primary engine for the agent
        **kwargs: Additional arguments

    Returns:
        Agent instance
    """
    if agent_type == "llm":
        return LLMAgent(name, engine, **kwargs)
    if agent_type == "workflow":
        return WorkflowAgent(name, engine, **kwargs)
    if agent_type == "meta":
        return MetaAgent(name, engine, **kwargs)
    if agent_type == "reactive":
        return ReactiveAgent(name, engine, **kwargs)
    if agent_type == "adaptive":
        return AdaptiveAgent(name, engine, **kwargs)
    return BaseAgent(name, engine, **kwargs)
