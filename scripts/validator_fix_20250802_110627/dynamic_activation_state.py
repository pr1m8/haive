"""Dynamic Activation State for Component Management.

This module provides DynamicActivationState, a specialized state schema for
dynamic component activation patterns. It extends StateSchema with registry
management, MetaStateSchema integration, and activation tracking.

Based on the Dynamic Activation Pattern:
@project_docs/active/patterns/dynamic_activation_pattern.md
"""

from datetime import datetime
from typing import Any, Self, TypeVar

from haive.core.registry import DynamicRegistry
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from haive.core.schema.state_schema import StateSchema
from pydantic import Field, field_validator, model_validator

T = TypeVar("T")


class DynamicActivationState(StateSchema):
    """State schema for dynamic component activation patterns.

    This state schema provides the foundation for dynamic component activation
    using MetaStateSchema for component wrapping and DynamicRegistry for
    component management. It supports discovery, activation, and tracking
    of components with full type safety.

    Key Features:
        - Generic component registry with activation tracking
        - MetaStateSchema integration for component wrapping
        - Discovery configuration for component finding
        - Activation history with detailed tracking
        - Component lifecycle management
        - Type-safe component access

    Args:
        registry: Registry of available components
        active_meta_states: MetaStateSchema instances for active components
        discovery_config: Configuration for component discovery
        activation_history: History of activation/deactivation events
        current_task: Current task being processed
        required_capabilities: Capabilities needed for current task
        missing_capabilities: Capabilities currently missing

    Examples:
        Basic usage::

            from haive.core.schema.prebuilt.dynamic_activation_state import DynamicActivationState
            from haive.core.registry import DynamicRegistry, RegistryItem
            from langchain_core.tools import tool

            @tool
            def calculator(expression: str) -> float:
                '''Calculate mathematical expression.'''
                return eval(expression)

            # Create state with registry
            state = DynamicActivationState()

            # Register a component
            item = RegistryItem(
                id="calc",
                name="calculator",
                description="Math operations",
                component=calculator
            )
            state.registry.register(item)

            # Activate component
            meta_state = state.activate_component("calc")
            assert meta_state is not None

        With discovery configuration::

            state = DynamicActivationState(
                discovery_config={
                    "source": "@haive-tools/docs",
                    "auto_discover": True,
                    "query": "math tools"
                }
            )

            # Track required capabilities
            state.required_capabilities = ["math", "calculation"]
            state.missing_capabilities = ["math"]

            # Activate component to fill capability gap
            meta_state = state.activate_component("calc")
            state.missing_capabilities.remove("math")

        With activation history::

            # Check activation history
            recent_activations = [
                event for event in state.activation_history
                if event["action"] == "activate"
            ]

            print(f"Recent activations: {len(recent_activations)}")
            for event in recent_activations[-3:]:
                print(f"- {event['component_name']} at {event['timestamp']}")
    """

    registry: DynamicRegistry = Field(
        default_factory=DynamicRegistry, description="Registry of available components"
    )
    active_meta_states: dict[str, MetaStateSchema] = Field(
        default_factory=dict,
        description="MetaStateSchema instances for active components",
    )
    discovery_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for component discovery"
    )
    activation_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of activation/deactivation events"
    )
    current_task: str = Field(default="", description="Current task being processed")
    required_capabilities: list[str] = Field(
        default_factory=list, description="Capabilities needed for current task"
    )
    missing_capabilities: list[str] = Field(
        default_factory=list, description="Capabilities currently missing"
    )
    execution_context: dict[str, Any] = Field(
        default_factory=dict, description="Current execution context and metadata"
    )
    __shared_fields__ = [
        "active_meta_states",
        "activation_history",
        "execution_context",
    ]
    __reducer_fields__ = {
        "activation_history": lambda a, b: (a or []) + (b or []),
        "execution_context": lambda a, b: {**(a or {}), **(b or {})},
        "discovery_config": lambda a, b: {**(a or {}), **(b or {})},
    }

    @field_validator("current_task")
    def validate_current_task(cls, v: str) -> str:
        """Validate current task is properly formatted."""
        return v.strip()

    @field_validator("required_capabilities")
    def validate_required_capabilities(cls, v: list[str]) -> list[str]:
        """Validate required capabilities list."""
        return [cap.strip().lower() for cap in v if cap.strip()]

    @field_validator("missing_capabilities")
    def validate_missing_capabilities(cls, v: list[str]) -> list[str]:
        """Validate missing capabilities list."""
        return [cap.strip().lower() for cap in v if cap.strip()]

    @model_validator(mode="after")
    def setup_dynamic_activation(self) -> Self:
        """Setup dynamic activation state after model creation.

        This validator:
        1. Initializes discovery configuration if empty
        2. Sets up execution context
        3. Validates capability consistency
        4. Initializes tracking systems
        """
        if not self.discovery_config:
            self.discovery_config = {
                "auto_discover": False,
                "max_discoveries": 10,
                "discovery_timeout": 30,
                "created_at": str(datetime.now()),
            }
        if not self.execution_context:
            self.execution_context = {
                "created_at": str(datetime.now()),
                "activation_mode": "dynamic",
                "state_version": "1.0",
            }
        if self.missing_capabilities:
            self.missing_capabilities = [
                cap
                for cap in self.missing_capabilities
                if cap in self.required_capabilities
            ]
        if self.active_meta_states:
            self.execution_context["active_components"] = len(self.active_meta_states)
        return self

    def activate_component(self, component_id: str) -> MetaStateSchema | None:
        """Activate a component and wrap in MetaStateSchema.

        Args:
            component_id: ID of component to activate

        Returns:
            MetaStateSchema instance if activation succeeded, None otherwise

        Examples:
            Activate a registered component::

                # Register component first
                item = RegistryItem(
                    id="my_tool",
                    name="My Tool",
                    description="Useful tool",
                    component=tool_instance
                )
                state.registry.register(item)

                # Activate component
                meta_state = state.activate_component("my_tool")
                if meta_state:
                    print(f"Component {component_id} activated successfully")

            Check activation result::

                meta_state = state.activate_component("calculator")
                if meta_state:
                    # Use the wrapped component
                    result = await meta_state.execute_agent(
                        input_data={"expression": "2 + 2"}
                    )
                    print(f"Result: {result}")
        """
        if self.registry.activate(component_id):
            item = self.registry.items[component_id]
            meta_state = MetaStateSchema(
                agent=item.component,
                agent_state={"activated_at": str(datetime.now())},
                graph_context={
                    "registry_id": component_id,
                    "activation_reason": "dynamic_activation",
                    "component_name": item.name,
                    "component_description": item.description,
                },
            )
            self.active_meta_states[component_id] = meta_state
            self.activation_history.append(
                {
                    "timestamp": str(datetime.now()),
                    "action": "activate",
                    "component_id": component_id,
                    "component_name": item.name,
                    "component_type": type(item.component).__name__,
                    "activation_count": item.activation_count,
                    "total_active": len(self.active_meta_states),
                }
            )
            self.execution_context["last_activation"] = str(datetime.now())
            self.execution_context["active_components"] = len(self.active_meta_states)
            return meta_state
        return None

    def deactivate_component(self, component_id: str) -> bool:
        """Deactivate a component and remove from active states.

        Args:
            component_id: ID of component to deactivate

        Returns:
            True if deactivation succeeded, False otherwise

        Examples:
            Deactivate a component::

                success = state.deactivate_component("my_tool")
                if success:
                    print("Component deactivated successfully")

            Deactivate all components::

                active_ids = list(state.active_meta_states.keys())
                for comp_id in active_ids:
                    state.deactivate_component(comp_id)

                assert len(state.active_meta_states) == 0
        """
        if self.registry.deactivate(component_id):
            if component_id in self.active_meta_states:
                del self.active_meta_states[component_id]
            item = self.registry.items.get(component_id)
            if item:
                self.activation_history.append(
                    {
                        "timestamp": str(datetime.now()),
                        "action": "deactivate",
                        "component_id": component_id,
                        "component_name": item.name,
                        "component_type": type(item.component).__name__,
                        "total_active": len(self.active_meta_states),
                    }
                )
            self.execution_context["last_deactivation"] = str(datetime.now())
            self.execution_context["active_components"] = len(self.active_meta_states)
            return True
        return False

    def get_active_components(self) -> list[Any]:
        """Get all active component instances.

        Returns:
            List of active component instances

        Examples:
            Get active components::

                active_components = state.get_active_components()
                print(f"Active components: {len(active_components)}")

                for component in active_components:
                    print(f"- {type(component).__name__}")

            Use active components::

                tools = state.get_active_components()
                for tool in tools:
                    if hasattr(tool, 'invoke'):
                        result = tool.invoke({"input": "test"})
        """
        return self.registry.get_active_components()

    def get_meta_state(self, component_id: str) -> MetaStateSchema | None:
        """Get MetaStateSchema for a specific component.

        Args:
            component_id: ID of component to get meta state for

        Returns:
            MetaStateSchema instance if found, None otherwise

        Examples:
            Get meta state for execution::

                meta_state = state.get_meta_state("calculator")
                if meta_state:
                    result = await meta_state.execute_agent(
                        input_data={"expression": "10 * 5"}
                    )
                    print(f"Calculation result: {result}")
        """
        return self.active_meta_states.get(component_id)

    def update_capabilities(
        self, required: list[str], missing: list[str] | None = None
    ) -> None:
        """Update required and missing capabilities.

        Args:
            required: List of required capabilities
            missing: List of missing capabilities (defaults to copy of required)

        Examples:
            Update capabilities for new task::

                state.update_capabilities(
                    required=["math", "visualization", "data_processing"],
                    missing=["visualization", "data_processing"]
                )

            Auto-detect missing capabilities::

                state.update_capabilities(
                    required=["math", "web_search", "file_processing"]
                )
                # missing will be set to all required capabilities
        """
        self.required_capabilities = [
            cap.strip().lower() for cap in required if cap.strip()
        ]
        if missing is None:
            self.missing_capabilities = self.required_capabilities.copy()
        else:
            self.missing_capabilities = [
                cap.strip().lower() for cap in missing if cap.strip()
            ]
        self.execution_context["capabilities_updated"] = str(datetime.now())
        self.execution_context["required_count"] = len(self.required_capabilities)
        self.execution_context["missing_count"] = len(self.missing_capabilities)

    def mark_capability_satisfied(self, capability: str) -> bool:
        """Mark a capability as satisfied (remove from missing).

        Args:
            capability: Name of capability that was satisfied

        Returns:
            True if capability was removed from missing, False otherwise

        Examples:
            Mark capability as satisfied after activation::

                # Activate math tool
                meta_state = state.activate_component("calculator")
                if meta_state:
                    # Mark math capability as satisfied
                    state.mark_capability_satisfied("math")

            Check satisfaction status::

                if state.mark_capability_satisfied("web_search"):
                    print("Web search capability now satisfied")
                else:
                    print("Web search was not in missing capabilities")
        """
        capability = capability.strip().lower()
        if capability in self.missing_capabilities:
            self.missing_capabilities.remove(capability)
            self.activation_history.append(
                {
                    "timestamp": str(datetime.now()),
                    "action": "capability_satisfied",
                    "capability": capability,
                    "remaining_missing": len(self.missing_capabilities),
                }
            )
            return True
        return False

    def get_activation_stats(self) -> dict[str, Any]:
        """Get statistics about component activation.

        Returns:
            Dictionary with activation statistics

        Examples:
            Show activation statistics::

                stats = state.get_activation_stats()
                print(f"Total components: {stats['total_components']}")
                print(f"Active components: {stats['active_components']}")
                print(f"Activation rate: {stats['activation_rate']:.1%}")
                print(f"Most activated: {stats['most_activated_component']}")
        """
        registry_stats = self.registry.get_stats()
        activations = sum(
            (1 for event in self.activation_history if event["action"] == "activate")
        )
        deactivations = sum(
            (1 for event in self.activation_history if event["action"] == "deactivate")
        )
        return {
            **registry_stats,
            "meta_states_active": len(self.active_meta_states),
            "total_activation_events": activations,
            "total_deactivation_events": deactivations,
            "net_activations": activations - deactivations,
            "capabilities_required": len(self.required_capabilities),
            "capabilities_missing": len(self.missing_capabilities),
            "capability_satisfaction_rate": (
                (len(self.required_capabilities) - len(self.missing_capabilities))
                / len(self.required_capabilities)
                if self.required_capabilities
                else 1.0
            ),
            "current_task": self.current_task,
            "discovery_enabled": self.discovery_config.get("auto_discover", False),
        }

    def is_capability_satisfied(self, capability: str) -> bool:
        """Check if a capability is satisfied.

        Args:
            capability: Name of capability to check

        Returns:
            True if capability is satisfied (not in missing), False otherwise

        Examples:
            Check capability status::

                if state.is_capability_satisfied("math"):
                    print("Math capability is available")
                else:
                    print("Need to activate math tool")
        """
        capability = capability.strip().lower()
        return (
            capability in self.required_capabilities
            and capability not in self.missing_capabilities
        )

    def get_unsatisfied_capabilities(self) -> list[str]:
        """Get list of capabilities that are still unsatisfied.

        Returns:
            List of capability names that are still missing

        Examples:
            Check what capabilities are still needed::

                unsatisfied = state.get_unsatisfied_capabilities()
                if unsatisfied:
                    print(f"Still need: {', '.join(unsatisfied)}")
                else:
                    print("All capabilities satisfied!")
        """
        return self.missing_capabilities.copy()

    def reset_state(self) -> None:
        """Reset the activation state to initial values.

        Examples:
            Reset state for new task::

                # Clear previous state
                state.reset_state()

                # Set up for new task
                state.current_task = "new task"
                state.required_capabilities = ["new", "capabilities"]
        """
        active_ids = list(self.active_meta_states.keys())
        for comp_id in active_ids:
            self.deactivate_component(comp_id)
        self.current_task = ""
        self.required_capabilities = []
        self.missing_capabilities = []
        created_at = self.execution_context.get("created_at")
        self.execution_context = {
            "created_at": created_at or str(datetime.now()),
            "reset_at": str(datetime.now()),
            "activation_mode": "dynamic",
            "state_version": "1.0",
        }
        self.activation_history.append(
            {
                "timestamp": str(datetime.now()),
                "action": "reset",
                "details": {"full_reset": True},
            }
        )
