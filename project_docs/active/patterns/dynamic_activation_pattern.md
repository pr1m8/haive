# Dynamic Activation Pattern with MetaStateSchema

**Version**: 1.1  
**Purpose**: Generalized pattern for dynamic component activation using MetaStateSchema  
**Last Updated**: 2025-01-15  
**Location**: `/project_docs/active/patterns/dynamic_activation_pattern.md`

## 🎯 Overview

This document outlines a reusable pattern for dynamic component activation (agents, tools, services) using MetaStateSchema as the foundation. The pattern enables runtime discovery, loading, and activation of components with full type safety and recompilation support.

## 📋 Core Architecture

### 1. Generic Registry System

```python
from typing import TypeVar, Generic, Dict, Set, Optional, Type
from pydantic import BaseModel, Field, field_validator
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

T = TypeVar('T')  # Generic type for registry items

class RegistryItem(BaseModel, Generic[T]):
    """Base class for registry items with activation state."""
    id: str
    name: str
    description: str
    component: T
    is_active: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    activation_count: int = 0
    last_activated: Optional[datetime] = None

class DynamicRegistry(BaseModel, Generic[T]):
    """Generic registry for managing activatable components."""
    items: Dict[str, RegistryItem[T]] = Field(default_factory=dict)
    active_items: Set[str] = Field(default_factory=set)
    max_active: Optional[int] = None

    def register(self, item: RegistryItem[T]) -> None:
        """Register a new component."""
        self.items[item.id] = item

    def activate(self, item_id: str) -> bool:
        """Activate a component by ID."""
        if item_id in self.items:
            if self.max_active and len(self.active_items) >= self.max_active:
                return False
            self.items[item_id].is_active = True
            self.items[item_id].activation_count += 1
            self.items[item_id].last_activated = datetime.now()
            self.active_items.add(item_id)
            return True
        return False
```

### 2. Dynamic Activation State with MetaStateSchema

```python
from haive.core.schema import StateSchema
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

class DynamicActivationState(StateSchema):
    """State for dynamic activation patterns."""

    # Registry for components (tools, agents, etc.)
    registry: DynamicRegistry = Field(
        default_factory=DynamicRegistry,
        description="Registry of available components"
    )

    # Meta states for active components
    active_meta_states: Dict[str, MetaStateSchema] = Field(
        default_factory=dict,
        description="MetaStateSchema instances for active components"
    )

    # Discovery configuration
    discovery_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for component discovery"
    )

    # Activation history
    activation_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of activation/deactivation events"
    )

    def activate_component(self, component_id: str) -> Optional[MetaStateSchema]:
        """Activate a component and wrap in MetaStateSchema."""
        if self.registry.activate(component_id):
            item = self.registry.items[component_id]
            # Wrap component in MetaStateSchema for meta capabilities
            meta_state = MetaStateSchema.from_agent(
                agent=item.component,
                initial_state={"activated_at": datetime.now()},
                graph_context={
                    "registry_id": component_id,
                    "activation_reason": "dynamic_activation"
                }
            )
            self.active_meta_states[component_id] = meta_state

            # Track activation
            self.activation_history.append({
                "timestamp": datetime.now(),
                "action": "activate",
                "component_id": component_id,
                "component_name": item.name
            })

            return meta_state
        return None
```

### 3. Discovery Agent Pattern

