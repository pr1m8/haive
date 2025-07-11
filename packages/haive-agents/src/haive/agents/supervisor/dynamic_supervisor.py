"""Dynamic LangGraph-style Supervisor Implementation.

This module provides a dynamic supervisor agent that can add/remove agents at runtime,
adapt agent responses, and handle complex multi-agent coordination patterns similar
to LangGraph's supervisor package but with enhanced Haive-specific functionality.
"""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import uuid4

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor.dynamic_state import (
    AgentExecutionConfig,
    AgentExecutionResult,
    DynamicSupervisorState,
    SupervisorDecision,
)
from haive.agents.supervisor.registry import AgentRegistry

logger = logging.getLogger(__name__)
console = Console()


class DynamicSupervisorAgent(ReactAgent):
    """Dynamic supervisor agent with runtime agent management and adaptive responses.

    This supervisor extends the base haive Agent architecture to provide:
    - Runtime agent registration/deregistration
    - Dynamic graph rebuilding
    - Adaptive response handling
    - Performance monitoring and optimization
    - LangGraph-style coordination patterns

    Key features:
    - Hot-swappable agent configuration
    - Intelligent routing with reasoning
    - Response adaptation and filtering
    - Parallel and sequential execution modes
    - Comprehensive performance tracking
    """

    def __init__(
        self,
        name: str = "dynamic_supervisor",
        engine: AugLLMConfig | None = None,
        auto_rebuild_graph: bool = True,
        max_execution_history: int = 100,
        enable_parallel_execution: bool = False,
        **kwargs,
    ):
        """Initialize dynamic supervisor agent.

        Args:
            name: Supervisor agent name
            engine: LLM engine for routing decisions
            auto_rebuild_graph: Whether to automatically rebuild graph on agent changes
            max_execution_history: Maximum execution history to maintain
            enable_parallel_execution: Enable parallel agent execution
            **kwargs: Additional Agent arguments
        """
        # Set enhanced state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = DynamicSupervisorState

        super().__init__(name=name, engine=engine, **kwargs)

        # Configuration
        self.auto_rebuild_graph = auto_rebuild_graph
        self.max_execution_history = max_execution_history
        self.enable_parallel_execution = enable_parallel_execution

        # Internal state
        self._graph_built = False
        self._execution_lock = asyncio.Lock()
        self._performance_monitor = PerformanceMonitor()

        # Initialize agent registry with enhanced capabilities
        from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel

        routing_model = DynamicChoiceModel[str](
            options=[], model_name="DynamicSupervisorChoice", include_end=True
        )
        self.agent_registry = AgentRegistry(routing_model)

        logger.info(f"DynamicSupervisorAgent '{name}' initialized")

    def _aggregate_agent_tools(self) -> dict:
        """Aggregate tools from all registered agents into supervisor routing options."""
        aggregated_tools = {}
        tool_to_agent_mapping = {}

        for agent_name in self.agent_registry.get_available_agents():
            agent = self.agent_registry.get_agent(agent_name)
            if not agent:
                continue

            # Get agent's tools if they exist
            agent_tools = []
            if hasattr(agent, "tools") and agent.tools:
                agent_tools.extend(agent.tools)
            if (
                hasattr(agent, "engine")
                and agent.engine
                and hasattr(agent.engine, "tools")
            ) and agent.engine.tools:
                agent_tools.extend(agent.engine.tools)

            # Add tools to aggregated set with agent mapping
            for tool in agent_tools:
                tool_name = getattr(tool, "name", str(tool))
                aggregated_tools[tool_name] = tool
                tool_to_agent_mapping[tool_name] = agent_name

        return {"tools": aggregated_tools, "tool_to_agent": tool_to_agent_mapping}

    def _create_dynamic_tool_choice(self) -> str:
        """Create dynamic routing choice that includes tools from registered agents."""
        tool_info = self._aggregate_agent_tools()

        # Update supervisor's routing model to include agent tools as options
        available_agents = self.agent_registry.get_available_agents()
        all_options = available_agents.copy()

        # Add tool-based routing options
        for tool_name, agent_name in tool_info["tool_to_agent"].items():
            # Create routing option for tool that maps to owning agent
            option_name = f"use_{tool_name}_via_{agent_name}"
            all_options.append(option_name)

        return tool_info

    def _update_supervisor_tools(self) -> None:
        """Update supervisor's own engine tools with aggregated agent tools."""
        if not self.main_engine:
            return

        tool_info = self._aggregate_agent_tools()
        aggregated_tools = list(tool_info.get("tools", {}).values())

        # Update supervisor engine with all agent tools
        if hasattr(self.main_engine, "tools"):
            self.main_engine.tools = aggregated_tools
            logger.info(
                f"Updated supervisor tools: {len(aggregated_tools)} total tools from registered agents"
            )

        # Update tool routes mapping
        if hasattr(self.main_engine, "tool_routes"):
            tool_routes = {}
            for tool_name in tool_info.get("tools", {}):
                tool_routes[tool_name] = "langchain_tool"  # Default route type
            self.main_engine.tool_routes = tool_routes

    async def register_agent(
        self,
        agent: Agent,
        capability_description: str | None = None,
        execution_config: dict[str, Any] | None = None,
        rebuild_graph: bool | None = None,
    ) -> bool:
        """Register an agent with enhanced configuration.

        Args:
            agent: Agent instance to register
            capability_description: Description of agent capabilities
            execution_config: Custom execution configuration
            rebuild_graph: Whether to rebuild graph (uses auto_rebuild_graph if None)

        Returns:
            bool: True if registration successful
        """
        # Create execution config
        config = AgentExecutionConfig(
            agent_name=agent.name,
            capability_description=capability_description
            or f"Handles {agent.name} tasks",
            agent_type=agent.__class__.__name__,
            **(execution_config or {}),
        )

        # Register with base registry
        success = self.agent_registry.register(agent, capability_description)

        if success:
            # Update state with config
            if hasattr(self, "_state") and self._state:
                self._state.add_agent_config(agent.name, config)

            # Update supervisor tools with new agent's tools
            self._update_supervisor_tools()

            # Rebuild graph if needed
            should_rebuild = (
                rebuild_graph if rebuild_graph is not None else self.auto_rebuild_graph
            )
            if should_rebuild and self._graph_built:
                await self._rebuild_graph()

            console.print(f"[green]✅ Registered dynamic agent:[/green] {agent.name}")

        return success

    async def unregister_agent(
        self, agent_name: str, rebuild_graph: bool | None = None
    ) -> bool:
        """Unregister an agent with graph rebuilding.

        Args:
            agent_name: Name of agent to remove
            rebuild_graph: Whether to rebuild graph (uses auto_rebuild_graph if None)

        Returns:
            bool: True if removal successful
        """
        success = self.agent_registry.unregister(agent_name)

        if success:
            # Update state
            if hasattr(self, "_state") and self._state:
                self._state.remove_agent_config(agent_name)

            # Update supervisor tools after removing agent
            self._update_supervisor_tools()

            # Rebuild graph if needed
            should_rebuild = (
                rebuild_graph if rebuild_graph is not None else self.auto_rebuild_graph
            )
            if should_rebuild and self._graph_built:
                await self._rebuild_graph()

            console.print(f"[red]❌ Unregistered dynamic agent:[/red] {agent_name}")

        return success

    async def update_agent_config(
        self, agent_name: str, config_updates: dict[str, Any]
    ) -> bool:
        """Update agent execution configuration at runtime.

        Args:
            agent_name: Name of agent to update
            config_updates: Configuration updates to apply

        Returns:
            bool: True if update successful
        """
        if not self.agent_registry.is_agent_registered(agent_name):
            logger.warning(f"Agent {agent_name} not registered")
            return False

        if hasattr(self, "_state") and self._state:
            config = self._state.get_agent_config(agent_name)
            if config:
                # Update configuration
                for key, value in config_updates.items():
                    if hasattr(config, key):
                        setattr(config, key, value)

                logger.info(f"Updated configuration for agent {agent_name}")
                return True

        return False

    def build_graph(self) -> BaseGraph:
        """Build dynamic supervisor graph with enhanced routing."""
        graph = BaseGraph(self.state_schema)

        # Add supervisor decision node
        supervisor_node = self._create_enhanced_supervisor_node()
        graph.add_node("supervisor", supervisor_node)
        graph.add_edge(START, "supervisor")

        # Add routing/coordination node
        coordinator_node = self._create_coordinator_node()
        graph.add_node("coordinator", coordinator_node)
        graph.add_edge("supervisor", "coordinator")

        # Add response adapter node
        adapter_node = self._create_response_adapter_node()
        graph.add_node("adapter", adapter_node)

        # Add registered agents as nodes
        self._add_agent_nodes(graph)

        # Set up conditional routing
        self._setup_conditional_routing(graph)

        self._graph_built = True
        logger.info("Dynamic supervisor graph built successfully")

        return graph

    async def _rebuild_graph(self) -> None:
        """Rebuild the supervisor graph with current agents."""
        logger.info("Rebuilding supervisor graph...")

        # Build new graph with current agents
        new_graph = self.build_graph()

        # Update the agent's graph reference
        self.graph = new_graph

        # Recompile the graph - this is crucial!
        if hasattr(self, "_compiled_graph"):
            self._compiled_graph = new_graph.compile()

        # Update internal tracking
        self._graph_built = True
        self.agent_registry.mark_rebuilt()

        logger.info(
            f"Supervisor graph rebuilt with {len(self.agent_registry.get_available_agents())} agents"
        )

        # Log new routing destinations for debugging
        available_agents = self.agent_registry.get_available_agents()
        logger.debug(f"New routing destinations: {[*available_agents, '__end__']}")

    def _create_enhanced_supervisor_node(self) -> Callable:
        """Create enhanced supervisor node with reasoning and context."""

        async def supervisor_node(state: DynamicSupervisorState, config=None) -> dict:
            """Enhanced supervisor node with decision reasoning."""
            # Update performance monitoring
            self._performance_monitor.start_decision()

            try:
                # Analyze input and context
                input_analysis = await self._analyze_input(state)

                # Get available agents with performance data
                available_agents = self._get_available_agents_with_context(state)

                # Get aggregated tool information
                tool_info = self._aggregate_agent_tools()

                # Create enhanced prompt with reasoning including tool capabilities
                prompt = self._create_enhanced_decision_prompt(
                    state, input_analysis, available_agents, tool_info
                )

                # Get LLM decision with reasoning
                if self.main_engine:
                    response = await self.main_engine.ainvoke(prompt, config)
                    decision_data = self._parse_decision_response(
                        response, available_agents
                    )
                else:
                    decision_data = {
                        "target": "END",
                        "reasoning": "No engine available",
                    }

                # Create decision record
                decision = SupervisorDecision(
                    target_agent=decision_data["target"],
                    reasoning=decision_data["reasoning"],
                    confidence=decision_data.get("confidence", 0.5),
                    available_agents=list(available_agents.keys()),
                    input_analysis=input_analysis,
                    alternatives=decision_data.get("alternatives", []),
                )

                # Update state
                updates = {
                    "current_decision": decision,
                    "routing_decisions": [*state.routing_decisions, decision],
                }

                # Update registered agents in state
                agent_configs = {}
                for agent_name in self.agent_registry.get_available_agents():
                    config = state.get_agent_config(agent_name)
                    if config:
                        agent_configs[agent_name] = config

                updates["registered_agents"] = agent_configs

                self._performance_monitor.end_decision(decision.target_agent)

                return updates

            except Exception as e:
                logger.exception(f"Supervisor decision failed: {e}")
                self._performance_monitor.end_decision("ERROR")

                error_decision = SupervisorDecision(
                    target_agent="END",
                    reasoning=f"Error in decision making: {e!s}",
                    confidence=0.0,
                )

                return {
                    "current_decision": error_decision,
                    "routing_decisions": [*state.routing_decisions, error_decision],
                }

        return supervisor_node

    def _create_coordinator_node(self) -> Callable:
        """Create coordination node for managing execution flow."""

        async def coordinator_node(state: DynamicSupervisorState, config=None) -> dict:
            """Coordinate agent execution based on decision."""
            if not state.current_decision:
                return {"conversation_complete": True}

            target_agent = state.current_decision.target_agent

            if target_agent == "END" or not target_agent:
                return {"conversation_complete": True}

            # Prepare execution context
            execution_id = str(uuid4())
            start_time = time.time()

            # Create execution result placeholder
            execution_result = AgentExecutionResult(
                execution_id=execution_id,
                agent_name=target_agent,
                success=False,
                start_time=start_time,
            )

            return {
                "current_execution": execution_result,
                "execution_queue": (
                    [target_agent]
                    if not self.enable_parallel_execution
                    else [*state.execution_queue, target_agent]
                ),
            }

        return coordinator_node

    def _create_response_adapter_node(self) -> Callable:
        """Create response adaptation node."""

        async def adapter_node(state: DynamicSupervisorState, config=None) -> dict:
            """Adapt agent responses based on configuration."""
            if not state.current_execution or not state.current_execution.success:
                return {}

            agent_name = state.current_execution.agent_name
            adapted_messages = state.adapt_response_for_agent(
                agent_name, state.current_execution.messages
            )

            # Update execution result with adapted response
            if adapted_messages != state.current_execution.messages:
                state.current_execution.messages = adapted_messages
                logger.info(f"Adapted response for agent {agent_name}")

            return {}

        return adapter_node

    def _add_agent_nodes(self, graph: BaseGraph) -> None:
        """Add registered agents as graph nodes."""
        for agent_name in self.agent_registry.get_available_agents():
            agent_wrapper = self._create_enhanced_agent_wrapper(agent_name)
            graph.add_node(agent_name, agent_wrapper)

            # Connect agent to adapter
            graph.add_edge(agent_name, "adapter")
            # Connect adapter back to supervisor
            graph.add_edge("adapter", "supervisor")

    def _setup_conditional_routing(self, graph: BaseGraph) -> None:
        """Setup conditional routing from coordinator."""
        # Get current available agents for destinations
        available_agents = self.agent_registry.get_available_agents()
        routing_destinations = [*available_agents, "__end__"]

        def routing_condition(state: DynamicSupervisorState) -> str:
            """Determine routing destination dynamically."""
            if state.conversation_complete:
                return "__end__"

            if state.current_decision and state.current_decision.target_agent:
                target = state.current_decision.target_agent
                if target == "END":
                    return "__end__"
                # ✅ Check against CURRENT registry state, not static list
                if self.agent_registry.is_agent_registered(target):
                    return target

            return "__end__"

        graph.add_conditional_edges(
            "coordinator", routing_condition, routing_destinations
        )

    def _create_enhanced_agent_wrapper(self, agent_name: str) -> Callable:
        """Create enhanced agent wrapper with performance tracking."""

        async def agent_wrapper(state: DynamicSupervisorState, config=None) -> dict:
            """Execute agent with enhanced tracking and error handling."""
            async with self._execution_lock:
                agent = self.agent_registry.get_agent(agent_name)
                if not agent:
                    error_result = AgentExecutionResult(
                        agent_name=agent_name,
                        success=False,
                        error=f"Agent {agent_name} not found",
                    )
                    return {"current_execution": error_result}

                # Get agent configuration
                agent_config = state.get_agent_config(agent_name)
                execution_timeout = (
                    agent_config.execution_timeout if agent_config else 300.0
                )

                try:
                    # Start execution tracking
                    start_time = time.time()

                    # Prepare agent state
                    agent_state = self._prepare_enhanced_agent_state(state, agent)

                    # Execute with timeout
                    result = await asyncio.wait_for(
                        agent.ainvoke(agent_state, config), timeout=execution_timeout
                    )

                    end_time = time.time()
                    duration = end_time - start_time

                    # Extract messages and metadata
                    result_messages = getattr(result, "messages", [])
                    if isinstance(result, dict):
                        result_messages = result.get("messages", [])

                    # Create successful execution result
                    execution_result = AgentExecutionResult(
                        agent_name=agent_name,
                        success=True,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        messages=result_messages,
                        output=result,
                    )

                    # Track tool calls if available
                    if hasattr(result, "tool_calls"):
                        execution_result.tool_calls = result.tool_calls

                    # Update state and reset retry count
                    state.add_execution_result(execution_result)
                    state.reset_retry_count(agent_name)

                    return {
                        "current_execution": execution_result,
                        "messages": state.messages + result_messages,
                        "agent_execution_history": state.agent_execution_history,
                    }

                except TimeoutError:
                    error_result = AgentExecutionResult(
                        agent_name=agent_name,
                        success=False,
                        start_time=start_time,
                        end_time=time.time(),
                        error=f"Agent execution timed out after {execution_timeout}s",
                    )

                    state.add_execution_result(error_result)
                    state.increment_retry_count(agent_name)

                    return {"current_execution": error_result}

                except Exception as e:
                    error_result = AgentExecutionResult(
                        agent_name=agent_name,
                        success=False,
                        start_time=start_time,
                        end_time=time.time(),
                        error=str(e),
                    )

                    state.add_execution_result(error_result)
                    state.increment_retry_count(agent_name)

                    logger.exception(f"Agent {agent_name} execution failed: {e}")
                    return {"current_execution": error_result}

        return agent_wrapper

    async def _analyze_input(self, state: DynamicSupervisorState) -> dict[str, Any]:
        """Analyze input messages for context and requirements."""
        if not state.messages:
            return {"type": "empty", "complexity": "simple"}

        last_message = state.messages[-1]
        content = getattr(last_message, "content", "")

        # Simple analysis - could be enhanced with NLP
        analysis = {
            "type": "user_query",
            "complexity": "simple",
            "keywords": [],
            "length": len(content),
            "question_type": "general",
        }

        # Detect complexity indicators
        complexity_indicators = [
            "analyze",
            "research",
            "compare",
            "multiple",
            "complex",
            "detailed",
        ]
        if any(indicator in content.lower() for indicator in complexity_indicators):
            analysis["complexity"] = "complex"

        # Extract keywords (basic implementation)
        words = content.lower().split()
        analysis["keywords"] = [word for word in words if len(word) > 3][:10]

        return analysis

    def _get_available_agents_with_context(
        self, state: DynamicSupervisorState
    ) -> dict[str, dict[str, Any]]:
        """Get available agents with performance context."""
        agents_context = {}

        for agent_name in self.agent_registry.get_available_agents():
            agent_config = state.get_agent_config(agent_name)
            performance = state.get_agent_performance(agent_name)

            agents_context[agent_name] = {
                "capability": self.agent_registry.get_agent_capability(agent_name),
                "performance": performance,
                "priority": agent_config.priority if agent_config else 1,
                "available": not (
                    agent_config
                    and agent_config.retry_count >= agent_config.max_retries
                ),
            }

        return agents_context

    def _create_enhanced_decision_prompt(
        self,
        state: DynamicSupervisorState,
        input_analysis: dict[str, Any],
        available_agents: dict[str, dict[str, Any]],
        tool_info: dict[str, Any] | None = None,
    ) -> ChatPromptTemplate:
        """Create enhanced prompt with reasoning and context."""
        # Build agent descriptions with performance data and tool information
        agent_descriptions = []
        for agent_name, context in available_agents.items():
            capability = context["capability"]
            performance = context["performance"]
            priority = context["priority"]
            available = context["available"]

            status = "✅ Available" if available else "❌ Unavailable"
            success_rate = performance.get("success_rate", 0.0) * 100

            # Add tool information for this agent
            agent_tools = []
            if tool_info and "tool_to_agent" in tool_info:
                agent_tools = [
                    tool_name
                    for tool_name, owner in tool_info["tool_to_agent"].items()
                    if owner == agent_name
                ]

            tools_text = (
                f"Tools: {', '.join(agent_tools)}" if agent_tools else "No tools"
            )

            description = f"""- {agent_name} (Priority: {priority}, {status})
  Capability: {capability}
  {tools_text}
  Performance: {success_rate:.1f}% success rate, {performance.get('executions', 0)} executions"""

            agent_descriptions.append(description)

        agents_text = (
            "\n".join(agent_descriptions)
            if agent_descriptions
            else "No agents available"
        )

        # Add overall tool summary
        tool_summary = ""
        if tool_info and tool_info.get("tools"):
            total_tools = len(tool_info["tools"])
            tool_summary = (
                f"\n\nAVAILABLE TOOLS ACROSS ALL AGENTS: {total_tools} tools total\n"
            )
            for tool_name, agent_name in tool_info.get("tool_to_agent", {}).items():
                tool_summary += f"- {tool_name} (via {agent_name})\n"

        # Include recent context
        recent_decisions = state.get_recent_decisions(3)
        context_text = ""
        if recent_decisions:
            context_text = "\n\nRecent decisions:\n"
            for decision in recent_decisions:
                context_text += f"- {decision.target_agent}: {decision.reasoning}\n"

        system_prompt = f"""You are an intelligent supervisor managing a dynamic team of AI agents.
Your task is to analyze the user's request and select the most appropriate agent or end the conversation.

INPUT ANALYSIS:
- Type: {input_analysis.get('type', 'unknown')}
- Complexity: {input_analysis.get('complexity', 'simple')}
- Keywords: {', '.join(input_analysis.get('keywords', [])[:5])}

AVAILABLE AGENTS:
{agents_text}
- END: Use this when the conversation should end or task is complete
{tool_summary}

INSTRUCTIONS:
1. Analyze the user's request in context of agent capabilities and performance
2. Consider recent conversation flow and agent performance
3. Provide your reasoning for the choice
4. Select the best agent or END

RESPONSE FORMAT:
Provide a JSON response with:
{{
  "target": "agent_name_or_END",
  "reasoning": "Detailed explanation of your choice",
  "confidence": 0.0-1.0,
  "alternatives": [
    {{"agent": "alternative_name", "score": 0.0-1.0}}
  ]
}}

{context_text}"""

        return ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("placeholder", "{messages}")]
        )

    def _parse_decision_response(
        self, response: Any, available_agents: dict[str, Any]
    ) -> dict[str, Any]:
        """Parse LLM decision response."""
        content = getattr(response, "content", str(response))

        try:
            import json

            # Try to parse as JSON first
            if "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_content = content[json_start:json_end]
                data = json.loads(json_content)

                # Validate target
                target = data.get("target", "END")
                if target not in available_agents and target != "END":
                    target = "END"

                return {
                    "target": target,
                    "reasoning": data.get("reasoning", "Decision made"),
                    "confidence": float(data.get("confidence", 0.5)),
                    "alternatives": data.get("alternatives", []),
                }
        except Exception as e:
            logger.warning(f"Failed to parse JSON decision: {e}")

        # Fallback to simple parsing
        content_upper = content.upper()
        for agent_name in available_agents:
            if agent_name.upper() in content_upper:
                return {
                    "target": agent_name,
                    "reasoning": f"Selected {agent_name} based on content match",
                    "confidence": 0.7,
                }

        return {
            "target": "END",
            "reasoning": "No clear agent match found",
            "confidence": 0.3,
        }

    def _prepare_enhanced_agent_state(
        self, supervisor_state: DynamicSupervisorState, agent: Agent
    ) -> Any:
        """Prepare enhanced state for agent execution."""
        # Try to use agent's specific state schema
        if hasattr(agent, "state_schema") and agent.state_schema:
            try:
                # Create state with relevant fields
                state_data = {"messages": supervisor_state.messages}

                # Add additional fields if they exist in target schema
                schema_fields = agent.state_schema.model_fields
                for field_name in schema_fields:
                    if (
                        hasattr(supervisor_state, field_name)
                        and field_name != "messages"
                    ):
                        state_data[field_name] = getattr(supervisor_state, field_name)

                return agent.state_schema(**state_data)

            except Exception as e:
                logger.warning(f"Could not create specific state for {agent.name}: {e}")

        # Fallback to basic state
        return type("State", (), {"messages": supervisor_state.messages})()

    def get_performance_summary(self) -> dict[str, Any]:
        """Get comprehensive performance summary."""
        if not hasattr(self, "_state") or not self._state:
            return {"error": "No state available"}

        state = self._state

        summary = {
            "session_stats": state.session_stats.copy(),
            "registered_agents": len(state.registered_agents),
            "total_executions": len(state.agent_execution_history),
            "success_rate": state.success_rate,
            "most_used_agent": state.most_used_agent,
            "agent_performance": {},
        }

        # Add per-agent performance
        for agent_name in state.get_available_agents():
            summary["agent_performance"][agent_name] = state.get_agent_performance(
                agent_name
            )

        return summary

    def print_supervisor_dashboard(self) -> None:
        """Print comprehensive supervisor dashboard."""
        if not hasattr(self, "_state") or not self._state:
            console.print("[red]No state available[/red]")
            return

        state = self._state

        # Main status table
        table = Table(title="🚀 Dynamic Supervisor Dashboard")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Supervisor Name", self.name)
        table.add_row("Registered Agents", str(len(state.registered_agents)))
        table.add_row("Total Executions", str(len(state.agent_execution_history)))
        table.add_row("Success Rate", f"{state.success_rate:.1%}")
        table.add_row("Most Used Agent", state.most_used_agent or "None")
        table.add_row("Auto Rebuild", str(self.auto_rebuild_graph))
        table.add_row("Parallel Execution", str(self.enable_parallel_execution))

        console.print(table)

        # Agent performance table
        if state.registered_agents:
            perf_table = Table(title="📊 Agent Performance")
            perf_table.add_column("Agent", style="cyan")
            perf_table.add_column("Executions", style="yellow")
            perf_table.add_column("Success Rate", style="green")
            perf_table.add_column("Avg Duration", style="blue")
            perf_table.add_column("Priority", style="magenta")

            for agent_name in state.get_available_agents():
                performance = state.get_agent_performance(agent_name)
                config = state.get_agent_config(agent_name)

                perf_table.add_row(
                    agent_name,
                    str(performance["executions"]),
                    f"{performance['success_rate']:.1%}",
                    f"{performance['average_duration']:.2f}s",
                    str(config.priority if config else 1),
                )

            console.print(perf_table)

        # Recent decisions
        recent_decisions = state.get_recent_decisions(5)
        if recent_decisions:
            decisions_table = Table(title="🎯 Recent Decisions")
            decisions_table.add_column("Target", style="cyan")
            decisions_table.add_column("Reasoning", style="green")
            decisions_table.add_column("Confidence", style="yellow")
            decisions_table.add_column("Time", style="blue")

            for decision in recent_decisions:
                decisions_table.add_row(
                    decision.target_agent or "END",
                    (
                        decision.reasoning[:50] + "..."
                        if len(decision.reasoning) > 50
                        else decision.reasoning
                    ),
                    f"{decision.confidence:.1%}",
                    time.strftime("%H:%M:%S", time.localtime(decision.timestamp)),
                )

            console.print(decisions_table)


class PerformanceMonitor:
    """Simple performance monitoring for supervisor operations."""

    def __init__(self):
        self.decision_start_time = None
        self.decision_count = 0
        self.total_decision_time = 0.0

    def start_decision(self):
        self.decision_start_time = time.time()

    def end_decision(self, target: str):
        if self.decision_start_time:
            duration = time.time() - self.decision_start_time
            self.total_decision_time += duration
            self.decision_count += 1
            logger.debug(f"Decision to {target} took {duration:.3f}s")

    def get_average_decision_time(self) -> float:
        return (
            self.total_decision_time / self.decision_count
            if self.decision_count > 0
            else 0.0
        )
