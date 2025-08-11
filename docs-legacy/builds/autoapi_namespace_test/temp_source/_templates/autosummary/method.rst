{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🔧 Method: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-info sd-text-white

   **Method**: {{ objname }}

   .. automethod:: {{ objname }}

.. tab-set::

   .. tab-item:: Details
      :sync: details

      .. rubric:: Method Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Class**
           - ``{{ module.split('.')[-1] }}``
         * - **Method**
           - ``{{ objname }}``
         * - **Full Path**
           - ``{{ fullname }}``

   .. tab-item:: Usage
      :sync: usage

      .. rubric:: Method Usage

      .. code-block:: python
         :caption: Using {{ objname }} method
         :linenos:

         # Import the class
         from {{ module }} import {{ module.split('.')[-1] }}

         # Create instance
         instance = {{ module.split('.')[-1] }}()

         # Call the method
         result = instance.{{ objname }}(
             # Add parameters as needed
         )
         print(result)

      .. dropdown:: 🧪 Test Method
         :color: success
         :icon: play

         .. exec_code::
            :caption: Test {{ objname }} availability
            :linenos:

            # Test method availability and signature
            try:
                from {{ module }} import {{ module.split('.')[-1] }}
                import inspect
                
                cls = {{ module.split('.')[-1] }}
                if hasattr(cls, '{{ objname }}'):
                    method = getattr(cls, '{{ objname }}')
                    if callable(method):
                        sig = inspect.signature(method)
                        print(f"✅ Method available: {{ objname }}")
                        print(f"📝 Signature: {{ objname }}{sig}")
                        print(f"🔧 Type: {type(method).__name__}")
                    else:
                        print(f"ℹ️ {{ objname }} is not callable")
                else:
                    print(f"⚠️ Method {{ objname }} not found")
                    
            except Exception as e:
                print(f"ℹ️ Method info: {e}")

      .. admonition:: 💡 Method Tips
         :class: tip

         * Check the :paramlink:`method signature <Parameters link to detailed docs>` for required parameters
         * Use :tippy:`type hints <Method type hints improve IDE support>` for better development
         * Read the :emoji:`books` docstring for parameter descriptions
         * Consider method :emoji:`chain` chaining if applicable

   .. tab-item:: Implementation
      :sync: impl

      .. rubric:: Method Implementation

      .. dropdown:: 📋 Method Details
         :color: info
         :icon: info

         **Method Type**: Instance Method

         **Return Type**: Check the method signature for return type annotations

         **Parameters**: Refer to the method signature above

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Class documentation
   * :doc:`/api/index` - Full API reference
   * :doc:`/examples/index` - Usage examples

.. req:: Method Requirements
   :id: REQ_METHOD_{{ objname.upper() }}_001
   :status: documented
   :priority: medium
   :tags: method, {{ objname.lower() }}

   Method {{ objname }} should have complete documentation including parameters, return values, and examples.

.. last-updated:: {{ fullname }}
   :format: Method documented: %Y-%m-%d %H:%M