# Multi-Agent Systems Guide - Haive Framework

**Version**: 1.0
**Purpose**: Bottom-up guide for building multi-agent systems from first principles
**Last Updated**: 2025-01-18

## 🎯 What This Guide Is

This is a **bottom-up, hands-on guide** for building multi-agent systems in Haive. We'll start from the fundamentals and build real systems together, focusing exclusively on **multi-agent coordination patterns**.

This guide is **NOT** about:
- Building single agents (that's elsewhere)
- General agent concepts
- Theory without practice

This guide **IS** about:
- How agents communicate through shared state
- Building systems where agents work together
- Practical patterns you can use immediately
- Real code that actually works

## 🏗️ Core Philosophy

### State-First Design
We start with **state design** first, then build agents around it. The state is the **communication medium** between agents.

### Direct Field Updates
Agents update shared state fields directly - no complex nested structures or message passing.

### Progressive Building
We build from 2-agent systems up to complex multi-agent workflows, adding one concept at a time.

## 📚 Learning Path

### Foundation (Start Here)
1. **[Two-Agent Communication](#two-agent-communication)** - Basic agent-to-agent communication
2. **[State Design Patterns](#state-design-patterns)** - How to design multi-agent state
3. **[Sequential Workflows](#sequential-workflows)** - Agent A → Agent B → Agent C

### Intermediate
4. **[Structured Outputs](#structured-outputs)** - Type-safe agent communication
5. **[Parallel Processing](#parallel-processing)** - Multiple agents working simultaneously
6. **[Dynamic Composition](#dynamic-composition)** - Adding agents at runtime

### Advanced
7. **[Self-Discover Patterns](#self-discover-patterns)** - Agents building on each other's reasoning
8. **[Hierarchical Systems](#hierarchical-systems)** - Multi-level agent coordination
9. **[Error Handling](#error-handling)** - Robust multi-agent systems

## 🚀 Section 1: Two-Agent Communication

Let's start with the simplest multi-agent system: two agents that need to communicate.

### The Problem
Agent A needs to analyze something, Agent B needs to use that analysis to make a decision.

### The Solution
Use a shared state where Agent A writes its results and Agent B reads them.

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define what Agent A will output
class AnalysisResult(BaseModel):
    analysis: str = Field(description="The analysis result")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level")
    key_points: List[str] = Field(description="Key points identified")

# Step 2: Define what Agent B will output
class DecisionResult(BaseModel):
    decision: str = Field(description="The decision made")
    reasoning: str = Field(description="Why this decision was made")
    next_steps: List[str] = Field(description="Recommended next steps")

# Step 3: Create a state that has fields for both agents
class TwoAgentState(MultiAgentState):
    # Input field
    input_text: str = ""
    
    # Agent A outputs (these fields will be updated directly)
    analysis: str = ""
    confidence: float = 0.0
    key_points: List[str] = Field(default_factory=list)
    
    # Agent B outputs (these fields will be updated directly)
    decision: str = ""
    reasoning: str = ""
    next_steps: List[str] = Field(default_factory=list)

# Step 4: Create the agents
analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="Analyze the input and provide insights."
    ),
    structured_output_model=AnalysisResult
)

decision_maker = SimpleAgent(
    name="decision_maker",
    engine=AugLLMConfig(
        temperature=0.5,
        system_message="Based on the analysis, make a decision."
    ),
    structured_output_model=DecisionResult
)

# Step 5: Initialize state with both agents
state = TwoAgentState(
    agents=[analyzer, decision_maker],
    input_text="We need to decide whether to launch the new product."
)

# Step 6: Create execution nodes
analyzer_node = create_agent_node_v3("analyzer")
decision_node = create_agent_node_v3("decision_maker")

# Step 7: Execute in sequence
config = {"configurable": {"thread_id": "two_agent_example"}}

# Agent A analyzes
result1 = analyzer_node(state, config)
print(f"Analysis: {state.analysis}")
print(f"Confidence: {state.confidence}")
print(f"Key points: {state.key_points}")

# Agent B makes decision based on Agent A's output
result2 = decision_node(state, config)
print(f"Decision: {state.decision}")
print(f"Reasoning: {state.reasoning}")
print(f"Next steps: {state.next_steps}")
```

### 🔑 Key Insights

1. **State is the communication medium** - Agents communicate through shared state fields
2. **Direct field updates** - `state.analysis` is updated directly by the analyzer
3. **Sequential execution** - Agent B automatically sees Agent A's outputs
4. **Type safety** - Pydantic ensures all fields are properly typed

### 🎯 Exercise 1: Build Your First Two-Agent System

Try building a two-agent system where:
- Agent A: Summarizes a document
- Agent B: Extracts action items from the summary

What fields would you need in your state? What would each agent output?

## 🛠️ Section 2: State Design Patterns

The key to successful multi-agent systems is **good state design**. Let's learn the patterns.

### Pattern 1: Input-Processing-Output States

```python
class WorkflowState(MultiAgentState):
    # Input section - what comes into the system
    task_description: str = ""
    requirements: List[str] = Field(default_factory=list)
    
    # Processing section - intermediate results
    analysis: str = ""
    plan: List[str] = Field(default_factory=list)
    
    # Output section - final results
    result: str = ""
    status: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### Pattern 2: Agent-Specific Sections

```python
class MultiStageState(MultiAgentState):
    # Input
    input_data: str = ""
    
    # Research agent outputs
    research_findings: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    
    # Analysis agent outputs
    analysis_summary: str = ""
    key_insights: List[str] = Field(default_factory=list)
    
    # Report agent outputs
    final_report: str = ""
    recommendations: List[str] = Field(default_factory=list)
```

### Pattern 3: Shared Resources

```python
class SharedResourceState(MultiAgentState):
    # Shared across all agents
    context: Dict[str, Any] = Field(default_factory=dict)
    shared_memory: List[str] = Field(default_factory=list)
    
    # Agent-specific outputs
    agent_a_result: str = ""
    agent_b_result: str = ""
    agent_c_result: str = ""
```

### 🔍 State Design Guidelines

1. **Group related fields** - Put similar outputs together
2. **Use descriptive names** - `analysis_summary` not `result1`
3. **Provide defaults** - Use `Field(default_factory=list)` for lists
4. **Think about flow** - Design fields based on how data flows between agents
5. **Consider typing** - Use specific types, not just `str` or `Any`

### 🎯 Exercise 2: Design Your State

Design a state for a three-agent system:
- Agent A: Gathers information
- Agent B: Analyzes the information
- Agent C: Creates a presentation

What fields would each agent need? What would they output?

## 🔄 Section 3: Sequential Workflows

Sequential workflows are the foundation of multi-agent systems. Agent A → Agent B → Agent C.

### The Pattern

```python
# Create nodes
node_a = create_agent_node_v3("agent_a")
node_b = create_agent_node_v3("agent_b")
node_c = create_agent_node_v3("agent_c")

# Execute in sequence
result1 = node_a(state, config)    # Updates state with Agent A's outputs
result2 = node_b(state, config)    # Reads Agent A's outputs, adds Agent B's outputs
result3 = node_c(state, config)    # Reads both previous outputs, adds Agent C's outputs
```

### Real Example: Document Processing Pipeline

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Define outputs for each agent
class DocumentAnalysis(BaseModel):
    summary: str
    key_topics: List[str]
    word_count: int
    readability_score: float

class KeyPoints(BaseModel):
    main_points: List[str]
    supporting_evidence: List[str]
    conclusions: List[str]

class ActionItems(BaseModel):
    action_items: List[str]
    priorities: List[str]
    deadlines: List[str]

# Define the workflow state
class DocumentWorkflowState(MultiAgentState):
    # Input
    document_text: str = ""
    
    # Analyzer outputs
    summary: str = ""
    key_topics: List[str] = Field(default_factory=list)
    word_count: int = 0
    readability_score: float = 0.0
    
    # Extractor outputs
    main_points: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    conclusions: List[str] = Field(default_factory=list)
    
    # Action planner outputs
    action_items: List[str] = Field(default_factory=list)
    priorities: List[str] = Field(default_factory=list)
    deadlines: List[str] = Field(default_factory=list)

# Create agents
analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(
        system_message="Analyze documents and provide summaries with key topics."
    ),
    structured_output_model=DocumentAnalysis
)

extractor = SimpleAgent(
    name="extractor",
    engine=AugLLMConfig(
        system_message="Extract key points and conclusions from the analysis."
    ),
    structured_output_model=KeyPoints
)

planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(
        system_message="Create action items based on the extracted points."
    ),
    structured_output_model=ActionItems
)

# Run the workflow
def run_document_workflow(document_text: str):
    # Initialize state
    state = DocumentWorkflowState(
        agents=[analyzer, extractor, planner],
        document_text=document_text
    )
    
    # Create nodes
    analyzer_node = create_agent_node_v3("analyzer")
    extractor_node = create_agent_node_v3("extractor")
    planner_node = create_agent_node_v3("planner")
    
    config = {"configurable": {"thread_id": "doc_workflow"}}
    
    # Execute pipeline
    print("📄 Step 1: Document Analysis")
    result1 = analyzer_node(state, config)
    print(f"   Summary: {state.summary[:100]}...")
    print(f"   Topics: {state.key_topics}")
    print(f"   Word count: {state.word_count}")
    
    print("\n🔍 Step 2: Key Point Extraction")
    result2 = extractor_node(state, config)
    print(f"   Main points: {len(state.main_points)}")
    print(f"   Conclusions: {len(state.conclusions)}")
    
    print("\n📋 Step 3: Action Planning")
    result3 = planner_node(state, config)
    print(f"   Action items: {len(state.action_items)}")
    print(f"   Priorities: {state.priorities}")
    
    return state

# Example usage
if __name__ == "__main__":
    sample_document = """
    Our quarterly review shows significant growth in customer satisfaction.
    However, we need to address the increasing support ticket volume.
    The engineering team should focus on bug fixes, while the customer 
    success team needs additional training on the new features.
    """
    
    result = run_document_workflow(sample_document)
    print(f"\n✅ Final Results:")
    print(f"Action Items: {result.action_items}")
```

### 🎯 Exercise 3: Build a Sequential Workflow

Create a three-agent sequential workflow for:
1. **Research Agent**: Gathers information on a topic
2. **Analysis Agent**: Analyzes the research findings
3. **Report Agent**: Creates a final report

What would each agent need from the previous agent?

## 📊 Section 4: Structured Outputs

Structured outputs are what enable clean agent communication. Let's master this pattern.

### Why Structured Outputs Matter

```python
# ❌ BAD - Unstructured output
agent_output = "The analysis shows 85% confidence with key findings: performance improved, costs decreased, user satisfaction high"

# ✅ GOOD - Structured output
class AnalysisResult(BaseModel):
    confidence: float = Field(ge=0.0, le=1.0)
    performance_change: str
    cost_change: str
    user_satisfaction: str
    key_findings: List[str]

# Agent outputs this structured data
result = AnalysisResult(
    confidence=0.85,
    performance_change="improved",
    cost_change="decreased", 
    user_satisfaction="high",
    key_findings=["performance improved", "costs decreased", "user satisfaction high"]
)
```

### Building Structured Output Models

```python
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from enum import Enum

# Use enums for constrained choices
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Create comprehensive output models
class TaskAnalysis(BaseModel):
    """Output from task analysis agent."""
    
    task_complexity: int = Field(ge=1, le=10, description="Complexity score 1-10")
    estimated_hours: float = Field(ge=0, description="Estimated hours to complete")
    priority: Priority = Field(description="Task priority level")
    required_skills: List[str] = Field(description="Skills needed for this task")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    risk_factors: List[str] = Field(default_factory=list, description="Potential risks")
    
    @validator('estimated_hours')
    def validate_hours(cls, v):
        if v > 1000:
            raise ValueError('Estimated hours cannot exceed 1000')
        return v

class TaskPlan(BaseModel):
    """Output from task planning agent."""
    
    planned_steps: List[str] = Field(description="Ordered list of steps")
    milestones: List[Dict[str, Any]] = Field(default_factory=list, description="Key milestones")
    timeline: Dict[str, str] = Field(default_factory=dict, description="Timeline for each phase")
    resource_allocation: Dict[str, float] = Field(default_factory=dict, description="Resource allocation")
    
class TaskExecution(BaseModel):
    """Output from task execution agent."""
    
    status: TaskStatus = Field(description="Current task status")
    completed_steps: List[str] = Field(default_factory=list, description="Completed steps")
    current_step: Optional[str] = Field(None, description="Current step being worked on")
    blockers: List[str] = Field(default_factory=list, description="Current blockers")
    progress_percentage: float = Field(ge=0, le=100, description="Progress percentage")
    
    @validator('progress_percentage')
    def validate_progress(cls, v):
        return round(v, 2)  # Round to 2 decimal places
```

### Using Structured Outputs in Multi-Agent Systems

```python
class TaskManagementState(MultiAgentState):
    # Input
    task_description: str = ""
    requirements: List[str] = Field(default_factory=list)
    
    # Analysis agent outputs
    task_complexity: int = 0
    estimated_hours: float = 0.0
    priority: str = ""
    required_skills: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    
    # Planning agent outputs
    planned_steps: List[str] = Field(default_factory=list)
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    timeline: Dict[str, str] = Field(default_factory=dict)
    resource_allocation: Dict[str, float] = Field(default_factory=dict)
    
    # Execution agent outputs
    status: str = ""
    completed_steps: List[str] = Field(default_factory=list)
    current_step: Optional[str] = None
    blockers: List[str] = Field(default_factory=list)
    progress_percentage: float = 0.0

# Create agents with structured outputs
analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(
        system_message="Analyze tasks for complexity, time, and requirements."
    ),
    structured_output_model=TaskAnalysis
)

planner = SimpleAgent(
    name="planner", 
    engine=AugLLMConfig(
        system_message="Create detailed execution plans based on task analysis."
    ),
    structured_output_model=TaskPlan
)

executor = SimpleAgent(
    name="executor",
    engine=AugLLMConfig(
        system_message="Track task execution and progress."
    ),
    structured_output_model=TaskExecution
)
```

### 🎯 Exercise 4: Design Structured Outputs

Design structured outputs for a content creation workflow:
1. **Content Planner**: Plans content strategy
2. **Writer**: Creates the content
3. **Editor**: Reviews and refines content

What fields would each agent need? What validations would you add?

## ⚡ Section 5: Parallel Processing

Sometimes you need multiple agents working on the same input simultaneously.

### The Pattern

```python
import asyncio

# Create multiple nodes
node_a = create_agent_node_v3("agent_a")
node_b = create_agent_node_v3("agent_b")
node_c = create_agent_node_v3("agent_c")

# Execute in parallel
async def parallel_execution():
    tasks = [
        node_a(state, config),
        node_b(state, config),
        node_c(state, config)
    ]
    results = await asyncio.gather(*tasks)
    return results

# Run parallel execution
results = asyncio.run(parallel_execution())
```

### Real Example: Multi-Perspective Analysis

```python
from typing import List, Dict, Any
import asyncio

# Define outputs for each perspective
class TechnicalAnalysis(BaseModel):
    technical_feasibility: float = Field(ge=0.0, le=1.0)
    complexity_score: int = Field(ge=1, le=10)
    technical_risks: List[str]
    required_technologies: List[str]

class BusinessAnalysis(BaseModel):
    business_value: float = Field(ge=0.0, le=1.0)
    market_potential: str
    revenue_impact: str
    business_risks: List[str]

class UserAnalysis(BaseModel):
    user_impact: float = Field(ge=0.0, le=1.0)
    usability_score: int = Field(ge=1, le=10)
    user_concerns: List[str]
    accessibility_notes: List[str]

# Multi-perspective state
class MultiPerspectiveState(MultiAgentState):
    # Input
    feature_description: str = ""
    
    # Technical perspective
    technical_feasibility: float = 0.0
    complexity_score: int = 0
    technical_risks: List[str] = Field(default_factory=list)
    required_technologies: List[str] = Field(default_factory=list)
    
    # Business perspective
    business_value: float = 0.0
    market_potential: str = ""
    revenue_impact: str = ""
    business_risks: List[str] = Field(default_factory=list)
    
    # User perspective
    user_impact: float = 0.0
    usability_score: int = 0
    user_concerns: List[str] = Field(default_factory=list)
    accessibility_notes: List[str] = Field(default_factory=list)

# Create perspective agents
tech_analyst = SimpleAgent(
    name="tech_analyst",
    engine=AugLLMConfig(
        system_message="Analyze from a technical perspective: feasibility, complexity, risks."
    ),
    structured_output_model=TechnicalAnalysis
)

business_analyst = SimpleAgent(
    name="business_analyst",
    engine=AugLLMConfig(
        system_message="Analyze from a business perspective: value, market, revenue."
    ),
    structured_output_model=BusinessAnalysis
)

user_analyst = SimpleAgent(
    name="user_analyst",
    engine=AugLLMConfig(
        system_message="Analyze from a user perspective: impact, usability, concerns."
    ),
    structured_output_model=UserAnalysis
)

# Parallel analysis workflow
async def run_parallel_analysis(feature_description: str):
    # Initialize state
    state = MultiPerspectiveState(
        agents=[tech_analyst, business_analyst, user_analyst],
        feature_description=feature_description
    )
    
    # Create nodes
    tech_node = create_agent_node_v3("tech_analyst")
    business_node = create_agent_node_v3("business_analyst")
    user_node = create_agent_node_v3("user_analyst")
    
    config = {"configurable": {"thread_id": "parallel_analysis"}}
    
    print("🔄 Starting Parallel Analysis")
    print(f"Feature: {feature_description}")
    print("-" * 50)
    
    # Execute all analyses in parallel
    start_time = asyncio.get_event_loop().time()
    
    tasks = [
        tech_node(state, config),
        business_node(state, config),
        user_node(state, config)
    ]
    
    results = await asyncio.gather(*tasks)
    
    end_time = asyncio.get_event_loop().time()
    
    print(f"✅ All analyses completed in {end_time - start_time:.2f} seconds")
    print(f"Technical Feasibility: {state.technical_feasibility:.2f}")
    print(f"Business Value: {state.business_value:.2f}")
    print(f"User Impact: {state.user_impact:.2f}")
    
    return state

# Example usage
if __name__ == "__main__":
    feature = "AI-powered code completion in our IDE"
    result = asyncio.run(run_parallel_analysis(feature))
    
    # Show combined results
    print("\n📊 Combined Analysis Results:")
    print(f"Technical Risks: {result.technical_risks}")
    print(f"Business Risks: {result.business_risks}")
    print(f"User Concerns: {result.user_concerns}")
```

### 🎯 Exercise 5: Build Parallel Processing

Create a parallel processing system for content analysis:
1. **SEO Analyzer**: Analyzes SEO potential
2. **Readability Analyzer**: Analyzes readability
3. **Sentiment Analyzer**: Analyzes sentiment

How would you structure the state? What would each agent analyze?

## 🔄 Section 6: Dynamic Composition

Sometimes you need to add agents at runtime based on conditions.

### The Pattern

```python
# Start with basic agents
initial_agents = [agent_a, agent_b]
state = MultiAgentState(agents=initial_agents)

# Add agents dynamically
if condition:
    new_agent = SimpleAgent(name="specialist", engine=config)
    state.agents["specialist"] = new_agent
    
    # Mark for recompilation if needed
    state.mark_agent_for_recompile("specialist", "Added specialist agent")
```

### Real Example: Adaptive Content Pipeline

```python
from typing import List, Dict, Any, Optional

class AdaptiveContentState(MultiAgentState):
    # Input
    content_type: str = ""  # "blog", "email", "social", "technical"
    content_text: str = ""
    target_audience: str = ""
    
    # Base analysis (always done)
    basic_analysis: str = ""
    word_count: int = 0
    
    # Specialized analysis (conditional)
    seo_analysis: str = ""
    technical_review: str = ""
    social_optimization: str = ""
    
    # Final output
    recommendations: List[str] = Field(default_factory=list)
    final_score: float = 0.0

# Base agents (always present)
base_analyzer = SimpleAgent(
    name="base_analyzer",
    engine=AugLLMConfig(
        system_message="Perform basic content analysis: structure, clarity, word count."
    ),
    structured_output_model=BasicAnalysis
)

# Specialized agents (added conditionally)
seo_specialist = SimpleAgent(
    name="seo_specialist",
    engine=AugLLMConfig(
        system_message="Analyze content for SEO: keywords, meta descriptions, readability."
    ),
    structured_output_model=SEOAnalysis
)

technical_reviewer = SimpleAgent(
    name="technical_reviewer",
    engine=AugLLMConfig(
        system_message="Review technical content: accuracy, clarity, completeness."
    ),
    structured_output_model=TechnicalReview
)

social_optimizer = SimpleAgent(
    name="social_optimizer",
    engine=AugLLMConfig(
        system_message="Optimize content for social media: engagement, hashtags, formatting."
    ),
    structured_output_model=SocialOptimization
)

def create_adaptive_pipeline(content_type: str, content_text: str, target_audience: str):
    """Create a content pipeline that adapts based on content type."""
    
    # Start with base agents
    agents = [base_analyzer]
    
    # Add specialized agents based on content type
    if content_type in ["blog", "article"]:
        agents.append(seo_specialist)
        print("🔍 Added SEO specialist for blog content")
    
    if content_type == "technical":
        agents.append(technical_reviewer)
        print("🔧 Added technical reviewer for technical content")
    
    if content_type in ["social", "email"]:
        agents.append(social_optimizer)
        print("📱 Added social optimizer for social/email content")
    
    # Create state with selected agents
    state = AdaptiveContentState(
        agents=agents,
        content_type=content_type,
        content_text=content_text,
        target_audience=target_audience
    )
    
    return state

def run_adaptive_pipeline(content_type: str, content_text: str, target_audience: str):
    """Run the adaptive content pipeline."""
    
    state = create_adaptive_pipeline(content_type, content_text, target_audience)
    
    print(f"🚀 Running adaptive pipeline for {content_type} content")
    print(f"Selected agents: {[agent.name for agent in state.agents]}")
    print("-" * 50)
    
    # Execute all agents
    config = {"configurable": {"thread_id": "adaptive_pipeline"}}
    
    for agent in state.agents:
        node = create_agent_node_v3(agent.name)
        result = node(state, config)
        print(f"✅ Completed {agent.name}")
    
    return state

# Example usage
if __name__ == "__main__":
    # Test with different content types
    test_cases = [
        ("blog", "How to build multi-agent systems...", "developers"),
        ("technical", "API documentation for...", "technical_users"),
        ("social", "Check out our new feature!", "general_public")
    ]
    
    for content_type, content_text, audience in test_cases:
        print(f"\n{'='*60}")
        result = run_adaptive_pipeline(content_type, content_text, audience)
        print(f"Final recommendations: {result.recommendations}")
```

### 🎯 Exercise 6: Build Dynamic Composition

Create a dynamic analysis system that adds agents based on:
- **Data type**: Add specialists for text, image, or numerical data
- **Complexity**: Add extra reviewers for complex analyses
- **Domain**: Add domain experts for specific fields

How would you decide which agents to add?

## 🧠 Section 7: Self-Discover Patterns

Self-Discover is an advanced pattern where agents build on each other's reasoning progressively.

### The Pattern

```python
# Agent A discovers something
# Agent B adapts that discovery to the specific context
# Agent C creates a complete solution based on both

# Each agent builds on the previous agent's output
result1 = agent_a_node(state, config)  # Discovers
result2 = agent_b_node(state, config)  # Adapts (reads Agent A's output)
result3 = agent_c_node(state, config)  # Solves (reads both previous outputs)
```

### Real Example: Problem-Solving Pipeline

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Self-Discover output models
class ProblemAnalysis(BaseModel):
    problem_type: str = Field(description="Type of problem identified")
    core_issues: List[str] = Field(description="Core issues identified")
    stakeholders: List[str] = Field(description="Key stakeholders involved")
    constraints: List[str] = Field(description="Constraints and limitations")
    success_criteria: List[str] = Field(description="What success looks like")

class SolutionApproaches(BaseModel):
    potential_solutions: List[Dict[str, str]] = Field(description="Potential solution approaches")
    evaluation_criteria: List[str] = Field(description="Criteria for evaluating solutions")
    recommended_approach: str = Field(description="Recommended approach")
    implementation_complexity: str = Field(description="Implementation complexity assessment")

class ActionPlan(BaseModel):
    action_steps: List[str] = Field(description="Specific action steps")
    timeline: Dict[str, str] = Field(description="Timeline for each phase")
    resource_requirements: List[str] = Field(description="Required resources")
    risk_mitigation: List[str] = Field(description="Risk mitigation strategies")
    success_metrics: List[str] = Field(description="How to measure success")

# Self-Discover state
class SelfDiscoverState(MultiAgentState):
    # Input
    problem_description: str = ""
    context: str = ""
    
    # Problem analyzer outputs
    problem_type: str = ""
    core_issues: List[str] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    
    # Solution strategist outputs
    potential_solutions: List[Dict[str, str]] = Field(default_factory=list)
    evaluation_criteria: List[str] = Field(default_factory=list)
    recommended_approach: str = ""
    implementation_complexity: str = ""
    
    # Action planner outputs
    action_steps: List[str] = Field(default_factory=list)
    timeline: Dict[str, str] = Field(default_factory=dict)
    resource_requirements: List[str] = Field(default_factory=list)
    risk_mitigation: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)

# Create Self-Discover agents
problem_analyzer = SimpleAgent(
    name="problem_analyzer",
    engine=AugLLMConfig(
        temperature=0.2,
        system_message="""You are a problem analysis specialist.
        
        Your job is to deeply understand problems by:
        1. Identifying the core issues
        2. Understanding stakeholders
        3. Recognizing constraints
        4. Defining success criteria
        
        Be thorough and systematic in your analysis."""
    ),
    structured_output_model=ProblemAnalysis
)

solution_strategist = SimpleAgent(
    name="solution_strategist",
    engine=AugLLMConfig(
        temperature=0.4,
        system_message="""You are a solution strategy specialist.
        
        Based on the problem analysis, your job is to:
        1. Generate multiple solution approaches
        2. Evaluate each approach
        3. Recommend the best approach
        4. Assess implementation complexity
        
        Consider the identified constraints and stakeholders."""
    ),
    structured_output_model=SolutionApproaches
)

action_planner = SimpleAgent(
    name="action_planner",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="""You are an action planning specialist.
        
        Based on the problem analysis and recommended solution, create:
        1. Specific, actionable steps
        2. Realistic timeline
        3. Resource requirements
        4. Risk mitigation strategies
        5. Success metrics
        
        Make the plan practical and executable."""
    ),
    structured_output_model=ActionPlan
)

def run_self_discover_workflow(problem_description: str, context: str = ""):
    """Run the Self-Discover problem-solving workflow."""
    
    # Initialize state
    state = SelfDiscoverState(
        agents=[problem_analyzer, solution_strategist, action_planner],
        problem_description=problem_description,
        context=context
    )
    
    # Create nodes
    analyzer_node = create_agent_node_v3("problem_analyzer")
    strategist_node = create_agent_node_v3("solution_strategist")
    planner_node = create_agent_node_v3("action_planner")
    
    config = {"configurable": {"thread_id": "self_discover"}}
    
    print("🧠 Starting Self-Discover Problem-Solving")
    print(f"Problem: {problem_description}")
    print("=" * 60)
    
    # Step 1: Problem Analysis
    print("🔍 Step 1: Problem Analysis")
    result1 = analyzer_node(state, config)
    print(f"   Problem type: {state.problem_type}")
    print(f"   Core issues: {len(state.core_issues)}")
    print(f"   Stakeholders: {state.stakeholders}")
    print(f"   Constraints: {len(state.constraints)}")
    
    # Step 2: Solution Strategy (builds on Step 1)
    print(f"\n💡 Step 2: Solution Strategy")
    result2 = strategist_node(state, config)
    print(f"   Potential solutions: {len(state.potential_solutions)}")
    print(f"   Recommended approach: {state.recommended_approach}")
    print(f"   Implementation complexity: {state.implementation_complexity}")
    
    # Step 3: Action Planning (builds on Steps 1 & 2)
    print(f"\n📋 Step 3: Action Planning")
    result3 = planner_node(state, config)
    print(f"   Action steps: {len(state.action_steps)}")
    print(f"   Timeline phases: {len(state.timeline)}")
    print(f"   Resource requirements: {len(state.resource_requirements)}")
    
    print(f"\n🎯 Self-Discover Complete!")
    print(f"Final action plan: {state.action_steps}")
    
    return state

# Example usage
if __name__ == "__main__":
    problem = """
    Our customer support team is overwhelmed with tickets.
    Response times have increased from 2 hours to 8 hours.
    Customer satisfaction scores are dropping.
    The team is working overtime but still can't keep up.
    """
    
    result = run_self_discover_workflow(problem)
    
    print("\n" + "=" * 60)
    print("🔍 Self-Discover Pattern Benefits:")
    print("1. Each agent builds on previous reasoning")
    print("2. Progressive refinement of understanding")
    print("3. Comprehensive problem-solving approach")
    print("4. Direct field access for clean communication")
    
    # Show how each agent used previous outputs
    print(f"\n📊 Information Flow:")
    print(f"Problem Analysis → Core Issues: {len(result.core_issues)}")
    print(f"Solution Strategy → Used Core Issues: {result.recommended_approach}")
    print(f"Action Planning → Used Strategy: {len(result.action_steps)} steps")
```

### 🎯 Exercise 7: Build Self-Discover

Create a Self-Discover system for content creation:
1. **Content Strategist**: Analyzes content needs and strategy
2. **Content Creator**: Creates content based on strategy
3. **Content Optimizer**: Optimizes based on creation results

How would each agent build on the previous agent's work?

## 🏗️ Section 8: Hierarchical Systems

Sometimes you need agents that coordinate other agents.

### The Pattern

```python
# Supervisor agent coordinates worker agents
supervisor = SimpleAgent(name="supervisor", ...)
worker_1 = SimpleAgent(name="worker_1", ...)
worker_2 = SimpleAgent(name="worker_2", ...)

# Supervisor decides which workers to use
supervisor_result = supervisor_node(state, config)
# Based on supervisor's decision, execute specific workers
if state.use_worker_1:
    worker_1_result = worker_1_node(state, config)
if state.use_worker_2:
    worker_2_result = worker_2_node(state, config)
```

### Real Example: Content Production System

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Supervisor output
class ContentStrategy(BaseModel):
    content_type: str = Field(description="Type of content to create")
    primary_focus: str = Field(description="Primary focus area")
    required_specialists: List[str] = Field(description="Which specialists are needed")
    content_outline: List[str] = Field(description="Content outline")
    quality_requirements: List[str] = Field(description="Quality requirements")

# Specialist outputs
class ResearchOutput(BaseModel):
    research_findings: List[str] = Field(description="Key research findings")
    sources: List[str] = Field(description="Source references")
    key_statistics: List[str] = Field(description="Important statistics")

class WritingOutput(BaseModel):
    content_draft: str = Field(description="Content draft")
    key_points_covered: List[str] = Field(description="Key points addressed")
    word_count: int = Field(description="Word count")

class EditingOutput(BaseModel):
    edited_content: str = Field(description="Edited content")
    improvements_made: List[str] = Field(description="Improvements made")
    final_quality_score: float = Field(ge=0.0, le=10.0, description="Quality score")

# Hierarchical state
class HierarchicalContentState(MultiAgentState):
    # Input
    content_request: str = ""
    target_audience: str = ""
    deadline: str = ""
    
    # Supervisor outputs
    content_type: str = ""
    primary_focus: str = ""
    required_specialists: List[str] = Field(default_factory=list)
    content_outline: List[str] = Field(default_factory=list)
    quality_requirements: List[str] = Field(default_factory=list)
    
    # Research specialist outputs
    research_findings: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    key_statistics: List[str] = Field(default_factory=list)
    
    # Writing specialist outputs
    content_draft: str = ""
    key_points_covered: List[str] = Field(default_factory=list)
    word_count: int = 0
    
    # Editing specialist outputs
    edited_content: str = ""
    improvements_made: List[str] = Field(default_factory=list)
    final_quality_score: float = 0.0

# Create hierarchical agents
content_supervisor = SimpleAgent(
    name="content_supervisor",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="""You are a content production supervisor.
        
        Your job is to:
        1. Analyze content requests
        2. Determine what type of content is needed
        3. Decide which specialists are required
        4. Create a content outline
        5. Set quality requirements
        
        Be strategic and consider the target audience and deadline."""
    ),
    structured_output_model=ContentStrategy
)

research_specialist = SimpleAgent(
    name="research_specialist",
    engine=AugLLMConfig(
        temperature=0.2,
        system_message="""You are a research specialist.
        
        Based on the content outline and requirements, provide:
        1. Relevant research findings
        2. Credible sources
        3. Key statistics and data
        
        Focus on accuracy and relevance."""
    ),
    structured_output_model=ResearchOutput
)

writing_specialist = SimpleAgent(
    name="writing_specialist",
    engine=AugLLMConfig(
        temperature=0.6,
        system_message="""You are a writing specialist.
        
        Based on the research and content outline, create:
        1. Engaging content draft
        2. Cover all key points
        3. Match the target audience
        
        Focus on clarity and engagement."""
    ),
    structured_output_model=WritingOutput
)

editing_specialist = SimpleAgent(
    name="editing_specialist",
    engine=AugLLMConfig(
        temperature=0.4,
        system_message="""You are an editing specialist.
        
        Review and improve the content draft:
        1. Fix grammar and style issues
        2. Improve clarity and flow
        3. Ensure quality requirements are met
        4. Provide quality score
        
        Focus on polish and professionalism."""
    ),
    structured_output_model=EditingOutput
)

def run_hierarchical_content_system(content_request: str, target_audience: str, deadline: str):
    """Run the hierarchical content production system."""
    
    # Initialize state with all agents
    state = HierarchicalContentState(
        agents=[content_supervisor, research_specialist, writing_specialist, editing_specialist],
        content_request=content_request,
        target_audience=target_audience,
        deadline=deadline
    )
    
    # Create nodes
    supervisor_node = create_agent_node_v3("content_supervisor")
    research_node = create_agent_node_v3("research_specialist")
    writing_node = create_agent_node_v3("writing_specialist")
    editing_node = create_agent_node_v3("editing_specialist")
    
    config = {"configurable": {"thread_id": "hierarchical_content"}}
    
    print("🏗️ Starting Hierarchical Content Production")
    print(f"Request: {content_request}")
    print(f"Audience: {target_audience}")
    print(f"Deadline: {deadline}")
    print("=" * 60)
    
    # Step 1: Supervisor Planning
    print("👔 Step 1: Supervisor Planning")
    supervisor_result = supervisor_node(state, config)
    print(f"   Content type: {state.content_type}")
    print(f"   Primary focus: {state.primary_focus}")
    print(f"   Required specialists: {state.required_specialists}")
    print(f"   Outline sections: {len(state.content_outline)}")
    
    # Step 2: Execute specialists based on supervisor's decision
    if "research_specialist" in state.required_specialists:
        print(f"\n🔍 Step 2a: Research Phase")
        research_result = research_node(state, config)
        print(f"   Research findings: {len(state.research_findings)}")
        print(f"   Sources: {len(state.sources)}")
    
    if "writing_specialist" in state.required_specialists:
        print(f"\n✏️ Step 2b: Writing Phase")
        writing_result = writing_node(state, config)
        print(f"   Content draft: {len(state.content_draft)} characters")
        print(f"   Word count: {state.word_count}")
    
    if "editing_specialist" in state.required_specialists:
        print(f"\n📝 Step 2c: Editing Phase")
        editing_result = editing_node(state, config)
        print(f"   Improvements made: {len(state.improvements_made)}")
        print(f"   Final quality score: {state.final_quality_score}/10")
    
    print(f"\n🎯 Hierarchical Production Complete!")
    print(f"Final content length: {len(state.edited_content)} characters")
    
    return state

# Example usage
if __name__ == "__main__":
    content_request = """
    Create a comprehensive guide on implementing AI chatbots for customer service.
    Should cover technical implementation, best practices, and ROI analysis.
    """
    
    result = run_hierarchical_content_system(
        content_request=content_request,
        target_audience="Technical decision makers",
        deadline="2 weeks"
    )
    
    print("\n" + "=" * 60)
    print("🏗️ Hierarchical System Benefits:")
    print("1. Supervisor coordinates the overall strategy")
    print("2. Specialists focus on their expertise")
    print("3. Dynamic specialist selection based on needs")
    print("4. Clear delegation and coordination")
    
    # Show the hierarchy in action
    print(f"\n📊 Coordination Results:")
    print(f"Supervisor decided on: {result.content_type}")
    print(f"Required specialists: {result.required_specialists}")
    print(f"Final quality score: {result.final_quality_score}/10")
```

### 🎯 Exercise 8: Build Hierarchical System

Create a hierarchical system for project management:
1. **Project Manager**: Coordinates overall project
2. **Task Analyzer**: Analyzes individual tasks
3. **Resource Planner**: Plans resource allocation
4. **Risk Assessor**: Evaluates project risks

How would the Project Manager coordinate the specialists?

## 🛡️ Section 9: Error Handling

Real multi-agent systems need robust error handling.

### The Pattern

```python
try:
    result = agent_node(state, config)
    
    # Validate results
    if not result.get("success", False):
        handle_agent_failure(agent_name, result)
    
    # Apply updates safely
    update_state_safely(state, result)
    
except AgentExecutionError as e:
    logger.error(f"Agent execution failed: {e}")
    handle_agent_error(agent_name, e)
    
except ValidationError as e:
    logger.error(f"State validation failed: {e}")
    handle_validation_error(state, e)
```

### Real Example: Robust Multi-Agent System

```python
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentExecutionError(Exception):
    """Custom exception for agent execution failures."""
    pass

class RobustAnalysisState(MultiAgentState):
    # Input
    input_data: str = ""
    
    # Analysis outputs
    analysis_results: List[str] = Field(default_factory=list)
    analysis_confidence: float = 0.0
    
    # Validation outputs
    validation_results: List[str] = Field(default_factory=list)
    validation_passed: bool = False
    
    # Summary outputs
    final_summary: str = ""
    overall_confidence: float = 0.0
    
    # Error tracking
    failed_agents: List[str] = Field(default_factory=list)
    error_messages: List[str] = Field(default_factory=list)
    recovery_actions: List[str] = Field(default_factory=list)

def execute_agent_safely(agent_name: str, state: RobustAnalysisState, config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an agent with comprehensive error handling."""
    
    try:
        logger.info(f"Executing agent: {agent_name}")
        
        # Create and execute node
        node = create_agent_node_v3(agent_name)
        result = node(state, config)
        
        # Validate result structure
        if not isinstance(result, dict):
            raise AgentExecutionError(f"Agent {agent_name} returned invalid result type")
        
        if not result.get("success", False):
            raise AgentExecutionError(f"Agent {agent_name} reported failure: {result.get('error', 'Unknown error')}")
        
        logger.info(f"Agent {agent_name} executed successfully")
        return result
        
    except ValidationError as e:
        error_msg = f"Validation error in agent {agent_name}: {e}"
        logger.error(error_msg)
        state.failed_agents.append(agent_name)
        state.error_messages.append(error_msg)
        raise AgentExecutionError(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error in agent {agent_name}: {e}"
        logger.error(error_msg)
        state.failed_agents.append(agent_name)
        state.error_messages.append(error_msg)
        raise AgentExecutionError(error_msg)

def recover_from_agent_failure(agent_name: str, state: RobustAnalysisState, error: AgentExecutionError):
    """Attempt to recover from agent failure."""
    
    logger.info(f"Attempting recovery for failed agent: {agent_name}")
    
    if agent_name == "analyzer":
        # Try with simplified analysis
        state.analysis_results.append("Simplified analysis due to error")
        state.analysis_confidence = 0.3
        state.recovery_actions.append("Used simplified analysis")
        return True
        
    elif agent_name == "validator":
        # Skip validation and proceed
        state.validation_results.append("Validation skipped due to error")
        state.validation_passed = False
        state.recovery_actions.append("Skipped validation")
        return True
        
    elif agent_name == "summarizer":
        # Create basic summary
        state.final_summary = "Basic summary due to error"
        state.overall_confidence = 0.2
        state.recovery_actions.append("Used basic summary")
        return True
    
    return False

def run_robust_multi_agent_system(input_data: str):
    """Run a multi-agent system with comprehensive error handling."""
    
    # Create agents (simplified for example)
    analyzer = SimpleAgent(name="analyzer", engine=AugLLMConfig())
    validator = SimpleAgent(name="validator", engine=AugLLMConfig())
    summarizer = SimpleAgent(name="summarizer", engine=AugLLMConfig())
    
    # Initialize state
    state = RobustAnalysisState(
        agents=[analyzer, validator, summarizer],
        input_data=input_data
    )
    
    config = {"configurable": {"thread_id": "robust_system"}}
    
    print("🛡️ Starting Robust Multi-Agent System")
    print(f"Input: {input_data}")
    print("=" * 60)
    
    # Execute agents with error handling
    agents_to_run = ["analyzer", "validator", "summarizer"]
    
    for agent_name in agents_to_run:
        try:
            print(f"\n🔄 Executing {agent_name}...")
            
            result = execute_agent_safely(agent_name, state, config)
            
            print(f"✅ {agent_name} completed successfully")
            
        except AgentExecutionError as e:
            print(f"❌ {agent_name} failed: {e}")
            
            # Attempt recovery
            if recover_from_agent_failure(agent_name, state, e):
                print(f"🔧 Recovery successful for {agent_name}")
            else:
                print(f"💥 Recovery failed for {agent_name}")
                
                # Decide whether to continue or abort
                if agent_name == "analyzer":
                    print("🛑 Critical agent failed, aborting workflow")
                    break
                else:
                    print("⚠️ Non-critical agent failed, continuing workflow")
    
    # Generate final report
    print(f"\n📊 Final System Report:")
    print(f"   Failed agents: {len(state.failed_agents)}")
    print(f"   Error messages: {len(state.error_messages)}")
    print(f"   Recovery actions: {len(state.recovery_actions)}")
    print(f"   Overall confidence: {state.overall_confidence}")
    
    if state.failed_agents:
        print(f"\n⚠️ System completed with errors:")
        for agent, error in zip(state.failed_agents, state.error_messages):
            print(f"   - {agent}: {error}")
        
        print(f"\n🔧 Recovery actions taken:")
        for action in state.recovery_actions:
            print(f"   - {action}")
    else:
        print(f"\n✅ System completed successfully!")
    
    return state

# Example usage with error simulation
if __name__ == "__main__":
    # Test with normal input
    print("=== Testing Normal Operation ===")
    result = run_robust_multi_agent_system("Analyze customer feedback data")
    
    # Test with error simulation (you would need to modify agents to simulate errors)
    print(f"\n=== Testing Error Handling ===")
    # This would require modifying the agents to simulate failures
    # For demonstration purposes only
    
    print("\n" + "=" * 60)
    print("🛡️ Error Handling Benefits:")
    print("1. Graceful degradation instead of complete failure")
    print("2. Detailed error logging and tracking")
    print("3. Recovery mechanisms for non-critical failures")
    print("4. Clear reporting of system health")
```

### 🎯 Exercise 9: Build Error Handling

Add error handling to one of your previous multi-agent systems:
1. **Identify critical vs non-critical agents**
2. **Create recovery strategies for each agent**
3. **Add error logging and reporting**
4. **Test with simulated failures**

How would you handle different types of failures?

## 🎯 Final Exercise: Build Your Own Multi-Agent System

Now that you've learned all the patterns, build a complete multi-agent system of your choice.

### Suggestions

1. **Content Marketing Pipeline**
   - Research trends → Create content → Optimize for SEO → Schedule posting

2. **Customer Support System**
   - Categorize tickets → Route to specialists → Generate responses → Quality check

3. **Data Analysis Workflow**
   - Collect data → Clean and validate → Analyze patterns → Generate insights

4. **Product Development Pipeline**
   - Analyze requirements → Design solution → Review feasibility → Create roadmap

### Requirements

1. **At least 3 agents** working together
2. **Structured outputs** for clean communication
3. **Error handling** for robustness
4. **One advanced pattern** (Self-Discover, Parallel, or Hierarchical)
5. **Real working code** that can be executed

### Template

```python
# Your multi-agent system
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3

# Define your output models
class Agent1Output(BaseModel):
    # Your fields here
    pass

class Agent2Output(BaseModel):
    # Your fields here
    pass

class Agent3Output(BaseModel):
    # Your fields here
    pass

# Define your state
class YourSystemState(MultiAgentState):
    # Input fields
    input_field: str = ""
    
    # Agent 1 outputs
    # Your fields here
    
    # Agent 2 outputs
    # Your fields here
    
    # Agent 3 outputs
    # Your fields here

# Create your agents
agent1 = SimpleAgent(
    name="agent1",
    engine=AugLLMConfig(system_message="Your system message"),
    structured_output_model=Agent1Output
)

# ... create other agents

def run_your_system(input_data: str):
    """Run your multi-agent system."""
    
    # Initialize state
    state = YourSystemState(
        agents=[agent1, agent2, agent3],
        input_field=input_data
    )
    
    # Create nodes
    node1 = create_agent_node_v3("agent1")
    node2 = create_agent_node_v3("agent2")
    node3 = create_agent_node_v3("agent3")
    
    config = {"configurable": {"thread_id": "your_system"}}
    
    # Execute your workflow
    # Your implementation here
    
    return state

# Test your system
if __name__ == "__main__":
    result = run_your_system("Your test input")
    print(f"Results: {result}")
```

## 🎉 Congratulations!

You've completed the comprehensive multi-agent systems guide! You now know:

1. **Two-Agent Communication** - Basic agent-to-agent communication
2. **State Design Patterns** - How to structure multi-agent state
3. **Sequential Workflows** - Agent A → Agent B → Agent C
4. **Structured Outputs** - Type-safe agent communication
5. **Parallel Processing** - Multiple agents working simultaneously
6. **Dynamic Composition** - Adding agents at runtime
7. **Self-Discover Patterns** - Agents building on each other's reasoning
8. **Hierarchical Systems** - Multi-level agent coordination
9. **Error Handling** - Robust multi-agent systems

### 🚀 Next Steps

1. **Build your own system** using the patterns you've learned
2. **Experiment with combinations** - Mix different patterns
3. **Add more sophisticated error handling** and recovery
4. **Create domain-specific agents** for your use cases
5. **Share your implementations** and learn from others

### 📚 Additional Resources

- **Multi-Agent Architecture**: `project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md`
- **Testing Philosophy**: `project_docs/active/standards/testing/philosophy.md`
- **Working Examples**: `packages/haive-core/tests/node/test_self_discover_workflow.py`

---

**Remember**: Multi-agent systems are about **coordination and communication**. Start simple, build incrementally, and always test with real components. The patterns you've learned here will serve as building blocks for any multi-agent system you create.

**Happy building!** 🎯