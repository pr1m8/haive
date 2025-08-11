{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🛠️ Tool Function: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-success sd-text-white

   **Tool Function**: {{ objname }}

   .. autofunction:: {{ objname }}

.. tab-set::

   .. tab-item:: 🔧 Details
      :sync: details

      .. rubric:: Tool Information

      .. list-table::
         :class: sd-table-hover
         :widths: 30 70

         * - **Module**
           - ``{{ module }}``
         * - **Function**
           - ``{{ objname }}``
         * - **Type**
           - Tool Function
         * - **Import**
           - ``from {{ module }} import {{ objname }}``

   .. tab-item:: 🚀 Usage
      :sync: usage

      .. rubric:: Tool Usage

      .. code-block:: python
         :caption: Using {{ objname }} as a tool
         :linenos:

         from {{ module }} import {{ objname }}
         from haive.agents import ReactAgent

         # Method 1: Direct function call
         result = {{ objname }}(
             # Add parameters as needed
         )
         print(result)

         # Method 2: Use with ReactAgent
         agent = ReactAgent(
             name="tool_agent",
             tools=[{{ objname }}]  # Add function as tool
         )

         # Agent will use the tool automatically
         response = await agent.arun("Use the {{ objname }} tool to help me")

      .. dropdown:: 🧪 Test Tool Function
         :color: success
         :icon: play

         .. exec_code::
            :caption: Test {{ objname }} tool availability
            :linenos:

            # Test tool function import and signature
            try:
                from {{ module }} import {{ objname }}
                import inspect
                
                sig = inspect.signature({{ objname }})
                print(f"✅ Tool function available: {{ objname }}")
                print(f"📝 Signature: {{ objname }}{sig}")
                print(f"🔧 Parameters: {len(sig.parameters)}")
                
                # Check if it has tool decorators or metadata
                if hasattr({{ objname }}, '__annotations__'):
                    print("📋 Type hints available")
                
                if hasattr({{ objname }}, 'name'):
                    print(f"🏷️ Tool name: {{{ objname }}.name}")
                
                if hasattr({{ objname }}, 'description'):
                    print(f"📄 Description: {{{ objname }}.description}")
                
                # Check docstring for tool info
                doc = {{ objname }}.__doc__
                if doc and 'tool' in doc.lower():
                    print("🛠️ Appears to be a LangChain tool")
                
                # Show parameter details for tools
                for name, param in sig.parameters.items():
                    param_type = param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'Any'
                    default = f" = {param.default}" if param.default != inspect.Parameter.empty else ""
                    print(f"  • {name}: {param_type}{default}")
                    
            except Exception as e:
                print(f"ℹ️ Tool function info: {e}")

      .. admonition:: 🛠️ Tool Integration Tips
         :class: tip

         * Use with :tippy:`ReactAgent <ReactAgent automatically uses tools>` for automatic tool selection
         * Add to agent's :paramlink:`tools list <Tool functions integrate seamlessly>`
         * Check :emoji:`books` docstring for parameter requirements
         * Use :emoji:`test_tube` type hints for better validation

   .. tab-item:: 🔌 Integration
      :sync: integration

      .. rubric:: Agent Integration

      .. dropdown:: 🤖 ReactAgent Integration
         :color: primary
         :icon: robot

         .. code-block:: python
            :caption: ReactAgent with {{ objname }} tool
            :linenos:

            from {{ module }} import {{ objname }}
            from haive.agents import ReactAgent
            from haive.core.engine import AugLLMConfig

            # Create agent with tool
            config = AugLLMConfig(temperature=0.7, max_tokens=1000)
            agent = ReactAgent(
                name="tool_user",
                engine=config,
                tools=[{{ objname }}]  # Tool automatically available
            )

            # Agent can now use the tool
            result = await agent.arun(
                "Please use the {{ objname }} tool to help with this task"
            )

      .. dropdown:: 🔧 Custom Tool Wrapper
         :color: info
         :icon: wrench

         .. code-block:: python
            :caption: Creating custom tool wrapper
            :linenos:

            from langchain_core.tools import tool
            from {{ module }} import {{ objname }}

            @tool
            def enhanced_{{ objname }}(input_text: str) -> str:
                """Enhanced wrapper for {{ objname }} with additional features."""
                try:
                    # Pre-processing
                    processed_input = preprocess(input_text)
                    
                    # Call original tool
                    result = {{ objname }}(processed_input)
                    
                    # Post-processing
                    enhanced_result = postprocess(result)
                    return enhanced_result
                    
                except Exception as e:
                    return f"Tool error: {e}"

      .. dropdown:: ⚡ Performance Optimization
         :color: warning
         :icon: zap

         **Tool Performance Tips:**

         * **Caching**: Cache results for expensive operations
         * **Batching**: Process multiple inputs together when possible  
         * **Async**: Use async versions for I/O-bound tools
         * **Timeout**: Set reasonable timeouts for external calls

         .. code-block:: python
            :caption: Optimized tool usage
            :linenos:

            import asyncio
            from functools import lru_cache

            # Cached version for expensive computations
            @lru_cache(maxsize=128)
            def cached_{{ objname }}(input_data):
                return {{ objname }}(input_data)

            # Async version for I/O operations
            async def async_{{ objname }}(input_data):
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, {{ objname }}, input_data)

   .. tab-item:: 📊 Examples
      :sync: examples

      .. rubric:: Usage Examples

      .. dropdown:: 💡 Common Use Cases
         :color: info
         :icon: lightbulb

         **Direct Function Call:**
         ```python
         from {{ module }} import {{ objname }}
         
         # Simple usage
         result = {{ objname }}("input data")
         print(result)
         
         # With error handling
         try:
             result = {{ objname }}("input data")
             if result:
                 print(f"Success: {result}")
             else:
                 print("No result returned")
         except Exception as e:
             print(f"Tool error: {e}")
         ```

         **Agent Integration:**
         ```python
         from haive.agents import ReactAgent
         
         agent = ReactAgent(
             name="assistant",
             tools=[{{ objname }}]
         )
         
         # Agent decides when to use the tool
         response = await agent.arun(
             "Help me with this task using available tools"
         )
         ```

      .. exec_code::
         :caption: Tool function demonstration
         :linenos:

         # Demonstrate tool function capabilities
         try:
             from {{ module }} import {{ objname }}
             import json
             
             print(f"🛠️ Tool Function Demo: {{ objname }}")
             print("=" * 40)
             
             # Function metadata
             func_name = {{ objname }}.__name__
             func_doc = {{ objname }}.__doc__ or "No description available"
             
             print(f"📋 Name: {func_name}")
             print(f"📄 Description: {func_doc[:100]}...")
             
             # Check if it's a LangChain tool
             is_tool = hasattr({{ objname }}, 'name') and hasattr({{ objname }}, 'description')
             print(f"🔧 LangChain Tool: {'Yes' if is_tool else 'No'}")
             
             if is_tool:
                 print(f"🏷️ Tool Name: {{{ objname }}.name}")
                 print(f"📝 Tool Description: {{{ objname }}.description}")
             
             # Parameter analysis
             import inspect
             sig = inspect.signature({{ objname }})
             params = list(sig.parameters.keys())
             
             print(f"🔢 Parameters ({len(params)}): {', '.join(params[:3])}")
             
             # Return type
             return_annotation = sig.return_annotation
             if return_annotation != inspect.Signature.empty:
                 return_type = return_annotation.__name__ if hasattr(return_annotation, '__name__') else str(return_annotation)
                 print(f"📤 Returns: {return_type}")
             
             print("\n✅ Tool function is documented and ready for use!")
             
         except Exception as e:
             print(f"ℹ️ Tool function demo: {e}")
             print("🛠️ Function is available for documentation")

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 📖 Documentation
      :shadow: sm
      :class-header: sd-bg-info sd-text-white
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - Module docs
      * :doc:`/examples/tools` - Tool examples

   .. grid-item-card:: 🤖 Agent Usage
      :shadow: sm  
      :class-header: sd-bg-primary sd-text-white
      
      * :doc:`/agents/react` - ReactAgent guide
      * :doc:`/guides/tool-integration` - Tool setup

   .. grid-item-card:: 🔧 Development
      :shadow: sm
      :class-header: sd-bg-success sd-text-white
      
      * :doc:`/development/tools` - Tool development
      * :doc:`/api/langchain-tools` - LangChain tools

   .. grid-item-card:: 🚀 Performance
      :shadow: sm
      :class-header: sd-bg-warning sd-text-dark
      
      * Caching strategies
      * Async optimization
      * Timeout handling

   .. grid-item-card:: 🔗 Integration
      :shadow: sm
      :class-header: sd-bg-secondary sd-text-white
      
      * :issue:`tool-features` - Tool requests
      * :pr:`tool-improvements` - Updates

   .. grid-item-card:: 📊 Analytics
      :shadow: sm
      :class-header: sd-bg-dark sd-text-white
      
      * Usage metrics
      * Performance stats
      * Error tracking

.. req:: Tool Function Requirements  
   :id: REQ_TOOL_{{ objname.upper() }}_001
   :status: documented
   :priority: high
   :tags: tool, function, {{ objname.lower() }}

   Tool function {{ objname }} should integrate seamlessly with agents and provide clear usage documentation.

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Module documentation
   * :doc:`/tools/index` - Tool documentation hub
   * :doc:`/agents/react` - ReactAgent integration guide
   * :doc:`/examples/tools` - Tool usage examples
   * :doc:`/development/tools` - Tool development guide

.. last-updated:: {{ fullname }}
   :format: Tool function documented: %Y-%m-%d %H:%M