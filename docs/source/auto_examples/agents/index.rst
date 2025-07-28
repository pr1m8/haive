:orphan:

# Haive Agent Examples

This directory contains demonstration scripts showing how to use the new agent patterns created using `agent.py`, `SimpleAgentV3`, and `EnhancedMultiAgentV4` as foundations.

## Overview

These examples demonstrate:

- Sequential multi-agent workflows (ReactAgent → SimpleAgent)
- Structured output with Pydantic models
- Chat prompt templates with input variables
- Pre/post processing hooks
- Real component usage (no mocks)

## Examples

### 1. `working_sequential_demo.py` ✅ TESTED & WORKING

Demonstrates a simple ReactAgent → SimpleAgent sequential flow:

- ReactAgent with tools for market analysis
- SimpleAgent with structured output (FinalReport model)
- Prompt templates with input variables
- Real execution with Azure OpenAI

```bash
poetry run python packages/haive-agents/examples/working_sequential_demo.py
```

### 2. `basic_agent_test.py` ✅ TESTED & WORKING

Tests individual agents without multi-agent orchestration:

- SimpleAgentV3 with structured output
- ReactAgent with tools
- Manual sequential execution

```bash
poetry run python packages/haive-agents/examples/basic_agent_test.py
```

### 3. `simple_sequential_demo.py`

More complex demo with hooks and multiple workflows:

- React → Simple with structured output
- Multi-agent workflow with hooks
- Structured output chain

```bash
poetry run python packages/haive-agents/examples/simple_sequential_demo.py
```

### 4. `sequential_multi_agent_demo.py`

Comprehensive demo using pattern files:

- Multiple workflow patterns
- RAG agents with structured output
- Research workflows
- Reflection patterns

```bash
poetry run python packages/haive-agents/examples/sequential_multi_agent_demo.py
```

### 5. `reflection_hooks_demo.py`

Advanced patterns with reflection and hooks:

- Pre/post processing agents
- Reflection workflows
- Quality gates and iterative improvement
- Comprehensive hook monitoring

```bash
poetry run python packages/haive-agents/examples/reflection_hooks_demo.py
```

## Key Patterns Demonstrated

### 1. Sequential Agent Flow

```python
# ReactAgent for analysis
react_agent = ReactAgent(
    name="analyst",
    engine=AugLLMConfig(tools=[tool1, tool2])
)

# SimpleAgent for structured output
simple_agent = SimpleAgentV3(
    name="formatter",
    engine=AugLLMConfig(structured_output_model=OutputModel)
)

# Execute sequentially
analysis = await react_agent.arun("Analyze X")
report = await simple_agent.arun({"analysis": analysis})
```

### 2. Structured Output Models

```python
class FinalReport(BaseModel):
    title: str = Field(description="Report title")
    key_findings: List[str] = Field(description="Main findings")
    confidence: float = Field(ge=0.0, le=1.0)
```

### 3. Prompt Templates with Variables

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("human", "Analyze: {topic}\nContext: {context}")
])
```

### 4. Hook Patterns

```python
@workflow.before_agent_execution
def log_start(agent_name: str, state: dict):
    print(f"Starting {agent_name}")

@workflow.after_agent_execution
def log_end(agent_name: str, result: Any):
    print(f"Completed {agent_name}")
