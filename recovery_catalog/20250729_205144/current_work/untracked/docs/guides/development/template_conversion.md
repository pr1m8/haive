# Template Conversion Workflow

This document provides a step-by-step workflow for converting static agent examples to dynamic Jinja2 templates in the Haive documentation system.

## 🎯 Quick Start Workflow

### 1. **Identify Files to Convert**

Current files that need conversion:

```bash
docs/source/agents/demos/
├── adaptiverag-demo.rst         # ⏳ To convert
├── baserag-demo.rst             # ⏳ To convert
├── debate-demo.rst              # ⏳ To convert
├── personresearch-demo.rst      # ⏳ To convert
├── planandexecute-demo.rst      # ⏳ To convert
├── react-demo.rst               # ⏳ To convert
├── reactwithmemory-demo.rst     # ⏳ To convert
├── reflection-demo.rst          # ⏳ To convert
├── simple-demo.rst              # ⏳ To convert
├── structuredoutput-demo.rst    # ⏳ To convert
├── summarizer-demo.rst          # ⏳ To convert
├── simple-demo-cached.rst       # ✅ Already converted
└── simple-demo-test.rst         # ✅ Test template
```

### 2. **Check Available Cache Data**

```bash
# Check what cached data is available
ls docs/source/agent_cache_*.json
# Current: agent_cache_simple.json, agent_cache_react.json

# Check cache contents
poetry run python -c "
from docs.scripts.agent_demos.agent_cache_loader import AgentCacheLoader
loader = AgentCacheLoader()
print('Available agent types:', loader.get_available_agent_types())
"
```

### 3. **Generate Additional Cache Data (If Needed)**

```bash
# Generate cache for additional agent types
poetry run python scripts/generate_agent_cache.py custom_agent_type

# Or extend existing cache generation script for new agents
```

## 📋 Step-by-Step Conversion Process

### Step 1: Analyze the Original File

**Example**: Converting `react-demo.rst`

**Original Content**:

```rst
ReactAgent Demo
===============

This demonstrates the ReactAgent with tools.

.. code-block:: python

    from haive.agents.react import ReactAgent

    agent = ReactAgent(name="demo", tools=[calculator])
    response = agent.run("What is 2+2?")
    print(response)  # Hardcoded: "The answer is 4"

The agent can use tools to solve problems.
```

### Step 2: Identify Dynamic Content

**Static Content** (to replace):

- Hardcoded responses: `"The answer is 4"`
- Example inputs: `"What is 2+2?"`
- Tool usage descriptions without real data

**Dynamic Content** (from cache):

- Real agent responses
- Actual tool calls made
- Execution timing and metadata
- Graph visualization data

### Step 3: Create Template Structure

**Template Framework**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set execution = agent_data.execution_data.executions[0] %}

   ReactAgent Demo
   ===============

   This demonstrates the ReactAgent with tools using real execution data.

   [CONTENT GOES HERE]
```

### Step 4: Replace Static Content

**Before**:

```rst
.. code-block:: python

    agent = ReactAgent(name="demo", tools=[calculator])
    response = agent.run("What is 2+2?")
    print(response)  # Hardcoded: "The answer is 4"
```

**After**:

```rst
.. code-block:: python

    agent = ReactAgent(name="demo", tools=[calculator])
    response = agent.run("{{ execution.input_text }}")
    print(response)

**Real Output** (from cached execution):

.. code-block:: text

    {{ agent_data.response }}

**Execution Details**:
- Duration: {{ "%.2f"|format(execution.execution_summary.duration_seconds) }}s
- Events: {{ execution.execution_summary.total_events }}
```

### Step 5: Add Advanced Features

**Tool Usage**:

```rst
{% if agent_data.tool_calls %}
**Tool Calls Made**:
{% for call in agent_data.tool_calls %}
- **{{ call.tool_name }}**: {{ call.tool_args }}
{% endfor %}
{% endif %}
```

**Graph Visualization**:

```rst
{% if agent_data.graph_data and agent_data.graph_data.has_graph %}
**Agent Graph**:

