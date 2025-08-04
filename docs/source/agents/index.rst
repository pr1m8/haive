.. title:: Haive Agent Ecosystem
.. _agents:

🤖 Haive Agent Showcase
========================

**Comprehensive collection of 80+ intelligent AI agents for every use case**

.. grid:: 1 2 4 4

   :gutter: 2
   :padding: 2

   .. grid-item::
      

      .. raw:: html

   .. raw:: html

   <div class="metric-card">
   <span class="value">80+</span>
   <span class="label">Agent Types</span>
   </div>

   .. grid-item::

   .. raw:: html

.. raw:: html

   <div class="metric-card">
   <span class="value">8</span>
   <span class="label">Categories</span>
   </div>

   .. grid-item::
      

      .. raw:: html

   .. raw:: html

   <div class="metric-card">
   <span class="value">20+</span>
   <span class="label">RAG Variants</span>
   </div>

   .. grid-item::

   .. raw:: html

.. raw:: html

   <div class="metric-card">
   <span class="value">100%</span>
   <span class="label">Type Safe</span>
   </div>

Agent Categories
----------------

🤖 All Agents
==============

.. grid:: 1 2 3 3

   :gutter: 3

   .. grid-item-card:: 💬 SimpleAgent

      :link: ../api/haive/agents/simple/index
      :shadow: lg
      
      **Basic Conversational Agent**
      
      General-purpose conversational agent for straightforward interactions and basic task completion. Perfect starting point for custom agents.
      
      +++
      
      ✓ Natural language processing  
      ✓ Context-aware responses  
      ✓ Memory integration  
      ✓ Customizable prompts  
      
      .. raw:: html

   .. raw:: html

   <div style="margin-top: 10px;">
   <a href="demos/simple-demo.html" class="btn btn-sm btn-primary">Try Demo</a>
   </div>

   .. grid-item-card:: 🧠 ReactAgent
   :link: ../api/haive/agents/react/index
   :shadow: lg

   **Reasoning & Acting Agent**

   Advanced reasoning agent that can use tools to solve complex problems through iterative thought and action cycles.

   +++

   ✓ Tool integration  
   ✓ Multi-step reasoning  
   ✓ Self-reflection capabilities  
   ✓ Error recovery  

   .. raw:: html

.. raw:: html

   <div style="margin-top: 10px;">
   <a href="demos/react-demo.html" class="btn btn-sm btn-primary">Try Demo</a>
   </div>

   .. grid-item-card:: 📚 RAGAgent

      :link: ../api/haive/agents/rag/index
      :shadow: lg
      
      **Retrieval-Augmented Generation**
      
      Knowledge-grounded agents that combine retrieval systems with generation for accurate, up-to-date responses.
      
      +++
      
      ✓ Vector search integration  
      ✓ Knowledge base queries  
      ✓ Source attribution  
      ✓ Adaptive retrieval  

   .. grid-item-card:: 🔬 ResearchAgent

      :link: ../api/src/haive/agents/research/index
      :shadow: lg
      
      **Advanced Research & Analysis**
      
      Specialized agents for comprehensive research, information gathering, and multi-source analysis.
      
      +++
      
      ✓ Multi-source research  
      ✓ Fact verification  
      ✓ Report generation  
      ✓ Citation management  

   .. grid-item-card:: 🎭 ConversationAgent

      :link: ../api/src/haive/agents/conversation/index
      :shadow: lg
      
      **Multi-Party Dialogue**
      
      Sophisticated dialogue management for multi-party conversations, debates, and collaborative discussions.
      
      +++
      
      ✓ Multi-participant management  
      ✓ Turn-taking protocols  
      ✓ Debate facilitation  
      ✓ Consensus building  

   .. grid-item-card:: 🎯 PlanningAgent

      :link: ../api/src/haive/agents/planning/index
      :shadow: lg
      
      **Task Planning & Execution**
      
      Advanced planning agents for task decomposition, workflow orchestration, and multi-step execution.
      
      +++
      
      ✓ Task decomposition  
      ✓ Workflow planning  
      ✓ Resource allocation  
      ✓ Progress tracking  

   .. grid-item-card:: 🌐 MultiAgent

      :link: ../api/src/haive/agents/multi/index
      :shadow: lg
      
      **Coordinated Agent Systems**
      
      Sophisticated multi-agent systems for complex problem-solving through coordinated collaboration.
      
      +++
      
      ✓ Agent coordination  
      ✓ Workflow orchestration  
      ✓ State synchronization  
      ✓ Distributed processing  

   .. grid-item-card:: 🔍 SearchAgent

      :link: ../api/src/haive/agents/research/perplexity/index
      :shadow: lg
      
      **Perplexity-Style Search**
      
      Advanced search agents including QuickSearch, ProSearch, DeepResearch, and Labs automation capabilities.
      
      +++
      
      ✓ Multi-tier search (Quick/Pro/Deep)  
      ✓ Source verification  
      ✓ Interactive dashboards  
      ✓ Automated workflows

