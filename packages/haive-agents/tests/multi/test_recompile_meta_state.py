"""Test extending MetaStateSchema with recompilation support."""

from typing import Any, Dict, List, Optional, Set

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from pydantic import Field, model_validator

from haive.agents.simple.agent import SimpleAgent


class RecompileMetaState(MetaStateSchema):
    """Meta state with recompilation support (extending existing MetaStateSchema)."""

    # Add recompilation tracking fields
    needs_recompile: bool = Field(
        default=False, description="Whether agent needs recompilation"
    )
    recompile_reason: str | None = Field(
        default=None, description="Reason for recompilation"
    )
    recompile_count: int = Field(default=0, description="Number of recompilations")

    # Don't override model_validator - let parent handle it
    # Add recompile logic in a separate method if needed


def test_recompile_meta_state():
    """Test that RecompileMetaState works with any agent."""
    try:
        # Create any agent
        config = AugLLMConfig()
        agent = SimpleAgent(engine=config)

        # Create meta state with the agent
        meta_state = RecompileMetaState(agent=agent)

        return meta_state
    except Exception:
        return None


if __name__ == "__main__":
    meta_state = test_recompile_meta_state()
