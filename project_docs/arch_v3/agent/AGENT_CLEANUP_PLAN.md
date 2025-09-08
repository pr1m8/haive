# Agent Cleanup Implementation Plan

**Domain**: Agent Simplification  
**Estimated Days**: 6-7 days  
**Target LOC**: 8,000 LOC (from 15,000 LOC - 47% reduction)  
**Dependencies**: [Contracts](../contracts/PROTOCOL_CONTRACTS_PLAN.md), [Engine](../engine/ENGINE_DECOMPOSITION_PLAN.md), [Workflow](../workflow/WORKFLOW_CREATION_PLAN.md)

## 🎯 Overview

Clean up 25 agent files scattered across multiple patterns into 12 focused, single-responsibility agent implementations. Transform agents from complex inheritance hierarchies into simple composition-based patterns using the new workflow layer.

## 📊 Current State Analysis

### The Agent Explosion Problem
```bash
# Current agent structure (15,000 total LOC)
packages/haive-agents/src/haive/agents/
├── base/
│   ├── agent.py                       # 1,200 LOC - Base agent
│   ├── enhanced_agent.py              # 800 LOC - Enhanced features
│   └── meta_agent.py                  # 600 LOC - Meta capabilities
├── simple/
│   ├── agent.py                       # 400 LOC - Simple agent v1
│   ├── agent_v2.py                    # 500 LOC - Simple agent v2
│   └── agent_v3.py                    # 600 LOC - Simple agent v3
├── react/
│   ├── agent.py                       # 1,500 LOC - ReactAgent
│   ├── react_node.py                  # 400 LOC - React execution
│   └── reasoning.py                   # 300 LOC - Reasoning patterns
├── rag/
│   ├── base/agent.py                  # 800 LOC - Base RAG
│   ├── simple/agent.py                # 600 LOC - Simple RAG
│   ├── enhanced/agent.py              # 700 LOC - Enhanced RAG
│   └── vector_agent.py                # 500 LOC - Vector operations
├── multi/
│   ├── enhanced_multi_agent_v4.py     # 2,000 LOC - Multi-agent v4
│   ├── multi_agent.py                 # 800 LOC - Basic multi-agent
│   ├── sequential_agent.py            # 400 LOC - Sequential pattern
│   └── parallel_agent.py              # 350 LOC - Parallel pattern
├── specialized/
│   ├── planning_agent.py              # 900 LOC - Planning logic
│   ├── research_agent.py              # 700 LOC - Research workflows
│   ├── coding_agent.py                # 800 LOC - Code generation
│   └── analysis_agent.py              # 600 LOC - Data analysis
├── memory/
│   ├── memory_agent.py                # 500 LOC - Memory management
│   └── context_agent.py               # 400 LOC - Context handling
└── experimental/
    ├── self_improving_agent.py        # 300 LOC - Self-improvement
    └── meta_learning_agent.py         # 250 LOC - Meta-learning
```

### Key Problems Identified

1. **Version Proliferation**: 3+ versions of SimpleAgent with unclear differences
2. **Mixed Abstractions**: Base agents handling workflow + LLM + state management
3. **Inheritance Hell**: Deep inheritance chains making changes risky
4. **Duplicate Code**: Same patterns implemented multiple times
5. **No Clear Patterns**: Each agent uses different approaches to similar problems

### Agent Responsibility Analysis
| Agent Type | Workflow Logic | LLM Integration | State Management | Tool Usage |
|------------|----------------|-----------------|------------------|------------|
| SimpleAgent | ✅ | ✅ | ✅ | ❌ |
| ReactAgent | ✅ | ✅ | ✅ | ✅ |
| RAGAgent | ✅ | ✅ | ✅ | ✅ |
| MultiAgent | ✅ | ❌ | ✅ | ❌ |
| PlanningAgent | ✅ | ✅ | ✅ | ✅ |

**Problem**: Every agent reimplements workflow logic differently.

## 🏗️ Target Architecture

