# Practical Template Examples - Sphinx Extensions

## 🎯 **Complete Working Templates**

### 1. **Professional Landing Page (index.rst)**

```rst
🤖 Haive AI Agent Framework Documentation
=========================================

.. container:: hero-banner

   .. container:: hero-content

      .. image:: /_static/images/haive-logo-light.svg
         :class: hero-logo
         :alt: Haive Logo
         :width: 200px
         :align: center

      **Build Intelligent AI Agents with Professional Tools**

      Professional framework for creating sophisticated AI agents with conversational intelligence,
      tool orchestration, game strategies, and multi-agent coordination.

      .. button-ref:: quickstart
         :ref-type: doc
         :color: primary
         :class: sd-rounded-pill

         🚀 Get Started

      .. button-link:: https://github.com/will-astley/haive
         :color: secondary
         :class: sd-rounded-pill

         📚 View on GitHub

.. card:: 🎯 Quick Start
   :class-card: sd-rounded-3

   Jump right in with our 5-minute quick start guide.

   +++

   .. button-ref:: quickstart
      :ref-type: doc
      :color: primary
      :expand:

.. grid:: 2 2 3 3
   :gutter: 3
   :class-container: feature-grid

   .. grid-item-card:: 🧠 AI Agents
      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg

      Build intelligent agents with memory, reasoning, and tool integration capabilities.

      .. list-table::
         :class: feature-list
         :widths: 20 80

         * - **Types**
           - Simple • React • RAG • Multi-Agent
         * - **Features**
           - Auto-persistence • Tool routing • State management

   .. grid-item-card:: 🎮 Game Intelligence
      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg

      Create AI opponents for strategic games with advanced algorithms and decision making.

      .. list-table::
         :class: feature-list
         :widths: 20 80

         * - **Games**
           - Chess • Go • Poker • Board Games
         * - **Features**
           - Strategy AI • Game state • Player modeling

   .. grid-item-card:: 🔧 Tool Orchestration
      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg

      Connect agents to APIs, databases, search engines, and external services seamlessly.

      .. list-table::
         :class: feature-list
         :widths: 20 80

         * - **Types**
           - Web APIs • Databases • File Systems
         * - **Features**
           - Auto-discovery • Type safety • Error handling

.. dropdown:: 💡 Why Choose Haive?
   :color: info
   :icon: light-bulb

   .. grid:: 1 2 4 4
      :gutter: 2

      .. grid-item::
         :class: benefit-item

         .. container:: benefit-icon

            ⚡

         **Production Ready**

         Battle-tested in production environments with comprehensive error handling.

      .. grid-item::
         :class: benefit-item

         .. container:: benefit-icon

            🔒

         **Type Safe**

         Full type hints and Pydantic models for reliable development.

      .. grid-item::
         :class: benefit-item

         .. container:: benefit-icon

            🚀

         **High Performance**

         Async-first architecture with optimized execution and caching.

      .. grid-item::
         :class: benefit-item

         .. container:: benefit-icon

            🎯

         **Extensible**

         Plugin architecture allows custom agents, tools, and integrations.

.. dropdown:: 📊 Live Performance Metrics
   :color: info
   :icon: graph

   .. exec_code::
      :caption: Real-time system metrics
      :linenos:

      import time
      import platform
      import sys
      from datetime import datetime
      
      print(f"🕰️ Timestamp: {datetime.now().strftime('%H:%M:%S')}")
      print(f"🚀 Python: {sys.version.split()[0]}")
      print(f"💻 Platform: {platform.system()}")
      print(f"⚡ CPU Count: {platform.machine()}")
      
      # Simulate performance metrics
      response_time = "<100ms"
      agents_per_hour = "10K+" 
      uptime = "99.9%"
      extensions = "86+"
      
      print(f"\n📊 Performance Metrics:")
      print(f"  ⏱️  Response Time: {response_time}")
      print(f"  🤖 Agents/Hour: {agents_per_hour}")
      print(f"  🟢 Uptime: {uptime}")
      print(f"  🔌 Extensions: {extensions}")
```

### 2. **Agent Documentation with All Features**

