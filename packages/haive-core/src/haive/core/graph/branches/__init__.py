"""
Branch system for dynamic routing based on state values.
"""

from typing import Any, Callable, Dict, List, Optional, Union

from haive.core.graph.branches.branch import Branch
from haive.core.graph.branches.dynamic import DynamicMapping
from haive.core.graph.branches.send_mapping import (
    SendGenerator,
    SendMapping,
    SendMappingList,
)
from haive.core.graph.branches.types import (
    BranchMode,
    BranchProtocol,
    BranchResult,
    ComparisonType,
)
from haive.core.graph.common.field_utils import (
    extract_base_field,
    extract_field,
    get_field_value,
)
from haive.core.graph.common.references import CallableReference

# Import from common utilities
from haive.core.graph.common.types import ConfigLike, NodeOutput, StateLike


# Factory functions for common branch types
def key_equals(
    key: str, value: Any, true_dest: str = "continue", false_dest: str = "END"
) -> Branch:
    """Create a Branch that checks if a key equals a value."""
    return Branch(
        key=key,
        value=value,
        comparison=ComparisonType.EQUALS,
        destinations={True: true_dest, False: false_dest},
    )


def key_exists(
    key: str, true_dest: str = "continue", false_dest: str = "END"
) -> Branch:
    """Create a Branch that checks if a key exists in the state."""
    return Branch(
        key=key,
        comparison=ComparisonType.EXISTS,
        destinations={True: true_dest, False: false_dest},
    )


def from_function(
    function: Callable[[StateLike], Union[bool, str]],
    destinations: Optional[Dict[Union[bool, str], str]] = None,
    default: str = "END",
) -> Branch:
    """Create a Branch from a function."""
    return Branch(
        function_ref=CallableReference.from_callable(function),
        destinations=destinations,
        default=default,
        mode=BranchMode.FUNCTION,
    )


def chain(*branches: Branch, default: str = "END") -> Branch:
    """Chain multiple branches together, evaluating them in sequence."""
    return Branch(chain_branches=list(branches), mode=BranchMode.CHAIN, default=default)


def conditional(
    condition: Callable[[StateLike], bool],
    if_true: Union[str, Branch],
    if_false: Union[str, Branch],
    default: str = "END",
) -> Branch:
    """Create a Branch with conditional evaluation."""
    return Branch(
        condition_ref=CallableReference.from_callable(condition),
        true_branch=if_true,
        false_branch=if_false,
        mode=BranchMode.CONDITION,
        default=default,
    )


def message_contains(
    text: str,
    true_dest: str = "continue",
    false_dest: str = "END",
    message_key: str = "messages",
) -> Branch:
    """Create a Branch that checks if the last message contains specific text."""
    return Branch(
        value=text,
        comparison=ComparisonType.MESSAGE_CONTAINS,
        destinations={True: true_dest, False: false_dest},
        message_key=message_key,
    )


def send_mapper(
    function: Optional[Callable[[StateLike], List[Any]]] = None,
    mappings: Optional[List[SendMapping]] = None,
    generators: Optional[List[SendGenerator]] = None,
) -> Branch:
    """Create a Branch that generates Send objects."""
    function_ref = CallableReference.from_callable(function) if function else None

    return Branch(
        function_ref=function_ref,
        send_mappings=mappings or [],
        send_generators=generators or [],
        mode=BranchMode.SEND_MAPPER,
    )


def create_from_send_function(
    mapper_function: Callable[[StateLike], List[Any]],
) -> Branch:
    """Create a Send mapper branch from a function that returns Send objects."""
    return send_mapper(function=mapper_function)
