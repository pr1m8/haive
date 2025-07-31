# Jinja Template Guide for Haive Documentation

This guide explains how to convert static agent examples to dynamic Jinja2 templates for the Haive documentation system.

## 🎯 Overview

The Haive documentation uses Jinja2 templates to generate dynamic content from cached agent execution data. This allows us to show real agent responses and visualizations without expensive LLM calls during documentation builds.

## 📋 Template System Components

### 1. **Sphinx Configuration** (`conf.py`)

```python
extensions = [
    "sphinx_jinja2",  # 🎨 Jinja2 template processing
    # ... other extensions
]

jinja2_contexts = {
    "agent_demo": {
        "get_agent_context": get_agent_context,
        "available_agents": AVAILABLE_AGENTS,
        "get_agent_demo_context": get_agent_demo_context,
        "get_available_agent_types": get_available_agent_types,
    }
}
```

### 2. **Data Loader** (`agent_cache_loader.py`)

```python
class AgentCacheLoader:
    def get_agent_demo_context(self, agent_type: str) -> Dict[str, Any]:
        """Load cached agent execution data for templates."""
        cache_data = self.load_agent_cache(agent_type)
        return {
            "agent_type": agent_type,
            "response": self.extract_clean_response(cache_data),
            "execution_data": cache_data,
            "visualization_data": self.prepare_visualization_data(cache_data),
            "tool_calls": self.extract_tool_calls(cache_data),
            "graph_data": self.prepare_graph_data(cache_data)
        }
```

### 3. **Cached Data** (`agent_cache_*.json`)

```json
{
  "agent_type": "simple",
  "agent_name": "SimpleAgent",
  "generated_at": "2025-07-18T12:00:00",
  "executions": [
    {
      "execution_id": "simple_agent_demo_1",
      "input_text": "Hello! Can you introduce yourself?",
      "agent_output": "Hello! I'm a SimpleAgent...",
      "execution_summary": {
        "duration_seconds": 2.34,
        "total_events": 2
      },
      "visualization_data": {
        /* ... */
      }
    }
  ]
}
```

## 🔄 Converting Examples to Templates

### Step 1: Identify Static Content

**Before (Static RST)**:

```rst
SimpleAgent Demo
================

Here's how to use SimpleAgent:

.. code-block:: python

    agent = SimpleAgent(name="demo", engine=config)
    response = agent.run("Hello!")
    print(response)  # Some hardcoded response

Output::

    Hello! I'm a helpful assistant. I can help you with various tasks...
```

### Step 2: Convert to Jinja Template

**After (Dynamic Jinja Template)**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "simple"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   SimpleAgent Demo
   ================

   Here's how to use SimpleAgent:

   .. code-block:: python

       agent = SimpleAgent(name="demo", engine=config)
       response = agent.run("{{ agent_data.input_text }}")
       print(response)

   **Real Output** (from cached execution):

   .. code-block:: text

       {{ agent_data.response }}

   **Execution Details**:
   - Duration: {{ "%.2f"|format(agent_data.execution_data.executions[0].execution_summary.duration_seconds) }}s
   - Events: {{ agent_data.execution_data.executions[0].execution_summary.total_events }}
```

## 🎨 Template Patterns by Agent Type

### SimpleAgent Template

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "simple"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set execution = agent_data.execution_data.executions[0] %}

   SimpleAgent Example
   ===================

   Basic conversation with SimpleAgent:

   .. code-block:: python

       from haive.agents.simple import SimpleAgent
       from haive.core.engine.aug_llm import AugLLMConfig

       config = AugLLMConfig(temperature=0.7)
       agent = SimpleAgent(name="demo", engine=config)

       response = agent.run("{{ execution.input_text }}")

   **Response**:

   .. code-block:: text

       {{ agent_data.response }}

   {% if agent_data.visualization_data %}
   **Visualization Data Available**:
   - Conversation history: {{ agent_data.visualization_data.conversation_history|length }} messages
   - Final state: {{ agent_data.visualization_data.final_state|length }} fields
   {% endif %}
```