```rst
SimpleAgent
===========

.. currentmodule:: haive.agents.simple

.. autopydantic_model:: SimpleAgent
   :model-show-json: False
   :model-show-config-summary: True
   :model-show-field-summary: True
   :model-show-validator-members: True
   :field-list-validators: True
   :field-show-constraints: True
   :members:
   :inherited-members:
   :member-order: bysource

.. rubric:: Overview

SimpleAgent provides basic conversational AI capabilities with state management and tool integration.

.. dropdown:: 🧪 Live Example
   :color: primary
   :icon: code-square
   :animate: fade-in-slide-down
   :open:

   .. exec_code::
      :caption: Test SimpleAgent functionality
      :linenos:

      from haive.agents.simple import SimpleAgent
      from haive.core.engine import AugLLMConfig

      # Verify imports work
      print("✅ Imports successful")

      # Create configuration
      config = AugLLMConfig(
          temperature=0.7,
          system_message="You are a helpful assistant"
      )
      print(f"✅ Config created: {type(config).__name__}")

      # Create agent instance
      agent = SimpleAgent(
          name="demo_agent",
          engine=config
      )
      print(f"✅ Agent created: {agent.name}")

      # Show agent structure
      print(f"\n📊 Agent attributes:")
      for attr in ['name', 'engine', 'state']:
          if hasattr(agent, attr):
              print(f"  • {attr}: ✓")

.. admonition:: 💡 Pro Tips
   :class: tip

   * Use :tippy:`type hints <Type hints provide better IDE support and catch errors early>` for all parameters
   * Configure :paramlink:`temperature <Temperature controls randomness: 0.0=deterministic, 1.0=creative>` based on use case
   * Enable :emoji:`rocket` async execution for better performance
   * Check :issue:`123` for common issues and solutions

.. mermaid::
   :align: center
   :caption: SimpleAgent Architecture

   classDiagram
       class SimpleAgent {
           +name: str
           +engine: AugLLMConfig
           +state: AgentState
           +tools: List[Tool]
           +run(input: str) str
           +arun(input: str) str
           +stream(input: str) Iterator
           +astream(input: str) AsyncIterator
       }
       
       class Agent {
           <<abstract>>
           +name: str
           +run(input: str)
           +arun(input: str)
       }
       
       class AugLLMConfig {
           +model: str
           +temperature: float
           +max_tokens: int
           +system_message: str
       }
       
       Agent <|-- SimpleAgent
       SimpleAgent --> AugLLMConfig

.. tab-set::

   .. tab-item:: Configuration
      :sync: config

      .. code-block:: python
         :caption: Basic configuration
         :linenos:
         :emphasize-lines: 5-8

         from haive.agents.simple import SimpleAgent
         from haive.core.engine import AugLLMConfig

         # Configure the agent
         config = AugLLMConfig(
             model="gpt-4",
             temperature=0.7,
             system_message="You are a helpful AI assistant"
         )

         agent = SimpleAgent(
             name="my_assistant",
             engine=config
         )

   .. tab-item:: Async Usage
      :sync: async

      .. code-block:: python
         :caption: Async execution
         :linenos:
         :emphasize-lines: 8-10

         import asyncio
         from haive.agents.simple import SimpleAgent
         from haive.core.engine import AugLLMConfig

         async def main():
             agent = SimpleAgent(name="async_agent", engine=AugLLMConfig())
             
             # Async execution
             response = await agent.arun("Hello, how are you?")
             print(response)
             
             # Async streaming
             async for chunk in agent.astream("Tell me a story"):
                 print(chunk, end="")

         asyncio.run(main())

   .. tab-item:: With Tools
      :sync: tools

      .. code-block:: python
         :caption: Tool integration
         :linenos:
         :emphasize-lines: 11-14

         from haive.agents.simple import SimpleAgent
         from haive.tools import WebSearchTool, CalculatorTool

         # Create tools
         search = WebSearchTool()
         calculator = CalculatorTool()

         # Configure agent with tools
         agent = SimpleAgent(
             name="tool_agent",
             engine=AugLLMConfig(),
             tools=[search, calculator]
         )

         # Agent can now use tools
         result = agent.run("Search for Python tutorials and calculate 15 * 23")

.. req:: Agent Requirements
   :id: REQ_SIMPLE_AGENT_001
   :status: implemented
   :priority: high
   :tags: agent, core

   SimpleAgent must support both synchronous and asynchronous execution modes.

.. test:: Async Execution Test
   :id: TEST_SIMPLE_AGENT_001
   :status: passed
   :links: REQ_SIMPLE_AGENT_001

   Verify that SimpleAgent correctly handles async/await patterns.

.. rubric:: Configuration Options

.. jsonschema::

   {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "title": "SimpleAgent Configuration",
     "type": "object",
     "properties": {
       "name": {
         "type": "string",
         "description": "Unique identifier for the agent",
         "minLength": 1,
         "maxLength": 50
       },
       "engine": {
         "type": "object",
         "description": "LLM configuration",
         "properties": {
           "model": {
             "type": "string",
             "enum": ["gpt-4", "gpt-3.5-turbo", "claude-3"]
           },
           "temperature": {
             "type": "number",
             "minimum": 0.0,
             "maximum": 2.0
           }
         }
       },
       "tools": {
         "type": "array",
         "description": "Available tools",
         "items": {
           "type": "object"
         }
       }
     },
     "required": ["name", "engine"]
   }

.. last-updated:: haive.agents.simple.SimpleAgent
   :format: Last updated: %Y-%m-%d %H:%M
```