.. raw:: html

    <div class="agent-graph-container">
        <div id="agent-graph-react" class="graph-display"></div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const graphData = {{ agent_data.graph_data|tojson }};
        const visualizer = new AgentDemoVisualizer();
        visualizer.createGraphVisualization(graphData, 'agent-graph-react');
    });
    </script>
{% endif %}
```

### Step 6: Test and Validate

```bash
# Test the template
nox -s docs_fast

# Check for errors
grep -r "ERROR" docs/build/html/

# Validate specific page
open docs/build/html/agents/demos/react-demo.html
```

## 🗂️ Agent Type Mappings

### Available Agent Types

| Agent Type | Cache File                | Template Context           | Special Features         |
| ---------- | ------------------------- | -------------------------- | ------------------------ |
| `simple`   | `agent_cache_simple.json` | `{"agent_type": "simple"}` | Basic conversation       |
| `react`    | `agent_cache_react.json`  | `{"agent_type": "react"}`  | Tool calls, reasoning    |
| `rag`      | _Need to generate_        | `{"agent_type": "rag"}`    | Document retrieval       |
| `multi`    | _Need to generate_        | `{"agent_type": "multi"}`  | Multi-agent coordination |

### Agent Type to Demo File Mapping

| Demo File                   | Agent Type     | Status        | Notes                                |
| --------------------------- | -------------- | ------------- | ------------------------------------ |
| `simple-demo.rst`           | `simple`       | ✅ Ready      | Use existing cache                   |
| `react-demo.rst`            | `react`        | ✅ Ready      | Use existing cache                   |
| `reactwithmemory-demo.rst`  | `react`        | ✅ Ready      | Use react cache                      |
| `baserag-demo.rst`          | `rag`          | ⏳ Need cache | Generate RAG cache                   |
| `adaptiverag-demo.rst`      | `rag`          | ⏳ Need cache | Generate RAG cache                   |
| `planandexecute-demo.rst`   | `plan_execute` | ⏳ Need cache | Generate P&E cache                   |
| `summarizer-demo.rst`       | `summarizer`   | ⏳ Need cache | Generate summarizer cache            |
| `debate-demo.rst`           | `debate`       | ⏳ Need cache | Generate debate cache                |
| `reflection-demo.rst`       | `reflection`   | ⏳ Need cache | Generate reflection cache            |
| `personresearch-demo.rst`   | `research`     | ⏳ Need cache | Generate research cache              |
| `structuredoutput-demo.rst` | `simple`       | ✅ Ready      | Use simple cache + structured output |

## 🔧 Common Template Patterns

### 1. **Basic Agent Demo**

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "AGENT_TYPE"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set execution = agent_data.execution_data.executions[0] %}

   AGENT_NAME Demo
   ===============

   Basic usage example:

   .. code-block:: python

       from haive.agents.MODULE import AGENT_CLASS
       from haive.core.engine.aug_llm import AugLLMConfig

       config = AugLLMConfig(temperature=0.7)
       agent = AGENT_CLASS(name="demo", engine=config)

       response = agent.run("{{ execution.input_text }}")

   **Response**:

   .. code-block:: text

       {{ agent_data.response }}
```

### 2. **Agent with Tools**

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set execution = agent_data.execution_data.executions[0] %}

   ReactAgent with Tools
   =====================

   .. code-block:: python

       @tool
       def calculator(expression: str) -> str:
           """Calculate expressions."""
           return str(eval(expression))

       agent = ReactAgent(
           name="demo",
           engine=config,
           tools=[calculator]
       )

       response = agent.run("{{ execution.input_text }}")

   **Response**:

   .. code-block:: text

       {{ agent_data.response }}

   {% if agent_data.tool_calls %}
   **Tool Calls**:
   {% for call in agent_data.tool_calls %}
   - {{ call.tool_name }}({{ call.tool_args }})
   {% endfor %}
   {% endif %}
```

### 3. **Agent with State Schema**

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "AGENT_TYPE", "show_state": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Agent with Custom State
   =======================

   .. code-block:: python

       from haive.core.schema.state_schema import StateSchema

       class CustomState(StateSchema):
           field1: str = Field(...)
           field2: int = Field(default=0)

       agent = AGENT_CLASS(
           name="demo",
           engine=config,
           state_schema=CustomState
       )

   {% if agent_data.execution_data.executions[0].state_history %}
   **State Evolution**:
   {% for state in agent_data.execution_data.executions[0].state_history %}
   {{ loop.index }}. {{ state.timestamp }} - {{ state.state.keys()|list }}
   {% endfor %}
   {% endif %}
```

