# Multi-Agent Flow Implementation Guide - Haive Framework

**Version**: 1.0  
**Date**: 2025-01-21  
**Status**: Complete - Based on Proven Patterns  
**Context**: Comprehensive guide from Plan-and-Execute V3 success and ReWOO research

## 🎯 **Overview**

This guide documents the proven patterns for implementing multi-agent flows using Enhanced MultiAgent V3, based on our successful Plan-and-Execute V3 implementation and extensive ReWOO research.

## 🏗️ **Core Architecture Pattern**

### **The Winning Formula**
```
Enhanced MultiAgent V3 + ChatPromptTemplate + Computed Fields + Sequential Mode = Success
```

### **Key Components**
1. **State Schema** - MessagesState extension with computed fields
2. **Structured Models** - Pydantic models for each agent's output
3. **ChatPromptTemplate** - Dynamic prompts using state field placeholders
4. **Sequential Coordination** - Reliable agent-to-agent flow
5. **Real Component Testing** - No mocks, actual LLM execution

## 📋 **Step-by-Step Implementation Process**

### **Phase 1: Research & Planning**
```bash
# 1. Research the methodology
# - Understand core concepts
# - Identify agent roles and coordination patterns
# - Map to Enhanced MultiAgent V3 architecture

# 2. Check existing implementations
find packages/haive-agents/ -name "*methodology_name*" -type d
grep -r "methodology_concepts" packages/haive-agents/

# 3. Document methodology in memory_index
# - Core concepts and advantages
# - Architecture mapping
# - Implementation plan
```

### **Phase 2: Directory Structure**
```bash
# Standard structure for all advanced agents
packages/haive-agents/src/haive/agents/planning/{agent_name}_v3/
├── models.py     # Pydantic structured output models
├── state.py      # State schema with computed fields
├── prompts.py    # ChatPromptTemplate for each sub-agent
├── agent.py      # Main agent using Enhanced MultiAgent V3
├── __init__.py   # Clean exports
└── README.md     # Usage examples and patterns
```

### **Phase 3: Pydantic Models (models.py)**

#### **Pattern: Input/Output + Internal Models**
```python
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# Status enums for workflow tracking
class ExecutionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success" 
    FAILED = "failed"
    PARTIAL = "partial"

# Individual step/component models
class WorkflowStep(BaseModel):
    step_id: str = Field(description="Unique step identifier")
    description: str = Field(description="What this step accomplishes")
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)
    depends_on: List[str] = Field(default_factory=list)
    
# Agent-specific structured outputs
class PlannerOutput(BaseModel):
    plan_id: str = Field(description="Unique plan identifier")
    objective: str = Field(description="Original objective")
    approach: str = Field(description="Overall approach")
    steps: List[WorkflowStep] = Field(description="Execution steps")
    reasoning: str = Field(description="Why this plan will work")
    created_at: datetime = Field(default_factory=datetime.now)

class ExecutorOutput(BaseModel):
    execution_id: str = Field(description="Unique execution identifier") 
    step_id: str = Field(description="Step being executed")
    result: str = Field(description="Execution result")
    tools_used: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.now)

# Main agent I/O models
class AgentInput(BaseModel):
    query: str = Field(description="User query to process")
    context: Optional[str] = Field(default=None)
    preferences: Optional[Dict[str, Any]] = Field(default=None)

class AgentOutput(BaseModel):
    query: str = Field(description="Original query")
    final_result: str = Field(description="Complete solution")
    execution_summary: str = Field(description="How solution was achieved")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    # Include timing, tools used, etc.
```

### **Phase 4: State Schema (state.py)**

#### **Pattern: MessagesState + Computed Fields**
```python
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import Field, computed_field
from haive.core.schema.prebuilt.messages_state import MessagesState
from .models import PlannerOutput, ExecutorOutput

class WorkflowState(MessagesState):
    """State schema with computed fields for dynamic prompts."""
    
    # Core workflow data
    original_query: str = Field(description="Original user query")
    current_phase: str = Field(default="planning", description="Current execution phase")
    
    # Agent results (stored as dicts, typed through models)
    planner_result: Optional[Dict[str, Any]] = Field(default=None)
    executor_results: List[Dict[str, Any]] = Field(default_factory=list)
    final_result: Optional[str] = Field(default=None)
    
    # Timing and metadata
    started_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # CRITICAL: Computed fields for prompt templates
    @computed_field
    @property 
    def current_plan_summary(self) -> str:
        """Formatted plan for executor prompts."""
        if not self.planner_result:
            return "No plan available"
            
        plan = PlannerOutput(**self.planner_result)
        summary = f"Objective: {plan.objective}\n\nApproach: {plan.approach}\n\nSteps:\n"
        for i, step in enumerate(plan.steps, 1):
            summary += f"{i}. {step.description}\n"
        return summary
    
    @computed_field
    @property
    def execution_history(self) -> str:
        """Formatted execution history for evaluator prompts."""
        if not self.executor_results:
            return "No executions completed"
            
        history = "Execution History:\n"
        for result_data in self.executor_results:
            result = ExecutorOutput(**result_data)
            history += f"- Step {result.step_id}: {result.result}\n"
        return history
    
    @computed_field
    @property
    def workflow_status(self) -> str:
        """Current workflow status for prompts."""
        if not self.planner_result:
            return "Planning phase"
        elif not self.executor_results:
            return "Ready for execution"
        elif not self.final_result:
            return f"Executing - {len(self.executor_results)} steps completed"
        else:
            return "Workflow completed"
    
    @computed_field 
    @property
    def available_context(self) -> str:
        """All available context for synthesis."""
        context = f"Query: {self.original_query}\n\n"
        context += f"Plan: {self.current_plan_summary}\n\n"
        context += f"Execution: {self.execution_history}\n\n"
        context += f"Status: {self.workflow_status}"
        return context
```

