"""Dynamic Activation Supervisor for Component Management.

This module provides DynamicActivationSupervisor, a supervisor agent that can
dynamically activate components based on task requirements using the Dynamic
Activation Pattern with MetaStateSchema integration.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- @packages/haive-agents/examples/supervisor/advanced/dynamic_activation_example.py

Implementation Notes:
- Uses factory methods for complex initialization (no __init__ override)
- Private attributes for internal state (_discovery_agent)
- MetaStateSchema for component wrapping
- DynamicActivationState as state schema
- Proper Pydantic patterns throughout
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph import BaseGraph
from haive.core.registry import RegistryItem
from haive.core.schema.prebuilt.dynamic_activation_state import DynamicActivationState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import PrivateAttr

from haive.agents.base.agent import Agent
from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent


class DynamicActivationSupervisor(Agent[DynamicActivationState]):
    """Supervisor agent that can dynamically activate components.

    This supervisor extends the basic Agent class with dynamic activation
    capabilities. It can discover, activate, and manage components based on
    task requirements using MetaStateSchema for component wrapping.

    Key Features:
        - Dynamic component discovery using ComponentDiscoveryAgent
        - Automatic component activation based on task analysis
        - MetaStateSchema integration for component tracking
        - Factory methods for complex initialization
        - Graph-based workflow with conditional routing
        - Capability gap detection and filling

    Args:
        name: Supervisor name
        engine: AugLLMConfig for LLM-based decision making
        state_schema: DynamicActivationState (set automatically)

    Private Attributes:
        _discovery_agent: ComponentDiscoveryAgent for finding components
        _meta_self: MetaStateSchema wrapper for self-tracking

    Examples:
        Basic usage::

            from haive.agents.supervisor.dynamic_activation_supervisor import DynamicActivationSupervisor
            from haive.core.engine.aug_llm import AugLLMConfig

            # Create supervisor
            supervisor = DynamicActivationSupervisor(
                name="dynamic_supervisor",
                engine=AugLLMConfig()
            )

            # Run task - supervisor will discover and activate components as needed
            result = await supervisor.arun("Calculate compound interest and create a chart")

        With discovery agent::

            supervisor = DynamicActivationSupervisor.create_with_discovery(
                name="discovery_supervisor",
                document_path="@haive-tools/docs",
                engine=AugLLMConfig()
            )

            # Supervisor will use discovery agent to find needed components
            result = await supervisor.arun("Process CSV data and generate insights")

        Manual component registration::

            supervisor = DynamicActivationSupervisor(
                name="manual_supervisor",
                engine=AugLLMConfig()
            )

            # Register components manually
            item = RegistryItem(
                id="calc_tool",
                name="Calculator",
                description="Mathematical calculations",
                component=calculator_tool
            )
            supervisor.state.registry.register(item)

            # Use registered components
            result = await supervisor.arun("Calculate 15 * 23")
    """

    # Set state schema to DynamicActivationState
    state_schema: type[DynamicActivationState] = DynamicActivationState

    # Private attributes for internal state (not serialized)
    _discovery_agent: ComponentDiscoveryAgent | None = PrivateAttr(default=None)
    _meta_self: MetaStateSchema | None = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Setup the dynamic activation supervisor.

        This method is called during agent initialization to set up
        the supervisor's internal state and components.
        """
        # Call parent setup
        super().setup_agent()

        # Initialize discovery agent if config is provided
        if hasattr(self, "_discovery_config"):
            self._discovery_agent = ComponentDiscoveryAgent(
                document_path=self._discovery_config["document_path"]
            )

        # Wrap self in MetaStateSchema for self-tracking
        self._meta_self = MetaStateSchema(
            agent=self,
            agent_state={"supervisor_mode": "dynamic_activation"},
            graph_context={
                "role": "supervisor",
                "activation_support": True,
                "discovery_enabled": self._discovery_agent is not None,
            },
        )

        # Set up default tools for the supervisor
        self._setup_supervisor_tools()

    @classmethod
    def create_with_discovery(
        cls, name: str, document_path: str, engine: AugLLMConfig, **kwargs
    ) -> "DynamicActivationSupervisor":
        """Factory method to create supervisor with discovery agent.

        Args:
            name: Supervisor name
            document_path: Path to documentation for component discovery
            engine: AugLLMConfig for supervisor
            **kwargs: Additional arguments for supervisor

        Returns:
            DynamicActivationSupervisor with discovery capabilities

        Examples:
            Create with Haive tools discovery::

                supervisor = DynamicActivationSupervisor.create_with_discovery(
                    name="haive_supervisor",
                    document_path="@haive-tools",
                    engine=AugLLMConfig()
                )

            Create with custom documentation::

                supervisor = DynamicActivationSupervisor.create_with_discovery(
                    name="custom_supervisor",
                    document_path="/path/to/docs",
                    engine=AugLLMConfig(temperature=0.3)
                )
        """
        # Create supervisor instance
        supervisor = cls(name=name, engine=engine, **kwargs)

        # Set discovery configuration (used in setup_agent)
        supervisor._discovery_config = {"document_path": document_path}

        return supervisor

    @classmethod
    def create_with_components(
        cls, name: str, components: list[dict[str, Any]], engine: AugLLMConfig, **kwargs
    ) -> "DynamicActivationSupervisor":
        """Factory method to create supervisor with pre-registered components.

        Args:
            name: Supervisor name
            components: List of component dictionaries to register
            engine: AugLLMConfig for supervisor
            **kwargs: Additional arguments for supervisor

        Returns:
            DynamicActivationSupervisor with pre-registered components

        Examples:
            Create with tools::

                components = [
                    {
                        "id": "calc",
                        "name": "Calculator",
                        "description": "Math operations",
                        "component": calculator_tool
                    },
                    {
                        "id": "search",
                        "name": "Web Search",
                        "description": "Web searching",
                        "component": search_tool
                    }
                ]

                supervisor = DynamicActivationSupervisor.create_with_components(
                    name="tool_supervisor",
                    components=components,
                    engine=AugLLMConfig()
                )
        """
        # Create supervisor instance
        supervisor = cls(name=name, engine=engine, **kwargs)

        # Register components after creation
        for comp_data in components:
            item = RegistryItem(
                id=comp_data["id"],
                name=comp_data["name"],
                description=comp_data["description"],
                component=comp_data["component"],
                metadata=comp_data.get("metadata", {}),
            )
            supervisor.state.registry.register(item)

        return supervisor

    def _setup_supervisor_tools(self) -> None:
        """Set up default tools for the supervisor.

        This method adds core supervisor tools to the engine for
        component management and task routing.
        """

        # Tool for analyzing task requirements
        @tool
        def analyze_task_requirements(task_description: str) -> dict[str, Any]:
            """Analyze task and identify required capabilities."""
            capabilities = []

            # Simple capability detection (can be enhanced)
            task_lower = task_description.lower()

            if any(
                word in task_lower
                for word in ["calculate", "math", "compute", "number"]
            ):
                capabilities.append("math")
            if any(word in task_lower for word in ["search", "find", "lookup", "web"]):
                capabilities.append("search")
            if any(
                word in task_lower for word in ["chart", "plot", "graph", "visualize"]
            ):
                capabilities.append("visualization")
            if any(word in task_lower for word in ["file", "read", "write", "process"]):
                capabilities.append("file_processing")
            if any(
                word in task_lower
                for word in ["data", "analyze", "process", "transform"]
            ):
                capabilities.append("data_processing")

            return {
                "task": task_description,
                "required_capabilities": capabilities,
                "analysis_method": "keyword_based",
            }

        # Tool for activating components
        @tool
        def activate_component(component_id: str, reason: str = "") -> dict[str, Any]:
            """Activate a component by ID."""
            # Access state through self (tool has access to supervisor context)
            meta_state = self.state.activate_component(component_id)

            if meta_state:
                return {
                    "success": True,
                    "component_id": component_id,
                    "reason": reason,
                    "meta_state_created": True,
                }
            return {
                "success": False,
                "component_id": component_id,
                "reason": reason,
                "error": "Component not found or already active",
            }

        # Tool for discovering components
        @tool
        def discover_components(
            query: str, max_results: int = 5
        ) -> list[dict[str, Any]]:
            """Discover components that match a query."""
            if self._discovery_agent:
                # Use discovery agent if available
                import asyncio

                try:
                    loop = asyncio.get_event_loop()
                    components = loop.run_until_complete(
                        self._discovery_agent.discover_components(query)
                    )
                    return components[:max_results]
                except Exception as e:
                    return [{"error": f"Discovery failed: {e}"}]
            else:
                # Fallback to registry search
                registry_items = self.state.registry.list_components()
                matches = []

                for item_id in registry_items:
                    item = self.state.registry.get_item(item_id)
                    if item and query.lower() in item.name.lower():
                        matches.append(
                            {
                                "id": item.id,
                                "name": item.name,
                                "description": item.description,
                                "is_active": item.is_active,
                            }
                        )

                return matches[:max_results]

        # Tool for checking component status
        @tool
        def check_component_status(component_id: str | None = None) -> dict[str, Any]:
            """Check status of components."""
            if component_id:
                # Check specific component
                item = self.state.registry.get_item(component_id)
                if item:
                    return {
                        "component_id": component_id,
                        "name": item.name,
                        "is_active": item.is_active,
                        "activation_count": item.activation_count,
                        "last_activated": (
                            str(item.last_activated) if item.last_activated else None
                        ),
                    }
                return {"error": f"Component {component_id} not found"}
            # Check all components
            stats = self.state.get_activation_stats()
            return {
                "total_components": stats["total_components"],
                "active_components": stats["active_components"],
                "activation_rate": stats["activation_rate"],
                "current_task": stats["current_task"],
            }

        # Add tools to engine if it has tools attribute
        if hasattr(self.engine, "tools"):
            self.engine.tools.extend(
                [
                    analyze_task_requirements,
                    activate_component,
                    discover_components,
                    check_component_status,
                ]
            )

    def build_graph(self) -> BaseGraph:
        """Build the dynamic activation supervisor graph.

        Returns:
            Compiled BaseGraph with supervisor workflow
        """
        graph = BaseGraph(name="DynamicActivationSupervisor")

        # Add nodes
        graph.add_node("supervisor", self._supervisor_node)
        graph.add_node("analyze_task", self._analyze_task_node)
        graph.add_node("discover_components", self._discover_components_node)
        graph.add_node("activate_components", self._activate_components_node)
        graph.add_node("execute_task", self._execute_task_node)

        # Add conditional edges
        graph.add_conditional_edges(
            "supervisof",
            self._route_supervisor,
            {
                "analyze": "analyze_task",
                "discover": "discover_components",
                "activate": "activate_components",
                "execute": "execute_task",
                "end": END,
            },
        )

        # Connect other nodes
        graph.add_edge("analyze_task", "supervisor")
        graph.add_edge("discover_components", "supervisor")
        graph.add_edge("activate_components", "supervisor")
        graph.add_edge("execute_task", END)

        # Set entry point
        graph.set_entry_point("supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: DynamicActivationState) -> dict[str, Any]:
        """Main supervisor logic node."""
        # Update current task
        if hasattr(state, "messages") and state.messages:
            latest_message = state.messages[-1]
            if hasattr(latest_message, "content"):
                state.current_task = latest_message.content

        # Determine next action based on state
        if not state.current_task:
            return {"next_action": "end", "reason": "No task to process"}

        # Check if we need to analyze the task
        if not state.required_capabilities:
            return {
                "next_action": "analyze",
                "reason": "Need to analyze task requirements",
            }

        # Check if we have missing capabilities
        if state.missing_capabilities:
            # Check if we have components to activate
            registry_items = state.registry.list_components()
            if registry_items:
                return {
                    "next_action": "activate",
                    "reason": "Have components to activate",
                }
            return {
                "next_action": "discover",
                "reason": "Need to discover components",
            }

        # All capabilities satisfied, execute task
        return {"next_action": "execute", "reason": "Ready to execute task"}

    async def _analyze_task_node(self, state: DynamicActivationState) -> dict[str, Any]:
        """Analyze task requirements and update state."""
        # Use LLM to analyze task requirements
        analysis_prompt = f"""
        Analyze this task and identify required capabilities:

        Task: {state.current_task}

        Identify what types of tools, agents, or components would be needed.
        Consider capabilities like: math, search, visualization, file_processing, data_processing, etc.

        Return a list of required capabilities.
        """

        # Execute through meta state for tracking
        result = await self._meta_self.execute_agent(
            input_data=analysis_prompt, update_state=True
        )

        # Parse capabilities from result
        capabilities = self._parse_capabilities(result.get("output", ""))

        # Update state
        state.update_capabilities(required=capabilities)

        return {"capabilities_identified": capabilities, "analysis_complete": True}

    async def _discover_components_node(
        self, state: DynamicActivationState
    ) -> dict[str, Any]:
        """Discover components for missing capabilities."""
        discovered_components = []

        for capability in state.missing_capabilities:
            if self._discovery_agent:
                # Use discovery agent
                components = await self._discovery_agent.discover_components(
                    f"components for {capability}"
                )
                discovered_components.extend(components)

        # Register discovered components
        for comp_data in discovered_components:
            # For now, just register the component data
            # In a real implementation, you'd load the actual component
            item = RegistryItem(
                id=comp_data.get("id", comp_data.get("name", "unknown")),
                name=comp_data.get("name", "Unknown Component"),
                description=comp_data.get("description", ""),
                component=comp_data,  # Store component data for now
            )
            state.registry.register(item)

        return {
            "components_discovered": len(discovered_components),
            "discovery_complete": True,
        }

    async def _activate_components_node(
        self, state: DynamicActivationState
    ) -> dict[str, Any]:
        """Activate components to satisfy missing capabilities."""
        activated_components = []

        # Try to activate components for each missing capability
        for capability in state.missing_capabilities.copy():
            # Find components that can satisfy this capability
            for item_id in state.registry.list_components():
                item = state.registry.get_item(item_id)
                if item and not item.is_active:
                    # Simple matching - check if capability is in description
                    if (
                        capability in item.description.lower()
                        or capability in item.name.lower()
                    ):
                        meta_state = state.activate_component(item_id)
                        if meta_state:
                            activated_components.append(item_id)
                            state.mark_capability_satisfied(capability)
                            break

        return {
            "components_activated": activated_components,
            "activation_complete": True,
        }

    async def _execute_task_node(self, state: DynamicActivationState) -> dict[str, Any]:
        """Execute the task using active components."""
        # Get active components
        active_components = state.get_active_components()

        if not active_components:
            return {
                "execution_result": "No active components available for task execution",
                "success": False,
            }

        # Execute task through LLM with available components
        execution_prompt = f"""
        Execute this task using the available components:

        Task: {state.current_task}

        Available components:
        {[str(comp) for comp in active_components]}

        Provide a step-by-step execution plan and result.
        """

        # Execute through meta state
        result = await self._meta_self.execute_agent(
            input_data=execution_prompt, update_state=True
        )

        return {
            "execution_result": result.get("output", ""),
            "components_used": len(active_components),
            "success": True,
        }

    def _route_supervisor(self, state: DynamicActivationState) -> str:
        """Route supervisor based on state."""
        # Check the next_action set by supervisor_node
        next_action = getattr(state, "next_action", "end")

        action_map = {
            "analyze": "analyze",
            "discover": "discover",
            "activate": "activate",
            "execute": "execute",
            "end": "end",
        }

        return action_map.get(next_action, "end")

    def _parse_capabilities(self, output: str) -> list[str]:
        """Parse capabilities from LLM output."""
        capabilities = []

        # Simple parsing - look for capability keywords
        capability_keywords = [
            "math",
            "calculation",
            "compute",
            "search",
            "web",
            "lookup",
            "visualization",
            "chart",
            "plot",
            "file",
            "processing",
            "data",
            "text",
            "analysis",
            "nlp",
        ]

        output_lower = output.lower()
        for key in capability_keywords:
            if key in output_lower:
                capabilities.append(key)

        return list(set(capabilities))  # Remove duplicates

    def get_registry_stats(self) -> dict[str, Any]:
        """Get statistics about the component registry.

        Returns:
            Dictionary with registry statistics

        Examples:
            Check registry status::

                stats = supervisor.get_registry_stats()
                print(f"Total components: {stats['total_components']}")
                print(f"Active components: {stats['active_components']}")
        """
        return self.state.get_activation_stats()

    async def activate_component_by_name(self, name: str) -> bool:
        """Activate a component by name.

        Args:
            name: Name of component to activate

        Returns:
            True if activation succeeded

        Examples:
            Activate specific component::

                success = await supervisor.activate_component_by_name("calculator")
                if success:
                    print("Calculator activated successfully")
        """
        # Find component by name
        for item_id in self.state.registry.list_components():
            item = self.state.registry.get_item(item_id)
            if item and item.name.lower() == name.lower():
                meta_state = self.state.activate_component(item_id)
                return meta_state is not None

        return False

    def get_active_component_names(self) -> list[str]:
        """Get names of all active components.

        Returns:
            List of active component names

        Examples:
            List active components::

                active_names = supervisor.get_active_component_names()
                print(f"Active components: {', '.join(active_names)}")
        """
        active_items = self.state.registry.get_active_items()
        return [item.name for item in active_items]