### Clean Agent Structure (8,000 total LOC)
```
packages/haive-agents/src/haive/agents/
├── __init__.py                         # Agent exports (100 LOC)
├── base/
│   ├── __init__.py                    # Base exports (30 LOC)
│   ├── agent.py                       # Core agent (300 LOC)
│   ├── workflow_agent.py              # Workflow + LLM composition (200 LOC)
│   └── protocol_agent.py              # Protocol implementation (150 LOC)
├── simple.py                          # Simple agent (200 LOC)
├── react.py                           # React agent (400 LOC)
├── rag/
│   ├── __init__.py                    # RAG exports (20 LOC)
│   ├── base_rag.py                    # Base RAG pattern (300 LOC)
│   ├── simple_rag.py                  # Simple RAG (150 LOC)
│   └── enhanced_rag.py                # Enhanced RAG features (250 LOC)
├── specialized/
│   ├── __init__.py                    # Specialized exports (20 LOC)
│   ├── planning.py                    # Planning agent (300 LOC)
│   ├── research.py                    # Research agent (250 LOC)
│   ├── coding.py                      # Coding agent (300 LOC)
│   └── analysis.py                    # Analysis agent (200 LOC)
├── composition/
│   ├── __init__.py                    # Composition exports (20 LOC)
│   ├── agent_factory.py               # Agent creation patterns (200 LOC)
│   └── common_patterns.py             # Reusable agent patterns (150 LOC)
└── legacy/
    ├── __init__.py                    # Legacy exports (50 LOC)
    ├── migration_guide.md             # Migration documentation
    └── compatibility_layer.py         # Backward compatibility (300 LOC)
```

**Total**: 12 focused files, ~8,000 LOC (47% reduction)

### Design Principles

1. **Composition over Inheritance**: Agents use workflows, not extend complex bases
2. **Single Responsibility**: Each agent has one clear purpose
3. **Protocol-Based**: All agents implement AgentProtocol
4. **Workflow Delegation**: Complex orchestration delegated to workflow layer
5. **No Version Suffixes**: One definitive implementation per pattern

## 📋 Detailed Implementation Steps

### Step 1: Create Clean Base Agent (Day 1)

#### 1.1 Core Agent Implementation
**File**: `base/agent.py`

```python
from typing import Any, Dict, Optional, TypeVar, Generic
from haive.core.contracts.agent.agent_protocol import AgentProtocol, AgentMetadata
from haive.core.contracts.engine.engine_protocol import EngineProtocol
from haive.core.workflow.base.base_workflow import BaseWorkflow
from pydantic import BaseModel, Field

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
ConfigT = TypeVar('ConfigT')
StateT = TypeVar('StateT')

class Agent(BaseModel, AgentProtocol[InputT, OutputT, ConfigT, StateT]):
    """Clean base agent implementation using composition."""
    
    # Core configuration
    name: str = Field(..., description="Agent identifier")
    engine: Optional[EngineProtocol] = Field(default=None, description="LLM engine")
    workflow: Optional[BaseWorkflow] = Field(default=None, description="Orchestration workflow")
    
    # Agent metadata
    agent_type: str = Field(default="base", description="Agent type identifier")
    version: str = Field(default="1.0", description="Agent version")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    
    # Runtime state
    _state: Dict[str, Any] = Field(default_factory=dict, description="Internal agent state")
    _execution_history: List[Dict[str, Any]] = Field(default_factory=list, description="Execution history")
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        extra = "forbid"
    
    @property
    def metadata(self) -> AgentMetadata:
        """Agent metadata."""
        return AgentMetadata(
            name=self.name,
            agent_type=self.agent_type,
            capabilities=self.capabilities,
            version=self.version
        )
    
    @property
    def config(self) -> ConfigT:
        """Agent configuration."""
        return self.engine.config if self.engine else None
    
    def configure(self, **kwargs) -> None:
        """Update agent configuration."""
        if self.engine:
            self.engine.configure(**kwargs)
    
    async def arun(self, input_data: InputT, state: StateT | None = None) -> OutputT:
        """Execute agent asynchronously."""
        # Update internal state if provided
        if state:
            self._state.update(state if isinstance(state, dict) else {})
        
        # Choose execution path
        if self.workflow:
            # Use workflow for orchestration
            workflow_input = self._prepare_workflow_input(input_data, self._state)
            result = await self.workflow.aexecute(workflow_input)
            return self._process_workflow_output(result)
        elif self.engine:
            # Direct engine execution
            engine_input = self._prepare_engine_input(input_data, self._state)
            result = await self.engine.arun(engine_input)
            return self._process_engine_output(result)
        else:
            raise ValueError("Agent requires either engine or workflow")
    
    def run(self, input_data: InputT, state: StateT | None = None) -> OutputT:
        """Execute agent synchronously."""
        import asyncio
        return asyncio.run(self.arun(input_data, state))
    
    def as_tool(self, name: str | None = None, description: str | None = None) -> Any:
        """Convert agent to a tool."""
        from langchain_core.tools import Tool
        
        tool_name = name or f"{self.name}_tool"
        tool_description = description or f"Execute {self.name} agent"
        
        def execute_agent(query: str) -> str:
            """Execute agent as tool."""
            result = self.run({"query": query})
            return str(result) if not isinstance(result, str) else result
        
        return Tool(
            name=tool_name,
            description=tool_description,
            func=execute_agent
        )
    
    def _prepare_workflow_input(self, input_data: InputT, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for workflow execution."""
        return {
            "input": input_data,
            "agent_state": state,
            "agent_name": self.name
        }
    
    def _prepare_engine_input(self, input_data: InputT, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for engine execution."""
        if isinstance(input_data, dict):
            return {**input_data, "state": state}
        else:
            return {"input": input_data, "state": state}
    
    def _process_workflow_output(self, workflow_result: Dict[str, Any]) -> OutputT:
        """Process workflow output."""
        # Extract final result from workflow
        if "final_result" in workflow_result:
            return workflow_result["final_result"]
        else:
            return workflow_result
    
    def _process_engine_output(self, engine_result: Any) -> OutputT:
        """Process engine output."""
        return engine_result
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state."""
        return self._state.copy()
    
    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update agent state."""
        self._state.update(updates)
    
    def reset_state(self) -> None:
        """Reset agent to initial state."""
        self._state.clear()
        self._execution_history.clear()
```

