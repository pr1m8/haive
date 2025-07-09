"""Example delegation tasks following LangGraph tutorial pattern.

This example demonstrates the Haive Supervisor agent managing specialized
worker agents for different types of tasks, similar to the LangGraph tutorial.
"""

import asyncio
import logging
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from rich.console import Console
from rich.panel import Panel

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.agent import SupervisorAgent, SupervisorState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


def create_mock_research_agent() -> SimpleAgent:
    """Create a mock research agent for testing."""

    # Mock LLM config (replace with real config)
    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0.1)

    engine_config = AugLLMConfig(
        llm=llm_config,
        system_prompt="You are a research specialist. You excel at finding information, analyzing data, and providing comprehensive research results.",
    )

    return SimpleAgent(
        name="research_agent",
        engine=engine_config,
        description="Specializes in research, information gathering, and data analysis",
    )


def create_mock_math_agent() -> SimpleAgent:
    """Create a mock math agent for testing."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0)

    engine_config = AugLLMConfig(
        llm=llm_config,
        system_prompt="You are a mathematics specialist. You excel at solving mathematical problems, performing calculations, and explaining mathematical concepts.",
    )

    return SimpleAgent(
        name="math_agent",
        engine=engine_config,
        description="Specializes in mathematics, calculations, and quantitative analysis",
    )


def create_mock_writing_agent() -> SimpleAgent:
    """Create a mock writing agent for testing."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0.7)

    engine_config = AugLLMConfig(
        llm=llm_config,
        system_prompt="You are a writing specialist. You excel at creating clear, engaging content, editing text, and various forms of written communication.",
    )

    return SimpleAgent(
        name="writing_agent",
        engine=engine_config,
        description="Specializes in writing, editing, and content creation",
    )


