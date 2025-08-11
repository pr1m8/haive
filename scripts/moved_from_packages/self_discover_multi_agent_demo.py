#!/usr/bin/env python3
"""Self-Discover Multi-Agent Demo - Working Implementation.

This demo implements the Self-Discover reasoning pattern using working agents:
1. Selector Agent - Select relevant reasoning modules
2. Adapter Agent - Adapt modules for specific task
3. Structurer Agent - Create structured reasoning plan
4. Executor Agent - Execute the plan to solve the task

Uses EnhancedMultiAgentV4 for coordination and SimpleAgentV3 as the base.
"""

import asyncio

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Import working agents
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field


# Structured output models for each stage
class SelectedModule(BaseModel):
    """A reasoning module selected for the task."""

    module_name: str = Field(description="Name of the reasoning module")
    relevance: str = Field(description="Why this module is relevant")
    contribution: str = Field(description="How it will help solve the task")


class ModuleSelection(BaseModel):
    """Output from the Selector Agent."""

    task_analysis: str = Field(description="Analysis of the task")
    selected_modules: list[SelectedModule] = Field(
        description="3-5 selected reasoning modules", min_length=3, max_length=5
    )
    selection_rationale: str = Field(description="Overall selection rationale")


class AdaptedModule(BaseModel):
    """A reasoning module adapted for the specific task."""

    module_name: str = Field(description="Name of the module")
    specific_strategy: str = Field(description="Task-specific strategy")
    action_steps: str = Field(description="Concrete steps to apply this module")


class ModuleAdaptation(BaseModel):
    """Output from the Adapter Agent."""

    adaptation_overview: str = Field(description="Overview of adaptations made")
    adapted_modules: list[AdaptedModule] = Field(description="Adapted modules")
    integration_approach: str = Field(description="How modules work together")


class ReasoningStep(BaseModel):
    """A step in the reasoning plan."""

    step_number: int = Field(description="Step number in the plan")
    step_description: str = Field(description="What to do in this step")
    module_used: str = Field(description="Which reasoning module is applied")
    expected_output: str = Field(description="What this step should produce")


class ReasoningStructure(BaseModel):
    """Output from the Structurer Agent."""

    plan_overview: str = Field(description="Overview of the reasoning plan")
    reasoning_steps: list[ReasoningStep] = Field(description="Ordered steps")
    success_criteria: str = Field(description="How to know if the plan worked")


class TaskSolution(BaseModel):
    """Output from the Executor Agent."""

    final_answer: str = Field(description="The final answer to the task")
    reasoning_trace: str = Field(description="Step-by-step reasoning process")
    confidence_level: str = Field(description="Confidence in the solution")
    alternative_approaches: str = Field(description="Other ways to solve this")


# Default reasoning modules available for selection
DEFAULT_REASONING_MODULES = """
1. Critical Thinking - Analyze assumptions, evaluate evidence, identify biases
2. Pattern Recognition - Identify patterns, structures, and relationships
3. Decomposition - Break complex problems into manageable parts
4. Systems Thinking - Consider interactions, feedback loops, and emergent properties
5. Analogical Reasoning - Draw parallels with similar known problems
6. Causal Analysis - Understand cause-and-effect relationships
7. Mathematical Reasoning - Apply quantitative analysis and logic
8. Creative Problem Solving - Generate innovative solutions and alternatives
9. Risk Assessment - Evaluate potential outcomes and uncertainties
10. Optimization - Find the best solution among alternatives
11. Temporal Reasoning - Consider sequence, timing, and temporal relationships
12. Spatial Reasoning - Understand geometric and spatial relationships
13. Logical Reasoning - Apply formal logic and deductive reasoning
14. Empirical Validation - Test hypotheses with evidence and data
15. Meta-cognitive Reflection - Think about thinking and reasoning processes
"""


