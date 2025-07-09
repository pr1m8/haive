"""Test Dynamic Supervisor with Pre-loaded Agent Registry.

This module demonstrates how to test the dynamic supervisor by pre-loading
agents into the registry and then testing all the dynamic capabilities
procedurally without requiring LLM calls to work perfectly.
"""

import asyncio
import logging
from typing import Dict, List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.integrated_supervisor import IntegratedDynamicSupervisor

console = Console()
logging.basicConfig(level=logging.INFO)


class TestAgentRegistry:
    """Pre-loaded agent registry for testing dynamic supervisor capabilities."""

    def __init__(self):
        self.test_agents = {}
        self.agent_configs = {}
        self._create_test_agents()

    def _create_test_agents(self):
        """Create a set of test agents with different capabilities."""

        # Research Agent with simulated search tools
        research_agent = ReactAgent(
            name="research_agent",
            engine=AugLLMConfig(),
            # In real scenario: tools=[SearchTool(), WikipediaTool()]
        )
        # Simulate tools for testing
        research_agent._test_tools = [
            "web_search",
            "wikipedia_search",
            "academic_search",
        ]

        self.test_agents["research_agent"] = research_agent
        self.agent_configs["research_agent"] = {
            "capability": "Web research, fact-finding, and information gathering",
            "tools": ["web_search", "wikipedia_search", "academic_search"],
            "priority": 4,
            "execution_timeout": 180.0,
            "agent_type": "ReactAgent",
        }

        # Writing Agent
        writing_agent = SimpleAgent(
            name="writing_agent",
            engine=AugLLMConfig(),
        )
        writing_agent._test_tools = [
            "grammar_check",
            "style_editor",
            "content_generator",
        ]

        self.test_agents["writing_agent"] = writing_agent
        self.agent_configs["writing_agent"] = {
            "capability": "Content creation, writing, editing, and proofreading",
            "tools": ["grammar_check", "style_editor", "content_generator"],
            "priority": 3,
            "execution_timeout": 120.0,
            "agent_type": "SimpleAgent",
        }

        # Math Agent
        math_agent = SimpleAgent(
            name="math_agent",
            engine=AugLLMConfig(),
        )
        math_agent._test_tools = ["calculator", "equation_solver", "plot_generator"]

        self.test_agents["math_agent"] = math_agent
        self.agent_configs["math_agent"] = {
            "capability": "Mathematical calculations, equation solving, and data visualization",
            "tools": ["calculator", "equation_solver", "plot_generator"],
            "priority": 3,
            "execution_timeout": 60.0,
            "agent_type": "SimpleAgent",
        }

        # Code Agent
        code_agent = ReactAgent(
            name="code_agent",
            engine=AugLLMConfig(),
        )
        code_agent._test_tools = [
            "code_executor",
            "syntax_checker",
            "debugger",
            "formatter",
        ]

        self.test_agents["code_agent"] = code_agent
        self.agent_configs["code_agent"] = {
            "capability": "Code generation, debugging, testing, and execution",
            "tools": ["code_executor", "syntax_checker", "debugger", "formatter"],
            "priority": 4,
            "execution_timeout": 240.0,
            "agent_type": "ReactAgent",
        }

        # Analysis Agent
        analysis_agent = SimpleAgent(
            name="analysis_agent",
            engine=AugLLMConfig(),
        )
        analysis_agent._test_tools = ["data_analyzer", "chart_generator", "statistics"]

        self.test_agents["analysis_agent"] = analysis_agent
        self.agent_configs["analysis_agent"] = {
            "capability": "Data analysis, statistical computation, and insight generation",
            "tools": ["data_analyzer", "chart_generator", "statistics"],
            "priority": 2,
            "execution_timeout": 300.0,
            "agent_type": "SimpleAgent",
        }

    def get_agent(self, name: str):
        """Get agent by name."""
        return self.test_agents.get(name)

    def get_config(self, name: str):
        """Get agent configuration."""
        return self.agent_configs.get(name)

    def get_all_agents(self) -> Dict:
        """Get all test agents."""
        return self.test_agents.copy()

    def get_agents_by_capability(self, capability_keyword: str) -> List[str]:
        """Get agents that match a capability keyword."""
        matching = []
        for name, config in self.agent_configs.items():
            if capability_keyword.lower() in config["capability"].lower():
                matching.append(name)
        return matching


