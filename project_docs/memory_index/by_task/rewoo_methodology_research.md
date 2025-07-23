# ReWOO (Reasoning without Observation) - Methodology Research

**Date**: 2025-01-21
**Status**: Research Complete - Ready for Implementation
**Context**: Building ReWOO V3 as expansion of Plan-and-Execute V3 success

## 🎯 **ReWOO Core Concept**

**ReWOO = Reasoning WithOut Observation**

Traditional ALM (Augmented Language Model) systems interleave reasoning and tool execution:

```
LLM → Tool Call → LLM → Tool Call → LLM → Final Answer
(Each step waits for tool response before proceeding)
```

ReWOO separates these phases completely:

```
PHASE 1: LLM creates complete plan upfront
PHASE 2: All tools execute in parallel/batch
PHASE 3: LLM synthesizes all results together
```

## 🏗️ **Three-Module Architecture**

### **1. Planner Module**

- **Role**: Creates complete execution blueprint upfront
- **Input**: Original problem/query
- **Output**: Structured plan with tool calls and evidence placeholders
- **Key**: Plans entire solution without seeing any tool results

**Plan Format**:

```
Plan step 1: Search for information about X
Evidence #E1: [search tool output placeholder]

Plan step 2: Analyze the data from #E1
Evidence #E2: [analysis tool output placeholder]

Plan step 3: Synthesize findings from #E1 and #E2
Evidence #E3: [synthesis result placeholder]
```

### **2. Worker Module**

- **Role**: Executes all tool calls from the plan
- **Input**: Tool instructions from plan
- **Output**: Evidence for each step
- **Key**: Operates independently without LLM interaction

**Worker Execution**:

```
Worker[Plan step 1] → Evidence #E1 = "Search results..."
Worker[Plan step 2] → Evidence #E2 = "Analysis results..."
Worker[Plan step 3] → Evidence #E3 = "Synthesis results..."
```

### **3. Solver Module**

- **Role**: Synthesizes all evidence into final answer
- **Input**: Original plan + all evidence
- **Output**: Complete solution/answer
- **Key**: Has full context without iterative back-and-forth

## 🚀 **Key Advantages**

### **1. Token Efficiency (5x improvement)**

- No repeated context in iterative calls
- Single comprehensive LLM invocation per phase
- Eliminates redundant prompt tokens

### **2. Parallelizable Execution**

- All tool calls can run concurrently
- No sequential dependencies during execution phase
- Dramatically faster overall execution

### **3. Fine-tuning Friendly**

- Modular design allows targeted improvements
- Can fine-tune smaller models for specific roles
- Decoupled components enable focused optimization

### **4. Robustness**

- Plan continues even if some tools fail
- Solver can work with partial evidence
- Less brittle than sequential execution

## 🔄 **ReWOO vs Plan-and-Execute**

### **Similarities**

- Both separate planning from execution
- Both use structured plans and results
- Both coordinate multiple agents
- Both benefit from our ChatPromptTemplate + computed fields pattern

### **Key Differences**

| Aspect           | Plan-and-Execute V3              | ReWOO V3                          |
| ---------------- | -------------------------------- | --------------------------------- |
| **Execution**    | Sequential with evaluation loops | Batch execution, single synthesis |
| **Observation**  | Each step sees previous results  | No observation during planning    |
| **Adaptation**   | Can revise plan based on results | Plan is fixed, solver adapts      |
| **Coordination** | Evaluator → Replanner cycles     | Planner → Worker → Solver linear  |
| **Tools**        | ReactAgent with tools per step   | Batch tool execution              |

## 🎯 **ReWOO V3 Architecture Design**

### **State Schema (MessagesState + Computed Fields)**

```python
class ReWOOV3State(MessagesState):
    # Core data
    original_query: str
    reasoning_plan: Optional[ReWOOPlan] = None
    evidence_results: Dict[str, Any] = Field(default_factory=dict)
    final_solution: Optional[str] = None

    # Timing
    started_at: datetime = Field(default_factory=datetime.now)

    # Computed fields for prompts
    @computed_field
    @property
    def plan_summary(self) -> str:
        """Formatted plan for worker agents"""

    @computed_field
    @property
    def evidence_summary(self) -> str:
        """Formatted evidence for solver"""

    @computed_field
    @property
    def execution_status(self) -> str:
        """Current phase status"""
```

### **Three Agents with Enhanced MultiAgent V3**

