"""Enhanced MultiAgent V3 - Full feature implementation using enhanced base Agent.

This version combines the best features from clean.py and enhanced_multi_agent_standalone.py:
- Production-ready coordination from clean.py
- Generic typing and performance features from standalone
- Full integration with enhanced base Agent class
- V3 pattern consistency with SimpleAgent V3 and ReactAgent V3

Key Features:
- Generic typing: MultiAgent[AgentsT] for type safety
- Performance tracking and adaptive routing
- Rich debugging and observability like other V3 agents
- Multi-engine coordination capabilities
- Comprehensive persistence and state management
- Backward compatibility with existing patterns
"""

import logging
import time
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.enhanced_multi_agent_state import (
    EnhancedMultiAgentState,
)
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from pydantic import Field, field_validator, model_validator
from rich.console import Console
from rich.table import Table

# Import the enhanced base Agent
from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)
console = Console()

# Generic type for agents contained in MultiAgent
AgentsT = TypeVar("AgentsT", bound=dict[str, Agent] | list[Agent])


# ========================================================================
# ENHANCED MULTI AGENT V3
# ========================================================================


class EnhancedMultiAgent(Agent, Generic[AgentsT]):
    """Enhanced MultiAgent V3 with full advanced features.

    This agent combines the production stability of clean.py with advanced features
    from enhanced_multi_agent_standalone.py, following the V3 pattern established
    by SimpleAgent V3 and ReactAgent V3.

    Core Features:
    - Generic typing for contained agents: MultiAgent[AgentsT]
    - Production-ready coordination patterns (sequential, parallel, conditional, custom)
    - Intelligent routing detection and BaseGraph integration
    - Rich API for flexible routing configuration
    - Real component testing (no mocks)

    Enhanced V3 Features:
    - Performance tracking and adaptive routing
    - Rich debugging and observability
    - Multi-engine coordination capabilities
    - Advanced persistence configuration
    - Comprehensive capabilities display and analysis

    Multi-Agent Specific Features:
    - Flexible agent management (dict or list)
    - Entry point configuration for workflow control
    - Branch configurations for complex routing
    - Custom routing methods: add_conditional_routing, add_parallel_group, add_edge
    - Intelligent vs custom routing detection

    Performance Features:
    - Agent performance metrics tracking
    - Adaptive routing based on success rates and timing
    - Execution optimization and caching
    - Load balancing across agents

    Attributes:
        agents: Generic collection of agents to coordinate (AgentsT)
        execution_mode: How to execute agents (infer/sequential/parallel/conditional/branch)
        entry_point: Starting agent for execution
        branches: Branch configurations for routing
        infer_sequence: Whether to auto-infer execution sequence

    Enhanced Attributes:
        multi_engine_mode: Enable multiple engines for coordination
        advanced_routing: Enable sophisticated routing algorithms
        performance_mode: Enable performance tracking and optimization
        debug_mode: Enable rich debugging and observability
        agent_performance: Performance metrics for each agent
        adaptation_rate: Rate of performance adaptation
        max_iterations: Maximum iterations for conditional flows

    Examples:
        Basic sequential execution (backwards compatible)::

            from haive.agents.simple import SimpleAgent

            agent1 = SimpleAgent(name="analyzer")
            agent2 = SimpleAgent(name="summarizer")

            multi_agent = EnhancedMultiAgent(agents=[agent1, agent2])
            result = await multi_agent.arun("Process this data")

        Enhanced features with performance tracking::

            multi_agent = EnhancedMultiAgent(
                name="adaptive_coordinatof",
                agents={"fast": fast_agent, "accurate": accurate_agent},
                execution_mode="branch",
                performance_mode=True,
                debug_mode=True,
                adaptation_rate=0.2
            )

        Conditional routing with entry point::

            multi_agent = EnhancedMultiAgent(
                agents=[classifier, billing_agent, technical_agent],
                entry_point="classifier",
                advanced_routing=True
            )

            multi_agent.add_conditional_routing(
                "classifier",
                lambda state: state.get("category", "general"),
                {
                    "billing": "billing_agent",
                    "technical": "technical_agent",
                    "general": "billing_agent"
                }
            )

        Parallel execution with convergence::

            multi_agent = EnhancedMultiAgent(
                agents=[processor1, processor2, processor3, aggregator],
                performance_mode=True
            )

            multi_agent.add_parallel_group(
                ["processor1", "processor2", "processor3"],
                next_agent="aggregatof"
            )

        Generic typing with specialized agents::

            from typing import Dict

            agents: Dict[str, SimpleAgent] = {
                "researcher": research_agent,
                "analyzer": analysis_agent,
                "writer": writing_agent
            }

            multi: EnhancedMultiAgent[Dict[str, SimpleAgent]] = EnhancedMultiAgent(
                name="content_team",
                agents=agents,
                multi_engine_mode=True,
                debug_mode=True
            )
    """

    # ========================================================================
    # CORE AGENT MANAGEMENT (from clean.py)
    # ========================================================================

    # Generic agents field - follows enhanced base Agent pattern
    agents: AgentsT = Field(
        default_factory=dict,  # Default to dict for backward compatibility
        description="Generic collection of agents this multi-agent coordinates",
    )

    agent: Agent | None = Field(
        default=None,
        description="Main/default agent for this multi-agent (legacy support)",
    )

    # Execution configuration
    execution_mode: str = Field(
        default="infer",
        description="How to execute agents: infer, sequential, parallel, conditional, branch",
    )

    infer_sequence: bool = Field(
        default=True,
        description="Whether to automatically infer execution sequence from agent dependencies",
    )

    # Branch configuration for custom routing
    branches: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Branch configurations for conditional and custom routing",
    )

    entry_point: str | None = Field(
        default=None,
        description="Starting agent for execution (if not specified, uses first agent or infers)",
    )

    # ========================================================================
    # ENHANCED V3 FEATURES (following SimpleAgent V3 pattern)
    # ========================================================================

    # Enhanced capabilities
    multi_engine_mode: bool = Field(
        default=False, description="Enable multiple engines for coordination"
    )

    advanced_routing: bool = Field(
        default=False, description="Enable sophisticated routing algorithms"
    )

    performance_mode: bool = Field(
        default=False, description="Enable performance tracking and optimization"
    )

    debug_mode: bool = Field(
        default=False, description="Enable rich debugging and observability"
    )

    persistence_config: dict[str, Any] | None = Field(
        default=None, description="Advanced persistence configuration"
    )

    # ========================================================================
    # PERFORMANCE TRACKING FEATURES (from standalone)
    # ========================================================================

    # Performance tracking for adaptive routing
    agent_performance: dict[str, dict[str, float]] = Field(
        default_factory=dict, description="Performance metrics for each agent"
    )

    adaptation_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Rate of performance adaptation (0.0 = no adaptation, 1.0 = immediate)",
    )

    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum iterations for conditional/branch modes",
    )

    # ========================================================================
    # VALIDATION AND SETUP
    # ========================================================================

    @model_validator(mode="before")
    @classmethod
    def normalize_agents_and_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Normalize agents dict and auto-generate name - follows engines pattern."""
        if not isinstance(values, dict):
            return values

        # Initialize agents if not present
        # Check the type annotation to determine default type
        if "agents" not in values or values.get("agents") is None:
            # Check the actual field annotation from the model
            if "agents" in cls.model_fields:
                field_info = cls.model_fields["agents"]

                # Check if the annotation is a List type
                from typing import get_origin

                annotation = field_info.annotation
                origin = get_origin(annotation)

                if origin is list or origin is list:
                    values["agents"] = []
                else:
                    # Default to dict for backward compatibility
                    values["agents"] = {}
            else:
                # Default to dict if field not found
                values["agents"] = {}

        # Move single agent to agents dict
        if "agent" in values and values["agent"] is not None:
            agent = values["agent"]
            # Add to agents dict with appropriate key
            if hasattr(agent, "name") and agent.name:
                values["agents"][agent.name] = agent
            else:
                values["agents"]["main"] = agent

        # Normalize agents field based on the generic type
        if "agents" in values and values["agents"] is not None:
            agents = values["agents"]

            # Check if we should keep as list based on the field annotation
            should_keep_list = False

            # Check the actual field annotation from the model
            if "agents" in cls.model_fields:
                field_info = cls.model_fields["agents"]

                # Check if the annotation is a List type
                from typing import get_origin

                annotation = field_info.annotation
                origin = get_origin(annotation)

                if origin is list or origin is list:
                    should_keep_list = True

            if isinstance(agents, list):
                if should_keep_list:
                    # Keep as list for List generic types
                    values["agents"] = agents
                else:
                    # Convert list to dict using agent names
                    agent_dict = {}
                    for i, agent in enumerate(agents):
                        if hasattr(agent, "name") and agent.name:
                            # Handle duplicate names by adding index
                            base_name = agent.name
                            if base_name in agent_dict:
                                agent_dict[f"{base_name}_{i}"] = agent
                            else:
                                agent_dict[base_name] = agent
                        else:
                            agent_dict[f"agent_{i}"] = agent
                    values["agents"] = agent_dict

            elif not isinstance(agents, dict):
                # Single agent not in dict form
                if should_keep_list:
                    values["agents"] = [agents]
                elif hasattr(agents, "name") and agents.name:
                    values["agents"] = {agents.name: agents}
                else:
                    values["agents"] = {"main": agents}

        return values

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: AgentsT) -> AgentsT:
        """Validate agents collection."""
        if isinstance(v, dict):
            # Allow empty dict during initialization - some subclasses populate later
            if v:
                # Validate all values are agents
                for name, agent in v.items():
                    if (
                        not hasattr(agent, "run")
                        and not hasattr(agent, "arun")
                        and not hasattr(agent, "invoke")
                    ):
                        raise ValueError(
                            f"Agent '{name}' must have run/arun/invoke method"
                        )
        elif isinstance(v, list):
            # Allow empty list during initialization - some subclasses populate later
            if v:
                # Validate all items are agents
                for i, agent in enumerate(v):
                    if (
                        not hasattr(agent, "run")
                        and not hasattr(agent, "arun")
                        and not hasattr(agent, "invoke")
                    ):
                        raise ValueError(
                            f"Agent at index {i} must have run/arun/invoke method"
                        )
        else:
            raise ValueError("Agents must be dict or list")
        return v

    @field_validator("adaptation_rate")
    @classmethod
    def validate_adaptation_rate(cls, v):
        """Validate adaptation rate range."""
        if not (0.0 <= v <= 1.0):
            raise ValueError("Adaptation rate must be between 0.0 and 1.0")
        return v

    # ========================================================================
    # AGENT SETUP AND CONFIGURATION
    # ========================================================================

    def setup_agent(self) -> None:
        """Enhanced multi-agent setup with V3 features.

        This setup method:
        1. Sets up MultiAgentState as default state schema
        2. Initializes performance tracking for all agents
        3. Configures multi-engine mode if enabled
        4. Sets up advanced routing if enabled
        5. Configures debug mode if enabled
        6. Sets up performance optimization if enabled
        7. Enables automatic schema generation
        """
        logger.debug(f"Setting up EnhancedMultiAgent V3: {self.name}")

        # Call parent setup
        super().setup_agent()

        # Set default state schema if none provided
        if self.state_schema is None:
            # Use enhanced state schema for V3 features, fallback to basic for compatibility
            if any([self.performance_mode, self.debug_mode, self.advanced_routing]):
                self.state_schema = EnhancedMultiAgentState
                logger.debug(f"Using EnhancedMultiAgentState for {self.name}")
            else:
                self.state_schema = MultiAgentState
                logger.debug(f"Using MultiAgentState for {self.name}")

        # Initialize performance tracking if in performance mode
        if self.performance_mode:
            self._initialize_performance_tracking()

        # Configure multi-engine mode
        if self.multi_engine_mode:
            self._setup_multi_engine_mode()

        # Configure advanced routing
        if self.advanced_routing:
            self._setup_advanced_routing()

        # Enable automatic schema generation
        self.set_schema = True

        logger.debug(f"EnhancedMultiAgent V3 setup complete: {self.name}")

    def _initialize_performance_tracking(self) -> None:
        """Initialize performance tracking for all agents."""
        for agent_name in self.get_agent_names():
            if agent_name not in self.agent_performance:
                self.agent_performance[agent_name] = {
                    "success_rate": 0.5,  # Start neutral
                    "avg_duration": 1.0,  # Start with 1 second baseline
                    "task_count": 0,
                    "last_execution": None,
                    "total_duration": 0.0,
                }
        logger.debug(
            f"Initialized performance tracking for {len(self.agent_performance)} agents"
        )

    def _setup_multi_engine_mode(self) -> None:
        """Configure multi-engine support."""
        # Create coordination engine if none exists
        if not self.engine:
            self.engine = AugLLMConfig(
                temperature=0.3,  # Lower temperature for coordination decisions
                system_message="You are a coordination agent managing multiple specialized agents.",
            )
            self.engines["coordinator"] = self.engine
        logger.debug("Multi-engine mode configured")

    def _setup_advanced_routing(self) -> None:
        """Configure advanced routing capabilities."""
        # Advanced routing setup - framework for future expansion
        logger.debug("Advanced routing configured")

    # ========================================================================
    # AGENT MANAGEMENT UTILITIES
    # ========================================================================

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        if isinstance(self.agents, dict):
            return list(self.agents.keys())
        # For list, generate names
        return [f"agent_{i}" for i in range(len(self.agents))]

    def get_agent(self, name: str) -> Agent | None:
        """Get agent by name."""
        if isinstance(self.agents, dict):
            return self.agents.get(name)
        # Handle list case
        if name.startswith("agent_"):
            try:
                idx = int(name.split("_")[1])
                return self.agents[idx] if idx < len(self.agents) else None
            except (IndexError, ValueError):
                return None
        return None

    # ========================================================================
    # GRAPH BUILDING (from clean.py)
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the BaseGraph for this multi-agent.

        Uses intelligent routing from BaseGraph for sequence inference and branching.
        Enhanced with V3 debugging and performance features.
        """
        if self.debug_mode:
            logger.info(f"Building graph for EnhancedMultiAgent V3: {self.name}")

        # Create BaseGraph with state schema
        graph = BaseGraph(name=f"{self.name}_graph", state_schema=self.state_schema)

        # Store agents in graph metadata for AgentNodeV3Config to access
        graph.metadata["agents"] = self.agents

        # Check if we have custom routing patterns
        has_custom_routing = any(
            branch.get("type") in ["conditional", "parallel", "direct"]
            for branch in self.branches.values()
        )

        if has_custom_routing:
            if self.debug_mode:
                logger.info("Using custom routing patterns")
            # Build custom graph with enhanced routing
            self._build_custom_routing(graph)
        else:
            if self.debug_mode:
                logger.info("Using intelligent routing")
            # Wrap agents in AgentNodeV3Config for intelligent routing
            wrapped_agents = {}
            for agent_name, agent in self.agents.items():
                # Create AgentNodeV3Config to make agent callable
                agent_node = AgentNodeV3Config(
                    name=f"agent_{agent_name}",
                    agent_name=agent_name,
                    agent=agent,  # Pass agent directly
                )
                wrapped_agents[agent_name] = agent_node

            # Use BaseGraph's intelligent routing with wrapped agents
            graph.add_intelligent_agent_routing(
                agents=wrapped_agents,
                execution_mode=self.execution_mode,
                branches=self.branches,
                prefix="",  # No prefix for clean agent names
            )

        if self.debug_mode:
            logger.info(f"Graph built successfully with {len(self.agents)} agents")

        return graph

    def _build_custom_routing(self, graph: BaseGraph):
        """Build custom routing based on enhanced branch configurations."""
        # Add all agents as nodes first, wrapped in AgentNodeV3Config
        for agent_name, agent in self.agents.items():
            # Create AgentNodeV3Config to make agent callable
            agent_node = AgentNodeV3Config(
                name=f"agent_{agent_name}",
                agent_name=agent_name,
                agent=agent,  # Pass agent directly
            )
            graph.add_node(agent_name, agent_node)

        # Track processed edges to handle entry point
        processed_sources = set()
        has_entry_edges = False

        # Process branches for custom routing
        for source, branch_config in self.branches.items():
            branch_type = branch_config.get("type", "legacy")

            if branch_type == "conditional":
                # Add conditional routing
                condition_fn = branch_config["condition_fn"]
                routes = branch_config["routes"]

                def make_condition_fn(fn, route_map) -> Any:
                    def condition_wrapper(state: dict[str, Any]):
                        route_key = fn(state)
                        return route_map.get(route_key, next(iter(route_map.values())))

                    return condition_wrapper

                graph.add_conditional_edges(
                    source, make_condition_fn(condition_fn, routes)
                )
                processed_sources.add(source)
                has_entry_edges = True

            elif branch_type == "direct":
                # Add direct edge
                target = branch_config["target"]
                graph.add_edge(source, target)
                processed_sources.add(source)
                has_entry_edges = True

            elif branch_type == "conditional_direct":
                # Handle add_conditional_edges compatibility
                path_fn = branch_config["path_fn"]
                graph.add_conditional_edges(source, path_fn)
                processed_sources.add(source)
                has_entry_edges = True

            elif branch_type == "parallel":
                # Handle parallel group properly
                agents = branch_config["agents"]
                next_agent = branch_config.get("next")

                # Add virtual nodes if they don't represent actual parallel groups
                if source.startswith("parallel_"):
                    # This is a parallel group configuration, not a real agent
                    # Create edges from START to each parallel agent
                    for agent_name in agents:
                        if agent_name in self.agents:
                            # If this is the first set of edges, connect from START
                            if not has_entry_edges and self.entry_point is None:
                                graph.add_edge("__start__", agent_name)

                            # Connect to next agent if specified
                            if next_agent and next_agent in self.agents:
                                graph.add_edge(agent_name, next_agent)
                            else:
                                # Otherwise connect to END
                                graph.add_edge(agent_name, "__end__")
                    has_entry_edges = True
                else:
                    # Source is a real agent that branches to parallel execution
                    for agent_name in agents:
                        if agent_name in self.agents:
                            graph.add_edge(source, agent_name)
                            if next_agent and next_agent in self.agents:
                                graph.add_edge(agent_name, next_agent)
                    processed_sources.add(source)
                    has_entry_edges = True

            else:
                # Legacy branch format - convert to conditional
                targets = branch_config.get("targets", [])
                if targets:
                    # Simple condition - route to first target
                    graph.add_edge(source, targets[0])
                    processed_sources.add(source)
                    has_entry_edges = True

        # Handle entry point
        if self.entry_point and self.entry_point in self.agents:
            graph.add_edge("__start__", self.entry_point)
        elif not has_entry_edges:
            # No explicit routing, connect first agent to start
            first_agent = next(iter(self.agents.keys())) if self.agents else None
            if first_agent:
                graph.add_edge("__start__", first_agent)

        # Ensure all terminal nodes connect to END
        for agent_name in self.agents:
            # Check if this node has any outgoing edges
            has_outgoing = any(source == agent_name for source in self.branches)
            if not has_outgoing and agent_name not in processed_sources:
                # This is a terminal node
                graph.add_edge(agent_name, "__end__")

    # ========================================================================
    # ROUTING CONFIGURATION METHODS (from clean.py)
    # ========================================================================

    def add_conditional_routing(
        self,
        source_agent: str,
        condition_fn: Callable[[dict[str, Any]], str],
        routes: dict[str, str],
    ) -> None:
        """Add conditional routing with a function that returns route keys.

        This method enables dynamic routing based on state conditions. The condition
        function receives the current state and returns a key that maps to a target
        agent in the routes dictionary.

        Args:
            source_agent: The agent to route from. Must exist in the agents dictionary.
            condition_fn: Function that takes state dict and returns a route key.
                Should return a string that exists as a key in the routes dictionary.
            routes: Dictionary mapping route keys to target agent names.
                Keys are the possible return values from condition_fn.
                Values are agent names that must exist in the agents dictionary.

        Examples:
            Basic conditional routing::

                def route_by_priority(state):
                    return "high" if state.get("priority", 0) > 5 else "normal"

                multi_agent.add_conditional_routing(
                    "classifief",
                    route_by_priority,
                    {"high": "urgent_processor", "normal": "standard_processor"}
                )
        """
        self.branches[source_agent] = {
            "condition_fn": condition_fn,
            "routes": routes,
            "type": "conditional",
        }

    def add_parallel_group(
        self, agent_names: list[str], next_agent: str | None = None
    ) -> None:
        """Add a group of agents that run in parallel.

        This method configures a set of agents to execute in parallel, with
        optional convergence to a single agent after parallel execution completes.

        Args:
            agent_names: List of agent names to run in parallel.
                All names must exist in the agents dictionary.
            next_agent: Optional next agent to run after the parallel group completes.
                If provided, must exist in the agents dictionary.

        Examples:
            Parallel processing with convergence::

                multi_agent.add_parallel_group(
                    ["data_processor", "image_processor", "text_processor"],
                    next_agent="aggregator"
                )
        """
        group_name = f"parallel_{'_'.join(agent_names)}"
        self.branches[group_name] = {
            "type": "parallel",
            "agents": agent_names,
            "next": next_agent,
        }

    def add_edge(self, source_agent: str, target_agent: str) -> None:
        """Add a direct edge between two agents.

        This method creates a direct connection from one agent to another,
        ensuring the target agent runs after the source agent completes.

        Args:
            source_agent: Source agent name. Must exist in the agents dictionary.
            target_agent: Target agent name. Must exist in the agents dictionary.

        Examples:
            Sequential flow::

                multi_agent.add_edge("preprocessor", "analyzer")
                multi_agent.add_edge("analyzer", "postprocessor")
        """
        self.branches[source_agent] = {"type": "direct", "target": target_agent}

    # ========================================================================
    # PERFORMANCE TRACKING (from standalone)
    # ========================================================================

    def update_performance(
        self, agent_name: str, success: bool, duration: float
    ) -> None:
        """Update agent performance metrics."""
        if not self.performance_mode or agent_name not in self.agent_performance:
            return

        metrics = self.agent_performance[agent_name]
        metrics["task_count"] += 1
        metrics["total_duration"] += duration
        metrics["last_execution"] = time.time()

        # Update success rate with exponential moving average
        current_rate = metrics["success_rate"]
        new_rate = (
            current_rate * (1 - self.adaptation_rate)
            + (1.0 if success else 0.0) * self.adaptation_rate
        )
        metrics["success_rate"] = new_rate

        # Update average duration
        metrics["avg_duration"] = metrics["total_duration"] / metrics["task_count"]

        if self.debug_mode:
            logger.debug(
                f"Updated performance for {agent_name}: success_rate={new_rate:.3f}, avg_duration={metrics['avg_duration']:.3f}s"
            )

    def get_best_agent_for_task(self, task_type: str = "general") -> str:
        """Get best performing agent based on metrics."""
        if not self.performance_mode or not self.agent_performance:
            # Fallback to first agent
            return next(iter(self.agents.keys())) if self.agents else ""

        best_agent = None
        best_score = 0.0

        for agent_name, metrics in self.agent_performance.items():
            # Score = success_rate / avg_duration (higher is better)
            score = metrics["success_rate"] / max(metrics["avg_duration"], 0.1)
            if score > best_score:
                best_score = score
                best_agent = agent_name

        result = best_agent or next(iter(self.agents.keys()))
        if self.debug_mode:
            logger.debug(f"Selected best agent: {result} (score: {best_score:.3f})")
        return result

    # ========================================================================
    # RICH CAPABILITIES DISPLAY (V3 pattern)
    # ========================================================================

    def display_capabilities(self) -> None:
        """Display comprehensive multi-agent capabilities."""
        table = Table(title=f"Enhanced MultiAgent Capabilities: {self.name}")
        table.add_column("Category", style="cyan")
        table.add_column("Details", style="green")

        # Basic info
        table.add_row("Type", "EnhancedMultiAgent")
        table.add_row("Agents", str(len(self.agents)))
        table.add_row("Execution Mode", self.execution_mode)

        # Enhanced features
        table.add_row("Multi-Engine", "✅" if self.multi_engine_mode else "❌")
        table.add_row("Advanced Routing", "✅" if self.advanced_routing else "❌")
        table.add_row("Performance Mode", "✅" if self.performance_mode else "❌")
        table.add_row("Debug Mode", "✅" if self.debug_mode else "❌")

        # Agent details
        agent_names = ", ".join(self.get_agent_names())
        table.add_row(
            "Agent Names",
            agent_names[:50] + "..." if len(agent_names) > 50 else agent_names,
        )

        # Routing info
        table.add_row("Custom Branches", str(len(self.branches)))
        table.add_row("Entry Point", self.entry_point or "Auto")

        console.print(table)

    def get_capabilities_summary(self) -> dict[str, Any]:
        """Get comprehensive capabilities summary."""
        return {
            "agent_type": "EnhancedMultiAgent",
            "agent_count": len(self.agents),
            "agent_names": self.get_agent_names(),
            "execution_mode": self.execution_mode,
            "features": {
                "multi_engine_mode": self.multi_engine_mode,
                "advanced_routing": self.advanced_routing,
                "performance_mode": self.performance_mode,
                "debug_mode": self.debug_mode,
                "has_custom_branches": len(self.branches) > 0,
                "has_entry_point": self.entry_point is not None,
                "has_performance_tracking": len(self.agent_performance) > 0,
            },
            "configuration": {
                "infer_sequence": self.infer_sequence,
                "adaptation_rate": self.adaptation_rate,
                "max_iterations": self.max_iterations,
                "custom_branches": len(self.branches),
                "entry_point": self.entry_point,
            },
            "performance": {
                "tracked_agents": len(self.agent_performance),
                "total_executions": sum(
                    metrics.get("task_count", 0)
                    for metrics in self.agent_performance.values()
                ),
            },
        }

    def analyze_agent_performance(self) -> dict[str, Any]:
        """Analyze agent performance metrics."""
        if not self.performance_mode:
            return {
                "performance_mode": False,
                "message": "Performance tracking disabled",
            }

        analysis = {
            "performance_mode": True,
            "adaptation_rate": self.adaptation_rate,
            "agents": {},
        }

        for agent_name, metrics in self.agent_performance.items():
            analysis["agents"][agent_name] = {
                "success_rate": round(metrics["success_rate"], 3),
                "avg_duration": round(metrics["avg_duration"], 3),
                "task_count": metrics["task_count"],
                "efficiency_score": round(
                    metrics["success_rate"] / max(metrics["avg_duration"], 0.1), 3
                ),
            }

        # Overall statistics
        if self.agent_performance:
            avg_success = sum(
                m["success_rate"] for m in self.agent_performance.values()
            ) / len(self.agent_performance)
            avg_duration = sum(
                m["avg_duration"] for m in self.agent_performance.values()
            ) / len(self.agent_performance)
            total_tasks = sum(m["task_count"] for m in self.agent_performance.values())

            analysis["overall"] = {
                "average_success_rate": round(avg_success, 3),
                "average_duration": round(avg_duration, 3),
                "total_tasks": total_tasks,
                "best_agent": self.get_best_agent_for_task(),
            }

        return analysis

    # ========================================================================
    # FACTORY METHODS
    # ========================================================================

    @classmethod
    def create(
        cls,
        agents: list[Agent] | dict[str, Agent],
        name: str = "multi_agent",
        execution_mode: str = "infer",
        **kwargs,
    ) -> "EnhancedMultiAgent":
        """Create an enhanced multi-agent from a collection of agents.

        This factory method provides a convenient way to create an EnhancedMultiAgent
        from a collection of agents with optional configuration.

        Args:
            agents: Collection of Agent instances to coordinate.
            name: Name for the multi-agent instance.
            execution_mode: Execution pattern - "infer", "sequential", "parallel",
                "conditional", or "branch".
            **kwargs: Additional key arguments passed to the constructor.

        Returns:
            EnhancedMultiAgent: Configured enhanced multi-agent instance.

        Examples:
            Basic creation::

                agents = [SimpleAgent(name="a"), SimpleAgent(name="b")]
                multi_agent = EnhancedMultiAgent.create(agents, name="my_workflow")

            With enhanced features::

                multi_agent = EnhancedMultiAgent.create(
                    agents,
                    name="adaptive_workflow",
                    execution_mode="branch",
                    performance_mode=True,
                    debug_mode=True
                )
        """
        return cls(name=name, agents=agents, execution_mode=execution_mode, **kwargs)

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================

    def __repr__(self) -> str:
        """Enhanced string representation."""
        agent_count = len(self.agents)
        agents_type = type(self.agents).__name__
        features = []

        if self.multi_engine_mode:
            features.append("multi-engine")
        if self.advanced_routing:
            features.append("advanced-routing")
        if self.performance_mode:
            features.append("performance")
        if self.debug_mode:
            features.append("debug")

        feature_str = f", features=[{', '.join(features)}]" if features else ""

        return (
            f"EnhancedMultiAgent[{agents_type}]("
            f"name='{self.name}', "
            f"agents={agent_count}, "
            f"mode='{self.execution_mode}'"
            f"{feature_str})"
        )
