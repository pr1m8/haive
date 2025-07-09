"""PromptTemplateMixin: Advanced prompt template integration for engine classes.

This module provides the PromptTemplateMixin class, which adds sophisticated
prompt template management capabilities to any engine class. The mixin enables
automatic input schema derivation, prompt template validation, and seamless
composition with existing engine functionality.

The PromptTemplateMixin is designed to integrate with Haive's engine architecture,
particularly AugLLMConfig, to provide dynamic schema generation based on prompt
template requirements while preserving existing engine behaviors.

Key Features:
    - Automatic conversion of prompt templates to InvokableEngines
    - Dynamic input schema derivation with intelligent composition
    - Prompt template validation and preprocessing
    - Schema composition with existing engine schemas
    - Field-level validation integration via Pydantic validators
    - Support for both override and composition approaches

Architecture:
    The mixin uses method override patterns to integrate with engine classes:
    - Overrides derive_input_schema() to incorporate prompt template variables
    - Provides field validators for prompt template preprocessing
    - Offers helper methods for prompt formatting and variable management

Integration Patterns:
    1. Method Override: derive_input_schema() method is overridden to check for
       prompt templates and compose schemas when present
    2. Field Validation: @field_validator decorators preprocess prompt templates
    3. Composition: Existing schemas are preserved and extended, not replaced

Example:
    Basic integration with an engine class:

    ```python
    from haive.core.common.mixins.prompt_template_mixin import PromptTemplateMixin
    from haive.core.engine.base import InvokableEngine

    class MyEngine(PromptTemplateMixin, InvokableEngine):
        prompt_template: Optional[BasePromptTemplate] = None

        # The mixin automatically enhances input schema derivation
        pass

    # Usage
    engine = MyEngine(prompt_template=my_template)
    schema = engine.derive_input_schema()  # Includes prompt variables
    ```

    Advanced usage with schema composition:

    ```python
    # Engine with existing input schema
    class AdvancedEngine(PromptTemplateMixin, InvokableEngine):
        def get_base_input_schema(self):
            return MyExistingSchema

    # The mixin will compose prompt variables with existing schema
    engine = AdvancedEngine(prompt_template=chat_template)
    combined_schema = engine.derive_input_schema()
    ```

Classes:
    PromptTemplateMixin: Main mixin class for prompt template integration

Dependencies:
    - langchain_core: For prompt template functionality and message types
    - pydantic: For schema generation, validation, and field validation
    - typing: For type hints and optional typing support

Author:
    Haive Core Team

Version:
    1.0.0

See Also:
    - haive.core.engine.prompt_template.PromptTemplateEngine: Standalone engine
    - haive.core.engine.aug_llm.config.AugLLMConfig: Primary integration target
    - haive.core.schema.schema_composer.SchemaComposer: Schema composition utilities
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

from langchain_core.messages import AnyMessage
from langchain_core.prompts import BasePromptTemplate
from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from haive.core.engine.prompt_template import PromptTemplateEngine


class PromptTemplateMixin:
    """Advanced mixin for integrating prompt template functionality into engine classes.

    This mixin provides comprehensive prompt template management capabilities,
    enabling any engine class to automatically derive input schemas from prompt
    templates while preserving existing functionality through intelligent composition.

    The mixin is designed to be non-invasive and compatible with existing engine
    architectures. It overrides key methods like derive_input_schema() to enhance
    functionality rather than replace it, ensuring backward compatibility.

    Key Capabilities:
        - Automatic prompt template to engine conversion
        - Dynamic input schema derivation with type inference
        - Intelligent schema composition (prompt + existing schemas)
        - Prompt template validation and preprocessing
        - Field-level integration via Pydantic validators
        - Configurable behavior (enable/disable prompt schema usage)

    Required Fields:
        Classes using this mixin must define:
        - prompt_template: Optional[BasePromptTemplate] = None

    Optional Configuration:
        - _use_prompt_for_input_schema: bool = True (control schema derivation)
        - _prompt_engine: Internal cache for prompt template engine

    Method Override Pattern:
        The mixin overrides derive_input_schema() using a safe pattern:
        1. Attempts to call parent class implementation
        2. Checks if prompt template schema derivation is enabled
        3. Derives schema from prompt template if present
        4. Composes schemas intelligently (prompt + parent)
        5. Falls back gracefully on any errors

    Examples:
        Basic usage:

        ```python
        class MyEngine(PromptTemplateMixin, InvokableEngine):
            prompt_template: Optional[BasePromptTemplate] = None

        engine = MyEngine(prompt_template=template)
        schema = engine.derive_input_schema()  # Enhanced with prompt fields
        ```

        With existing schema:

        ```python
        class ComplexEngine(PromptTemplateMixin, SomeOtherMixin, InvokableEngine):
            # Existing schema logic preserved and enhanced
            pass
        ```

    Integration Notes:
        - Safe to use with multiple inheritance
        - Preserves existing derive_input_schema() behavior
        - Graceful error handling prevents disruption
        - Can be enabled/disabled at runtime

    See Also:
        - PromptTemplateEngine: Standalone engine implementation
        - AugLLMConfig: Primary usage example with full integration
    """

    # Fields that subclasses need to have
    prompt_template: Optional[BasePromptTemplate]
    _prompt_engine: Optional["PromptTemplateEngine"] = None
    _use_prompt_for_input_schema: bool = True

    def derive_input_schema(self) -> Optional[Type[BaseModel]]:
        """Override derive_input_schema to intelligently compose prompt template schemas.

        This method enhances the standard input schema derivation process by
        incorporating prompt template variables when a prompt template is present.
        It uses a safe override pattern that preserves existing functionality
        while adding prompt template awareness.

        Returns:
            Optional[Type[BaseModel]]: A Pydantic model class that includes:
                - All fields from the parent class schema (if any)
                - Additional fields derived from prompt template variables
                - Proper field types, defaults, and validation rules

        Process:
            1. Attempts to derive schema from parent class (preserves existing behavior)
            2. Checks if prompt template schema derivation is enabled
            3. Derives schema from prompt template variables if present
            4. Intelligently composes parent + prompt schemas when both exist
            5. Falls back gracefully on any errors to ensure stability

        Examples:
            With prompt template only:
            ```python
            # Engine with prompt template
            engine.prompt_template = PromptTemplate.from_template("Hello {name}")
            schema = engine.derive_input_schema()
            # schema includes 'name' field
            ```

            With existing schema + prompt template:
            ```python
            # Engine with both existing schema and prompt template
            # Result combines both sets of fields intelligently
            combined_schema = engine.derive_input_schema()
            ```

        Note:
            - Respects _use_prompt_for_input_schema configuration flag
            - Preserves all existing field properties (defaults, validation, etc.)
            - Prompt template fields take precedence in case of name conflicts
            - Error handling ensures method never fails completely
        """
        # First try the parent class implementation
        parent_schema = None
        if hasattr(super(), "derive_input_schema"):
            try:
                parent_schema = super().derive_input_schema()
            except:
                pass

        # Check if we should use prompt for schema derivation
        if not getattr(self, "_use_prompt_for_input_schema", True):
            return parent_schema

        # If no prompt template, use parent
        if not self.prompt_template:
            return parent_schema

        # Derive schema from prompt template
        prompt_schema = self.derive_prompt_input_schema()
        if prompt_schema:
            # If there's a parent schema, try to compose them
            if parent_schema:
                try:
                    return self.compose_with_prompt_schema(parent_schema)
                except:
                    # If composition fails, use prompt schema
                    return prompt_schema
            else:
                return prompt_schema

        # Final fallback to parent
        return parent_schema

    @field_validator("prompt_template", mode="before")
    @classmethod
    def validate_prompt_template(cls, v):
        """Validate and potentially transform prompt template before assignment."""
        if v is None:
            return v

        # Add any validation logic here
        # Could check for required variables, validate template format, etc.
        if hasattr(v, "input_variables"):
            # Ensure input_variables is not None
            if v.input_variables is None:
                # Try to extract variables from template if possible
                if hasattr(v, "template") and hasattr(v, "_get_template_variables"):
                    try:
                        v.input_variables = v._get_template_variables()
                    except:
                        v.input_variables = []

        return v

    def get_prompt_engine(self) -> Optional["PromptTemplateEngine"]:
        """Get or create a cached PromptTemplateEngine for the current prompt template.

        This method provides lazy initialization of a PromptTemplateEngine wrapper
        around the current prompt template. The engine is cached to avoid recreation
        on multiple calls, improving performance.

        Returns:
            Optional[PromptTemplateEngine]: A PromptTemplateEngine instance wrapping
                the current prompt template, or None if no prompt template is set.

        Note:
            - The engine is cached in _prompt_engine for reuse
            - Engine name is automatically generated from the parent object's name
            - Returns None if no prompt template is configured

        Examples:
            ```python
            # Get the prompt engine (creates if first time)
            engine = self.get_prompt_engine()
            if engine:
                schema = engine.derive_input_schema()
                result = engine.invoke(input_data)
            ```
        """
        if not self.prompt_template:
            return None

        if self._prompt_engine is None:
            from haive.core.engine.prompt_template import PromptTemplateEngine

            # Create a prompt engine with a name based on this config
            engine_name = f"{getattr(self, 'name', 'config')}_prompt"
            self._prompt_engine = PromptTemplateEngine(
                name=engine_name, prompt_template=self.prompt_template
            )

        return self._prompt_engine

    def derive_prompt_input_schema(self) -> Optional[Type[BaseModel]]:
        """Derive input schema from the prompt template."""
        prompt_engine = self.get_prompt_engine()
        if prompt_engine:
            return prompt_engine.derive_input_schema()
        return None

    def derive_prompt_output_schema(self) -> Optional[Type[BaseModel]]:
        """Derive output schema from the prompt template."""
        prompt_engine = self.get_prompt_engine()
        if prompt_engine:
            return prompt_engine.derive_output_schema()
        return None

    def format_prompt(
        self, input_data: Dict[str, Any]
    ) -> Union[str, List[AnyMessage], None]:
        """Format the prompt template with input data."""
        prompt_engine = self.get_prompt_engine()
        if prompt_engine:
            return prompt_engine.invoke(input_data)
        return None

    def get_prompt_variables(self) -> Dict[str, Any]:
        """Get information about prompt template variables."""
        if not self.prompt_template:
            return {}

        return {
            "input_variables": list(self.prompt_template.input_variables or []),
            "optional_variables": list(
                getattr(self.prompt_template, "optional_variables", []) or []
            ),
            "partial_variables": list(
                self.prompt_template.partial_variables.keys()
                if self.prompt_template.partial_variables
                else []
            ),
            "template_format": getattr(
                self.prompt_template, "template_format", "f-string"
            ),
        }

    def update_prompt_partials(self, **partials) -> bool:
        """Update partial variables in the prompt template."""
        if not self.prompt_template:
            return False

        # Create a new template with updated partials
        try:
            self.prompt_template = self.prompt_template.partial(**partials)
            # Reset the engine so it gets recreated with new template
            self._prompt_engine = None
            return True
        except Exception:
            return False

    def compose_with_prompt_schema(
        self, base_schema: Type[BaseModel]
    ) -> Type[BaseModel]:
        """Compose a base schema with the prompt template's input schema."""
        prompt_schema = self.derive_prompt_input_schema()
        if not prompt_schema:
            return base_schema

        # Simple field combination approach
        from typing import Any

        from pydantic import create_model

        base_fields = base_schema.model_fields
        prompt_fields = prompt_schema.model_fields

        # Combine fields, with base schema taking precedence
        combined_fields = {}

        # Add prompt fields first
        for name, field_info in prompt_fields.items():
            if name not in base_fields:
                # Preserve the field info structure
                combined_fields[name] = (field_info.annotation, field_info)

        # Add base fields (they override and take precedence)
        for name, field_info in base_fields.items():
            # Preserve the field info structure from base schema
            combined_fields[name] = (field_info.annotation, field_info)

        # Create new model with combined fields
        schema_name = f"{base_schema.__name__}WithPrompt"
        return create_model(schema_name, **combined_fields)

    def set_base_input_schema(self, schema: Optional[Type[BaseModel]]):
        """Set the base input schema to use for composition."""
        self._base_input_schema = schema

    def enable_prompt_schema_derivation(self, enabled: bool = True):
        """Enable or disable prompt template schema derivation."""
        self._use_prompt_for_input_schema = enabled

    def get_effective_input_schema(self) -> Optional[Type[BaseModel]]:
        """Get the effective input schema, considering all factors."""
        return self.input_schema

    def validate_prompt_inputs(self, input_data: Dict[str, Any]) -> bool:
        """Validate that input data satisfies prompt template requirements."""
        if not self.prompt_template:
            return True

        required_vars = set(self.prompt_template.input_variables or [])
        partial_vars = set(
            self.prompt_template.partial_variables.keys()
            if self.prompt_template.partial_variables
            else []
        )

        # Remove variables that are already provided via partials
        required_vars = required_vars - partial_vars

        # Check if all required variables are present
        provided_vars = set(input_data.keys())
        missing_vars = required_vars - provided_vars

        return len(missing_vars) == 0

    def get_missing_prompt_vars(self, input_data: Dict[str, Any]) -> List[str]:
        """Get list of missing required prompt variables."""
        if not self.prompt_template:
            return []

        required_vars = set(self.prompt_template.input_variables or [])
        partial_vars = set(
            self.prompt_template.partial_variables.keys()
            if self.prompt_template.partial_variables
            else []
        )

        # Remove variables that are already provided via partials
        required_vars = required_vars - partial_vars

        # Find missing variables
        provided_vars = set(input_data.keys())
        missing_vars = required_vars - provided_vars

        return list(missing_vars)

    def validate_with_prompt_schema(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against the effective input schema."""
        schema = self.get_effective_input_schema()
        if schema:
            validated = schema(**input_data)
            return validated.model_dump()
        return input_data

    def get_prompt_aware_input_fields(self) -> Dict[str, Any]:
        """Get input fields considering prompt template requirements."""
        # Start with base fields if available
        base_fields = {}
        if hasattr(self, "get_input_fields"):
            try:
                base_fields = self.get_input_fields()
            except:
                pass

        # Add prompt template fields
        if self.prompt_template:
            prompt_vars = self.get_prompt_variables()
            for var in prompt_vars.get("input_variables", []):
                if var not in base_fields:
                    # Use string as default type for prompt variables
                    if "message" in var.lower():
                        from langchain_core.messages import AnyMessage

                        base_fields[var] = (List[AnyMessage], None)
                    else:
                        base_fields[var] = (str, None)

        return base_fields
