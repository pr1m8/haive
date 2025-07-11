"""Dynamic Multi-Agent Supervisor with Dynamic Execution Pattern.

This implementation integrates with the MultiAgent base class and uses
dynamic agent execution without graph rebuilding.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from pydantic import Field, PrivateAttr

from haive.agents.base.agent import Agent
from haive.agents.multi.agent import MultiAgent

logger = logging.getLogger(__name__)


class DynamicMultiAgent(MultiAgent):
    """Multi-agent system with dynamic agent execution capabilities.

    This extends MultiAgent to support:
    - Dynamic agent registration/unregistration at runtime
    - No graph rebuilding - uses executor pattern
    - Proper state extraction per agent schema
    - Agent capability-based routing
    - Performance tracking and selection
    """

    # Configuration
    coordination_mode: Literal["dynamic"] = Field(
        default="dynamic", description="Use dynamic coordination mode"
    )

    enable_capability_routing: bool = Field(
        default=True, description="Enable capability-based agent selection"
    )

    track_performance: bool = Field(
        default=True, description="Track agent performance metrics"
    )

    # Private attributes for dynamic management
    _capability_registry: dict[str, str] = PrivateAttr(default_factory=dict)
    _performance_metrics: dict[str, dict[str, Any]] = PrivateAttr(default_factory=dict)
    _execution_history: list[dict[str, Any]] = PrivateAttr(default_factory=list)

    def setup_agent(self) -> None:
        """Set up the dynamic multi-agent system."""
        # Initialize registries
        self._capability_registry = {}
        self._performance_metrics = {}
        self._execution_history = []

        # Call parent setup
        super().setup_agent()

        # Register initial agents with capabilities
        for agent_name, agent in self.agents.items():
            self._register_agent_capability(agent_name, agent)

    def _register_agent_capability(self, agent_name: str, agent: Agent) -> None:
        """Register agent capabilities for routing."""
        # Extract capability from agent
        capability = getattr(agent, "capability", None)
        if not capability:
            # Try to infer from agent type/name
            if "research" in agent_name.lower():
                capability = "research, information gathering, fact-finding"
            elif "write" in agent_name.lower() or "writing" in agent_name.lower():
                capability = "writing, content creation, documentation"
            elif "code" in agent_name.lower() or "coding" in agent_name.lower():
                capability = "coding, programming, software development"
            elif "analyze" in agent_name.lower() or "analysis" in agent_name.lower():
                capability = "analysis, data processing, insights"
            else:
                capability = f"general tasks for {agent_name}"

        self._capability_registry[agent_name] = capability

        # Initialize performance metrics
        self._performance_metrics[agent_name] = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0,
            "last_execution": None,
            "capability_score": 1.0,  # Start with neutral score
        }

        logger.info(f"Registered capability for {agent_name}: {capability}")

    def register_agent_dynamically(
        self, agent: Agent, capability: str | None = None, agent_name: str | None = None
    ) -> bool:
        """Register a new agent dynamically at runtime.

        Args:
            agent: The agent to register
            capability: Description of agent capabilities
            agent_name: Optional name override

        Returns:
            Success status
        """
        name = agent_name or getattr(agent, "name", agent.__class__.__name__)

        logger.info(f"Dynamically registering agent: {name}")

        # Add to agents dict
        self.agents[name] = agent

        # Register capability
        if capability:
            self._capability_registry[name] = capability
        else:
            self._register_agent_capability(name, agent)

        # Update agent order
        if hasattr(self, "_agent_order") and name not in self._agent_order:
            self._agent_order.append(name)

        logger.info(
            f"✅ Dynamically registered {name} (total agents: {len(self.agents)})"
        )
        return True

    def unregister_agent_dynamically(self, agent_name: str) -> bool:
        """Unregister an agent dynamically.

        Args:
            agent_name: Name of agent to remove

        Returns:
            Success status
        """
        if agent_name not in self.agents:
            return False

        logger.info(f"Dynamically unregistering agent: {agent_name}")

        # Remove from agents
        del self.agents[agent_name]

        # Remove from registries
        if agent_name in self._capability_registry:
            del self._capability_registry[agent_name]

        if agent_name in self._performance_metrics:
            del self._performance_metrics[agent_name]

        # Update agent order
        if hasattr(self, "_agent_order") and agent_name in self._agent_order:
            self._agent_order.remove(agent_name)

        logger.info(
            f"✅ Unregistered {agent_name} (remaining agents: {len(self.agents)})"
        )
        return True

    def build_graph(self) -> BaseGraph:
        """Build dynamic multi-agent graph with executor pattern."""
        logger.info(
            f"Building dynamic multi-agent graph with {len(self.agents)} agents"
        )

        # Create the graph
        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor node
        supervisor_node = self._create_dynamic_supervisor_node()
        graph.add_node("supervisor", supervisor_node)

        # Add dynamic executor node
        executor_node = self._create_dynamic_executor_node()
        graph.add_node("executor", executor_node)

        # Simple flow
        graph.set_entry_point("supervisor")

        # Supervisor routes to executor or END
        graph.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {"executor": "executor", "END": "__end__"},
        )

        # Executor always returns to supervisor
        graph.add_edge("executor", "supervisor")

        logger.info("✅ Built dynamic multi-agent graph")
        return graph

    def _create_dynamic_supervisor_node(self):
        """Create supervisor node for dynamic agent selection."""

        async def supervisor_node(state: Any) -> dict[str, Any]:
            """Select best agent for current task."""
            logger.info("=" * 60)
            logger.info("DYNAMIC SUPERVISOR NODE")
            logger.info("=" * 60)

            # Extract state
            state_dict = self._extract_state_dict(state)

            # Check completion conditions
            if state_dict.get("is_complete") or state_dict.get("error"):
                logger.info("Conversation complete or error occurred")
                return {"is_complete": True}

            # Get messages
            messages = state_dict.get("messages", [])
            if not messages:
                logger.info("No messages")
                return {"is_complete": True}

            # Check for AI loop
            last_message = messages[-1]
            if self._should_end_conversation(messages, state_dict):
                logger.info("Ending conversation to avoid loop")
                return {"is_complete": True}

            # Select best agent
            selected_agent = self._select_best_agent_for_task(last_message, state_dict)

            if selected_agent:
                logger.info(f"Selected agent: {selected_agent}")
                return {
                    "active_agent_id": selected_agent,
                    "target_agent": selected_agent,
                    "is_complete": False,
                }
            logger.info("No suitable agent found")
            return {"is_complete": True}

        return supervisor_node

    def _create_dynamic_executor_node(self):
        """Create executor node that dynamically runs selected agent."""

        async def executor_node(state: Any) -> dict[str, Any]:
            """Execute the selected agent with proper state handling."""
            logger.info("=" * 60)
            logger.info("DYNAMIC EXECUTOR NODE")
            logger.info("=" * 60)

            # Extract state
            state_dict = self._extract_state_dict(state)

            # Get target agent
            target_agent = state_dict.get("target_agent") or state_dict.get(
                "active_agent_id"
            )

            if not target_agent:
                logger.error("No target agent specified")
                return {"error": "No target agent specified"}

            logger.info(f"Executing agent: {target_agent}")

            # Get agent
            agent = self.agents.get(target_agent)
            if not agent:
                logger.error(f"Agent {target_agent} not found")
                return {"error": f"Agent {target_agent} not found"}

            # Track execution start
            start_time = datetime.now()

            try:
                # Prepare agent input following AgentNode pattern
                agent_input = self._prepare_agent_input(target_agent, agent, state_dict)

                # Execute agent
                if hasattr(agent, "ainvoke"):
                    result = await agent.ainvoke(agent_input)
                elif hasattr(agent, "invoke"):
                    result = agent.invoke(agent_input)
                else:
                    result = await agent(agent_input)

                # Process result
                update = self._process_agent_result(
                    target_agent, agent, result, state_dict
                )

                # Track performance
                if self.track_performance:
                    self._update_performance_metrics(
                        target_agent,
                        success=True,
                        execution_time=(datetime.now() - start_time).total_seconds(),
                    )

                # Add to execution history
                self._execution_history.append(
                    {
                        "agent": target_agent,
                        "timestamp": datetime.now(),
                        "success": True,
                        "execution_time": (datetime.now() - start_time).total_seconds(),
                    }
                )

                logger.info(f"✅ Agent {target_agent} executed successfully")
                return update

            except Exception as e:
                logger.exception(f"Error executing agent {target_agent}: {e}")

                # Track failure
                if self.track_performance:
                    self._update_performance_metrics(target_agent, success=False)

                return {
                    "error": str(e),
                    "last_agent": target_agent,
                    "is_complete": True,
                }

        return executor_node

    def _extract_state_dict(self, state: Any) -> dict[str, Any]:
        """Extract state dict with proper message handling."""
        if isinstance(state, dict):
            return state

        # Handle Pydantic model
        state_dict = state.model_dump()

        # Preserve BaseMessage objects
        if hasattr(state, "messages"):
            messages = getattr(state, "messages", [])
            if hasattr(messages, "root"):
                state_dict["messages"] = messages.root
            else:
                state_dict["messages"] = list(messages)

        return state_dict

    def _should_end_conversation(
        self, messages: list[BaseMessage], state: dict[str, Any]
    ) -> bool:
        """Check if we should end to avoid loops."""
        if not messages:
            return True

        last_message = messages[-1]

        # If last message is AI, check for human input after it
        if isinstance(last_message, AIMessage):
            # Find last human message
            human_messages = [
                (i, m) for i, m in enumerate(messages) if isinstance(m, HumanMessage)
            ]

            if human_messages:
                last_human_idx = human_messages[-1][0]
                # If AI already responded after last human message
                if last_human_idx < len(messages) - 1:
                    return True

        # Check if we've been through too many iterations
        completed = state.get("completed_agents", [])
        if len(completed) > len(self.agents) * 2:  # Prevent infinite loops
            return True

        return False

    def _select_best_agent_for_task(
        self, message: BaseMessage, state: dict[str, Any]
    ) -> str | None:
        """Select the best agent for the current task."""
        content = getattr(message, "content", str(message))

        if not self.agents:
            return None

        # Score each agent
        agent_scores = []

        for agent_name, _agent in self.agents.items():
            score = self._calculate_agent_score(agent_name, content, state)
            agent_scores.append((agent_name, score))
            logger.debug(f"Agent {agent_name} score: {score:.2f}")

        # Sort by score
        agent_scores.sort(key=lambda x: x[1], reverse=True)

        # Return highest scoring agent if above threshold
        if agent_scores and agent_scores[0][1] > 0.3:
            return agent_scores[0][0]

        # Default to first available agent
        return next(iter(self.agents.keys())) if self.agents else None

    def _calculate_agent_score(
        self, agent_name: str, content: str, state: dict[str, Any]
    ) -> float:
        """Calculate suitability score for an agent."""
        score = 0.0
        content_lower = content.lower()

        # Capability matching
        if self.enable_capability_routing:
            capability = self._capability_registry.get(agent_name, "").lower()

            # Direct capability word matches
            capability_words = capability.split()
            matches = sum(1 for word in capability_words if word in content_lower)
            score += min(0.5, matches * 0.1)

            # Semantic similarity (simple version)
            if any(word in content_lower for word in capability.split(",")):
                score += 0.3

        # Agent name matching
        if agent_name.lower() in content_lower:
            score += 0.4

        # Performance adjustment
        if self.track_performance:
            metrics = self._performance_metrics.get(agent_name, {})

            # Success rate
            total = metrics.get("total_executions", 0)
            if total > 0:
                success_rate = metrics.get("successful_executions", 0) / total
                score *= 0.5 + 0.5 * success_rate  # Adjust by 50-100%

            # Capability score from past performance
            score *= metrics.get("capability_score", 1.0)

        # Avoid recently used agents for variety
        last_agent = state.get("last_agent")
        if last_agent == agent_name:
            score *= 0.8  # Slight penalty for repetition

        return score

    def _prepare_agent_input(
        self, agent_name: str, agent: Agent, state: dict[str, Any]
    ) -> dict[str, Any]:
        """Prepare input for agent following AgentNode patterns."""
        # Use parent's extraction logic
        return self._extract_agent_input(agent_name, agent, state)

    def _process_agent_result(
        self, agent_name: str, agent: Agent, result: Any, state: dict[str, Any]
    ) -> dict[str, Any]:
        """Process agent result into state update."""
        # Use parent's output creation logic
        update = self._create_agent_output(agent_name, agent, result, state)

        # Add our tracking
        update["last_agent"] = agent_name

        # Update completed agents list
        completed = list(state.get("completed_agents", []))
        if agent_name not in completed:
            completed.append(agent_name)
        update["completed_agents"] = completed

        return update

    def _route_from_supervisor(self, state: Any) -> str:
        """Route from supervisor node."""
        state_dict = self._extract_state_dict(state)

        if state_dict.get("is_complete"):
            return "END"

        if state_dict.get("target_agent") or state_dict.get("active_agent_id"):
            return "executor"

        return "END"

    def _update_performance_metrics(
        self, agent_name: str, success: bool, execution_time: float | None = None
    ) -> None:
        """Update agent performance metrics."""
        if agent_name not in self._performance_metrics:
            return

        metrics = self._performance_metrics[agent_name]

        # Update counts
        metrics["total_executions"] += 1
        if success:
            metrics["successful_executions"] += 1
        else:
            metrics["failed_executions"] += 1

        # Update average execution time
        if success and execution_time:
            avg_time = metrics["average_execution_time"]
            total = metrics["successful_executions"]
            metrics["average_execution_time"] = (
                avg_time * (total - 1) + execution_time
            ) / total

        # Update last execution
        metrics["last_execution"] = datetime.now()

        # Adjust capability score based on performance
        success_rate = metrics["successful_executions"] / metrics["total_executions"]
        metrics["capability_score"] = 0.5 + 0.5 * success_rate

    def get_agent_performance(self, agent_name: str | None = None) -> dict[str, Any]:
        """Get performance metrics for agent(s)."""
        if agent_name:
            return self._performance_metrics.get(agent_name, {})
        return self._performance_metrics.copy()

    def get_execution_history(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Get execution history."""
        if limit:
            return self._execution_history[-limit:]
        return self._execution_history.copy()

    def get_agent_capabilities(self) -> dict[str, str]:
        """Get all agent capabilities."""
        return self._capability_registry.copy()


# Convenience factory function
def create_dynamic_multi_agent(
    agents: list[Agent], name: str = "DynamicMultiAgent", **kwargs
) -> DynamicMultiAgent:
    """Create a dynamic multi-agent system.

    Args:
        agents: List of agents to include
        name: Name for the multi-agent system
        **kwargs: Additional configuration

    Returns:
        DynamicMultiAgent instance
    """
    return DynamicMultiAgent(
        name=name, agents=agents, coordination_mode="dynamic", **kwargs
    )
