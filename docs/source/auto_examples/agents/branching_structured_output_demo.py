#!/usr/bin/env python3
"""Branching and Structured Output Demo - V3/V4 Architecture.

This demo shows how branching and structured output models work together:
1. Agent produces structured output
2. Routing function uses structured output to decide next agent
3. Different agents handle different branches with their own structured outputs
4. State flows consistently across all branches
"""

import asyncio
from typing import List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.simple.agent_v3 import SimpleAgentV3

# ========================================================================
# STRUCTURED OUTPUT MODELS
# ========================================================================


class TaskClassification(BaseModel):
    """Classification of incoming task."""

    task_type: str = Field(description="creative, analytical, or technical")
    complexity_score: float = Field(ge=0.0, le=1.0, description="Complexity rating")
    estimated_time: int = Field(description="Estimated minutes to complete")
    requires_tools: bool = Field(description="Whether task needs external tools")
    category: str = Field(description="More specific category within task_type")


class CreativeResult(BaseModel):
    """Result from creative processing."""

    creative_output: str = Field(description="Creative work produced")
    inspiration_sources: List[str] = Field(description="Sources of inspiration used")
    creativity_score: float = Field(
        ge=0.0, le=1.0, description="Self-assessed creativity"
    )
    additional_ideas: List[str] = Field(description="Additional creative ideas")


class AnalyticalResult(BaseModel):
    """Result from analytical processing."""

    analysis: str = Field(description="Detailed analysis")
    key_findings: List[str] = Field(description="Main findings from analysis")
    confidence_level: float = Field(
        ge=0.0, le=1.0, description="Confidence in analysis"
    )
    recommendations: List[str] = Field(description="Actionable recommendations")
    data_sources: List[str] = Field(description="Sources used in analysis")


class TechnicalResult(BaseModel):
    """Result from technical processing."""

    solution: str = Field(description="Technical solution provided")
    implementation_steps: List[str] = Field(description="Steps to implement")
    complexity_assessment: str = Field(description="Technical complexity assessment")
    required_skills: List[str] = Field(description="Skills needed for implementation")
    estimated_effort: str = Field(description="Effort estimate")


class FinalSummary(BaseModel):
    """Final consolidated summary."""

    task_summary: str = Field(description="Summary of what was accomplished")
    processing_path: str = Field(description="Which processing path was taken")
    quality_score: float = Field(
        ge=0.0, le=1.0, description="Overall quality assessment"
    )
    key_outputs: List[str] = Field(description="Main outputs produced")
    next_steps: Optional[List[str]] = Field(description="Suggested next steps")


# ========================================================================
# ROUTING FUNCTIONS
# ========================================================================


def route_by_task_type(state) -> str:
    """Route based on task classification."""
    classification = state.get("task_classification", {})
    task_type = classification.get("task_type", "analytical")
    complexity = classification.get("complexity_score", 0.5)

    print(f"🔀 Routing decision: task_type='{task_type}', complexity={complexity}")

    # Route based on task type and complexity
    if task_type == "creative":
        return "creative_processor"
    elif task_type == "technical":
        return "technical_processor"
    elif task_type == "analytical":
        if complexity > 0.7:
            return "complex_analytical_processor"
        else:
            return "simple_analytical_processor"
    else:
        return "simple_analytical_processor"  # Default fallback


def route_to_summary(state) -> str:
    """Always route to summary - this demonstrates reconvergence."""
    return "summarizer"


# ========================================================================
# MAIN DEMO
# ========================================================================


