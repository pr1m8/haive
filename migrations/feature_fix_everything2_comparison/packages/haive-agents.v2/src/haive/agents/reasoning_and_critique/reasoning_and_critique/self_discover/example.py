"""Example core module.

This module provides example functionality for the Haive framework.

Functions:
    example_math_problem: Example Math Problem functionality.
    example_svg_interpretation: Example Svg Interpretation functionality.
    example_logical_reasoning: Example Logical Reasoning functionality.
"""

# src/haive/agents/selfdiscover/examples.py

import json
import logging

from langchain_core.prompts import ChatPromptTemplate

from haive.agents.reasoning_and_critique.self_discover.agent2 import (
    SelfDiscoverAgent,
    create_self_discover_agent,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_math_problem():
    """Example using SelfDiscover on a math problem."""
    problem = "Lisa has 10 apples. She gives 3 apples to her friend and then buys 5 more apples from the store. How many apples does Lisa have now?"

    agent = create_self_discover_agent(
        name="math_problem_solver", model="gpt-4o", temperature=0.0
    )

    agent.run(problem)
    # Print full reasoning process


def example_svg_interpretation():
    """Example using SelfDiscover to interpret an SVG path."""
    problem = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon (H) rectangle (I) sector (J) triangle"""

    # Custom reasoning modules for visual interpretation
    visual_reasoning_modules = [
        "1. Parse the SVG path commands to understand the drawing instructions.",
        "2. Visualize the path by mentally following each command step by step.",
        "3. Identify the starting points and endpoints of lines to understand shape closure.",
        "4. Count the number of vertices or corners in the shape.",
        "5. Determine if the shape is regular (equal sides and angles) or irregular.",
        "6. Check for symmetry in the shape to narrow down possibilities.",
        "7. Compare the described path with known geometric properties of common shapes.",
        "8. Convert path coordinates to a visual representation.",
        "9. Analyze the sequence of movements to detect patterns in the path.",
        "10. Identify whether the shape is open or closed based on the path commands.",
    ]

    agent = create_self_discover_agent(
        name="svg_interpreter",
        model="gpt-4o",
        temperature=0.0,
        reasoning_modules=visual_reasoning_modules,
    )

    agent.run(problem)

    # Print full reasoning process


def example_logical_reasoning():
    """Example using SelfDiscover for a logical reasoning problem."""
    problem = """Four people (Alex, Blake, Casey, and Dana) each have a different favorite color 
(red, blue, green, and yellow) and a different favorite fruit (apple, banana, cherry, and date). 
Given the following clues, determine each person\'s favorite color and fruit:

1. The person who likes red also likes dates.
2. Dana doesn\'t like yellow or apples.
3. Casey likes cherries.
4. The person who likes blue also likes bananas.
5. Alex likes green.
6. Blake doesn\'t like red."""

    # Custom reasoning modules for logical problems
    logical_reasoning_modules = [
        "1. Organize all given information into a structured format.",
        "2. Create logical tables or matrices to track possible combinations.",
        "3. Use process of elimination to reduce possible options.",
        "4. Check for direct one-to-one mappings in the constraints.",
        "5. Identify constraints that create chain reactions of implications.",
        "6. Verify that the solution satisfies all given constraints.",
        "7. Work sequentially through each clue, updating possibilities after each.",
        "8. Make tentative assumptions when necessary and verify their consistency.",
        "9. Use logical operators (AND, OR, NOT) to combine constraints.",
        "10. Identify any potential contradictions that would invalidate a solution path.",
    ]

    agent = create_self_discover_agent(
        name="logical_problem_solver",
        model="gpt-4o",
        temperature=0.0,
        reasoning_modules=logical_reasoning_modules,
    )

    agent.run(problem)

    # Print full reasoning process


def create_custom_domain_agent(
    domain: str, custom_modules: list[str] | None = None, model: str = "gpt-4o"
) -> SelfDiscoverAgent:
    """Create a SelfDiscover agent specialized for a particular domain.

    Args:
        domain: Domain to specialize in (e.g., "math", "logic", "programming")
        custom_modules: Optional custom reasoning modules
        model: Model to use

    Returns:
        Specialized SelfDiscoverAgent
    """
    # Base modules that are useful across domains
    base_modules = [
        "1. Break down the problem into smaller, more manageable sub-problems.",
        "2. Identify the key components or variables in the problem.",
        "3. Apply systematic step-by-step reasoning to solve the problem.",
        "4. Review the solution for consistency and correctness.",
        "5. Consider alternative approaches to verify the solution.",
    ]

    # Domain-specific modules
    domain_modules = {
        "math": [
            "6. Identify the mathematical operations needed (addition, subtraction, etc.).",
            "7. Set up equations to represent the relationships in the problem.",
            "8. Apply algebraic manipulations to solve for unknown values.",
            "9. Use numerical estimation to check if the answer is reasonable.",
            "10. Convert between different units or representations if needed.",
        ],
        "logic": [
            "6. Create logical tables to track possible states or combinations.",
            "7. Apply process of elimination based on given constraints.",
            "8. Identify logical implications (if A then B) within the problem.",
            "9. Check for consistency among all constraints and rules.",
            "10. Formulate the problem using logical operators and propositions.",
        ],
        "programming": [
            "6. Design the algorithm before implementing any code.",
            "7. Break the solution into functions or modules with clear purposes.",
            "8. Consider edge cases and error handling scenarios.",
            "9. Analyze time and space complexity of the proposed solution.",
            "10. Look for patterns that suggest known algorithms or data structures.",
        ],
        "language": [
            "6. Identify the linguistic context and key terms in the problem.",
            "7. Consider multiple meanings or interpretations of ambiguous phrases.",
            "8. Apply grammatical rules to analyze sentence structure.",
            "9. Break down complex sentences into simpler components.",
            "10. Use semantic analysis to understand implied meanings.",
        ],
    }

    # Combine base modules with domain-specific ones
    modules = base_modules + domain_modules.get(domain.lower(), [])

    # Add custom modules if provided
    if custom_modules:
        modules.extend(custom_modules)

    # Create and return the agent
    return create_self_discover_agent(
        name=f"{domain}_specialist",
        model=model,
        temperature=0.0,
        reasoning_modules=modules,
    )


def run_batch_problems(
    agent: SelfDiscoverAgent, problems: list[str], output_file: str | None = None
):
    """Run a batch of problems through a SelfDiscover agent and optionally save results.

    Args:
        agent: SelfDiscoverAgent to use
        problems: List of problem statements
        output_file: Optional file to save results
    """
    results = []

    for i, problem in enumerate(problems):
        try:
            # Run the agent on this problem
            result = agent.run(problem)

            # Store the result
            problem_result = {
                "problem": problem,
                "selected_modules": result.get("selected_modules", ""),
                "adapted_modules": result.get("adapted_modules", ""),
                "reasoning_structure": result.get("reasoning_structure", ""),
                "answer": result.get("answer", ""),
                "error": result.get("error", None),
            }

            results.append(problem_result)

            # Print just the answer for progress tracking

        except Exception as e:
            logger.exception(f"Error processing problem {i+1}: {e!s}")
            results.append({"problem": problem, "error": str(e)})

    # Save to file if requested
    if output_file:
        try:
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            logger.exception(f"Error saving results to {output_file}: {e!s}")

    return results


def example_advanced_configuration():
    """Example showing advanced configuration of the SelfDiscover agent."""
    # Custom prompts for each stage
    select_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert problem solver."),
            (
                "human",
                """Look at the problem below and select the 3-5 most appropriate reasoning techniques from the available options.
        Choose only techniques that will directly contribute to solving this specific problem.

        Available reasoning techniques:
        {reasoning_modules}

        Problem to solve:
        {task_description}

        Selected reasoning techniques (list only the numbers of your chosen techniques):
        """,
            ),
        ]
    )

    adapt_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert problem solver."),
            (
                "human",
                """Customize these selected reasoning techniques specifically for the problem at hand:

        Selected techniques:
        {selected_modules}

        Problem to solve:
        {task_description}

        For each technique, provide a customized version that addresses the specific challenges of this problem:
        """,
            ),
        ]
    )

    structure_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert problem solver."),
            (
                "human",
                """Create a structured reasoning plan as a JSON object to solve this problem.
        Your JSON should contain keys for each step of analysis, with explanations for what needs to be determined at each step.
        Do NOT solve the problem yet - only create the plan framework.

        Customized reasoning techniques:
        {adapted_modules}

        Problem to solve:
        {task_description}

        JSON reasoning plan structure:
        """,
            ),
        ]
    )

    reasoning_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert problem solver."),
            (
                "human",
                """
        Follow this reasoning structure to methodically solve the problem.
        Fill in each component of the structure with your actual reasoning and calculations.

        Reasoning structure:
        {reasoning_structure}

        Problem to solve:
        {task_description}

        Complete solution with all reasoning steps:
        """,
            ),
        ]
    )

    # Custom set of reasoning modules
    reasoning_modules = [
        "1. Mathematical Decomposition: Break down mathematical problems into simpler components.",
        "2. Pattern Recognition: Identify recurring patterns in the problem data.",
        "3. Logical Deduction: Use if-then reasoning to reach conclusions.",
        "4. Visual Mapping: Create visual representations of the problem space.",
        "5. Algorithmic Thinking: Apply step-by-step procedures to solve problems systematically.",
        "6. Comparative Analysis: Compare and contrast different elements of the problem.",
        "7. Causal Reasoning: Identify cause-and-effect relationships.",
        "8. Numerical Estimation: Use approximations to guide exact solutions.",
        "9. Constraint Analysis: Identify and work within the constraints of the problem.",
        "10. Probabilistic Reasoning: Consider the likelihood of different outcomes.",
    ]

    # Problem to solve
    problem = "A store has a special offer: buy 2 items, get 1 free (of equal or lesser value). If you have $50 to spend and each item costs $15, what is the maximum number of items you can get?"

    # Create the agent with custom configuration
    agent = create_self_discover_agent(
        name="custom_configured_agent",
        model="gpt-4o",
        temperature=0.0,
        reasoning_modules=reasoning_modules,
        select_prompt=select_prompt,
        adapt_prompt=adapt_prompt,
        structure_prompt=structure_prompt,
        reasoning_prompt=reasoning_prompt,
    )

    # Run the agent
    agent.run(problem)

    # Print results


