"""Debug the field validator to understand info.data access."""

from typing import Optional

from pydantic import Field, ValidationInfo, field_validator

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def test_validator_access():
    """Test what info.data contains during validation."""

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)


    # Create a custom debug validator to see what we get
    class DebugState(SupervisorStateWithTools):
        @field_validator("next_agent")
        @classmethod
        def debug_validate_chosen_agent(
            cls, v: str | None, info: ValidationInfo
        ) -> str | None:

            if info.data:
                if hasattr(info.data, "agents"):
                    pass
                else:
                    pass

            # Return value unchanged for debugging
            return v

    # Test with debug validator
    debug_state = DebugState()
    debug_state.add_agent("search_agent", agents["search_agent"], "Test", True)

    try:
        debug_state.next_agent = "search_agent"
    except Exception as e:
        pass")


if __name__ == "__main__":
    test_validator_access()
