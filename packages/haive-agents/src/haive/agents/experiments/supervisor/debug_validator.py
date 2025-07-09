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
    print("🔍 Debugging Field Validator Access...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)

    print(f"\nState setup complete:")
    print(f"  state.agents keys: {list(state.agents.keys())}")
    print(f"  state.agents dict: {state.agents}")

    # Create a custom debug validator to see what we get
    class DebugState(SupervisorStateWithTools):
        @field_validator("next_agent")
        @classmethod
        def debug_validate_chosen_agent(
            cls, v: Optional[str], info: ValidationInfo
        ) -> Optional[str]:
            print(f"\n🔍 VALIDATOR DEBUG:")
            print(f"  Input value: {v}")
            print(f"  info type: {type(info)}")
            print(f"  info.data type: {type(info.data)}")
            print(f"  info.data: {info.data}")

            if info.data:
                print(f"  info.data attributes: {dir(info.data)}")
                if hasattr(info.data, "agents"):
                    print(
                        f"  info.data.agents: {info.data.get('agents', 'NO AGENTS KEY')}"
                    )
                else:
                    print(f"  info.data has no agents attribute")

            # Return value unchanged for debugging
            return v

    # Test with debug validator
    debug_state = DebugState()
    debug_state.add_agent("search_agent", agents["search_agent"], "Test", True)

    print(f"\n🧪 Testing debug state assignment...")
    try:
        debug_state.next_agent = "search_agent"
        print(f"✅ Assignment worked")
    except Exception as e:
        print(f"❌ Assignment failed: {e}")


if __name__ == "__main__":
    test_validator_access()