def analyze_reasoning_process(
    agent_results: list[dict], output_file: str | None = None
):
    """Analyze the reasoning process across multiple problems to identify patterns.

    Args:
        agent_results: List of results from run_batch_problems
        output_file: Optional file to save analysis
    """
    if not agent_results:
        return None

    # Initialize analysis data
    analysis = {
        "total_problems": len(agent_results),
        "successful_problems": 0,
        "failed_problems": 0,
        "module_usage": {},
        "reasoning_patterns": [],
        "common_errors": {},
    }

    # Process each result
    for result in agent_results:
        # Check for errors
        if result.get("error"):
            analysis["failed_problems"] += 1
            error = result.get("error")
            analysis["common_errors"][error] = (
                analysis["common_errors"].get(error, 0) + 1
            )
        else:
            analysis["successful_problems"] += 1

            # Analyze selected modules
            selected = result.get("selected_modules", "")
            # Extract module numbers from text (assuming format like "1. Module name")
            import re

            module_numbers = re.findall(r"(\d+)\.", selected)
            for num in module_numbers:
                analysis["module_usage"][num] = analysis["module_usage"].get(num, 0) + 1

    # Calculate module usage percentages
    for module, count in analysis["module_usage"].items():
        analysis["module_usage"][module] = {
            "count": count,
            "percentage": round((count / analysis["successful_problems"]) * 100, 2),
        }

    # Sort modules by usage
    sorted_modules = sorted(
        analysis["module_usage"].items(), key=lambda x: x[1]["count"], reverse=True
    )

    # Print analysis

    for module, _data in sorted_modules[:5]:
        pass

    if analysis["common_errors"]:
        for error, count in sorted(
            analysis["common_errors"].items(), key=lambda x: x[1], reverse=True
        )[:3]:
            pass

    # Save to file if requested
    if output_file:
        try:
            with open(output_file, "w") as f:
                json.dump(analysis, f, indent=2)
        except Exception as e:
            logger.exception(f"Error saving analysis to {output_file}: {e!s}")

    return analysis