### **Phase 5: Prompt Templates (prompts.py)**

#### **Pattern: ChatPromptTemplate + State Field Placeholders**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# System messages - methodology-specific instructions
PLANNER_SYSTEM_MESSAGE = """You are an expert planning agent for [methodology name].

Your role:
- Analyze the user's query thoroughly
- Create a comprehensive execution plan
- Define clear steps with dependencies
- Consider available tools and constraints

Key principles:
- [Methodology-specific principles]
- Plan the complete solution upfront
- Use structured output format
- Be thorough and systematic"""

EXECUTOR_SYSTEM_MESSAGE = """You are a tool-using execution agent for [methodology name].

Your role:
- Execute individual plan steps
- Use available tools effectively
- Gather evidence and results
- Report execution outcomes

Key principles:
- Follow the plan precisely
- Use tools when needed
- Document all results
- Handle errors gracefully"""

# CRITICAL: Use state field placeholders in ChatPromptTemplate
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", PLANNER_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Query: {original_query}

Current Status: {workflow_status}

Create a comprehensive execution plan for this query.

Available tools: {available_tools}

Generate a structured plan with clear steps and reasoning.""")
])

executor_prompt = ChatPromptTemplate.from_messages([
    ("system", EXECUTOR_SYSTEM_MESSAGE), 
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Current Plan:
{current_plan_summary}

Execution History:
{execution_history}

Workflow Status: {workflow_status}

Execute the next step in the plan using available tools.""")
])

evaluator_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an evaluation agent..."),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Available Context:
{available_context}

