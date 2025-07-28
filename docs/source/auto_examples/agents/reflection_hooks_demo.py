#!/usr/bin/env python3
"""Reflection and Hooks Demo - Advanced multi-agent patterns with reflection.

This demo showcases:
1. Pre/post processing agents with reflection
2. Hook system for monitoring agent execution
3. Structured output with reflection patterns
4. Multi-stage workflows with quality gates
"""

import asyncio
from typing import Any, Dict, List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.base.hooks import HookContext, HookEvent
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent_v3 import SimpleAgentV3


# Structured models for reflection patterns
class ContentQuality(BaseModel):
    """Quality assessment of generated content."""

    clarity_score: float = Field(ge=0.0, le=1.0, description="Clarity rating")
    completeness_score: float = Field(ge=0.0, le=1.0, description="Completeness rating")
    accuracy_score: float = Field(ge=0.0, le=1.0, description="Accuracy rating")
    overall_score: float = Field(ge=0.0, le=1.0, description="Overall quality score")
    improvement_areas: List[str] = Field(description="Areas needing improvement")
    strengths: List[str] = Field(description="Strong points in the content")


class ReflectionResult(BaseModel):
    """Result of reflection analysis."""

    original_content: str = Field(description="Original content analyzed")
    quality_assessment: ContentQuality = Field(description="Quality scores")
    suggested_improvements: List[str] = Field(description="Specific improvements")
    revised_content: str = Field(description="Improved version of content")


class FinalOutput(BaseModel):
    """Final polished output after reflection."""

    title: str = Field(description="Content title")
    content: str = Field(description="Final polished content")
    metadata: Dict[str, Any] = Field(description="Additional metadata")
    quality_metrics: ContentQuality = Field(description="Final quality scores")
    revision_history: List[str] = Field(description="History of revisions")


