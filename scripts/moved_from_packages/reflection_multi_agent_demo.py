#!/usr/bin/env python3
"""Reflection Multi-Agent Demo - Working Example.

This demo shows how to create a reflection-like pattern using working agents:
1. SimpleAgentV3 for initial response
2. SimpleAgentV3 configured as a "reflection agent" for critique
3. SimpleAgentV3 for improvement
4. EnhancedMultiAgentV4 for coordination

This pattern mimics the reasoning_and_critique reflection module but uses
working components that are production-ready.
"""

import asyncio

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent_v3 import ReactAgentV3

# Import working agents
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


@tool
def research_tool(query: str) -> str:
    """Research tool for gathering information."""
    research_data = {
        "climate_change": "Climate change is causing global temperature rise, extreme weather events, and ecosystem disruption.",
        "ai_ethics": "AI ethics involves fairness, transparency, accountability, privacy, and human autonomy considerations.",
        "renewable_energy": "Renewable energy sources include solar, wind, hydro, and geothermal power technologies.",
        "quantum_computing": "Quantum computing uses quantum mechanical phenomena to process information exponentially faster.",
    }

    query_lower = query.lower()
    for key, info in research_data.items():
        if key.replace("_", " ") in query_lower:
            return f"Research on {key}: {info}"

    return f"General research for '{query}': Additional research may be needed for comprehensive analysis."


class ReflectionMultiAgentSystem:
    """Multi-agent system that mimics reflection patterns using working agents."""

    def __init__(self):
        """Initialize the reflection multi-agent system."""
        # Agent 1: Initial Response Generator (ReactAgent with tools)
        self.initial_responder = ReactAgentV3(
            name="initial_responder",
            engine=AugLLMConfig(
                temperature=0.7,
                tools=[research_tool],
                system_message="""You are an intelligent assistant that provides initial responses to questions.
                Use the research tool when you need additional information.
                Provide comprehensive but concise responses.""",
            ),
            max_iterations=2,
        )

        # Agent 2: Reflection Critic (SimpleAgent configured for critique)
        self.reflection_critic = SimpleAgentV3(
            name="reflection_critic",
            engine=AugLLMConfig(
                temperature=0.3,  # Lower temperature for more analytical critique
                system_message="""You are a critical but constructive reviewer. Your task is to analyze responses and provide specific feedback.

                For each response you review, provide feedback in this format:

                REFLECTION ANALYSIS:
                - Quality Score (1-10): [Your assessment of overall quality]
                - Missing Information: [What important details are missing]
                - Superfluous Content: [What could be removed or simplified]
                - Strengths: [What the response does well]
                - Improvement Suggestions: [Specific actionable recommendations]
                - Overall Assessment: [Whether the response adequately addresses the original question]

                Be thorough but concise in your analysis.""",
            ),
        )

        # Agent 3: Response Improver (SimpleAgent for refinement)
        self.response_improver = SimpleAgentV3(
            name="response_improver",
            engine=AugLLMConfig(
                temperature=0.6,
                system_message="""You are a response improvement specialist. Your job is to take an original response
                and critique feedback, then produce an improved version.

                Guidelines for improvement:
                - Address all missing information identified in the critique
                - Remove or simplify superfluous content
                - Maintain the helpful tone while being more precise
                - Ensure the improved response fully answers the original question
                - Make the response clear, comprehensive, and well-structured""",
            ),
        )

        # Multi-agent coordinator for the reflection workflow
        self.reflection_workflow = EnhancedMultiAgentV4(
            name="reflection_workflow",
            agents=[
                self.initial_responder,
                self.reflection_critic,
                self.response_improver,
            ],
            execution_mode="sequential",
        )

    async def run_reflection_process(self, user_question: str):
        """Run the complete reflection process: respond → reflect → improve."""
        # Execute the sequential workflow
        result = await self.reflection_workflow.arun(
            {
                "messages": [
                    HumanMessage(
                        content=f"""
            REFLECTION WORKFLOW INSTRUCTION:

            Original Question: {user_question}

            WORKFLOW STAGES:
            1. Initial Response: Provide a comprehensive initial answer to the question above
            2. Reflection Analysis: Critically analyze the initial response for quality, completeness, and areas for improvement
            3. Improved Response: Create an enhanced version based on the reflection feedback

            Please proceed through all three stages sequentially.
            """
                    )
                ]
            }
        )

        return result

    def analyze_workflow_result(self, result):
        """Analyze and display the results of the reflection workflow."""
        if hasattr(result, "messages"):
            # Track the progression through agents
            agent_messages = []
            for i, msg in enumerate(result.messages):
                msg_content = (
                    str(msg.content)[:150] + "..."
                    if len(str(msg.content)) > 150
                    else str(msg.content)
                )
                msg_type = type(msg).__name__
                agent_messages.append(f"  {i + 1}. {msg_type}: {msg_content}")

            for msg in agent_messages:
                pass

            # Look for reflection patterns
            content = str(result).lower()
            reflection_indicators = {
                "reflection_analysis": "reflection analysis" in content,
                "quality_score": "quality score" in content or "score" in content,
                "missing_information": "missing" in content,
                "improvement": "improvement" in content or "improved" in content,
                "critique": "critique" in content or "critical" in content,
            }

            for _indicator, _present in reflection_indicators.items():
                pass

            success_score = sum(reflection_indicators.values())

            if success_score >= 4 or success_score >= 3:
                pass
            else:
                pass

        return result