```

## Pattern Files Created

The following pattern files were created in `packages/haive-agents/src/haive/agents/patterns/`:

1. **`simple_rag_agent_pattern.py`** - RAG agents using SimpleAgentV3 as base
2. **`sequential_workflow_agent.py`** - Workflow patterns using EnhancedMultiAgentV4
3. **`react_structured_agent_variants.py`** - React → Structured patterns
4. **`hybrid_multi_agent_patterns.py`** - Advanced hybrid agent patterns

## Notes

- All examples use real LLM execution (Azure OpenAI)
- No mocks are used - everything is tested with real components
- The patterns directory needs proper imports to work with multi-agent demos
- SimpleAgentV3 and ReactAgent work well individually
- EnhancedMultiAgentV4 has some type validation issues that need resolution



.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demonstrates the powerful pattern of adding structured output to any agent using the class method approach with future annotations.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_agent_with_structured_output_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_agent_with_structured_output.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example showing how to use the with_structured_output class method.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo shows how branching and structured output models work together: 1. Agent produces structured output 2. Routing function uses structured output to decide next agent 3. Different agents handle different branches with their own structured outputs 4. State flows consistently across all branches">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_branching_structured_output_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_branching_structured_output_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Branching and Structured Output Demo - V3/V4 Architecture.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo uses: - SimpleAgentV3 (with enhanced base agent) - ReactAgent (standard version) - EnhancedMultiAgentV4 (with enhanced base agent and AgentNodeV3)">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_consistent_v3_v4_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_consistent_v3_v4_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Consistent V3/V4 Demo - Using the latest enhanced base agent patterns.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Debug EnhancedMultiAgentV4 state handling with V3 agents.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_debug_multi_agent_v4_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_debug_multi_agent_v4.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Debug EnhancedMultiAgentV4 state handling with V3 agents.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the basic usage of the Dynamic Activation Pattern with real components following Pydantic best practices.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_dynamic_activation_basic_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_dynamic_activation_basic_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Basic Dynamic Activation Pattern Example.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the DynamicReactAgent&#x27;s ability to: 1. Start with basic tools 2. Discover and load new tools dynamically 3. Use both discovery agents and RAG-based tool finding 4. Show the &quot;tool that exists to search for other tools&quot; functionality">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_dynamic_react_agent_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_dynamic_react_agent_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example: DynamicReactAgent with Dynamic Tool Discovery.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demonstrates the dynamic supervisor with real agents, following the pattern we built in experiments.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_dynamic_supervisor_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_dynamic_supervisor_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dynamic Supervisor Demo - Shows the working implementation.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the dynamic supervisor agent coordinating multiple specialized agents to handle complex, multi-step tasks.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_dynamic_supervisor_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_dynamic_supervisor_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dynamic Supervisor Example.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates: 1. The enhanced agent pattern: Agent[EngineT] 2. How SimpleAgent is just Agent[AugLLMConfig] 3. How different engine types create different agent types 4. The clean type safety this provides">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_enhanced_agent_pattern_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_enhanced_agent_pattern_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Enhanced Agent Pattern Demo - Shows the engine-focused generic pattern.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the Enhanced Self-Query Memory Retriever that builds on the memory classification system to provide intelligent, context-aware retrieval.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_enhanced_memory_retriever_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_enhanced_memory_retriever_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Enhanced Memory Retriever Demo - Phase 2 Implementation.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates: 1. Enhanced base agent pattern (extending Agent, implementing build_graph) 2. Direct list initialization of agents 3. Sequential execution mode 4. AgentNodeV3 integration for state projection 5. Real LLM execution (no mocks)">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_enhanced_multi_agent_v4_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_enhanced_multi_agent_v4_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of Enhanced MultiAgent V4 - Sequential ReactAgent → SimpleAgent pattern.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo shows that: 1. SimpleAgentV3 and ReactAgentV3 work individually 2. EnhancedMultiAgentV4 works with V3 agents in sequential mode 3. All components use the enhanced base agent architecture consistently 4. Structured output and tool integration work properly">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_final_v3_v4_working_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_final_v3_v4_working_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Final V3/V4 Working Demo - Complete consistency verified.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This shows the supervisor actually executing agent handoffs with real state management.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_full_supervisor_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_full_supervisor_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Full Supervisor Demo - Complete workflow demonstration.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how the hook patterns from reflection agents have been generalized to work with any enhanced agent, providing comprehensive monitoring and processing capabilities.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_generalized_hooks_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_generalized_hooks_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating the generalized hook system in enhanced agents.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates: 1. ReactAgent with tools → SimpleAgent with structured output 2. Prompt templates with input variables 3. Hook integration for monitoring 4. Reflection patterns">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_multi_agent_structured_output_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_multi_agent_structured_output_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Multi-Agent Structured Output Demo</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Demo of OutputAdapter and transformation functionality.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_output_adapter_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_output_adapter_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Demo of OutputAdapter and transformation functionality.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to use the PlanAndExecuteAgent to: 1. Create a plan for a complex task 2. Execute steps with tool access 3. Handle replanning when needed">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_plan_and_execute_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_plan_and_execute_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of using the Plan and Execute Agent.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo showcases: 1. Pre/post processing agents with reflection 2. Hook system for monitoring agent execution 3. Structured output with reflection patterns 4. Multi-stage workflows with quality gates">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_reflection_hooks_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_reflection_hooks_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Reflection and Hooks Demo - Advanced multi-agent patterns with reflection.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example of using the Self-Discover agent.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_self_discover_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_self_discover_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of using the Self-Discover agent.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example of using the Self-Discover Sequential V2 agent with proper patterns.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_self_discover_sequential_v2_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_self_discover_sequential_v2_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of using the Self-Discover Sequential V2 agent with proper patterns.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example of Self-Discover V4 with proper state handling.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_self_discover_v4_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_self_discover_v4_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of Self-Discover V4 with proper state handling.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo shows how to use the new agent patterns created with agent.py, SimpleAgentV3, and EnhancedMultiAgentV4 as foundations. It demonstrates:">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_sequential_multi_agent_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_sequential_multi_agent_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Sequential Multi-Agent Demo - Showcasing new pattern implementations.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example script with invalid Python syntax ">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_simple_agent_v3_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_simple_agent_v3_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">SyntaxError</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demonstrates the generalized hook system working with SimpleAgentV3, showing how the reflection patterns have been integrated into the enhanced base agent.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_simple_agent_v3_hooks_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_simple_agent_v3_hooks_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">SimpleAgentV3 with Generalized Hooks Demo.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This simplified demo shows the core branching concepts: 1. Classifier produces structured output 2. Router uses structured output to choose next agent 3. Different specialized agents handle different cases 4. All use V3/V4 architecture consistently">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_simple_branching_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_simple_branching_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Simple Branching Demo - Working V3/V4 Branching with Structured Output.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demo shows how to use the core agent classes directly: - SimpleAgentV3 - ReactAgent - EnhancedMultiAgentV4">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_simple_sequential_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_simple_sequential_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Simple Sequential Multi-Agent Demo - Direct usage without patterns module.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script demonstrates how to use StructuredOutputAgent to convert any agent&#x27;s output into structured formats.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_structured_output_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_structured_output_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example usage of StructuredOutputAgent in multi-agent workflows.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to use the TokenTrackingAgent base class to automatically track token usage and costs for LLM-based agents.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_token_tracking_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_token_tracking_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of using TokenTrackingAgent for cost-aware agent development.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example showing SimpleAgentWithValidation in action.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_validation_integration_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_validation_integration_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example showing SimpleAgentWithValidation in action.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Working Sequential Demo - Shows ReactAgent → SimpleAgent with structured output.">

.. only:: html

  .. image:: /auto_examples/agents/images/thumb/sphx_glr_working_sequential_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_working_sequential_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Working Sequential Demo - Shows ReactAgent → SimpleAgent with structured output.</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/agents/agent_with_structured_output
   /auto_examples/agents/branching_structured_output_demo
   /auto_examples/agents/consistent_v3_v4_demo
   /auto_examples/agents/debug_multi_agent_v4
   /auto_examples/agents/dynamic_activation_basic_example
   /auto_examples/agents/dynamic_react_agent_example
   /auto_examples/agents/dynamic_supervisor_demo
   /auto_examples/agents/dynamic_supervisor_example
   /auto_examples/agents/enhanced_agent_pattern_demo
   /auto_examples/agents/enhanced_memory_retriever_demo
   /auto_examples/agents/enhanced_multi_agent_v4_example
   /auto_examples/agents/final_v3_v4_working_demo
   /auto_examples/agents/full_supervisor_demo
   /auto_examples/agents/generalized_hooks_example
   /auto_examples/agents/multi_agent_structured_output_demo
   /auto_examples/agents/output_adapter_demo
   /auto_examples/agents/plan_and_execute_example
   /auto_examples/agents/reflection_hooks_demo
   /auto_examples/agents/self_discover_example
   /auto_examples/agents/self_discover_sequential_v2_example
   /auto_examples/agents/self_discover_v4_example
   /auto_examples/agents/sequential_multi_agent_demo
   /auto_examples/agents/simple_agent_v3_example
   /auto_examples/agents/simple_agent_v3_hooks_demo
   /auto_examples/agents/simple_branching_demo
   /auto_examples/agents/simple_sequential_demo
   /auto_examples/agents/structured_output_example
   /auto_examples/agents/token_tracking_example
   /auto_examples/agents/validation_integration_example
   /auto_examples/agents/working_sequential_demo

# Supervisor Examples

This directory contains comprehensive examples demonstrating different supervisor patterns and usage scenarios. Examples are organized by complexity and use case.

## Directory Structure

### `/basic/`

Simple, straightforward examples for getting started:

- **basic_supervisor_example.py** - Basic supervisor with multiple agents

### `/advanced/`

Complex examples showing sophisticated patterns:

- **dynamic_activation_example.py** - Dynamic agent activation based on capabilities

### `/patterns/`

Architectural pattern demonstrations:

- **agent_execution_node_pattern.py** - Agent execution node pattern
- **dynamic_tool_generation_pattern.py** - Dynamic tool generation
- **state_synchronized_tools_pattern.py** - State-synchronized tool management
- **base_supervisor_pattern.py** - Base supervisor implementation
- **three_node_supervisor_pattern.py** - Three-node supervisor architecture
- **integrated_supervisor_with_handoff.py** - Integrated supervisor with handoffs
- **enhanced_supervisor_with_choice.py** - Enhanced supervisor with choice models

## Quick Start

### Basic Supervisor Usage

```python
from haive.agents.dynamic_supervisor import create_dynamic_supervisor
from haive.agents.simple import SimpleAgent

