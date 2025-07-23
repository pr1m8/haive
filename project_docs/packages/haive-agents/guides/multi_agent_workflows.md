# Multi-Agent Workflow Guide - Building with EnhancedMultiAgent V3

**Version**: 1.0  
**Date**: 2025-01-21  
**Status**: Complete Guide

## 🎯 **Overview**

This guide shows you how to build multi-agent workflows using EnhancedMultiAgent V3. You'll learn patterns, best practices, and real-world examples.

## 🏗️ **Core Concepts**

### What is EnhancedMultiAgent V3?

EnhancedMultiAgent V3 is a powerful orchestrator that combines multiple agents:

- **Generic Typing**: Proper type safety with StateType
- **Execution Modes**: Sequential, parallel, or custom
- **Performance Tracking**: Built-in execution time monitoring
- **Debug Support**: Detailed logging for development
- **State Management**: Shared state across agents

### Key Features

```python
EnhancedMultiAgent[StateType](
    agents: list[Agent] | dict[str, Agent],
    execution_mode: Literal["sequential", "parallel", "custom"],
    performance_mode: bool = True,
    debug_mode: bool = False
)
```

## 🚀 **Quick Start Examples**

### 1. Sequential Workflow (Step-by-Step)

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent

# Create agents
analyzer = ReactAgent(name="analyzer", engine=config, tools=[...])
writer = SimpleAgent(name="writer", engine=config)

# Sequential: analyzer → writer
workflow = EnhancedMultiAgent.create(
    agents=[analyzer, writer],
    execution_mode="sequential",
    name="analysis_workflow"
)

# Execute
result = await workflow.arun("Analyze market trends and write report")
```

### 2. Parallel Workflow (Simultaneous)

```python
# Create specialized agents
researcher = SimpleAgent(name="researcher", engine=config)
fact_checker = SimpleAgent(name="fact_checker", engine=config)
summarizer = SimpleAgent(name="summarizer", engine=config)

# Parallel execution
workflow = EnhancedMultiAgent.create(
    agents=[researcher, fact_checker, summarizer],
    execution_mode="parallel",
    name="research_workflow"
)

# All agents work simultaneously
results = await workflow.arun("Research AI trends")
```

### 3. Named Agent Workflow (Selective Execution)

```python
# Use dict for named agents
agents = {
    "planner": PlannerAgent(name="planner", engine=config),
    "coder": CodingAgent(name="coder", engine=config),
    "tester": TestingAgent(name="tester", engine=config),
    "reviewer": ReviewAgent(name="reviewer", engine=config)
}

# Create workflow
dev_workflow = EnhancedMultiAgent(
    agents=agents,
    execution_mode="custom",  # Define custom flow
    name="development_pipeline"
)
```

## 📋 **Common Patterns**

### Pattern 1: Research → Analysis → Report

```python
# Research and report pattern
research_workflow = EnhancedMultiAgent.create(
    agents=[
        ResearchAgent(name="researcher", tools=[web_search, arxiv]),
        AnalysisAgent(name="analyzer", engine=analytical_config),
        ReportAgent(name="reporter", structured_output=ReportModel)
    ],
    execution_mode="sequential",
    name="research_pipeline"
)

report = await research_workflow.arun("Latest developments in quantum computing")
```

### Pattern 2: Plan → Execute → Verify

```python
# Planning and execution pattern
task_workflow = EnhancedMultiAgent.create(
    agents=[
        PlannerAgent(name="planner", engine=planning_config),
        ExecutorAgent(name="executor", tools=[...]),
        VerifierAgent(name="verifier", engine=verification_config)
    ],
    execution_mode="sequential",
    name="task_pipeline"
)

