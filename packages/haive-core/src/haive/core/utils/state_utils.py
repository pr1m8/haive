def _debug_state_object(state, label="State"):
    """Debug the state object structure to help diagnose persistence issues."""
    if hasattr(state, "values"):
        if isinstance(state.values, dict) and "messages" in state.values:
            pass

    if hasattr(state, "channel_values") and (
        state.channel_values
        and isinstance(state.channel_values, dict)
        and "messages" in state.channel_values
    ):
        pass