```python
from haive.agents.rag.base import BaseRAGAgent
from haive.core.engine.retriever import BaseRetrieverConfig
from pydantic import ConfigDict

class ComponentDiscoveryAgent(BaseModel):
    """RAG-based agent for discovering components from documentation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    document_path: str
    discovery_agent: BaseRAGAgent = Field(default=None)
    meta_state: MetaStateSchema = Field(default=None)

    @model_validator(mode="after")
    def setup_discovery_agent(self) -> "ComponentDiscoveryAgent":
        """Initialize the discovery agent after model creation."""
        if self.discovery_agent is None:
            # Create retriever for component documentation
            retriever_config = BaseRetrieverConfig(
                name="component_retriever",
                documents=self._load_documents(self.document_path)
            )

            # Create RAG agent with retriever
            self.discovery_agent = BaseRAGAgent(
                name="component_discovery",
                engine=retriever_config
            )

            # Wrap in MetaStateSchema for tracking
            self.meta_state = MetaStateSchema.from_agent(
                agent=self.discovery_agent,
                initial_state={"discovery_mode": "components"},
                graph_context={"purpose": "component_discovery"}
            )

        return self

    async def discover_components(self, query: str) -> List[Dict[str, Any]]:
        """Discover components based on query."""
        result = await self.meta_state.execute_agent(
            input_data=f"Find components that can: {query}",
            update_state=True
        )

        # Parse discovered components from result
        return self._parse_components(result["output"])

    def _load_documents(self, path: str) -> List[str]:
        """Load documents from path."""
        # Implementation to load documents
        return []

    def _parse_components(self, output: Any) -> List[Dict[str, Any]]:
        """Parse component data from discovery output."""
        # Implementation to parse components
        return []
```

### 4. Dynamic Supervisor Pattern

```python
from haive.agents.base import Agent
from haive.core.graph import BaseGraph
from langgraph.prebuilt import ToolNode
from pydantic import PrivateAttr

class DynamicActivationSupervisor(Agent[DynamicActivationState]):
    """Supervisor that can dynamically activate components."""

    # Use private attribute for discovery agent
    _discovery_agent: ComponentDiscoveryAgent = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Setup the supervisor agent."""
        super().setup_agent()

        # Initialize discovery agent if provided
        if hasattr(self, 'discovery_agent_config'):
            self._discovery_agent = ComponentDiscoveryAgent(
                document_path=self.discovery_agent_config['document_path']
            )

    @classmethod
    def create_with_discovery(
        cls,
        name: str,
        document_path: str,
        **kwargs
    ) -> "DynamicActivationSupervisor":
        """Factory method to create supervisor with discovery agent."""
        supervisor = cls(name=name, **kwargs)
        supervisor.discovery_agent_config = {'document_path': document_path}
        return supervisor

    def build_graph(self) -> BaseGraph:
        """Build graph with dynamic activation capabilities."""
        graph = BaseGraph()

        # Main supervisor node
        graph.add_node("supervisor", self._supervisor_node)

        # Discovery node
        graph.add_node("discovery", self._discovery_node)

        # Activation node
        graph.add_node("activation", self._activation_node)

        # Execution node for active components
        graph.add_node("execution", self._execution_node)

        # Conditional edges
        graph.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {
                "discover": "discovery",
                "activate": "activation",
                "execute": "execution",
                "end": END
            }
        )

        # Set entry point
        graph.set_entry_point("supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: DynamicActivationState) -> Dict[str, Any]:
        """Main supervisor logic."""
        # Check if we need to discover new components
        if self._needs_discovery(state):
            return {"next": "discover"}

        # Check if we need to activate components
        if self._needs_activation(state):
            return {"next": "activate"}

        # Execute with active components
        return {"next": "execute"}

    async def _discovery_node(self, state: DynamicActivationState) -> Dict[str, Any]:
        """Discover new components using RAG."""
        query = state.discovery_config.get("query", "")

        # Use discovery agent
        components = await self._discovery_agent.discover_components(query)

        # Register discovered components
        for comp_data in components:
            component = await self._load_component(comp_data)
            if component:
                item = RegistryItem(
                    id=comp_data["id"],
                    name=comp_data["name"],
                    description=comp_data["description"],
                    component=component
                )
                state.registry.register(item)

        return {"discovered_count": len(components)}
```

### Dynamic Tool Loading for ReactAgent