result = await task_workflow.arun("Implement user authentication system")
```

### Pattern 3: Multi-Stage RAG

```python
# Advanced RAG with reranking
advanced_rag = EnhancedMultiAgent.create(
    agents=[
        BaseRAGAgent.from_documents(documents, name="retriever"),
        RerankingAgent(name="reranker", model="cross-encoder"),
        SimpleAgent(name="answerer", prompt_template=RAG_ANSWER_WITH_CITATIONS)
    ],
    execution_mode="sequential",
    name="advanced_rag"
)
```

### Pattern 4: Consensus Decision Making

```python
# Multiple agents vote on decision
consensus_workflow = EnhancedMultiAgent.create(
    agents=[
        ExpertAgent(name="expert1", domain="finance"),
        ExpertAgent(name="expert2", domain="technology"),
        ExpertAgent(name="expert3", domain="strategy"),
        ConsensusAgent(name="moderator", voting_threshold=0.66)
    ],
    execution_mode="parallel",  # Experts work in parallel
    name="consensus_decision"
)
```

## 🔧 **Advanced Features**

### Custom Execution Flow

```python
class CustomWorkflow(EnhancedMultiAgent):
    """Custom execution logic for complex workflows."""

    async def execute_agents(self, input_data: Any) -> Any:
        """Custom execution pattern."""
        # Phase 1: Initial analysis
        analysis = await self.agents["analyzer"].arun(input_data)

        # Phase 2: Conditional execution
        if "urgent" in analysis.lower():
            result = await self.agents["fast_processor"].arun(analysis)
        else:
            # Parallel processing for non-urgent
            tasks = [
                self.agents["deep_analyzer"].arun(analysis),
                self.agents["fact_checker"].arun(analysis)
            ]
            results = await asyncio.gather(*tasks)
            result = await self.agents["synthesizer"].arun(results)

        return result
```

### State Sharing Between Agents

```python
from haive.core.schema import StateSchema

class SharedWorkflowState(StateSchema):
    """Shared state for workflow agents."""
    research_findings: list[str] = []
    verified_facts: list[str] = []
    final_report: str = ""

# Agents can read/write shared state
workflow = EnhancedMultiAgent[SharedWorkflowState].create(
    agents=[research_agent, verification_agent, report_agent],
    execution_mode="sequential",
    shared_state_schema=SharedWorkflowState
)
```

### Performance Optimization

```python
# Enable performance tracking
optimized_workflow = EnhancedMultiAgent.create(
    agents=agents,
    execution_mode="parallel",
    performance_mode=True,  # Track execution times
    max_concurrency=5,     # Limit parallel execution
    timeout=30.0          # Global timeout
)

# Check performance after execution
result = await optimized_workflow.arun(input_data)
print(f"Total time: {optimized_workflow.execution_time}s")
print(f"Agent times: {optimized_workflow.agent_execution_times}")
```

### Error Handling and Recovery

```python
# Robust workflow with error handling
robust_workflow = EnhancedMultiAgent.create(
    agents=agents,
    execution_mode="sequential",
    error_handling="continue",  # Continue on agent failure
    retry_config={
        "max_retries": 3,
        "backoff_factor": 2.0
    }
)

try:
    result = await robust_workflow.arun(input_data)
except WorkflowError as e:
    print(f"Workflow failed: {e}")
    print(f"Failed agents: {e.failed_agents}")
    print(f"Partial results: {e.partial_results}")
```

## 🎨 **Design Patterns**

### 1. Pipeline Pattern

Sequential processing through specialized stages:

```
Input → PreProcessor → MainProcessor → PostProcessor → Output
```

### 2. MapReduce Pattern

Parallel processing with aggregation:

```
Input → Map(Agent1, Agent2, Agent3) → Reduce(Aggregator) → Output
```

### 3. Supervisor Pattern

One agent coordinates others:

```
Supervisor → assigns → [Worker1, Worker2, Worker3]
          ← reports ←
```

### 4. Debate Pattern

Agents discuss and refine:

```
Proposer ↔ Critic ↔ Synthesizer → Final Answer
```

## 📊 **Best Practices**

### 1. Agent Design

- **Single Responsibility**: Each agent should do one thing well
- **Clear Interfaces**: Define clear input/output schemas
- **Reusability**: Design agents to be reusable across workflows

### 2. Workflow Structure

- **Start Simple**: Begin with sequential, add complexity as needed
- **Test Incrementally**: Test each agent before combining
- **Monitor Performance**: Use performance_mode in production

### 3. State Management

- **Minimize Shared State**: Only share what's necessary
- **Use Schemas**: Define clear state schemas
- **Avoid Race Conditions**: Be careful with parallel writes

### 4. Error Handling

- **Graceful Degradation**: Plan for agent failures
- **Logging**: Use debug_mode during development
- **Timeouts**: Set reasonable timeouts for each agent

## 🚀 **Real-World Examples**

### Example 1: Content Creation Pipeline

```python
# Blog post creation workflow
content_pipeline = EnhancedMultiAgent.create(
    agents=[
        ResearchAgent(name="researcher", tools=[web_search, wikipedia]),
        OutlineAgent(name="outliner", engine=planning_config),
        WriterAgent(name="writer", style="professional"),
        EditorAgent(name="editor", focus=["grammar", "clarity"]),
        SEOAgent(name="seo_optimizer", target_keywords=keywords)
    ],
    execution_mode="sequential",
    name="content_pipeline"
)