### Step 2: Simple Agents (Day 2)

#### 2.1 Definitive Simple Agent
**File**: `simple.py`

```python
from typing import Dict, Any, Optional
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from .base.agent import Agent

class SimpleAgent(Agent):
    """Simple agent with direct LLM execution."""
    
    def __init__(
        self,
        name: str,
        engine: Optional[AugLLMConfig] = None,
        system_message: Optional[str] = None,
        **kwargs
    ):
        # Create default engine if not provided
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.7,
                system_message=system_message
            )
        elif system_message:
            engine.system_message = system_message
        
        super().__init__(
            name=name,
            engine=engine,
            agent_type="simple",
            capabilities=["text_generation", "conversation"],
            **kwargs
        )
    
    async def arun(self, input_data: Dict[str, Any] | str, state: Dict[str, Any] | None = None) -> str:
        """Execute simple agent."""
        # Convert string input to message format
        if isinstance(input_data, str):
            input_data = {"messages": [{"role": "user", "content": input_data}]}
        elif isinstance(input_data, dict) and "messages" not in input_data:
            # Assume single message
            content = input_data.get("content") or input_data.get("query") or str(input_data)
            input_data = {"messages": [{"role": "user", "content": content}]}
        
        # Execute using engine
        result = await self.engine.arun(input_data)
        
        # Record execution
        self._execution_history.append({
            "input": input_data,
            "output": result,
            "timestamp": time.time()
        })
        
        return result
    
    def run(self, input_data: Dict[str, Any] | str, state: Dict[str, Any] | None = None) -> str:
        """Execute simple agent synchronously."""
        import asyncio
        return asyncio.run(self.arun(input_data, state))

# Factory function for common patterns
def create_simple_agent(
    name: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    system_message: Optional[str] = None
) -> SimpleAgent:
    """Factory for creating simple agents."""
    return SimpleAgent(
        name=name,
        engine=AugLLMConfig(
            model=model,
            temperature=temperature,
            system_message=system_message
        )
    )

def create_deterministic_agent(name: str, model: str = "gpt-3.5-turbo") -> SimpleAgent:
    """Factory for deterministic simple agents."""
    return create_simple_agent(
        name=name,
        model=model,
        temperature=0.0,
        system_message="You are a helpful and precise assistant."
    )
```

### Step 3: React Agent (Day 3)

#### 2.1 Clean React Implementation
**File**: `react.py`