async def main():
    """Demonstrate branching with structured output."""
    print("🌳 BRANCHING & STRUCTURED OUTPUT DEMO")
    print("=" * 80)
    print("Flow: Classifier → [Creative|Analytical|Technical] → Summarizer")
    print("=" * 80)

    # Step 1: Create classifier agent
    classifier = SimpleAgentV3(
        name="classifier",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a task classifier. Analyze tasks and provide structured classification.",
            structured_output_model=TaskClassification,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Classify this task:

{task_description}

Provide structured classification with:
- Task type (creative, analytical, or technical)
- Complexity score (0.0-1.0)
- Estimated time in minutes
- Whether it requires external tools
- Specific category within the task type""",
                ),
            ]
        ),
    )

    # Step 2: Create specialized processing agents
    creative_processor = SimpleAgentV3(
        name="creative_processor",
        engine=AugLLMConfig(
            temperature=0.8,
            system_message="You are a creative specialist. Generate innovative, original creative work.",
            structured_output_model=CreativeResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Based on this classified task:

Task Type: {task_type}
Category: {category}
Complexity: {complexity_score}
Original Task: {task_description}

Create innovative creative work with inspiration sources and additional ideas.""",
                ),
            ]
        ),
    )

    simple_analytical_processor = SimpleAgentV3(
        name="simple_analytical_processor",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are an analytical specialist for straightforward analysis tasks.",
            structured_output_model=AnalyticalResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Analyze this task:

Task Type: {task_type}
Category: {category}  
Complexity: {complexity_score}
Original Task: {task_description}

Provide structured analysis with findings, recommendations, and confidence level.""",
                ),
            ]
        ),
    )

    complex_analytical_processor = SimpleAgentV3(
        name="complex_analytical_processor",
        engine=AugLLMConfig(
            temperature=0.2,
            system_message="You are a senior analytical specialist for complex, high-stakes analysis.",
            structured_output_model=AnalyticalResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Perform deep analysis of this complex task:

Task Type: {task_type}
Category: {category}
Complexity: {complexity_score}
Original Task: {task_description}

Provide comprehensive structured analysis with detailed findings and high-confidence recommendations.""",
                ),
            ]
        ),
    )

    technical_processor = SimpleAgentV3(
        name="technical_processor",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a technical specialist. Provide detailed technical solutions.",
            structured_output_model=TechnicalResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Solve this technical task:

Task Type: {task_type}
Category: {category}
Complexity: {complexity_score}
Original Task: {task_description}

Provide detailed technical solution with implementation steps and effort estimates.""",
                ),
            ]
        ),
    )

    # Step 3: Create summarizer that reconverges all branches
    summarizer = SimpleAgentV3(
        name="summarizer",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are a summary specialist. Consolidate processing results into final summary.",
            structured_output_model=FinalSummary,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Summarize the completed processing:

Original Task: {task_description}
Classification: {task_classification}

Processing Results:
{processing_results}

Create a final summary with quality assessment and next steps.""",
                ),
            ]
        ),
    )

    # Step 4: Create branching workflow
    print("✅ Creating agents...")
    workflow = EnhancedMultiAgentV4(
        name="branching_workflow",
        agents=[
            classifier,
            creative_processor,
            simple_analytical_processor,
            complex_analytical_processor,
            technical_processor,
            summarizer,
        ],
        execution_mode="manual",  # Manual mode for custom routing
    )

    print(f"✅ Created workflow with {len(workflow.agents)} agents")

    # Step 5: Add conditional routing
    print("🔗 Setting up branching logic...")

    # First branch: Classifier → Specialized processors
    workflow.add_multi_conditional_edge(
        from_agent="classifier",
        condition=route_by_task_type,
        routes={
            "creative_processor": "creative_processor",
            "simple_analytical_processor": "simple_analytical_processor",
            "complex_analytical_processor": "complex_analytical_processor",
            "technical_processor": "technical_processor",
        },
        default="simple_analytical_processor",
    )

    # Reconvergence: All processors → Summarizer
    for processor in [
        "creative_processor",
        "simple_analytical_processor",
        "complex_analytical_processor",
        "technical_processor",
    ]:
        workflow.add_conditional_edge(
            from_agent=processor, condition=route_to_summary, true_agent="summarizer"
        )

    print("✅ Branching logic configured")

    # Step 6: Test different task types
    test_tasks = [
        {
            "description": "Write a creative short story about AI and humanity",
            "expected_path": "classifier → creative_processor → summarizer",
        },
        {
            "description": "Analyze the performance metrics of our Q3 sales data and identify trends",
            "expected_path": "classifier → simple_analytical_processor → summarizer",
        },
        {
            "description": "Perform comprehensive competitive analysis of the enterprise AI market including market sizing, key players, growth projections, and strategic recommendations for market entry",
            "expected_path": "classifier → complex_analytical_processor → summarizer",
        },
        {
            "description": "Design a microservices architecture for a high-traffic e-commerce platform with Redis caching, PostgreSQL database, and Kubernetes orchestration",
            "expected_path": "classifier → technical_processor → summarizer",
        },
    ]

    # Step 7: Execute tests
    for i, test_case in enumerate(test_tasks, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test_case['description'][:60]}...")
        print(f"Expected: {test_case['expected_path']}")
        print("=" * 80)

        # Create proper state for workflow
        initial_state = {
            "messages": [HumanMessage(content=test_case["description"])],
            "task_description": test_case["description"],
            "agent_states": {},
            "execution_order": [],
            "current_agent": None,
        }

        try:
            result = await workflow.arun(initial_state)

            print(f"\n🎯 RESULTS FOR TEST {i}:")
            print("-" * 40)

            # Show classification results
            if hasattr(result, "task_classification"):
                classification = result.task_classification
                print(f"📊 Classification:")
                print(f"   Task Type: {classification.get('task_type', 'N/A')}")
                print(f"   Complexity: {classification.get('complexity_score', 0):.2f}")
                print(f"   Category: {classification.get('category', 'N/A')}")
                print(
                    f"   Requires Tools: {classification.get('requires_tools', False)}"
                )

            # Show processing results
            processing_results = []
            for field_name in [
                "creative_result",
                "analytical_result",
                "technical_result",
            ]:
                if hasattr(result, field_name):
                    processing_results.append(field_name)

            if processing_results:
                print(f"🛠️  Processing Results: {', '.join(processing_results)}")

            # Show final summary
            if hasattr(result, "final_summary"):
                summary = result.final_summary
                print(f"📋 Final Summary:")
                print(f"   Processing Path: {summary.get('processing_path', 'N/A')}")
                print(f"   Quality Score: {summary.get('quality_score', 0):.2f}")
                print(f"   Key Outputs: {len(summary.get('key_outputs', []))} items")

            print(f"✅ Test {i} completed successfully!")

        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n{'='*80}")
    print("🌳 BRANCHING DEMO COMPLETED")
    print("Key Features Demonstrated:")
    print("✅ Structured output drives routing decisions")
    print("✅ Different agents handle different task types")
    print("✅ State flows consistently across all branches")
    print("✅ Branches reconverge for final processing")
    print("✅ Complex conditional routing with fallbacks")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
