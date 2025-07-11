"""Data models for dynamic supervisor agent.

This module contains Pydantic models used by the dynamic supervisor for
agent metadata, routing information, and configuration.

Classes:
    AgentInfo: Metadata container for agents (v1 with exclusion)
    AgentInfoV2: Experimental version with full serialization
    AgentRequest: Model for agent addition requests
    RoutingDecision: Model for routing decisions

Example:
    Creating agent metadata::

        info = AgentInfo(
            agent=search_agent,
            name="search",
            description="Web search specialist",
            active=True
        )
"""

from typing import Any

from pydantic import BaseModel, Field, field_serializer, model_validator


class AgentInfo(BaseModel):
    """Information about an agent including instance and metadata.

    This model stores agent metadata and the agent instance itself. The agent
    field is excluded from serialization to avoid msgpack serialization issues
    with complex objects.

    Attributes:
        agent: The actual agent instance (excluded from serialization)
        name: Unique identifier for the agent
        description: Human-readable description of capabilities
        active: Whether the agent is currently active
        capabilities: List of capability keywords for discovery
        metadata: Additional metadata (versions, config, etc.)

    Example:
        Creating agent info::

            info = AgentInfo(
                agent=math_agent,
                name="math",
                description="Mathematics and calculation expert",
                capabilities=["math", "calculation", "statistics"]
            )
    """

    agent: Any = Field(
        ...,
        description="The actual agent instance",
        exclude=True,  # Critical: Exclude from serialization!
    )
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="What the agent is good at or used for")
    active: bool = Field(default=True, description="Whether agent is currently active")
    capabilities: list[str] = Field(
        default_factory=list,
        description="List of capability keywords (e.g., 'search', 'math', 'code')",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the agent"
    )

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def extract_agent_info(self) -> "AgentInfo":
        """Extract name and description from agent if not provided.

        Returns:
            Self with extracted information
        """
        # If name not provided, try to get from agent
        if not self.name and hasattr(self.agent, "name"):
            self.name = self.agent.name

        # If description not provided, try to get from agent or engine
        if not self.description:
            if hasattr(self.agent, "description"):
                self.description = self.agent.description
            elif hasattr(self.agent, "engine") and hasattr(
                self.agent.engine, "system_message"
            ):
                self.description = (
                    self.agent.engine.system_message or "Agent specialist"
                )
            else:
                self.description = f"{self.name} specialist"

        # Extract capabilities from description if not provided
        if not self.capabilities and self.description:
            # Simple keyword extraction
            keywords = [
                "search",
                "math",
                "code",
                "translate",
                "analyze",
                "summarize",
                "write",
                "plan",
                "research",
            ]
            desc_lower = self.description.lower()
            self.capabilities = [kw for kw in keywords if kw in desc_lower]

        return self

    def get_agent(self) -> Any:
        """Get the agent instance.

        Returns:
            The agent instance
        """
        return self.agent

    def is_active(self) -> bool:
        """Check if agent is active.

        Returns:
            True if active, False otherwise
        """
        return self.active

    def activate(self) -> None:
        """Activate the agent."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.active = False

    def matches_capability(self, required: str) -> bool:
        """Check if agent has a required capability.

        Args:
            required: Capability keyword to check

        Returns:
            True if agent has the capability
        """
        required_lower = required.lower()
        return any(
            cap.lower() in required_lower or required_lower in cap.lower()
            for cap in self.capabilities
        )


class AgentInfoV2(BaseModel):
    """Experimental version with full agent serialization.

    This version attempts to serialize the agent object. Requires custom
    serialization logic or agents that support model_dump().

    Warning:
        Experimental - may not work with all agent types.
    """

    agent: Any = Field(..., description="The actual agent instance")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    active: bool = Field(default=True)
    capabilities: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}

    @field_serializer("agent")
    def serialize_agent(self, agent: Any) -> dict[str, Any]:
        """Attempt to serialize agent to dict.

        Args:
            agent: Agent instance

        Returns:
            Serialized representation
        """
        if hasattr(agent, "model_dump"):
            return agent.model_dump()
        if hasattr(agent, "dict"):
            return agent.dict()
        # Fallback: Store type and config info
        return {
            "type": type(agent).__name__,
            "module": type(agent).__module__,
            "name": getattr(agent, "name", "unknown"),
            "config": getattr(agent, "config", {}),
        }


class AgentRequest(BaseModel):
    """Model for requesting a new agent be added.

    Used when the supervisor identifies a missing capability and needs
    to request a new agent from an agent builder or registry.

    Attributes:
        capability: The required capability (e.g., "translation", "code_analysis")
        task_context: Context about what task needs this capability
        suggested_name: Suggested name for the new agent
        requirements: Specific requirements or constraints

    Example:
        Requesting a new agent::

            request = AgentRequest(
                capability="translation",
                task_context="Need to translate search results to French",
                suggested_name="translator",
                requirements=["Support French", "Maintain formatting"]
            )
    """

    capability: str = Field(
        ..., description="Required capability (e.g., 'translation', 'math')"
    )
    task_context: str = Field(
        ..., description="Context about why this capability is needed"
    )
    suggested_name: str | None = Field(
        default=None, description="Suggested name for the new agent"
    )
    requirements: list[str] = Field(
        default_factory=list, description="Specific requirements or constraints"
    )
    priority: str = Field(
        default="medium", description="Priority level: low, medium, high"
    )


class RoutingDecision(BaseModel):
    """Model for supervisor routing decisions.

    Represents a decision made by the supervisor about which agent
    to route to or what action to take.

    Attributes:
        agent_name: Name of agent to route to (or "END")
        task: Task to give to the agent
        reasoning: Explanation of the routing decision
        confidence: Confidence level in the decision (0-1)
        alternatives: Other agents that could handle this
    """

    agent_name: str = Field(..., description="Agent to route to or 'END'")
    task: str = Field(default="", description="Task for the agent")
    reasoning: str = Field(default="", description="Explanation of routing decision")
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence in decision"
    )
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative agents that could handle this"
    )
