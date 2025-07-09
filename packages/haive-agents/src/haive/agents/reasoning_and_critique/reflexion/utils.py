from pydantic import BaseModel


def _get_num_iterations(state: BaseModel) -> int:
    """Counts consecutive 'tool' or 'ai' message types from the end of the list."""
    i = 0
    for m in reversed(state.messages):  # Reverse iteration for efficiency
        if isinstance(m, dict):  # Ensure compatibility with dict-based messages
            msg_type = m.get("type", "")
        else:
            msg_type = getattr(m, "type", "")

        if msg_type not in {"tool", "ai"}:
            break
        i += 1
    return i
