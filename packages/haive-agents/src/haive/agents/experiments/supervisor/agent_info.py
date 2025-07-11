"""AgentInfo class for holding agent metadata and instance."""

from typing import Any

from pydantic import BaseModel, Field, model_validator


class AgentInfo(BaseModel):
    """Information about an agent including the agent instance and metadata."""

    agent: Any = Field(..., description="The actual agent instance", exclude=True)
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="What the agent is good at or used for")
    active: bool = Field(default=True, description="Whether agent is currently active")

    # Store serializable agent metadata
    agent_metadata: dict = Field(
        default_factory=dict, description="Serializable agent metadata"
    )

    model_config = {"arbitrary_types_allowed": True}  # Allow agent instances

    @model_validator(mode="after")
    def extract_agent_info(self):
        """Extract name and description from agent if not provided."""
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

        return self

    def get_agent(self) -> Any:
        """Get the agent instance."""
        return self.agent

    def is_active(self) -> bool:
        """Check if agent is active."""
        return self.active

    def activate(self):
        """Activate the agent."""
        self.active = True

    def deactivate(self):
        """Deactivate the agent."""
        self.active = False
