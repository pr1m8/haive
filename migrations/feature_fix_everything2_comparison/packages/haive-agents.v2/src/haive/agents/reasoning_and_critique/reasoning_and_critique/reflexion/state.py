from agents.simple.state import SimpleAgentState


class ReflexionState(SimpleAgentState):
    """State for the Reflexion agent."""

    reflections_count: int = 0
    answer: str = ""