```python
from typing import Dict, Any, List, Optional
from haive.core.engine.aug_llm import AugLLMConfig  
from haive.core.workflow.loop_workflow import LoopWorkflow
from .base.agent import Agent

class ReactAgent(Agent):
    """React agent using loop workflow for reasoning."""
    
    def __init__(
        self,
        name: str,
        engine: Optional[AugLLMConfig] = None,
        tools: List[Any] = None,
        max_iterations: int = 10,
        **kwargs
    ):
        # Create engine with tools
        if engine is None:
            engine = AugLLMConfig(temperature=0.3)
        
        if tools:
            for tool in tools:
                engine.add_tool(tool)
        
        # Create reasoning workflow
        reasoning_workflow = self._create_reasoning_workflow(max_iterations)
        
        super().__init__(
            name=name,
            engine=engine,
            workflow=reasoning_workflow,
            agent_type="react",
            capabilities=["reasoning", "tool_usage", "planning"],
            **kwargs
        )
        
        self.tools = tools or []
        self.max_iterations = max_iterations
    
    def _create_reasoning_workflow(self, max_iterations: int) -> LoopWorkflow:
        """Create reasoning loop workflow."""
        workflow = LoopWorkflow(
            name=f"{self.name}_reasoning",
            max_iterations=max_iterations
        )
        
        def reasoning_step(data, context):
            """Single reasoning step."""
            # Get current thought and observations
            thought = self._generate_thought(data)
            action = self._decide_action(thought, data)
            observation = self._execute_action(action)
            
            # Update reasoning state
            reasoning_state = data.get("reasoning_state", {
                "thoughts": [],
                "actions": [],
                "observations": [],
                "iteration": 0
            })
            
            reasoning_state["thoughts"].append(thought)
            reasoning_state["actions"].append(action)
            reasoning_state["observations"].append(observation)
            reasoning_state["iteration"] += 1
            
            return {
                **data,
                "reasoning_state": reasoning_state,
                "latest_thought": thought,
                "latest_action": action,
                "latest_observation": observation
            }
        
        def should_continue(data):
            """Continue if we haven't found a final answer."""
            reasoning_state = data.get("reasoning_state", {})
            latest_action = reasoning_state.get("actions", [])
            
            if not latest_action:
                return True
            
            # Stop if we have a final answer
            last_action = latest_action[-1]
            return not (last_action.get("type") == "final_answer")
        
        workflow.add_step(reasoning_step, "reason")
        workflow.set_continue_condition(should_continue)
        
        return workflow
    
    def _generate_thought(self, data: Dict[str, Any]) -> str:
        """Generate reasoning thought."""
        context = self._build_reasoning_context(data)
        
        thought_prompt = f"""
        Current situation: {context}
        
        Think about this step by step. What should I consider next?
        
        Thought:"""
        
        return self.engine.run({"messages": [{"role": "user", "content": thought_prompt}]})
    
    def _decide_action(self, thought: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Decide next action based on thought."""
        available_tools = [tool.name for tool in self.tools] if self.tools else []
        
        action_prompt = f"""
        Thought: {thought}
        
        Available actions:
        - Use tool: {', '.join(available_tools)}
        - Final answer: Provide the final response
        
        What action should I take?
        
        Action:"""
        
        action_text = self.engine.run({"messages": [{"role": "user", "content": action_prompt}]})
        
        # Parse action (simplified - could be more sophisticated)
        if "final answer" in action_text.lower():
            return {"type": "final_answer", "content": action_text}
        else:
            # Assume tool usage
            return {"type": "tool_use", "tool": "calculator", "input": action_text}
    
    def _execute_action(self, action: Dict[str, Any]) -> str:
        """Execute the decided action."""
        if action["type"] == "final_answer":
            return action["content"]
        elif action["type"] == "tool_use":
            # Execute tool (simplified)
            tool_name = action.get("tool")
            tool_input = action.get("input")
            
            # Find and execute tool
            for tool in self.tools:
                if getattr(tool, 'name', str(tool)) == tool_name:
                    try:
                        result = tool.run(tool_input)
                        return f"Tool result: {result}"
                    except Exception as e:
                        return f"Tool error: {e}"
            
            return f"Tool {tool_name} not found"
        
        return "Unknown action"
    
    def _build_reasoning_context(self, data: Dict[str, Any]) -> str:
        """Build context for reasoning."""
        reasoning_state = data.get("reasoning_state", {})
        original_query = data.get("input", {}).get("query", "")
        
        context_parts = [f"Original query: {original_query}"]
        
        if reasoning_state.get("thoughts"):
            context_parts.append("Previous thoughts:")
            for i, thought in enumerate(reasoning_state["thoughts"]):
                context_parts.append(f"  {i+1}. {thought}")
        
        if reasoning_state.get("observations"):
            context_parts.append("Previous observations:")
            for i, obs in enumerate(reasoning_state["observations"]):
                context_parts.append(f"  {i+1}. {obs}")
        
        return "\n".join(context_parts)

# Factory function
def create_react_agent(
    name: str,
    tools: List[Any] = None,
    model: str = "gpt-4",
    max_iterations: int = 10
) -> ReactAgent:
    """Factory for creating React agents."""
    return ReactAgent(
        name=name,
        engine=AugLLMConfig(
            model=model,
            temperature=0.3,
            system_message="You are a helpful assistant that thinks step by step and uses tools when needed."
        ),
        tools=tools or [],
        max_iterations=max_iterations
    )
```

### Step 4: RAG Agents (Day 4)

#### 4.1 Base RAG Pattern
**File**: `rag/base_rag.py`

