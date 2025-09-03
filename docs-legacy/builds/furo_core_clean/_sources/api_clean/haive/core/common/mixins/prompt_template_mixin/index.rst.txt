
haive.core.common.mixins.prompt_template_mixin
==============================================

.. py:module:: haive.core.common.mixins.prompt_template_mixin

.. autoapi-nested-parse::

   PromptTemplateMixin: Advanced prompt template integration for engine classes.

   from typing import Any
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

   .. admonition:: Example

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

   .. seealso::

      - haive.core.engine.prompt_template.PromptTemplateEngine: Standalone engine
      - haive.core.engine.aug_llm.config.AugLLMConfig: Primary integration target
      - haive.core.schema.schema_composer.SchemaComposer: Schema composition utilities







Classes
-------

* :py:class:`PromptTemplateMixin` - Advanced mixin for integrating prompt template functionality into engine classes.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/prompt_template_mixin/PromptTemplateMixin

Package Contents
----------------

