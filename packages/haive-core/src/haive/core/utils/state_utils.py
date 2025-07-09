def _debug_state_object(state, label="State"):
    """Debug the state object structure to help diagnose persistence issues."""
    print(f"\n--- {label} Debug ---")
    print(f"Type: {type(state)}")

    if hasattr(state, "values"):
        print(f"Has values: {type(state.values)}")
        if isinstance(state.values, dict) and "messages" in state.values:
            print(f"Messages in values: {len(state.values['messages'])}")

    if hasattr(state, "channel_values"):
        print(f"Has channel_values: {type(state.channel_values)}")
        if (
            state.channel_values
            and isinstance(state.channel_values, dict)
            and "messages" in state.channel_values
        ):
            print(
                f"Messages in channel_values: {len(state.channel_values['messages'])}"
            )

    print(f"State attributes: {dir(state)[:10]}...")
    print(
        f"State dict keys: {dir(state.__dict__) if hasattr(state, '__dict__') else 'No __dict__'}"
    )
    print("------------------------\n")