Agent Catalog by Category
-------------------------

.. tab-set::

   .. tab-item:: 💬 Simple Agents
      

      **Basic agents for straightforward tasks and conversations.**
      
      - **SimpleAgent** - General purpose conversational agent
      - **SimpleAnalysisAgent** - Basic data analysis capabilities
      - **StructuredOutputAgent** - Agents with typed outputs
      - **AsyncAgent** - Asynchronous agent base class

   .. tab-item:: 🧠 ReAct Agents
      

      **Reasoning and action agents that use tools to solve problems.**
      
      - **ReactAgent** - Standard ReAct implementation
      - **ReactResearchAgent** - Research-focused ReAct
      - **ReactWithMemory** - ReAct with persistent memory
      - **DynamicReactAgent** - Dynamic tool selection

   .. tab-item:: 📚 RAG Agents
      

      **Retrieval-Augmented Generation agents for knowledge-grounded responses.**
      
      - **BaseRAGAgent** - Standard RAG implementation
      - **AdaptiveRAGAgent** - Dynamic retrieval strategies
      - **SelfRAGAgent** - Self-reflective RAG
      - **MultiStrategyRAG** - Multiple retrieval approaches
      - **HyDEAgent** - Hypothetical Document Embeddings

   .. tab-item:: 🌐 Multi-Agent
      

      **Coordinated systems of multiple agents working together.**
      
      - **SupervisorAgent** - Hierarchical coordination
      - **SequentialAgent** - Sequential execution
      - **ParallelAgent** - Parallel processing
      - **DynamicMultiAgent** - Dynamic agent activation

   .. tab-item:: 🎯 Specialized
      

      **Agents designed for specific use cases and domains.**
      
      - **ResearchAgent** - Academic research assistant
      - **DebateAgent** - Multi-perspective debates
      - **PlanAndExecuteAgent** - Strategic planning
      - **ReflectionAgent** - Self-improving agents
      - **TreeOfThoughtsAgent** - Complex reasoning

Quick Start
-----------

.. raw:: html

   .. raw:: html

   <div class="code-example-section">
   <h4>🚀 Get Started in 30 Seconds</h4>

.. code-block:: python

   from haive.agents.simple import SimpleAgent
   from haive.agents.react import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_core.tools import tool

   # 1. Simple conversational agent
   simple_agent = SimpleAgent(
   name="assistant",
   engine=AugLLMConfig(temperature=0.7)
   )
   response = await simple_agent.arun("What's the weather like?")

   # 2. ReAct agent with tools
   @tool
   def calculator(expression: str) -> str:
   """Evaluate mathematical expressions."""
   return str(eval(expression))

   @tool
   def web_search(query: str) -> str:
   """Search the web for information."""
   # Implementation here
   return f"Results for: {query}"

   react_agent = ReactAgent(
   name="researcher",
   engine=AugLLMConfig(),
   tools=[calculator, web_search]
   )
   result = await react_agent.arun(
   "Find the population of Tokyo and calculate its density"
   )

   .. raw:: html

   </div>

   Agent Patterns
   --------------

   .. raw:: html

   .. raw:: html

   <div class="api-grid">

   .. raw:: html

   <div class="api-section">
   <h4>🎯 Single Agent Patterns</h4>
   <ul>
   <li><strong>Conversational</strong> - Natural dialogue flows</li>
   <li><strong>Task-oriented</strong> - Specific goal completion</li>
   <li><strong>Analytical</strong> - Data analysis and insights</li>
   <li><strong>Creative</strong> - Content generation</li>
   </ul>
   </div>

   .. raw:: html

   <div class="api-section">
   <h4>🔄 Multi-Agent Patterns</h4>
   <ul>
   <li><strong>Pipeline</strong> - Sequential processing</li>
   <li><strong>Ensemble</strong> - Parallel consensus</li>
   <li><strong>Hierarchical</strong> - Supervisor coordination</li>
   <li><strong>Collaborative</strong> - Peer-to-peer</li>
   </ul>
   </div>

   .. raw:: html

   <div class="api-section">
   <h4>🧩 Composition Patterns</h4>
   <ul>
   <li><strong>Agent as Tool</strong> - Agents calling agents</li>
   <li><strong>Meta-Agent</strong> - Self-modifying agents</li>
   <li><strong>Dynamic Routing</strong> - Runtime selection</li>
   <li><strong>State Sharing</strong> - Cross-agent memory</li>
   </ul>
   </div>

   .. raw:: html

   </div>

   Building Custom Agents
   ----------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🛠️ Create Your Own Agent</h3>
   <p>Build custom agents by extending our base classes.</p>

