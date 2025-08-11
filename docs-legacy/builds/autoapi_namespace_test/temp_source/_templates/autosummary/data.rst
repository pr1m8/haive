{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 📊 Data: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-secondary sd-text-white

   **Module Data**: {{ objname }}

   .. autodata:: {{ objname }}

.. tab-set::

   .. tab-item:: Details
      :sync: details

      .. rubric:: Data Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Module**
           - ``{{ module }}``
         * - **Data Name**
           - ``{{ objname }}``
         * - **Full Path**
           - ``{{ fullname }}``
         * - **Import**
           - ``from {{ module }} import {{ objname }}``

   .. tab-item:: Usage
      :sync: usage

      .. rubric:: Data Access

      .. code-block:: python
         :caption: Using {{ objname }} data
         :linenos:

         # Import the data
         from {{ module }} import {{ objname }}

         # Use the data
         print(f"Data value: {{{ objname }}}")
         print(f"Data type: {type({{ objname }}).__name__}")

         # Use in expressions
         if {{ objname }}:
             print("Data is truthy")

      .. dropdown:: 🧪 Inspect Data
         :color: success
         :icon: play

         .. exec_code::
            :caption: Inspect {{ objname }} data
            :linenos:

            # Inspect data value and properties
            try:
                from {{ module }} import {{ objname }}
                
                print(f"📊 Data name: {{ objname }}")
                print(f"🏷️ Type: {type({{ objname }}).__name__}")
                print(f"📏 Value: {repr({{ objname }})}")
                
                # Additional type information
                import sys
                print(f"💾 Size: {sys.getsizeof({{ objname }})} bytes")
                
                # Check if it's a constant (uppercase)
                if '{{ objname }}'.isupper():
                    print("🔒 Appears to be a constant")
                else:
                    print("🔧 Appears to be a variable")
                
                # Check if it's mutable
                try:
                    hash({{ objname }})
                    print("🔗 Hashable (immutable)")
                except TypeError:
                    print("📝 Not hashable (mutable)")
                    
            except Exception as e:
                print(f"ℹ️ Data info: {e}")

      .. admonition:: 📋 Data Usage Tips
         :class: tip

         * Import data directly: ``from {{ module }} import {{ objname }}``
         * Check data type with :tippy:`type() <Built-in type checking>`
         * Constants are typically :emoji:`lock` UPPERCASE
         * Variables may be :emoji:`edit` mutable or :emoji:`shield` immutable

   .. tab-item:: Context
      :sync: context

      .. rubric:: Data Context

      .. dropdown:: 📚 Data Categories
         :color: info
         :icon: list

         **Constants**: Fixed values that don't change
         ```python
         # Example constants
         DEFAULT_TIMEOUT = 30
         MAX_RETRIES = 3
         API_VERSION = "v1"
         ```

         **Configuration**: Settings and options
         ```python
         # Example configuration
         DEFAULT_CONFIG = {
             "setting": "value",
             "enabled": True
         }
         ```

         **Type Aliases**: Alternative names for types
         ```python
         # Example type aliases
         from typing import Dict, Any
         ConfigDict = Dict[str, Any]
         ```

      .. dropdown:: 🎯 Best Practices
         :color: warning
         :icon: best-practice

         * **Constants**: Use UPPERCASE names
         * **Private data**: Prefix with underscore
         * **Type hints**: Add type annotations
         * **Documentation**: Include docstrings for complex data

.. autorun::

   # Show data usage statistics
   try:
       from {{ module }} import {{ objname }}
       
       print(f"🎯 Data Analysis for {{ objname }}:")
       print(f"  📊 Type: {type({{ objname }}).__name__}")
       
       # Show value summary
       value_str = str({{ objname }})
       if len(value_str) > 100:
           value_str = value_str[:100] + "..."
       print(f"  💼 Value: {value_str}")
       
       # Check common data patterns
       if isinstance({{ objname }}, (str, int, float, bool)):
           print(f"  🔤 Primitive type: {type({{ objname }}).__name__}")
       elif isinstance({{ objname }}, (list, tuple, set)):
           print(f"  📝 Collection with {len({{ objname }})} items")
       elif isinstance({{ objname }}, dict):
           print(f"  📚 Dictionary with {len({{ objname }})} keys")
       else:
           print(f"  🔧 Complex type: {type({{ objname }}).__name__}")
           
   except Exception as e:
       print(f"ℹ️ Data analysis not available: {e}")

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 📖 Documentation
      :shadow: sm
      :class-header: sd-bg-info sd-text-white
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - Module docs
      * :doc:`/examples/constants` - Data examples

   .. grid-item-card:: 🔗 Related
      :shadow: sm
      :class-header: sd-bg-success sd-text-white
      
      * :issue:`data-constants` - Data requests
      * :pr:`data-improvements` - Recent updates

.. req:: Data Requirements
   :id: REQ_DATA_{{ objname.upper() }}_001
   :status: documented
   :priority: low
   :tags: data, constant, {{ objname.lower() }}

   Module data {{ objname }} should have clear type information and usage examples.

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Module documentation
   * :doc:`/guides/constants` - Constants and data guide
   * :doc:`/api/index` - Full API reference

.. last-updated:: {{ fullname }}
   :format: Data documented: %Y-%m-%d %H:%M