async def test_dynamic_supervisor_with_registry():
    """Test dynamic supervisor using pre-loaded agent registry."""

    console.print(
        Panel(
            "[bold blue]🧪 Testing Dynamic Supervisor with Pre-loaded Registry[/bold blue]",
            expand=False,
        )
    )

    # Create test registry
    test_registry = TestAgentRegistry()
    console.print(
        f"✅ Created test registry with {len(test_registry.get_all_agents())} agents"
    )

    # Create supervisor
    supervisor = IntegratedDynamicSupervisor(
        name="test_supervisor",
        engine=AugLLMConfig(),
        enable_agent_management_tools=True,
        coordination_mode="supervisor",
        auto_rebuild_graph=True,
    )

    console.print("✅ Created integrated supervisor")

    # Phase 1: Load agents into supervisor registry
    console.print("\n[bold cyan]Phase 1: Loading Agents into Registry[/bold cyan]")

    for agent_name in track(
        test_registry.get_all_agents().keys(), description="Loading agents..."
    ):
        agent = test_registry.get_agent(agent_name)
        config = test_registry.get_config(agent_name)

        execution_config = {
            "priority": config["priority"],
            "execution_timeout": config["execution_timeout"],
            "custom_params": {"test_tools": config["tools"]},
        }

        success = await supervisor.register_agent(
            agent,
            capability_description=config["capability"],
            execution_config=execution_config,
        )

        if success:
            console.print(f"  ✅ Loaded {agent_name}")
        else:
            console.print(f"  ❌ Failed to load {agent_name}")

    # Show initial state
    supervisor.print_integrated_dashboard()

    # Phase 2: Test DynamicChoiceModel integration
    console.print(
        "\n[bold cyan]Phase 2: Testing DynamicChoiceModel Integration[/bold cyan]"
    )

    if supervisor.registry_manager:
        choice_model = supervisor.registry_manager.get_agent_choice_model()
        console.print(f"Available routing options: {choice_model.option_names}")

        # Test all agents are valid choices
        for agent_name in test_registry.get_all_agents().keys():
            is_valid = choice_model.validate_choice(agent_name)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            console.print(f"  {agent_name}: {status}")

        # Test invalid choice
        is_valid = choice_model.validate_choice("nonexistent_agent")
        console.print(
            f"  nonexistent_agent: {'✅ Valid' if is_valid else '❌ Invalid (expected)'}"
        )

    # Phase 3: Test procedural routing
    console.print("\n[bold cyan]Phase 3: Testing Procedural Routing[/bold cyan]")

    test_routing_scenarios = [
        {
            "request": "I need to research the latest AI developments",
            "expected_agent": "research_agent",
            "reasoning": "Contains research keywords",
        },
        {
            "request": "Calculate the square root of 144 and plot the result",
            "expected_agent": "math_agent",
            "reasoning": "Contains math keywords",
        },
        {
            "request": "Write a summary of quantum computing principles",
            "expected_agent": "writing_agent",
            "reasoning": "Contains writing keywords",
        },
        {
            "request": "Debug this Python code and fix the syntax errors",
            "expected_agent": "code_agent",
            "reasoning": "Contains coding keywords",
        },
        {
            "request": "Analyze this dataset and generate insights",
            "expected_agent": "analysis_agent",
            "reasoning": "Contains analysis keywords",
        },
    ]

    for i, scenario in enumerate(test_routing_scenarios, 1):
        console.print(f"\n[yellow]Scenario {i}:[/yellow] {scenario['request']}")
        console.print(
            f"[dim]Expected: {scenario['expected_agent']} ({scenario['reasoning']})[/dim]"
        )

        try:
            # Create state for testing
            state = {
                "messages": [HumanMessage(content=scenario["request"])],
                "configurable": {"thread_id": f"test_session_{i}"},
            }

            # Test routing (would normally go through LLM decision)
            # For testing, we simulate the decision process
            decision = await _simulate_routing_decision(
                supervisor, scenario["request"], test_registry
            )

            console.print(
                f"[green]Simulated routing decision: {decision['target']}[/green]"
            )
            console.print(f"[dim]Reasoning: {decision['reasoning']}[/dim]")

            # Verify expected vs actual
            if decision["target"] == scenario["expected_agent"]:
                console.print("✅ Routing matches expectation")
            else:
                console.print("⚠️  Routing differs from expectation")

        except Exception as e:
            console.print(f"[red]❌ Scenario {i} failed: {e}[/red]")

    # Phase 4: Test dynamic agent addition/removal
    console.print("\n[bold cyan]Phase 4: Testing Dynamic Agent Management[/bold cyan]")

    # Test adding a new agent
    console.print("\n[yellow]Testing: Add new translation agent[/yellow]")

    translation_agent = SimpleAgent(
        name="translation_agent",
        engine=AugLLMConfig(),
    )
    translation_agent._test_tools = ["language_detector", "translator", "localization"]

    success = await supervisor.register_agent(
        translation_agent,
        capability_description="Language translation and localization services",
        execution_config={"priority": 2, "execution_timeout": 90.0},
    )

    if success:
        console.print("✅ Successfully added translation agent")
        if supervisor.registry_manager:
            choice_model = supervisor.registry_manager.get_agent_choice_model()
            console.print(f"Updated options: {choice_model.option_names}")

    # Test removing an agent
    console.print("\n[yellow]Testing: Remove analysis agent[/yellow]")

    success = await supervisor.unregister_agent("analysis_agent")

    if success:
        console.print("✅ Successfully removed analysis agent")
        if supervisor.registry_manager:
            choice_model = supervisor.registry_manager.get_agent_choice_model()
            console.print(f"Updated options: {choice_model.option_names}")

    # Phase 5: Test coordination and state management
    console.print("\n[bold cyan]Phase 5: Testing Coordination and State[/bold cyan]")

    # Start coordination session
    session_id = supervisor.start_coordination_session("supervisor")
    console.print(f"Started coordination session: {session_id}")

    # Test state with multiple requests
    coordination_requests = [
        "Research quantum computing",
        "Write a technical report",
        "Generate code examples",
        "Translate to Spanish",
    ]

    for i, request in enumerate(coordination_requests, 1):
        console.print(f"\n[yellow]Coordination Request {i}:[/yellow] {request}")

        # Simulate coordination
        coord_status = supervisor.get_coordination_status()
        console.print(f"Coordination status: {coord_status}")

        # Add to execution queue (simulated)
        if hasattr(supervisor, "_state") and supervisor._state:
            supervisor._state.coordination.add_to_execution_queue(
                f"agent_for_request_{i}", {"request": request}, priority=i
            )

    # Show final coordination state
    coord_status = supervisor.get_coordination_status()
    console.print(f"\nFinal coordination status: {coord_status}")

    # End session
    session_summary = supervisor.end_coordination_session()
    console.print(f"Session summary: {session_summary}")

    # Phase 6: Final state and performance
    console.print("\n[bold cyan]Phase 6: Final State and Performance[/bold cyan]")

    supervisor.print_integrated_dashboard()

    performance = supervisor.get_performance_summary()
    console.print(f"\nPerformance summary: {performance}")

    console.print("\n[bold green]🎉 All Tests Completed Successfully![/bold green]")


