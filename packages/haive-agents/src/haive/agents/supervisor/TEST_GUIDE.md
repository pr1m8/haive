# Dynamic Supervisor Testing Guide

This guide explains how to test the dynamic supervisor system procedurally and how it will work when agent building is fully implemented.

## 🧪 Test Setup Overview

### Current Testing Approach

Since we're testing without full LLM integration, we use **procedural testing** with:

1. **Pre-loaded Agent Registry** - Test agents with known capabilities
2. **Mock LLM Responses** - Simulated routing decisions
3. **Keyword-based Routing** - Deterministic routing for testing
4. **Manual Agent Management** - Direct agent addition/removal

### Test Files Structure

```
packages/haive-agents/src/haive/agents/supervisor/
├── test_with_registry.py      # Full integration test with mock agents
├── simple_test_runner.py      # Simplified test focusing on core flow
└── TEST_GUIDE.md             # This guide
```

## 🚀 Running the Tests

### Option 1: Full Integration Test

```bash
cd /home/will/Projects/haive/backend/haive
poetry run python packages/haive-agents/src/haive/agents/supervisor/test_with_registry.py
```

**What this tests:**

- Complete dynamic supervisor with all components
- Pre-loaded registry with 5 test agents
- DynamicChoiceModel integration
- Tool aggregation and routing
- Agent addition/removal
- Multi-agent coordination state

### Option 2: Simple Core Flow Test

```bash
cd /home/will/Projects/haive/backend/haive
poetry run python packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py
```

**What this tests:**

- Core dynamic supervisor logic
- Agent registration/unregistration
- Routing decisions
- Tool-to-agent mapping
- Simple coordination

## 📋 Test Scenarios Covered

### 1. Agent Registry Management

```python
# Test adding agents dynamically
research_agent = MockAgent(name="research_agent", tools=["web_search", "wikipedia"])
await supervisor.register_agent(research_agent, "Research and fact-finding")

# Choice model automatically updates
choice_model.option_names  # Now includes "research_agent"

# Test removing agents
await supervisor.unregister_agent("research_agent")
choice_model.option_names  # "research_agent" removed
```

### 2. Dynamic Routing

```python
# Test routing decisions
request = "Research the latest AI developments"
decision = await supervisor.route_request(request)
# Expected: routes to "research_agent" based on keywords

request = "Calculate square root of 144"
decision = await supervisor.route_request(request)
# Expected: routes to "math_agent" based on keywords
```

### 3. Tool Integration

```python
# Test tool aggregation
tool_info = supervisor._aggregate_agent_tools()
# Returns: {"tools": {...}, "tool_to_agent": {"web_search": "research_agent", ...}}

# Test tool routing
agent = supervisor.route_tool_to_agent("web_search")
# Returns: "research_agent"
```

### 4. Multi-Agent Coordination

```python
# Test coordination session
session_id = supervisor.start_coordination_session("supervisor")
coordinator_status = supervisor.get_coordination_status()
# Shows: active session, queue status, current agent

# Test execution queue
supervisor.add_to_execution_queue("research_agent", task, priority=3)
# Agent added to coordination queue
```

## 🔄 How It Works End-to-End

### Current Test Flow

```
1. Create Dynamic Supervisor
   ↓
2. Pre-load Test Agents (research, math, writing, code, analysis)
   ↓
3. Test Dynamic Routing
   - "Research AI" → research_agent
   - "Calculate sqrt(144)" → math_agent
   - "Write summary" → writing_agent
   ↓
4. Test Dynamic Management
   - Add translation_agent
   - Remove analysis_agent
   - Verify choice model updates
   ↓
5. Test Coordination
   - Start session
   - Queue multiple requests
   - Track execution state
```

### Future Agent Building Flow

```
User Request: "I need an agent for language translation"
   ↓
LLM Analysis: Determines need for translation capability
   ↓
Agent Specification Generation:
   - Name: translation_agent
   - Type: SimpleAgent
   - Tools: [language_detector, translator, localization]
   - Capability: "Language translation services"
   ↓
Agent Building:
   - Create agent instance with tools
   - Configure execution parameters
   ↓
Dynamic Registration:
   - Add to supervisor registry
   - Update choice model options
   - Aggregate tools
   - Rebuild graph
   ↓
Ready for Use:
   - "Translate this to Spanish" → routes to translation_agent
   - Tool calls work automatically
```

## 🧩 Key Components Tested

### 1. DynamicChoiceModel Integration

```python
# Before adding agent
choice_model.option_names  # ["END"]

# Add agent
await supervisor.register_agent(new_agent, capability)

# After adding agent
choice_model.option_names  # ["new_agent", "END"]

# Validation works
choice_model.validate_choice("new_agent")  # True
choice_model.validate_choice("nonexistent")  # False
```

### 2. Tool Aggregation

