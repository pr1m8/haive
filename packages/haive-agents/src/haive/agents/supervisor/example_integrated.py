"""Example of Integrated Dynamic Multi-Agent Supervisor.

This example demonstrates:
- Adding agents dynamically through tools
- DynamicChoiceModel integration
- Multi-agent coordination
- Tool-based agent management
- Dynamic routing based on agent capabilities and tools
"""

import asyncio
from typing import Any, Dict

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from rich.console import Console

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.integrated_supervisor import IntegratedDynamicSupervisor

console = Console()


async def demonstrate_integrated_supervisor():
    """Complete demonstration of integrated dynamic supervisor."""
    console.print(
        "\n[bold blue]🚀 Integrated Dynamic Multi-Agent Supervisor Demo[/bold blue]\n"
    )

    # Create integrated supervisor with all features enabled
    supervisor = IntegratedDynamicSupervisor(
        name="integrated_supervisor",
        engine=AugLLMConfig(),
        enable_agent_management_tools=True,
        coordination_mode="supervisor",
        auto_rebuild_graph=True,
    )

    console.print("✅ Created integrated supervisor with full capabilities")

    # Register agent constructors for dynamic creation
    supervisor.register_agent_constructor("SimpleAgent", SimpleAgent)
    supervisor.register_agent_constructor("ReactAgent", ReactAgent)

    console.print("✅ Registered agent constructors")

    # Phase 1: Start with empty supervisor and demonstrate tool-based agent addition
    console.print("\n[bold cyan]Phase 1: Dynamic Agent Addition via Tools[/bold cyan]")

    supervisor.print_integrated_dashboard()

    # Simulate tool calls for adding agents (in real usage, these would come from LLM tool calls)
    console.print(
        "\n[yellow]Simulating: 'add a research agent that can search the web'[/yellow]"
    )

    # Manually add agents to demonstrate the flow (normally done via tool calls)
    research_agent = ReactAgent(
        name="research_agent",
        engine=AugLLMConfig(),
        # In real scenario, would have actual tools like SearchTool()
    )

    await supervisor.register_agent(
        research_agent,
        capability_description="Handles research tasks, web searches, and fact-finding",
        execution_config={"priority": 3, "execution_timeout": 180.0, "max_retries": 2},
    )

    console.print("✅ Added research agent dynamically")

    # Add writing agent
    writing_agent = SimpleAgent(
        name="writing_agent",
        engine=AugLLMConfig(),
    )

    await supervisor.register_agent(
        writing_agent,
        capability_description="Handles writing, editing, and content creation",
        execution_config={"priority": 2, "output_mode": "last_message"},
    )

    console.print("✅ Added writing agent dynamically")
    supervisor.print_integrated_dashboard()

    # Phase 2: Demonstrate DynamicChoiceModel integration
    console.print("\n[bold cyan]Phase 2: DynamicChoiceModel Routing[/bold cyan]")

    if supervisor.registry_manager:
        choice_model = supervisor.registry_manager.get_agent_choice_model()
        console.print(f"Choice model options: {choice_model.option_names}")

        # Test choice validation
        test_choices = ["research_agent", "writing_agent", "nonexistent_agent", "END"]
        for choice in test_choices:
            is_valid = choice_model.validate_choice(choice)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            console.print(f"  {choice}: {status}")

    # Phase 3: Multi-agent coordination
    console.print("\n[bold cyan]Phase 3: Multi-Agent Coordination[/bold cyan]")

    # Start coordination session
    session_id = supervisor.start_coordination_session("supervisor")
    console.print(f"Started coordination session: {session_id}")

    # Simulate requests that require different agents
    test_requests = [
        "Research the latest AI developments",
        "Write a summary of quantum computing",
        "Find information about Python programming and create a tutorial",
    ]

    for i, request in enumerate(test_requests, 1):
        console.print(f"\n[yellow]Request {i}:[/yellow] {request}")

        try:
            # Create state for request
            state = {
                "messages": [HumanMessage(content=request)],
                "configurable": {"thread_id": f"coord_session_{i}"},
            }

            # Run supervisor (this would trigger coordination)
            await supervisor.ainvoke(state)
            console.print(f"[green]✅ Request {i} processed[/green]")

            # Show coordination status
            coord_status = supervisor.get_coordination_status()
            console.print(f"Coordination status: {coord_status}")

        except Exception as e:
            console.print(f"[red]❌ Request {i} failed: {e}[/red]")

    # Phase 4: Tool-based agent management
    console.print("\n[bold cyan]Phase 4: Tool-Based Agent Management[/bold cyan]")

    # Simulate agent management requests
    mgmt_requests = [
        "List all available agents",
        "Add a math agent for calculations",
        "Remove the writing agent",
        "Change the research agent priority to 5",
    ]

    for i, request in enumerate(mgmt_requests, 1):
        console.print(f"\n[yellow]Management Request {i}:[/yellow] {request}")

        try:
            # In real usage, these would be processed by the agent management tools
            # Here we simulate the effects

            if "list" in request.lower():
                agents = supervisor.agent_registry.get_available_agents()
                console.print(f"Available agents: {agents}")

            elif "add a math agent" in request.lower():
                math_agent = SimpleAgent(
                    name="math_agent",
                    engine=AugLLMConfig(),
                )

                await supervisor.register_agent(
                    math_agent,
                    capability_description="Handles mathematical calculations and computations",
                    execution_config={"priority": 2},
                )
                console.print("✅ Added math agent")

            elif "remove" in request.lower() and "writing" in request.lower():
                success = await supervisor.unregister_agent("writing_agent")
                status = "✅ Removed" if success else "❌ Failed to remove"
                console.print(f"{status} writing agent")

            elif "change" in request.lower() and "priority" in request.lower():
                success = await supervisor.update_agent_config(
                    "research_agent", {"priority": 5}
                )
                status = "✅ Updated" if success else "❌ Failed to update"
                console.print(f"{status} research agent priority")

        except Exception as e:
            console.print(f"[red]❌ Management request {i} failed: {e}[/red]")

    # Phase 5: Final state and performance
    console.print("\n[bold cyan]Phase 5: Final State and Performance[/bold cyan]")

    supervisor.print_integrated_dashboard()

    # Show coordination session summary
    session_summary = supervisor.end_coordination_session()
    console.print(f"\nCoordination session summary: {session_summary}")

    # Performance summary
    performance = supervisor.get_performance_summary()
    console.print(f"\nPerformance summary: {performance}")

    console.print("\n[bold green]🎉 Integrated Supervisor Demo Complete![/bold green]")