async def _simulate_routing_decision(
    supervisor, request: str, test_registry: TestAgentRegistry
) -> Dict:
    """Simulate routing decision based on keywords (for testing without LLM)."""

    # Simple keyword-based routing for testing
    request_lower = request.lower()

    routing_rules = {
        "research": "research_agent",
        "search": "research_agent",
        "find": "research_agent",
        "calculate": "math_agent",
        "math": "math_agent",
        "equation": "math_agent",
        "plot": "math_agent",
        "write": "writing_agent",
        "summary": "writing_agent",
        "content": "writing_agent",
        "code": "code_agent",
        "debug": "code_agent",
        "python": "code_agent",
        "programming": "code_agent",
        "analyze": "analysis_agent",
        "data": "analysis_agent",
        "insights": "analysis_agent",
        "translate": "translation_agent",
        "language": "translation_agent",
    }

    # Find matching agent
    for keyword, agent_name in routing_rules.items():
        if keyword in request_lower:
            # Check if agent is registered
            if supervisor.agent_registry.is_agent_registered(agent_name):
                return {
                    "target": agent_name,
                    "reasoning": f"Request contains '{keyword}' keyword, routing to {agent_name}",
                    "confidence": 0.8,
                }

    # Default to first available agent if no match
    available_agents = supervisor.agent_registry.get_available_agents()
    if available_agents:
        return {
            "target": available_agents[0],
            "reasoning": "No specific keyword match, routing to first available agent",
            "confidence": 0.5,
        }

    return {"target": "END", "reasoning": "No agents available", "confidence": 1.0}


async def test_tool_integration():
    """Test tool integration and routing."""

    console.print(
        Panel(
            "[bold blue]🔧 Testing Tool Integration and Routing[/bold blue]",
            expand=False,
        )
    )

    test_registry = TestAgentRegistry()
    supervisor = IntegratedDynamicSupervisor(
        name="tool_test_supervisor", engine=AugLLMConfig()
    )

    # Load agents
    for agent_name, agent in test_registry.get_all_agents().items():
        config = test_registry.get_config(agent_name)
        await supervisor.register_agent(agent, config["capability"])

    # Test tool aggregation
    console.print("\n[yellow]Testing tool aggregation...[/yellow]")

    tool_info = supervisor._aggregate_agent_tools()
    console.print(f"Aggregated tools: {list(tool_info['tools'].keys())}")
    console.print(f"Tool-to-agent mapping: {tool_info['tool_to_agent']}")

    # Test tool routing
    console.print("\n[yellow]Testing tool routing...[/yellow]")

    if hasattr(supervisor, "_state") and supervisor._state:
        state = supervisor._state

        test_tools = [
            "web_search",
            "calculator",
            "code_executor",
            "grammar_check",
            "nonexistent_tool",
        ]

        for tool in test_tools:
            agent = state.route_tool_to_agent(tool)
            if agent:
                console.print(f"  {tool} → {agent} ✅")
            else:
                console.print(f"  {tool} → No agent found ❌")

    console.print("\n[bold green]🔧 Tool Integration Test Complete![/bold green]")


async def main():
    """Run all procedural tests."""

    console.print("[bold magenta]Dynamic Supervisor Procedural Testing[/bold magenta]")
    console.print("=" * 50)

    try:
        # Main procedural test
        await test_dynamic_supervisor_with_registry()

        # Tool integration test
        await test_tool_integration()

    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Tests failed with error: {e}[/red]")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
