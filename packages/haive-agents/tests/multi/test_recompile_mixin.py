"""Test RecompileMixin that adds recompilation support to any state schema.

This follows the pattern of MetaStateSchema but adds recompilation tracking.
"""

from typing import Any, Dict, List, Optional, Set

from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from pydantic import Field, model_validator


class RecompileMixin:
    """Mixin that adds recompilation support to any state schema."""

    # Recompilation tracking fields
    needs_recompile: bool = Field(
        default=False, description="Whether the state needs recompilation"
    )

    recompile_reason: str | None = Field(
        default=None, description="Reason why recompilation is needed"
    )

    fields_changed: set[str] = Field(
        default_factory=set,
        description="Set of field names that changed and triggered recompilation",
    )

    recompile_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of recompilation events"
    )

    def mark_for_recompile(self, reason: str, changed_fields: set[str] | None = None):
        """Mark this state as needing recompilation."""
        self.needs_recompile = True
        self.recompile_reason = reason
        if changed_fields:
            self.fields_changed.update(changed_fields)

        # Add to history
        import datetime

        self.recompile_history.append(
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "reason": reason,
                "changed_fields": list(changed_fields) if changed_fields else [],
            }
        )

    def clear_recompile_flag(self):
        """Clear the recompilation flag after recompilation is complete."""
        self.needs_recompile = False
        self.recompile_reason = None
        self.fields_changed.clear()


class RecompileMetaState(MetaStateSchema, RecompileMixin):
    """MetaStateSchema with recompilation support.

    This extends MetaStateSchema to add recompilation tracking for any generic agent.
    """

    @model_validator(mode="after")
    def setup_recompile_tracking(self) -> "RecompileMetaState":
        """Set up recompilation tracking after MetaStateSchema setup."""
        # Call parent setup first
        super().setup_agent_integration()

        # Add recompilation-specific setup
        if self.agent is not None:
            # Check if agent state has changed and needs recompilation
            if hasattr(self.agent, "state_schema"):
                try:
                    current_state = self.agent.state_schema()
                    current_dump = current_state.model_dump()

                    # If we have previous state, compare for changes
                    if self.agent_state and self.agent_state != current_dump:
                        changed_fields = set()
                        for key in current_dump:
                            if (
                                key not in self.agent_state
                                or self.agent_state[key] != current_dump[key]
                            ):
                                changed_fields.add(key)

                        if changed_fields:
                            self.mark_for_recompile(
                                "Agent state changed", changed_fields
                            )

                    # Update our cached state
                    self.agent_state = current_dump

                except Exception as e:
                    # Log but don't fail
                    from haive.core.logging.rich_logger import get_logger

                    logger = get_logger(__name__)
                    logger.debug(f"Could not check for state changes: {e}")

        return self


def test_recompile_mixin():
    """Test the RecompileMixin with any generic agent."""
    from haive.core.engine.aug_llm import AugLLMConfig

    from haive.agents.simple.agent import SimpleAgent

    # Create any agent - don't define model in AugLLMConfig
    config = AugLLMConfig()  # Use defaults
    agent = SimpleAgent(engine=config)

    # Create recompile meta state
    meta_state = RecompileMetaState(agent=agent)

    # Test manual recompilation marking
    meta_state.mark_for_recompile("Manual test", {"messages", "context"})

    # Test clearing flag
    meta_state.clear_recompile_flag()


if __name__ == "__main__":
    test_recompile_mixin()
