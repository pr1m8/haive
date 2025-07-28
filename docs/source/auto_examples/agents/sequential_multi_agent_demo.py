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
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Import the pattern implementations we created
from haive.agents.patterns.react_structured_agent_variants import (
    AnalysisResult,
    StructuredSolution,
    create_multi_stage_reasoning_agent,
    create_react_structured_agent,
)
from haive.agents.patterns.sequential_workflow_agent import (
    FinalReport,
    ResearchBrief,
    ResearchFindings,
    create_research_workflow,
)
from haive.agents.patterns.simple_rag_agent_pattern import (
    AnswerWithSources,
    create_simple_rag_agent,
)
from haive.agents.react.agent import ReactAgent

# For direct agent creation
from haive.agents.simple.agent_v3 import SimpleAgentV3


# Custom structured output models for demo
class ProblemAnalysis(BaseModel):
    """Structured problem analysis from ReactAgent."""

    problem_type: str = Field(
        description="Type of problem: technical, business, or research"
    )
    complexity_level: str = Field(description="Complexity: simple, medium, or complex")
    key_challenges: List[str] = Field(description="Main challenges identified")
    recommended_approach: str = Field(description="Recommended solution approach")
    required_resources: List[str] = Field(description="Resources needed")


class FormattedSolution(BaseModel):
    """Final formatted solution from SimpleAgent."""

    title: str = Field(description="Solution title")
    executive_summary: str = Field(description="Brief summary for executives")
    detailed_solution: str = Field(description="Comprehensive solution details")
    implementation_timeline: List[str] = Field(
        description="Implementation steps with timeline"
    )
    success_metrics: List[str] = Field(description="How to measure success")
    risk_mitigation: List[str] = Field(description="Risk mitigation strategies")


async def demo_react_to_simple_structured():
    """Demo 1: ReactAgent → SimpleAgent with structured output."""
    print("\n=== Demo 1: React → Simple with Structured Output ===\n")

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
        print(f"\n[Hook] Agent '{agent_name}' completed:")
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"  - {key}: {value}")
        else:
            print(f"  Result: {result}")

    # Execute workflow
    problem = "Design a scalable microservices architecture for an e-commerce platform"
    print(f"Problem: {problem}\n")

    result = await workflow.arun({"messages": [{"role": "user", "content": problem}]})

    print("\n=== Final Formatted Solution ===")
    if isinstance(result, dict) and "formatter" in result:
        solution = result["formatter"]
        print(f"Title: {solution.get('title', 'N/A')}")
        print(f"Executive Summary: {solution.get('executive_summary', 'N/A')}")
        print(f"Implementation Timeline: {solution.get('implementation_timeline', [])}")


async def demo_research_workflow():
    """Demo 2: Research workflow with multiple stages."""
    print("\n\n=== Demo 2: Multi-Stage Research Workflow ===\n")

    # Create research workflow with structured outputs
    research_flow = create_research_workflow(
        name="ai_research", stages=["analyze", "research", "synthesize", "format"]
    )

    # Add pre/post processing hooks
    @research_flow.before_agent_execution
    def pre_process(agent_name: str, state: dict):
        print(f"\n[Pre-Hook] Starting {agent_name} agent...")

    @research_flow.after_agent_execution
    def post_process(agent_name: str, result: any):
        print(f"[Post-Hook] {agent_name} completed successfully")

    # Execute research
    topic = "The impact of generative AI on software development practices"
    print(f"Research Topic: {topic}\n")

    result = await research_flow.arun(
        {
            "messages": [{"role": "user", "content": f"Research: {topic}"}],
            "depth": "comprehensive",
            "audience": "technical leaders",
        }
    )

    print("\n=== Research Results ===")
    # The workflow returns results from each stage
    for stage_name, stage_result in result.items():
        print(f"\n{stage_name.upper()}:")
        if isinstance(stage_result, dict):
            for key, value in stage_result.items():
                print(f"  {key}: {value}")


