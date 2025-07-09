"""Debug import issue - maybe it's comparing different AgentInfo classes."""

import sys


def test_import_paths():
    """Check if we have import path issues."""
    print("\n=== Import Path Debug ===\n")

    # Import AgentInfo two ways
    from agent_info import AgentInfo as AgentInfo1

    from haive.agents.experiments.supervisor.agent_info import AgentInfo as AgentInfo2

    print(f"1. Import comparison:")
    print(f"   agent_info.AgentInfo: {AgentInfo1}")
    print(f"   Full path AgentInfo: {AgentInfo2}")
    print(f"   Same class? {AgentInfo1 is AgentInfo2}")
    print(f"   Same module? {AgentInfo1.__module__ == AgentInfo2.__module__}")

    # Create instances
    class DummyAgent:
        name = "dummy"

    agent = DummyAgent()

    info1 = AgentInfo1(agent=agent, name="test", description="Test")
    info2 = AgentInfo2(agent=agent, name="test", description="Test")

    print(f"\n2. Instance comparison:")
    print(f"   info1 type: {type(info1)}")
    print(f"   info2 type: {type(info2)}")
    print(f"   isinstance(info1, AgentInfo1): {isinstance(info1, AgentInfo1)}")
    print(f"   isinstance(info1, AgentInfo2): {isinstance(info1, AgentInfo2)}")
    print(f"   isinstance(info2, AgentInfo1): {isinstance(info2, AgentInfo1)}")
    print(f"   isinstance(info2, AgentInfo2): {isinstance(info2, AgentInfo2)}")

    # Now test with SupervisorState using different imports
    print(f"\n3. Testing with SupervisorState:")

    from supervisor_state import SupervisorState

    try:
        state1 = SupervisorState(agents={"test": info1})
        print("   ✅ Works with relative import AgentInfo")
    except Exception as e:
        print(f"   ❌ Failed with relative import: {e}")

    try:
        state2 = SupervisorState(agents={"test": info2})
        print("   ✅ Works with full import AgentInfo")
    except Exception as e:
        print(f"   ❌ Failed with full import: {e}")

    # Check what SupervisorState expects
    print(f"\n4. What SupervisorState expects:")
    agents_field = SupervisorState.model_fields.get("agents")
    if agents_field:
        print(f"   Field annotation: {agents_field.annotation}")
        # Try to get the actual AgentInfo class from the annotation
        import typing

        if hasattr(typing, "get_args"):
            args = typing.get_args(agents_field.annotation)
            if len(args) > 1:
                expected_type = args[1]
                print(f"   Expected AgentInfo type: {expected_type}")
                print(
                    f"   Expected module: {getattr(expected_type, '__module__', 'Unknown')}"
                )


if __name__ == "__main__":
    test_import_paths()
