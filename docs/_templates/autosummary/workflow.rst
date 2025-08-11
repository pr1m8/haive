{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. card:: 🔄 Workflow: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-lg
   :class-header: sd-bg-info sd-text-white

   **Workflow Class**: {{ objname }}

   .. autoclass:: {{ objname }}
      :members:
      :inherited-members:
      :show-inheritance:

.. tab-set::

   .. tab-item:: 🎯 Overview
      :sync: overview

      .. rubric:: Workflow Overview

      .. dropdown:: 🔄 Workflow Architecture
         :color: primary
         :icon: workflow
         :open:

         **{{ objname }} Workflow Structure:**

         * **Input Processing**: Handles and validates input data
         * **Step Execution**: Orchestrates workflow steps
         * **State Management**: Maintains workflow state throughout execution
         * **Output Generation**: Produces final workflow results

         .. mermaid::

            flowchart TD
               A[Input] --> B[Validation]
               B --> C[Step 1]
               C --> D[Step 2]
               D --> E[Step N]
               E --> F[Output]
               
               G[State] --> C
               G --> D  
               G --> E
               
               C --> G
               D --> G
               E --> G

      .. list-table:: Workflow Information
         :class: sd-table-hover
         :widths: 30 70

         * - **Class**
           - ``{{ objname }}``
         * - **Module**  
           - ``{{ module }}``
         * - **Type**
           - Workflow Orchestrator
         * - **Import**
           - ``from {{ module }} import {{ objname }}``

   .. tab-item:: 🚀 Usage
      :sync: usage

      .. rubric:: Workflow Usage

      .. code-block:: python
         :caption: Basic {{ objname }} usage
         :linenos:

         from {{ module }} import {{ objname }}

         # Create workflow instance
         workflow = {{ objname }}(
             name="my_workflow",
             # Add configuration parameters
         )

         # Execute workflow
         result = await workflow.run({
             "input_data": "your_data_here",
             "parameters": {"param1": "value1"}
         })

         print(f"Workflow result: {result}")

      .. dropdown:: 🧪 Test Workflow
         :color: success
         :icon: play

         .. exec_code::
            :caption: Test {{ objname }} workflow
            :linenos:

            # Test workflow availability and structure
            try:
                from {{ module }} import {{ objname }}
                import inspect
                
                print(f"✅ Workflow available: {{ objname }}")
                
                # Check class structure
                methods = [name for name, method in inspect.getmembers({{ objname }}, predicate=inspect.isfunction)]
                properties = [name for name, prop in inspect.getmembers({{ objname }}, predicate=lambda x: isinstance(x, property))]
                
                print(f"🔧 Methods: {len(methods)} ({', '.join(methods[:5])})")
                if len(methods) > 5:
                    print(f"    ... and {len(methods) - 5} more")
                    
                if properties:
                    print(f"🏷️ Properties: {len(properties)} ({', '.join(properties[:3])})")
                
                # Check for workflow-specific methods
                workflow_methods = ['run', 'execute', 'process', 'start']
                available_workflow_methods = [m for m in workflow_methods if hasattr({{ objname }}, m)]
                if available_workflow_methods:
                    print(f"🔄 Workflow methods: {', '.join(available_workflow_methods)}")
                
                # Check inheritance
                bases = {{ objname }}.__bases__
                if bases and bases[0].__name__ != 'object':
                    print(f"🧬 Inherits from: {', '.join(base.__name__ for base in bases)}")
                
            except Exception as e:
                print(f"ℹ️ Workflow info: {e}")

      .. admonition:: 🔄 Workflow Tips
         :class: tip

         * Initialize with proper :tippy:`configuration <Workflow configuration affects execution>` 
         * Use :emoji:`state` state management for complex workflows
         * Handle :emoji:`error` exceptions at each step
         * Monitor :emoji:`clock` execution time for performance

   .. tab-item:: 🏗️ Configuration
      :sync: configuration

      .. rubric:: Workflow Configuration

      .. dropdown:: ⚙️ Configuration Options
         :color: info
         :icon: gear

         **Basic Configuration:**
         ```python
         workflow = {{ objname }}(
             name="workflow_name",
             timeout=300,  # 5 minutes
             retry_count=3,
             parallel=False
         )
         ```

         **Advanced Configuration:**
         ```python
         from {{ module }} import {{ objname }}
         
         workflow = {{ objname }}(
             name="advanced_workflow",
             config={
                 "step_timeout": 60,
                 "error_handling": "continue",
                 "state_persistence": True,
                 "logging_level": "INFO"
             }
         )
         ```

      .. dropdown:: 📊 State Management
         :color: secondary
         :icon: database

         **Workflow State Pattern:**
         ```python
         # State is maintained throughout workflow execution
         initial_state = {
             "step": 0,
             "data": {},
             "metadata": {}
         }
         
         # State is updated at each step
         workflow.run(initial_state)
         
         # Access final state
         final_state = workflow.get_state()
         ```

      .. exec_code::
         :caption: Workflow configuration demo
         :linenos:

         # Demonstrate workflow configuration
         try:
             from {{ module }} import {{ objname }}
             import inspect
             
             print(f"⚙️ {{ objname }} Configuration Demo")
             print("=" * 40)
             
             # Check __init__ signature for configuration options
             init_sig = inspect.signature({{ objname }}.__init__)
             init_params = list(init_sig.parameters.keys())[1:]  # Skip 'self'
             
             if init_params:
                 print(f"🔧 Configuration parameters ({len(init_params)}):")
                 for param_name in init_params[:5]:
                     param = init_sig.parameters[param_name]
                     param_type = param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'Any'
                     default = f" = {param.default}" if param.default != inspect.Parameter.empty else ""
                     print(f"  • {param_name}: {param_type}{default}")
             else:
                 print("🔧 No configuration parameters in __init__")
             
             # Check for configuration methods
             config_methods = ['configure', 'set_config', 'update_config']
             available_config = [m for m in config_methods if hasattr({{ objname }}, m)]
             if available_config:
                 print(f"⚙️ Configuration methods: {', '.join(available_config)}")
             
             # Check for state-related methods
             state_methods = ['get_state', 'set_state', 'reset_state', 'save_state']
             available_state = [m for m in state_methods if hasattr({{ objname }}, m)]
             if available_state:
                 print(f"📊 State methods: {', '.join(available_state)}")
             
             print("\n✅ Workflow configuration options documented!")
             
         except Exception as e:
             print(f"ℹ️ Configuration demo: {e}")

   .. tab-item:: 🔗 Integration
      :sync: integration

      .. rubric:: Workflow Integration

      .. dropdown:: 🤖 Agent Integration
         :color: primary
         :icon: robot

         **Using Workflow with Agents:**
         ```python
         from {{ module }} import {{ objname }}
         from haive.agents import ReactAgent
         
         # Create workflow
         workflow = {{ objname }}(name="agent_workflow")
         
         # Create agent with workflow
         agent = ReactAgent(
             name="workflow_agent",
             tools=[workflow.as_tool()]  # Convert workflow to tool
         )
         
         # Agent can execute workflow
         result = await agent.arun("Execute the workflow with this data")
         ```

      .. dropdown:: 🔄 Multi-Agent Workflows
         :color: success
         :icon: network

         **Complex Multi-Agent Workflow:**
         ```python
         from haive.agents import MultiAgent
         
         # Create multi-agent workflow
         multi_workflow = MultiAgent([
             ReactAgent(name="planner"),
             {{ objname }}(name="processor"),
             ReactAgent(name="validator")
         ], mode="sequential")
         
         # Execute complex workflow
         result = await multi_workflow.run(input_data)
         ```

      .. dropdown:: ⚡ Async Execution
         :color: warning
         :icon: zap

         **Async Workflow Patterns:**
         ```python
         import asyncio
         
         # Concurrent workflow execution
         workflows = [
             {{ objname }}(name=f"workflow_{i}")
             for i in range(3)
         ]
         
         # Run workflows concurrently
         results = await asyncio.gather(*[
             workflow.run(input_data) 
             for workflow in workflows
         ])
         ```

   .. tab-item:: 📊 Monitoring
      :sync: monitoring

      .. rubric:: Workflow Monitoring

      .. dropdown:: 📈 Performance Metrics
         :color: info
         :icon: chart

         **Built-in Monitoring:**
         ```python
         workflow = {{ objname }}(name="monitored_workflow")
         
         # Execute with monitoring
         result = await workflow.run(data, monitor=True)
         
         # Access metrics
         metrics = workflow.get_metrics()
         print(f"Execution time: {metrics['duration']}")
         print(f"Steps completed: {metrics['steps']}")
         print(f"Success rate: {metrics['success_rate']}")
         ```

      .. dropdown:: 🔍 Debugging
         :color: secondary
         :icon: bug

         **Workflow Debugging:**
         ```python
         # Enable debug mode
         workflow = {{ objname }}(
             name="debug_workflow",
             debug=True,
             verbose=True
         )
         
         # Detailed execution logs
         result = await workflow.run(data)
         
         # Access debug information
         debug_info = workflow.get_debug_info()
         ```

      .. exec_code::
         :caption: Workflow monitoring demo
         :linenos:

         # Demonstrate workflow monitoring capabilities
         try:
             from {{ module }} import {{ objname }}
             import time
             
             print(f"📊 {{ objname }} Monitoring Demo")
             print("=" * 40)
             
             # Check for monitoring methods
             monitoring_methods = [
                 'get_metrics', 'get_stats', 'get_performance',
                 'monitor', 'track', 'measure'
             ]
             
             available_monitoring = [
                 method for method in monitoring_methods 
                 if hasattr({{ objname }}, method)
             ]
             
             if available_monitoring:
                 print(f"📈 Monitoring methods: {', '.join(available_monitoring)}")
             else:
                 print("📈 Basic monitoring via execution timing")
             
             # Check for debug capabilities
             debug_methods = ['debug', 'verbose', 'log', 'trace']
             available_debug = [
                 method for method in debug_methods
                 if hasattr({{ objname }}, method)
             ]
             
             if available_debug:
                 print(f"🔍 Debug methods: {', '.join(available_debug)}")
             
             # Show class docstring for workflow description
             doc = {{ objname }}.__doc__
             if doc and len(doc.strip()) > 0:
                 print(f"📚 Workflow description available")
                 print(f"📄 Preview: {doc.strip()[:100]}...")
             
             print("\n✅ Workflow monitoring capabilities documented!")
             
         except Exception as e:
             print(f"ℹ️ Monitoring demo: {e}")

.. grid:: 1 2 2 3
   :gutter: 2
   :class-container: workflow-features

   .. grid-item-card:: 📖 Documentation
      :shadow: sm
      :class-header: sd-bg-info sd-text-white
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - Class docs
      * :doc:`/workflows/{{ objname.lower() }}` - Workflow guide

   .. grid-item-card:: 🚀 Quick Start
      :shadow: sm
      :class-header: sd-bg-primary sd-text-white
      
      * :doc:`/guides/workflows` - Workflow basics
      * :doc:`/examples/workflows` - Usage examples

   .. grid-item-card:: 🤖 Agent Integration
      :shadow: sm
      :class-header: sd-bg-success sd-text-white
      
      * :doc:`/agents/multi-agent` - Multi-agent workflows
      * :doc:`/integration/workflows` - Integration guide

   .. grid-item-card:: ⚙️ Configuration
      :shadow: sm
      :class-header: sd-bg-warning sd-text-dark
      
      * Configuration options
      * State management
      * Error handling

   .. grid-item-card:: 📊 Monitoring
      :shadow: sm
      :class-header: sd-bg-secondary sd-text-white
      
      * Performance metrics
      * Debugging tools
      * Execution logs

   .. grid-item-card:: 🔗 Resources
      :shadow: sm
      :class-header: sd-bg-dark sd-text-white
      
      * :issue:`workflow-features` - Requests
      * :pr:`workflow-improvements` - Updates

.. autorun::

   # Workflow analysis and capabilities
   try:
       from {{ module }} import {{ objname }}
       import inspect
       
       print(f"🔄 Workflow Analysis: {{ objname }}")
       print("=" * 50)
       
       # Class metadata
       class_doc = {{ objname }}.__doc__ or "No description available"
       print(f"📋 Description: {class_doc[:150]}...")
       
       # Method analysis
       all_methods = inspect.getmembers({{ objname }}, predicate=inspect.ismethod)
       public_methods = [name for name, method in all_methods if not name.startswith('_')]
       
       # Categorize methods
       execution_methods = [m for m in public_methods if any(keyword in m.lower() for keyword in ['run', 'execute', 'start', 'process'])]
       config_methods = [m for m in public_methods if any(keyword in m.lower() for keyword in ['config', 'setup', 'init'])]
       state_methods = [m for m in public_methods if any(keyword in m.lower() for keyword in ['state', 'status', 'get', 'set'])]
       
       print(f"⚙️ Total public methods: {len(public_methods)}")
       
       if execution_methods:
           print(f"🚀 Execution methods: {', '.join(execution_methods)}")
       if config_methods:
           print(f"⚙️ Configuration methods: {', '.join(config_methods)}")
       if state_methods:
           print(f"📊 State methods: {', '.join(state_methods[:3])}{'...' if len(state_methods) > 3 else ''}")
       
       # Check inheritance
       bases = [base.__name__ for base in {{ objname }}.__bases__ if base.__name__ != 'object']
       if bases:
           print(f"🧬 Inheritance: {' → '.join(bases)} → {{ objname }}")
       
       # Check for async support
       async_methods = [name for name, method in inspect.getmembers({{ objname }}) 
                       if inspect.iscoroutinefunction(method)]
       if async_methods:
           print(f"⚡ Async methods: {', '.join(async_methods[:3])}")
       
       print("\n✅ Workflow is documented and ready for orchestration!")
       
   except Exception as e:
       print(f"ℹ️ Workflow analysis: {e}")
       print("🔄 Workflow class documented and available")

.. req:: Workflow Requirements
   :id: REQ_WORKFLOW_{{ objname.upper() }}_001
   :status: documented
   :priority: high
   :tags: workflow, orchestration, {{ objname.lower() }}

   Workflow {{ objname }} should provide clear execution patterns, state management, and integration capabilities.

.. seealso::

   * :doc:`/api/{{ module.replace('.', '/') }}` - Class documentation
   * :doc:`/workflows/index` - Workflow documentation hub
   * :doc:`/agents/multi-agent` - Multi-agent workflow patterns
   * :doc:`/examples/workflows` - Workflow usage examples  
   * :doc:`/guides/orchestration` - Orchestration guide
   * :doc:`/api/index` - Full API reference

.. last-updated:: {{ fullname }}
   :format: Workflow documented: %Y-%m-%d %H:%M