"""Example demonstrating the generalized hook system in enhanced agents.

This example shows how the hook patterns from reflection agents have been
generalized to work with any enhanced agent, providing comprehensive
monitoring and processing capabilities.

Key patterns demonstrated:
1. Basic hook usage with decorators
2. Pre/post processing with message transformation
3. Multi-stage workflow monitoring
4. Reflection and grading hooks
5. Factory patterns for common use cases
"""

import asyncio
import contextlib
import logging

from haive.agents.base.hooks import (
    HookContext,
    HookEvent,
    comprehensive_workflow_hook,
    create_multi_stage_hook,
)
from haive.agents.base.pre_post_agent_mixin import (
    create_graded_reflection_agent,
    create_reflection_agent,
)
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Set up logging to see hook events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_basic_hooks():
    """Example 1: Basic hook usage with decorators."""
    # Create a simple agent
    agent = SimpleAgent(
        name="basic_writer",
        engine=AugLLMConfig(
            system_message="You are a helpful writing assistant.", temperature=0.7
        ),
    )

    # Add hooks using decorators
    @agent.before_run
    def log_start(context: HookContext):
        pass

    @agent.after_run
    def log_completion(context: HookContext):
        if context.output_data:
            str(context.output_data).replace("\n", " ")[:100]

    @agent.on_error
    def handle_error(context: HookContext):
        pass

    # Execute agent
    with contextlib.suppress(Exception):
        await agent.arun("Write a brief haiku about programming")


async def example_pre_post_processing():
    """Example 2: Pre/post processing with message transformation."""
    # Create main agent
    main_agent = SimpleAgent(
        name="story_writer",
        engine=AugLLMConfig(
            system_message="You are a creative story writer.", temperature=0.8
        ),
    )

    # Create reflection agent
    reflection_agent = SimpleAgent(
        name="story_critic",
        engine=AugLLMConfig(
            system_message="You are a literary critic who improves stories.",
            temperature=0.4,
        ),
    )

    # Set up pre/post processing
    main_agent.post_agent = reflection_agent
    main_agent.use_post_transform = True
    main_agent.post_transform_type = "reflection"

    # Add hooks to monitor the process
    @main_agent.post_process
    def monitor_post_processing(context: HookContext):
        if context.post_agent_result:
            pass

    @main_agent.before_message_transform
    def monitor_transformation(context: HookContext):
        if context.messages:
            pass

    @main_agent.after_reflection
    def monitor_reflection(context: HookContext):
        pass

    # Execute with pre/post processing
    try:
        result = await main_agent.arun(
            "Write a short story about a robot learning to dream"
        )

        # Show the structured result
        if isinstance(result, dict) and "transformations_applied" in result:
            pass

    except Exception:
        pass


async def example_multi_stage_monitoring():
    """Example 3: Multi-stage workflow monitoring."""
    # Create an agent with multiple processing stages
    agent = SimpleAgent(
        name="research_analyst",
        engine=AugLLMConfig(
            system_message="You are a research analyst who provides detailed analysis.",
            temperature=0.6,
        ),
    )

    # Add multi-stage monitoring hook
    multi_stage_hook = create_multi_stage_hook(["analysis", "validation", "formatting"])

    agent.add_hook(HookEvent.PRE_PROCESS, multi_stage_hook)
    agent.add_hook(HookEvent.POST_PROCESS, multi_stage_hook)
    agent.add_hook(HookEvent.AFTER_STRUCTURED_OUTPUT, multi_stage_hook)

    # Add comprehensive workflow monitoring
    agent.add_hook(HookEvent.BEFORE_RUN, comprehensive_workflow_hook)
    agent.add_hook(HookEvent.AFTER_RUN, comprehensive_workflow_hook)
    agent.add_hook(HookEvent.ON_ERROR, comprehensive_workflow_hook)

    # Execute agent
    try:
        # Manually trigger pre/post process events to simulate multi-stage workflow
        agent.execute_hooks(HookEvent.PRE_PROCESS)

        await agent.arun("Analyze the current trends in artificial intelligence")

        # Simulate stage completions
        agent.execute_hooks(HookEvent.AFTER_STRUCTURED_OUTPUT)
        agent.execute_hooks(HookEvent.POST_PROCESS)

    except Exception:
        pass