def create_supervisor_agent() -> SupervisorAgent:
    """Create the supervisor agent."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0.1)

    supervisor_engine = AugLLMConfig(
        llm=llm_config,
        system_prompt="You are a task supervisor. Analyze requests and delegate to the most appropriate specialist agent.",
    )

    return SupervisorAgent(name="task_supervisor", engine=supervisor_engine)


async def test_delegation_flow():
    """Test the delegation flow with various task types."""

    console.print(
        Panel("🚀 Starting Haive Supervisor Delegation Test", style="bold blue")
    )

    # Create supervisor
    supervisor = create_supervisor_agent()

    # Create and register specialist agents
    research_agent = create_mock_research_agent()
    math_agent = create_mock_math_agent()
    writing_agent = create_mock_writing_agent()

    console.print("\n[yellow]📝 Registering agents...[/yellow]")
    supervisor.register_agent(research_agent)
    supervisor.register_agent(math_agent)
    supervisor.register_agent(writing_agent)

    # Show supervisor status
    console.print("\n[cyan]📊 Supervisor Status:[/cyan]")
    supervisor.print_supervisor_status()

    # Test cases from LangGraph tutorial
    test_cases = [
        {
            "description": "Research Task",
            "message": "What are the key trends in AI development for 2024?",
            "expected_agent": "research_agent",
        },
        {
            "description": "Math Task",
            "message": "Calculate the compound interest on $10,000 at 5% annually for 10 years",
            "expected_agent": "math_agent",
        },
        {
            "description": "Writing Task",
            "message": "Write a professional email announcing a new product launch",
            "expected_agent": "writing_agent",
        },
        {
            "description": "Complex Multi-step Task",
            "message": "Research the market size for electric vehicles, calculate growth projections, and write a summary report",
            "expected_agent": None,  # Should route intelligently
        },
        {
            "description": "Completion Task",
            "message": "Thank you, that's all I needed",
            "expected_agent": "END",
        },
    ]

    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        console.print(
            f"\n[bold green]🧪 Test Case {i}: {test_case['description']}[/bold green]"
        )
        console.print(f"[dim]Message: {test_case['message']}[/dim]")

        try:
            # Create initial state
            initial_state = SupervisorState(
                messages=[HumanMessage(content=test_case["message"])]
            )

            # Build and compile graph
            graph = supervisor.build_graph()
            compiled_graph = graph.compile()

            # Execute
            console.print("[yellow]⚡ Executing delegation...[/yellow]")
            result = await compiled_graph.ainvoke(initial_state)

            # Show results
            routing_decision = getattr(result, "routing_decision", "Unknown")
            target_agent = getattr(result, "target_agent", "Unknown")

            console.print(f"[cyan]📍 Routing Decision:[/cyan] {routing_decision}")
            console.print(f"[cyan]🎯 Target Agent:[/cyan] {target_agent}")

            if test_case["expected_agent"]:
                if routing_decision == test_case["expected_agent"]:
                    console.print("[green]✅ Expected routing achieved![/green]")
                else:
                    console.print(
                        f"[yellow]⚠️  Expected {test_case['expected_agent']}, got {routing_decision}[/yellow]"
                    )

            # Show final messages
            final_messages = getattr(result, "messages", [])
            if final_messages:
                console.print(
                    f"[dim]Final message: {final_messages[-1].content if final_messages else 'None'}[/dim]"
                )

        except Exception as e:
            console.print(f"[red]❌ Test failed: {str(e)}[/red]")
            logger.error(f"Test case {i} failed", exc_info=True)

        console.print("-" * 60)

    console.print(Panel("🎉 Delegation test completed!", style="bold green"))


async def test_dynamic_agent_management():
    """Test dynamic agent registration/removal."""

    console.print(Panel("🔄 Testing Dynamic Agent Management", style="bold cyan"))

    # Create supervisor
    supervisor = create_supervisor_agent()

    # Start with one agent
    research_agent = create_mock_research_agent()
    supervisor.register_agent(research_agent)

    console.print("\n[yellow]📋 Initial state - 1 agent:[/yellow]")
    supervisor.print_supervisor_status()

    # Add more agents
    math_agent = create_mock_math_agent()
    writing_agent = create_mock_writing_agent()

    console.print("\n[yellow]➕ Adding math and writing agents:[/yellow]")
    supervisor.register_agent(math_agent)
    supervisor.register_agent(writing_agent)
    supervisor.print_supervisor_status()

    # Remove an agent
    console.print("\n[yellow]➖ Removing research agent:[/yellow]")
    supervisor.unregister_agent("research_agent")
    supervisor.print_supervisor_status()

    # Test routing with reduced agents
    console.print("\n[yellow]🧪 Testing routing with reduced agent set:[/yellow]")

    initial_state = SupervisorState(
        messages=[HumanMessage(content="Calculate the area of a circle with radius 5")]
    )

    try:
        graph = supervisor.build_graph()
        compiled_graph = graph.compile()
        result = await compiled_graph.ainvoke(initial_state)

        routing_decision = getattr(result, "routing_decision", "Unknown")
        console.print(f"[cyan]Routing decision:[/cyan] {routing_decision}")

    except Exception as e:
        console.print(f"[red]Dynamic test failed: {str(e)}[/red]")


def main():
    """Main test function."""

    console.print(
        Panel(
            """
🏗️  Haive Supervisor Agent Test Suite

This test demonstrates:
1. Agent registration and management
2. Intelligent task delegation
3. Dynamic agent management
4. Routing validation

Based on LangGraph tutorial patterns but implemented
with Haive's ReactAgent architecture.
    """,
            title="Supervisor Test Suite",
            style="bold blue",
        )
    )

    try:
        # Run delegation tests
        asyncio.run(test_delegation_flow())

        # Run dynamic management tests
        asyncio.run(test_dynamic_agent_management())

        console.print(Panel("🎊 All tests completed successfully!", style="bold green"))

    except Exception as e:
        console.print(f"[red]❌ Test suite failed: {str(e)}[/red]")
        logger.error("Test suite failed", exc_info=True)


if __name__ == "__main__":
    main()