# Create supervisor
supervisor = create_dynamic_supervisor(name="task_router")

# Create state and add agents
state = supervisor.create_initial_state()
state.add_agent("math_agent", math_agent, "Mathematics expert")
state.add_agent("search_agent", search_agent, "Web search specialist")

# Route tasks
result = await supervisor.arun("Calculate 15 * 23", state=state)
```

### Running Examples

```bash
# Run basic example
poetry run python examples/supervisor/basic/basic_supervisor_example.py

# Run advanced example
poetry run python examples/supervisor/advanced/dynamic_activation_example.py

# Run pattern examples
poetry run python examples/supervisor/patterns/agent_execution_node_pattern.py
```

## Example Categories

### 1. Basic Examples

#### basic_supervisor_example.py

Demonstrates fundamental supervisor concepts:

- Creating specialized agents
- Setting up supervisor with factory function
- Adding agents to supervisor state
- Basic task routing
- Multi-step coordination

**Key Concepts:**

- Agent specialization
- Supervisor configuration
- State management
- Task routing

**Use Cases:**

- Simple task delegation
- Multi-agent coordination
- Basic routing decisions

### 2. Advanced Examples

#### dynamic_activation_example.py

Shows sophisticated agent lifecycle management:

- Starting with subset of active agents
- Keeping agents in registry but inactive
- Task analysis to identify required capabilities
- Dynamic agent activation based on need
- Resource-efficient multi-agent systems

**Key Concepts:**

- Capability-based routing
- Agent lifecycle management
- Resource optimization
- Dynamic activation

**Use Cases:**

- Resource-constrained environments
- Scalable multi-agent systems
- On-demand agent activation
- Cost-efficient agent management

### 3. Pattern Examples

#### agent_execution_node_pattern.py

Demonstrates clean agent execution architecture:

- Single generic execution node
- State-based routing decisions
- Clean separation of concerns
- Flexible agent selection

**Key Concepts:**

- Agent execution node
- State-based routing
- Generic execution patterns
- Clean architecture

#### dynamic_tool_generation_pattern.py

Shows dynamic tool creation and management:

- Registry-based tool generation
- Dynamic choice models
- Tool rebuilding on changes
- Validated agent selection

**Key Concepts:**

- Dynamic tool creation
- Registry patterns
- Choice model integration
- Tool lifecycle management

#### state_synchronized_tools_pattern.py

Demonstrates state-tool synchronization:

- Tools synchronized from state
- State-driven tool generation
- Complex state management
- Tool-state coordination

**Key Concepts:**

- State-tool synchronization
- Complex state management
- Tool generation patterns
- State coordination

## Running Examples

### Prerequisites

```bash
# Install dependencies
poetry install

