# Haive Agent Patterns - Complete Guide

This comprehensive guide documents all the patterns available in the Haive Agent Framework, from basic agent patterns to advanced multi-agent orchestration strategies.

## Table of Contents

- [Introduction](#introduction)
- [Core Agent Patterns](#core-agent-patterns)
  - [Basic Agent Pattern](#basic-agent-pattern)
  - [Agent with Tools Pattern](#agent-with-tools-pattern)
  - [Structured Output Pattern](#structured-output-pattern)
  - [Hooks and Lifecycle Pattern](#hooks-and-lifecycle-pattern)
- [ReAct Patterns](#react-patterns)
  - [Basic ReAct Pattern](#basic-react-pattern)
  - [Research Agent Pattern](#research-agent-pattern)
  - [Multi-Tool Reasoning Pattern](#multi-tool-reasoning-pattern)
- [Multi-Agent Patterns](#multi-agent-patterns)
  - [Sequential Pipeline Pattern](#sequential-pipeline-pattern)
  - [Parallel Processing Pattern](#parallel-processing-pattern)
  - [Conditional Routing Pattern](#conditional-routing-pattern)
  - [Hierarchical Coordination Pattern](#hierarchical-coordination-pattern)
- [Advanced Patterns](#advanced-patterns)
  - [Agent-as-Tool Pattern](#agent-as-tool-pattern)
  - [Self-Discover Pattern](#self-discover-pattern)
  - [Dynamic Recompilation Pattern](#dynamic-recompilation-pattern)
  - [Meta-Agent Pattern](#meta-agent-pattern)
- [Specialized Patterns](#specialized-patterns)
  - [RAG Agent Pattern](#rag-agent-pattern)
  - [Reflection Pattern](#reflection-pattern)
  - [Planning and Execution Pattern](#planning-and-execution-pattern)
  - [Supervisor Pattern](#supervisor-pattern)
- [Production Patterns](#production-patterns)
  - [Error Recovery Pattern](#error-recovery-pattern)
  - [Performance Optimization Pattern](#performance-optimization-pattern)
  - [Monitoring and Observability Pattern](#monitoring-and-observability-pattern)
- [Best Practices](#best-practices)

## Introduction

Haive provides a rich set of patterns for building AI agents, from simple conversational agents to complex multi-agent systems. These patterns are designed to be:

- **Composable**: Patterns can be combined for complex behaviors
- **Type-Safe**: Full Pydantic validation and type hints
- **Production-Ready**: Built-in error handling and monitoring
- **Extensible**: Easy to customize and extend

## Core Agent Patterns

### Basic Agent Pattern

The foundational pattern for creating a simple conversational agent.

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# Pattern: Basic conversational agent
def create_basic_agent(name: str, system_message: str) -> SimpleAgentV3:
    """Create a basic conversational agent."""
    return SimpleAgentV3(
        name=name,
        engine=AugLLMConfig(
            temperature=0.7,
            max_tokens=500,
            system_message=system_message
        ),
        debug=True  # Enable comprehensive logging
    )

# Usage
assistant = create_basic_agent(
    name="helpful_assistant",
    system_message="You are a helpful AI assistant"
)

response = assistant.run("How can I learn Python?")
```

### Agent with Tools Pattern

Enhance agents with tool-calling capabilities for extended functionality.

```python
from langchain_core.tools import tool
from typing import List

# Pattern: Agent with multiple tools
class TooledAgent:
    """Pattern for creating agents with tool capabilities."""

    @staticmethod
    def create_with_tools(
        name: str,
        tools: List,
        system_message: str = None
    ) -> SimpleAgentV3:
        """Create an agent with tool capabilities."""
        return SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(
                tools=tools,
                system_message=system_message or "You are an assistant with access to tools",
                temperature=0.7,
                force_tool_use=False  # Let agent decide when to use tools
            )
        )

# Define tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Mock implementation
    return f"Search results for '{query}': [Information would be here]"

@tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create tooled agent
agent = TooledAgent.create_with_tools(
    name="research_assistant",
    tools=[calculator, web_search, get_current_time]
)

# Agent automatically uses tools when needed
result = agent.run("What's 15% of 2500 and what time is it now?")
```

### Structured Output Pattern

Ensure consistent, validated outputs using Pydantic models.

```python
from pydantic import BaseModel, Field
from typing import List, Optional

# Pattern: Structured output for consistent responses
class StructuredOutputPattern:
    """Pattern for agents with structured, validated outputs."""

    @staticmethod
    def create_analysis_agent(output_model: type[BaseModel]) -> SimpleAgentV3:
        """Create an agent that produces structured analysis."""
        return SimpleAgentV3(
            name="structured_analyzer",
            engine=AugLLMConfig(
                structured_output_model=output_model,
                temperature=0.3,  # Lower temperature for consistency
                system_message="You are an expert analyst. Provide thorough analysis."
            )
        )

# Define output models
class SentimentAnalysis(BaseModel):
    text: str = Field(description="The analyzed text")
    sentiment: str = Field(description="Overall sentiment: positive, negative, or neutral")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    key_phrases: List[str] = Field(description="Important phrases affecting sentiment")
    reasoning: str = Field(description="Explanation of the sentiment analysis")

class BusinessAnalysis(BaseModel):
    company: str = Field(description="Company being analyzed")
    strengths: List[str] = Field(description="Key strengths identified")
    weaknesses: List[str] = Field(description="Key weaknesses identified")
    opportunities: List[str] = Field(description="Potential opportunities")
    threats: List[str] = Field(description="Potential threats")
    recommendation: str = Field(description="Strategic recommendation")
    confidence: float = Field(ge=0.0, le=1.0)

# Create specialized analyzers
sentiment_analyzer = StructuredOutputPattern.create_analysis_agent(SentimentAnalysis)
business_analyzer = StructuredOutputPattern.create_analysis_agent(BusinessAnalysis)

# Get structured results
sentiment_result = sentiment_analyzer.run(
    "The new product launch was incredibly successful, exceeding all expectations!"
)
assert isinstance(sentiment_result, SentimentAnalysis)
print(f"Sentiment: {sentiment_result.sentiment} (confidence: {sentiment_result.confidence})")

business_result = business_analyzer.run(
    "Analyze Tesla's current market position"
)
assert isinstance(business_result, BusinessAnalysis)
```

### Hooks and Lifecycle Pattern

Monitor and control agent execution with lifecycle hooks.

```python
import logging
from datetime import datetime
from typing import Dict, Any

# Pattern: Comprehensive lifecycle monitoring
class MonitoredAgentPattern:
    """Pattern for agents with comprehensive monitoring."""

    @staticmethod
    def create_monitored_agent(
        name: str,
        enable_timing: bool = True,
        enable_logging: bool = True,
        enable_validation: bool = True
    ) -> SimpleAgentV3:
        """Create an agent with full lifecycle monitoring."""

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(temperature=0.7),
            debug=True,
            hooks_enabled=True
        )

        # Execution timing
        execution_times: Dict[str, float] = {}

        if enable_timing:
            @agent.before_run
            def start_timer(context):
                execution_times['start'] = datetime.now().timestamp()

            @agent.after_run
            def end_timer(context):
                execution_times['end'] = datetime.now().timestamp()
                duration = execution_times['end'] - execution_times['start']
                logging.info(f"Execution took {duration:.2f} seconds")

        if enable_logging:
            @agent.before_run
            def log_input(context):
                logging.info(f"Input: {context.input_data}")

            @agent.after_run
            def log_output(context):
                output_preview = str(context.output_data)[:200]
                logging.info(f"Output preview: {output_preview}...")

            @agent.on_error
            def log_error(context):
                logging.error(f"Error occurred: {context.error}")

        if enable_validation:
            @agent.before_run
            def validate_input(context):
                if not context.input_data:
                    raise ValueError("Input cannot be empty")

            @agent.after_run
            def validate_output(context):
                if not context.output_data:
                    logging.warning("Empty output generated")

        # State monitoring
        @agent.before_state_update
        def monitor_state_change(context):
            logging.debug(f"State update: {context.metadata}")

        # Graph building monitoring
        @agent.before_build_graph
        def monitor_graph_build(context):
            logging.info("Building agent graph...")

        @agent.after_build_graph
        def confirm_graph_built(context):
            logging.info("Graph successfully built")

        return agent

# Create fully monitored agent
monitored_agent = MonitoredAgentPattern.create_monitored_agent(
    name="monitored_assistant",
    enable_timing=True,
    enable_logging=True,
    enable_validation=True
)

# All lifecycle events are monitored
result = monitored_agent.run("Explain quantum computing")
```

## ReAct Patterns

### Basic ReAct Pattern

Implement reasoning and acting loops for complex problem-solving.

```python
from haive.agents.react.agent_v3 import ReactAgentV3, create_react_agent

# Pattern: Basic ReAct agent with reasoning loops
class ReActPattern:
    """Pattern for ReAct agents with iterative reasoning."""

    @staticmethod
    def create_problem_solver(
        name: str,
        tools: List,
        max_iterations: int = 5
    ) -> ReactAgentV3:
        """Create a ReAct agent for problem solving."""
        return ReactAgentV3(
            name=name,
            engine=AugLLMConfig(
                tools=tools,
                temperature=0.7,
                max_tokens=1000,
                system_message="You are a problem solver. Think step by step."
            ),
            max_iterations=max_iterations,
            stop_on_first_tool_result=False,  # Continue reasoning
            require_final_answer=True,  # Always provide conclusion
            debug=True
        )

# Create problem solver
problem_solver = ReActPattern.create_problem_solver(
    name="math_solver",
    tools=[calculator, web_search],
    max_iterations=6
)

# Solve complex problem with reasoning
result = problem_solver.run(
    "If a train travels 120 km in 1.5 hours, how long will it take to travel 200 km? "
    "Also, what's the world record for fastest train?"
)

# Access reasoning trace
reasoning_steps = problem_solver.get_reasoning_trace()
tool_history = problem_solver.get_tool_usage_history()
```

### Research Agent Pattern

Specialized ReAct pattern for research and information gathering.

```python
from typing import List, Dict

# Pattern: Research agent with structured findings
class ResearchPattern:
    """Pattern for comprehensive research agents."""

    class ResearchFindings(BaseModel):
        topic: str = Field(description="Research topic")
        questions_explored: List[str] = Field(description="Questions investigated")
        sources_consulted: List[str] = Field(description="Information sources used")
        key_findings: List[str] = Field(description="Important discoveries")
        data_points: Dict[str, Any] = Field(description="Specific data collected")
        conclusion: str = Field(description="Research conclusion")
        confidence: float = Field(ge=0.0, le=1.0)
        further_research: List[str] = Field(description="Areas for further investigation")

    @staticmethod
    def create_researcher(
        name: str,
        research_tools: List,
        max_research_depth: int = 8
    ) -> ReactAgentV3:
        """Create a specialized research agent."""
        return ReactAgentV3(
            name=name,
            engine=AugLLMConfig(
                tools=research_tools,
                structured_output_model=ResearchPattern.ResearchFindings,
                temperature=0.3,  # More focused for research
                max_tokens=1500,
                system_message=(
                    "You are a thorough researcher. "
                    "Investigate topics systematically, "
                    "gather data from multiple sources, "
                    "and provide comprehensive findings."
                )
            ),
            max_iterations=max_research_depth,
            require_final_answer=True
        )

# Research tools
@tool
def search_academic(query: str) -> str:
    """Search academic papers and journals."""
    return f"Academic results for '{query}': [Scholar data]"

@tool
def search_statistics(query: str) -> str:
    """Search for statistical data."""
    return f"Statistics for '{query}': [Statistical data]"

@tool
def fact_checker(claim: str) -> str:
    """Verify facts and claims."""
    return f"Fact check for '{claim}': [Verification result]"

# Create researcher
researcher = ResearchPattern.create_researcher(
    name="academic_researcher",
    research_tools=[web_search, search_academic, search_statistics, fact_checker],
    max_research_depth=10
)

# Conduct research
findings = researcher.run("Research the impact of AI on employment rates")
print(f"Confidence: {findings.confidence}")
print(f"Key findings: {findings.key_findings}")
```

### Multi-Tool Reasoning Pattern

Complex reasoning with multiple specialized tools.

```python
# Pattern: Multi-tool reasoning for complex tasks
class MultiToolReasoningPattern:
    """Pattern for agents that coordinate multiple tools."""

    @staticmethod
    def create_multi_tool_agent(
        name: str,
        tool_categories: Dict[str, List]
    ) -> ReactAgentV3:
        """Create agent with categorized tools."""

        # Flatten all tools
        all_tools = []
        for category, tools in tool_categories.items():
            all_tools.extend(tools)

        return ReactAgentV3(
            name=name,
            engine=AugLLMConfig(
                tools=all_tools,
                temperature=0.6,
                system_message=(
                    f"You have access to tools in these categories: "
                    f"{', '.join(tool_categories.keys())}. "
                    f"Use them wisely to solve complex problems."
                )
            ),
            max_iterations=8,
            debug=True
        )

# Define categorized tools
calculation_tools = [
    tool(lambda x: str(eval(x)))(name="calculator"),
    tool(lambda x, y: f"{x}% of {y} = {x * y / 100}")(name="percentage"),
    tool(lambda nums: str(sum(map(float, nums.split(',')))))(name="sum_numbers")
]

data_tools = [
    tool(lambda query: f"Data for {query}")(name="fetch_data"),
    tool(lambda data: f"Analysis of {data}")(name="analyze_data"),
    tool(lambda data: f"Visualization of {data}")(name="visualize_data")
]

communication_tools = [
    tool(lambda msg: f"Email sent: {msg}")(name="send_email"),
    tool(lambda num: f"SMS to {num}")(name="send_sms")
]

# Create multi-tool agent
analyst = MultiToolReasoningPattern.create_multi_tool_agent(
    name="business_analyst",
    tool_categories={
        "calculation": calculation_tools,
        "data": data_tools,
        "communication": communication_tools
    }
)

# Complex multi-tool task
result = analyst.run(
    "Analyze sales data for Q4, calculate 15% growth projection, "
    "and send summary to management"
)
```

## Multi-Agent Patterns

### Sequential Pipeline Pattern

Chain agents in sequence where each builds on the previous output.

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Pattern: Sequential processing pipeline
class SequentialPipelinePattern:
    """Pattern for sequential agent pipelines."""

    @staticmethod
    def create_analysis_pipeline(
        stages: List[Dict[str, Any]]
    ) -> EnhancedMultiAgentV4:
        """Create a sequential analysis pipeline."""

        agents = []
        for stage in stages:
            agent = SimpleAgentV3(
                name=stage['name'],
                engine=AugLLMConfig(
                    structured_output_model=stage.get('output_model'),
                    temperature=stage.get('temperature', 0.5),
                    system_message=stage['system_message']
                )
            )
            agents.append(agent)

        return EnhancedMultiAgentV4(
            name="analysis_pipeline",
            agents=agents,
            execution_mode="sequential"
        )

# Define pipeline stages
class DataExtraction(BaseModel):
    raw_data: List[Dict[str, Any]] = Field(description="Extracted data points")
    data_quality: float = Field(ge=0.0, le=1.0)
    missing_fields: List[str] = Field(description="Fields that couldn't be extracted")

class DataAnalysis(BaseModel):
    patterns: List[str] = Field(description="Patterns identified")
    anomalies: List[str] = Field(description="Anomalies detected")
    insights: List[str] = Field(description="Key insights")
    recommendations: List[str] = Field(description="Actionable recommendations")

class ExecutiveSummary(BaseModel):
    summary: str = Field(description="One paragraph executive summary")
    key_metrics: Dict[str, float] = Field(description="Important metrics")
    action_items: List[str] = Field(description="Prioritized action items")
    next_steps: List[str] = Field(description="Recommended next steps")

# Create pipeline
pipeline = SequentialPipelinePattern.create_analysis_pipeline([
    {
        'name': 'extractor',
        'system_message': 'You extract and structure data from raw inputs',
        'output_model': DataExtraction,
        'temperature': 0.3
    },
    {
        'name': 'analyzer',
        'system_message': 'You analyze data for patterns and insights',
        'output_model': DataAnalysis,
        'temperature': 0.5
    },
    {
        'name': 'summarizer',
        'system_message': 'You create executive summaries for leadership',
        'output_model': ExecutiveSummary,
        'temperature': 0.7
    }
])

# Execute pipeline
result = await pipeline.arun({
    "data": "Raw business data here...",
    "context": "Q4 2023 performance review"
})
```

### Parallel Processing Pattern

Execute multiple agents simultaneously for faster processing.

```python
# Pattern: Parallel agent execution
class ParallelProcessingPattern:
    """Pattern for parallel agent processing."""

    @staticmethod
    def create_parallel_analyzer(
        analysis_aspects: Dict[str, Dict[str, Any]]
    ) -> EnhancedMultiAgentV4:
        """Create parallel analysis system."""

        agents = []
        for aspect_name, config in analysis_aspects.items():
            agent = SimpleAgentV3(
                name=aspect_name,
                engine=AugLLMConfig(
                    structured_output_model=config['model'],
                    temperature=config.get('temperature', 0.5),
                    system_message=config['system_message']
                )
            )
            agents.append(agent)

        return EnhancedMultiAgentV4(
            name="parallel_analyzer",
            agents=agents,
            execution_mode="parallel"
        )

# Define parallel analysis models
class TechnicalAnalysis(BaseModel):
    technology_stack: List[str]
    technical_debt: List[str]
    performance_metrics: Dict[str, float]
    recommendations: List[str]

class FinancialAnalysis(BaseModel):
    revenue: float
    costs: float
    profit_margin: float
    growth_rate: float
    financial_health: str

class MarketAnalysis(BaseModel):
    market_size: float
    market_share: float
    competitors: List[str]
    trends: List[str]
    opportunities: List[str]

# Create parallel analyzer
parallel_analyzer = ParallelProcessingPattern.create_parallel_analyzer({
    'technical': {
        'model': TechnicalAnalysis,
        'system_message': 'You are a technical analyst',
        'temperature': 0.3
    },
    'financial': {
        'model': FinancialAnalysis,
        'system_message': 'You are a financial analyst',
        'temperature': 0.4
    },
    'market': {
        'model': MarketAnalysis,
        'system_message': 'You are a market analyst',
        'temperature': 0.5
    }
})

# All agents run simultaneously
results = await parallel_analyzer.arun({
    "company": "TechCorp",
    "period": "2023",
    "data": "Company data..."
})
```

### Conditional Routing Pattern

Route execution based on dynamic conditions.

```python
# Pattern: Conditional routing based on input
class ConditionalRoutingPattern:
    """Pattern for conditional agent routing."""

    @staticmethod
    def create_smart_router(
        routing_rules: Dict[str, Any]
    ) -> EnhancedMultiAgentV4:
        """Create conditional routing system."""

        # Create classifier
        classifier = SimpleAgentV3(
            name="classifier",
            engine=AugLLMConfig(
                structured_output_model=routing_rules['classification_model'],
                temperature=0.2,
                system_message="You classify inputs for appropriate routing"
            )
        )

        # Create specialized agents
        agents = [classifier]
        for route_name, config in routing_rules['routes'].items():
            agent = SimpleAgentV3(
                name=route_name,
                engine=AugLLMConfig(
                    structured_output_model=config.get('output_model'),
                    tools=config.get('tools', []),
                    temperature=config.get('temperature', 0.5),
                    system_message=config['system_message']
                )
            )
            agents.append(agent)

        # Create workflow
        workflow = EnhancedMultiAgentV4(
            name="smart_router",
            agents=agents,
            execution_mode="conditional",
            build_mode="manual"
        )

        # Add routing logic
        for route_name, config in routing_rules['routes'].items():
            condition = config['condition']
            workflow.add_conditional_edge(
                from_agent="classifier",
                condition=condition,
                destinations=config['destinations']
            )

        return workflow

# Define routing
class TaskClassification(BaseModel):
    task_type: str = Field(description="Type of task: simple, complex, research")
    complexity: float = Field(ge=0.0, le=1.0)
    requires_tools: bool
    estimated_time: int = Field(description="Estimated minutes")

routing_config = {
    'classification_model': TaskClassification,
    'routes': {
        'simple_processor': {
            'system_message': 'You handle simple tasks quickly',
            'temperature': 0.3,
            'condition': lambda state: state.get('complexity', 0) < 0.3,
            'destinations': {'True': 'simple_processor', 'False': 'complex_processor'}
        },
        'complex_processor': {
            'system_message': 'You handle complex tasks thoroughly',
            'tools': [calculator, web_search],
            'temperature': 0.7,
            'condition': lambda state: state.get('complexity', 0) >= 0.3,
            'destinations': {'True': 'complex_processor', 'False': 'simple_processor'}
        },
        'research_processor': {
            'system_message': 'You conduct thorough research',
            'tools': [web_search, search_academic],
            'temperature': 0.5,
            'condition': lambda state: state.get('task_type') == 'research',
            'destinations': {'True': 'research_processor', 'False': 'complex_processor'}
        }
    }
}

# Create smart router
smart_router = ConditionalRoutingPattern.create_smart_router(routing_config)
```

### Hierarchical Coordination Pattern

Nested agent hierarchies for complex organizational structures.

```python
# Pattern: Hierarchical agent coordination
class HierarchicalPattern:
    """Pattern for hierarchical agent organizations."""

    @staticmethod
    def create_department(
        department_name: str,
        manager_config: Dict,
        team_configs: List[Dict]
    ) -> EnhancedMultiAgentV4:
        """Create a hierarchical department structure."""

        # Create manager
        manager = ReactAgentV3(
            name=f"{department_name}_manager",
            engine=AugLLMConfig(
                tools=manager_config.get('tools', []),
                temperature=manager_config.get('temperature', 0.5),
                system_message=manager_config['system_message']
            ),
            max_iterations=manager_config.get('max_iterations', 5)
        )

        # Create team members
        team_members = []
        for member_config in team_configs:
            member = SimpleAgentV3(
                name=member_config['name'],
                engine=AugLLMConfig(
                    structured_output_model=member_config.get('output_model'),
                    tools=member_config.get('tools', []),
                    temperature=member_config.get('temperature', 0.5),
                    system_message=member_config['system_message']
                )
            )
            team_members.append(member)

        # Create department workflow
        all_agents = [manager] + team_members
        department = EnhancedMultiAgentV4(
            name=f"{department_name}_department",
            agents=all_agents,
            execution_mode="manual",
            build_mode="manual"
        )

        # Manager routes to team members
        for member in team_members:
            department.add_edge(manager.name, member.name)
            department.add_edge(member.name, END)

        return department

# Create engineering department
engineering = HierarchicalPattern.create_department(
    department_name="engineering",
    manager_config={
        'system_message': 'You are an engineering manager who delegates tasks',
        'tools': [project_tracker, team_calendar],
        'temperature': 0.6,
        'max_iterations': 5
    },
    team_configs=[
        {
            'name': 'frontend_dev',
            'system_message': 'You are a frontend developer',
            'tools': [code_analyzer, ui_tester],
            'temperature': 0.5
        },
        {
            'name': 'backend_dev',
            'system_message': 'You are a backend developer',
            'tools': [code_analyzer, api_tester],
            'temperature': 0.5
        },
        {
            'name': 'qa_engineer',
            'system_message': 'You are a QA engineer',
            'tools': [test_runner, bug_tracker],
            'temperature': 0.4
        }
    ]
)
```

## Advanced Patterns

### Agent-as-Tool Pattern

Convert agents into reusable tools for other agents.

```python
# Pattern: Agent as a tool for composition
class AgentAsToolPattern:
    """Pattern for using agents as tools."""

    @staticmethod
    def create_expert_tools(
        experts: Dict[str, Dict[str, Any]]
    ) -> List:
        """Create expert agents as tools."""

        expert_tools = []

        for expert_name, config in experts.items():
            # Create expert agent
            expert = SimpleAgentV3(
                name=expert_name,
                engine=AugLLMConfig(
                    structured_output_model=config.get('output_model'),
                    temperature=config.get('temperature', 0.3),
                    system_message=config['system_message']
                )
            )

            # Convert to tool
            expert_tool = expert.as_tool(
                name=f"{expert_name}_expert",
                description=config['tool_description']
            )
            expert_tools.append(expert_tool)

        return expert_tools

    @staticmethod
    def create_coordinator_with_experts(
        coordinator_name: str,
        expert_tools: List
    ) -> ReactAgentV3:
        """Create coordinator that uses expert agents."""

        return ReactAgentV3(
            name=coordinator_name,
            engine=AugLLMConfig(
                tools=expert_tools,
                temperature=0.7,
                system_message="You coordinate with expert agents to solve complex problems"
            ),
            max_iterations=8
        )

# Define experts
class LegalAdvice(BaseModel):
    issue: str
    applicable_laws: List[str]
    risks: List[str]
    recommendations: List[str]
    confidence: float

class FinancialAdvice(BaseModel):
    situation: str
    analysis: str
    recommendations: List[str]
    risk_level: str

experts_config = {
    'legal': {
        'system_message': 'You are a legal expert',
        'output_model': LegalAdvice,
        'tool_description': 'Consult legal expert for advice',
        'temperature': 0.2
    },
    'financial': {
        'system_message': 'You are a financial advisor',
        'output_model': FinancialAdvice,
        'tool_description': 'Consult financial expert',
        'temperature': 0.3
    },
    'technical': {
        'system_message': 'You are a technical architect',
        'tool_description': 'Consult technical expert',
        'temperature': 0.4
    }
}

# Create expert tools
expert_tools = AgentAsToolPattern.create_expert_tools(experts_config)

# Create coordinator
coordinator = AgentAsToolPattern.create_coordinator_with_experts(
    "project_coordinator",
    expert_tools
)

# Coordinator can now consult experts
result = coordinator.run(
    "We're planning to launch a fintech app. What legal, financial, and technical considerations should we address?"
)
```

### Self-Discover Pattern

Agents that build on each other's discoveries sequentially.

```python
# Pattern: Self-discovering agent system
class SelfDiscoverPattern:
    """Pattern for self-discovering multi-agent systems."""

    @staticmethod
    def create_self_discover_workflow(
        discovery_stages: List[Dict[str, Any]]
    ) -> EnhancedMultiAgentV4:
        """Create self-discovering workflow."""

        agents = []

        for i, stage in enumerate(discovery_stages):
            # Each stage reads from previous stages
            system_message = stage['base_message']
            if i > 0:
                system_message += f" You have access to discoveries from previous {i} stages."

            agent = SimpleAgentV3(
                name=stage['name'],
                engine=AugLLMConfig(
                    structured_output_model=stage['discovery_model'],
                    temperature=stage.get('temperature', 0.4),
                    system_message=system_message
                )
            )
            agents.append(agent)

        return EnhancedMultiAgentV4(
            name="self_discover",
            agents=agents,
            execution_mode="sequential"
        )

# Define discovery stages
class ModuleDiscovery(BaseModel):
    task_description: str
    discovered_modules: List[str] = Field(description="Reasoning modules discovered")
    module_descriptions: Dict[str, str] = Field(description="What each module does")
    selection_criteria: str = Field(description="Why these modules were selected")

class ModuleAdaptation(BaseModel):
    original_modules: List[str]
    adapted_modules: Dict[str, str] = Field(description="Modules adapted for specific task")
    connections: List[str] = Field(description="How modules connect")
    optimization_notes: str

class ReasoningStructure(BaseModel):
    modules_used: Dict[str, str]
    reasoning_flow: List[str] = Field(description="Step-by-step reasoning flow")
    decision_points: List[str]
    final_approach: str

discovery_config = [
    {
        'name': 'module_selector',
        'base_message': 'You discover and select reasoning modules for complex tasks',
        'discovery_model': ModuleDiscovery,
        'temperature': 0.5
    },
    {
        'name': 'module_adapter',
        'base_message': 'You adapt and connect reasoning modules for specific tasks',
        'discovery_model': ModuleAdaptation,
        'temperature': 0.4
    },
    {
        'name': 'structure_builder',
        'base_message': 'You build complete reasoning structures from adapted modules',
        'discovery_model': ReasoningStructure,
        'temperature': 0.3
    }
]

# Create self-discover system
self_discover = SelfDiscoverPattern.create_self_discover_workflow(discovery_config)

# Execute discovery process
result = await self_discover.arun({
    "task": "Design a sustainable city transportation system",
    "constraints": ["Environmental", "Economic", "Social"]
})
```

### Dynamic Recompilation Pattern

Agents that adapt their structure at runtime.

```python
# Pattern: Dynamic agent recompilation
class DynamicRecompilationPattern:
    """Pattern for dynamically adaptive agents."""

    @staticmethod
    def create_adaptive_agent(
        name: str,
        initial_tools: List,
        tool_discovery_function: callable
    ) -> SimpleAgentV3:
        """Create agent that adapts its tools dynamically."""

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(
                tools=initial_tools,
                temperature=0.6
            ),
            auto_recompile=True,  # Enable automatic recompilation
            debug=True
        )

        # Add dynamic tool discovery
        @agent.before_run
        def discover_tools(context):
            """Discover and add new tools based on context."""
            task = context.input_data
            new_tools = tool_discovery_function(task)

            current_tool_names = {t.name for t in agent.engine.tools}

            for tool in new_tools:
                if tool.name not in current_tool_names:
                    agent.add_tool(tool)
                    logging.info(f"Added new tool: {tool.name}")

        return agent

# Tool discovery function
def discover_tools_for_task(task: str) -> List:
    """Discover relevant tools based on task."""
    discovered = []

    if "calculate" in task.lower() or "math" in task.lower():
        @tool
        def advanced_calculator(expression: str) -> str:
            """Advanced mathematical calculations."""
            import math
            return str(eval(expression, {"__builtins__": {}}, math.__dict__))
        discovered.append(advanced_calculator)

    if "data" in task.lower() or "analyze" in task.lower():
        @tool
        def data_analyzer(data: str) -> str:
            """Analyze data patterns."""
            return f"Analysis of {data}: [patterns found]"
        discovered.append(data_analyzer)

    if "code" in task.lower() or "program" in task.lower():
        @tool
        def code_generator(spec: str) -> str:
            """Generate code from specifications."""
            return f"Generated code for: {spec}"
        discovered.append(code_generator)

    return discovered

# Create adaptive agent
adaptive_agent = DynamicRecompilationPattern.create_adaptive_agent(
    name="adaptive_assistant",
    initial_tools=[web_search],  # Start with minimal tools
    tool_discovery_function=discover_tools_for_task
)

# Agent discovers and adds tools as needed
result1 = adaptive_agent.run("Search for Python tutorials")  # Uses web_search
result2 = adaptive_agent.run("Calculate sin(45) + cos(30)")  # Discovers and adds calculator
result3 = adaptive_agent.run("Analyze this data set")  # Discovers and adds analyzer
```

### Meta-Agent Pattern

Agents that can reason about and modify their own behavior.

```python
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Pattern: Meta-cognitive agents
class MetaAgentPattern:
    """Pattern for meta-cognitive agents."""

    @staticmethod
    def create_meta_agent(
        name: str,
        base_capabilities: Dict[str, Any]
    ) -> MetaStateSchema:
        """Create agent with meta-cognitive abilities."""

        # Create base agent
        base_agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(
                temperature=base_capabilities.get('temperature', 0.5),
                system_message=base_capabilities['system_message']
            )
        )

        # Wrap in meta-state for self-monitoring
        meta_state = MetaStateSchema.from_agent(
            agent=base_agent,
            initial_state={
                'performance_metrics': {},
                'adaptation_history': [],
                'current_strategy': base_capabilities.get('initial_strategy', 'default')
            },
            graph_context={
                'meta_enabled': True,
                'self_monitoring': True,
                'adaptation_threshold': 0.7
            }
        )

        return meta_state

    @staticmethod
    async def execute_with_reflection(
        meta_state: MetaStateSchema,
        task: str
    ) -> Dict[str, Any]:
        """Execute task with meta-cognitive reflection."""

        # Pre-execution analysis
        pre_analysis = await meta_state.execute_agent({
            "task": f"Analyze this task and plan approach: {task}",
            "mode": "planning"
        })

        # Main execution
        main_result = await meta_state.execute_agent({
            "task": task,
            "mode": "execution",
            "plan": pre_analysis.get('output')
        })

        # Post-execution reflection
        reflection = await meta_state.execute_agent({
            "task": "Reflect on your performance and identify improvements",
            "mode": "reflection",
            "result": main_result.get('output')
        })

        # Update meta-state based on reflection
        if reflection.get('improvements'):
            meta_state.agent_state['adaptation_history'].append({
                'task': task,
                'improvements': reflection['improvements'],
                'timestamp': datetime.now().isoformat()
            })

        return {
            'planning': pre_analysis,
            'execution': main_result,
            'reflection': reflection,
            'meta_state': meta_state.get_execution_summary()
        }

# Create meta-cognitive agent
meta_agent = MetaAgentPattern.create_meta_agent(
    name="self_aware_assistant",
    base_capabilities={
        'system_message': 'You are a self-aware AI that can reflect on and improve your performance',
        'temperature': 0.6,
        'initial_strategy': 'analytical'
    }
)

# Execute with reflection
result = await MetaAgentPattern.execute_with_reflection(
    meta_agent,
    "Solve this complex problem and learn from the process"
)

print(f"Planning: {result['planning']}")
print(f"Execution: {result['execution']}")
print(f"Reflection: {result['reflection']}")
print(f"Meta-state: {result['meta_state']}")
```

## Specialized Patterns

### RAG Agent Pattern

Retrieval-Augmented Generation for knowledge-based agents.

```python
# Pattern: RAG (Retrieval-Augmented Generation)
class RAGPattern:
    """Pattern for RAG agents with document retrieval."""

    @staticmethod
    def create_rag_agent(
        name: str,
        retriever_config: Dict[str, Any],
        answer_config: Dict[str, Any]
    ) -> EnhancedMultiAgentV4:
        """Create RAG agent with retrieval and generation."""

        # Create retriever agent
        retriever = SimpleAgentV3(
            name=f"{name}_retriever",
            engine=AugLLMConfig(
                tools=retriever_config.get('tools', []),
                temperature=0.3,
                system_message="You retrieve relevant documents and information"
            )
        )

        # Create answer agent
        answer_agent = SimpleAgentV3(
            name=f"{name}_answerer",
            engine=AugLLMConfig(
                structured_output_model=answer_config.get('output_model'),
                temperature=answer_config.get('temperature', 0.5),
                system_message="You answer questions based on retrieved context"
            )
        )

        # Create RAG workflow
        rag_workflow = EnhancedMultiAgentV4(
            name=f"{name}_rag",
            agents=[retriever, answer_agent],
            execution_mode="sequential"
        )

        return rag_workflow

class QAResponse(BaseModel):
    question: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str] = Field(description="Sources used")
    follow_up_questions: List[str] = Field(description="Suggested follow-ups")

# Create document search tool
@tool
def search_knowledge_base(query: str) -> str:
    """Search internal knowledge base."""
    # Mock implementation
    return f"Retrieved documents for '{query}': [Document content here]"

# Create RAG agent
rag_agent = RAGPattern.create_rag_agent(
    name="knowledge_assistant",
    retriever_config={
        'tools': [search_knowledge_base]
    },
    answer_config={
        'output_model': QAResponse,
        'temperature': 0.5
    }
)

# Use RAG agent
result = await rag_agent.arun({
    "question": "What are the best practices for Python async programming?"
})
```

### Reflection Pattern

Agents that reflect on their outputs for quality improvement.

```python
# Pattern: Self-reflection for quality improvement
class ReflectionPattern:
    """Pattern for agents with reflection capabilities."""

    @staticmethod
    def create_reflective_agent(
        name: str,
        main_config: Dict[str, Any],
        reflection_config: Dict[str, Any]
    ) -> SimpleAgentV3:
        """Create agent with reflection capabilities."""

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(**main_config)
        )

        # Create reflection agent
        reflector = SimpleAgentV3(
            name=f"{name}_reflector",
            engine=AugLLMConfig(
                temperature=reflection_config.get('temperature', 0.3),
                system_message=reflection_config['system_message']
            )
        )

        # Store reflection agent as attribute
        agent.reflector = reflector

        # Add reflection hook
        @agent.after_run
        async def reflect_on_output(context):
            """Reflect on output quality."""
            output = context.output_data

            reflection_prompt = f"""
            Review this output and assess:
            1. Accuracy and correctness
            2. Completeness
            3. Clarity
            4. Areas for improvement

            Output to review: {output}
            """

            reflection = await reflector.arun(reflection_prompt)

            # Store reflection
            if not hasattr(agent, 'reflections'):
                agent.reflections = []

            agent.reflections.append({
                'output': output,
                'reflection': reflection,
                'timestamp': datetime.now()
            })

            # Log significant issues
            if "improvement" in reflection.lower():
                logging.info(f"Reflection identified improvements: {reflection[:200]}...")

        return agent

# Create reflective writer
reflective_writer = ReflectionPattern.create_reflective_agent(
    name="reflective_writer",
    main_config={
        'temperature': 0.8,
        'system_message': 'You are a creative writer'
    },
    reflection_config={
        'temperature': 0.3,
        'system_message': 'You are a critical editor who provides constructive feedback'
    }
)

# Writing with automatic reflection
result = await reflective_writer.arun("Write a short story about AI")
# Check reflections
if hasattr(reflective_writer, 'reflections'):
    latest_reflection = reflective_writer.reflections[-1]
    print(f"Reflection: {latest_reflection['reflection']}")
```

### Planning and Execution Pattern

Separate planning from execution for complex tasks.

```python
# Pattern: Plan and Execute
class PlanAndExecutePattern:
    """Pattern for planning before execution."""

    class TaskPlan(BaseModel):
        objective: str = Field(description="Main objective")
        steps: List[str] = Field(description="Ordered list of steps")
        requirements: List[str] = Field(description="Required resources/tools")
        success_criteria: List[str] = Field(description="How to measure success")
        estimated_duration: int = Field(description="Estimated minutes")

    class ExecutionResult(BaseModel):
        step: str
        result: str
        success: bool
        issues: List[str] = Field(description="Any issues encountered")

    @staticmethod
    def create_plan_execute_system(
        name: str,
        available_tools: List
    ) -> EnhancedMultiAgentV4:
        """Create plan and execute system."""

        # Planning agent
        planner = SimpleAgentV3(
            name=f"{name}_planner",
            engine=AugLLMConfig(
                structured_output_model=PlanAndExecutePattern.TaskPlan,
                temperature=0.4,
                system_message="You create detailed execution plans"
            )
        )

        # Execution agent
        executor = ReactAgentV3(
            name=f"{name}_executor",
            engine=AugLLMConfig(
                tools=available_tools,
                structured_output_model=PlanAndExecutePattern.ExecutionResult,
                temperature=0.5,
                system_message="You execute plans step by step"
            ),
            max_iterations=10
        )

        # Review agent
        reviewer = SimpleAgentV3(
            name=f"{name}_reviewer",
            engine=AugLLMConfig(
                temperature=0.3,
                system_message="You review execution results and provide final summary"
            )
        )

        return EnhancedMultiAgentV4(
            name=f"{name}_plan_execute",
            agents=[planner, executor, reviewer],
            execution_mode="sequential"
        )

# Create plan-execute system
plan_execute = PlanAndExecutePattern.create_plan_execute_system(
    name="project_manager",
    available_tools=[web_search, calculator, project_tracker, send_email]
)

# Execute complex project
result = await plan_execute.arun({
    "task": "Plan and execute a product launch campaign",
    "budget": "$50,000",
    "timeline": "3 months"
})
```

### Supervisor Pattern

Supervisor agent that manages and coordinates other agents.

```python
# Pattern: Supervisor coordination
class SupervisorPattern:
    """Pattern for supervisor-based coordination."""

    @staticmethod
    def create_supervisor_system(
        supervisor_name: str,
        team_members: Dict[str, Dict[str, Any]]
    ) -> EnhancedMultiAgentV4:
        """Create supervisor system with team."""

        # Create supervisor
        supervisor = ReactAgentV3(
            name=supervisor_name,
            engine=AugLLMConfig(
                temperature=0.6,
                system_message=(
                    f"You are a supervisor managing these team members: "
                    f"{', '.join(team_members.keys())}. "
                    f"Delegate tasks appropriately and coordinate results."
                )
            ),
            max_iterations=8
        )

        # Create team members
        agents = [supervisor]
        member_tools = []

        for member_name, config in team_members.items():
            member = SimpleAgentV3(
                name=member_name,
                engine=AugLLMConfig(
                    structured_output_model=config.get('output_model'),
                    tools=config.get('tools', []),
                    temperature=config.get('temperature', 0.5),
                    system_message=config['system_message']
                )
            )
            agents.append(member)

            # Convert member to tool for supervisor
            member_tool = member.as_tool(
                name=f"delegate_to_{member_name}",
                description=config['description']
            )
            member_tools.append(member_tool)

        # Give supervisor access to team as tools
        supervisor.engine.tools.extend(member_tools)

        # Create workflow
        workflow = EnhancedMultiAgentV4(
            name="supervisor_system",
            agents=agents,
            execution_mode="manual",
            build_mode="manual"
        )

        # Supervisor can delegate to any team member
        for member_name in team_members.keys():
            workflow.add_edge(supervisor_name, member_name)
            workflow.add_edge(member_name, supervisor_name)  # Report back

        workflow.add_edge(supervisor_name, END)

        return workflow

# Define team
team_config = {
    'researcher': {
        'description': 'Delegate research tasks',
        'system_message': 'You are a research specialist',
        'tools': [web_search, search_academic],
        'temperature': 0.4
    },
    'analyst': {
        'description': 'Delegate analysis tasks',
        'system_message': 'You are a data analyst',
        'tools': [calculator, data_analyzer],
        'temperature': 0.3
    },
    'writer': {
        'description': 'Delegate writing tasks',
        'system_message': 'You are a technical writer',
        'temperature': 0.7
    }
}

# Create supervisor system
supervisor_system = SupervisorPattern.create_supervisor_system(
    supervisor_name="project_supervisor",
    team_members=team_config
)

# Execute with supervisor coordination
result = await supervisor_system.arun({
    "project": "Create a comprehensive report on renewable energy trends",
    "requirements": ["Current data", "Market analysis", "Future projections"]
})
```

## Production Patterns

### Error Recovery Pattern

Robust error handling and recovery mechanisms.

```python
# Pattern: Error recovery and resilience
class ErrorRecoveryPattern:
    """Pattern for resilient agents with error recovery."""

    @staticmethod
    def create_resilient_agent(
        name: str,
        config: Dict[str, Any],
        recovery_strategies: Dict[str, callable]
    ) -> SimpleAgentV3:
        """Create agent with error recovery capabilities."""

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(**config)
        )

        # Track errors
        agent.error_history = []
        agent.recovery_attempts = {}

        @agent.on_error
        def handle_error(context):
            """Handle errors with recovery strategies."""
            error = context.error
            error_type = type(error).__name__

            # Log error
            agent.error_history.append({
                'error': str(error),
                'type': error_type,
                'timestamp': datetime.now(),
                'input': context.input_data
            })

            # Attempt recovery
            if error_type in recovery_strategies:
                recovery_strategy = recovery_strategies[error_type]
                try:
                    recovery_result = recovery_strategy(context)
                    agent.recovery_attempts[error_type] = {
                        'success': True,
                        'result': recovery_result
                    }
                    return recovery_result
                except Exception as recovery_error:
                    agent.recovery_attempts[error_type] = {
                        'success': False,
                        'error': str(recovery_error)
                    }

            # Fallback response
            return {
                'error': True,
                'message': f"Error occurred: {error}",
                'recovery_attempted': error_type in recovery_strategies
            }

        return agent

# Define recovery strategies
def recover_from_timeout(context):
    """Recovery strategy for timeouts."""
    simplified_input = context.input_data[:100]  # Truncate input
    return f"Task timed out. Summary based on partial processing: {simplified_input}..."

def recover_from_validation(context):
    """Recovery strategy for validation errors."""
    return {
        'partial_result': 'Validation failed',
        'suggestions': ['Check input format', 'Verify required fields']
    }

def recover_from_tool_error(context):
    """Recovery strategy for tool errors."""
    return "Tool execution failed. Proceeding with general knowledge."

recovery_strategies = {
    'TimeoutError': recover_from_timeout,
    'ValidationError': recover_from_validation,
    'ToolExecutionError': recover_from_tool_error
}

# Create resilient agent
resilient_agent = ErrorRecoveryPattern.create_resilient_agent(
    name="resilient_assistant",
    config={
        'temperature': 0.7,
        'timeout': 30,
        'retry_attempts': 3
    },
    recovery_strategies=recovery_strategies
)
```

### Performance Optimization Pattern

Optimize agent performance for production workloads.

```python
# Pattern: Performance-optimized agents
class PerformancePattern:
    """Pattern for performance-optimized agents."""

    @staticmethod
    def create_optimized_agent(
        name: str,
        optimization_config: Dict[str, Any]
    ) -> SimpleAgentV3:
        """Create performance-optimized agent."""

        # Base configuration for performance
        base_config = {
            'temperature': optimization_config.get('temperature', 0.3),
            'max_tokens': optimization_config.get('max_tokens', 500),
            'timeout': optimization_config.get('timeout', 30),
            'cache_enabled': optimization_config.get('cache_enabled', True)
        }

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(**base_config),
            debug=False,  # Disable debug for performance
            change_tracking_enabled=False  # Disable if not needed
        )

        # Response cache
        if optimization_config.get('cache_enabled', True):
            agent.response_cache = {}

            @agent.before_run
            def check_cache(context):
                """Check cache before execution."""
                cache_key = str(context.input_data)[:100]  # Simple key
                if cache_key in agent.response_cache:
                    # Check cache age
                    cached = agent.response_cache[cache_key]
                    age = (datetime.now() - cached['timestamp']).seconds
                    if age < optimization_config.get('cache_ttl', 300):  # 5 min default
                        context.cached_response = cached['response']
                        return cached['response']

            @agent.after_run
            def update_cache(context):
                """Update cache after execution."""
                if not hasattr(context, 'cached_response'):
                    cache_key = str(context.input_data)[:100]
                    agent.response_cache[cache_key] = {
                        'response': context.output_data,
                        'timestamp': datetime.now()
                    }

        # Batch processing support
        if optimization_config.get('batch_enabled', False):
            agent.batch_queue = []

            def process_batch(items: List[str]) -> List[Any]:
                """Process items in batch."""
                results = []
                for item in items:
                    result = agent.run(item)
                    results.append(result)
                return results

            agent.process_batch = process_batch

        return agent

# Create optimized agent
fast_agent = PerformancePattern.create_optimized_agent(
    name="fast_assistant",
    optimization_config={
        'temperature': 0.3,  # Lower for consistency
        'max_tokens': 300,   # Limit response size
        'timeout': 20,       # Shorter timeout
        'cache_enabled': True,
        'cache_ttl': 600,    # 10 minute cache
        'batch_enabled': True
    }
)

# Single request (may use cache)
result = fast_agent.run("Common question")

# Batch processing
if hasattr(fast_agent, 'process_batch'):
    batch_results = fast_agent.process_batch([
        "Question 1",
        "Question 2",
        "Question 3"
    ])
```

### Monitoring and Observability Pattern

Comprehensive monitoring for production agents.

```python
# Pattern: Observable agents with metrics
class ObservabilityPattern:
    """Pattern for observable agents with metrics."""

    @staticmethod
    def create_observable_agent(
        name: str,
        config: Dict[str, Any],
        metrics_config: Dict[str, Any]
    ) -> SimpleAgentV3:
        """Create agent with comprehensive observability."""

        agent = SimpleAgentV3(
            name=name,
            engine=AugLLMConfig(**config),
            debug=metrics_config.get('debug', False)
        )

        # Initialize metrics
        agent.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'average_latency': 0.0,
            'error_rate': 0.0,
            'cache_hit_rate': 0.0
        }

        agent.request_history = []

        @agent.before_run
        def start_request_tracking(context):
            """Start tracking request metrics."""
            context.start_time = datetime.now()
            agent.metrics['total_requests'] += 1

        @agent.after_run
        def complete_request_tracking(context):
            """Complete request tracking."""
            # Calculate latency
            latency = (datetime.now() - context.start_time).total_seconds()

            # Update metrics
            agent.metrics['successful_requests'] += 1

            # Token tracking (if available)
            if hasattr(context, 'token_usage'):
                agent.metrics['total_tokens'] += context.token_usage.get('total', 0)
                agent.metrics['total_cost'] += context.token_usage.get('cost', 0.0)

            # Update average latency
            total = agent.metrics['successful_requests']
            current_avg = agent.metrics['average_latency']
            agent.metrics['average_latency'] = (
                (current_avg * (total - 1) + latency) / total
            )

            # Store in history
            agent.request_history.append({
                'timestamp': datetime.now(),
                'input': str(context.input_data)[:100],
                'latency': latency,
                'success': True
            })

            # Emit metrics (to monitoring system)
            if metrics_config.get('emit_metrics'):
                emit_metrics(agent.metrics)

        @agent.on_error
        def track_error(context):
            """Track error metrics."""
            agent.metrics['failed_requests'] += 1
            agent.metrics['error_rate'] = (
                agent.metrics['failed_requests'] / agent.metrics['total_requests']
            )

            # Log error details
            logging.error(f"Agent {name} error: {context.error}")

            # Store in history
            agent.request_history.append({
                'timestamp': datetime.now(),
                'input': str(context.input_data)[:100],
                'error': str(context.error),
                'success': False
            })

        # Metrics reporting function
        def get_metrics_summary():
            """Get current metrics summary."""
            return {
                **agent.metrics,
                'uptime': (datetime.now() - agent.created_at).total_seconds(),
                'recent_errors': [
                    r for r in agent.request_history[-10:]
                    if not r['success']
                ]
            }

        agent.get_metrics = get_metrics_summary
        agent.created_at = datetime.now()

        return agent

# Metrics emission function (mock)
def emit_metrics(metrics: Dict[str, Any]):
    """Emit metrics to monitoring system."""
    # In production, this would send to Prometheus, CloudWatch, etc.
    logging.info(f"Metrics: {metrics}")

# Create observable agent
monitored_agent = ObservabilityPattern.create_observable_agent(
    name="production_agent",
    config={
        'temperature': 0.5,
        'model': 'gpt-4'
    },
    metrics_config={
        'debug': False,
        'emit_metrics': True
    }
)

# Use agent
result = monitored_agent.run("Process this request")

# Get metrics
metrics = monitored_agent.get_metrics()
print(f"Success rate: {1 - metrics['error_rate']:.2%}")
print(f"Average latency: {metrics['average_latency']:.2f}s")
print(f"Total cost: ${metrics['total_cost']:.4f}")
```

## Best Practices

### 1. Pattern Selection

- Choose patterns based on your specific use case
- Start simple and add complexity as needed
- Consider performance implications of complex patterns

### 2. Error Handling

- Always implement error recovery strategies
- Log errors comprehensively for debugging
- Provide fallback responses when possible

### 3. Performance

- Use caching for frequently repeated queries
- Limit token usage with max_tokens
- Consider batch processing for multiple requests

### 4. Monitoring

- Track key metrics (latency, errors, costs)
- Set up alerts for anomalies
- Regular review of agent performance

### 5. Testing

- Test each pattern in isolation
- Use real components (no mocks)
- Validate structured outputs thoroughly

### 6. Security

- Validate all inputs
- Limit tool access appropriately
- Monitor for unusual usage patterns

## Next Steps

1. **Experiment**: Try different patterns with your use cases
2. **Combine**: Mix patterns for more sophisticated behaviors
3. **Customize**: Adapt patterns to your specific needs
4. **Contribute**: Share new patterns with the community

For more information, see the [main documentation](../README.md) and [examples](../../examples/).