.. code-block:: python

   from haive.agents.base import Agent
   from haive.core.schema.prebuilt.messages_state import MessagesState
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_core.messages import AIMessage
   from typing import Dict, Any

   class MyCustomAgent(Agent):
   """Custom agent with specialized behavior."""

   def __init__(
   self,
   name: str,
   engine: AugLLMConfig,
   custom_param: str = "default"
   ):
   super().__init__(name=name, engine=engine)
   self.custom_param = custom_param

   async def _arun(
   self,
   input_data: Dict[str, Any],
   config: Optional[Dict[str, Any]] = None,
   **kwargs**
   ) -> Dict[str, Any]:
   """Execute agent logic."""
   # Get messages from input
   messages = input_data.get("messages", [])

   # Add system message if needed
   if self.custom_param:
   messages = self._add_system_message(
   messages,
   f"Custom behavior: {self.custom_param}"
   )

   # Call LLM
   response = await self.engine.ainvoke(messages)

   # Process response
   return {
   "messages": messages + [response],
   "custom_output": self._process_response(response)
   }

   def _process_response(self, response: AIMessage) -> Any:
   """Custom response processing."""
   # Your logic here
   return response.content

   # Use your custom agent
   agent = MyCustomAgent(
   name="my_agent",
   engine=AugLLMConfig(),
   custom_param="specialized_behavior"
   )
   result = await agent.arun({"messages": [...]})

   .. raw:: html

   </div>

   Agent Configuration
   -------------------

   .. raw:: html

   .. raw:: html

   <div class="showcase-section">

   .. raw:: html

   <div class="showcase-header">
   <h2>⚙️ Configuration Options</h2>
   <p>Configure agents for different use cases and performance requirements</p>
   </div>

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig
   from haive.agents.simple import SimpleAgent

   # Basic configuration
   config = AugLLMConfig(

       model="gpt-4",                    # Model selection
       temperature=0.7,                  # Creativity level
       max_tokens=1000,                  # Response length
       system_message="You are helpful", # System prompt
       streaming=True,                   # Enable streaming
       retry_config={                    # Retry settings
           "max_attempts": 3,
           "backoff_factor": 2
       }

   )

   # Performance optimization
   fast_config = AugLLMConfig(

       model="gpt-3.5-turbo",
       temperature=0.1,                  # More deterministic
       max_tokens=500,                   # Shorter responses
       timeout=10.0,                     # Faster timeout
       cache_responses=True              # Enable caching

   )

   # High-quality configuration
   quality_config = AugLLMConfig(

       model="gpt-4-turbo",
       temperature=0.3,
       max_tokens=2000,
       top_p=0.95,                       # Nucleus sampling
       frequency_penalty=0.5,            # Reduce repetition
       presence_penalty=0.5              # Encourage diversity

   )

   .. raw:: html

   </div>

   Performance Benchmarks
   ----------------------

   .. raw:: html

   .. raw:: html

   <div class="performance-section">
   <h3>⚡ Agent Performance Metrics</h3>
   <table class="performance-table">
   <thead>
   <tr>
   <th>Agent Type</th>
   <th>Avg Response Time</th>
   <th>Token Usage</th>
   <th>Success Rate</th>
   <th>Cost/Request</th>
   </tr>
   </thead>
   <tbody>
   <tr>
   <td>SimpleAgent</td>
   <td>1.2s</td>
   <td>~500 tokens</td>
   <td>98%</td>
   <td>$0.02</td>
   </tr>
   <tr>
   <td>ReactAgent</td>
   <td>3.5s</td>
   <td>~1500 tokens</td>
   <td>95%</td>
   <td>$0.08</td>
   </tr>
   <tr>
   <td>RAGAgent</td>
   <td>2.8s</td>
   <td>~1000 tokens</td>
   <td>97%</td>
   <td>$0.05</td>
   </tr>
   <tr>
   <td>MultiAgent</td>
   <td>5-15s</td>
   <td>~3000 tokens</td>
   <td>93%</td>
   <td>$0.15</td>
   </tr>
   </tbody>
   </table>
   </div>

   Debugging & Testing
   -------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🐛 Debug and Test Your Agents</h3>

