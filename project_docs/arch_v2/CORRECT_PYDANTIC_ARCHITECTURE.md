# Correct Pydantic-Based Architecture - End-to-End Flow

**Created**: 2025-01-07  
**Purpose**: Redesign Haive with proper Pydantic patterns - NO **init** overrides  
**Status**: Complete correct design

## 🚨 **CRITICAL: Pydantic Design Rules**

### **NEVER DO THIS**

```python
# ❌ WRONG - Breaks Pydantic completely
class Agent(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # DESTROYS VALIDATION
        self.setup()  # WRONG PATTERN
```

### **ALWAYS DO THIS**

```python
# ✅ CORRECT - Pydantic patterns
class Agent(BaseModel):
    # Fields with defaults or factories
    name: str = Field(...)
    engine: Engine = Field(default_factory=lambda: Engine())

    # Use validators for computed fields
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.lower().strip()

    # Use model_post_init for setup
    def model_post_init(self, __context):
        """Called after Pydantic initialization"""
        super().model_post_init(__context)
        # Setup logic here
```

## 🏗️ **Correct State Architecture**

### **Modular State with Pydantic**

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import uuid4

# Base State Module - Pure Pydantic
class CoreState(BaseModel):
    """Core state fields - immutable structure, mutable values"""

    model_config = ConfigDict(
        # Allow field mutation but validate
        validate_assignment=True,
        # Use defaults for missing fields
        use_enum_values=True,
        # Better serialization
        arbitrary_types_allowed=True
    )

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    version: int = Field(default=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Message State Module
class MessageState(BaseModel):
    """Message handling state"""

    model_config = ConfigDict(validate_assignment=True)

    messages: List[Message] = Field(default_factory=list)
    max_messages: int = Field(default=100, ge=1, le=10000)

    @field_validator('messages')
    @classmethod
    def limit_messages(cls, v, info):
        """Keep only recent messages"""
        if len(v) > info.data.get('max_messages', 100):
            return v[-info.data['max_messages']:]
        return v

# Engine State Module
class EngineState(BaseModel):
    """Engine management state"""

    model_config = ConfigDict(validate_assignment=True)

    engines: Dict[str, Any] = Field(default_factory=dict)
    primary_engine: Optional[str] = Field(default=None)

    @model_validator(mode='after')
    def validate_primary(self):
        """Ensure primary engine exists"""
        if self.primary_engine and self.primary_engine not in self.engines:
            raise ValueError(f"Primary engine {self.primary_engine} not in engines")
        return self

# Unified State - Composition
class UnifiedState(CoreState, MessageState, EngineState):
    """Complete state through composition"""

    # Additional unified fields
    tools: List[Any] = Field(default_factory=list)
    nodes: Dict[str, Any] = Field(default_factory=dict)
    edges: List[tuple] = Field(default_factory=list)

    def model_post_init(self, __context):
        """Post-init setup"""
        super().model_post_init(__context)
        # Any setup that needs all fields initialized
        if not self.primary_engine and self.engines:
            self.primary_engine = next(iter(self.engines.keys()))
```

## 🎭 **Correct Mixin Pattern with Pydantic**

```python
# Mixins that work with Pydantic
class StatefulMixin(BaseModel):
    """State management mixin"""

    state: UnifiedState = Field(default_factory=UnifiedState)
    state_history: List[Dict] = Field(default_factory=list, exclude=True)

    def save_state_snapshot(self) -> None:
        """Save current state"""
        snapshot = self.state.model_dump()
        self.state_history.append(snapshot)

    def restore_state(self, index: int = -1) -> None:
        """Restore from history"""
        if self.state_history:
            snapshot = self.state_history[index]
            self.state = UnifiedState.model_validate(snapshot)

class ExecutableMixin(BaseModel):
    """Execution capability mixin"""

    execution_count: int = Field(default=0, exclude=True)
    last_execution: Optional[datetime] = Field(default=None, exclude=True)

    async def execute(self, input_data: Any) -> Any:
        """Main execution method"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        return await self._execute_core(input_data)

    async def _execute_core(self, input_data: Any) -> Any:
        """Override in subclasses"""
        raise NotImplementedError

class ObservableMixin(BaseModel):
    """Observability mixin"""

    observers: List[Any] = Field(default_factory=list, exclude=True)
    hooks: Dict[str, List[Any]] = Field(default_factory=dict, exclude=True)
    debug: bool = Field(default=False)

    async def notify(self, event: str, data: Any) -> None:
        """Notify observers and run hooks"""
        if self.debug:
            print(f"Event: {event}, Data: {data}")

        for observer in self.observers:
            await observer.update(event, data)

        for hook in self.hooks.get(event, []):
            await hook(data)
```

## 🎯 **Correct Agent Hierarchy**

```python
# Correct Workflow - Pure Pydantic
class Workflow(StatefulMixin, ExecutableMixin, ObservableMixin):
    """Base workflow with proper Pydantic patterns"""

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    name: str = Field(..., min_length=1, max_length=100)
    utility_engines: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('name')
    @classmethod
    def clean_name(cls, v):
        """Clean and validate name"""
        return v.strip().replace(' ', '_').lower()

    def model_post_init(self, __context):
        """Post-init setup"""
        super().model_post_init(__context)
        # Setup after all fields initialized
        self.state.metadata['workflow_name'] = self.name

    async def _execute_core(self, input_data: Any) -> Any:
        """Workflow execution"""
        result = input_data
        for engine_name, engine in self.utility_engines.items():
            result = await engine.process(result)
            await self.notify('engine_executed', {'engine': engine_name})
        return result

# Correct Agent - Adds Intelligence
class Agent(Workflow):
    """Agent with LLM - proper Pydantic inheritance"""

    # Required intelligence engine
    intelligence_engine: Any = Field(...)

    # Optional tools
    tools: List[Any] = Field(default_factory=list)

    @field_validator('intelligence_engine')
    @classmethod
    def validate_engine(cls, v):
        """Ensure engine is valid"""
        if not hasattr(v, 'process'):
            raise ValueError("Engine must have process method")
        return v

    def model_post_init(self, __context):
        """Agent-specific setup"""
        super().model_post_init(__context)
        # Register tools in state
        self.state.tools.extend(self.tools)
        # Set primary engine
        self.state.engines['intelligence'] = self.intelligence_engine
        self.state.primary_engine = 'intelligence'

    async def _execute_core(self, input_data: Any) -> Any:
        """Agent execution with intelligence"""
        # Run workflow processing first
        processed = await super()._execute_core(input_data)

        # Add intelligence
        result = await self.intelligence_engine.process(processed)

        # Update state
        self.state.messages.append(
            Message(role='assistant', content=str(result))
        )

        return result

# Correct MultiAgent - Coordinates Agents
class MultiAgent(Agent):
    """Multi-agent coordinator - proper Pydantic patterns"""

    agents: Dict[str, Agent] = Field(default_factory=dict)
    coordination_engine: Any = Field(...)

    @field_validator('agents')
    @classmethod
    def validate_agents(cls, v):
        """Ensure all agents are valid"""
        if not v:
            raise ValueError("MultiAgent needs at least one agent")
        for name, agent in v.items():
            if not isinstance(agent, Agent):
                raise ValueError(f"Agent {name} must be an Agent instance")
        return v

    def model_post_init(self, __context):
        """Multi-agent setup"""
        super().model_post_init(__context)
        # Register all sub-agents
        for name, agent in self.agents.items():
            self.state.metadata[f'agent_{name}'] = agent.name

    async def _execute_core(self, input_data: Any) -> Any:
        """Coordinate multiple agents"""
        # Use coordination engine to plan
        plan = await self.coordination_engine.create_plan(
            input_data,
            available_agents=list(self.agents.keys())
        )

        # Execute plan
        results = {}
        for step in plan.steps:
            agent = self.agents[step.agent_name]
            result = await agent.execute(step.input_data)
            results[step.agent_name] = result

        # Aggregate results
        return await self.coordination_engine.aggregate(results)
```

## 🔄 **Correct Recompilation Pattern**

```python
class SmartRecompiler(BaseModel):
    """Recompilation with proper Pydantic"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cache: Dict[str, Any] = Field(default_factory=dict, exclude=True)
    compile_times: List[float] = Field(default_factory=list, exclude=True)

    async def recompile(self, state: UnifiedState, change_type: str) -> None:
        """Smart recompilation based on change"""

        if change_type in ['message', 'metadata']:
            # No recompilation needed
            return

        if change_type in ['engine_swap', 'tool_add']:
            # Soft recompile (<100ms)
            await self._soft_recompile(state)
        else:
            # Hard recompile
            await self._hard_recompile(state)

    async def _soft_recompile(self, state: UnifiedState) -> None:
        """Fast targeted update"""
        start = time.time()

        # Get cached graph
        graph = self.cache.get(state.id)
        if graph:
            # Update only changed parts
            graph.update_from_state(state)
        else:
            # First compile
            graph = await self._build_graph(state)

        self.cache[state.id] = graph
        self.compile_times.append(time.time() - start)

    async def _hard_recompile(self, state: UnifiedState) -> None:
        """Full rebuild"""
        start = time.time()

        # Clear cache and rebuild
        self.cache.pop(state.id, None)
        graph = await self._build_graph(state)
        self.cache[state.id] = graph

        self.compile_times.append(time.time() - start)
```

## 🌊 **Complete End-to-End Flow (Correct Pydantic)**

```python
# 1. REQUEST ENTRY - Pure Pydantic models
class Request(BaseModel):
    """Incoming request model"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

# 2. STATE INITIALIZATION - No __init__ override
class StateInitializer(BaseModel):
    """Initialize state from request"""

    @staticmethod
    def from_request(request: Request) -> UnifiedState:
        """Create state from request"""
        return UnifiedState(
            messages=[Message(role='user', content=request.content)],
            metadata={'request_id': request.id}
        )

# 3. WORKFLOW EXECUTION - Proper Pydantic workflow
class ResearchWorkflow(Workflow):
    """Research workflow with correct patterns"""

    name: str = Field(default="research_workflow")

    # Utility engines via default factory
    utility_engines: Dict[str, Any] = Field(
        default_factory=lambda: {
            'router': RouterEngine(),
            'validator': ValidatorEngine(),
            'formatter': FormatterEngine()
        }
    )

    async def _execute_core(self, input_data: UnifiedState) -> UnifiedState:
        """Process through utilities"""
        # Route
        input_data = await self.utility_engines['router'].process(input_data)
        # Validate
        input_data = await self.utility_engines['validator'].process(input_data)
        # Format
        input_data = await self.utility_engines['formatter'].process(input_data)

        return input_data

# 4. AGENT INTELLIGENCE - No __init__, use factories
class ResearchAgent(Agent):
    """Research agent with proper initialization"""

    name: str = Field(default="research_agent")

    # Engine via factory
    intelligence_engine: Any = Field(
        default_factory=lambda: LLMEngine(model="gpt-4")
    )

    # Tools via factory
    tools: List[Any] = Field(
        default_factory=lambda: [
            WebSearchTool(),
            DocumentAnalyzer()
        ]
    )

    # Recompiler as a field
    recompiler: SmartRecompiler = Field(
        default_factory=SmartRecompiler,
        exclude=True
    )

    async def add_capability(self, capability: Any) -> None:
        """Add capability dynamically"""
        if hasattr(capability, '__call__'):
            self.tools.append(capability)
            self.state.tools.append(capability)
            # Trigger soft recompile
            await self.recompiler.recompile(self.state, 'tool_add')

# 5. MULTI-AGENT COORDINATION - Composition pattern
class ResearchTeam(MultiAgent):
    """Research team with proper Pydantic patterns"""

    name: str = Field(default="research_team")

    # Coordination engine factory
    coordination_engine: Any = Field(
        default_factory=lambda: CoordinationEngine(model="gpt-4")
    )

    # Agents via factory
    agents: Dict[str, Agent] = Field(
        default_factory=lambda: {
            'researcher': ResearchAgent(),
            'analyst': AnalysisAgent(),
            'writer': WritingAgent()
        }
    )

    def model_post_init(self, __context):
        """Setup team coordination"""
        super().model_post_init(__context)
        # Share state references
        for agent in self.agents.values():
            agent.state.metadata['team_id'] = self.state.id

# 6. SYSTEM ORCHESTRATION - Top level
class HaiveSystem(BaseModel):
    """Complete system with proper Pydantic"""

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    # Components via factories
    workflow: Workflow = Field(default_factory=ResearchWorkflow)
    agent: Agent = Field(default_factory=ResearchAgent)
    multi_agent: MultiAgent = Field(default_factory=ResearchTeam)
    recompiler: SmartRecompiler = Field(default_factory=SmartRecompiler)

    # State
    current_state: Optional[UnifiedState] = Field(default=None)

    async def process(self, request: Request) -> Dict[str, Any]:
        """Process request through system"""

        # Initialize state
        self.current_state = StateInitializer.from_request(request)

        # Execute through layers
        self.current_state = await self.workflow.execute(self.current_state)
        self.current_state = await self.agent.execute(self.current_state)
        self.current_state = await self.multi_agent.execute(self.current_state)

        # Return result
        return self.current_state.model_dump()
```

## 🎯 **Key Pydantic Patterns Used**

1. **Field with default_factory** - For mutable defaults
2. **field_validator** - For field validation
3. **model_validator** - For cross-field validation
4. **model_post_init** - For post-initialization setup
5. **ConfigDict** - For model configuration
6. **Composition over inheritance** - Multiple inheritance of mixins
7. **No **init** override** - Let Pydantic handle initialization

## ✅ **Benefits of Correct Pydantic Design**

1. **Validation works** - All fields validated automatically
2. **Serialization works** - model_dump() and model_validate()
3. **Type safety** - Pydantic enforces types
4. **Default handling** - Proper mutable defaults with factories
5. **Field exclusion** - Control what gets serialized
6. **Settings management** - Easy configuration
7. **Schema generation** - Automatic OpenAPI schemas

## 🚀 **The Result: Clean, Correct Architecture**

With this Pydantic-correct design:

- No **init** overrides breaking validation
- All setup in model_post_init or validators
- Proper use of Field() with factories
- Clean composition with mixins
- Full validation and serialization support
- Type safety throughout

**This is how Haive should be built - respecting Pydantic's design patterns for a robust, maintainable system.**
