"""Debug the validation bypass issue."""

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def debug_setattr_bypass():
    """Debug why our validation bypass isn't working."""
    print("🔍 Debugging Validation Bypass...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)

    print(f"\nState setup:")
    print(f"  agents: {list(state.agents.keys())}")
    print(f"  current next_agent: {state.next_agent}")

    # Test different bypass approaches
    print(f"\n🧪 Testing different bypass approaches...")

    # Approach 1: super() bypass (what we tried)
    print(f"\nApproach 1: super().__setattr__")
    try:
        super(SupervisorStateWithTools, state).__setattr__(
            "next_agent", "nonexistent_agent"
        )
        print(f"✅ super() bypass worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ super() bypass failed: {e}")

    # Approach 2: object.__setattr__
    print(f"\nApproach 2: object.__setattr__")
    try:
        object.__setattr__(state, "next_agent", "nonexistent_agent")
        print(f"✅ object.__setattr__ worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ object.__setattr__ failed: {e}")

    # Approach 3: __dict__ access
    print(f"\nApproach 3: __dict__ access")
    try:
        state.__dict__["next_agent"] = "nonexistent_agent"
        print(f"✅ __dict__ access worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ __dict__ access failed: {e}")

    # Approach 4: Disable validation temporarily
    print(f"\nApproach 4: Disable validation")
    try:
        # Temporarily disable validation
        original_config = state.model_config
        state.model_config = {}  # Remove validate_assignment
        state.next_agent = "nonexistent_agent"
        state.model_config = original_config  # Restore
        print(f"✅ Disable validation worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ Disable validation failed: {e}")

    # Approach 5: Check what type of validation is happening
    print(f"\nApproach 5: Check validation details")
    try:
        print(f"  model_config: {state.model_config}")
        print(
            f"  Has validate_assignment: {'validate_assignment' in state.model_config}"
        )
        print(
            f"  validate_assignment value: {state.model_config.get('validate_assignment')}"
        )

        # Try to understand the validation chain
        state.next_agent = "search_agent"  # Valid assignment
        print(f"  Valid assignment works: {state.next_agent}")

    except Exception as e:
        print(f"❌ Check validation failed: {e}")


if __name__ == "__main__":
    debug_setattr_bypass()
