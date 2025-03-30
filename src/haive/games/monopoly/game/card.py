from typing import Any

class Card:
    """Represents a Chance or Community Chest card."""
    def __init__(self, text: str, action: str, value: Any = None):
        self.text = text
        self.action = action  # Type of action: move, pay, collect, etc.
        self.value = value    # Amount to pay/collect or position to move to