### 3. **Interactive Tool Documentation**

```rst
WebSearchTool
=============

.. currentmodule:: haive.tools.web

.. autoclass:: WebSearchTool
   :members:
   :show-inheritance:
   :special-members: __init__

.. card:: Quick Info
   :class-card: sd-rounded-2

   .. grid:: 2
      :gutter: 2

      .. grid-item::
         :columns: 6

         **Category**: Web Integration
         **Async**: Yes ✅
         **Rate Limited**: Yes (100/min)

      .. grid-item::
         :columns: 6

         **Requires**: API Key
         **Cost**: $0.001/search
         **Timeout**: 30s

.. dropdown:: 🚀 Quick Start
   :color: primary
   :open:

   .. tab-set::

      .. tab-item:: Basic Usage

         .. code-block:: python
            :linenos:
            :emphasize-lines: 5-7

            from haive.tools.web import WebSearchTool

            # Create tool
            tool = WebSearchTool(api_key="your-key")
            
            # Search
            results = tool.invoke({"query": "Python tutorials 2025"})
            print(f"Found {len(results)} results")

      .. tab-item:: With Agent

         .. code-block:: python
            :linenos:

            from haive.agents.react import ReactAgent
            from haive.tools.web import WebSearchTool

            agent = ReactAgent(
                name="research_agent",
                tools=[WebSearchTool(api_key="your-key")]
            )

            response = agent.run("Find recent AI developments")

      .. tab-item:: Advanced Config

         .. code-block:: python
            :linenos:

            tool = WebSearchTool(
                api_key="your-key",
                max_results=20,
                region="us",
                safe_search=True,
                timeout=60,
                retry_count=3
            )

.. mermaid::
   :align: center
   :caption: WebSearchTool Flow

   sequenceDiagram
       participant Agent
       participant WebSearchTool
       participant SearchAPI
       participant Cache

       Agent->>WebSearchTool: invoke(query)
       WebSearchTool->>Cache: check_cache(query)
       alt Cache Hit
           Cache-->>WebSearchTool: cached_results
       else Cache Miss
           WebSearchTool->>SearchAPI: search(query)
           SearchAPI-->>WebSearchTool: raw_results
           WebSearchTool->>WebSearchTool: parse_results()
           WebSearchTool->>Cache: store(query, results)
       end
       WebSearchTool-->>Agent: SearchResults

.. exec_code::
   :caption: Tool capabilities demonstration
   :hide_output:

   # This would demonstrate tool capabilities if API was available
   capabilities = {
       "search_types": ["web", "news", "images", "videos"],
       "languages": ["en", "es", "fr", "de", "ja", "zh"],
       "regions": ["us", "uk", "eu", "asia"],
       "filters": ["date", "domain", "filetype"]
   }

   print("🔍 WebSearchTool Capabilities:")
   for category, options in capabilities.items():
       print(f"\n{category.replace('_', ' ').title()}:")
       for opt in options:
           print(f"  • {opt}")
```