### 4. **Agent with Visualization**

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "include_graph": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Agent Visualization
   ===================

   {% if agent_data.graph_data and agent_data.graph_data.has_graph %}
   **Agent Graph**:

   .. raw:: html

       <div class="agent-graph-container">
           <div id="agent-graph-{{ agent_type }}" class="graph-display"></div>
       </div>

       <script>
       document.addEventListener('DOMContentLoaded', function() {
           const graphData = {{ agent_data.graph_data|tojson }};
           const visualizer = new AgentDemoVisualizer();
           visualizer.createGraphVisualization(graphData, 'agent-graph-{{ agent_type }}');
       });
       </script>
   {% endif %}
```

## 🚀 Batch Conversion Process

### Convert All Simple Agents

```bash
# These can use the existing simple cache
FILES_TO_CONVERT=(
    "simple-demo.rst"
    "structuredoutput-demo.rst"
)

for file in "${FILES_TO_CONVERT[@]}"; do
    echo "Converting $file..."
    # Apply simple agent template pattern
done
```

### Convert ReactAgent Variants

```bash
# These can use the existing react cache
FILES_TO_CONVERT=(
    "react-demo.rst"
    "reactwithmemory-demo.rst"
)

for file in "${FILES_TO_CONVERT[@]}"; do
    echo "Converting $file..."
    # Apply react agent template pattern
done
```

### Generate New Caches

```bash
# Create cache generation scripts for missing agent types
AGENT_TYPES=(
    "rag"
    "plan_execute"
    "summarizer"
    "debate"
    "reflection"
    "research"
)

for agent_type in "${AGENT_TYPES[@]}"; do
    echo "Generating cache for $agent_type..."
    # Extend generate_agent_cache.py
done
```

## 🔍 Quality Assurance

### Validation Checklist

For each converted file:

- [ ] Template directive is correct
- [ ] Agent type context is appropriate
- [ ] All variables are properly referenced
- [ ] Conditional blocks handle missing data
- [ ] Graph visualization works (if applicable)
- [ ] Tool calls display correctly (if applicable)
- [ ] Page builds without errors
- [ ] Content is accurate and helpful

### Testing Commands

```bash
# Build and test specific file
nox -s docs_fast -- agents/demos/react-demo.html

# Check for template errors
grep -r "jinja2" docs/build/html/ | grep -i error

# Validate all demo pages
for file in docs/source/agents/demos/*.rst; do
    echo "Testing $file..."
    # Check if builds successfully
done
```

## 📊 Progress Tracking

### Conversion Status

```bash
# Track progress
echo "📊 Conversion Progress:"
echo "✅ Completed: 2/11 files"
echo "⏳ In Progress: 9/11 files"
echo "🎯 Target: 11/11 files"
echo ""
echo "Cache Status:"
echo "✅ SimpleAgent: Available"
echo "✅ ReactAgent: Available"
echo "⏳ RAG agents: Need to generate"
echo "⏳ Planning agents: Need to generate"
echo "⏳ Multi-agent: Need to generate"
```

### Completion Metrics

- **Files converted**: 2/11 (18%)
- **Cache files available**: 2/6 (33%)
- **Visualization ready**: 100% (framework complete)
- **Documentation**: 100% (guides complete)

## 🎯 Next Steps

### Immediate Actions

1. **Convert Simple Cases**: Start with files that can use existing caches
2. **Generate Missing Caches**: Create cache data for remaining agent types
3. **Test Thoroughly**: Validate each conversion before moving to next
4. **Update Navigation**: Ensure all links work correctly

### Long-term Goals

1. **Automated Conversion**: Create script to automate template conversion
2. **Cache Management**: Implement cache refresh and update system
3. **Enhanced Visualizations**: Add more interactive features
4. **Performance Optimization**: Optimize build times and page loading

---

This workflow provides a complete guide for converting all static agent examples to dynamic Jinja2 templates, ensuring consistent, maintainable, and engaging documentation throughout the Haive project.