```python
from typing import Dict, Any, List, Optional
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from haive.core.engine.aug_llm import AugLLMConfig
from ..base.agent import Agent

class BaseRAGAgent(Agent):
    """Base RAG agent with retrieval → generation pattern."""
    
    def __init__(
        self,
        name: str,
        vector_store: Any = None,
        retriever_config: Optional[Dict[str, Any]] = None,
        generator_config: Optional[AugLLMConfig] = None,
        **kwargs
    ):
        # Set up retriever
        self.vector_store = vector_store or self._create_default_vector_store()
        self.retriever_config = retriever_config or {"k": 5, "score_threshold": 0.7}
        
        # Set up generator
        if generator_config is None:
            generator_config = AugLLMConfig(
                temperature=0.3,
                system_message="You are a helpful assistant that answers questions based on provided context."
            )
        
        # Create RAG workflow
        rag_workflow = self._create_rag_workflow()
        
        super().__init__(
            name=name,
            engine=generator_config,
            workflow=rag_workflow,
            agent_type="rag",
            capabilities=["retrieval", "generation", "question_answering"],
            **kwargs
        )
    
    def _create_default_vector_store(self):
        """Create default in-memory vector store."""
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Create empty vector store (would be populated with documents)
        import numpy as np
        dummy_texts = ["This is a placeholder document."]
        dummy_embeddings = embeddings.embed_documents(dummy_texts)
        
        return FAISS.from_embeddings(
            list(zip(dummy_texts, dummy_embeddings)),
            embeddings
        )
    
    def _create_rag_workflow(self) -> SequentialWorkflow:
        """Create RAG workflow: retrieve → generate."""
        workflow = SequentialWorkflow(f"{self.name}_rag")
        
        def retrieve_step(data, context):
            """Retrieve relevant documents."""
            query = data.get("query") or data.get("input", "")
            
            # Retrieve documents
            retriever = self.vector_store.as_retriever(**self.retriever_config)
            docs = retriever.get_relevant_documents(query)
            
            # Format context
            context_text = "\n\n".join([doc.page_content for doc in docs])
            
            return {
                **data,
                "retrieved_docs": docs,
                "context": context_text,
                "num_docs_retrieved": len(docs)
            }
        
        def generate_step(data, context):
            """Generate answer based on retrieved context."""
            query = data.get("query") or data.get("input", "")
            context_text = data.get("context", "")
            
            # Create prompt with context
            prompt = f"""
            Context:
            {context_text}
            
            Question: {query}
            
            Based on the provided context, please answer the question. If the context doesn't contain enough information to answer the question, say so clearly.
            
            Answer:"""
            
            # Generate response
            response = self.engine.run({"messages": [{"role": "user", "content": prompt}]})
            
            return {
                **data,
                "answer": response,
                "generation_input": prompt
            }
        
        workflow.add_step(retrieve_step, "retrieve")
        workflow.add_step(generate_step, "generate")
        
        return workflow
    
    def add_documents(self, documents: List[str]) -> None:
        """Add documents to vector store."""
        from langchain_core.documents import Document
        
        docs = [Document(page_content=doc) for doc in documents]
        self.vector_store.add_documents(docs)
    
    async def arun(self, input_data: Dict[str, Any] | str, state: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Execute RAG agent."""
        # Convert string input to query format
        if isinstance(input_data, str):
            input_data = {"query": input_data}
        
        # Execute RAG workflow
        result = await super().arun(input_data, state)
        
        # Return structured RAG result
        return {
            "answer": result.get("answer", ""),
            "context": result.get("context", ""),
            "num_docs_retrieved": result.get("num_docs_retrieved", 0),
            "query": input_data.get("query", "")
        }

# Factory functions
def create_simple_rag_agent(
    name: str,
    documents: List[str] = None,
    model: str = "gpt-3.5-turbo"
) -> BaseRAGAgent:
    """Factory for simple RAG agents."""
    agent = BaseRAGAgent(
        name=name,
        generator_config=AugLLMConfig(
            model=model,
            temperature=0.3
        )
    )
    
    if documents:
        agent.add_documents(documents)
    
    return agent
```

### Step 5: Specialized Agents (Day 5)

#### 5.1 Planning Agent
**File**: `specialized/planning.py`

