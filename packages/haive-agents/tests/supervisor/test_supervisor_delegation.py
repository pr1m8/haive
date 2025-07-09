"""Real Supervisor Delegation Tests - No Mocks, Real Implementation.

Tests the Haive Supervisor with actual agent delegation using real engines and tools.
"""

import asyncio
import logging
import os
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from rich.console import Console
from rich.panel import Panel

from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor.agent_v2 import SupervisorAgent, SupervisorState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


# Real tools for testing
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    try:
        # Safe evaluation of basic math expressions
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"

        result = eval(expression)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


@tool
def text_analyzer(text: str) -> str:
    """Analyze text and provide statistics."""
    words = text.split()
    sentences = text.split(".")
    chars = len(text)

    analysis = f"""Text Analysis Results:
- Character count: {chars}
- Word count: {len(words)}
- Sentence count: {len(sentences)}
- Average words per sentence: {len(words)/max(len(sentences), 1):.1f}
- Most common words: {', '.join(sorted(set(words), key=words.count, reverse=True)[:3])}
"""
    return analysis


@tool
def create_simple_agent(name: str, description: str) -> str:
    """Create a new simple agent and add it to the supervisor."""
    # This tool will be used by the supervisor to dynamically add agents
    return f"Agent '{name}' created with description: {description}. Ready to be registered with supervisor."


def create_math_agent() -> ReactAgent:
    """Create a real math agent with calculator tool."""

    # Use environment variable or fallback
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    llm_config = LLMConfig(provider="openai", model=model, temperature=0)

    engine_config = AugLLMConfig(
        llm_config=llm_config,
        system_message="""You are a mathematics specialist. Use the calculator tool to solve mathematical problems.
        
When given a math problem:
1. Use the calculator tool to perform calculations  
2. Show your work step by step
3. Provide clear, accurate results""",
        tools=[calculator],
    )

    agent = ReactAgent(name="math_agent", engine=engine_config)
    agent.description = "Specializes in mathematical calculations and problem solving"

    return agent


def create_text_agent() -> ReactAgent:
    """Create a real text analysis agent."""

    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    llm_config = LLMConfig(provider="openai", model=model, temperature=0.3)

    engine_config = AugLLMConfig(
        llm_config=llm_config,
        system_message="""You are a text analysis specialist. Use the text_analyzer tool to analyze text.

When given text to analyze:
1. Use the text_analyzer tool to get statistics
2. Provide insights about the text
3. Offer suggestions for improvement""",
        tools=[text_analyzer],
    )

    agent = ReactAgent(name="text_agent", engine=engine_config)
    agent.description = "Specializes in text analysis and linguistic insights"

    return agent


def create_supervisor() -> SupervisorAgent:
    """Create a real supervisor agent."""

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    llm_config = LLMConfig(provider="openai", model=model, temperature=0.1)

    supervisor_engine = AugLLMConfig(
        llm_config=llm_config,
        system_message="""You are a task supervisor. Analyze user requests and delegate to the most appropriate specialist agent.

Available tools:
- create_simple_agent: Create new agents dynamically

Routing rules:
- Math problems → math_agent
- Text analysis → text_agent  
- Agent creation requests → use create_simple_agent tool
- Task completion → FINISH""",
        tools=[create_simple_agent],
    )

    return SupervisorAgent(name="supervisor", engine=supervisor_engine)


async def test_real_delegation():
    """Test real delegation with actual agents and tools."""

    console.print(Panel("🧪 Testing Real Supervisor Delegation", style="bold blue"))

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping real tests.[/red]")
        return

    try:
        # Create supervisor and agents
        supervisor = create_supervisor()
        math_agent = create_math_agent()
        text_agent = create_text_agent()

        # Register agents
        supervisor.add_worker_agent(math_agent)
        supervisor.add_worker_agent(text_agent)

        # Show setup
        supervisor.print_supervisor_status()

        # Real test cases
        test_cases = [
            {
                "name": "Math Calculation",
                "message": "Calculate 15 * 23 + 47",
                "expected_agent": "math_agent",
            },
            {
                "name": "Text Analysis",
                "message": "Analyze this text: 'The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.'",
                "expected_agent": "text_agent",
            },
            {
                "name": "Complex Math",
                "message": "What is the square root of 144 plus 25% of 200?",
                "expected_agent": "math_agent",
            },
            {
                "name": "Agent Creation",
                "message": "Create a new agent called 'weather_agent' that can check weather conditions",
                "expected_agent": "supervisor",  # Should use create_simple_agent tool
            },
        ]

        # Build graph once
        graph = supervisor.build_graph()
        compiled_graph = graph.compile()

        # Run test cases
        for i, test_case in enumerate(test_cases, 1):
            console.print(
                f"\n[bold green]🧪 Test {i}: {test_case['name']}[/bold green]"
            )
            console.print(f"[dim]Request: {test_case['message']}[/dim]")

            try:
                # Create initial state
                initial_state = SupervisorState(
                    messages=[HumanMessage(content=test_case["message"])]
                )

                # Execute delegation
                console.print("[yellow]⚡ Executing...[/yellow]")
                result = await compiled_graph.ainvoke(initial_state)

                # Show results
                next_agent = getattr(result, "next", "Unknown")
                available_agents = getattr(result, "available_agents", [])

                console.print(f"[cyan]📍 Routing Decision:[/cyan] {next_agent}")
                console.print(
                    f"[cyan]🎯 Available Agents:[/cyan] {', '.join(available_agents)}"
                )

                # Show final messages
                final_messages = getattr(result, "messages", [])
                if final_messages:
                    last_message = final_messages[-1]
                    if hasattr(last_message, "content"):
                        content = (
                            last_message.content[:200] + "..."
                            if len(last_message.content) > 200
                            else last_message.content
                        )
                        console.print(f"[green]📝 Response:[/green] {content}")

                # Check if expectation met
                if next_agent == test_case["expected_agent"]:
                    console.print("[green]✅ Expected routing achieved![/green]")
                else:
                    console.print(
                        f"[yellow]⚠️  Expected {test_case['expected_agent']}, got {next_agent}[/yellow]"
                    )

            except Exception as e:
                console.print(f"[red]❌ Test failed: {str(e)}[/red]")
                logger.error(f"Test {i} failed", exc_info=True)

            console.print("-" * 60)

    except Exception as e:
        console.print(f"[red]❌ Test setup failed: {str(e)}[/red]")
        logger.error("Test setup failed", exc_info=True)


