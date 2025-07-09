from typing import Any, Protocol, runtime_checkable

from langchain_core.runnables import RunnableConfig


@runtime_checkable
class ConfigurableProtocol(Protocol):
    """Protocol for objects that can be configured with runtime configs."""

    def apply_runnable_config(self, config: RunnableConfig) -> dict[str, Any]: ...
