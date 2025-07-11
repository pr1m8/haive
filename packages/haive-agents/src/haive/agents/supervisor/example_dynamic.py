"""Example usage of DynamicSupervisorAgent.

This example demonstrates the dynamic supervisor capabilities including:
- Runtime agent registration and deregistration
- Adaptive response handling
- Performance monitoring
- Dynamic configuration updates
"""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from rich.console import Console

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.dynamic_supervisor import DynamicSupervisorAgent

console = Console()


async def demonstrate_dynamic_supervisor():
    """Comprehensive demonstration of dynamic supervisor capabilities."""
    console.print("\n[bold blue]🚀 Dynamic Supervisor Agent Demo[/bold blue]\n")

    # Create supervisor with enhanced configuration
    supervisor = DynamicSupervisorAgent(
        name="demo_supervisor",
        engine=AugLLMConfig(),
        auto_rebuild_graph=True,
        enable_parallel_execution=False,
        max_execution_history=50,
    )

    console.print("✅ Created dynamic supervisor")

    # Phase 1: Start with no agents
    console.print("\n[bold cyan]Phase 1: Empty Supervisor[/bold cyan]")
    supervisor.print_supervisor_dashboard()

    # Phase 2: Add some agents dynamically
    console.print("\n[bold cyan]Phase 2: Adding Agents Dynamically[/bold cyan]")

    # Create specialized agents
    research_agent = ReactAgent(
        name="research_agent",
        engine=AugLLMConfig(),
    )

    writing_agent = SimpleAgent(
        name="writing_agent",
        engine=AugLLMConfig(),
    )

    math_agent = SimpleAgent(
        name="math_agent",
        engine=AugLLMConfig(),
    )

    # Register agents with capabilities and configs
    await supervisor.register_agent(
        research_agent,
        capability_description="Handles research tasks, web searches, and fact-finding",
        execution_config={"priority": 3, "execution_timeout": 180.0, "max_retries": 2},
    )

    await supervisor.register_agent(
        writing_agent,
        capability_description="Handles writing, editing, and content creation tasks",
        execution_config={
            "priority": 2,
            "execution_timeout": 120.0,
            "output_mode": "last_message",
        },
    )

    await supervisor.register_agent(
        math_agent,
        capability_description="Handles mathematical calculations and problem solving",
        execution_config={
            "priority": 2,
            "execution_timeout": 60.0,
            "custom_params": {"precision": "high"},
        },
    )

    console.print("✅ Registered 3 agents")
    supervisor.print_supervisor_dashboard()

    # Phase 3: Test supervisor routing
    console.print("\n[bold cyan]Phase 3: Testing Dynamic Routing[/bold cyan]")

    test_queries = [
        "What is the capital of France?",
        "Write a short poem about AI",
        "Calculate the square root of 144",
        "Research the latest developments in quantum computing",
        "Thank you, that's all I need",
    ]

    for i, query in enumerate(test_queries, 1):
        console.print(f"\n[yellow]Query {i}:[/yellow] {query}")

        try:
            # Create conversation state
            state = {
                "messages": [HumanMessage(content=query)],
                "configurable": {"thread_id": f"demo_session_{i}"},
            }

            # Run supervisor
            await supervisor.ainvoke(state)

            console.print(f"[green]✅ Query {i} completed[/green]")

            # Show performance after each query
            if i % 2 == 0:  # Show dashboard every 2 queries
                supervisor.print_supervisor_dashboard()

        except Exception as e:
            console.print(f"[red]❌ Query {i} failed: {e}[/red]")

    # Phase 4: Dynamic agent management
    console.print("\n[bold cyan]Phase 4: Dynamic Agent Management[/bold cyan]")

    # Update agent configuration
    console.print("Updating math_agent configuration...")
    await supervisor.update_agent_config(
        "math_agent",
        {
            "priority": 4,  # Increase priority
            "execution_timeout": 30.0,  # Reduce timeout
            "custom_params": {"precision": "ultra_high", "show_steps": True},
        },
    )

    # Add another agent
    console.print("Adding code_agent...")
    code_agent = SimpleAgent(
        name="code_agent",
        engine=AugLLMConfig(),
    )

    await supervisor.register_agent(
        code_agent,
        capability_description="Handles coding, debugging, and software development tasks",
        execution_config={
            "priority": 3,
            "execution_timeout": 240.0,
            "output_mode": "full_history",
        },
    )

    # Remove writing agent
    console.print("Removing writing_agent...")
    await supervisor.unregister_agent("writing_agent")

    supervisor.print_supervisor_dashboard()

    # Phase 5: Test with updated agent configuration
    console.print("\n[bold cyan]Phase 5: Testing Updated Configuration[/bold cyan]")

    updated_queries = [
        "Write a Python function to calculate fibonacci numbers",
        "What is 15 squared plus 20 cubed?",
        "Research current programming language trends",
    ]

    for i, query in enumerate(updated_queries, 1):
        console.print(f"\n[yellow]Updated Query {i}:[/yellow] {query}")

        try:
            state = {
                "messages": [HumanMessage(content=query)],
                "configurable": {"thread_id": f"updated_session_{i}"},
            }

            await supervisor.ainvoke(state)
            console.print(f"[green]✅ Updated Query {i} completed[/green]")

        except Exception as e:
            console.print(f"[red]❌ Updated Query {i} failed: {e}[/red]")

    # Phase 6: Performance analysis
    console.print("\n[bold cyan]Phase 6: Performance Analysis[/bold cyan]")

    performance_summary = supervisor.get_performance_summary()

    console.print("\n[bold yellow]Performance Summary:[/bold yellow]")
    console.print(f"Total Executions: {performance_summary.get('total_executions', 0)}")
    console.print(
        f"Overall Success Rate: {performance_summary.get('success_rate', 0.0):.1%}"
    )
    console.print(
        f"Most Used Agent: {performance_summary.get('most_used_agent', 'None')}"
    )

    # Show final dashboard
    supervisor.print_supervisor_dashboard()

    console.print("\n[bold green]🎉 Dynamic Supervisor Demo Complete![/bold green]")