### 4. **Step-by-Step Tutorial with All Features**

```rst
Building Your First AI Agent
============================

.. rubric:: What You'll Learn

.. checklist::

   * ✅ Core concepts of AI agents
   * ✅ How to configure and create agents
   * ✅ Tool integration patterns
   * ✅ Best practices for production
   * ✅ Common pitfalls and solutions

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: ⏱️ Time to Complete
      :text-align: center

      **~30 minutes**

   .. grid-item-card:: 📊 Difficulty
      :text-align: center

      **Beginner**

.. dropdown:: 📋 Prerequisites
   :color: warning
   :icon: alert

   Before starting, ensure you have:

   .. code-block:: bash
      :caption: Check your setup

      # Python 3.8+
      python --version

      # Haive installed
      pip show haive

      # API keys configured
      echo $OPENAI_API_KEY

.. dropdown:: 🎯 Learning Objectives
   :color: info

   By the end of this tutorial, you will:

   1. Understand agent architecture
   2. Create and configure agents
   3. Add tool capabilities
   4. Handle errors gracefully
   5. Deploy to production

Step 1: Understanding Agents
----------------------------

.. tab-set::

   .. tab-item:: Concept
      :sync: concept1

      .. admonition:: What is an AI Agent?
         :class: note

         An AI agent is an autonomous system that can:
         
         * 🤔 Reason about tasks
         * 🛠️ Use tools to accomplish goals
         * 💾 Maintain conversation context
         * 🔄 Learn from interactions

      .. mermaid::
         :caption: Agent Components

         graph LR
             Input[User Input] --> Agent{AI Agent}
             Agent --> LLM[Language Model]
             Agent --> Tools[External Tools]
             Agent --> Memory[Context Memory]
             Agent --> Output[Response]

   .. tab-item:: Code Structure
      :sync: code1

      .. code-block:: python
         :caption: Basic agent structure
         :linenos:

         from haive.agents.base import Agent
         from haive.core.engine import AugLLMConfig

         class MyAgent(Agent):
             """Custom agent implementation."""
             
             def __init__(self, name: str, config: AugLLMConfig):
                 super().__init__(name=name, engine=config)
                 
             async def process(self, input_text: str) -> str:
                 """Process user input and return response."""
                 # Agent logic here
                 return await self.engine.complete(input_text)

   .. tab-item:: Architecture
      :sync: arch1

      .. inheritance-diagram:: haive.agents.simple.SimpleAgent
         :parts: 2
         :caption: Agent Class Hierarchy

Step 2: Create Your First Agent
-------------------------------

.. exec_code::
   :caption: Live agent creation demo
   :linenos:

   from haive.agents.simple import SimpleAgent
   from haive.core.engine import AugLLMConfig

   print("🚀 Creating your first AI agent...\n")

   # Step 1: Configure the language model
   config = AugLLMConfig(
       model="gpt-3.5-turbo",  # Or "gpt-4", "claude-3"
       temperature=0.7,        # 0.0 = focused, 1.0 = creative
       max_tokens=1000,        # Maximum response length
       system_message="You are a helpful AI assistant named Alex."
   )
   print("✅ Configuration created")

   # Step 2: Create the agent
   agent = SimpleAgent(
       name="alex",
       engine=config
   )
   print(f"✅ Agent '{agent.name}' created")

   # Step 3: Verify agent is ready
   print(f"\n📊 Agent Status:")
   print(f"  • Name: {agent.name}")
   print(f"  • Type: {type(agent).__name__}")
   print(f"  • Ready: ✅")

.. dropdown:: 💡 Configuration Tips
   :color: success

   .. list-table:: Temperature Settings Guide
      :header-rows: 1
      :widths: 20 40 40

      * - Temperature
        - Use Case
        - Example Output
      * - 0.0 - 0.3
        - Factual, deterministic tasks
        - Code generation, data extraction
      * - 0.4 - 0.7
        - Balanced responses
        - General assistance, Q&A
      * - 0.8 - 1.0
        - Creative tasks
        - Story writing, brainstorming

Step 3: Add Tool Capabilities
-----------------------------

.. code-block:: python
   :caption: Enhanced agent with tools
   :linenos:
   :emphasize-lines: 15-23

   from haive.agents.react import ReactAgent
   from haive.tools import WebSearchTool, CalculatorTool, WeatherTool
   from haive.core.engine import AugLLMConfig

   # Configure agent
   config = AugLLMConfig(
       model="gpt-4",
       temperature=0.5,
       system_message="You are a research assistant with access to tools."
   )

   # Create tools
   tools = [
       WebSearchTool(api_key=os.getenv("SEARCH_API_KEY")),
       CalculatorTool(),
       WeatherTool(api_key=os.getenv("WEATHER_API_KEY"))
   ]

   # Create agent with tools
   agent = ReactAgent(
       name="researcher",
       engine=config,
       tools=tools
   )

   # Agent can now search, calculate, and check weather!
   response = await agent.arun(
       "What's the weather in Tokyo and calculate the Celsius to Fahrenheit conversion"
   )

.. mermaid::
   :caption: Agent with Tools Flow

   sequenceDiagram
       participant User
       participant Agent
       participant LLM
       participant Tools

       User->>Agent: "Weather in Tokyo?"
       Agent->>LLM: Analyze request
       LLM-->>Agent: Need weather tool
       Agent->>Tools: get_weather("Tokyo")
       Tools-->>Agent: 22°C, Sunny
       Agent->>LLM: Format response
       LLM-->>Agent: Formatted answer
       Agent-->>User: "Tokyo: 22°C (72°F), Sunny"

.. req:: Tool Integration
   :id: REQ_TUTORIAL_001
   :status: demonstrated
   :tags: tutorial, tools

   Agents must seamlessly integrate multiple tools for complex tasks.

Best Practices
--------------

.. card-carousel:: 2

   .. card:: ✅ Do This
      :class-card: sd-bg-success sd-text-white

      * Use descriptive agent names
      * Configure appropriate temperature
      * Add error handling
      * Log important events
      * Test with real scenarios
      * Monitor token usage

   .. card:: ❌ Avoid This
      :class-card: sd-bg-danger sd-text-white

      * Hardcoding API keys
      * Ignoring rate limits
      * Skipping error handling
      * Using temperature = 2.0
      * Blocking on async calls
      * Infinite tool loops

Common Issues & Solutions
-------------------------

.. accordion::

   .. accordion-item:: Issue: Agent returns generic responses
      :class-title: sd-bg-warning

      **Problem**: Agent gives vague, unhelpful responses
      
      **Solution**:
      
      .. code-block:: python
         :emphasize-lines: 4-7

         # ❌ Too vague
         config = AugLLMConfig(system_message="You are helpful")

         # ✅ Specific and detailed
         config = AugLLMConfig(
             system_message="""You are an expert Python developer assistant.
             Provide detailed, accurate code examples with explanations.
             Always consider best practices and potential edge cases."""
         )

   .. accordion-item:: Issue: Tool calls fail
      :class-title: sd-bg-warning

      **Problem**: Agent can't use tools properly
      
      **Solution**:

      .. code-block:: python
         :emphasize-lines: 8-13

         # Ensure tools are properly configured
         tool = WebSearchTool(
             api_key=os.getenv("SEARCH_KEY"),
             timeout=30,
             retry_count=3
         )

         # Add error handling
         try:
             result = await agent.arun("Search for Python tutorials")
         except ToolError as e:
             logger.error(f"Tool failed: {e}")
             result = "Search unavailable, please try again"

Next Steps
----------

.. card:: 🎉 Congratulations!
   :class-card: sd-rounded-3

   You've successfully created your first AI agent! Here's what to explore next:

   .. grid:: 2
      :gutter: 2

      .. grid-item::
         
         .. button-ref:: /guides/advanced-agents
            :color: primary
            :expand:

            Advanced Agent Patterns

      .. grid-item::

         .. button-ref:: /guides/production-deployment  
            :color: primary
            :expand:

            Deploy to Production

   .. admonition:: 📚 Additional Resources
      :class: seealso

      * :doc:`/api/agents/index` - Complete API reference
      * :doc:`/examples/index` - More code examples
      * :issue:`new` - Request features
      * :pr:`help-wanted` - Contribute to Haive
```