```python
from typing import Dict, Any, List, Optional
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from haive.core.engine.aug_llm import AugLLMConfig
from ..base.agent import Agent
from pydantic import BaseModel

class PlanStep(BaseModel):
    """Single step in a plan."""
    step_number: int
    description: str
    dependencies: List[int] = []
    estimated_time: Optional[str] = None

class Plan(BaseModel):
    """Complete plan structure."""
    goal: str
    steps: List[PlanStep]
    total_estimated_time: Optional[str] = None

class PlanningAgent(Agent):
    """Agent specialized for creating structured plans."""
    
    def __init__(
        self,
        name: str,
        planning_style: str = "detailed",
        engine: Optional[AugLLMConfig] = None,
        **kwargs
    ):
        # Configure for planning
        if engine is None:
            engine = AugLLMConfig(
                model="gpt-4",
                temperature=0.3,
                structured_output_model=Plan,
                system_message="You are an expert planning assistant that creates detailed, actionable plans."
            )
        
        # Create planning workflow
        planning_workflow = self._create_planning_workflow(planning_style)
        
        super().__init__(
            name=name,
            engine=engine,
            workflow=planning_workflow,
            agent_type="planning",
            capabilities=["planning", "task_decomposition", "structured_output"],
            **kwargs
        )
        
        self.planning_style = planning_style
    
    def _create_planning_workflow(self, style: str) -> SequentialWorkflow:
        """Create planning workflow."""
        workflow = SequentialWorkflow(f"{self.name}_planning")
        
        def analyze_goal_step(data, context):
            """Analyze the goal and requirements."""
            goal = data.get("goal") or data.get("input", "")
            
            analysis_prompt = f"""
            Goal: {goal}
            
            Analyze this goal and identify:
            1. Key requirements
            2. Potential challenges  
            3. Success criteria
            4. Resource needs
            
            Analysis:"""
            
            analysis = self.engine.run({"messages": [{"role": "user", "content": analysis_prompt}]})
            
            return {
                **data,
                "goal_analysis": analysis,
                "analyzed_goal": goal
            }
        
        def create_plan_step(data, context):
            """Create structured plan."""
            goal = data.get("analyzed_goal", "")
            analysis = data.get("goal_analysis", "")
            
            planning_prompt = f"""
            Goal: {goal}
            Analysis: {analysis}
            
            Create a detailed plan with specific steps. Each step should be:
            - Clear and actionable
            - Include dependencies if any
            - Have estimated time if possible
            
            Plan:"""
            
            # Use structured output
            plan = self.engine.run({"messages": [{"role": "user", "content": planning_prompt}]})
            
            return {
                **data,
                "plan": plan,
                "planning_style": self.planning_style
            }
        
        workflow.add_step(analyze_goal_step, "analyze")
        workflow.add_step(create_plan_step, "plan")
        
        return workflow
    
    async def arun(self, input_data: Dict[str, Any] | str, state: Dict[str, Any] | None = None) -> Plan:
        """Execute planning agent."""
        # Convert string input to goal format
        if isinstance(input_data, str):
            input_data = {"goal": input_data}
        
        # Execute planning workflow
        result = await super().arun(input_data, state)
        
        # Return structured plan
        if isinstance(result.get("plan"), Plan):
            return result["plan"]
        else:
            # Fallback to manual parsing if structured output failed
            return self._parse_plan_manually(result)
    
    def _parse_plan_manually(self, result: Dict[str, Any]) -> Plan:
        """Manual plan parsing if structured output fails."""
        goal = result.get("analyzed_goal", "Unknown goal")
        plan_text = str(result.get("plan", ""))
        
        # Simple parsing (could be more sophisticated)
        steps = []
        lines = plan_text.split('\n')
        step_number = 1
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                steps.append(PlanStep(
                    step_number=step_number,
                    description=line
                ))
                step_number += 1
        
        return Plan(goal=goal, steps=steps)

# Factory functions
def create_project_planner(name: str) -> PlanningAgent:
    """Factory for project planning agents."""
    return PlanningAgent(
        name=name,
        planning_style="project",
        engine=AugLLMConfig(
            model="gpt-4",
            temperature=0.2,
            system_message="You are a project management expert who creates comprehensive project plans."
        )
    )

def create_task_planner(name: str) -> PlanningAgent:
    """Factory for task planning agents."""
    return PlanningAgent(
        name=name,
        planning_style="task",
        engine=AugLLMConfig(
            model="gpt-3.5-turbo",
            temperature=0.3,
            system_message="You are a productivity expert who breaks down tasks into actionable steps."
        )
    )
```

### Step 6: Agent Factory & Composition (Day 6)

#### 6.1 Agent Factory
**File**: `composition/agent_factory.py`

