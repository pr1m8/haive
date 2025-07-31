"""Example: ReactAgent → SimpleAgent Sequential Pattern with EnhancedMultiAgentV4.

This example demonstrates a common pattern where:
1. ReactAgent performs reasoning and analysis with tools
2. SimpleAgent formats the results into structured output

This showcases the enhanced base agent pattern with real LLM execution.
"""

import asyncio

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Define structured output model for the formatter
class AnalysisReport(BaseModel):
    """Structured analysis report output."""

    title: str = Field(..., description="Report title")
    summary: str = Field(..., description="Executive summary")
    key_findings: list[str] = Field(..., description="List of key findings")
    recommendations: list[str] = Field(..., description="List of recommendations")
    confidence_score: float = Field(..., description="Confidence score 0-1")


# Create example tools for ReactAgent
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2")

    Returns:
        str: Result of the calculation
    """
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating {expression}: {e!s}"


@tool
def word_counter(text: str) -> str:
    """Count words in a text.

    Args:
        text: Text to count words in

    Returns:
        str: Word count information
    """
    words = text.split()
    return f"The text contains {len(words)} words"


@tool
def sentiment_analyzer(text: str) -> str:
    """Analyze sentiment of text (mock implementation).

    Args:
        text: Text to analyze

    Returns:
        str: Sentiment analysis result
    """
    # Mock sentiment analysis
    positive_words = ["good", "great", "excellent", "wonderful", "amazing", "positive"]
    negative_words = ["bad", "poor", "terrible", "awful", "negative", "worse"]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
        score = 0.7 + (0.3 * min(positive_count / 5, 1))
    elif negative_count > positive_count:
        sentiment = "negative"
        score = 0.3 - (0.2 * min(negative_count / 5, 1))
    else:
        sentiment = "neutral"
        score = 0.5

    return f"Sentiment: {sentiment} (confidence: {score:.2f})"


async def main():
    """Run ReactAgent → SimpleAgent sequential pattern example."""
    print("=" * 80)
    print("EnhancedMultiAgentV4 Example: ReactAgent → SimpleAgent Pattern")
    print("=" * 80)

    # Create configuration for agents
    config = AugLLMConfig(
        temperature=0.3, max_tokens=1000  # Low temperature for consistent results
    )

    # Step 1: Create ReactAgent for reasoning and analysis
    analyzer = ReactAgent(
        name="analyzer",
        engine=config,
        tools=[calculator, word_counter, sentiment_analyzer],
        system_message=(
            "You are an analytical agent that uses tools to gather data and perform analysis. "
            "Be thorough in your analysis and use multiple tools when appropriate. "
            "Always provide detailed findings and insights."
        ),
    )

    # Step 2: Create SimpleAgent for structured output formatting
    formatter = SimpleAgent(
        name="formatter",
        engine=config,
        structured_output_model=AnalysisReport,
        system_message=(
            "You are a report formatting agent. Take the analysis provided and format it into "
            "a professional report with clear findings and recommendations. "
            "Extract key insights and provide actionable recommendations."
        ),
    )

    # Step 3: Create multi-agent workflow
    workflow = EnhancedMultiAgentV4(
        name="analysis_workflow",
        agents=[analyzer, formatter],
        execution_mode="sequential",  # Analyzer runs first, then formatter
        build_mode="auto",  # Build graph automatically
    )

    # Display workflow configuration
    print("\nWorkflow Configuration:")
    workflow.display_info()

    # Step 4: Execute workflow with a complex task
    test_task = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Analyze the following customer feedback and provide a comprehensive report:\n\n"
                    "'The product quality is excellent and I'm very satisfied with my purchase. "
                    "However, the shipping took 15 days which was much longer than the promised 5-7 days. "
                    "The customer service was helpful when I contacted them about the delay. "
                    "Overall, I would rate my experience 7/10. The product itself deserves 10/10 but "
                    "the shipping experience brings down the overall score. I would still recommend "
                    "this to others but with a warning about potential shipping delays.'\n\n"
                    "Please analyze the sentiment, calculate relevant metrics, and provide recommendations."
                ),
            }
        ]
    }

    print("\nExecuting workflow...")
    print("-" * 40)

    try:
        # Execute the workflow
        result = await workflow.arun(test_task)

        print("\n✅ Workflow completed successfully!")

        # Extract the formatted report from the result
        if hasattr(result, "analysis_report"):
            report = result.analysis_report
            print("\n📊 Formatted Analysis Report:")
            print(f"\nTitle: {report.title}")
            print(f"\nSummary:\n{report.summary}")
            print("\nKey Findings:")
            for i, finding in enumerate(report.key_findings, 1):
                print(f"  {i}. {finding}")
            print("\nRecommendations:")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")
            print(f"\nConfidence Score: {report.confidence_score:.2f}")
        else:
            print("\nRaw result:")
            print(result)

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)


# Advanced example with conditional routing
async def advanced_example():
    """Advanced example with conditional routing based on complexity."""
    print("\n" + "=" * 80)
    print("Advanced Example: Conditional Routing Based on Complexity")
    print("=" * 80)

    config = AugLLMConfig(temperature=0.3)

    # Create agents
    classifier = SimpleAgent(
        name="classifier",
        engine=config,
        system_message="Classify the complexity of the task as 'simple' or 'complex'.",
    )

    simple_processor = SimpleAgent(
        name="simple_processor",
        engine=config,
        system_message="Process simple tasks quickly with basic analysis.",
    )

    complex_processor = ReactAgent(
        name="complex_processor",
        engine=config,
        tools=[calculator, word_counter, sentiment_analyzer],
        system_message="Process complex tasks with detailed tool-based analysis.",
    )

    # Create conditional workflow
    workflow = EnhancedMultiAgentV4(
        name="adaptive_workflow",
        agents=[classifier, simple_processor, complex_processor],
        execution_mode="conditional",
        build_mode="manual",  # We'll add edges manually
    )

    # Define routing condition
    def check_complexity(state) -> bool:
        """Check if task is complex based on classifier output."""
        # In real implementation, this would check the classifier's output
        # For now, we'll use a simple heuristic
        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", "")
            return "complex" in content.lower()
        return False

    # Add conditional routing
    workflow.add_conditional_edge(
        from_agent="classifier",
        condition=check_complexity,
        true_agent="complex_processor",
        false_agent="simple_processor",
    )

    # Build the workflow
    workflow.build()

    print("\nConditional workflow configured!")
    workflow.display_info()

    # Test with different complexity levels
    test_cases = [
        {
            "messages": [
                {"role": "user", "content": "What is 2 + 2? This is a simple question."}
            ]
        },
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "This is a complex analysis task. Calculate the compound interest on $10,000 "
                        "at 5% annual rate for 10 years, analyze the sentiment of this message, "
                        "and count the total words used."
                    ),
                }
            ]
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        try:
            result = await workflow.arun(test_case)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Run the basic example
    asyncio.run(main())

    # Uncomment to run the advanced example
