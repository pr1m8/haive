#!/usr/bin/env python3
"""Sequential Multi-Agent Demo - Showcasing new pattern implementations.

This demo shows how to use the new agent patterns created with agent.py,
SimpleAgentV3, and EnhancedMultiAgentV4 as foundations. It demonstrates:

1. Sequential ReactAgent → SimpleAgent flow with structured output
2. Chat prompt templates with input variables
3. Pre/post processing hooks
4. Real multi-agent patterns (no mocks)
"""

import asyncio

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Import the pattern implementations we created
from haive.agents.patterns.react_structured_agent_variants import (
    StructuredSolution,
    create_react_structured_agent,
)
from haive.agents.patterns.sequential_workflow_agent import (
    create_research_workflow,
)
from haive.agents.patterns.simple_rag_agent_pattern import (
    create_simple_rag_agent,
)
from haive.agents.react.agent import ReactAgent

# For direct agent creation
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Custom structured output models for demo
class ProblemAnalysis(BaseModel):
    """Structured problem analysis from ReactAgent."""

    problem_type: str = Field(
        description="Type of problem: technical, business, or research"
    )
    complexity_level: str = Field(description="Complexity: simple, medium, or complex")
    key_challenges: list[str] = Field(description="Main challenges identified")
    recommended_approach: str = Field(description="Recommended solution approach")
    required_resources: list[str] = Field(description="Resources needed")


class FormattedSolution(BaseModel):
    """Final formatted solution from SimpleAgent."""

    title: str = Field(description="Solution title")
    executive_summary: str = Field(description="Brief summary for executives")
    detailed_solution: str = Field(description="Comprehensive solution details")
    implementation_timeline: list[str] = Field(
        description="Implementation steps with timeline"
    )
    success_metrics: list[str] = Field(description="How to measure success")
    risk_mitigation: list[str] = Field(description="Risk mitigation strategies")