```python
from typing import Any, Dict, List, Optional, Type, Union
from ..simple import SimpleAgent
from ..react import ReactAgent
from ..rag.base_rag import BaseRAGAgent
from ..specialized.planning import PlanningAgent
from haive.core.engine.aug_llm import AugLLMConfig

class AgentFactory:
    """Factory for creating agents with common patterns."""
    
    @staticmethod
    def create_simple_agent(
        name: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        system_message: Optional[str] = None,
        **kwargs
    ) -> SimpleAgent:
        """Create a simple conversation agent."""
        return SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                model=model,
                temperature=temperature,
                system_message=system_message
            ),
            **kwargs
        )
    
    @staticmethod
    def create_react_agent(
        name: str,
        tools: List[Any],
        model: str = "gpt-4",
        max_iterations: int = 10,
        **kwargs
    ) -> ReactAgent:
        """Create a reasoning and acting agent."""
        return ReactAgent(
            name=name,
            engine=AugLLMConfig(
                model=model,
                temperature=0.3,
                system_message="You are a helpful assistant that reasons step by step and uses tools."
            ),
            tools=tools,
            max_iterations=max_iterations,
            **kwargs
        )
    
    @staticmethod
    def create_rag_agent(
        name: str,
        documents: List[str],
        model: str = "gpt-3.5-turbo",
        **kwargs
    ) -> BaseRAGAgent:
        """Create a RAG agent with document knowledge."""
        agent = BaseRAGAgent(
            name=name,
            generator_config=AugLLMConfig(
                model=model,
                temperature=0.3
            ),
            **kwargs
        )
        agent.add_documents(documents)
        return agent
    
    @staticmethod
    def create_planning_agent(
        name: str,
        planning_type: str = "general",
        model: str = "gpt-4",
        **kwargs
    ) -> PlanningAgent:
        """Create a planning agent."""
        if planning_type == "project":
            system_message = "You are a project management expert."
        elif planning_type == "task":
            system_message = "You are a productivity expert."
        else:
            system_message = "You are a planning specialist."
        
        return PlanningAgent(
            name=name,
            engine=AugLLMConfig(
                model=model,
                temperature=0.2,
                system_message=system_message
            ),
            **kwargs
        )
    
    @staticmethod
    def create_agent_team(
        agents_config: List[Dict[str, Any]],
        coordination_mode: str = "sequential"
    ) -> List[Any]:
        """Create a team of agents."""
        agents = []
        
        for config in agents_config:
            agent_type = config.pop("type", "simple")
            
            if agent_type == "simple":
                agent = AgentFactory.create_simple_agent(**config)
            elif agent_type == "react":
                agent = AgentFactory.create_react_agent(**config)
            elif agent_type == "rag":
                agent = AgentFactory.create_rag_agent(**config)
            elif agent_type == "planning":
                agent = AgentFactory.create_planning_agent(**config)
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            agents.append(agent)
        
        return agents

# Common agent patterns
class CommonAgentPatterns:
    """Pre-configured agent patterns for common use cases."""
    
    @staticmethod
    def customer_service_agent(name: str) -> SimpleAgent:
        """Customer service agent."""
        return AgentFactory.create_simple_agent(
            name=name,
            model="gpt-3.5-turbo",
            temperature=0.6,
            system_message="You are a helpful and empathetic customer service representative."
        )
    
    @staticmethod
    def research_assistant(name: str, tools: List[Any]) -> ReactAgent:
        """Research assistant with tools."""
        return AgentFactory.create_react_agent(
            name=name,
            tools=tools,
            model="gpt-4",
            max_iterations=8
        )
    
    @staticmethod
    def technical_writer(name: str) -> SimpleAgent:
        """Technical writing agent."""
        return AgentFactory.create_simple_agent(
            name=name,
            model="gpt-4",
            temperature=0.3,
            system_message="You are a technical writer who creates clear, accurate documentation."
        )
    
    @staticmethod
    def code_reviewer(name: str) -> SimpleAgent:
        """Code review agent."""
        return AgentFactory.create_simple_agent(
            name=name,
            model="gpt-4",
            temperature=0.2,
            system_message="You are an expert code reviewer focusing on quality, security, and best practices."
        )

# Usage examples
def example_agent_creation():
    """Examples of creating agents with the factory."""
    
    # Simple conversation agent
    chat_agent = AgentFactory.create_simple_agent(
        name="chat_assistant",
        temperature=0.8
    )
    
    # RAG agent with knowledge base
    knowledge_agent = AgentFactory.create_rag_agent(
        name="knowledge_assistant",
        documents=["Document 1 content", "Document 2 content"]
    )
    
    # Research team
    team_config = [
        {"type": "planning", "name": "planner", "planning_type": "project"},
        {"type": "react", "name": "researcher", "tools": []},
        {"type": "simple", "name": "writer", "temperature": 0.4}
    ]
    
    research_team = AgentFactory.create_agent_team(team_config)
    
    return chat_agent, knowledge_agent, research_team
```

### Step 7: Backward Compatibility & Migration (Day 7)

#### 7.1 Compatibility Layer
**File**: `legacy/compatibility_layer.py`