### 5. **MCP Server Documentation Template**

```rst
PostgreSQL MCP Server
=====================

.. card:: Server Information
   :class-card: sd-rounded-3 sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: server-info-table

      * - **Category**
        - Database Integration
      * - **Author**
        - Model Context Protocol Team
      * - **License**
        - MIT
      * - **Version**
        - |version|
      * - **Status**
        - .. badge:: Production Ready
             :class: badge-success

.. dropdown:: 🚀 Installation & Setup
   :color: primary
   :icon: rocket
   :animate: fade-in-slide-down
   :open:

   .. tab-set::

      .. tab-item:: Quick Install
         :sync: install

         .. code-block:: bash
            :caption: Install via Claude MCP
            :linenos:

            # Add to Claude
            claude mcp add postgres-server -s user -- \
              npx -y @modelcontextprotocol/server-postgres \
              "postgresql://localhost/mydb"

            # With authentication
            claude mcp add postgres-server -s user -- \
              npx -y @modelcontextprotocol/server-postgres \
              "postgresql://user:pass@localhost:5432/mydb"

      .. tab-item:: Manual Config
         :sync: manual

         .. code-block:: json
            :caption: claude_desktop_config.json
            :linenos:
            :emphasize-lines: 5-11

            {
              "mcpServers": {
                "postgres": {
                  "command": "npx",
                  "args": [
                    "-y",
                    "@modelcontextprotocol/server-postgres",
                    "postgresql://localhost/mydb"
                  ],
                  "env": {
                    "POSTGRES_SSL": "true"
                  }
                }
              }
            }

      .. tab-item:: Docker Setup
         :sync: docker

         .. code-block:: yaml
            :caption: docker-compose.yml
            :linenos:

            version: '3.8'
            services:
              postgres:
                image: postgres:15
                environment:
                  POSTGRES_PASSWORD: secret
                  POSTGRES_DB: haive
                ports:
                  - "5432:5432"
                volumes:
                  - postgres_data:/var/lib/postgresql/data

            volumes:
              postgres_data:

.. rubric:: Available Tools

.. exec_code::
   :caption: List available database tools
   :hide_code:

   tools = {
       "query": "Execute SQL queries",
       "list_tables": "List all tables in database",
       "describe_table": "Get table schema",
       "insert": "Insert data into tables", 
       "update": "Update existing records",
       "delete": "Delete records",
       "create_table": "Create new tables",
       "drop_table": "Remove tables"
   }

   print("🛠️ PostgreSQL MCP Tools:\n")
   for tool, description in tools.items():
       print(f"📌 {tool:<15} - {description}")

.. mermaid::
   :caption: PostgreSQL MCP Architecture
   :align: center

   graph TB
       subgraph Claude
           A[Claude Code]
       end
       
       subgraph "MCP Server"
           B[PostgreSQL MCP]
           C[Connection Pool]
           D[Query Parser]
       end
       
       subgraph Database
           E[(PostgreSQL)]
           F[Tables]
           G[Indexes]
       end
       
       A <-->|MCP Protocol| B
       B --> C
       C --> D
       D <--> E
       E --> F
       E --> G
       
       style A fill:#e1f5fe
       style B fill:#4fc3f7
       style E fill:#81c784

.. dropdown:: 📊 Usage Examples
   :color: info
   :icon: code

   .. tab-set::

      .. tab-item:: Basic Queries

         .. code-block:: sql
            :caption: Simple SELECT query

            -- In Claude, use @postgres
            SELECT * FROM users 
            WHERE created_at > '2025-01-01'
            ORDER BY created_at DESC
            LIMIT 10;

      .. tab-item:: Data Analysis

         .. code-block:: sql
            :caption: Aggregation example

            -- User activity analysis
            SELECT 
                DATE_TRUNC('day', created_at) as day,
                COUNT(*) as new_users,
                COUNT(DISTINCT country) as countries
            FROM users
            GROUP BY day
            ORDER BY day DESC;

      .. tab-item:: Schema Management

         .. code-block:: sql
            :caption: Create tables with MCP

            -- Create agents table
            CREATE TABLE agents (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                config JSONB,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );

            -- Add indexes
            CREATE INDEX idx_agents_name ON agents(name);
            CREATE INDEX idx_agents_config ON agents USING GIN(config);

.. req:: Database Security
   :id: REQ_POSTGRES_MCP_001
   :status: implemented
   :priority: critical
   :tags: security, database

   PostgreSQL MCP must use secure connections and respect database permissions.

.. admonition:: ⚠️ Security Best Practices
   :class: warning

   * Always use SSL connections in production
   * Create read-only users for queries
   * Never expose credentials in logs
   * Use connection pooling
   * Set query timeouts

.. last-updated::
   :format: Documentation updated: %Y-%m-%d
```