class SelfDiscoverWorkflow:
    """Self-Discover multi-agent reasoning workflow."""

    def __init__(self):
        """Initialize the Self-Discover workflow with four specialized agents."""
        # Agent 1: Module Selector
        self.selector_agent = SimpleAgentV3(
            name="module_selector",
            engine=AugLLMConfig(
                temperature=0.3,
                structured_output_model=ModuleSelection,
                system_message="""You are an expert at analyzing problems and selecting optimal reasoning strategies.

                Your task is to:
                1. Analyze the given task thoroughly
                2. Select 3-5 most relevant reasoning modules from the available options
                3. Explain why each module is relevant and how it will contribute
                4. Ensure the selected modules complement each other

                Focus on problem-specific relevance and comprehensive coverage.""",
            ),
        )

        # Agent 2: Module Adapter
        self.adapter_agent = SimpleAgentV3(
            name="module_adapter",
            engine=AugLLMConfig(
                temperature=0.4,
                structured_output_model=ModuleAdaptation,
                system_message="""You are an expert at adapting general reasoning strategies for specific tasks.

                Your task is to:
                1. Take the selected reasoning modules
                2. Adapt each module with task-specific strategies
                3. Provide concrete action steps for applying each module
                4. Show how the adapted modules will work together

                Make the modules actionable and specific to the given task.""",
            ),
        )

        # Agent 3: Plan Structurer
        self.structurer_agent = SimpleAgentV3(
            name="plan_structurer",
            engine=AugLLMConfig(
                temperature=0.2,
                structured_output_model=ReasoningStructure,
                system_message="""You are an expert at creating structured, step-by-step reasoning plans.

                Your task is to:
                1. Take the adapted reasoning modules
                2. Create a clear, ordered sequence of reasoning steps
                3. Specify which module is used in each step
                4. Define what each step should accomplish
                5. Establish success criteria for the plan

                Create a logical, executable plan that leads to a solution.""",
            ),
        )

        # Agent 4: Plan Executor
        self.executor_agent = SimpleAgentV3(
            name="plan_executor",
            engine=AugLLMConfig(
                temperature=0.6,
                structured_output_model=TaskSolution,
                system_message="""You are an expert at executing reasoning plans to solve complex tasks.

                Your task is to:
                1. Follow the reasoning plan step by step
                2. Apply each reasoning module as specified
                3. Build upon insights from previous steps
                4. Provide a comprehensive final answer
                5. Reflect on the reasoning process

                Execute systematically and provide clear reasoning traces.""",
            ),
        )

        # Create the coordinated workflow
        self.workflow = EnhancedMultiAgentV4(
            name="self_discover_workflow",
            agents=[
                self.selector_agent,
                self.adapter_agent,
                self.structurer_agent,
                self.executor_agent,
            ],
            execution_mode="sequential",
        )

    async def solve_task(self, task_description: str):
        """Solve a task using the Self-Discover methodology."""
        # Create input for the workflow
        workflow_input = {
            "messages": [
                HumanMessage(
                    content=f"""
            SELF-DISCOVER WORKFLOW INSTRUCTION:

            Task to Solve: {task_description}

            Available Reasoning Modules:
            {DEFAULT_REASONING_MODULES}

            WORKFLOW STAGES:
            1. MODULE SELECTION: Analyze the task and select 3-5 most relevant reasoning modules
            2. MODULE ADAPTATION: Adapt each selected module with specific strategies for this task
            3. PLAN STRUCTURING: Create a step-by-step reasoning plan using the adapted modules
            4. PLAN EXECUTION: Execute the plan systematically to solve the original task

            Please proceed through all four stages sequentially.
            """
                )
            ]
        }

        # Execute the workflow
        result = await self.workflow.arun(workflow_input)

        return result

    def analyze_self_discover_result(self, result):
        """Analyze the results of the Self-Discover workflow."""
        if hasattr(result, "messages"):
            # Track progression through the four stages
            stage_indicators = {
                "module_selection": ["select", "module", "relevant"],
                "adaptation": ["adapt", "specific", "strategy"],
                "structuring": ["plan", "step", "structure"],
                "execution": ["execute", "answer", "solution"],
            }

            content = str(result).lower()

            stage_scores = {}
            for stage, keywords in stage_indicators.items():
                score = sum(1 for keyword in keywords if keyword in content)
                stage_scores[stage] = score

            # Overall quality assessment
            total_score = sum(stage_scores.values())
            max_score = len(stage_indicators) * 3

            if total_score >= max_score * 0.8 or total_score >= max_score * 0.6:
                pass
            else:
                pass

            # Look for structured reasoning indicators
            reasoning_indicators = {
                "structured_output": "structured" in content or "pydantic" in content,
                "step_by_step": "step" in content
                and ("1." in content or "first" in content),
                "module_usage": "module" in content
                and ("reasoning" in content or "strategy" in content),
                "final_answer": "answer" in content
                or "solution" in content
                or "conclusion" in content,
            }

            for _indicator, _present in reasoning_indicators.items():
                pass

        return result


async def demo_problem_solving_task():
    """Demo Self-Discover on a problem-solving task."""
    workflow = SelfDiscoverWorkflow()

    task = """How should a small startup with limited budget approach entering a highly competitive market dominated by large corporations?"""

    result = await workflow.solve_task(task)
    workflow.analyze_self_discover_result(result)

    return result


async def demo_analytical_reasoning_task():
    """Demo Self-Discover on an analytical reasoning task."""
    workflow = SelfDiscoverWorkflow()

    task = """A city is experiencing increased traffic congestion, air pollution, and parking shortages. The mayor has a budget of $50 million and needs to choose between: (A) building a new subway line, (B) expanding bus rapid transit, (C) implementing congestion pricing, or (D) building more parking garages. What should they choose and why?"""

    result = await workflow.solve_task(task)
    workflow.analyze_self_discover_result(result)

    return result


async def demo_creative_problem_solving():
    """Demo Self-Discover on a creative problem-solving task."""
    workflow = SelfDiscoverWorkflow()

    task = """Design an innovative solution to help elderly people who live alone stay connected with their families and maintain their independence while ensuring their safety and wellbeing."""

    result = await workflow.solve_task(task)
    workflow.analyze_self_discover_result(result)

    return result


async def demo_technical_analysis():
    """Demo Self-Discover on a technical analysis task."""
    workflow = SelfDiscoverWorkflow()

    task = """A software company's application is experiencing frequent crashes, slow performance, and user complaints. The development team needs to decide between: (A) rewriting the application from scratch, (B) refactoring the existing codebase, (C) migrating to a new technology stack, or (D) optimizing the current system. What approach should they take?"""

    result = await workflow.solve_task(task)
    workflow.analyze_self_discover_result(result)

    return result


async def main():
    """Run all Self-Discover demos."""
    # Run all demos
    demo_results = {}

    try:
        demo_results["problem_solving"] = await demo_problem_solving_task()
        demo_results["analytical_reasoning"] = await demo_analytical_reasoning_task()
        demo_results["creative_problem_solving"] = await demo_creative_problem_solving()
        demo_results["technical_analysis"] = await demo_technical_analysis()

        for _demo_name, _result in demo_results.items():
            pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