```python
from typing import Any, Dict, List, Optional
from ..simple import SimpleAgent
from ..react import ReactAgent
from ..rag.base_rag import BaseRAGAgent
from haive.core.engine.aug_llm import AugLLMConfig

class LegacyAgentWrapper:
    """Wrapper to maintain backward compatibility."""
    
    @staticmethod
    def create_simple_agent_v2(**kwargs):
        """Legacy SimpleAgentV2 compatibility."""
        # Map old parameters to new agent
        name = kwargs.get('name', 'legacy_simple_agent')
        engine_config = kwargs.get('engine', AugLLMConfig())
        
        return SimpleAgent(name=name, engine=engine_config)
    
    @staticmethod
    def create_simple_agent_v3(**kwargs):
        """Legacy SimpleAgentV3 compatibility.""" 
        # Map old parameters to new agent
        name = kwargs.get('name', 'legacy_simple_agent_v3')
        engine_config = kwargs.get('engine', AugLLMConfig())
        
        return SimpleAgent(name=name, engine=engine_config)

# Legacy class aliases for backward compatibility
SimpleAgentV2 = LegacyAgentWrapper.create_simple_agent_v2
SimpleAgentV3 = LegacyAgentWrapper.create_simple_agent_v3

# Migration utilities
class AgentMigrationUtils:
    """Utilities for migrating to new agent architecture."""
    
    @staticmethod
    def migrate_agent_config(old_config: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate old agent configuration to new format."""
        new_config = {}
        
        # Map common fields
        if 'name' in old_config:
            new_config['name'] = old_config['name']
        
        if 'engine' in old_config:
            new_config['engine'] = old_config['engine']
        
        # Handle deprecated fields
        deprecated_mappings = {
            'llm_config': 'engine',
            'model_config': 'engine',
            'ai_config': 'engine'
        }
        
        for old_key, new_key in deprecated_mappings.items():
            if old_key in old_config and new_key not in new_config:
                new_config[new_key] = old_config[old_key]
        
        return new_config
    
    @staticmethod
    def check_migration_compatibility(agent_instance: Any) -> Dict[str, Any]:
        """Check if agent instance is compatible with new architecture."""
        compatibility_report = {
            "compatible": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check for old patterns
        if hasattr(agent_instance, 'llm_config'):
            compatibility_report["issues"].append("Uses deprecated llm_config attribute")
            compatibility_report["recommendations"].append("Migrate to engine attribute")
        
        if hasattr(agent_instance, 'prompt_template'):
            compatibility_report["issues"].append("Uses old prompt_template pattern")
            compatibility_report["recommendations"].append("Migrate to workflow-based approach")
        
        compatibility_report["compatible"] = len(compatibility_report["issues"]) == 0
        
        return compatibility_report
```

## 📊 Success Metrics

### Technical Metrics
- [ ] **47% LOC reduction** (15,000 → 8,000 LOC)
- [ ] **12 focused agents** (from 25+ scattered implementations)
- [ ] **Zero version suffixes** - one definitive implementation per pattern
- [ ] **100% protocol compliance** - all agents implement AgentProtocol
- [ ] **Workflow delegation** - complex orchestration uses workflow layer

### Quality Metrics
- [ ] **Single responsibility** - each agent has one clear purpose
- [ ] **Composition over inheritance** - agents use workflows, not complex bases
- [ ] **Clear patterns** - consistent approach to similar problems
- [ ] **Backward compatibility** - existing code works through compatibility layer

### Developer Experience
- [ ] **Simple agent creation** - factory functions for common patterns
- [ ] **Clear documentation** - purpose and usage of each agent type
- [ ] **Easy testing** - agents testable in isolation
- [ ] **Migration path** - clear upgrade path from old to new agents

## 🔗 Integration Points

### With Workflow Domain
- Agents delegate orchestration to workflow layer
- Complex execution patterns implemented as workflows
- Agent execution becomes: Workflow + LLM Engine

### With Engine Domain  
- Agents use decomposed engine configurations
- Tool management handled by engine layer
- Clear separation between agent logic and LLM concerns

### With Contracts Domain
- All agents implement AgentProtocol interface
- Consistent behavior across agent types
- Type safety through protocol compliance

## 🚨 Common Pitfalls

### 1. Over-simplification
**Problem**: Removing necessary complexity during cleanup
**Solution**: Careful analysis of what complexity is actually needed

### 2. Breaking Changes
**Problem**: New architecture incompatible with existing usage
**Solution**: Comprehensive compatibility layer and migration tools

### 3. Performance Regression
**Problem**: New composition approach slower than old inheritance
**Solution**: Performance testing and optimization during migration

### 4. Lost Functionality
**Problem**: Features getting lost during consolidation
**Solution**: Feature audit and comprehensive testing

## 🔄 Rollback Strategy

### If Agent Cleanup Issues Arise
1. **Agent-by-agent rollback**: Each agent is independent
2. **Compatibility layer**: Keep old interfaces working
3. **Gradual migration**: Migrate one agent pattern at a time  
4. **Feature preservation**: Ensure no functionality loss

### Risk Mitigation
- Maintain compatibility layer throughout migration
- Comprehensive testing of new vs old agent behavior
- Clear migration guides for each agent type
- Performance monitoring during transition

---

**Next Steps**:
1. Start with SimpleAgent consolidation (most straightforward)
2. Build comprehensive testing for each new agent type
3. Create migration utilities and compatibility layer
4. Validate performance improvements with clean architecture