async def test_dynamic_agent_management():
    """Test dynamic agent registration and management."""

    console.print(Panel("🔄 Testing Dynamic Agent Management", style="bold cyan"))

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping dynamic tests.[/red]")
        return

    try:
        # Start with minimal supervisor
        supervisor = create_supervisor()

        console.print("\n[yellow]📋 Initial state - no agents:[/yellow]")
        supervisor.print_supervisor_status()

        # Add agents one by one
        agents_to_add = [create_math_agent(), create_text_agent()]

        for agent in agents_to_add:
            console.print(f"\n[yellow]➕ Adding {agent.name}:[/yellow]")
            supervisor.add_worker_agent(agent)
            supervisor.print_supervisor_status()

        # Test routing with full agent set
        console.print("\n[yellow]🧪 Testing routing with all agents:[/yellow]")

        graph = supervisor.build_graph()
        compiled_graph = graph.compile()

        test_message = "Calculate the area of a circle with radius 7"
        initial_state = SupervisorState(messages=[HumanMessage(content=test_message)])

        result = await compiled_graph.ainvoke(initial_state)

        next_agent = getattr(result, "next", "Unknown")
        console.print(f"[cyan]Routing decision for math problem:[/cyan] {next_agent}")

        # Remove an agent
        console.print(f"\n[yellow]➖ Removing math_agent:[/yellow]")
        supervisor.remove_worker_agent("math_agent")
        supervisor.print_supervisor_status()

    except Exception as e:
        console.print(f"[red]❌ Dynamic test failed: {str(e)}[/red]")
        logger.error("Dynamic test failed", exc_info=True)


async def test_supervisor_tool_usage():
    """Test supervisor using its own tools to create agents."""

    console.print(Panel("🛠️ Testing Supervisor Tool Usage", style="bold magenta"))

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping tool tests.[/red]")
        return

    try:
        supervisor = create_supervisor()

        # Test supervisor using create_simple_agent tool
        console.print("\n[yellow]🔧 Testing agent creation tool:[/yellow]")

        graph = supervisor.build_graph()
        compiled_graph = graph.compile()

        creation_request = (
            "Create a weather agent that can check current weather conditions"
        )
        initial_state = SupervisorState(
            messages=[HumanMessage(content=creation_request)]
        )

        result = await compiled_graph.ainvoke(initial_state)

        # Show what happened
        final_messages = getattr(result, "messages", [])
        if final_messages:
            for msg in final_messages[-2:]:  # Show last couple messages
                if hasattr(msg, "content"):
                    console.print(f"[green]📝 Message:[/green] {msg.content}")

    except Exception as e:
        console.print(f"[red]❌ Tool test failed: {str(e)}[/red]")
        logger.error("Tool test failed", exc_info=True)


def main():
    """Main test runner."""

    console.print(
        Panel(
            """
🏗️ Haive Supervisor Real Delegation Test Suite

Tests:
1. Real delegation with actual LLM calls
2. Dynamic agent management
3. Supervisor tool usage
4. No mocks - real implementation testing

Requires OPENAI_API_KEY environment variable.
    """,
            title="Real Supervisor Tests",
            style="bold blue",
        )
    )

    async def run_all_tests():
        try:
            await test_real_delegation()
            await test_dynamic_agent_management()
            await test_supervisor_tool_usage()

            console.print(Panel("🎉 All tests completed!", style="bold green"))

        except Exception as e:
            console.print(f"[red]❌ Test suite failed: {str(e)}[/red]")
            logger.error("Test suite failed", exc_info=True)

    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()