async def demonstrate_dynamic_choice_model_integration():
    """Demonstrate DynamicChoiceModel integration specifically."""
    console.print("\n[bold blue]🎯 DynamicChoiceModel Integration Demo[/bold blue]\n")

    supervisor = IntegratedDynamicSupervisor(
        name="choice_model_supervisor",
        engine=AugLLMConfig(),
        enable_agent_management_tools=True,
    )

    # Add agents one by one and show choice model updates
    agents_to_add = [
        ("researcher", "ReactAgent", "Research and fact-finding"),
        ("writer", "SimpleAgent", "Content creation and writing"),
        ("calculator", "SimpleAgent", "Mathematical computations"),
        ("analyzer", "ReactAgent", "Data analysis and insights"),
    ]

    for agent_name, agent_type, capability in agents_to_add:
        console.print(f"\n[yellow]Adding {agent_name}...[/yellow]")

        # Create and register agent
        if agent_type == "ReactAgent":
            agent = ReactAgent(name=agent_name, engine=AugLLMConfig())
        else:
            agent = SimpleAgent(name=agent_name, engine=AugLLMConfig())

        await supervisor.register_agent(agent, capability)

        # Show updated choice model
        if supervisor.registry_manager:
            choice_model = supervisor.registry_manager.get_agent_choice_model()
            console.print(f"Choice model updated: {choice_model.option_names}")

            # Test the model
            try:
                test_instance = choice_model.current_model(choice=agent_name)
                console.print(f"✅ Valid choice created: {test_instance.choice}")
            except Exception as e:
                console.print(f"❌ Choice validation failed: {e}")

    # Demonstrate dynamic removal
    console.print("\n[yellow]Removing calculator agent...[/yellow]")
    await supervisor.unregister_agent("calculator")

    if supervisor.registry_manager:
        choice_model = supervisor.registry_manager.get_agent_choice_model()
        console.print(f"Choice model after removal: {choice_model.option_names}")

    console.print(
        "\n[bold green]🎯 DynamicChoiceModel Integration Demo Complete![/bold green]"
    )


async def demonstrate_tool_routing():
    """Demonstrate tool-based routing to agents."""
    console.print("\n[bold blue]🔧 Tool-Based Routing Demo[/bold blue]\n")

    supervisor = IntegratedDynamicSupervisor(
        name="tool_routing_supervisor", engine=AugLLMConfig()
    )

    # Add agents with different tool capabilities
    console.print("Setting up agents with different tools...")

    # Research agent with search tools
    research_agent = ReactAgent(
        name="research_agent",
        engine=AugLLMConfig(),
        # In real scenario: tools=[SearchTool(), WikipediaTool()]
    )

    await supervisor.register_agent(
        research_agent, "Research agent with search and Wikipedia tools"
    )

    # Math agent with calculation tools
    math_agent = SimpleAgent(
        name="math_agent",
        engine=AugLLMConfig(),
        # In real scenario: tools=[CalculatorTool(), PlotTool()]
    )

    await supervisor.register_agent(
        math_agent, "Math agent with calculator and plotting tools"
    )

    # Show tool-to-agent mapping
    if hasattr(supervisor, "_state") and supervisor._state:
        state = supervisor._state
        console.print(
            f"Tool-to-agent mapping: {state.agent_registry.tool_to_agent_mapping}"
        )

        # Simulate tool routing
        test_tools = ["search", "calculator", "wikipedia", "plot"]
        for tool in test_tools:
            agent = state.route_tool_to_agent(tool)
            if agent:
                console.print(f"Tool '{tool}' → Agent '{agent}'")
            else:
                console.print(f"Tool '{tool}' → No agent found")

    console.print("\n[bold green]🔧 Tool-Based Routing Demo Complete![/bold green]")


async def main():
    """Run all integrated supervisor demonstrations."""
    console.print(
        "[bold magenta]Integrated Dynamic Multi-Agent Supervisor Examples[/bold magenta]"
    )
    console.print("=" * 60)

    try:
        # Main integrated demo
        await demonstrate_integrated_supervisor()

        # DynamicChoiceModel specific demo
        await demonstrate_dynamic_choice_model_integration()

        # Tool routing demo
        await demonstrate_tool_routing()

    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed with error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())