async def demo_basic_reflection():
    """Demo basic reflection workflow."""
    reflection_system = ReflectionMultiAgentSystem()

    question = (
        "What are the key challenges and opportunities for renewable energy adoption?"
    )

    result = await reflection_system.run_reflection_process(question)
    reflection_system.analyze_workflow_result(result)

    return result


async def demo_complex_reasoning_reflection():
    """Demo reflection on complex reasoning task."""
    reflection_system = ReflectionMultiAgentSystem()

    question = """Analyze the ethical implications of AI in healthcare decision-making.
    Consider patient autonomy, algorithmic bias, transparency, and accountability."""

    result = await reflection_system.run_reflection_process(question)
    reflection_system.analyze_workflow_result(result)

    return result


async def demo_research_intensive_reflection():
    """Demo reflection on research-intensive questions."""
    reflection_system = ReflectionMultiAgentSystem()

    question = """How might quantum computing impact climate change research and modeling?
    Include current limitations and future potential."""

    result = await reflection_system.run_reflection_process(question)
    reflection_system.analyze_workflow_result(result)

    return result


async def demo_comparison_with_single_agent():
    """Compare reflection workflow with single agent response."""
    question = "Explain the benefits and risks of artificial intelligence in education."

    # Single agent response

    single_agent = SimpleAgentV3(
        name="single_responder", engine=AugLLMConfig(temperature=0.7)
    )

    single_result = await single_agent.arun(question)

    # Reflection system response

    reflection_system = ReflectionMultiAgentSystem()
    reflection_result = await reflection_system.run_reflection_process(question)

    # Compare complexity and depth
    single_content = str(single_result).lower()
    reflection_content = str(reflection_result).lower()

    depth_indicators = [
        "analysis",
        "consider",
        "however",
        "furthermore",
        "additionally",
        "perspective",
    ]

    sum(1 for indicator in depth_indicators if indicator in single_content)
    sum(1 for indicator in depth_indicators if indicator in reflection_content)

    return single_result, reflection_result


async def main():
    """Run all reflection demos."""
    # Run all demos
    demo_results = {}

    try:
        demo_results["basic"] = await demo_basic_reflection()
        demo_results["complex"] = await demo_complex_reasoning_reflection()
        demo_results["research"] = await demo_research_intensive_reflection()
        demo_results["comparison"] = await demo_comparison_with_single_agent()

        for demo_name, result in demo_results.items():
            if demo_name != "comparison":  # Handle comparison separately
                pass
            else:
                single_result, reflection_result = result

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
