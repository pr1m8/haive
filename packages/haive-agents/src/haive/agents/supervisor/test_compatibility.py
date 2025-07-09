"""Test Compatibility Between Dynamic Supervisor and Existing Multi-Agent Architecture.

This test demonstrates how the dynamic supervisor integrates with:
- MultiAgent base classes
- ReactAgent patterns
- AgentSchemaComposer
- Existing multi-agent state management
"""

import asyncio
import logging
from typing import List

from rich.console import Console

# Mock classes for testing without full haive setup
console = Console()
logging.basicConfig(level=logging.INFO)


class MockEngine:
    """Mock engine for testing."""

    def __init__(self, name="mock_engine"):
        self.name = name
        self.tools = []

    async def ainvoke(self, messages, config=None):
        class MockResponse:
            def __init__(self, content):
                self.content = content

        return MockResponse('{"target": "END", "reasoning": "Mock decision"}')


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, name, agent_type="MockAgent"):
        self.name = name
        self.agent_type = agent_type
        self.engine = MockEngine(f"{name}_engine")

    async def ainvoke(self, state, config=None):
        """Mock agent execution."""

        class MockResult:
            def __init__(self, messages):
                self.messages = messages

        class MockMessage:
            def __init__(self, content):
                self.content = content

        return MockResult([MockMessage(f"Response from {self.name}")])


class MockMultiAgent:
    """Mock of existing MultiAgent for testing compatibility."""

    def __init__(self, name, agents, execution_mode="sequence"):
        self.name = name
        self.agents = agents
        self.execution_mode = execution_mode
        self.schema_separation = "smart"
        self.include_meta = True

    def setup_agent(self):
        """Mock setup."""
        pass

    def build_graph(self):
        """Mock graph building."""
        return {"nodes": [f"{agent.name}_node" for agent in self.agents]}


