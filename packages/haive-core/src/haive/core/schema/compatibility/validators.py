"""
Field and model validation framework with async support.
"""

from __future__ import annotations

import asyncio
import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel

from haive.core.schema.compatibility.types import (
    FieldInfo,
    SchemaInfo,
    ValidationError,
    ValidationResult,
    ValidationWarning,
)


class ValidationContext(BaseModel):
    """Context passed through validation chain."""

    current_path: List[str] = []
    root_value: Any = None
    parent_value: Any = None
    field_info: Optional[FieldInfo] = None
    schema_info: Optional[SchemaInfo] = None
    custom_data: Dict[str, Any] = {}

    def push_path(self, segment: str) -> None:
        """Push a path segment."""
        self.current_path.append(segment)

    def pop_path(self) -> Optional[str]:
        """Pop a path segment."""
        return self.current_path.pop() if self.current_path else None

    @property
    def current_path_str(self) -> str:
        """Get current path as string."""
        return ".".join(self.current_path)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True


class Validator(ABC):
    """Base validator class."""

    @abstractmethod
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate a value."""
        pass

    @property
    def supports_async(self) -> bool:
        """Whether this validator supports async validation."""
        return hasattr(self, "avalidate")

    async def avalidate(
        self, value: Any, context: ValidationContext
    ) -> ValidationResult:
        """Async validation (optional)."""
        # Default: run sync validation in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.validate, value, context)


class FieldValidator(Validator):
    """Validator for individual fields."""

    def __init__(
        self,
        field_name: str,
        validators: Optional[List[Callable[[Any], bool]]] = None,
        error_messages: Optional[Dict[str, str]] = None,
    ):
        self.field_name = field_name
        self.validators = validators or []
        self.error_messages = error_messages or {}

    def add_validator(
        self,
        validator: Callable[[Any], bool],
        error_message: Optional[str] = None,
    ) -> None:
        """Add a validator function."""
        self.validators.append(validator)
        if error_message:
            self.error_messages[str(validator)] = error_message

    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate field value."""
        result = ValidationResult(is_valid=True)

        for validator in self.validators:
            try:
                if not validator(value):
                    error_msg = self.error_messages.get(
                        str(validator), f"Validation failed for {self.field_name}"
                    )
                    result.add_error(
                        ValidationError(
                            field=self.field_name,
                            message=error_msg,
                            error_type="field_validation",
                            context={"value": value, "path": context.current_path_str},
                        )
                    )
            except Exception as e:
                result.add_error(
                    ValidationError(
                        field=self.field_name,
                        message=f"Validator error: {str(e)}",
                        error_type="validator_exception",
                        context={"exception": str(e)},
                    )
                )

        return result