async def demo_custom_sequential_with_hooks():
    """Demo 3: Custom sequential workflow with advanced hooks."""
    print("\n\n=== Demo 3: Custom Sequential with Advanced Hooks ===\n")

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
        print("\n[Workflow Hook] Starting innovation pipeline...")

    @workflow.before_agent_execution
    def before_agent(agent_name, state):
        execution_log.append(f"→ {agent_name} starting")
        print(f"\n[Agent Hook] {agent_name} is processing...")

    @workflow.after_agent_execution
    def after_agent(agent_name, result):
        execution_log.append(f"✓ {agent_name} completed")
        print(f"[Agent Hook] {agent_name} finished successfully")

    @workflow.after_workflow
    def end_workflow(final_result):
        execution_log.append("=== Workflow Completed ===")
        print("\n[Workflow Hook] Innovation pipeline completed!")
        print("\nExecution Log:")
        for entry in execution_log:
            print(f"  {entry}")

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

    print("\n=== Final Implementation Plan ===")
    if "implementation_planner" in result:
        plan = result["implementation_planner"]
        print(f"Solution Summary: {plan.get('solution_summary', 'N/A')}")
        print(f"Success Metrics: {plan.get('success_metrics', [])}")


async def demo_react_structured_pattern():
    """Demo 4: Using the ReactToStructuredAgent pattern directly."""
    print("\n\n=== Demo 4: React → Structured Pattern ===\n")

    # Use the pattern we created
    agent = create_react_structured_agent(
        name="problem_solver", output_model=StructuredSolution
    )

    # Add monitoring hooks
    @agent.on_reasoning_complete
    def log_reasoning(reasoning_output):
        print(
            f"\n[Reasoning Complete] Found {len(reasoning_output.get('key_factors', []))} key factors"
        )

    @agent.on_structuring_complete
    def log_structuring(structured_output):
        print(
            f"[Structuring Complete] Generated solution with {len(structured_output.get('implementation_steps', []))} steps"
        )

    # Execute
    problem = "How can we reduce technical debt in a large legacy codebase?"
    print(f"Problem: {problem}\n")

    result = await agent.arun(problem)

    print("\n=== Structured Solution ===")
    if isinstance(result, dict):
        print(f"Title: {result.get('solution_summary', 'N/A')}")
        print(f"Implementation Steps: {result.get('implementation_steps', [])}")
        print(f"Risk Mitigation: {result.get('risks', [])}")


async def demo_rag_with_structured_output():
    """Demo 5: RAG agent with structured output."""
    print("\n\n=== Demo 5: RAG Agent with Structured Output ===\n")

    # Create RAG agent with structured output
    rag_agent = create_simple_rag_agent(
        name="knowledge_assistant", temperature=0.3, include_sources=True
    )

    # Add retrieval monitoring
    @rag_agent.on_retrieval
    def log_retrieval(query, documents):
        print(f"\n[Retrieval] Found {len(documents)} documents for: '{query}'")

    @rag_agent.on_answer_generation
    def log_answer(answer):
        print(
            f"[Generation] Created answer with confidence: {answer.get('confidence', 0)}"
        )

    # Ask question
    question = "What are the best practices for implementing microservices?"
    print(f"Question: {question}\n")

    result = await rag_agent.arun(question)

    print("\n=== RAG Answer with Sources ===")
    if isinstance(result, dict):
        print(f"Answer: {result.get('answer', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 0)}")
        print(f"Sources: {result.get('sources', [])}")
        print(f"Follow-up Questions: {result.get('follow_up_questions', [])}")


async def main():
    """Run all demos."""
    print("=" * 80)
    print("SEQUENTIAL MULTI-AGENT DEMOS")
    print("Using patterns built on agent.py, SimpleAgentV3, and EnhancedMultiAgentV4")
    print("=" * 80)

    # Run demos
    await demo_react_to_simple_structured()
    await demo_research_workflow()
    await demo_custom_sequential_with_hooks()
    await demo_react_structured_pattern()
    await demo_rag_with_structured_output()

    print("\n" + "=" * 80)
    print("ALL DEMOS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    # Run with poetry run python sequential_multi_agent_demo.py
    asyncio.run(main())
