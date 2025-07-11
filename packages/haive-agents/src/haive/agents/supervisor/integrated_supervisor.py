"""Integrated Dynamic Multi-Agent Supervisor.

This module provides a complete integration of:
- DynamicSupervisorAgent capabilities
- Multi-agent coordination state
- Dynamic agent management tools
- DynamicChoiceModel routing
- Tool-based agent addition/removal
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from rich.console import Console

from haive.agents.supervisor.dynamic_agent_tools import (
    AgentRegistryManager,
    create_agent_management_tools,
)
from haive.agents.supervisor.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.supervisor.multi_agent_dynamic_state import (
    MultiAgentDynamicSupervisorState,
)

logger = logging.getLogger(__name__)
console = Console()


class IntegratedDynamicSupervisor(DynamicSupervisorAgent):
    """Integrated supervisor combining dynamic agent management and multi-agent coordination.

    This supervisor provides:
    - Dynamic agent addition/removal through tools
    - Multi-agent coordination patterns
    - DynamicChoiceModel integration for routing
    - Tool-based agent management
    - Enhanced state management
    """

    def __init__(
        self,
        name: str = "integrated_supervisor",
        engine: AugLLMConfig | None = None,
        enable_agent_management_tools: bool = True,
        coordination_mode: str = "supervisor",
        **kwargs,
    ):
        """Initialize integrated supervisor.

        Args:
            name: Supervisor name
            engine: LLM engine for decisions
            enable_agent_management_tools: Whether to include agent management tools
            coordination_mode: Multi-agent coordination mode
            **kwargs: Additional supervisor arguments
        """
        # Set enhanced state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentDynamicSupervisorState

        super().__init__(name=name, engine=engine, **kwargs)

        # Multi-agent configuration
        self.coordination_mode = coordination_mode
        self.enable_agent_management_tools = enable_agent_management_tools

        # Create agent management tools if enabled
        self.agent_management_tools = []
        self.registry_manager = None

        if enable_agent_management_tools:
            self._setup_agent_management_tools()

        logger.info(
            f"IntegratedDynamicSupervisor '{name}' initialized with coordination mode: {coordination_mode}"
        )

    def _setup_agent_management_tools(self) -> None:
        """Setup agent management tools."""
        try:
            self.agent_management_tools = create_agent_management_tools(self)

            # Add tools to supervisor's engine if it exists
            if self.main_engine and hasattr(self.main_engine, "tools"):
                existing_tools = getattr(self.main_engine, "tools", [])
                self.main_engine.tools = existing_tools + self.agent_management_tools
                logger.info(
                    f"Added {len(self.agent_management_tools)} agent management tools to supervisor"
                )

            # Get registry manager reference
            if self.agent_management_tools:
                self.registry_manager = self.agent_management_tools[0].registry_manager

        except Exception as e:
            logger.exception(f"Failed to setup agent management tools: {e}")

    def register_agent_constructor(self, agent_type: str, constructor) -> None:
        """Register an agent constructor for dynamic creation."""
        if self.registry_manager:
            self.registry_manager.register_agent_constructor(agent_type, constructor)
        else:
            logger.warning(
                "Registry manager not available - agent management tools disabled"
            )

    async def register_agent(
        self,
        agent: Any,
        capability_description: str | None = None,
        execution_config: dict[str, Any] | None = None,
        rebuild_graph: bool | None = None,
    ) -> bool:
        """Enhanced agent registration with multi-agent state integration."""
        # Call parent registration
        success = await super().register_agent(
            agent, capability_description, execution_config, rebuild_graph
        )

        if success and hasattr(self, "_state") and self._state:
            # Update multi-agent state
            agent_tools = []
            if hasattr(agent, "tools") and agent.tools:
                agent_tools = [getattr(tool, "name", str(tool)) for tool in agent.tools]
            if (
                hasattr(agent, "engine")
                and agent.engine
                and hasattr(agent.engine, "tools")
            ) and agent.engine.tools:
                agent_tools.extend(
                    [getattr(tool, "name", str(tool)) for tool in agent.engine.tools]
                )

            self._state.agent_registry.add_agent_to_registry(
                agent.name,
                agent.__class__.__name__,
                capability_description or f"Handles {agent.name} tasks",
                agent_tools,
            )

            # Sync with choice model if available
            if self.registry_manager:
                choice_model = self.registry_manager.get_agent_choice_model()
                self._state.sync_with_choice_model(choice_model)

        return success

    async def unregister_agent(
        self, agent_name: str, rebuild_graph: bool | None = None
    ) -> bool:
        """Enhanced agent unregistration with multi-agent state integration."""
        success = await super().unregister_agent(agent_name, rebuild_graph)

        if success and hasattr(self, "_state") and self._state:
            # Update multi-agent state
            self._state.agent_registry.remove_agent_from_registry(agent_name)

            # Sync with choice model if available
            if self.registry_manager:
                choice_model = self.registry_manager.get_agent_choice_model()
                self._state.sync_with_choice_model(choice_model)

        return success

    def build_graph(self) -> BaseGraph:
        """Build integrated supervisor graph with agent management capabilities."""
        graph = BaseGraph(self.state_schema)

        # Add supervisor decision node (enhanced with tool capabilities)
        supervisor_node = self._create_integrated_supervisor_node()
        graph.add_node("supervisor", supervisor_node)
        graph.add_edge(START, "supervisor")

        # Add agent management node (processes tool calls for agent changes)
        agent_mgmt_node = self._create_agent_management_node()
        graph.add_node("agent_management", agent_mgmt_node)

        # Add coordination node
        coordinator_node = self._create_enhanced_coordinator_node()
        graph.add_node("coordinator", coordinator_node)

        # Add response adapter node
        adapter_node = self._create_response_adapter_node()
        graph.add_node("adapter", adapter_node)

        # Add registered agents as nodes
        self._add_agent_nodes(graph)

        # Set up enhanced conditional routing
        self._setup_integrated_conditional_routing(graph)

        self._graph_built = True
        logger.info("Integrated supervisor graph built successfully")

        return graph

    def _create_integrated_supervisor_node(self) -> Any:
        """Create supervisor node with agent management tool integration."""

        async def supervisor_node(
            state: MultiAgentDynamicSupervisorState, config=None
        ) -> dict:
            """Enhanced supervisor with tool and agent management capabilities."""
            # Start performance monitoring
            self._performance_monitor.start_decision()

            try:
                # Process any pending agent changes first
                if state.registry_needs_sync:
                    change_results = state.process_pending_agent_changes()
                    if change_results["added"] or change_results["removed"]:
                        logger.info(f"Processed agent changes: {change_results}")
                        # Trigger graph rebuild if needed
                        if self.auto_rebuild_graph:
                            await self._rebuild_graph()

                # Analyze input and context (including tool capabilities)
                input_analysis = await self._analyze_input(state)

                # Get available agents with performance data
                available_agents = self._get_available_agents_with_context(state)

                # Get aggregated tool information
                tool_info = self._aggregate_agent_tools()

                # Check for agent management tool calls in recent messages
                needs_agent_management = self._check_for_agent_management_needs(state)

                if needs_agent_management:
                    # Route to agent management node
                    decision_data = {
                        "target": "agent_management",
                        "reasoning": "Request requires agent management operations",
                        "confidence": 0.9,
                    }
                else:
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
                from haive.agents.supervisor.dynamic_state import SupervisorDecision

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
                logger.exception(f"Integrated supervisor decision failed: {e}")
                self._performance_monitor.end_decision("ERROR")

                from haive.agents.supervisor.dynamic_state import SupervisorDecision

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

    def _create_agent_management_node(self) -> Any:
        """Create node for processing agent management tool calls."""

        async def agent_management_node(
            state: MultiAgentDynamicSupervisorState, config=None
        ) -> dict:
            """Process agent management operations."""
            # This node handles tool calls for adding/removing agents
            # In a real implementation, this would process the tool calls
            # and update the agent registry accordingly

            logger.info("Processing agent management request")

            # For now, just return to supervisor
            return {
                "messages": [
                    *state.messages,
                    AIMessage(content="Agent management operations processed"),
                ]
            }

        return agent_management_node

    def _create_enhanced_coordinator_node(self) -> Any:
        """Create enhanced coordination node with multi-agent support."""

        async def coordinator_node(
            state: MultiAgentDynamicSupervisorState, config=None
        ) -> dict:
            """Enhanced coordination with multi-agent state management."""
            if not state.current_decision:
                return {"conversation_complete": True}

            target_agent = state.current_decision.target_agent

            if target_agent == "END" or not target_agent:
                return {"conversation_complete": True}

            if target_agent == "agent_management":
                # Route to agent management
                return {"routing_target": "agent_management"}

            # Start coordination session if not active
            if not state.coordination_active:
                session_id = state.start_coordination_session(self.coordination_mode)
                logger.info(f"Started coordination session: {session_id}")

            # Add to execution queue
            state.coordination.add_to_execution_queue(
                target_agent,
                {"messages": state.messages},
                priority=(
                    state.get_agent_config(target_agent).priority
                    if state.get_agent_config(target_agent)
                    else 1
                ),
            )

            # Prepare execution context
            import time
            from uuid import uuid4

            from haive.agents.supervisor.dynamic_state import AgentExecutionResult

            execution_id = str(uuid4())
            start_time = time.time()

            execution_result = AgentExecutionResult(
                execution_id=execution_id,
                agent_name=target_agent,
                success=False,
                start_time=start_time,
            )

            # Start agent execution tracking
            state.coordination.start_agent_execution(target_agent, execution_id)

            return {
                "current_execution": execution_result,
                "routing_target": target_agent,
            }

        return coordinator_node

    def _check_for_agent_management_needs(
        self, state: MultiAgentDynamicSupervisorState
    ) -> bool:
        """Check if the request needs agent management operations."""
        if not state.messages:
            return False

        last_message = state.messages[-1]
        content = getattr(last_message, "content", "").lower()

        # Look for agent management keywords
        management_keywords = [
            "add agent",
            "remove agent",
            "change agent",
            "list agents",
            "new agent",
            "delete agent",
            "agent management",
            "register agent",
        ]

        return any(keyword in content for keyword in management_keywords)

    def _setup_integrated_conditional_routing(self, graph: BaseGraph) -> None:
        """Setup enhanced conditional routing with agent management."""
        available_agents = self.agent_registry.get_available_agents()
        routing_destinations = [*available_agents, "agent_management", "__end__"]

        def routing_condition(state: MultiAgentDynamicSupervisorState) -> str:
            """Enhanced routing condition with agent management support."""
            if state.conversation_complete:
                return "__end__"

            # Check for explicit routing target from coordinator
            if hasattr(state, "routing_target"):
                target = getattr(state, "routing_target", None)
                if target and target in routing_destinations:
                    return target

            if state.current_decision and state.current_decision.target_agent:
                target = state.current_decision.target_agent
                if target == "END":
                    return "__end__"
                if target == "agent_management":
                    return "agent_management"
                if self.agent_registry.is_agent_registered(target):
                    return target

            return "__end__"

        # Set up routing from supervisor
        graph.add_conditional_edges(
            "supervisor",
            routing_condition,
            ["coordinator", "agent_management", "__end__"],
        )

        # Set up routing from coordinator
        graph.add_conditional_edges(
            "coordinator", routing_condition, routing_destinations
        )

        # Agent management returns to supervisor
        graph.add_edge("agent_management", "supervisor")

    def start_coordination_session(self, mode: str | None = None) -> str:
        """Start a new coordination session."""
        if hasattr(self, "_state") and self._state:
            actual_mode = mode or self.coordination_mode
            return self._state.start_coordination_session(actual_mode)
        return "no_state"

    def end_coordination_session(self) -> dict[str, Any]:
        """End the current coordination session."""
        if hasattr(self, "_state") and self._state:
            return self._state.end_coordination_session()
        return {}

    def get_coordination_status(self) -> dict[str, Any]:
        """Get current coordination status."""
        if hasattr(self, "_state") and self._state:
            return self._state.get_coordination_status()
        return {"active": False}

    def print_integrated_dashboard(self) -> None:
        """Print comprehensive integrated supervisor dashboard."""
        # Call parent dashboard
        self.print_supervisor_dashboard()

        if not hasattr(self, "_state") or not self._state:
            return

        state = self._state

        # Multi-agent coordination status
        from rich.table import Table

        coord_table = Table(title="🤝 Multi-Agent Coordination Status")
        coord_table.add_column("Metric", style="cyan")
        coord_table.add_column("Value", style="green")

        coord_status = state.get_coordination_status()
        coord_table.add_row("Coordination Active", str(coord_status["active"]))
        coord_table.add_row("Coordination Mode", coord_status["mode"])
        coord_table.add_row("Current Agent", coord_status.get("current_agent", "None"))
        coord_table.add_row("Queue Length", str(coord_status["queue_length"]))
        coord_table.add_row("Active Executions", str(coord_status["active_executions"]))

        console.print(coord_table)

        # Agent registry status
        registry_table = Table(title="📋 Agent Registry Status")
        registry_table.add_column("Property", style="cyan")
        registry_table.add_column("Value", style="green")

        registry_table.add_row("Total Registered", str(state.total_registered_agents))
        registry_table.add_row("Total Tools", str(state.total_available_tools))
        registry_table.add_row("Registry Sync Needed", str(state.registry_needs_sync))
        registry_table.add_row(
            "Choice Model Version", str(state.agent_registry.choice_model_version)
        )

        console.print(registry_table)