class ModelValidator(Validator):
    """Validator for entire models/schemas."""

    def __init__(
        self,
        schema_info: Optional[SchemaInfo] = None,
        field_validators: Optional[Dict[str, FieldValidator]] = None,
        cross_field_validators: Optional[List[Callable]] = None,
    ):
        self.schema_info = schema_info
        self.field_validators = field_validators or {}
        self.cross_field_validators = cross_field_validators or []

    def add_field_validator(self, field_name: str, validator: FieldValidator) -> None:
        """Add a field validator."""
        self.field_validators[field_name] = validator

    def add_cross_field_validator(self, validator: Callable) -> None:
        """Add a cross-field validator."""
        self.cross_field_validators.append(validator)

    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate entire model."""
        result = ValidationResult(is_valid=True)

        # Convert to dict if BaseModel
        if isinstance(value, BaseModel):
            data = value.model_dump()
        elif isinstance(value, dict):
            data = value
        else:
            result.add_error(
                ValidationError(
                    field=None,
                    message="Value must be a dict or BaseModel",
                    error_type="type_error",
                )
            )
            return result

        # Validate individual fields
        for field_name, field_validator in self.field_validators.items():
            if field_name in data:
                context.push_path(field_name)
                field_result = field_validator.validate(data[field_name], context)

                for error in field_result.errors:
                    result.add_error(error)
                for warning in field_result.warnings:
                    result.add_warning(warning)

                context.pop_path()

        # Cross-field validation
        for validator in self.cross_field_validators:
            try:
                validation = validator(data)
                if isinstance(validation, bool) and not validation:
                    result.add_error(
                        ValidationError(
                            field=None,
                            message="Cross-field validation failed",
                            error_type="cross_field_validation",
                        )
                    )
                elif isinstance(validation, tuple) and len(validation) == 2:
                    is_valid, message = validation
                    if not is_valid:
                        result.add_error(
                            ValidationError(
                                field=None,
                                message=message,
                                error_type="cross_field_validation",
                            )
                        )
            except Exception as e:
                result.add_error(
                    ValidationError(
                        field=None,
                        message=f"Cross-field validator error: {str(e)}",
                        error_type="validator_exception",
                    )
                )

        return result


@dataclass
class ValidatorChain:
    """Chain multiple validators together."""

    validators: List[Validator]
    stop_on_first_error: bool = False

    def validate(
        self, value: Any, context: Optional[ValidationContext] = None
    ) -> ValidationResult:
        """Run all validators in chain."""
        if context is None:
            context = ValidationContext(root_value=value)

        result = ValidationResult(is_valid=True)

        for validator in self.validators:
            val_result = validator.validate(value, context)

            # Merge results
            for error in val_result.errors:
                result.add_error(error)
            for warning in val_result.warnings:
                result.add_warning(warning)

            # Stop if requested
            if self.stop_on_first_error and not val_result.is_valid:
                break

        return result

    async def avalidate(
        self, value: Any, context: Optional[ValidationContext] = None
    ) -> ValidationResult:
        """Async validation of chain."""
        if context is None:
            context = ValidationContext(root_value=value)

        result = ValidationResult(is_valid=True)

        for validator in self.validators:
            if validator.supports_async:
                val_result = await validator.avalidate(value, context)
            else:
                val_result = validator.validate(value, context)

            # Merge results
            for error in val_result.errors:
                result.add_error(error)
            for warning in val_result.warnings:
                result.add_warning(warning)

            # Stop if requested
            if self.stop_on_first_error and not val_result.is_valid:
                break

        return result


class ValidatorBuilder:
    """Builder for creating validators."""

    @staticmethod
    def for_type(type_hint: type) -> FieldValidator:
        """Create validator for a specific type."""
        validator = FieldValidator(f"{type_hint.__name__}_validator")

        # Add type check
        validator.add_validator(
            lambda x: isinstance(x, type_hint),
            f"Value must be of type {type_hint.__name__}",
        )

        return validator

    @staticmethod
    def for_range(
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        field_name: str = "value",
    ) -> FieldValidator:
        """Create range validator."""
        validator = FieldValidator(field_name)

        if min_value is not None:
            validator.add_validator(
                lambda x: x >= min_value, f"Value must be >= {min_value}"
            )

        if max_value is not None:
            validator.add_validator(
                lambda x: x <= max_value, f"Value must be <= {max_value}"
            )

        return validator

    @staticmethod
    def for_length(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        field_name: str = "value",
    ) -> FieldValidator:
        """Create length validator."""
        validator = FieldValidator(field_name)

        if min_length is not None:
            validator.add_validator(
                lambda x: len(x) >= min_length, f"Length must be >= {min_length}"
            )

        if max_length is not None:
            validator.add_validator(
                lambda x: len(x) <= max_length, f"Length must be <= {max_length}"
            )

        return validator

    @staticmethod
    def for_pattern(pattern: str, field_name: str = "value") -> FieldValidator:
        """Create regex pattern validator."""
        import re

        regex = re.compile(pattern)

        validator = FieldValidator(field_name)
        validator.add_validator(
            lambda x: bool(regex.match(str(x))), f"Value must match pattern: {pattern}"
        )

        return validator

    @staticmethod
    def combine(*validators: Validator) -> ValidatorChain:
        """Combine multiple validators into a chain."""
        return ValidatorChain(validators=list(validators))


# Common validators
class CommonValidators:
    """Collection of common validators."""

    @staticmethod
    def not_empty(value: Any) -> bool:
        """Check value is not empty."""
        if value is None:
            return False
        if hasattr(value, "__len__"):
            return len(value) > 0
        return True

    @staticmethod
    def is_email(value: str) -> bool:
        """Basic email validation."""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, value))

    @staticmethod
    def is_url(value: str) -> bool:
        """Basic URL validation."""
        import re

        pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        return bool(re.match(pattern, value))

    @staticmethod
    def is_uuid(value: str) -> bool:
        """UUID validation."""
        import re

        pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        return bool(re.match(pattern, value.lower()))


# Convenience function
def create_validator(
    schema_info: SchemaInfo,
    custom_validators: Optional[Dict[str, List[Callable]]] = None,
) -> ModelValidator:
    """Create a model validator from schema info."""
    model_validator = ModelValidator(schema_info=schema_info)

    # Add validators for each field
    for field_name, field_info in schema_info.fields.items():
        field_validator = FieldValidator(field_name)

        # Add type validator
        if field_info.type_info.type_hint:
            field_validator.add_validator(
                lambda x, t=field_info.type_info.type_hint: isinstance(x, t),
                f"Must be of type {field_info.type_info.type_hint}",
            )

        # Add required validator
        if field_info.is_required:
            field_validator.add_validator(
                CommonValidators.not_empty, "Field is required"
            )

        # Add custom validators
        if custom_validators and field_name in custom_validators:
            for validator in custom_validators[field_name]:
                field_validator.add_validator(validator)

        model_validator.add_field_validator(field_name, field_validator)

    return model_validator
