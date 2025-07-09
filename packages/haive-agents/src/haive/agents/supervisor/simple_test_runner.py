"""Simple Test Runner for Dynamic Supervisor.

This demonstrates the core flow of how dynamic agent addition/removal works
and how it would integrate with eventual agent building capabilities.
"""

import asyncio
import logging
from typing import Any, Dict

from rich.console import Console
from rich.table import Table

# Mock imports for testing without full haive setup
console = Console()


class MockEngine:
    """Mock engine for testing without real LLM."""

    def __init__(self, name="mock_engine"):
        self.name = name
        self.tools = []
        self.tool_routes = {}

    async def ainvoke(self, messages, config=None):
        """Mock LLM response for testing."""

        class MockResponse:
            def __init__(self, content):
                self.content = content

        # Simple keyword-based routing for testing
        if hasattr(messages, "__iter__") and len(messages) > 0:
            last_message = str(messages[-1])
        else:
            last_message = str(messages)

        content_lower = last_message.lower()

        if "research" in content_lower or "search" in content_lower:
            return MockResponse(
                '{"target": "research_agent", "reasoning": "Request needs research capabilities", "confidence": 0.8}'
            )
        elif "math" in content_lower or "calculate" in content_lower:
            return MockResponse(
                '{"target": "math_agent", "reasoning": "Request needs mathematical computation", "confidence": 0.9}'
            )
        elif "write" in content_lower or "content" in content_lower:
            return MockResponse(
                '{"target": "writing_agent", "reasoning": "Request needs writing capabilities", "confidence": 0.7}'
            )
        elif "code" in content_lower or "program" in content_lower:
            return MockResponse(
                '{"target": "code_agent", "reasoning": "Request needs coding capabilities", "confidence": 0.8}'
            )
        else:
            return MockResponse(
                '{"target": "END", "reasoning": "No specific agent needed", "confidence": 0.5}'
            )


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, name, agent_type="MockAgent", tools=None):
        self.name = name
        self.agent_type = agent_type
        self.tools = tools or []
        self.engine = MockEngine(f"{name}_engine")

        # Add tools to engine
        if self.tools:
            self.engine.tools = self.tools
            self.engine.tool_routes = {tool: "langchain_tool" for tool in self.tools}

    async def ainvoke(self, state, config=None):
        """Mock agent execution."""

        class MockResult:
            def __init__(self, messages):
                self.messages = messages

        # Simulate agent response
        response_content = f"Response from {self.name}: I processed your request using my {len(self.tools)} tools."

        # Mock message type
        class MockMessage:
            def __init__(self, content):
                self.content = content

        return MockResult([MockMessage(response_content)])


