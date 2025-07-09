"""Simple Supervisor Test - ReactAgent with Real Implementation.

Test ReactAgent-based supervisor with:
1. Agent registry with add_agent tool
2. Dynamic routing tool
3. Generic agent execution node
"""

import asyncio
import logging
import os
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from rich.console import Console
from rich.panel import Panel

from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.agent_v2 import SupervisorAgent, SupervisorState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


class EchoAgent(SimpleAgent):
    """Simple echo agent for testing - no API calls needed."""

    response_prefix: str = ""

    def __init__(self, name: str, response_prefix: str = ""):
        super().__init__(name=name)
        self.response_prefix = response_prefix
        self.description = (
            f"Test agent that echoes messages with prefix: {response_prefix}"
        )

    async def ainvoke(self, state: Any, config=None) -> Any:
        """Echo the last message with a prefix."""
        messages = getattr(state, "messages", [])
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", str(last_message))
            response = f"{self.response_prefix}: {content}"
        else:
            response = f"{self.response_prefix}: No message to echo"

        # Return new state with echo response
        new_messages = list(messages) + [AIMessage(content=response)]

        # Return the same type of state we received
        if hasattr(state, "__class__"):
            try:
                return state.__class__(messages=new_messages)
            except:
                pass

        # Fallback to generic state
        return type("EchoState", (), {"messages": new_messages})()


async def test_supervisor_basic():
    """Test basic supervisor functionality."""

    console.print(Panel("🧪 Testing ReactAgent Supervisor", style="bold blue"))

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping LLM tests.[/red]")
        return

    try:
        # Create supervisor
        supervisor = SupervisorAgent("test_supervisor")

        # Add some test agents
        hello_agent = EchoAgent("hello_echo", "HELLO")
        math_agent = EchoAgent("math_echo", "MATH_RESULT")

        supervisor.add_worker_agent(hello_agent)
        supervisor.add_worker_agent(math_agent)

        # Show status
        supervisor.print_supervisor_status()

        # Test message
        test_message = "Hello, I need to calculate 5 + 5"
        initial_state = {"messages": [HumanMessage(content=test_message)]}

        console.print(f"\n[yellow]📝 Test Input:[/yellow] {test_message}")

        # Run supervisor (ReactAgent)
        result = await supervisor.ainvoke(initial_state)

        # Show results
        final_messages = getattr(result, "messages", [])
        if final_messages:
            last_message = final_messages[-1]
            if hasattr(last_message, "content"):
                console.print(
                    f"[green]📤 Supervisor Response:[/green] {last_message.content}"
                )

        console.print("[green]✅ Basic test completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Test failed: {str(e)}[/red]")
        logger.error("Basic test failed", exc_info=True)


async def test_agent_registration():
    """Test dynamic agent registration via tools."""

    console.print(Panel("🔧 Testing Agent Registration Tools", style="bold cyan"))

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping tool tests.[/red]")
        return

    try:
        # Create supervisor
        supervisor = SupervisorAgent("registration_supervisor")

        # Test agent registration request
        registration_message = (
            "Please add a weather agent that can check current weather conditions"
        )
        initial_state = {"messages": [HumanMessage(content=registration_message)]}

        console.print(
            f"\n[yellow]📝 Registration Request:[/yellow] {registration_message}"
        )

        # Run supervisor
        result = await supervisor.ainvoke(initial_state)

        # Show results
        final_messages = getattr(result, "messages", [])
        console.print(f"\n[cyan]📋 Message Flow:[/cyan]")
        for i, msg in enumerate(final_messages[-3:], 1):  # Show last 3 messages
            if hasattr(msg, "content"):
                role = msg.__class__.__name__.replace("Message", "")
                console.print(f"  {i}. [{role}] {msg.content[:100]}...")

        # Check registry
        console.print(
            f"\n[green]📊 Registry Status:[/green] {len(supervisor._agent_registry)} agents"
        )
        for name, info in supervisor._agent_registry.items():
            description = (
                info.get("description", "No description")
                if isinstance(info, dict)
                else getattr(info, "description", "No description")
            )
            console.print(f"  - {name}: {description}")

        console.print("[green]✅ Registration test completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Registration test failed: {str(e)}[/red]")
        logger.error("Registration test failed", exc_info=True)


async def test_routing_flow():
    """Test the complete routing flow."""

    console.print(Panel("🎯 Testing Complete Routing Flow", style="bold magenta"))

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]❌ OPENAI_API_KEY not found. Skipping routing tests.[/red]")
        return

    try:
        # Create supervisor
        supervisor = SupervisorAgent("routing_supervisor")

        # Add real agents
        text_agent = EchoAgent("text_analyzer", "TEXT_ANALYSIS")
        calc_agent = EchoAgent("calculator", "CALCULATION")

        supervisor.add_worker_agent(text_agent)
        supervisor.add_worker_agent(calc_agent)

        # Test routing request
        routing_message = "I need to analyze this text: 'Hello world, this is a test message for analysis.'"
        initial_state = {"messages": [HumanMessage(content=routing_message)]}

        console.print(f"\n[yellow]📝 Routing Request:[/yellow] {routing_message}")

        # Run supervisor
        result = await supervisor.ainvoke(initial_state)

        # Show complete flow
        final_messages = getattr(result, "messages", [])
        console.print(f"\n[cyan]🔄 Complete Flow:[/cyan]")
        for i, msg in enumerate(final_messages, 1):
            if hasattr(msg, "content"):
                role = msg.__class__.__name__.replace("Message", "")
                content = (
                    msg.content[:150] + "..." if len(msg.content) > 150 else msg.content
                )
                console.print(f"  {i}. [{role}] {content}")

        console.print("[green]✅ Routing test completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Routing test failed: {str(e)}[/red]")
        logger.error("Routing test failed", exc_info=True)


def main():
    """Main test runner."""

    console.print(
        Panel(
            """
🏗️ Haive ReactAgent Supervisor Test Suite

Architecture:
✅ ReactAgent with add_agent tool
✅ Dynamic routing tool with base model  
✅ Prompt template with agents in state
✅ Generic agent execution node
✅ Real LLM-powered routing decisions

Tests:
1. Basic supervisor functionality
2. Dynamic agent registration via tools
3. Complete routing flow with real agents
    """,
            title="ReactAgent Supervisor Tests",
            style="bold blue",
        )
    )

    async def run_all_tests():
        try:
            await test_supervisor_basic()
            await test_agent_registration()
            await test_routing_flow()

            console.print(Panel("🎉 All tests completed!", style="bold green"))

        except Exception as e:
            console.print(f"[red]❌ Test suite failed: {str(e)}[/red]")
            logger.error("Test suite failed", exc_info=True)

    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()