```python
# Each agent has tools
research_agent.tools = ["web_search", "wikipedia"]
math_agent.tools = ["calculator", "plotter"]

# Supervisor aggregates all tools
aggregated = supervisor._aggregate_agent_tools()
# Result: {
#   "tools": {"web_search": <tool>, "calculator": <tool>, ...},
#   "tool_to_agent": {"web_search": "research_agent", "calculator": "math_agent"}
# }

# Supervisor can route tool calls
supervisor.route_tool_to_agent("web_search")  # → "research_agent"
```

### 3. Graph Rebuilding

```python
# Initial graph: START → supervisor → coordinator → END

# Add agent
await supervisor.register_agent(new_agent)

# Graph rebuilt: START → supervisor → coordinator → [new_agent] → supervisor
#                                               ↓         ↑
#                                            END       adapter

# Conditional routing includes new agent
routing_destinations = ["new_agent", "existing_agent", "__end__"]
```

### 4. State Management

```python
# Enhanced state tracks everything
state = MultiAgentDynamicSupervisorState()

# Agent registry
state.agent_registry.available_agents  # {"agent_name": "agent_type"}
state.agent_registry.tool_to_agent_mapping  # {"tool": "agent"}

# Coordination
state.coordination.execution_queue  # [{"agent": "name", "task": {...}}]
state.coordination.active_executions  # {"agent": {"status": "active"}}

# Performance tracking
state.agent_execution_history  # [AgentExecutionResult(...)]
state.get_agent_performance("agent_name")  # {"executions": 5, "success_rate": 0.8}
```

## 🔍 Test Verification Points

### ✅ What to Check

1. **Agent Registration**
   - Agent appears in registry
   - Choice model options updated
   - Tools aggregated correctly
   - Graph rebuilt successfully

2. **Routing Decisions**
   - Correct agent selected for request type
   - Reasoning makes sense
   - Confidence scores reasonable
   - Fallback to END when appropriate

3. **Tool Integration**
   - Tools from all agents available
   - Tool-to-agent mapping correct
   - Supervisor engine has aggregated tools
   - Tool calls route to correct agent

4. **Dynamic Updates**
   - Adding agent updates all systems
   - Removing agent cleans up references
   - Choice model stays synchronized
   - Graph structure adapts

5. **Coordination**
   - Sessions start/stop correctly
   - Execution queue manages priorities
   - State tracks active agents
   - Handoffs work between agents

### ❌ Common Issues to Watch

1. **Graph Rebuild Failures**
   - Check if `auto_rebuild_graph=True`
   - Verify agent nodes added correctly
   - Ensure routing destinations updated

2. **Choice Model Sync Issues**
   - Verify `choice_model.option_names` includes all agents
   - Check for duplicate options
   - Ensure removed agents are cleaned up

3. **Tool Aggregation Problems**
   - Check agent tools are detected
   - Verify tool-to-agent mapping
   - Ensure supervisor engine gets tools

4. **State Consistency**
   - Registry state matches actual agents
   - Coordination state tracks correctly
   - Performance metrics update

## 🚀 Future Integration Points

### When Agent Building is Implemented

1. **LLM-Driven Agent Creation**

   ```python
   # User: "I need an agent for image processing"
   # LLM analyzes and generates:
   agent_spec = {
       "name": "image_agent",
       "type": "ReactAgent",
       "tools": ["resize", "filter", "convert"],
       "capability": "Image processing and editing"
   }
   ```

2. **Tool Generation**

   ```python
   # LLM determines needed tools and generates them
   tools = [
       ImageResizerTool(),
       FilterApplierTool(),
       FormatConverterTool()
   ]
   ```

3. **Automatic Registration**

   ```python
   # Built agent automatically registered
   built_agent = AgentBuilder.create(agent_spec, tools)
   await supervisor.register_agent(built_agent, agent_spec["capability"])
   ```

4. **Seamless Integration**
   - New agent immediately available for routing
   - Tools work in supervisor context
   - Choice model includes new option
   - Graph adapts to new capability

### Testing the Full Flow

When LLM integration is complete, the test flow becomes:

```python
# User request
user_input = "I need help with image processing tasks"

# Supervisor analyzes and decides to build new agent
decision = await supervisor.analyze_request(user_input)
if decision.needs_new_agent:
    # Build agent dynamically
    agent_spec = await supervisor.generate_agent_spec(user_input)
    new_agent = await supervisor.build_agent(agent_spec)
    await supervisor.register_agent(new_agent)

# Use the new agent
result = await supervisor.route_request("Resize this image to 800x600")
# Routes to newly built image_agent
```

## 🎯 Current Test Results

When you run the tests, you should see:

1. **Agent Registration**: All test agents load successfully
2. **Choice Model**: Options include all registered agents + "END"
3. **Routing**: Requests route to appropriate agents based on keywords
4. **Tool Mapping**: All agent tools aggregated and mapped correctly
5. **Dynamic Changes**: Adding/removing agents updates all systems
6. **Coordination**: Multi-agent sessions track state properly

The tests demonstrate that the **dynamic supervisor framework is ready** for LLM-driven agent building integration!