Evaluate the current state and determine next actions.""")
])
```

### **Phase 6: Main Agent (agent.py)**

#### **Pattern: Enhanced MultiAgent V3 + Sequential Coordination**
```python
from typing import Any, Dict, List, Optional
from haive.agents.multi.enhanced_multi_agent import EnhancedMultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from .models import AgentInput, AgentOutput, PlannerOutput, ExecutorOutput
from .prompts import planner_prompt, executor_prompt, evaluator_prompt  
from .state import WorkflowState

class AdvancedMethodologyAgent:
    """Advanced agent using [methodology] with Enhanced MultiAgent V3."""
    
    def __init__(
        self,
        name: str,
        config: AugLLMConfig,
        tools: Optional[List] = None,
        **kwargs
    ):
        self.name = name
        self.config = config
        self.tools = tools or []
        
        # CRITICAL: Create sub-agents with prompt_template (NOT system_message)
        self._setup_sub_agents()
        
        # Enhanced MultiAgent V3 coordination
        self.multi_agent = EnhancedMultiAgent(
            name=f"{name}_coordinator",
            agents={
                "planner": self.planner,
                "executor": self.executor, 
                "evaluator": self.evaluator
            },
            execution_mode="sequential",  # Proven reliable
            state_schema=WorkflowState,
            **kwargs
        )
    
    def _setup_sub_agents(self):
        """Create sub-agents with proper prompt templates."""
        
        # Planner: SimpleAgent with structured output
        planner_config = AugLLMConfig.model_copy(self.config)
        planner_config.prompt_template = planner_prompt  # NOT system_message!
        
        self.planner = SimpleAgent(
            name=f"{self.name}_planner",
            engine=planner_config,
            structured_output_model=PlannerOutput
        )
        
        # Executor: ReactAgent with tools
        executor_config = AugLLMConfig.model_copy(self.config)
        executor_config.prompt_template = executor_prompt
        
        self.executor = ReactAgent(
            name=f"{self.name}_executor", 
            engine=executor_config,
            tools=self.tools,
            structured_output_model=ExecutorOutput
        )
        
        # Evaluator: SimpleAgent for assessment  
        evaluator_config = AugLLMConfig.model_copy(self.config)
        evaluator_config.prompt_template = evaluator_prompt
        
        self.evaluator = SimpleAgent(
            name=f"{self.name}_evaluator",
            engine=evaluator_config,
            structured_output_model=EvaluationResult  # Define as needed
        )
    
    async def arun(
        self,
        query: str,
        context: Optional[str] = None,
        **kwargs
    ) -> AgentOutput:
        """Execute the multi-agent workflow."""
        
        # Create initial state
        initial_state = WorkflowState(
            original_query=query,
            messages=[{"role": "user", "content": query}]
        )
        
        # Enhanced MultiAgent V3 handles coordination automatically
        result = await self.multi_agent.arun(
            state=initial_state,
            **kwargs
        )
        
        # Extract and format final output
        return self._format_output(result, query)
    
    def _format_output(self, result: Dict[str, Any], query: str) -> AgentOutput:
        """Format result into structured output."""
        # Extract final result from state
        # Calculate timing, confidence, etc.
        # Return structured AgentOutput
        pass
```

## 🔧 **Critical Implementation Patterns**

### **1. ALWAYS Use prompt_template, NOT system_message**
```python
# ✅ CORRECT
config = AugLLMConfig.model_copy(base_config)  
config.prompt_template = my_chat_prompt_template

# ❌ WRONG  
config = AugLLMConfig.model_copy(base_config)
config.system_message = "You are an agent..."
```

### **2. Computed Fields for Dynamic Prompts**
```python
# ✅ CORRECT - Computed fields provide dynamic values
@computed_field
@property
def current_status(self) -> str:
    """Dynamic status for prompt templates."""
    if not self.plan:
        return "Planning phase"
    # ... dynamic logic

# ❌ WRONG - Static strings in prompts
("human", "Status: planning")  # Never updates!
```

### **3. Sequential Mode for Reliability**
```python
# ✅ CORRECT - Sequential execution is proven
self.multi_agent = EnhancedMultiAgent(
    execution_mode="sequential",  # Reliable
    # ...
)

# ❌ AVOID - Complex routing until proven
execution_mode="conditional"  # Can cause routing issues
```

### **4. State Field Mapping**
```
Prompt Variable    →    State Field
{original_query}   →    state.original_query
{current_plan}     →    state.current_plan_summary (computed)
{workflow_status}  →    state.workflow_status (computed)  
{execution_history}→    state.execution_history (computed)
```

## 🧪 **Testing Pattern**

### **Real Component Testing Template**
```python
import pytest
from haive.core.engine.aug_llm import AugLLMConfig

@pytest.mark.asyncio
async def test_methodology_agent_real_execution():
    """Test with real LLM - no mocks."""
    
    # Real configuration
    config = AugLLMConfig(temperature=0.1)  # Low for consistency
    
    # Real tools (if needed)
    from haive.tools.math import Calculator
    tools = [Calculator()]
    
    # Create real agent
    agent = AdvancedMethodologyAgent(
        name="test_agent",
        config=config,
        tools=tools
    )
    
    # Real execution
    result = await agent.arun("Solve this complex problem requiring multiple steps")
    
    # Verify real behavior
    assert isinstance(result, AgentOutput)
    assert result.final_result
    assert result.confidence > 0.0
    assert len(result.execution_summary) > 0
    
    # Verify state management
    final_state = agent.multi_agent.last_state
    assert final_state.original_query == "Solve this complex problem requiring multiple steps"
    assert final_state.workflow_status == "Workflow completed"
```

## 📊 **Proven Infrastructure**

### **What's Working**
- ✅ **Enhanced MultiAgent V3**: Sequential coordination reliable
- ✅ **PostgreSQL Integration**: Connection and persistence working  
- ✅ **DateTime Serialization**: JSON serialization resolved
- ✅ **LangGraph Routing**: Auto state transitions working
- ✅ **ChatPromptTemplate**: Dynamic prompt generation working
- ✅ **Computed Fields**: State field placeholders working
- ✅ **Real LLM Testing**: Azure OpenAI integration working

### **Infrastructure Commands**
```bash
# Test real components
poetry run pytest packages/haive-agents/tests/planning/test_plan_execute_v3.py -v

# Check imports
poetry run python -c "from haive.agents.planning.plan_execute_v3 import PlanExecuteV3Agent"

# Run infrastructure tests
poetry run python -c "
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple import SimpleAgent
config = AugLLMConfig()
agent = SimpleAgent(engine=config)
print('Infrastructure working')
"
```

## 🎯 **Methodology-Specific Adaptations**

### **For Different Agent Patterns**

#### **Tree of Thoughts (ToT)**
- **State Fields**: tree_structure, current_node, exploration_paths
- **Sub-Agents**: node_generator, evaluator, selector
- **Coordination**: Tree traversal with backtracking

#### **Reflexion**
- **State Fields**: reflection_history, improvement_suggestions, iteration_count  
- **Sub-Agents**: actor, critic, memory_manager
- **Coordination**: Iterative actor-critic loops

#### **LATS (Language Agent Tree Search)**
- **State Fields**: search_tree, current_trajectory, value_estimates
- **Sub-Agents**: policy_agent, value_agent, search_controller
- **Coordination**: Monte Carlo Tree Search pattern

#### **ReWOO**
- **State Fields**: reasoning_plan, evidence_collection, synthesis_context
- **Sub-Agents**: planner, worker, solver  
- **Coordination**: Plan → Execute → Synthesize (no observation)

#### **LLM Compiler**
- **State Fields**: task_graph, execution_plan, dependency_tracking
- **Sub-Agents**: planner, executor, optimizer
- **Coordination**: Dependency-aware parallel execution

## 🚨 **Common Pitfalls & Solutions**

### **1. Import Path Issues**
```python
# ✅ CORRECT - Absolute imports
from haive.agents.planning.methodology_v3.models import ModelClass

# ❌ WRONG - Relative imports can break
from .models import ModelClass  # Can fail in tests
```

### **2. State Schema Flattening**
```python
# ✅ CORRECT - Store as dicts, cast to models when needed
planner_result: Optional[Dict[str, Any]] = None

# Access via model
plan = PlannerOutput(**self.planner_result)

# ❌ WRONG - Direct Pydantic in state (gets flattened)
planner_result: Optional[PlannerOutput] = None  # Flattening issues
```

### **3. Manual Node Functions**
```python
# ✅ CORRECT - Let Enhanced MultiAgent V3 handle routing
execution_mode="sequential"  # Automatic state transitions

# ❌ WRONG - Manual node functions (unnecessary complexity)
def custom_routing_node(state):
    # Manual routing logic
    pass
```

## 🎯 **Success Metrics**

### **Implementation Success Indicators**
- ✅ **Real LLM Execution**: No mocks, actual tool usage  
- ✅ **State Management**: Computed fields updating correctly
- ✅ **Agent Coordination**: Sequential execution working
- ✅ **Structured Output**: Pydantic models validating properly
- ✅ **Error Handling**: Graceful failure recovery
- ✅ **Performance**: <30s execution for complex tasks

### **Quality Checklist**
- [ ] All imports use absolute paths
- [ ] State schema has computed fields for prompt variables
- [ ] ChatPromptTemplate uses state field placeholders
- [ ] All sub-agents use prompt_template (not system_message)
- [ ] Enhanced MultiAgent V3 uses sequential mode
- [ ] Test file uses real LLM (no mocks)
- [ ] Structured output models validate correctly
- [ ] Documentation includes usage examples

## 🚀 **Implementation Roadmap**

### **For Each New Methodology**

1. **Research** (1-2 hours)
   - Study methodology papers/tutorials
   - Map to Enhanced MultiAgent V3 architecture
   - Create memory documentation

2. **Structure** (30 minutes)
   - Create directory with standard files
   - Set up imports and basic structure

3. **Models** (1 hour)
   - Define Pydantic models for each agent output
   - Create input/output models for main agent
   - Add proper validation and examples

4. **State** (1 hour)
   - Extend MessagesState with methodology fields
   - Create computed fields for prompt variables
   - Ensure proper typing and validation

5. **Prompts** (1 hour)
   - Create ChatPromptTemplate for each sub-agent
   - Use state field placeholders in prompts
   - Write methodology-specific system messages

6. **Agent** (1 hour)
   - Implement main agent with Enhanced MultiAgent V3
   - Create sub-agents with proper prompt templates
   - Set up sequential coordination

7. **Testing** (1 hour)
   - Write real component tests (no mocks)
   - Test with actual LLM and tools
   - Validate structured outputs and state management

8. **Documentation** (30 minutes)
   - Update memory files with patterns learned
   - Document any methodology-specific insights
   - Add usage examples

**Total per methodology: ~6 hours**

## 🎯 **Next Implementation Priorities**

Based on our success with Plan-and-Execute V3:

1. **ReWOO V3** - Already researched, models started
2. **LLM Compiler V3** - Update with proven patterns  
3. **Tree of Thoughts V3** - Complex but well-documented
4. **Reflexion V3** - Iterative pattern, interesting challenge
5. **LATS V3** - Most complex, save for last

---

**This guide represents the proven patterns from our Plan-and-Execute V3 success. Follow these patterns exactly for reliable implementation of advanced agent methodologies.**