"""Debug import issue - maybe it's comparing different AgentInfo classes."""



def test_import_paths():
    """Check if we have import path issues."""

    # Import AgentInfo two ways
    from agent_info import AgentInfo as AgentInfo1

    from haive.agents.experiments.supervisor.agent_info import AgentInfo as AgentInfo2

    # Create instances
    class DummyAgent:
        name = "dummy"

    agent = DummyAgent()

    info1 = AgentInfo1(agent=agent, name="test", description="Test")
    info2 = AgentInfo2(agent=agent, name="test", description="Test")


    # Now test with SupervisorState using different imports

    from supervisor_state import SupervisorState

    try:
        SupervisorState(agents={"test": info1})
    except Exception as e:
        pass")

    try:
        SupervisorState(agents={"test": info2})
    except Exception as e:
        pass")

    # Check what SupervisorState expects
    agents_field = SupervisorState.model_fields.get("agents")
    if agents_field:
        # Try to get the actual AgentInfo class from the annotation
        import typing

        if hasattr(typing, "get_args"):
            args = typing.get_args(agents_field.annotation)
            if len(args) > 1:
                expected_type = args[1]


if __name__ == "__main__":
    test_import_paths()
