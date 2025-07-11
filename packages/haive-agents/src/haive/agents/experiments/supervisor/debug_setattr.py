"""Debug the validation bypass issue."""

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def debug_setattr_bypass():
    """Debug why our validation bypass isn't working."""

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)


    # Test different bypass approaches

    # Approach 1: super() bypass (what we tried)
    try:
        super(SupervisorStateWithTools, state).__setattr__(
            "next_agent", "nonexistent_agent"
        )
    except Exception as e:
        pass")

    # Approach 2: object.__setattr__
    try:
        object.__setattr__(state, "next_agent", "nonexistent_agent")
    except Exception as e:
        pass")

    # Approach 3: __dict__ access
    try:
        state.__dict__["next_agent"] = "nonexistent_agent"
    except Exception as e:
        pass")

    # Approach 4: Disable validation temporarily
    try:
        # Temporarily disable validation
        original_config = state.model_config
        state.model_config = {}  # Remove validate_assignment
        state.next_agent = "nonexistent_agent"
        state.model_config = original_config  # Restore
    except Exception as e:
        pass")

    # Approach 5: Check what type of validation is happening
    try:

        # Try to understand the validation chain
        state.next_agent = "search_agent"  # Valid assignment

    except Exception as e:
        pass")


if __name__ == "__main__":
    debug_setattr_bypass()