async def demonstrate_parallel_execution():
    """Demonstrate parallel agent execution capabilities."""
    console.print("\n[bold blue]🔄 Parallel Execution Demo[/bold blue]\n")

    # Create supervisor with parallel execution enabled
    parallel_supervisor = DynamicSupervisorAgent(
        name="parallel_supervisor",
        engine=AugLLMConfig(),
        enable_parallel_execution=True,
        auto_rebuild_graph=True,
    )

    # Add multiple agents
    agents_to_add = [
        ("agent_1", "Handles type 1 tasks"),
        ("agent_2", "Handles type 2 tasks"),
        ("agent_3", "Handles type 3 tasks"),
    ]

    for agent_name, capability in agents_to_add:
        agent = SimpleAgent(name=agent_name, engine=AugLLMConfig())
        await parallel_supervisor.register_agent(agent, capability)

    console.print("✅ Created parallel supervisor with 3 agents")

    # Test parallel coordination
    parallel_query = (
        "Analyze this problem from multiple perspectives: How can AI improve education?"
    )

    console.print(f"\n[yellow]Parallel Query:[/yellow] {parallel_query}")

    try:
        state = {
            "messages": [HumanMessage(content=parallel_query)],
            "configurable": {"thread_id": "parallel_session"},
        }

        await parallel_supervisor.ainvoke(state)
        console.print("[green]✅ Parallel execution completed[/green]")

        parallel_supervisor.print_supervisor_dashboard()

    except Exception as e:
        console.print(f"[red]❌ Parallel execution failed: {e}[/red]")


async def demonstrate_adaptation_rules():
    """Demonstrate response adaptation capabilities."""
    console.print("\n[bold blue]🔧 Response Adaptation Demo[/bold blue]\n")

    # Create supervisor with adaptation enabled
    adaptive_supervisor = DynamicSupervisorAgent(
        name="adaptive_supervisor", engine=AugLLMConfig(), auto_rebuild_graph=True
    )

    # Create agent with adaptation rules
    adaptive_agent = SimpleAgent(
        name="adaptive_agent",
        engine=AugLLMConfig(),
    )

    # Register with custom adaptation configuration
    await adaptive_supervisor.register_agent(
        adaptive_agent,
        capability_description="Agent with response adaptation",
        execution_config={
            "output_mode": "last_message",
            "state_adapters": {
                "response_filter": {"remove_markdown": True},
                "length_limiter": {"max_length": 200},
            },
            "custom_params": {"adaptation_level": "high", "filter_sensitive": True},
        },
    )

    console.print("✅ Created adaptive supervisor with adaptation rules")

    # Test adaptation
    adaptation_query = (
        "Provide a detailed explanation with examples and markdown formatting"
    )

    console.print(f"\n[yellow]Adaptation Query:[/yellow] {adaptation_query}")

    try:
        state = {
            "messages": [HumanMessage(content=adaptation_query)],
            "configurable": {"thread_id": "adaptation_session"},
        }

        await adaptive_supervisor.ainvoke(state)
        console.print("[green]✅ Response adaptation completed[/green]")

        adaptive_supervisor.print_supervisor_dashboard()

    except Exception as e:
        console.print(f"[red]❌ Response adaptation failed: {e}[/red]")


async def main():
    """Run all dynamic supervisor demonstrations."""
    console.print("[bold magenta]Dynamic Supervisor Agent Examples[/bold magenta]")
    console.print("=" * 50)

    try:
        # Main dynamic supervisor demo
        await demonstrate_dynamic_supervisor()

        # Parallel execution demo
        await demonstrate_parallel_execution()

        # Response adaptation demo
        await demonstrate_adaptation_rules()

    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed with error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())