blog_post = await content_pipeline.arun("Write about sustainable technology")
```

### Example 2: Code Review System

```python
# Automated code review
review_system = EnhancedMultiAgent.create(
    agents=[
        StyleChecker(name="style", rules=style_guide),
        SecurityAuditor(name="security", vulnerability_db=vuln_db),
        PerformanceAnalyzer(name="performance", benchmarks=benchmarks),
        TestCoverage(name="coverage", min_coverage=80),
        ReviewSummarizer(name="summarizer")
    ],
    execution_mode="parallel",  # All checks run simultaneously
    name="code_review"
)

review = await review_system.arun(code_changes)
```

### Example 3: Customer Support Bot

```python
# Multi-stage support system
support_bot = EnhancedMultiAgent.create(
    agents=[
        IntentClassifier(name="classifier", intents=support_intents),
        KnowledgeRetriever(name="kb_search", knowledge_base=kb),
        ResponseGenerator(name="responder", tone="helpful"),
        SatisfactionChecker(name="satisfaction", threshold=0.8)
    ],
    execution_mode="sequential",
    name="support_bot"
)

response = await support_bot.arun(customer_query)
```

## 🔍 **Debugging Workflows**

### Enable Debug Mode

```python
# Debug mode for development
debug_workflow = EnhancedMultiAgent.create(
    agents=agents,
    execution_mode="sequential",
    debug_mode=True,  # Detailed logging
    name="debug_workflow"
)

# See detailed execution logs
result = await debug_workflow.arun(input_data)
```

### Inspect Intermediate Results

```python
# Custom workflow with inspection points
class InspectableWorkflow(EnhancedMultiAgent):
    async def execute_agents(self, input_data):
        results = {}

        for agent_name, agent in self.agents.items():
            result = await agent.arun(input_data)
            results[agent_name] = result

            # Log intermediate result
            logger.info(f"{agent_name} output: {result[:100]}...")

            # Update input for next agent
            input_data = result

        return results
```

## 📚 **Advanced Patterns**

### Dynamic Agent Selection

```python
class DynamicWorkflow(EnhancedMultiAgent):
    """Workflow that selects agents based on input."""

    async def execute_agents(self, input_data):
        # Analyze input
        analysis = await self.agents["analyzer"].arun(input_data)

        # Select appropriate agents
        if "technical" in analysis:
            selected = ["technical_expert", "code_generator"]
        else:
            selected = ["general_expert", "writer"]

        # Execute selected agents
        for agent_name in selected:
            result = await self.agents[agent_name].arun(input_data)
            input_data = result

        return result
```

### Recursive Workflows

```python
class RecursiveWorkflow(EnhancedMultiAgent):
    """Workflow that can call itself."""

    async def execute_agents(self, input_data, depth=0):
        if depth > 3:  # Prevent infinite recursion
            return input_data

        result = await self.agents["processor"].arun(input_data)

        if "needs_refinement" in result:
            # Recursive call with refined input
            return await self.execute_agents(result, depth + 1)

        return result
```

## 🎯 **Choosing Execution Modes**

### Sequential

Best for:

- Step-by-step processes
- When output of one agent is input to next
- Ordered workflows

### Parallel

Best for:

- Independent tasks
- Performance optimization
- Multiple perspectives

### Custom

Best for:

- Complex logic
- Conditional execution
- Dynamic workflows

## 🚀 **Getting Started Checklist**

1. **Define Your Goal**: What should the workflow accomplish?
2. **Identify Agents**: What specialized agents do you need?
3. **Choose Execution Mode**: Sequential, parallel, or custom?
4. **Design State Schema**: What data needs to be shared?
5. **Build Incrementally**: Start simple, add complexity
6. **Test Thoroughly**: Test each agent and the complete workflow
7. **Monitor Performance**: Use performance_mode in production

## 🔗 **Next Steps**

- [SimpleRAG Guide](simple_rag_complete.md) - Dead simple RAG pattern
- [Agent Development Guide](../haive-agents/development_guide.md)
- [State Management Guide](../haive-core/state_management.md)
- [Performance Optimization](../guides/performance_optimization.md)

---

**Remember**: Start simple with sequential workflows, then add complexity as needed. The power of multi-agent systems comes from combining specialized agents to solve complex problems.
