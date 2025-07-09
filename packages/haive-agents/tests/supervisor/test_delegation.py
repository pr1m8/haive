"""Test Delegation Tasks - Following LangGraph Tutorial Pattern.

This test exactly follows the LangGraph tutorial structure:
https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#4-create-delegation-tasks

But implemented using Haive's architecture with MultiAgent base and proper state management.
"""

import asyncio
import logging
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.agent_v2 import SupervisorAgent, SupervisorState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


# Create tools for agents (following LangGraph tutorial)
@tool
def tavily_search(query: str) -> str:
    """Search the web for information (mock implementation)."""
    return f"Research results for '{query}': Found comprehensive information about {query} from multiple sources."


@tool
def python_repl(code: str) -> str:
    """Execute Python code (mock implementation)."""
    try:
        # Simple mock calculation
        if "compound interest" in code.lower():
            return "Compound Interest Result: $16,288.95 after 10 years"
        elif "area" in code.lower() and "circle" in code.lower():
            return "Circle Area Result: 78.54 square units"
        else:
            return f"Executed: {code}\nResult: Calculation completed successfully"
    except Exception as e:
        return f"Error: {str(e)}"


def create_research_agent() -> ReactAgent:
    """Create research agent following LangGraph tutorial pattern."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0.1)

    engine_config = AugLLMConfig(
        llm_config=llm_config,
        system_message="""You are a research assistant. Your role is to search for information and provide comprehensive research results.
        
When given a research task:
1. Use the tavily_search tool to find relevant information
2. Synthesize the findings into a clear, informative response
3. Provide sources and context when possible

Focus on being thorough and accurate in your research.""",
        tools=[tavily_search],
    )

    agent = ReactAgent(name="research_agent", engine=engine_config)
    agent.description = "Specializes in web search and information gathering"

    return agent


def create_math_agent() -> ReactAgent:
    """Create math agent following LangGraph tutorial pattern."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0)

    engine_config = AugLLMConfig(
        llm_config=llm_config,
        system_message="""You are a mathematics expert. Your role is to solve mathematical problems and perform calculations.

When given a math task:
1. Use the python_repl tool to perform calculations
2. Show your work and explain the steps
3. Provide clear, accurate results

Focus on precision and clarity in your mathematical solutions.""",
        tools=[python_repl],
    )

    agent = ReactAgent(name="math_agent", engine=engine_config)
    agent.description = "Specializes in mathematical calculations and problem solving"

    return agent


def create_supervisor() -> SupervisorAgent:
    """Create supervisor agent following LangGraph tutorial pattern."""

    llm_config = LLMConfig(provider="openai", model="gpt-4", temperature=0.1)

    supervisor_engine = AugLLMConfig(
        llm_config=llm_config,
        system_message="You are a helpful assistant supervisor. Analyze user requests and delegate to the most appropriate specialist.",
    )

    return SupervisorAgent(name="supervisor", engine=supervisor_engine)


async def test_basic_delegation():
    """Test basic delegation following LangGraph tutorial tasks."""

    console.print(
        Panel(
            "🧪 Testing Basic Delegation (LangGraph Tutorial Pattern)",
            style="bold blue",
        )
    )

    # Create agents
    supervisor = create_supervisor()
    research_agent = create_research_agent()
    math_agent = create_math_agent()

    # Add workers to supervisor
    supervisor.add_worker_agent(research_agent)
    supervisor.add_worker_agent(math_agent)

    # Show setup
    supervisor.print_supervisor_status()

    # Test cases from LangGraph tutorial
    test_cases = [
        {
            "name": "Research Task",
            "message": "What are the latest trends in artificial intelligence?",
            "expected_worker": "research_agent",
        },
        {
            "name": "Math Task",
            "message": "Calculate the compound interest on $10,000 at 5% annually for 10 years",
            "expected_worker": "math_agent",
        },
        {
            "name": "Research Task 2",
            "message": "Find information about renewable energy sources",
            "expected_worker": "research_agent",
        },
        {
            "name": "Math Task 2",
            "message": "What's the area of a circle with radius 5?",
            "expected_worker": "math_agent",
        },
        {
            "name": "Completion",
            "message": "Thank you, that's all I needed",
            "expected_worker": "FINISH",
        },
    ]

    # Build and compile graph
    graph = supervisor.build_graph()
    compiled_graph = graph.compile()

    # Run test cases
    results_table = Table(title="🎯 Delegation Test Results")
    results_table.add_column("Test", style="cyan")
    results_table.add_column("Expected", style="green")
    results_table.add_column("Actual", style="yellow")
    results_table.add_column("Status", style="bold")

    for i, test_case in enumerate(test_cases, 1):
        console.print(f"\n[bold]Test {i}: {test_case['name']}[/bold]")
        console.print(f"[dim]Message: {test_case['message']}[/dim]")

        try:
            # Create initial state
            initial_state = SupervisorState(
                messages=[HumanMessage(content=test_case["message"])]
            )

            # Execute
            result = await compiled_graph.ainvoke(initial_state)

            # Check routing decision
            next_agent = getattr(result, "next", "Unknown")

            # Determine status
            if next_agent == test_case["expected_worker"]:
                status = "✅ PASS"
                status_style = "green"
            else:
                status = "❌ FAIL"
                status_style = "red"

            results_table.add_row(
                test_case["name"], test_case["expected_worker"], next_agent, status
            )

            console.print(f"[cyan]Routed to:[/cyan] {next_agent}")

            # Show final messages
            final_messages = getattr(result, "messages", [])
            if final_messages:
                last_message = final_messages[-1]
                console.print(f"[dim]Response: {last_message.content[:100]}...[/dim]")

        except Exception as e:
            console.print(f"[red]❌ Test failed: {str(e)}[/red]")
            results_table.add_row(
                test_case["name"], test_case["expected_worker"], "ERROR", "❌ ERROR"
            )

    console.print("\n")
    console.print(results_table)


