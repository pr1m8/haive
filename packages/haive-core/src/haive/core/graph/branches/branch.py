"""
Core Branch implementation for dynamic routing.

This module provides a unified Branch class that replaces the need for
separate ConditionalEdge objects, consolidating all routing logic.
"""

import logging
import uuid
from typing import Any, Callable, Dict, List, Optional, Set, Union

from langgraph.graph import END
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator

from haive.core.graph.branches.dynamic import DynamicMapping
from haive.core.graph.branches.send_mapping import (
    SendGenerator,
    SendMapping,
    SendMappingList,
)
from haive.core.graph.branches.types import (
    BranchMode,
    BranchResult,
    ComparisonType,
)
from haive.core.graph.common.field_utils import (
    extract_base_field,
    extract_field,
    get_last_message_content,
)
from haive.core.graph.common.references import CallableReference
from haive.core.graph.common.types import ConfigLike, NodeOutput, StateLike

logger = logging.getLogger(__name__)


class Branch(BaseModel):
    """
    Unified branch for dynamic routing based on state values.

    This class combines the functionality of branch routing and conditional edges,
    providing a single unified interface for graph routing.
    """

    # Core identification
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default_factory=lambda: f"branch_{uuid.uuid4().hex[:8]}")

    # Connection information (replaces ConditionalEdge)
    source_node: Optional[str] = Field(default=None)
    destinations: Dict[Union[bool, str], str] = Field(
        default_factory=lambda: {True: "continue", False: END}
    )
    default: Optional[str] = None

    # Evaluation properties
    mode: BranchMode = BranchMode.DIRECT
    key: Optional[str] = None
    value: Any = None
    comparison: Union[ComparisonType, str] = ComparisonType.EQUALS
    function: Optional[Callable] = None
    function_ref: Optional[CallableReference] = None
    allow_none: bool = False
    message_key: str = "messages"

    # Advanced features
    send_mappings: List[SendMapping] = Field(default_factory=list)
    send_generators: List[SendGenerator] = Field(default_factory=list)
    dynamic_mapping: Optional[DynamicMapping] = None
    chain_branches: List["Branch"] = Field(default_factory=list)
    condition_ref: Optional[CallableReference] = None
    true_branch: Optional[Union[str, "Branch"]] = None
    false_branch: Optional[Union[str, "Branch"]] = None

    # Implementation details
    send_mapping_list: Optional[SendMappingList] = None

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def setup_function_and_mappings(self) -> "Branch":
        """Set up function and mappings after initialization."""
        # Resolve function from reference
        if self.function_ref and not self.function:
            resolved = self.function_ref.resolve()
            # Handle case where resolve returns a tuple
            if isinstance(resolved, tuple) and len(resolved) > 0:
                self.function = resolved[0]  # Extract the function from the tuple
            else:
                self.function = resolved

        # Set up send mapping list
        if not self.send_mapping_list and (self.send_mappings or self.send_generators):
            self.send_mapping_list = SendMappingList(
                mappings=self.send_mappings, generators=self.send_generators
            )

        return self

    @model_validator(mode="after")
    def validate_destinations_and_default(self) -> "Branch":
        """Validate destinations and set default if needed."""
        if not self.destinations:
            self.destinations = {True: "continue", False: END}
        elif len(self.destinations) == 1:
            # Only convert to boolean mapping if the key is already a boolean
            # or if the key is a generic string like "continue"
            single_key = next(iter(self.destinations.keys()))
            if isinstance(single_key, bool) or single_key in ["continue", "default"]:
                # If only one destination is provided with a boolean/generic key, map it to True and END to False
                true_dest = next(iter(self.destinations.values()))
                self.destinations = {True: true_dest, False: END}
            # Otherwise, preserve the original string key and don't add boolean fallbacks
        # Only set default if we have multiple destinations and no default is set
        # AND we don't have a list of destinations (True/False mapping)
        elif (
            len(self.destinations) > 1
            and self.default is None
            and not all(isinstance(k, bool) for k in self.destinations.keys())
        ):
            self.default = END
        return self

    def __call__(
        self, state: StateLike, config: Optional[ConfigLike] = None
    ) -> NodeOutput:
        """Make Branch directly callable for use in conditional edges."""
        try:
            # Define common variables that might be accessed

            # Special handling for dynamic branch with dynamic_mapping
            if self.mode == BranchMode.DYNAMIC and self.dynamic_mapping:
                # Get the next node and mapping
                next_node, output_mapping = self.dynamic_mapping.get_mapping(state)

                # Always return a Command for dynamic branches
                return Command(
                    goto=next_node,
                    update={"output_mapping": output_mapping} if output_mapping else {},
                )

            # Regular branch evaluation for other modes
            result = self.evaluate(state)

            # Handle None results
            if result is None:
                # If we have a default destination, use it
                if self.default is not None:
                    return self.default
                # Otherwise use False route
                if False in self.destinations:
                    return self.destinations[False]
                # Last resort - return first destination
                if self.destinations:
                    return next(iter(self.destinations.values()))
                return END  # Final fallback

            return result

        except NameError as ne:
            # Handle specific NameError cases (like 'model' not defined)
            error_msg = str(ne).lower()

            # Only log for non-model errors (suppress expected errors)
            if "model" not in error_msg:
                logger.error(f"NameError in branch evaluation: {ne}")

            # Same fallback logic as other exceptions
            if self.default is not None:
                return self.default
            if False in self.destinations:
                return self.destinations[False]
            if self.destinations:
                return next(iter(self.destinations.values()))
            return END
        except Exception as e:
            logger.error(f"Error in branch evaluation: {e}")
            # Same fallback logic as None
            if self.default is not None:
                return self.default
            if False in self.destinations:
                return self.destinations[False]
            if self.destinations:
                return next(iter(self.destinations.values()))
            return END

    def evaluator(self, state: Dict[str, Any]) -> str:
        """
        Evaluate the branch condition and return the next node.

        Args:
            state: Current graph state

        Returns:
            Name of the next node
        """
        try:
            # Define common variables that might be accessed

            result = self.function(state)

            # Look up the destination
            if result in self.destinations:
                return self.destinations[result]

            # Use default if no match
            if self.default is not None:
                return self.default

            # No match and no default - use first destination as fallback
            if self.destinations:
                return next(iter(self.destinations.values()))

            # No destinations - return empty string
            return ""

        except NameError as ne:
            # Handle specific NameError cases quietly
            error_msg = str(ne).lower()

            if "model" not in error_msg:
                # Log non-model errors
                print(f"Error evaluating branch: {ne}")

            return self.default if self.default else ""
        except Exception as e:
            # Log and return default or fallback
            print(f"Error evaluating branch: {e}")
            return self.default if self.default else ""

    def evaluate(self, state: StateLike) -> NodeOutput:
        """Evaluate the branch against state."""
        try:
            # Define common variables that might be accessed

            # Handle different branch modes
            if self.mode == BranchMode.FUNCTION and self.function:
                return self._process_result(self.function(state), state)

            elif self.mode == BranchMode.CHAIN and self.chain_branches:
                return self._evaluate_chain(state)

            elif self.mode == BranchMode.CONDITION and self.condition_ref:
                return self._evaluate_condition(state)

            elif self.mode == BranchMode.SEND_MAPPER:
                return self._evaluate_send_mapper(state)

            elif self.mode == BranchMode.DYNAMIC and self.dynamic_mapping:
                return self._evaluate_dynamic(state)

            # Default direct mode
            # Handle existence checks
            if self.comparison in [ComparisonType.EXISTS, ComparisonType.NOT_EXISTS]:
                result = self._check_exists(state)
                if self.comparison == ComparisonType.NOT_EXISTS:
                    result = not result
                return self._get_destination(result)

            # Handle special message comparisons
            elif self.comparison == ComparisonType.MESSAGE_CONTAINS:
                result = self._check_message_contains(state)
                return self._get_destination(result)

            # Regular field comparison
            else:
                field_value = extract_field(state, self.key)

                # Handle None values
                if field_value is None and not self.allow_none:
                    logger.warning(
                        f"Field '{self.key}' is None and allow_none is False"
                    )
                    return self.default

                # Perform comparison
                result = self._compare(field_value)
                return self._get_destination(result)

        except NameError as ne:
            # Handle specific NameError cases (like 'model' not defined)
            error_msg = str(ne).lower()

            # Only log for non-model errors (suppress expected errors)
            if "model" not in error_msg:
                logger.error(f"NameError in branch evaluation: {ne}")

            return self.default
        except Exception as e:
            logger.error(f"Error evaluating branch: {e}")
            return self.default

    def _process_result(self, result: Any, state: StateLike) -> NodeOutput:
        """Process the result of a branch evaluation."""
        from langgraph.types import Command

        # Handle Send objects
        if isinstance(result, Send):
            return BranchResult(send_objects=[result])

        # Handle lists of Send objects
        if isinstance(result, list) and all(isinstance(item, Send) for item in result):
            return BranchResult(send_objects=result)

        # Handle Command objects
        if isinstance(result, Command):
            return BranchResult(command_object=result)

        # Handle dictionaries with special keys
        if isinstance(result, dict):
            if "_output_mapping" in result:
                # Handle dynamic output mapping
                mapping = result.pop("_output_mapping")
                next_node = result.pop("_next_node", self.default)
                return BranchResult(next_node=next_node, output_mapping=mapping)

            # Handle dictionaries with send objects
            if "_send_objects" in result:
                send_objects = result["_send_objects"]
                if isinstance(send_objects, list) and all(
                    isinstance(item, Send) for item in send_objects
                ):
                    return BranchResult(send_objects=send_objects)

        # Handle regular destination lookup
        if isinstance(result, (bool, str)):
            return self._get_destination(result)

        # Fallback
        return self.default

    def _get_destination(self, result: Union[bool, str]) -> str:
        """Get destination from result."""
        return self.destinations.get(result, self.default)

    def _compare(self, value: Any) -> bool:
        """Compare a value against the branch's value."""
        comparison = self.comparison
        target = self.value

        # Convert string comparison to enum if needed
        if isinstance(comparison, str):
            try:
                comparison = ComparisonType(comparison)
            except ValueError:
                # Use as string if not an enum value
                pass

        # Perform comparison
        if comparison == ComparisonType.EQUALS:
            return value == target
        elif comparison == ComparisonType.NOT_EQUALS:
            return value != target
        elif comparison == ComparisonType.GREATER_THAN:
            return value > target
        elif comparison == ComparisonType.LESS_THAN:
            return value < target
        elif comparison == ComparisonType.GREATER_EQUALS:
            return value >= target
        elif comparison == ComparisonType.LESS_EQUALS:
            return value <= target
        elif comparison == ComparisonType.IN:
            return value in target if isinstance(target, (list, tuple, set)) else False
        elif comparison == ComparisonType.CONTAINS:
            if isinstance(value, str):
                return target in value
            if isinstance(value, (list, tuple, set, dict)):
                return target in value
            return False
        elif comparison == ComparisonType.IS:
            return value is target
        elif comparison == ComparisonType.IS_NOT:
            return value is not target
        elif comparison == ComparisonType.MATCHES:
            import re

            if isinstance(value, str) and isinstance(target, str):
                return bool(re.match(target, value))
            return False
        elif comparison == ComparisonType.STARTS_WITH:
            return value.startswith(target) if isinstance(value, str) else False
        elif comparison == ComparisonType.ENDS_WITH:
            return value.endswith(target) if isinstance(value, str) else False
        elif comparison == ComparisonType.HAS_LENGTH:
            try:
                return len(value) == target
            except (TypeError, AttributeError):
                return False

        logger.warning(f"Unknown comparison type: {comparison}")
        return False

    def _check_exists(self, state: StateLike) -> bool:
        """Check if a field exists in state."""
        if self.key is None:
            return False

        value = extract_field(state, self.key)
        return value is not None

    def _check_message_contains(self, state: StateLike) -> bool:
        """Check if the last message contains specified text."""
        content = get_last_message_content(state, self.message_key)
        if not content or not isinstance(content, str):
            return False

        # Check if content contains value
        return self.value in content

    def _evaluate_chain(self, state: StateLike) -> NodeOutput:
        """Evaluate a chain of branches."""
        for branch in self.chain_branches:
            result = branch.evaluate(state)

            # If result is BranchResult with content, return it
            if isinstance(result, BranchResult) and (
                result.is_send or result.is_command or result.has_mapping
            ):
                return result

            # If string result is not the branch's default, return it
            if isinstance(result, str) and result != branch.default:
                return result

        # If all branches returned default, use this branch's default
        return self.default

    def _evaluate_condition(self, state: StateLike) -> NodeOutput:
        """Evaluate a conditional branch."""
        if not self.condition_ref:
            return self.default

        try:
            condition_func = self.condition_ref.resolve()
            if not condition_func:
                return self.default

            condition_result = condition_func(state)

            if condition_result:
                if isinstance(self.true_branch, Branch):
                    return self.true_branch.evaluate(state)
                return self.true_branch or self.default
            else:
                if isinstance(self.false_branch, Branch):
                    return self.false_branch.evaluate(state)
                return self.false_branch or self.default

        except Exception as e:
            logger.error(f"Error in condition evaluation: {e}")
            return self.default

    def _evaluate_send_mapper(self, state: StateLike) -> BranchResult:
        """Evaluate a mapper branch that creates Send objects."""
        sends = []

        # Use send_mapping_list
        if self.send_mapping_list:
            sends.extend(self.send_mapping_list.create_sends(state))

        # Use function if available and no sends yet
        if not sends and self.function:
            try:
                result = self.function(state)

                # Handle list of Send objects
                if isinstance(result, list):
                    from langgraph.types import Send

                    sends.extend([obj for obj in result if isinstance(obj, Send)])

                # Handle single Send object
                elif hasattr(result, "node") and hasattr(result, "arg"):
                    sends.append(result)

            except Exception as e:
                logger.error(f"Error in mapper function: {e}")

        return BranchResult(send_objects=sends)

    def _evaluate_dynamic(self, state: StateLike) -> Any:
        """Evaluate a dynamic branch that selects output mapping based on state."""
        from langgraph.types import Command

        if not self.dynamic_mapping:
            return Command(goto=self.default)

        # Get mapping
        next_node, output_mapping = self.dynamic_mapping.get_mapping(state)

        # Always return a Command object for dynamic branches
        return Command(
            goto=next_node,
            update={"output_mapping": output_mapping} if output_mapping else {},
        )

    def extract_field_references(self) -> Set[str]:
        """Extract field references used by this branch."""
        fields = set()

        # Add direct key reference
        if self.key:
            fields.add(extract_base_field(self.key))

        # Add message key if used
        if self.comparison == ComparisonType.MESSAGE_CONTAINS:
            fields.add(self.message_key)

        # Add fields from send mappings
        if self.send_mapping_list:
            for mapping in self.send_mapping_list.mappings:
                if mapping.condition:
                    fields.add(extract_base_field(mapping.condition))
                for source_field in mapping.fields.values():
                    fields.add(extract_base_field(source_field))

            for generator in self.send_mapping_list.generators:
                fields.add(extract_base_field(generator.collection_field))

        return fields
