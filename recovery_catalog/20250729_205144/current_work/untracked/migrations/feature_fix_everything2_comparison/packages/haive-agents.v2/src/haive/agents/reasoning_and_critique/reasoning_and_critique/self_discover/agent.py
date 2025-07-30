"""Self-Discover MultiAgent implementation."""

from haive.agents.multi.clean import MultiAgent

from .adapter import AdapterAgent
from .executor import ExecutorAgent
from .selector import SelectorAgent
from .structurer import StructurerAgent


def get_default_modules() -> str:
    """Get default reasoning modules for Self-Discover process."""
    return """1. Critical Thinking: Question assumptions, identify biases, evaluate evidence
2. Systems Analysis: Break down complex systems, identify components and relationships
3. Root Cause Analysis: Identify underlying causes of problems or phenomena
4. Stakeholder Analysis: Identify and understand different perspectives and interests
5. SWOT Analysis: Analyze strengths, weaknesses, opportunities, and threats
6. Cost-Benefit Analysis: Evaluate trade-offs and resource allocation
7. Risk Assessment: Identify and evaluate potential risks and mitigation strategies
8. Design Thinking: User-centered approach to innovation and problem-solving
9. Analogical Reasoning: Draw insights from similar situations or domains
10. Causal Analysis: Understand cause-and-effect relationships
11. Scenario Planning: Consider multiple future possibilities and outcomes
12. Constraint Analysis: Identify limitations and work within boundaries
13. Optimization: Find the best solution within given parameters
14. Pattern Recognition: Identify recurring themes, trends, or structures
15. Hypothesis Testing: Formulate and test explanatory theories
16. Brainstorming: Generate creative ideas and solutions
17. Prioritization: Rank options by importance or impact
18. Process Analysis: Examine workflows and procedures for improvement
19. Competitive Analysis: Understand competitive landscape and positioning
20. Data Analysis: Extract insights from quantitative and qualitative data"""


def create_self_discover_agent(name: str = "self_discover") -> MultiAgent:
    """Create a Self-Discover MultiAgent with the four-stage process.

    Args:
        name: Name for the multi-agent system

    Returns:
        MultiAgent configured for Self-Discover workflow
    """
    # Create the four specialized agents in sequential order
    agents = [SelectorAgent(), AdapterAgent(), StructurerAgent(), ExecutorAgent()]

    # Create and return the MultiAgent (no engine needed for sequential execution)
    return MultiAgent(name=name, agents=agents)


# Create a default instance for easy import
SelfDiscoverAgent = create_self_discover_agent()


import asyncio


async def main():
    """Example usage of Self-Discover agent."""
    # Create Self-Discover agent
    agent = create_self_discover_agent()

    # Example task
    task_example = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon(H) rectangle (I) sector (J) triangle"""

    # Prepare input with modules and task
    input_data = {
        "available_modules": get_default_modules(),
        "task_description": task_example,
    }

    # Execute the Self-Discover process
    await agent.arun(input_data)


if __name__ == "__main__":
    asyncio.run(main())