## 🎨 **CSS Enhancements for Templates**

Create `_static/custom.css`:

```css
/* Haive Documentation Custom Styles */

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    border-radius: 12px;
    margin-bottom: 3rem;
    text-align: center;
    color: white;
}

.hero-content h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.hero-logo {
    filter: brightness(0) invert(1);
    margin-bottom: 2rem;
}

/* Feature Cards */
.feature-card-header {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white !important;
    font-weight: 600;
}

.feature-card-body {
    padding: 1.5rem;
}

.feature-list {
    margin: 0;
    border: none;
}

/* Code Execution Output */
.exec-code-output {
    background: #f8f9fa;
    border-left: 4px solid #28a745;
    padding: 1rem;
    margin-top: 1rem;
    font-family: 'Fira Code', monospace;
}

/* Interactive Elements */
.tippy-box {
    background: #333;
    color: white;
    border-radius: 6px;
    padding: 0.5rem 1rem;
}

/* Mermaid Diagrams */
.mermaid {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin: 2rem 0;
    text-align: center;
}

/* Requirements Tracking */
.req {
    background: #e3f2fd;
    border-left: 4px solid #2196f3;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
}

.req-id {
    font-weight: bold;
    color: #1976d2;
}

/* Checklist Styling */
.checklist {
    list-style: none;
    padding-left: 0;
}

.checklist li::before {
    content: "☐ ";
    color: #666;
    font-weight: bold;
    margin-right: 0.5rem;
}

.checklist li.done::before {
    content: "✅ ";
    color: #28a745;
}

/* Tab Improvements */
.sphinx-tabs {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 2rem 0;
}

.sphinx-tabs-nav {
    background: #f8f9fa;
    border-bottom: 2px solid #dee2e6;
}

.sphinx-tabs-tab[aria-selected="true"] {
    background: white;
    border-bottom: 2px solid #007bff;
    color: #007bff;
    font-weight: 600;
}

/* JSON Schema Styling */
.jsonschema-container {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.jsonschema-property {
    margin: 1rem 0;
    padding: 0.5rem;
    background: white;
    border-radius: 4px;
}

/* Dropdown Enhancements */
.sd-dropdown summary {
    cursor: pointer;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.sd-dropdown summary:hover {
    background: #e9ecef;
    transform: translateY(-1px);
}

.sd-dropdown[open] summary {
    background: #007bff;
    color: white;
}

/* Grid Improvements */
.sd-card {
    transition: all 0.3s ease;
    height: 100%;
}

.sd-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

/* Copy Button Styling */
.copybutton {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    opacity: 0;
    transition: opacity 0.3s ease;
    background: #007bff;
    color: white;
    border: none;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
}

.highlight:hover .copybutton {
    opacity: 1;
}

/* Server Info Table */
.server-info-table {
    width: 100%;
    margin: 1rem 0;
}

.server-info-table td:first-child {
    font-weight: 600;
    color: #495057;
}

/* Badge Styling */
.badge-success {
    background: #28a745;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
}

/* Animated Elements */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeInUp 0.5s ease-out;
}
```

## 📝 **Summary**

This comprehensive guide now includes:

1. **Complete working templates** for all major documentation types
2. **Practical examples** showing real extension usage
3. **CSS styling** for professional appearance
4. **Best practices** for each extension category
5. **Integration patterns** for combining multiple extensions

The templates demonstrate:
- Live code execution with `sphinx_exec_code`
- Interactive schemas with `sphinx_jsonschema`
- Modern UI with `sphinx_design`
- Diagrams with `sphinxcontrib.mermaid`
- Requirements tracking with `sphinx_needs`
- GitHub integration with `sphinx_issues`
- And much more!

Use these templates as starting points and customize them for your specific documentation needs.