def example_compare_models():
    """Example comparing different models on the same problem."""
    problem = """If a sequence follows the pattern: 2, 6, 12, 20, 30, ..., what is the next number in the sequence?"""

    models = ["gpt-4o", "gpt-3.5-turbo"]
    results = {}

    for model in models:
        agent = create_self_discover_agent(
            name=f"{model}_sequence_agent", model=model, temperature=0.0
        )

        result = agent.run(problem)
        results[model] = {
            "selected_modules": result.get("selected_modules", ""),
            "adapted_modules": result.get("adapted_modules", ""),
            "reasoning_structure": result.get("reasoning_structure", ""),
            "answer": result.get("answer", ""),
        }

    # Compare reasoning structures
    for model in models:
        pass
    # Compare final answers
    for model in models:
        pass


if __name__ == "__main__":
    # Run different examples based on command line arguments
    import sys

    if len(sys.argv) == 1 or sys.argv[1] == "math":
        example_math_problem()
    elif sys.argv[1] == "svg":
        example_svg_interpretation()
    elif sys.argv[1] == "logic":
        example_logical_reasoning()
    elif sys.argv[1] == "advanced":
        example_advanced_configuration()
    elif sys.argv[1] == "compare":
        example_compare_models()
    elif sys.argv[1] == "all":
        example_math_problem()
        example_svg_interpretation()
        example_logical_reasoning()
        example_advanced_configuration()
        example_compare_models()
    else:
        pass