class SimpleDynamicSupervisorTest:
    """Simplified test of dynamic supervisor capabilities."""

    def __init__(self):
        self.agents = {}
        self.agent_configs = {}
        self.choice_options = ["END"]
        self.tool_to_agent_mapping = {}
        self.execution_history = []
        self.routing_decisions = []

        console.print(
            "[bold blue]🚀 Simple Dynamic Supervisor Test Initialized[/bold blue]"
        )

    async def register_agent(
        self, agent, capability_description, execution_config=None
    ):
        """Register an agent in the test supervisor."""
        agent_name = agent.name

        # Add to registry
        self.agents[agent_name] = agent
        self.agent_configs[agent_name] = {
            "capability": capability_description,
            "config": execution_config or {},
            "tools": agent.tools,
        }

        # Update choice options
        if agent_name not in self.choice_options:
            self.choice_options.append(agent_name)

        # Update tool mapping
        for tool in agent.tools:
            self.tool_to_agent_mapping[tool] = agent_name

        console.print(f"[green]✅ Registered agent: {agent_name}[/green]")
        console.print(f"   Capability: {capability_description}")
        console.print(f"   Tools: {agent.tools}")

        return True

    async def unregister_agent(self, agent_name):
        """Remove an agent from the test supervisor."""
        if agent_name not in self.agents:
            console.print(f"[red]❌ Agent not found: {agent_name}[/red]")
            return False

        # Remove agent
        agent = self.agents.pop(agent_name)
        config = self.agent_configs.pop(agent_name)

        # Remove from choice options
        if agent_name in self.choice_options:
            self.choice_options.remove(agent_name)

        # Remove tool mappings
        for tool in config["tools"]:
            self.tool_to_agent_mapping.pop(tool, None)

        console.print(f"[red]➖ Unregistered agent: {agent_name}[/red]")
        return True

    async def route_request(self, request):
        """Simulate routing a request to an agent."""
        console.print(f"\n[yellow]📝 Processing request:[/yellow] {request}")

        # Simple keyword-based routing for testing
        request_lower = request.lower()

        routing_rules = {
            "research": "research_agent",
            "search": "research_agent",
            "calculate": "math_agent",
            "math": "math_agent",
            "write": "writing_agent",
            "content": "writing_agent",
            "code": "code_agent",
            "program": "code_agent",
        }

        selected_agent = None
        reasoning = "No matching keywords found"

        for keyword, agent_name in routing_rules.items():
            if keyword in request_lower and agent_name in self.agents:
                selected_agent = agent_name
                reasoning = f"Found keyword '{keyword}', routing to {agent_name}"
                break

        if not selected_agent:
            if self.agents:
                selected_agent = list(self.agents.keys())[0]
                reasoning = "No keyword match, using first available agent"
            else:
                selected_agent = "END"
                reasoning = "No agents available"

        # Record decision
        decision = {
            "target": selected_agent,
            "reasoning": reasoning,
            "request": request,
            "available_agents": list(self.agents.keys()),
        }
        self.routing_decisions.append(decision)

        console.print(f"[cyan]🎯 Routing decision: {selected_agent}[/cyan]")
        console.print(f"[dim]   Reasoning: {reasoning}[/dim]")

        # Execute agent if not END
        if selected_agent != "END" and selected_agent in self.agents:
            result = await self.execute_agent(selected_agent, request)
            return result

        return {"status": "completed", "target": selected_agent}

    async def execute_agent(self, agent_name, request):
        """Execute a specific agent."""
        agent = self.agents[agent_name]
        config = self.agent_configs[agent_name]

        console.print(f"[green]⚡ Executing {agent_name}...[/green]")

        # Mock execution
        result = await agent.ainvoke({"request": request})

        # Record execution
        execution_record = {
            "agent": agent_name,
            "request": request,
            "tools_used": config["tools"],
            "status": "success",
        }
        self.execution_history.append(execution_record)

        console.print(f"[green]✅ {agent_name} completed execution[/green]")
        return {"status": "success", "agent": agent_name, "result": result}

    def print_status(self):
        """Print current supervisor status."""
        # Agents table
        table = Table(title="🤖 Registered Agents")
        table.add_column("Agent", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Tools", style="yellow")
        table.add_column("Capability", style="blue")

        for name, agent in self.agents.items():
            config = self.agent_configs[name]
            table.add_row(
                name,
                agent.agent_type,
                ", ".join(agent.tools) if agent.tools else "None",
                (
                    config["capability"][:50] + "..."
                    if len(config["capability"]) > 50
                    else config["capability"]
                ),
            )

        console.print(table)

        # Statistics
        stats_table = Table(title="📊 Supervisor Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Total Agents", str(len(self.agents)))
        stats_table.add_row("Total Tools", str(len(self.tool_to_agent_mapping)))
        stats_table.add_row("Choice Options", str(len(self.choice_options)))
        stats_table.add_row("Executions", str(len(self.execution_history)))
        stats_table.add_row("Routing Decisions", str(len(self.routing_decisions)))

        console.print(stats_table)

        # Tool mapping
        if self.tool_to_agent_mapping:
            tool_table = Table(title="🔧 Tool-to-Agent Mapping")
            tool_table.add_column("Tool", style="yellow")
            tool_table.add_column("Agent", style="cyan")

            for tool, agent in self.tool_to_agent_mapping.items():
                tool_table.add_row(tool, agent)

            console.print(tool_table)


async def run_simple_test():
    """Run the simple test scenario."""

    console.print("[bold magenta]Simple Dynamic Supervisor Test[/bold magenta]")
    console.print("=" * 50)

    # Create test supervisor
    supervisor = SimpleDynamicSupervisorTest()

    # Phase 1: Start empty
    console.print("\n[bold cyan]Phase 1: Empty Supervisor[/bold cyan]")
    supervisor.print_status()

    # Phase 2: Add agents one by one
    console.print("\n[bold cyan]Phase 2: Adding Agents Dynamically[/bold cyan]")

    # Add research agent
    research_agent = MockAgent(
        name="research_agent",
        agent_type="ReactAgent",
        tools=["web_search", "wikipedia_search", "academic_search"],
    )

    await supervisor.register_agent(
        research_agent,
        "Handles research tasks, web searches, and information gathering",
    )

    # Add math agent
    math_agent = MockAgent(
        name="math_agent",
        agent_type="SimpleAgent",
        tools=["calculator", "equation_solver", "plot_generator"],
    )

    await supervisor.register_agent(
        math_agent,
        "Mathematical calculations, equation solving, and data visualization",
    )

    # Add writing agent
    writing_agent = MockAgent(
        name="writing_agent",
        agent_type="SimpleAgent",
        tools=["grammar_check", "style_editor", "content_generator"],
    )

    await supervisor.register_agent(
        writing_agent, "Content creation, writing, editing, and proofreading"
    )

    # Show status after additions
    supervisor.print_status()

    # Phase 3: Test routing
    console.print("\n[bold cyan]Phase 3: Testing Dynamic Routing[/bold cyan]")

    test_requests = [
        "Research the latest developments in AI",
        "Calculate the square root of 144",
        "Write a summary about quantum computing",
        "Search for information about Python programming",
        "Generate a mathematical proof",
        "Create content for a blog post",
    ]

    for request in test_requests:
        await supervisor.route_request(request)

    # Phase 4: Add more agents dynamically
    console.print("\n[bold cyan]Phase 4: Adding More Agents[/bold cyan]")

    code_agent = MockAgent(
        name="code_agent",
        agent_type="ReactAgent",
        tools=["code_executor", "syntax_checker", "debugger"],
    )

    await supervisor.register_agent(
        code_agent, "Code generation, debugging, testing, and execution"
    )

    # Test with new agent
    await supervisor.route_request("Debug this Python code and fix syntax errors")

    # Phase 5: Remove an agent
    console.print("\n[bold cyan]Phase 5: Removing Agent[/bold cyan]")

    await supervisor.unregister_agent("writing_agent")

    # Test routing after removal
    await supervisor.route_request("Write a technical document")

    # Phase 6: Final status
    console.print("\n[bold cyan]Phase 6: Final State[/bold cyan]")
    supervisor.print_status()

    console.print("\n[bold green]🎉 Simple Test Complete![/bold green]")


async def simulate_agent_building_flow():
    """Simulate how eventual agent building would work."""

    console.print("\n[bold blue]🏗️ Simulating Future Agent Building Flow[/bold blue]")

    supervisor = SimpleDynamicSupervisorTest()

    # Simulate agent building requests
    agent_building_requests = [
        {
            "request": "I need an agent that can translate languages",
            "agent_spec": {
                "name": "translation_agent",
                "type": "SimpleAgent",
                "tools": ["language_detector", "translator", "localization"],
                "capability": "Language translation and localization services",
            },
        },
        {
            "request": "Create an agent for image processing tasks",
            "agent_spec": {
                "name": "image_agent",
                "type": "ReactAgent",
                "tools": ["image_resizer", "filter_applier", "format_converter"],
                "capability": "Image processing, editing, and format conversion",
            },
        },
        {
            "request": "I need help with database queries and management",
            "agent_spec": {
                "name": "database_agent",
                "type": "ReactAgent",
                "tools": ["sql_executor", "schema_analyzer", "query_optimizer"],
                "capability": "Database management, query optimization, and analysis",
            },
        },
    ]

    for i, building_request in enumerate(agent_building_requests, 1):
        console.print(
            f"\n[yellow]Building Request {i}:[/yellow] {building_request['request']}"
        )

        # Simulate agent building process
        spec = building_request["agent_spec"]
        console.print(
            f"[dim]Analyzing request and generating agent specification...[/dim]"
        )
        console.print(f"[dim]Agent Name: {spec['name']}[/dim]")
        console.print(f"[dim]Agent Type: {spec['type']}[/dim]")
        console.print(f"[dim]Tools Needed: {spec['tools']}[/dim]")

        # Create the agent
        console.print(f"[green]🏗️  Building {spec['name']}...[/green]")

        new_agent = MockAgent(
            name=spec["name"], agent_type=spec["type"], tools=spec["tools"]
        )

        # Register the built agent
        await supervisor.register_agent(new_agent, spec["capability"])

        console.print(f"[green]✅ {spec['name']} built and registered![/green]")

    # Show final built state
    console.print("\n[bold cyan]Final Built State:[/bold cyan]")
    supervisor.print_status()

    # Test the built agents
    console.print("\n[bold cyan]Testing Built Agents:[/bold cyan]")

    test_requests_for_built = [
        "Translate this text to Spanish",
        "Resize this image and apply a filter",
        "Optimize this SQL query for better performance",
    ]

    for request in test_requests_for_built:
        await supervisor.route_request(request)

    console.print("\n[bold green]🏗️ Agent Building Simulation Complete![/bold green]")


async def main():
    """Run all test scenarios."""

    try:
        # Run simple test
        await run_simple_test()

        # Simulate agent building
        await simulate_agent_building_flow()

    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Test failed: {e}[/red]")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