### ReactAgent Template with Tool Calls

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set execution = agent_data.execution_data.executions[0] %}

   ReactAgent with Tools
   =====================

   ReactAgent with calculator and word counter tools:

   .. code-block:: python

       from haive.agents.react import ReactAgent
       from haive.core.engine.aug_llm import AugLLMConfig
       from langchain_core.tools import tool

       @tool
       def calculator(expression: str) -> str:
           """Calculate mathematical expressions."""
           return str(eval(expression))

       @tool
       def word_counter(text: str) -> str:
           """Count words in text."""
           return f"Word count: {len(text.split())}"

       config = AugLLMConfig(temperature=0.3)
       agent = ReactAgent(
           name="demo",
           engine=config,
           tools=[calculator, word_counter]
       )

       response = agent.run("{{ execution.input_text }}")

   **Response**:

   .. code-block:: text

       {{ agent_data.response }}

   {% if agent_data.tool_calls %}
   **Tool Usage**:
   {% for call in agent_data.tool_calls %}
   - {{ call.tool_name }}: {{ call.tool_args }}
   {% endfor %}
   {% endif %}

   **Execution Time**: {{ "%.2f"|format(execution.execution_summary.duration_seconds) }}s
```

## 📊 State Schema Templates

### MessagesState Schema

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "simple", "focus": "messages_state"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   MessagesState Usage
   ===================

   The agent uses MessagesState for conversation management:

   .. code-block:: python

       from haive.core.schema.prebuilt.messages_state import MessagesState

       # State automatically manages conversation history
       state = MessagesState()
       state.add_message(HumanMessage(content="Hello"))

       # Agent processes with state
       result = agent.run(state)

   **Message Flow**:

   {% if agent_data.execution_data.executions[0].state_history %}
   {% for state_update in agent_data.execution_data.executions[0].state_history %}
   {{ loop.index }}. **{{ state_update.timestamp }}**: {{ state_update.state.messages|length }} messages
   {% endfor %}
   {% endif %}
```

### ToolState Schema

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "focus": "tool_state"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   ToolState Schema
   ================

   ReactAgent uses ToolState for tool management:

   .. code-block:: python

       from haive.core.schema.prebuilt.tool_state import ToolState

       # State manages both messages and tools
       state = ToolState(tools=[calculator, word_counter])

       # Tools are automatically routed based on type
       print(f"Tool routes: {state.tool_routes}")

   **Tool Configuration**:

   {% if agent_data.execution_data.executions[0].agent_type == "react" %}
   - Tools available: {{ agent_data.execution_data.executions[0].state_history[0].state.tools_used|length }}
   - Tool routes configured: Yes
   - Engine route config: LLM tools supported
   {% endif %}
```

### Custom State Schema

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "custom", "schema": "PlanExecuteState"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Custom State Schema
   ===================

   Creating custom state schemas:

   .. code-block:: python

       from haive.core.schema.state_schema import StateSchema
       from pydantic import Field
       from typing import List, Dict, Any

       class PlanExecuteState(StateSchema):
           """Custom state for planning agents."""

           plan: List[str] = Field(default_factory=list)
           current_step: int = Field(default=0)
           execution_results: Dict[str, Any] = Field(default_factory=dict)

           def add_step(self, step: str):
               """Add a step to the plan."""
               self.plan.append(step)

           def complete_step(self, result: Any):
               """Mark current step as complete."""
               self.execution_results[self.current_step] = result
               self.current_step += 1

   **Usage Example**:

   .. code-block:: python

       state = PlanExecuteState()
       state.add_step("Research topic")
       state.add_step("Write summary")

       # Agent processes with custom state
       agent = PlanningAgent(state_schema=PlanExecuteState)
       result = agent.run("Create a report on AI", state=state)
```

## 🔄 Graph Visualization Templates

### Basic Graph Template

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "include_graph": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Agent Graph Structure
   =====================

   {% if agent_data.graph_data and agent_data.graph_data.has_graph %}
   The agent uses this graph structure:

   .. raw:: html

       <div class="agent-graph-container">
           <div id="agent-graph-{{ agent_type }}"></div>
       </div>

       <script>
       // Initialize graph visualization
       const graphData = {{ agent_data.graph_data|tojson }};
       const visualizer = new AgentDemoVisualizer();
       visualizer.createGraphVisualization(graphData, 'agent-graph-{{ agent_type }}');
       </script>

   **Graph Details**:
   - Nodes: {{ agent_data.graph_data.nodes|length }}
   - Edges: {{ agent_data.graph_data.edges|length }}
   - Graph type: {{ agent_data.graph_data.graph_type }}
   {% else %}
   This agent doesn't expose graph structure.
   {% endif %}