# Set up environment variables (if needed)
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

### Basic Execution

```bash
# Run from project root
poetry run python examples/supervisor/basic/basic_supervisor_example.py

# Run with verbose output
poetry run python examples/supervisor/basic/basic_supervisor_example.py --verbose

# Run specific pattern
poetry run python examples/supervisor/patterns/agent_execution_node_pattern.py
```

### Advanced Execution

```bash
# Run with custom configuration
poetry run python examples/supervisor/advanced/dynamic_activation_example.py --config custom_config.json

# Run with different models
poetry run python examples/supervisor/basic/basic_supervisor_example.py --model gpt-4-turbo

# Run with debugging
poetry run python examples/supervisor/patterns/dynamic_tool_generation_pattern.py --debug
```

## Example Modifications

### Customizing Agents

```python
# Create custom agents for your use case
custom_agent = SimpleAgent(
    name="custom_agent",
    engine=AugLLMConfig(
        model="gpt-4",
        tools=[your_custom_tools],
        system_message="Your custom system message"
    )
)

# Add to supervisor
state.add_agent("custom", custom_agent, "Custom agent description")
```

### Modifying Supervisor Configuration

```python
# Create custom supervisor
supervisor = DynamicSupervisorAgent(
    name="custom_supervisor",
    engine=AugLLMConfig(
        model="gpt-4",
        temperature=0.0,
        system_message="Custom supervisor instructions"
    ),
    enable_agent_builder=True,
    auto_sync_tools=True
)
```