.. code-block:: python

   import logging
   from haive.agents.simple import SimpleAgent

   # Enable debug logging
   logging.basicConfig(level=logging.DEBUG)

   # Create agent with debug mode
   agent = SimpleAgent(
   name="debug_agent",
   engine=AugLLMConfig(),
   debug=True  # Enable debug output
   )

   # Test with different inputs
   test_cases = [
   "Simple greeting",
   "Complex reasoning task",
   "Error handling test"
   ]

   for test in test_cases:
   try:
   result = await agent.arun(test)
   print(f"✅ Test passed: {test}")
   print(f"   Response: {result[:100]}...")
   except Exception as e:
   print(f"❌ Test failed: {test}")
   print(f"   Error: {e}")

   # Performance testing
   import time

   start = time.time()
   for _ in range(10):
   await agent.arun("Quick test")

   avg_time = (time.time() - start) / 10
   print(f"Average response time: {avg_time:.2f}s")

   .. raw:: html

   </div>

   Related Components
   ------------------

   .. raw:: html

   .. raw:: html

   <div class="showcase-section">

   .. raw:: html

   <div class="showcase-header">
   <h2>🌐 Extend Your Agents</h2>
   <p>Enhance agent capabilities with tools, games, and external integrations</p>
   </div>

   .. raw:: html

   <div class="agent-showcase">

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">🔧</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Agent Tools</h3>
   <p class="agent-subtitle">Powerful capabilities</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Give your agents powerful tools for web search, code execution, data processing, and API integration.
   .. raw:: html

   </p>

   .. raw:: html

   <div class="agent-features">
   <span class="feature-tag">WebSearch</span>
   <span class="feature-tag">PythonREPL</span>
   <span class="feature-tag">Calculator</span>
   <span class="feature-tag">APIs</span>
   </div>

   .. raw:: html

   <a href="../tools/index.html" class="agent-link">Browse Tools</a>
   </div>

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">🎮</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Test in Games</h3>
   <p class="agent-subtitle">Strategic environments</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Test and train your agents in strategic game environments with intelligent opponents.
   .. raw:: html

   </p>

   .. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Chess</span>
   <span class="feature-tag">Poker</span>
   <span class="feature-tag">Strategy</span>
   <span class="feature-tag">Board Games</span>
   </div>

   .. raw:: html

   <a href="../games/index.html" class="agent-link">View Games</a>
   </div>

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">📡</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">MCP Connections</h3>
   <p class="agent-subtitle">External systems</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Connect agents to databases, filesystems, GitHub, and external APIs through Model Context Protocol.
   .. raw:: html

   </p>

   .. raw:: html

   <div class="agent-features">
   <span class="feature-tag">PostgreSQL</span>
   <span class="feature-tag">GitHub</span>
   <span class="feature-tag">Filesystem</span>
   <span class="feature-tag">Docker</span>
   </div>

   .. raw:: html

   <a href="../mcp/index.html" class="agent-link">Setup MCP</a>
   </div>

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">📖</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Complete API</h3>
   <p class="agent-subtitle">Full documentation</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Explore the complete API reference with detailed documentation for all agent classes and methods.
   .. raw:: html

   </p>

   .. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Core API</span>
   <span class="feature-tag">Examples</span>
   <span class="feature-tag">Guides</span>
   <span class="feature-tag">Reference</span>
   </div>

   .. raw:: html

   <a href="../api/index.html" class="agent-link">API Docs</a>
   </div>
   </div>
   </div>

   Interactive Demos
   -----------------

   .. raw:: html

   .. raw:: html

   <div class="showcase-section">

   .. raw:: html

   <div class="showcase-header">
   <h2>🎮 Try Agent Demos</h2>
   <p>Interactive demonstrations with live graph visualization</p>
   </div>

   .. raw:: html

   <div class="agent-showcase">
   <a href="demos/index.html" class="demo-button">
   <span class="demo-icon">🚀</span>
   <span class="demo-text">Launch Interactive Demos</span>
   </a>
   </div>

   .. raw:: html

   </div>

   API Reference
   -------------

   .. toctree::

   :maxdepth: 2
   :hidden:

   demos/index
   ../api/agents/index
   gallery
   showcase
   complete_index

   Quick Links
   ^^^^^^^^^^^

   - :doc:`Agent Gallery <gallery>` - Visual showcase of all agents
   - :doc:`API Reference <../api/agents/index>` - Complete API documentation
   - :doc:`Building Agents Guide <../guides/building_agents>` - Step-by-step guide
   - :doc:`Agent Patterns <../guides/agent_patterns>` - Common design patterns

   .. seealso::

   - :doc:`../tools/index` - Tools that agents can use
   - :doc:`../guides/multi_agent_systems` - Building multi-agent systems
   - :doc:`../examples/index` - Example implementations