async def test_multi_turn_conversation():
    """Test multi-turn conversation with state preservation."""

    console.print(Panel("💬 Testing Multi-Turn Conversation", style="bold green"))

    # Create system
    supervisor = create_supervisor()
    supervisor.add_worker_agent(create_research_agent())
    supervisor.add_worker_agent(create_math_agent())

    # Build graph
    graph = supervisor.build_graph()
    compiled_graph = graph.compile()

    # Simulate conversation
    conversation = [
        "Research the current state of quantum computing",
        "Based on that research, calculate how many qubits would be needed for a 1024-bit encryption",
        "Now research commercial applications of quantum computing",
        "That's all, thank you",
    ]

    state = SupervisorState(messages=[])

    for i, message in enumerate(conversation, 1):
        console.print(f"\n[bold cyan]Turn {i}:[/bold cyan] {message}")

        # Add user message
        state.messages.append(HumanMessage(content=message))

        # Execute
        try:
            result = await compiled_graph.ainvoke(state)

            # Update state for next turn
            state = result

            next_agent = getattr(result, "next", "Unknown")
            console.print(f"[yellow]Supervisor decision:[/yellow] {next_agent}")

            # Show agent response if available
            if hasattr(result, "messages") and result.messages:
                last_msg = result.messages[-1]
                if isinstance(last_msg, AIMessage):
                    console.print(
                        f"[green]Response:[/green] {last_msg.content[:150]}..."
                    )

        except Exception as e:
            console.print(f"[red]❌ Turn failed: {str(e)}[/red]")


async def test_error_handling():
    """Test error handling and fallback mechanisms."""

    console.print(Panel("🛡️ Testing Error Handling", style="bold yellow"))

    supervisor = create_supervisor()
    supervisor.add_worker_agent(create_research_agent())

    # Test with invalid request
    try:
        graph = supervisor.build_graph()
        compiled_graph = graph.compile()

        # Ambiguous request
        state = SupervisorState(
            messages=[HumanMessage(content="Do something unclear and undefined")]
        )

        result = await compiled_graph.ainvoke(state)

        next_agent = getattr(result, "next", "Unknown")
        console.print(f"[cyan]Ambiguous request routed to:[/cyan] {next_agent}")

        # Test with no agents
        empty_supervisor = create_supervisor()
        empty_graph = empty_supervisor.build_graph()
        empty_compiled = empty_graph.compile()

        result2 = await empty_compiled.ainvoke(state)
        next_agent2 = getattr(result2, "next", "Unknown")
        console.print(f"[cyan]No agents available, routed to:[/cyan] {next_agent2}")

    except Exception as e:
        console.print(f"[red]Error handling test failed: {str(e)}[/red]")


def main():
    """Main test runner."""

    console.print(
        Panel(
            """
🏗️ Haive Supervisor Delegation Test Suite

Following LangGraph Tutorial Pattern:
- Supervisor analyzes requests  
- Sets 'next' field for routing
- Workers execute and return to supervisor
- Simple state with messages + next

Using Haive Architecture:
- MultiAgent base class
- AgentSchemaComposer
- Proper state management
    """,
            title="Delegation Test Suite",
            style="bold blue",
        )
    )

    async def run_all_tests():
        try:
            await test_basic_delegation()
            await test_multi_turn_conversation()
            await test_error_handling()

            console.print(Panel("🎉 All tests completed!", style="bold green"))

        except Exception as e:
            console.print(f"[red]❌ Test suite failed: {str(e)}[/red]")
            logger.error("Test suite failed", exc_info=True)

    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()
