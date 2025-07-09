from pydantic import RootModel


class Reasoning(RootModel):
    """A mixin for reasoning about the world."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reasoning = []
