"""Protocols graph module.

This module provides protocols functionality for the Haive framework.

Classes:
    NodeProcessor: NodeProcessor implementation.
    CommandHandler: CommandHandler implementation.
    InputProcessor: InputProcessor implementation.

Functions:
    can_process: Can Process functionality.
    create_node_function: Create Node Function functionality.
    process_result: Process Result functionality.
"""

# src/haive/core/graph/node/protocols.py

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class NodeProcessor(Protocol):
    """Protocol for node processors that handle specific node types."""

    def can_process(self, engine: Any) -> bool: ...

    def create_node_function(self, engine: Any, node_config: Any) -> callable: ...


@runtime_checkable
class CommandHandler(Protocol):
    """Protocol for handlers that process command patterns."""

    def process_result(
        self, result: Any, config: Any, original_state: dict[str, Any]
    ) -> Any: ...


@runtime_checkable
class InputProcessor(Protocol):
    """Protocol for input processing strategies."""

    def extract_input(self, state: dict[str, Any], config: Any) -> Any: ...


@runtime_checkable
class OutputProcessor(Protocol):
    """Protocol for output processing strategies."""

    def process_output(
        self, result: Any, config: Any, original_state: dict[str, Any]
    ) -> dict[str, Any]: ...
