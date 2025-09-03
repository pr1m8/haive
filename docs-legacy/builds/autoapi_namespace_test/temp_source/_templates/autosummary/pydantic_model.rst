{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🔧 Pydantic Model: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-lg
   :class-header: sd-bg-info sd-text-white

   **Configuration Model**: {{ objname }}

   .. autopydantic_model:: {{ objname }}
      :model-show-json: False
      :model-show-config-summary: True
      :model-show-field-summary: True
      :model-show-validator-members: True
      :field-list-validators: True
      :field-show-constraints: True
      :field-show-default: True
      :field-show-required: True
      :show-inheritance: True
      :members:
      :undoc-members:

.. tab-set::

   .. tab-item:: Overview
      :sync: overview

      .. rubric:: Model Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Module**
           - ``{{ module }}``
         * - **Model**
           - ``{{ objname }}``
         * - **Import**
           - ``from {{ module }} import {{ objname }}``

      {% if bases %}
      .. rubric:: Inheritance

      .. inheritance-diagram:: {{ fullname }}
         :parts: 2
         :caption: {{ objname }} Model Hierarchy
      {% endif %}

   .. tab-item:: Usage
      :sync: usage

      .. rubric:: Basic Usage

      .. code-block:: python
         :caption: Creating {{ objname }} instance
         :linenos:

         from {{ module }} import {{ objname }}

         # Create model instance
         config = {{ objname }}(
             # Add fields as needed
         )

         # Validate and serialize
         print(config.model_dump())
         print(config.model_dump_json(indent=2))

      .. rubric:: Field Validation

      .. code-block:: python
         :caption: Field validation example
         :linenos:

         try:
             # This will validate all fields
             config = {{ objname }}(
                 # fields here
             )
             print("✅ Validation passed")
         except ValidationError as e:
             print("❌ Validation failed:")
             for error in e.errors():
                 print(f"  - {error['loc'][0]}: {error['msg']}")

   .. tab-item:: JSON Schema
      :sync: schema

      .. rubric:: Interactive JSON Schema

      .. jsonschema:: {{ fullname }}
         :lift_description: true
         :lift_definitions: true
         :auto_reference: true
         :examples:

      .. dropdown:: 📊 Live Schema Analysis
         :color: info
         :icon: graph

         .. autorun::

            from {{ module }} import {{ objname }}
            import json
            
            schema = {{ objname }}.model_json_schema()
            print(f"🔧 Schema for {{ objname }}:")
            print(f"📝 Properties: {len(schema.get('properties', {}))}")
            print(f"🔒 Required: {schema.get('required', [])}")
            print(f"📋 Type: {schema.get('type', 'object')}")
            
            # Show field details
            properties = schema.get('properties', {})
            for field_name, field_info in properties.items():
                field_type = field_info.get('type', 'unknown')
                print(f"  • {field_name}: {field_type}")

      .. admonition:: 🔗 Schema Integration
         :class: tip

         * Use the schema for API documentation (OpenAPI)
         * Generate forms from the schema  
         * Validate external data against the schema
         * :tippy:`Interactive validation <Click field names for validation details>`

.. dropdown:: 🧪 Live Validation Testing
   :color: primary
   :icon: flask

   .. exec_code::
      :caption: Interactive validation testing
      :linenos:

      # Live validation testing for {{ objname }}
      try:
          from {{ module }} import {{ objname }}
          from pydantic import ValidationError
          import inspect
          
          print(f"🔧 Testing {{ objname }} validation...")
          
          # Test 1: Model availability
          print(f"✅ Model class: {{{ objname }}.__name__}")
          
          # Test 2: Field inspection
          fields = {{ objname }}.model_fields
          print(f"📝 Model fields ({len(fields)}):")
          for name, field in fields.items():
              required = "🔒 Required" if field.is_required() else "🔓 Optional"
              print(f"  • {name}: {required}")
          
          # Test 3: Create with defaults
          try:
              default_instance = {{ objname }}()
              print(f"✅ Default instance created")
          except Exception as e:
              print(f"ℹ️ Requires parameters: {e}")
          
          # Test 4: Schema validation
          schema = {{ objname }}.model_json_schema()
          properties_count = len(schema.get('properties', {}))
          required_count = len(schema.get('required', []))
          print(f"📊 Schema: {properties_count} properties, {required_count} required")
          
      except Exception as e:
          print(f"ℹ️ Model info: {e}")

   .. dropdown:: 💻 Code Examples
      :color: secondary
      :icon: code

      .. code-block:: python
         :caption: Common validation patterns
         :linenos:

         from {{ module }} import {{ objname }}
         from pydantic import ValidationError
         import json

         # Example 1: Valid data
         try:
             valid_data = {
                 # Add example valid data
             }
             config = {{ objname }}(**valid_data)
             print("✅ Valid configuration created")
         except ValidationError as e:
             print(f"❌ Validation failed: {e}")

         # Example 2: From JSON string
         json_str = '{"field": "value"}'  # Replace with actual JSON
         try:
             config = {{ objname }}.model_validate_json(json_str)
             print("✅ Loaded from JSON")
         except ValidationError as e:
             print(f"❌ JSON validation failed: {e}")

         # Example 3: Field updates
         config = {{ objname }}()  # Default values
         updated_config = config.model_copy(update={"field": "new_value"})
         print(f"Updated config: {updated_config}")

.. admonition:: 📋 Model Features
   :class: note

   This Pydantic model provides:

   * **Type Safety**: All fields are type-checked at runtime
   * **Validation**: Built-in and custom validators ensure data integrity
   * **Serialization**: Easy conversion to JSON, dict, and other formats
   * **Documentation**: Self-documenting with field descriptions and constraints
   * **IDE Support**: Full autocomplete and type hints in modern IDEs

.. seealso::

   * `Pydantic Documentation <https://docs.pydantic.dev/latest/>`_ - Official Pydantic docs
   * :doc:`/guides/configuration` - Configuration guide
   * :doc:`/api/{{ module.replace('.', '/') }}` - Module documentation
   * :doc:`/examples/configuration` - Configuration examples