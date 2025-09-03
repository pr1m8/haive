{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🏷️ Property: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-warning sd-text-white

   **Property**: {{ objname }}

   .. autoproperty:: {{ objname }}

.. tab-set::

   .. tab-item:: Details
      :sync: details

      .. rubric:: Property Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Class**
           - ``{{ module.split('.')[-1] }}``
         * - **Property**
           - ``{{ objname }}``
         * - **Type**
           - Property (getter/setter)
         * - **Full Path**
           - ``{{ fullname }}``

   .. tab-item:: Usage
      :sync: usage

      .. rubric:: Property Access

      .. code-block:: python
         :caption: Accessing {{ objname }} property
         :linenos:

         # Import the class
         from {{ module }} import {{ module.split('.')[-1] }}

         # Create instance
         instance = {{ module.split('.')[-1] }}()

         # Access the property (getter)
         value = instance.{{ objname }}
         print(f"Property value: {value}")

         # Set the property (if setter exists)
         try:
             instance.{{ objname }} = new_value
             print("✅ Property is writable")
         except AttributeError:
             print("ℹ️ Property is read-only")

      .. dropdown:: 🧪 Test Property
         :color: success
         :icon: play

         .. exec_code::
            :caption: Test {{ objname }} property
            :linenos:

            # Test property availability and type
            try:
                from {{ module }} import {{ module.split('.')[-1] }}
                import inspect
                
                cls = {{ module.split('.')[-1] }}
                if hasattr(cls, '{{ objname }}'):
                    prop = getattr(cls, '{{ objname }}')
                    print(f"✅ Property available: {{ objname }}")
                    print(f"🏷️ Type: {type(prop).__name__}")
                    
                    # Check if it's a property
                    if isinstance(prop, property):
                        print("📋 Property details:")
                        print(f"  🔍 Has getter: {prop.fget is not None}")
                        print(f"  ✏️ Has setter: {prop.fset is not None}")
                        print(f"  🗑️ Has deleter: {prop.fdel is not None}")
                        
                        if prop.fget:
                            sig = inspect.signature(prop.fget)
                            print(f"  📝 Getter signature: {sig}")
                    else:
                        print(f"ℹ️ {{ objname }} is a {type(prop).__name__}")
                else:
                    print(f"⚠️ Property {{ objname }} not found")
                    
            except Exception as e:
                print(f"ℹ️ Property info: {e}")

      .. admonition:: 🔒 Property Access
         :class: tip

         * Use :tippy:`dot notation <instance.property>` to access property values
         * Check if property is :emoji:`lock` read-only or :emoji:`edit` writable
         * Properties often use :emoji:`cached` caching for performance
         * Consider property :emoji:`chain` chaining in method calls

   .. tab-item:: Implementation
      :sync: impl

      .. rubric:: Property Implementation

      .. dropdown:: 📊 Property Behavior
         :color: info
         :icon: settings

         **Access Type**: Property (computed attribute)

         **Getter**: Retrieves the property value
         
         **Setter**: Sets the property value (if writable)

         **Performance**: Properties may cache values or compute them dynamically

      .. dropdown:: 🎯 Common Property Patterns
         :color: secondary
         :icon: pattern

         **Computed Property**: Value calculated from other attributes
         
         **Cached Property**: Value computed once and cached
         
         **Validated Property**: Value validated on assignment
         
         **Lazy Property**: Value computed only when first accessed

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 📖 Documentation
      :shadow: sm
      :class-header: sd-bg-info sd-text-white
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - Class docs
      * :doc:`/examples/properties` - Property examples

   .. grid-item-card:: 🔗 Related
      :shadow: sm
      :class-header: sd-bg-success sd-text-white
      
      * :issue:`property-features` - Property requests
      * :pr:`property-improvements` - Recent changes

.. req:: Property Requirements
   :id: REQ_PROP_{{ objname.upper() }}_001
   :status: documented
   :priority: medium
   :tags: property, {{ objname.lower() }}

   Property {{ objname }} should have clear getter/setter behavior documentation.

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Class documentation
   * :doc:`/guides/properties` - Property usage guide
   * :doc:`/api/index` - Full API reference

.. last-updated:: {{ fullname }}
   :format: Property documented: %Y-%m-%d %H:%M