async def demo_reflection_workflow():
    """Demo 1: Content creation with reflection and improvement."""
    print("\n=== Demo 1: Reflection-Enhanced Content Creation ===\n")

    # Create content generator
    content_creator = SimpleAgentV3(
        name="content_creator",
        engine=AugLLMConfig(
            temperature=0.7,
            system_message="You are a creative content writer. Generate engaging content.",
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    "Create content about: {topic}\nTone: {tone}\nLength: {length}",
                ),
            ]
        ),
    )

    # Create reflection agent with structured output
    reflection_agent = SimpleAgentV3(
        name="reflection_agent",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a critical content reviewer. Analyze content quality and suggest improvements.",
            structured_output_model=ReflectionResult,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    "Analyze this content:\n\n{content}\n\nProvide detailed quality assessment and improvements.",
                ),
            ]
        ),
    )

    # Create improvement agent
    improvement_agent = SimpleAgentV3(
        name="improvement_agent",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are an expert editor. Improve content based on feedback.",
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Original content: {original_content}
            
Quality Assessment:
- Clarity: {clarity_score}
- Completeness: {completeness_score}
- Accuracy: {accuracy_score}

Improvement Areas: {improvement_areas}
Suggested Improvements: {suggested_improvements}

Please create an improved version addressing all feedback.""",
                ),
            ]
        ),
    )

    # Create final formatter
    final_formatter = SimpleAgentV3(
        name="final_formatter",
        engine=AugLLMConfig(
            temperature=0.2,
            system_message="You are a professional formatter. Create polished final output.",
            structured_output_model=FinalOutput,
        ),
    )

    # Create workflow with reflection pattern
    workflow = EnhancedMultiAgentV4(
        name="reflection_workflow",
        agents=[content_creator, reflection_agent, improvement_agent, final_formatter],
        execution_mode="sequential",
    )

    # Add comprehensive hooks
    execution_metrics = {
        "iterations": 0,
        "quality_improvements": [],
        "processing_time": {},
    }

    @workflow.before_agent_execution
    def track_execution(agent_name: str, state: dict):
        execution_metrics["iterations"] += 1
        print(
            f"\n[Pre-Hook] {agent_name} starting (iteration {execution_metrics['iterations']})"
        )

    @workflow.after_agent_execution
    def track_results(agent_name: str, result: Any):
        print(f"[Post-Hook] {agent_name} completed")

        # Track quality improvements
        if agent_name == "reflection_agent" and isinstance(result, dict):
            quality = result.get("quality_assessment", {})
            overall = quality.get("overall_score", 0)
            execution_metrics["quality_improvements"].append(overall)
            print(f"  Quality Score: {overall:.2f}")

    # Execute workflow
    result = await workflow.arun(
        {
            "topic": "The future of AI in healthcare",
            "tone": "professional yet accessible",
            "length": "medium (500 words)",
            "messages": [{"role": "user", "content": "Create content"}],
        }
    )

    print("\n=== Reflection Workflow Results ===")
    print(f"Total iterations: {execution_metrics['iterations']}")
    print(f"Quality progression: {execution_metrics['quality_improvements']}")

    if "final_formatter" in result:
        final = result["final_formatter"]
        print(f"\nFinal Title: {final.get('title', 'N/A')}")
        print(f"Quality Metrics: {final.get('quality_metrics', {})}")
        print(f"Revision History: {len(final.get('revision_history', []))} revisions")


async def demo_pre_post_processing():
    """Demo 2: Pre and post processing pattern."""
    print("\n\n=== Demo 2: Pre/Post Processing Pattern ===\n")

    # Pre-processor: Analyze and prepare input
    preprocessor = SimpleAgentV3(
        name="preprocessor",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a data preprocessor. Analyze input and prepare it for processing.",
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Raw input: {raw_input}
            
Analyze this input and prepare:
1. Clean and normalized version
2. Key entities and concepts
3. Processing requirements
4. Potential challenges""",
                ),
            ]
        ),
    )

    # Main processor with tools
    @tool
    def entity_extractor(text: str) -> str:
        """Extract entities from text."""
        return f"Extracted entities from '{text[:50]}...': [Person: John, Company: TechCorp, Date: 2024]"

    @tool
    def sentiment_analyzer(text: str) -> str:
        """Analyze sentiment of text."""
        return f"Sentiment analysis: Positive (0.8), Professional tone, Constructive feedback"

    main_processor = ReactAgent(
        name="main_processor",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are the main processor. Use tools to analyze prepared data.",
            tools=[entity_extractor, sentiment_analyzer],
        ),
    )

    # Post-processor: Enhance and finalize output
    postprocessor = SimpleAgentV3(
        name="postprocessor",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a post-processor. Enhance and finalize the output.",
            structured_output_model=FinalOutput,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Processing results: {processing_results}
            
Create final polished output with:
1. Clear structure
2. Enhanced formatting
3. Metadata
4. Quality metrics""",
                ),
            ]
        ),
    )

    # Create workflow
    workflow = EnhancedMultiAgentV4(
        name="pre_post_workflow",
        agents=[preprocessor, main_processor, postprocessor],
        execution_mode="sequential",
    )

    # Add stage-specific hooks
    stage_outputs = {}

    @workflow.after_agent_execution
    def capture_stage_output(agent_name: str, result: Any):
        stage_outputs[agent_name] = result
        print(f"\n[Stage Output - {agent_name}]")
        if isinstance(result, dict):
            for key in list(result.keys())[:3]:  # Show first 3 keys
                print(f"  {key}: {str(result[key])[:100]}...")

    # Execute
    raw_input = """
    Subject: Quarterly Review Meeting
    From: John Smith (TechCorp)
    Date: March 15, 2024
    
    I wanted to share some thoughts on our Q1 performance. Overall, I'm pleased with 
    the progress we've made, particularly in the AI integration project. The team has 
    shown exceptional dedication, and our metrics are trending positively.
    
    However, we need to address some challenges in the deployment pipeline...
    """

    result = await workflow.arun(
        {
            "raw_input": raw_input,
            "messages": [{"role": "user", "content": "Process this communication"}],
        }
    )

    print("\n=== Pre/Post Processing Results ===")
    print(f"Stages completed: {list(stage_outputs.keys())}")

    if "postprocessor" in result:
        final = result["postprocessor"]
        print(f"\nFinal Title: {final.get('title', 'N/A')}")
        print(f"Metadata: {final.get('metadata', {})}")


async def demo_multi_stage_reflection():
    """Demo 3: Multi-stage reflection with conditional improvement."""
    print("\n\n=== Demo 3: Multi-Stage Reflection with Quality Gates ===\n")

    # Quality threshold for acceptance
    QUALITY_THRESHOLD = 0.85

    # Initial creator
    creator = SimpleAgentV3(
        name="creator",
        engine=AugLLMConfig(
            temperature=0.7,
            system_message="Create initial content based on requirements.",
        ),
    )

    # Quality evaluator
    evaluator = SimpleAgentV3(
        name="evaluator",
        engine=AugLLMConfig(
            temperature=0.2,
            system_message="Evaluate content quality rigorously.",
            structured_output_model=ContentQuality,
        ),
    )

    # Iterative improver
    improver = SimpleAgentV3(
        name="improver",
        engine=AugLLMConfig(
            temperature=0.5, system_message="Improve content based on quality feedback."
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Current content: {content}
            
Quality Scores:
- Clarity: {clarity_score}
- Completeness: {completeness_score}
- Accuracy: {accuracy_score}
- Overall: {overall_score}

Issues: {improvement_areas}

Improve the content to achieve a quality score above {threshold}.""",
                ),
            ]
        ),
    )

    # Final polisher
    polisher = SimpleAgentV3(
        name="polisher",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="Apply final polish to high-quality content.",
        ),
    )

    # Create conditional workflow
    workflow = EnhancedMultiAgentV4(
        name="quality_gate_workflow",
        agents=[creator, evaluator, improver, polisher],
        execution_mode="conditional",
        build_mode="manual",
    )

    # Build graph with conditional routing
    workflow.build()

    # Add conditional routing based on quality
    def check_quality(state: Dict[str, Any]) -> str:
        """Route based on quality score."""
        # Get quality score from evaluator output
        eval_result = state.get("evaluator", {})
        quality = eval_result.get("quality_assessment", {})
        overall_score = quality.get("overall_score", 0)

        if overall_score >= QUALITY_THRESHOLD:
            return "polisher"  # Quality is good, go to final polish
        else:
            return "improver"  # Need improvement

    # Add edges
    workflow.add_edge("creator", "evaluator")
    workflow.add_conditional_edge(
        from_agent="evaluator",
        condition=check_quality,
        true_agent="polisher",
        false_agent="improver",
    )
    workflow.add_edge("improver", "evaluator")  # Loop back for re-evaluation
    workflow.add_edge("polisher", "END")

    # Track iteration count
    iteration_count = {"count": 0, "scores": []}

    @workflow.before_agent_execution
    def track_iterations(agent_name: str, state: dict):
        if agent_name == "evaluator":
            iteration_count["count"] += 1
            print(f"\n[Quality Gate] Evaluation iteration {iteration_count['count']}")

    @workflow.after_agent_execution
    def track_quality(agent_name: str, result: Any):
        if agent_name == "evaluator" and isinstance(result, dict):
            quality = result.get("quality_assessment", {})
            score = quality.get("overall_score", 0)
            iteration_count["scores"].append(score)
            print(f"[Quality Gate] Score: {score:.2f} (Threshold: {QUALITY_THRESHOLD})")

    # Execute
    result = await workflow.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Write a technical blog post about quantum computing",
                }
            ],
            "threshold": QUALITY_THRESHOLD,
        }
    )

    print("\n=== Quality Gate Results ===")
    print(f"Total iterations: {iteration_count['count']}")
    print(f"Quality progression: {[f'{s:.2f}' for s in iteration_count['scores']]}")
    print(
        f"Final quality achieved: {iteration_count['scores'][-1] if iteration_count['scores'] else 'N/A'}"
    )