```

### Interactive Graph with Mermaid

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "mermaid": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Interactive Agent Flow
   ======================

   {% if agent_data.graph_data.mermaid_available %}
   .. raw:: html

       <div class="mermaid-container">
           <div class="mermaid" id="mermaid-{{ agent_type }}">
           graph TD
           {% for node in agent_data.graph_data.nodes %}
           {{ node.id }}[{{ node.type }}]
           {% endfor %}
           {% for edge in agent_data.graph_data.edges %}
           {{ edge.from }} --> {{ edge.to }}
           {% endfor %}
           </div>
       </div>

       <script>
       // Initialize Mermaid
       mermaid.initialize({startOnLoad: true});
       </script>
   {% endif %}

   **Execution Flow**:

   {% if agent_data.execution_data.executions[0].execution_trace %}
   {% for step in agent_data.execution_data.executions[0].execution_trace %}
   {{ loop.index }}. **{{ step.node }}** ({{ step.action }}) - {{ step.timestamp }}
   {% endfor %}
   {% endif %}
```

## 🎛️ Advanced Template Features

### Conditional Content

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   {% if agent_data.tool_calls %}
   Tool Usage Demo
   ===============
   This agent used {{ agent_data.tool_calls|length }} tools.
   {% else %}
   Basic Agent Demo
   ================
   This agent completed without tool usage.
   {% endif %}
```

### Loops and Data Processing

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Multiple Executions
   ===================

   {% for execution in agent_data.execution_data.executions %}

   Execution {{ loop.index }}
   --------------------------

   **Input**: {{ execution.input_text }}

   **Output**: {{ execution.agent_output }}

   **Duration**: {{ "%.2f"|format(execution.execution_summary.duration_seconds) }}s

   {% if execution.visualization_data.tool_calls %}
   **Tools Used**:
   {% for call in execution.visualization_data.tool_calls %}
   - {{ call.tool_name }}: {{ call.tool_args }}
   {% endfor %}
   {% endif %}

   {% endfor %}
```

### Custom Filters

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "simple"}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Response Analysis
   =================

   **Response Length**: {{ agent_data.response|length }} characters
   **Word Count**: {{ agent_data.response.split()|length }} words
   **First Line**: {{ agent_data.response.split('\n')[0] }}

   {% if agent_data.response|length > 100 %}
   **Summary**: {{ agent_data.response[:100] }}...
   {% else %}
   **Full Response**: {{ agent_data.response }}
   {% endif %}
```

## 📋 Template Conversion Checklist

### Before Converting

- [ ] Identify static content that should be dynamic
- [ ] Check if cached data exists for the agent type
- [ ] Review existing template patterns
- [ ] Plan visualization needs

### During Conversion

- [ ] Add Jinja2 directive with correct context
- [ ] Replace static content with template variables
- [ ] Add conditional blocks for optional content
- [ ] Include execution metadata and timing
- [ ] Add tool call information if applicable
- [ ] Include graph visualization if available

### After Conversion

- [ ] Test template rendering
- [ ] Verify all data displays correctly
- [ ] Check formatting and styling
- [ ] Ensure links and references work
- [ ] Test with different agent types
- [ ] Update navigation if needed

## 🔍 Debugging Templates

### Common Issues

1. **Template not rendering**: Check Jinja2 directive syntax
2. **Data not available**: Verify cache file exists and loader works
3. **Formatting errors**: Check RST syntax after template processing
4. **Missing variables**: Add default values with `|default("")`

### Debug Commands

```bash
# Test template processing
poetry run python -c "
from docs.scripts.agent_demos.agent_cache_loader import AgentCacheLoader
loader = AgentCacheLoader()
data = loader.get_agent_demo_context('simple')
print(data.keys())
"

# Build with debug
nox -s docs_fast -- --verbose
```

## 📚 Examples Gallery

### File Locations

- `docs/source/agents/demos/simple-demo-cached.rst` - SimpleAgent template
- `docs/source/agents/demos/react-demo.rst` - ReactAgent template
- `docs/source/agents/demos/index.rst` - Demo index with all agents

### Live Examples

See the built documentation at `/docs/build/html/agents/demos/` for rendered examples.

---

This guide provides everything needed to convert static agent examples to dynamic Jinja2 templates. The template system makes documentation maintenance easier and ensures examples always show real, up-to-date agent behavior.
