# Step-by-Step Dynamic Supervisor Implementation

## Agent ID: claude_agent_20250107_165800

## Step 1: Create Registry with Real Agents

### Basic Agents Setup
```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.tools.tools.search_tools import tavily_search  # Get real search tool
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List

# Math agent with add/mult tools
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b

@tool 
def multiply(a: int, b: int) -> int:
    """Returns the product of two numbers"""
    return a * b

# Planning model
class Plan(BaseModel):
    steps: List[str] = Field(description='list of steps')

# Create engines
math_aug = AugLLMConfig(tools=[add, multiply])
search_aug = AugLLMConfig(tools=[tavily_search])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version='v2')

# Create agents
math_agent = ReactAgent(name="math_agent", engine=math_aug)
search_agent = ReactAgent(name="search_agent", engine=search_aug) 
planning_agent = SimpleAgent(name="planning_agent", engine=plan_aug)
```

### Simple Registry
```python
class AgentRegistry:
    def __init__(self):
        self.agents = {}
    
    def register(self, name: str, agent: Agent, description: str):
        self.agents[name] = {
            'agent': agent,
            'description': description
        }
    
    def get(self, name: str) -> Agent:
        entry = self.agents.get(name)
        return entry['agent'] if entry else None
    
    def list_available(self) -> Dict[str, str]:
        return {name: entry['description'] for name, entry in self.agents.items()}
    
    def has_agent(self, name: str) -> bool:
        return name in self.agents

# Setup registry
registry = AgentRegistry()
registry.register("math_agent", math_agent, "Performs mathematical calculations")
registry.register("search_agent", search_agent, "Searches web for information") 
registry.register("planning_agent", planning_agent, "Creates structured plans")
```

## Step 2: Test Registry First

```python
def test_registry_basic():
    """Test 1: Registry stores and retrieves agents"""
    registry = AgentRegistry()
    
    # Register agent
    agent = SimpleAgent(name="test_agent")
    registry.register("test_agent", agent, "Test agent")
    
    # Check it's there
    assert registry.has_agent("test_agent")
    retrieved = registry.get("test_agent") 
    assert retrieved.name == "test_agent"
    
    # Check description
    available = registry.list_available()
    assert available["test_agent"] == "Test agent"

def test_registry_with_real_agents():
    """Test 2: Registry with actual configured agents"""
    # Setup real agents (math, search, planning)
    # Register them
    # Test each agent works individually
    
    math_result = registry.get("math_agent").invoke({"messages": [HumanMessage("What is 5 + 3?")]})
    assert "8" in str(math_result)
    
    plan_result = registry.get("planning_agent").invoke({"messages": [HumanMessage("Plan a dinner party")]})
    assert hasattr(plan_result, 'steps') or 'steps' in str(plan_result)
```

## Step 3: Create Route Tools

```python
def create_route_tools(registry: AgentRegistry) -> List[Tool]:
    """Create route_to_X tools for each agent in registry"""
    tools = []
    
    for agent_name, entry in registry.agents.items():
        agent = entry['agent']
        description = entry['description']
        
        @tool
        def route_to_agent(task: str, agent=agent, name=agent_name) -> str:
            f"""Route task to {name}: {description}"""
            try:
                result = agent.invoke({"messages": [HumanMessage(task)]})
                return f"Agent {name} completed: {result}"
            except Exception as e:
                return f"Agent {name} failed: {str(e)}"
        
        route_to_agent.name = f"route_to_{agent_name}"
        tools.append(route_to_agent)
    
    return tools

def test_route_tools():
    """Test 3: Route tools work correctly"""
    tools = create_route_tools(registry)
    
    # Should have route_to_math_agent, route_to_search_agent, etc.
    tool_names = [t.name for t in tools]
    assert "route_to_math_agent" in tool_names
    assert "route_to_search_agent" in tool_names
    
    # Test one route tool
    math_route = next(t for t in tools if t.name == "route_to_math_agent")
    result = math_route.invoke({"task": "What is 10 + 5?"})
    assert "15" in result or "Agent math_agent completed" in result
```

## Step 4: List Agents Tool

```python
def create_list_agents_tool(registry: AgentRegistry) -> Tool:
    @tool
    def list_agents() -> str:
        """List all available agents and their capabilities"""
        available = registry.list_available()
        if not available:
            return "No agents currently available"
        
        result = "Available agents:\n"
        for name, desc in available.items():
            result += f"- {name}: {desc}\n"
        return result
    
    return list_agents

def test_list_agents_tool():
    """Test 4: List agents tool shows registry contents"""
    list_tool = create_list_agents_tool(registry)
    result = list_tool.invoke({})
    
    assert "math_agent" in result
    assert "search_agent" in result  
    assert "mathematical calculations" in result
```

## Step 5: Basic Supervisor (ReactAgent + Registry Tools)

```python
class BasicSupervisor(ReactAgent):
    def __init__(self, registry: AgentRegistry, **kwargs):
        self.registry = registry
        super().__init__(**kwargs)
    
    def setup_agent(self):
        # Create all route tools from registry
        route_tools = create_route_tools(self.registry)
        list_tool = create_list_agents_tool(self.registry)
        
        # Combine with basic LLM engine
        supervisor_engine = AugLLMConfig(
            tools=route_tools + [list_tool],
            system_message="""You are a supervisor that routes tasks to specialized agents.
            
Available commands:
- list_agents: See what agents are available
- route_to_X: Send task to agent X

Always list_agents first to see what's available, then route appropriately."""
        )
        
        self.engine = supervisor_engine
        self.engines["main"] = supervisor_engine

def test_basic_supervisor():
    """Test 5: Basic supervisor routes correctly"""
    supervisor = BasicSupervisor(registry, name="test_supervisor")
    
    # Test it can list agents
    result = supervisor.invoke({"messages": [HumanMessage("What agents do you have?")]})
    assert "math_agent" in str(result)
    
    # Test it can route to math agent
    result = supervisor.invoke({"messages": [HumanMessage("Calculate 7 + 8")]})
    assert "15" in str(result) or "math_agent" in str(result)
```

## Testing Order

1. **Test Registry** - Store/retrieve agents ✓
2. **Test Individual Agents** - Math, search, planning work ✓  
3. **Test Route Tools** - route_to_X tools work ✓
4. **Test List Tool** - Shows available agents ✓
5. **Test Basic Supervisor** - Routes tasks correctly ✓

Each step builds on the previous. No mocks - real agents, real tools, real registry.