```python
from haive.agents.react import ReactAgent
from langchain_core.tools import Tool

class DynamicToolState(DynamicActivationState):
    """Specialized state for dynamic tool management."""

    # Tool-specific fields
    tool_categories: Dict[str, List[str]] = Field(default_factory=dict)
    tool_usage_stats: Dict[str, int] = Field(default_factory=dict)

    def get_active_tools(self) -> List[Tool]:
        """Get all active tools as LangChain tools."""
        tools = []
        for item_id in self.registry.active_items:
            item = self.registry.items[item_id]
            if isinstance(item.component, Tool):
                tools.append(item.component)
        return tools

class DynamicReactAgent(ReactAgent):
    """ReactAgent with dynamic tool loading capabilities."""

    # Private attributes for internal state
    _discovery_agent: ComponentDiscoveryAgent = PrivateAttr(default=None)
    _meta_self: MetaStateSchema = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Setup the dynamic React agent."""
        # Set state schema before parent setup
        self.state_schema = DynamicToolState
        super().setup_agent()

        # Initialize discovery agent if config provided
        if hasattr(self, 'discovery_config'):
            self._discovery_agent = ComponentDiscoveryAgent(
                document_path=self.discovery_config['document_path']
            )

        # Wrap self in MetaStateSchema for recompilation
        self._meta_self = MetaStateSchema.from_agent(
            agent=self,
            initial_state={"dynamic_tools": True},
            graph_context={"recompilation_enabled": True}
        )

    @classmethod
    def create_with_discovery(
        cls,
        name: str,
        document_path: str,
        **kwargs
    ) -> "DynamicReactAgent":
        """Factory method to create agent with discovery."""
        agent = cls(name=name, **kwargs)
        agent.discovery_config = {'document_path': document_path}
        return agent

    async def discover_and_load_tools(self, task: str) -> List[Tool]:
        """Discover and load tools for a specific task."""
        # Discover tools using RAG
        tool_docs = await self._discovery_agent.discover_components(
            f"tools needed for: {task}"
        )

        loaded_tools = []
        for doc in tool_docs:
            # Load tool from document (using @notebooks/tool_loader.ipynb pattern)
            tool = await self._load_tool_from_document(doc)
            if tool:
                # Register in state
                item = RegistryItem(
                    id=doc["id"],
                    name=doc["name"],
                    description=doc["description"],
                    component=tool
                )
                self.state.registry.register(item)

                # Activate tool
                self.state.activate_component(doc["id"])
                loaded_tools.append(tool)

        # Mark for recompilation to include new tools
        if loaded_tools:
            self._meta_self.mark_for_recompile(
                f"Added {len(loaded_tools)} new tools"
            )

            # Trigger recompilation
            await self._recompile_with_new_tools(loaded_tools)

        return loaded_tools
```

## 🌐 MCP Implementation Pattern

### MCP Version for haive-mcp

```python
# @haive-mcp/src/haive/mcp/dynamic_activation.py

from haive.mcp.base import MCPServer, MCPTool
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from pydantic import Field, model_validator

class DynamicMCPRegistry(DynamicRegistry[MCPTool]):
    """MCP-specific registry for dynamic tool activation."""

    async def activate_mcp_tool(self, tool_id: str) -> Optional[MCPTool]:
        """Activate an MCP tool and register with server."""
        if self.activate(tool_id):
            tool = self.items[tool_id].component
            # Register with MCP server
            await self._register_with_mcp(tool)
            return tool
        return None

class DynamicActivationMCPServer(MCPServer):
    """MCP server with dynamic tool activation."""

    # Configuration fields
    discovery_source: str
    tool_registry: DynamicMCPRegistry = Field(default_factory=DynamicMCPRegistry)
    discovery_config: Dict[str, Any] = Field(default_factory=dict)
    meta_state: MetaStateSchema = Field(default=None)

    @model_validator(mode="after")
    def setup_mcp_server(self) -> "DynamicActivationMCPServer":
        """Initialize MCP server components."""
        # Set up discovery configuration
        self.discovery_config = {
            "source": self.discovery_source,
            "auto_discover": True
        }

        # Wrap in MetaStateSchema for tracking
        self.meta_state = MetaStateSchema(
            agent=self,  # MCP server as "agent"
            agent_state={"mcp_mode": True},
            graph_context={"protocol": "mcp"}
        )

        return self

    async def handle_tool_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle dynamic tool requests from MCP clients."""
        tool_name = request.get("tool")

        # Check if tool is active
        if tool_name not in self.tool_registry.active_items:
            # Try to discover and activate
            discovered = await self._discover_tool(tool_name)
            if discovered:
                await self.tool_registry.activate_mcp_tool(discovered["id"])

        # Execute through meta state for tracking
        result = await self.meta_state.execute_agent(
            input_data=request,
            update_state=True
        )

        return result["output"]
```