async def example_reflection_factory_pattern():
    """Example 4: Using factory patterns for reflection agents."""
    # Create base agent
    base_agent = SimpleAgent(
        name="essay_writer",
        engine=AugLLMConfig(
            system_message="You are an academic essay writer.", temperature=0.7
        ),
    )

    # Use factory to add reflection capabilities
    reflection_agent = create_reflection_agent(base_agent)

    # Add hooks to monitor reflection process
    @reflection_agent.before_reflection
    def track_reflection_start(context: HookContext):
        pass

    @reflection_agent.after_reflection
    def track_reflection_end(context: HookContext):
        if context.reflection_data:
            pass

    # Execute with reflection
    try:
        result = await reflection_agent.arun(
            "Write an essay about the impact of AI on education"
        )

        if isinstance(result, dict) and "processing_stages" in result:
            pass

    except Exception:
        pass


async def example_graded_reflection_pattern():
    """Example 5: Graded reflection with comprehensive monitoring."""
    # Create base agent
    base_agent = SimpleAgent(
        name="proposal_writer",
        engine=AugLLMConfig(
            system_message="You are a business proposal writer.", temperature=0.6
        ),
    )

    # Create grading agent
    grading_agent = SimpleAgent(
        name="proposal_grader",
        engine=AugLLMConfig(
            system_message="You are an expert who grades business proposals on clarity, feasibility, and impact.",
            temperature=0.1,
        ),
    )

    # Create reflection agent
    reflection_agent = SimpleAgent(
        name="proposal_improver",
        engine=AugLLMConfig(
            system_message="You improve business proposals based on grades and feedback.",
            temperature=0.4,
        ),
    )

    # Use factory to create graded reflection agent
    enhanced_agent = create_graded_reflection_agent(
        main_agent=base_agent,
        grading_agent=grading_agent,
        reflection_agent=reflection_agent,
    )

    # Add comprehensive monitoring
    @enhanced_agent.before_grading
    def track_grading(context: HookContext):
        pass

    @enhanced_agent.after_grading
    def track_grading_complete(context: HookContext):
        if context.grade_data:
            pass

    @enhanced_agent.before_reflection
    def track_improvement(context: HookContext):
        if context.grade_data:
            pass

    # Execute graded reflection workflow
    try:
        result = await enhanced_agent.arun(
            "Write a proposal for implementing AI in small businesses"
        )

        if isinstance(result, dict) and "transformations_applied" in result:
            pass

    except Exception:
        pass


async def example_custom_hook_development():
    """Example 6: Developing custom hooks for specific use cases."""
    # Create agent
    agent = SimpleAgent(
        name="content_creator",
        engine=AugLLMConfig(
            system_message="You are a content creator who writes engaging articles.",
            temperature=0.8,
        ),
    )

    # Custom hook for content quality tracking
    content_metrics = {
        "word_count": 0,
        "readability_score": 0,
        "engagement_factors": [],
    }

    def content_quality_hook(context: HookContext):
        """Custom hook to track content quality metrics."""
        if context.event == HookEvent.AFTER_RUN:
            if context.output_data and isinstance(context.output_data, dict):
                # Simulate content analysis
                content = str(context.output_data)
                content_metrics["word_count"] = len(content.split())
                content_metrics["readability_score"] = min(
                    100, max(0, 100 - len(content) // 50)
                )
                content_metrics["engagement_factors"] = [
                    "storytelling",
                    "examples",
                    "call_to_action",
                ]

    # Custom hook for performance monitoring
    performance_data = {"start_time": None, "end_time": None, "duration": 0}

    def performance_monitoring_hook(context: HookContext):
        """Custom hook to monitor performance."""
        import time

        if context.event == HookEvent.BEFORE_RUN:
            performance_data["start_time"] = time.time()

        elif context.event == HookEvent.AFTER_RUN:
            performance_data["end_time"] = time.time()
            performance_data["duration"] = (
                performance_data["end_time"] - performance_data["start_time"]
            )

    # Add custom hooks
    agent.add_hook(HookEvent.BEFORE_RUN, performance_monitoring_hook)
    agent.add_hook(HookEvent.AFTER_RUN, performance_monitoring_hook)
    agent.add_hook(HookEvent.AFTER_RUN, content_quality_hook)

    # Execute with custom monitoring
    with contextlib.suppress(Exception):
        await agent.arun(
            "Write an engaging article about the future of sustainable technology"
        )


async def main():
    """Run all hook examples."""
    try:
        await example_basic_hooks()
        await example_pre_post_processing()
        await example_multi_stage_monitoring()
        await example_reflection_factory_pattern()
        await example_graded_reflection_pattern()
        await example_custom_hook_development()

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())