### Adding Custom Tools

```python
from langchain_core.tools import tool

@tool
def custom_tool(input_data: str) -> str:
    \"\"\"Custom tool for specific functionality.\"\"\"
    # Your tool implementation
    return processed_result

# Add to agent
agent = SimpleAgent(
    name="tool_agent",
    engine=AugLLMConfig(tools=[custom_tool])
)
```

## Common Patterns

### 1. Multi-Domain Coordination

```python
# Agents for different domains
agents = {
    "math": create_math_agent(),
    "search": create_search_agent(),
    "code": create_code_agent(),
    "analysis": create_analysis_agent()
}

# Supervisor coordinates across domains
for name, agent in agents.items():
    state.add_agent(name, agent, f"{name.title()} specialist")
```

### 2. Hierarchical Supervision

```python
# Create sub-supervisors for specific domains
research_supervisor = create_research_supervisor()
analysis_supervisor = create_analysis_supervisor()

# Main supervisor coordinates sub-supervisors
state.add_agent("research", research_supervisor, "Research coordination")
state.add_agent("analysis", analysis_supervisor, "Analysis coordination")
```

### 3. Conditional Agent Activation

```python
# Activate agents based on task analysis
task_analysis = analyze_task(user_request)

for capability in task_analysis.required_capabilities:
    if capability == "search" and not state.is_agent_active("search"):
        state.activate_agent("search")
    elif capability == "calculation" and not state.is_agent_active("math"):
        state.activate_agent("math")
```

