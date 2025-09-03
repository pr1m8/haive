{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🔧 Object: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-secondary sd-text-white

   **Object**: {{ objname }}

   .. autodata:: {{ objname }}

.. tab-set::

   .. tab-item:: Details
      :sync: details

      .. rubric:: Object Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Module**
           - ``{{ module }}``
         * - **Object Name**
           - ``{{ objname }}``
         * - **Full Path**
           - ``{{ fullname }}``
         * - **Import**
           - ``from {{ module }} import {{ objname }}``

   .. tab-item:: Usage
      :sync: usage

      .. rubric:: Object Access

      .. code-block:: python
         :caption: Accessing {{ objname }}
         :linenos:

         # Import the object
         from {{ module }} import {{ objname }}

         # Use the object
         print(f"Object: {{{ objname }}}")
         print(f"Type: {type({{ objname }}).__name__}")

         # Check if callable
         if callable({{ objname }}):
             print("✅ Object is callable")
             # result = {{ objname }}()  # Call if needed
         else:
             print("ℹ️ Object is not callable")

      .. dropdown:: 🧪 Inspect Object
         :color: success
         :icon: play

         .. exec_code::
            :caption: Inspect {{ objname }} object
            :linenos:

            # Comprehensive object inspection
            try:
                from {{ module }} import {{ objname }}
                import inspect
                
                print(f"🔍 Object Analysis: {{ objname }}")
                print(f"🏷️ Type: {type({{ objname }}).__name__}")
                print(f"📦 Module: {getattr({{ objname }}, '__module__', 'Unknown')}")
                
                # Check object category
                if callable({{ objname }}):
                    print("📞 Category: Callable")
                    if hasattr({{ objname }}, '__call__'):
                        try:
                            sig = inspect.signature({{ objname }})
                            print(f"📝 Signature: {{ objname }}{sig}")
                        except (ValueError, TypeError):
                            print("📝 Signature: Not available")
                elif hasattr({{ objname }}, '__class__') and hasattr({{ objname }}.__class__, '__name__'):
                    if {{ objname }}.__class__.__name__ in ['type', 'ABCMeta']:
                        print("🏗️ Category: Class/Type")
                    else:
                        print("📦 Category: Instance")
                else:
                    print("📊 Category: Data/Value")
                
                # Show attributes (top 10)
                attrs = [attr for attr in dir({{ objname }}) if not attr.startswith('_')]
                if attrs:
                    print(f"🔧 Public attributes ({min(10, len(attrs))}):")
                    for attr in attrs[:10]:
                        attr_type = type(getattr({{ objname }}, attr, None)).__name__
                        print(f"  • {attr} ({attr_type})")
                
                # Check for documentation
                doc = getattr({{ objname }}, '__doc__', None)
                if doc and doc.strip():
                    print("📚 Has documentation: Yes")
                    print(f"📄 Doc preview: {doc.strip()[:100]}...")
                else:
                    print("📚 Has documentation: No")
                
                # Memory usage
                import sys
                size = sys.getsizeof({{ objname }})
                print(f"💾 Memory size: {size} bytes")
                
            except Exception as e:
                print(f"ℹ️ Object inspection: {e}")

      .. admonition:: 🔍 Object Analysis
         :class: tip

         * Use :tippy:`type() <Check object type>` to determine the object's type
         * Check :tippy:`callable() <Test if object is callable>` to see if it can be invoked
         * Use :emoji:`magnifying_glass` :tippy:`dir() <List object attributes>` to explore available attributes
         * Read :emoji:`books` ``__doc__`` attribute for documentation

   .. tab-item:: Type Info
      :sync: type_info

      .. rubric:: Type Analysis

      .. dropdown:: 🏷️ Object Type Details
         :color: info
         :icon: tag

         .. autorun::

            # Detailed type analysis
            try:
                from {{ module }} import {{ objname }}
                import inspect
                
                obj_type = type({{ objname }})
                print(f"🎯 Type Analysis for {{ objname }}:")
                print(f"  📋 Type: {obj_type.__name__}")
                print(f"  📦 Type module: {obj_type.__module__}")
                
                # Check inheritance (if it's a class)
                if inspect.isclass({{ objname }}):
                    mro = {{ objname }}.__mro__[1:]  # Exclude self
                    if mro:
                        print(f"  🧬 Inherits from: {', '.join(cls.__name__ for cls in mro[:3])}")
                
                # Check if it has special methods
                special_methods = [attr for attr in dir({{ objname }}) 
                                 if attr.startswith('__') and attr.endswith('__') and callable(getattr({{ objname }}, attr, None))]
                if special_methods:
                    print(f"  🔮 Special methods ({len(special_methods)}): {', '.join(special_methods[:5])}...")
                
                # Protocol support
                protocols = []
                if hasattr({{ objname }}, '__iter__'):
                    protocols.append("Iterable")
                if hasattr({{ objname }}, '__len__'):
                    protocols.append("Sized")
                if hasattr({{ objname }}, '__getitem__'):
                    protocols.append("Sequence/Mapping")
                if hasattr({{ objname }}, '__enter__'):
                    protocols.append("Context Manager")
                
                if protocols:
                    print(f"  🤝 Protocols: {', '.join(protocols)}")
                else:
                    print("  🤝 Protocols: None detected")
                
            except Exception as e:
                print(f"ℹ️ Type analysis: {e}")

      .. dropdown:: 🎯 Usage Patterns
         :color: secondary
         :icon: pattern

         **Common Object Patterns:**

         **Classes/Types**: Create instances or use as type hints
         ```python
         instance = {{ objname }}()  # If it's a class
         def func(param: {{ objname }}):  # Type hint usage
         ```

         **Functions**: Call with appropriate arguments
         ```python
         result = {{ objname }}(arg1, arg2)  # If it's a function
         ```

         **Data/Constants**: Use directly in expressions
         ```python
         if some_value == {{ objname }}:  # If it's a constant
             do_something()
         ```

         **Context Managers**: Use with 'with' statement (if supported)
         ```python
         with {{ objname }} as context:  # If it supports context management
             do_work()
         ```

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 📖 Documentation
      :shadow: sm
      :class-header: sd-bg-info sd-text-white
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - Module docs
      * :doc:`/examples/objects` - Object examples

   .. grid-item-card:: 🔗 Related
      :shadow: sm
      :class-header: sd-bg-success sd-text-white
      
      * :issue:`object-features` - Object requests
      * :pr:`object-improvements` - Recent updates

   .. grid-item-card:: 🧪 Testing
      :shadow: sm
      :class-header: sd-bg-warning sd-text-dark
      
      * Test object import and usage
      * Verify type and attributes
      * Check documentation completeness

   .. grid-item-card:: 🎯 Best Practices
      :shadow: sm
      :class-header: sd-bg-primary sd-text-white
      
      * Use type hints for better IDE support
      * Check callable() before invoking
      * Read docstrings for usage guidance

.. req:: Object Requirements
   :id: REQ_OBJ_{{ objname.upper() }}_001
   :status: documented
   :priority: medium
   :tags: object, {{ objname.lower() }}

   Object {{ objname }} should have clear type information and usage documentation.

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Module documentation
   * :doc:`/guides/objects` - Object usage guide
   * :doc:`/api/index` - Full API reference

.. last-updated:: {{ fullname }}
   :format: Object documented: %Y-%m-%d %H:%M