```python
# Planner Agent (SimpleAgent)
self.planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig.model_copy(config, prompt_template=planner_prompt),
    structured_output_model=ReWOOPlan
)

# Worker Agent (ReactAgent with all tools)
self.worker = ReactAgent(
    name="worker",
    engine=AugLLMConfig.model_copy(config, prompt_template=worker_prompt),
    tools=self.tools,
    structured_output_model=EvidenceCollection
)

# Solver Agent (SimpleAgent)
self.solver = SimpleAgent(
    name="solver",
    engine=AugLLMConfig.model_copy(config, prompt_template=solver_prompt),
    structured_output_model=ReWOOSolution
)

# Enhanced MultiAgent V3 Coordination
self.multi_agent = EnhancedMultiAgent(
    name="rewoo_coordinator",
    agents={"planner": self.planner, "worker": self.worker, "solver": self.solver},
    execution_mode="sequential",  # planner → worker → solver
    state_schema=ReWOOV3State
)
```

### **ChatPromptTemplates with State Fields**

#### **Planner Prompt**

```python
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", PLANNER_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Query: {original_query}

Create a complete reasoning plan with evidence placeholders.
Plan the ENTIRE solution upfront without seeing any tool results.

Available tools: {available_tools}

Generate a structured plan with clear evidence references (#E1, #E2, etc.).""")
])
```

#### **Worker Prompt**

```python
worker_prompt = ChatPromptTemplate.from_messages([
    ("system", WORKER_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Execute all tool calls from the plan:

{plan_summary}

Use available tools to gather evidence for each step. Work through ALL steps systematically.""")
])
```

#### **Solver Prompt**

```python
solver_prompt = ChatPromptTemplate.from_messages([
    ("system", SOLVER_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Original Query: {original_query}

Reasoning Plan:
{plan_summary}

Evidence Collected:
{evidence_summary}

Current Status: {execution_status}

Synthesize all evidence to provide a comprehensive final answer.""")
])
```

## 📋 **Implementation Plan**

### **1. Create ReWOO V3 Directory Structure**

```
packages/haive-agents/src/haive/agents/planning/rewoo_v3/
├── models.py     # ReWOOPlan, EvidenceCollection, ReWOOSolution
├── state.py      # ReWOOV3State with computed fields
├── prompts.py    # ChatPromptTemplate for planner/worker/solver
├── agent.py      # ReWOOV3Agent with Enhanced MultiAgent V3
├── __init__.py   # Clean exports
└── README.md     # Usage examples
```

### **2. Pydantic Models**

- **ReWOOPlan**: Structured planning output with evidence placeholders
- **EvidenceCollection**: Worker results mapped to evidence IDs
- **ReWOOSolution**: Final synthesized answer with reasoning

### **3. State Management**

- Extend MessagesState with ReWOO-specific fields
- Computed fields for plan_summary, evidence_summary, execution_status
- Automatic state transitions through Enhanced MultiAgent V3

### **4. Agent Coordination**

- Sequential execution: planner → worker → solver
- No iterative loops (unlike Plan-and-Execute)
- Single pass through each agent

### **5. Testing Strategy**

- Real LLM execution (no mocks)
- Multi-step reasoning tasks requiring tool use
- Validation of evidence collection and synthesis
- Performance comparison with Plan-and-Execute V3

## 🎯 **Success Metrics**

### **Performance Targets**

- **Token Efficiency**: Fewer tokens than Plan-and-Execute V3
- **Execution Speed**: Faster with parallel tool execution
- **Accuracy**: Match or exceed Plan-and-Execute results
- **Robustness**: Handle partial tool failures gracefully

### **Validation Tasks**

- Complex research questions requiring multiple tools
- Multi-step mathematical problems
- Analysis tasks needing synthesis of information
- Scenarios with tool failures or partial results

## 🚀 **Implementation Advantages**

### **Building on Plan-and-Execute V3 Success**

- ✅ **Infrastructure proven**: PostgreSQL, datetime serialization, LangGraph routing
- ✅ **Patterns validated**: ChatPromptTemplate + computed fields working
- ✅ **Enhanced MultiAgent V3**: Sequential coordination reliable
- ✅ **Real component testing**: No mocks needed

### **ReWOO-Specific Benefits**

- **Simpler coordination**: No evaluation/replanning loops
- **Better parallelism**: All tool calls can run concurrently
- **Token efficiency**: Single comprehensive context per phase
- **Fine-tuning ready**: Modular design for targeted improvements

**ReWOO V3 represents the natural evolution of our planning agent architecture, leveraging all proven patterns while achieving superior efficiency through upfront planning and batch execution.**