### 4. Error Handling and Recovery

```python
try:
    result = await supervisor.arun(task, state=state)
except AgentExecutionError as e:
    # Handle agent execution errors
    logger.error(f"Agent execution failed: {e}")
    # Implement retry logic or fallback
    result = await supervisor.arun(simplified_task, state=state)
```

## Best Practices

### 1. Agent Design

- **Specialized agents** for specific tasks
- **Clear agent descriptions** for routing
- **Robust error handling** in agent implementations
- **Appropriate tool selection** for each agent

### 2. Supervisor Configuration

- **Clear system messages** for routing logic
- **Appropriate model selection** for complexity
- **Proper state management** for multi-turn interactions
- **Resource optimization** for cost efficiency

### 3. State Management

- **Minimal state** for performance
- **Clear state transitions** for debugging
- **Proper state persistence** for long conversations
- **State validation** for correctness

### 4. Error Handling

- **Graceful degradation** when agents fail
- **Retry logic** for transient failures
- **Fallback agents** for critical functions
- **Comprehensive logging** for debugging

## Performance Considerations

### 1. Agent Activation

- **Lazy loading** - Only activate agents when needed
- **Resource pooling** - Share resources between agents
- **Caching** - Cache agent results when appropriate
- **Monitoring** - Track agent performance and usage

### 2. State Management

- **State size** - Keep state minimal for performance
- **State updates** - Batch updates when possible
- **State persistence** - Use appropriate storage
- **State cleanup** - Clean up old state regularly

### 3. Tool Management

- **Tool caching** - Cache tool results when appropriate
- **Tool optimization** - Optimize tool implementations
- **Tool monitoring** - Track tool usage and performance
- **Tool updates** - Keep tools synchronized with state

## Troubleshooting

### Common Issues

1. **Agent not found** - Check agent registration and activation
2. **Tool generation fails** - Verify agent descriptions and state
3. **Execution errors** - Check agent implementations and tool definitions
4. **Performance issues** - Monitor agent usage and state size

### Debug Tips

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check agent registry
print(state.list_agents())

# Verify tool generation
tools = state.get_all_tools()
print([tool.name for tool in tools])

# Monitor execution
supervisor.auto_sync_tools = True
```

## Contributing

When adding new examples:

1. Follow the existing structure and naming conventions
2. Include comprehensive docstrings and comments
3. Test examples thoroughly before submission
4. Update this README with new example descriptions
5. Ensure examples work with current API versions

## Related Documentation

- [Supervisor Implementation](../../src/haive/agents/supervisor/) - Main supervisor code
- [Dynamic Supervisor](../../src/haive/agents/dynamic_supervisor/) - Dynamic supervisor implementation
- [Tests](../../tests/supervisor/) - Test implementations
- [Documentation](../../docs/supervisor/) - Architecture and patterns



.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how the supervisor can: 1. Discover agents dynamically from multiple sources 2. Add specialized agents based on task requirements 3. Route tasks to appropriate specialists 4. Build a team of agents on-demand">

.. only:: html

  .. image:: /auto_examples/agents/supervisor/images/thumb/sphx_glr_dynamic_agent_discovery_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_supervisor_dynamic_agent_discovery_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating DynamicAgentDiscoverySupervisor capabilities.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how the supervisor can: 1. Discover tools dynamically from multiple sources 2. Distribute tools to appropriate agents 3. Route tasks based on available tools and agent capabilities">

.. only:: html

  .. image:: /auto_examples/agents/supervisor/images/thumb/sphx_glr_dynamic_tool_discovery_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agents_supervisor_dynamic_tool_discovery_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating DynamicToolDiscoverySupervisor capabilities.</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:
   :includehidden:


   /auto_examples/agents/supervisor/index.rst



.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