async def demo_hook_monitoring_system():
    """Demo 4: Comprehensive hook monitoring system."""
    print("\n\n=== Demo 4: Comprehensive Hook Monitoring System ===\n")

    # Create a simple workflow
    analyzer = SimpleAgentV3(name="analyzer", engine=AugLLMConfig(temperature=0.4))

    processor = SimpleAgentV3(name="processor", engine=AugLLMConfig(temperature=0.5))

    finalizer = SimpleAgentV3(name="finalizer", engine=AugLLMConfig(temperature=0.3))

    workflow = EnhancedMultiAgentV4(
        name="monitored_workflow",
        agents=[analyzer, processor, finalizer],
        execution_mode="sequential",
    )

    # Create comprehensive monitoring
    class WorkflowMonitor:
        def __init__(self):
            self.events = []
            self.timings = {}
            self.state_snapshots = {}
            self.errors = []

        def log_event(self, event_type: str, details: Dict[str, Any]):
            self.events.append(
                {
                    "type": event_type,
                    "timestamp": asyncio.get_event_loop().time(),
                    "details": details,
                }
            )

        def print_summary(self):
            print("\n=== Workflow Monitoring Summary ===")
            print(f"Total events: {len(self.events)}")

            # Event type breakdown
            event_types = {}
            for event in self.events:
                event_type = event["type"]
                event_types[event_type] = event_types.get(event_type, 0) + 1

            print("\nEvent breakdown:")
            for event_type, count in event_types.items():
                print(f"  {event_type}: {count}")

            print("\nAgent execution order:")
            agent_events = [e for e in self.events if e["type"] == "agent_start"]
            for i, event in enumerate(agent_events, 1):
                print(f"  {i}. {event['details']['agent_name']}")

            if self.errors:
                print(f"\nErrors encountered: {len(self.errors)}")
                for error in self.errors:
                    print(f"  - {error}")

    monitor = WorkflowMonitor()

    # Add all hook types
    @workflow.before_workflow
    def monitor_start(state):
        monitor.log_event("workflow_start", {"state_keys": list(state.keys())})

    @workflow.after_workflow
    def monitor_end(result):
        monitor.log_event(
            "workflow_end",
            {
                "result_keys": (
                    list(result.keys()) if isinstance(result, dict) else "non-dict"
                )
            },
        )

    @workflow.before_agent_execution
    def monitor_agent_start(agent_name, state):
        monitor.log_event("agent_start", {"agent_name": agent_name})
        monitor.state_snapshots[f"{agent_name}_input"] = state

    @workflow.after_agent_execution
    def monitor_agent_end(agent_name, result):
        monitor.log_event("agent_end", {"agent_name": agent_name})
        monitor.state_snapshots[f"{agent_name}_output"] = result

    @workflow.on_error
    def monitor_error(error, context):
        monitor.errors.append(str(error))
        monitor.log_event("error", {"error": str(error), "context": context})

    # Execute
    result = await workflow.arun(
        {"messages": [{"role": "user", "content": "Analyze market trends in AI"}]}
    )

    # Print monitoring summary
    monitor.print_summary()


async def main():
    """Run all reflection and hook demos."""
    print("=" * 80)
    print("REFLECTION AND HOOKS DEMONSTRATION")
    print("Advanced patterns with pre/post processing and monitoring")
    print("=" * 80)

    await demo_reflection_workflow()
    await demo_pre_post_processing()
    await demo_multi_stage_reflection()
    await demo_hook_monitoring_system()

    print("\n" + "=" * 80)
    print("ALL DEMOS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    # Run with poetry run python reflection_hooks_demo.py
    asyncio.run(main())