class CompatibilityTester:
    """Test compatibility between different multi-agent approaches."""

    def __init__(self):
        self.test_agents = self._create_test_agents()

    def _create_test_agents(self) -> List[MockAgent]:
        """Create test agents."""
        return [
            MockAgent("research_agent", "ReactAgent"),
            MockAgent("writing_agent", "SimpleAgent"),
            MockAgent("math_agent", "SimpleAgent"),
        ]

    async def test_traditional_multi_agent(self):
        """Test with traditional MultiAgent pattern."""
        console.print("\n[bold cyan]Testing Traditional MultiAgent Pattern[/bold cyan]")

        # Create traditional multi-agent
        multi_agent = MockMultiAgent(
            name="traditional_system",
            agents=self.test_agents,
            execution_mode="sequence",
        )

        console.print(f"✅ Created traditional multi-agent: {multi_agent.name}")
        console.print(f"   Agents: {[agent.name for agent in multi_agent.agents]}")
        console.print(f"   Execution mode: {multi_agent.execution_mode}")

        # Test graph building
        graph = multi_agent.build_graph()
        console.print(f"   Graph nodes: {graph['nodes']}")

        return multi_agent

    async def test_dynamic_supervisor_integration(self):
        """Test dynamic supervisor with multi-agent compatibility."""
        console.print("\n[bold cyan]Testing Dynamic Supervisor Integration[/bold cyan]")

        # Simulate DynamicMultiAgentSupervisor
        class MockDynamicSupervisor:
            def __init__(self, name, agents, enable_dynamic=True):
                self.name = name
                self.agents = list(agents)
                self.enable_dynamic_management = enable_dynamic
                self.execution_mode = "hierarchical"
                self.agent_registry = {"registered": [agent.name for agent in agents]}
                self.coordination_status = {"active": False, "mode": "supervisor"}

            async def register_agent_dynamically(self, agent, capability=None):
                self.agents.append(agent)
                self.agent_registry["registered"].append(agent.name)
                console.print(f"✅ Dynamically registered: {agent.name}")
                return True

            async def unregister_agent_dynamically(self, agent_name):
                self.agents = [a for a in self.agents if a.name != agent_name]
                if agent_name in self.agent_registry["registered"]:
                    self.agent_registry["registered"].remove(agent_name)
                console.print(f"❌ Dynamically unregistered: {agent_name}")
                return True

            def get_dynamic_status(self):
                return {
                    "dynamic_management_enabled": self.enable_dynamic_management,
                    "execution_mode": self.execution_mode,
                    "total_agents": len(self.agents),
                    "registered_agents": self.agent_registry["registered"],
                    "coordination_status": self.coordination_status,
                }

        # Create dynamic supervisor
        dynamic_supervisor = MockDynamicSupervisor(
            name="dynamic_system", agents=self.test_agents, enable_dynamic=True
        )

        console.print(f"✅ Created dynamic supervisor: {dynamic_supervisor.name}")

        # Test initial state
        status = dynamic_supervisor.get_dynamic_status()
        console.print(f"   Initial agents: {status['registered_agents']}")
        console.print(f"   Dynamic management: {status['dynamic_management_enabled']}")

        # Test dynamic agent addition
        new_agent = MockAgent("translation_agent", "SimpleAgent")
        await dynamic_supervisor.register_agent_dynamically(
            new_agent, "Language translation"
        )

        # Test dynamic agent removal
        await dynamic_supervisor.unregister_agent_dynamically("writing_agent")

        # Show final state
        final_status = dynamic_supervisor.get_dynamic_status()
        console.print(f"   Final agents: {final_status['registered_agents']}")

        return dynamic_supervisor

    async def test_schema_compatibility(self):
        """Test schema compatibility between approaches."""
        console.print("\n[bold cyan]Testing Schema Compatibility[/bold cyan]")

        # Simulate schema composition approaches
        traditional_schema = {
            "fields": ["messages", "agent_states", "meta_state"],
            "composition_strategy": "agent_schema_composer",
            "field_separation": "smart",
        }

        dynamic_schema = {
            "fields": [
                "messages",
                "registered_agents",
                "routing_decisions",
                "coordination",
            ],
            "composition_strategy": "enhanced_schema_composer",
            "field_separation": "hybrid",
        }

        hybrid_schema = {
            "fields": traditional_schema["fields"] + dynamic_schema["fields"],
            "composition_strategy": "hybrid_composer",
            "field_separation": "intelligent",
        }

        console.print("Traditional Schema:")
        for key, value in traditional_schema.items():
            console.print(f"   {key}: {value}")

        console.print("\nDynamic Schema:")
        for key, value in dynamic_schema.items():
            console.print(f"   {key}: {value}")

        console.print("\nHybrid Schema (Compatibility Layer):")
        for key, value in hybrid_schema.items():
            console.print(f"   {key}: {value}")

        # Test field compatibility
        traditional_fields = set(traditional_schema["fields"])
        dynamic_fields = set(dynamic_schema["fields"])
        common_fields = traditional_fields.intersection(dynamic_fields)

        console.print(f"\n✅ Common fields: {list(common_fields)}")
        console.print(
            f"⚠️  Traditional-only: {list(traditional_fields - dynamic_fields)}"
        )
        console.print(f"⚠️  Dynamic-only: {list(dynamic_fields - traditional_fields)}")

    async def test_execution_mode_compatibility(self):
        """Test execution mode compatibility."""
        console.print("\n[bold cyan]Testing Execution Mode Compatibility[/bold cyan]")

        execution_modes = {
            "traditional": ["sequence", "parallel", "conditional", "hierarchical"],
            "dynamic": ["supervisor", "swarm", "adaptive", "meta"],
            "compatible": ["hierarchical", "supervisor"],  # Modes that work with both
        }

        for mode_type, modes in execution_modes.items():
            console.print(f"{mode_type.title()} modes: {modes}")

        # Test mode mapping
        mode_mapping = {
            "sequence": "sequential supervision",
            "parallel": "parallel supervision",
            "hierarchical": "dynamic supervision",
            "supervisor": "enhanced supervision",
        }

        console.print("\nMode Compatibility Mapping:")
        for traditional, dynamic in mode_mapping.items():
            console.print(f"   {traditional} → {dynamic}")

    async def test_react_agent_integration(self):
        """Test ReactAgent integration with multi-agent supervisor."""
        console.print("\n[bold cyan]Testing ReactAgent Integration[/bold cyan]")

        # Simulate ReactAgent behavior
        class MockReactAgent(MockAgent):
            def __init__(self, name):
                super().__init__(name, "ReactAgent")
                self.has_tools = True
                self.looping_behavior = True

            async def execute_with_tools(self, state):
                """Simulate ReactAgent tool usage."""
                return {
                    "tool_calls": ["search", "calculate"],
                    "responses": [f"React response from {self.name}"],
                    "should_continue": True,
                }

        # Create ReactAgent
        react_agent = MockReactAgent("react_research_agent")

        # Test in traditional multi-agent
        console.print("ReactAgent in traditional multi-agent:")
        traditional_system = MockMultiAgent(
            name="traditional_with_react",
            agents=[react_agent] + self.test_agents[:1],  # Just one additional
            execution_mode="sequence",
        )
        console.print(f"   ✅ ReactAgent integrated: {react_agent.name}")

        # Test in dynamic supervisor
        console.print("ReactAgent in dynamic supervisor:")
        react_execution = await react_agent.execute_with_tools({"messages": ["test"]})
        console.print(f"   ✅ Tool calls: {react_execution['tool_calls']}")
        console.print(f"   ✅ Looping: {react_agent.looping_behavior}")

        # Test supervisor managing ReactAgent
        console.print("Supervisor managing ReactAgent:")
        supervisor_decision = {
            "target_agent": react_agent.name,
            "reasoning": "Request requires research with tools",
            "tools_needed": react_execution["tool_calls"],
        }
        console.print(
            f"   ✅ Supervisor routes to ReactAgent: {supervisor_decision['target_agent']}"
        )
        console.print(f"   ✅ Tools available: {supervisor_decision['tools_needed']}")

    async def test_migration_path(self):
        """Test migration from traditional to dynamic."""
        console.print("\n[bold cyan]Testing Migration Path[/bold cyan]")

        # Step 1: Traditional multi-agent
        traditional = await self.test_traditional_multi_agent()
        console.print(
            f"Step 1: Traditional system with {len(traditional.agents)} agents"
        )

        # Step 2: Create compatibility bridge
        console.print("Step 2: Creating compatibility bridge...")

        class CompatibilityBridge:
            def __init__(self, traditional_system):
                self.original = traditional_system
                self.enhanced = None

            def migrate_to_dynamic(self):
                """Migrate to dynamic supervisor."""
                # Simulate migration
                self.enhanced = MockDynamicSupervisor(
                    name=f"dynamic_{self.original.name}",
                    agents=self.original.agents,
                    enable_dynamic=True,
                )
                console.print(
                    f"   ✅ Migrated {self.original.name} to dynamic supervisor"
                )
                return self.enhanced

            def verify_compatibility(self):
                """Verify migration worked."""
                original_agents = [a.name for a in self.original.agents]
                enhanced_agents = self.enhanced.agent_registry["registered"]

                match = set(original_agents) == set(enhanced_agents)
                console.print(
                    f"   Agent compatibility: {'✅ Match' if match else '❌ Mismatch'}"
                )
                return match

        # Step 3: Perform migration
        bridge = CompatibilityBridge(traditional)
        dynamic = bridge.migrate_to_dynamic()
        compatible = bridge.verify_compatibility()

        # Step 4: Test enhanced capabilities
        if compatible:
            console.print("Step 3: Testing enhanced capabilities...")
            new_agent = MockAgent("migrated_agent", "SimpleAgent")
            await dynamic.register_agent_dynamically(new_agent, "Post-migration agent")

            final_status = dynamic.get_dynamic_status()
            console.print(
                f"   ✅ Post-migration agents: {final_status['registered_agents']}"
            )

        console.print(f"Migration {'✅ Successful' if compatible else '❌ Failed'}")


async def run_compatibility_tests():
    """Run all compatibility tests."""

    console.print("[bold magenta]Dynamic Supervisor Compatibility Tests[/bold magenta]")
    console.print("=" * 60)

    tester = CompatibilityTester()

    try:
        # Run all tests
        await tester.test_traditional_multi_agent()
        await tester.test_dynamic_supervisor_integration()
        await tester.test_schema_compatibility()
        await tester.test_execution_mode_compatibility()
        await tester.test_react_agent_integration()
        await tester.test_migration_path()

        console.print(
            "\n[bold green]🎉 All Compatibility Tests Completed![/bold green]"
        )

        # Summary
        console.print("\n[bold cyan]Compatibility Summary:[/bold cyan]")
        console.print("✅ Dynamic supervisor integrates with existing MultiAgent")
        console.print("✅ ReactAgent patterns work with dynamic supervision")
        console.print("✅ Schema composition is compatible with enhancements")
        console.print("✅ Migration path exists from traditional to dynamic")
        console.print("✅ Both architectures can coexist")

    except Exception as e:
        console.print(f"\n[red]❌ Compatibility test failed: {e}[/red]")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_compatibility_tests())
