# Agent-as-Tool Pattern - Haive Framework

**Document Version**: 1.0
**Purpose**: Documentation for the agent-as-tool pattern implementation
**Last Updated**: 2025-01-14
**Status**: Implemented

## 🎯 Overview

The agent-as-tool pattern allows any Haive agent to be converted into a LangChain tool, enabling seamless composition and integration of agents within other agents or workflows. This pattern is now available on all agents through the base Agent class.

## 🏗️ Architecture

### Class Methods on Base Agent

```python
class Agent:
    @classmethod
    def as_tool(cls, name: str | None = None, description: str | None = None, **agent_kwargs):
        """Convert this agent class to a LangChain tool."""
        ...

    @classmethod
    def create_retriever_tool(cls, vector_store, name: str | None = None, description: str | None = None, **search_kwargs):
        """Create a retriever tool from a vector store."""
        ...
```

### Key Features

1. **Universal Availability**: All agents inherit these methods from the base Agent class
2. **Class Method Design**: No instance needed to create tools
3. **Schema Awareness**: TODOs for respecting agent input/output schemas
4. **Flexible Configuration**: Pass agent configuration through `**agent_kwargs`

## 📋 Usage Examples

### Basic Agent-as-Tool

```python
from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Convert SimpleAgent to a tool
simple_tool = SimpleAgent.as_tool(
    name="research_assistant",
    description="Research and analyze topics",
    engine=AugLLMConfig(temperature=0.7)
)

# Use in another agent
coordinator = ReactAgent(
    name="coordinator",
    engine=AugLLMConfig(),
    tools=[simple_tool]  # Agent as tool!
)
```

### Creating Retriever Tools

```python
from haive.agents.rag import BaseRAGAgent

# Create a retriever tool from any agent class
knowledge_tool = BaseRAGAgent.create_retriever_tool(
    vector_store=my_vector_store,
    name="knowledge_search",
    description="Search company knowledge base",
    k=5,  # Return top 5 results
    score_threshold=0.7
)

# Use in an agent
expert = SimpleAgent(
    name="expert",
    engine=AugLLMConfig(),
    tools=[knowledge_tool]
)
```

### Complex Multi-Agent Patterns

```python
# Create specialized agent tools
planner_tool = PlannerAgent.as_tool(
    name="strategic_planner",
    description="Create strategic plans",
    engine=AugLLMConfig(temperature=0.3)
)

analyzer_tool = AnalyzerAgent.as_tool(
    name="data_analyzer",
    description="Analyze data and trends",
    engine=AugLLMConfig()
)

writer_tool = WriterAgent.as_tool(
    name="content_writer",
    description="Write professional content",
    engine=AugLLMConfig(temperature=0.8)
)

# Coordinate with a master agent
master = ReactAgent(
    name="project_manager",
    engine=AugLLMConfig(),
    tools=[planner_tool, analyzer_tool, writer_tool]
)

# Execute complex workflow
result = await master.arun(
    "Create a market analysis report for our new product launch"
)
```

## 🔧 Implementation Details

### Current Implementation

1. **Simple String I/O**: Currently uses `query: str` → `str` interface
2. **Message Format**: Wraps input as user message for compatibility
3. **Response Extraction**: Extracts content from messages or output field
4. **Tool Naming**: Defaults to `{agent_class_name}_tool`

### Future Enhancements (TODOs)

1. **Schema Respect**: Use agent's actual input/output schemas
2. **Type Safety**: Proper type hints based on agent schemas
3. **State Handling**: Include agent state in parent state schema
4. **Tool Routes**: Support tool routing and recompilation
5. **Async Support**: Add async version of agent tools

## 🎯 Use Cases

### 1. Memory-First Routing

```python
# Memory agent that routes to specialized agents
memory_agent = LongTermMemoryAgent(
    name="memory_coordinator",
    tools=[
        SemanticMemoryAgent.as_tool(),
        EpisodicMemoryAgent.as_tool(),
        ProceduralMemoryAgent.as_tool()
    ]
)
```

### 2. Dynamic Agent Composition

```python
# Dynamically add agent capabilities
base_agent = SimpleAgent(name="base", engine=AugLLMConfig())

# Add specialized capabilities as needed
if needs_research:
    base_agent.add_tool(ResearchAgent.as_tool())
if needs_coding:
    base_agent.add_tool(CodingAgent.as_tool())
```

### 3. Hierarchical Agent Systems

```python
# Build agent hierarchies
team_lead = SupervisorAgent(
    name="team_lead",
    tools=[
        DeveloperAgent.as_tool(),
        TesterAgent.as_tool(),
        DocumenterAgent.as_tool()
    ]
)

department_head = DirectorAgent(
    name="department_head",
    tools=[
        team_lead.as_tool(),  # Agents can be nested!
        AnalystTeam.as_tool(),
        DesignTeam.as_tool()
    ]
)
```

## 🔄 Tool Routes and Recompilation

When agents are added as tools, the system supports:

1. **Automatic Registration**: Tools are registered in the engine
2. **Route Configuration**: Tool routes determine execution paths
3. **Dynamic Recompilation**: Graph recompiles when tools change
4. **State Integration**: Agent states can be included in parent state

## 📊 Benefits

1. **Composability**: Any agent can become a building block
2. **Reusability**: Agents can be reused across different contexts
3. **Flexibility**: Dynamic agent composition at runtime
4. **Scalability**: Build complex systems from simple agents
5. **Maintainability**: Each agent remains focused and testable

## 🚀 Next Steps

1. **Implement Schema Respect**: Use actual agent schemas for type safety
2. **Add State Integration**: Include agent state in parent state schema
3. **Support Tool Routes**: Enable proper routing and recompilation
4. **Create Examples**: Build example multi-agent systems
5. **Performance Testing**: Benchmark agent-as-tool overhead

## 🔗 Related Documentation

- [Multi-Agent Architecture](multi_agent_meta_agent_memory_hub.md)
- [Base Agent Class](../../haive-agents/README.md)
- [Tool Integration Patterns](../standards/coding/AGENT_CONFIGURATION_GUIDE.md)

---

**Navigation**:

- [Back to Architecture](./README.md)
- [Multi-Agent Hub](multi_agent_meta_agent_memory_hub.md)
- [CLAUDE.md](../../../CLAUDE.md)