## 🎯 Usage Examples

### Example 1: Dynamic Tool Loading

```python
# Create dynamic React agent with discovery
agent = DynamicReactAgent.create_with_discovery(
    name="dynamic_react",
    document_path="@haive-tools/docs",
    engine=AugLLMConfig()
)

# Task that needs specific tools
task = "Calculate compound interest and create a visualization"

# Agent discovers and loads needed tools
tools = await agent.discover_and_load_tools(task)
print(f"Loaded tools: {[t.name for t in tools]}")
# Output: ["calculator", "compound_interest", "chart_creator"]

# Execute task with dynamically loaded tools
result = await agent.arun(task)
```

### Example 2: Dynamic Agent Activation

```python
# Create supervisor with discovery using factory method
supervisor = DynamicActivationSupervisor.create_with_discovery(
    name="dynamic_supervisor",
    document_path="@haive-agents/docs",
    engine=AugLLMConfig()
)

# Configure discovery
supervisor.state.discovery_config = {
    "query": "agents for data analysis",
    "max_active": 3
}

# Run supervisor - it will discover and activate agents as needed
result = await supervisor.arun("Analyze this dataset and create a report")
```

### Example 3: MCP Dynamic Tools

```python
# Create MCP server with dynamic activation
mcp_server = DynamicActivationMCPServer(
    discovery_source="@haive-tools/mcp"
)

# Start server
await mcp_server.start()

# Client requests will trigger dynamic tool discovery/activation
# Tools are wrapped in MetaStateSchema for tracking
```

## 🔗 Integration Points

### With Existing Systems

1. **@project_docs/active/architecture/meta_state_pattern.md** - Uses MetaStateSchema for all component wrapping
2. **@packages/haive-agents/examples/supervisor/advanced/dynamic_activation_example.py** - Extends this pattern
3. **@notebooks/tool_loader.ipynb** - Tool loading implementation
4. **@project_docs/active/architecture/generalized_recompilation_system.md** - Recompilation integration
5. **@project_docs/active/standards/coding/PYDANTIC_PATTERNS.md** - Proper Pydantic usage

### Key Benefits

- **Type Safety**: Generic registries ensure type safety
- **Reusability**: Pattern works for tools, agents, or any component
- **Meta Tracking**: All components wrapped in MetaStateSchema
- **Dynamic Discovery**: RAG-based discovery from documentation
- **Recompilation**: Automatic graph updates when components change
- **MCP Compatible**: Same pattern works for MCP protocol
- **No **init\*\*\*\*: Follows Pydantic best practices

## 📊 State Management

### Registry State Structure

```python
{
    "registry": {
        "items": {
            "tool_123": {
                "id": "tool_123",
                "name": "calculator",
                "description": "Basic math operations",
                "component": <Tool instance>,
                "is_active": true,
                "activation_count": 5,
                "last_activated": "2025-01-15T10:30:00"
            }
        },
        "active_items": {"tool_123", "tool_456"},
        "max_active": 10
    },
    "active_meta_states": {
        "tool_123": <MetaStateSchema instance>
    },
    "activation_history": [
        {
            "timestamp": "2025-01-15T10:30:00",
            "action": "activate",
            "component_id": "tool_123",
            "component_name": "calculator"
        }
    ]
}
```

## 🚀 Implementation Checklist

- [ ] Implement `DynamicRegistry[T]` generic class (no **init**)
- [ ] Create `DynamicActivationState` with proper validators
- [ ] Build `ComponentDiscoveryAgent` using model_validator
- [ ] Implement `DynamicActivationSupervisor` with factory methods
- [ ] Create `DynamicReactAgent` with private attributes
- [ ] Build MCP version with proper Pydantic patterns
- [ ] Add tests with real components (no mocks)
- [ ] Create examples following Pydantic best practices

---

**Remember**:

- Never use `__init__` with Pydantic models
- Use `model_validator(mode="after")` for post-initialization
- Use factory methods (`create_with_*`) for complex initialization
- Use `PrivateAttr` for internal state that shouldn't be serialized
- Follow **@project_docs/active/standards/coding/PYDANTIC_PATTERNS.md**