async def demo_react_to_simple_structured():
    """Demo 1: ReactAgent → SimpleAgent with structured output."""

    # Create tools for ReactAgent
    @tool
    def analyze_complexity(problem: str) -> str:
        """Analyze the complexity of a problem."""
        return f"Analysis: The problem '{problem}' appears to be moderately complex with technical and business aspects."

    @tool
    def identify_resources(task: str) -> str:
        """Identify required resources for a task."""
        return f"Resources needed for '{task}': 2 developers, 1 designer, cloud infrastructure, and 3 months timeline."

    # Create ReactAgent for analysis
    react_agent = ReactAgent(
        name="analyzer",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are an expert problem analyzer. Use tools to analyze problems thoroughly.",
            tools=[analyze_complexity, identify_resources],
            structured_output_model=ProblemAnalysis,
        ),
    )

    # Create SimpleAgent for formatting with prompt template
    format_agent = SimpleAgentV3(
        name="formatter",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a professional solution formatter. Create comprehensive, well-structured solutions.",
            structured_output_model=FormattedSolution,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Based on this analysis:
Problem Type: {problem_type}
Complexity: {complexity_level}
Key Challenges: {key_challenges}
Recommended Approach: {recommended_approach}
Required Resources: {required_resources}

Create a comprehensive, formatted solution document.""",
                ),
            ]
        ),
    )

    # Create multi-agent workflow
    workflow = EnhancedMultiAgentV4(
        name="analysis_pipeline",
        agents=[react_agent, format_agent],
        execution_mode="sequential",
    )

    # Add hook to see intermediate results
    @workflow.after_agent_execution
    def log_agent_result(agent_name: str, result: any):
        if isinstance(result, dict):
            for _key, _value in result.items():
                pass
        else:
            pass

    # Execute workflow
    problem = "Design a scalable microservices architecture for an e-commerce platform"

    result = await workflow.arun({"messages": [{"role": "user", "content": problem}]})

    if isinstance(result, dict) and "formatter" in result:
        result["formatter"]


async def demo_research_workflow():
    """Demo 2: Research workflow with multiple stages."""
    # Create research workflow with structured outputs
    research_flow = create_research_workflow(
        name="ai_research", stages=["analyze", "research", "synthesize", "format"]
    )

    # Add pre/post processing hooks
    @research_flow.before_agent_execution
    def pre_process(agent_name: str, state: dict):
        pass

    @research_flow.after_agent_execution
    def post_process(agent_name: str, result: any):
        pass

    # Execute research
    topic = "The impact of generative AI on software development practices"

    result = await research_flow.arun(
        {
            "messages": [{"role": "user", "content": f"Research: {topic}"}],
            "depth": "comprehensive",
            "audience": "technical leaders",
        }
    )

    # The workflow returns results from each stage
    for _stage_name, stage_result in result.items():
        if isinstance(stage_result, dict):
            for _key, _value in stage_result.items():
                pass


async def demo_custom_sequential_with_hooks():
    """Demo 3: Custom sequential workflow with advanced hooks."""
    # Create agents with specific prompt templates
    idea_generator = SimpleAgentV3(
        name="idea_generator",
        engine=AugLLMConfig(
            temperature=0.8, system_message="You are a creative idea generator."
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    "Generate innovative ideas for: {topic}\nContext: {context}\nConstraints: {constraints}",
                ),
            ]
        ),
    )

    idea_evaluator = SimpleAgentV3(
        name="idea_evaluator",
        engine=AugLLMConfig(
            temperature=0.3, system_message="You are a critical idea evaluator."
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    "Evaluate these ideas:\n{ideas}\n\nEvaluation criteria: {criteria}",
                ),
            ]
        ),
    )

    implementation_planner = SimpleAgentV3(
        name="implementation_planner",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are an implementation planning expert.",
            structured_output_model=StructuredSolution,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    "Create implementation plan for:\n{selected_idea}\nEvaluation: {evaluation}",
                ),
            ]
        ),
    )

    # Create workflow
    workflow = EnhancedMultiAgentV4(
        name="innovation_pipeline",
        agents=[idea_generator, idea_evaluator, implementation_planner],
        execution_mode="sequential",
    )

    # Add comprehensive hooks
    execution_log = []

    @workflow.before_workflow
    def start_workflow(state):
        execution_log.append("=== Workflow Started ===")

    @workflow.before_agent_execution
    def before_agent(agent_name, state):
        execution_log.append(f"→ {agent_name} starting")

    @workflow.after_agent_execution
    def after_agent(agent_name, result):
        execution_log.append(f"✓ {agent_name} completed")

    @workflow.after_workflow
    def end_workflow(final_result):
        execution_log.append("=== Workflow Completed ===")
        for _entry in execution_log:
            pass

    # Execute with input variables
    result = await workflow.arun(
        {
            "topic": "sustainable urban transportation",
            "context": "growing cities with traffic congestion",
            "constraints": "limited budget, must be eco-friendly",
            "criteria": "feasibility, impact, cost-effectiveness",
            "messages": [{"role": "user", "content": "Create innovative solution"}],
        }
    )

    if "implementation_planner" in result:
        result["implementation_planner"]


async def demo_react_structured_pattern():
    """Demo 4: Using the ReactToStructuredAgent pattern directly."""
    # Use the pattern we created
    agent = create_react_structured_agent(
        name="problem_solver", output_model=StructuredSolution
    )

    # Add monitoring hooks
    @agent.on_reasoning_complete
    def log_reasoning(reasoning_output):
        pass

    @agent.on_structuring_complete
    def log_structuring(structured_output):
        pass

    # Execute
    problem = "How can we reduce technical debt in a large legacy codebase?"

    result = await agent.arun(problem)

    if isinstance(result, dict):
        pass


async def demo_rag_with_structured_output():
    """Demo 5: RAG agent with structured output."""
    # Create RAG agent with structured output
    rag_agent = create_simple_rag_agent(
        name="knowledge_assistant", temperature=0.3, include_sources=True
    )

    # Add retrieval monitoring
    @rag_agent.on_retrieval
    def log_retrieval(query, documents):
        pass

    @rag_agent.on_answer_generation
    def log_answer(answer):
        pass

    # Ask question
    question = "What are the best practices for implementing microservices?"

    result = await rag_agent.arun(question)

    if isinstance(result, dict):
        pass


async def main():
    """Run all demos."""
    # Run demos
    await demo_react_to_simple_structured()
    await demo_research_workflow()
    await demo_custom_sequential_with_hooks()
    await demo_react_structured_pattern()
    await demo_rag_with_structured_output()


if __name__ == "__main__":
    # Run with poetry run python sequential_multi_agent_demo.py
    asyncio.run(main())
