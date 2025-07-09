"""
Test file for the new MultiAgentBase with no mocks - using real agents.

This test file demonstrates the new MultiAgentBase functionality with:
- Sequential multi-agent flows
- Conditional routing with branches
- Entry/finish points
- Workflow nodes
- State schema composition
- Plan and Execute patterns
"""

from typing import Any, Dict, List

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

from haive.agents.multi.enhanced_base import (
    MultiAgentBase,
    create_branching_multi_agent,
    create_plan_execute_multi_agent,
    create_sequential_multi_agent,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


@pytest.fixture
def simple_agent_1():
    """Create a simple agent for testing."""
    config = AugLLMConfig(
        name="agent1",
        system_message="You are Agent 1. Respond with 'Agent 1 processed: [input]'",
        temperature=0.1,
    )
    return SimpleAgent(name="Agent1", engine=config)


@pytest.fixture
def simple_agent_2():
    """Create another simple agent for testing."""
    config = AugLLMConfig(
        name="agent2",
        system_message="You are Agent 2. Respond with 'Agent 2 analyzed: [input]'",
        temperature=0.1,
    )
    return SimpleAgent(name="Agent2", engine=config)


@pytest.fixture
def simple_agent_3():
    """Create a third simple agent for testing."""
    config = AugLLMConfig(
        name="agent3",
        system_message="You are Agent 3. Respond with 'Agent 3 completed: [input]'",
        temperature=0.1,
    )
    return SimpleAgent(name="Agent3", engine=config)


class TestMultiAgentBaseBasic:
    """Test basic MultiAgentBase functionality."""

    def test_creation_with_agents_only(self, simple_agent_1, simple_agent_2):
        """Test creating MultiAgentBase with just agents (sequential default)."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        assert len(system.agents) == 2
        assert system.agents[0].name == "Agent1"
        assert system.agents[1].name == "Agent2"
        assert len(system.entry_points) == 1
        assert len(system.finish_points) == 1
        assert system.conditional_edges == []
        assert system.state_schema is not None

    def test_agent_node_mapping(self, simple_agent_1, simple_agent_2):
        """Test that agent node names are properly mapped."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        # Test node name mapping
        node1 = system._get_agent_node_name(simple_agent_1)
        node2 = system._get_agent_node_name(simple_agent_2)

        assert node1 == "Agent1"
        assert node2 == "Agent2"
        assert node1 in system.agent_node_mapping.values()
        assert node2 in system.agent_node_mapping.values()

    def test_state_schema_composition(self, simple_agent_1, simple_agent_2):
        """Test that state schema is properly composed from agents."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        assert system.state_schema is not None
        assert hasattr(system.state_schema, "model_fields")
        assert "messages" in system.state_schema.model_fields

    def test_build_graph_sequential(self, simple_agent_1, simple_agent_2):
        """Test building a sequential graph."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])
        graph = system.build_graph()

        assert graph is not None
        assert len(graph.nodes) == 2
        assert "Agent1" in graph.nodes
        assert "Agent2" in graph.nodes


class TestMultiAgentBaseBranches:
    """Test MultiAgentBase with conditional branches."""

    def test_creation_with_branches(
        self, simple_agent_1, simple_agent_2, simple_agent_3
    ):
        """Test creating MultiAgentBase with conditional branches."""

        def route_condition(state) -> str:
            """Simple routing condition."""
            if hasattr(state, "messages") and state.messages:
                last_msg = state.messages[-1]
                if "continue" in str(last_msg.content).lower():
                    return "continue"
                else:
                    return "finish"
            return "finish"

        branches = [
            (
                simple_agent_1,
                route_condition,
                {"continue": simple_agent_2, "finish": simple_agent_3},
            )
        ]

        system = MultiAgentBase(
            agents=[simple_agent_1, simple_agent_2, simple_agent_3], branches=branches
        )

        assert len(system.conditional_edges) == 1
        assert system.conditional_edges[0]["source_agent"] == simple_agent_1
        assert system.conditional_edges[0]["condition"] == route_condition

    def test_add_conditional_edges_method(self, simple_agent_1, simple_agent_2):
        """Test the add_conditional_edges method."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        def simple_condition(state) -> bool:
            return True

        system.add_conditional_edges(
            source_agent=simple_agent_1,
            condition=simple_condition,
            destinations={True: simple_agent_2, False: END},
        )

        assert len(system.conditional_edges) == 1
        edge_config = system.conditional_edges[0]
        assert edge_config["source_agent"] == simple_agent_1
        assert edge_config["condition"] == simple_condition

    def test_add_edge_method(self, simple_agent_1, simple_agent_2):
        """Test the add_edge method for simple edges."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        system.add_edge(simple_agent_1, simple_agent_2)

        assert len(system.conditional_edges) == 1
        edge_config = system.conditional_edges[0]
        assert edge_config["source_agent"] == simple_agent_1
        assert edge_config["destinations"] == simple_agent_2
        assert edge_config["condition"] is None


class TestMultiAgentBaseAdvanced:
    """Test advanced MultiAgentBase features."""

    def test_custom_entry_exit_points(
        self, simple_agent_1, simple_agent_2, simple_agent_3
    ):
        """Test custom entry and finish points."""
        system = MultiAgentBase(
            agents=[simple_agent_1, simple_agent_2, simple_agent_3],
            entry_points=[simple_agent_1, simple_agent_2],
            finish_points=[simple_agent_3],
        )

        assert len(system.entry_points) == 2
        assert len(system.finish_points) == 1
        assert simple_agent_1 in system.entry_points
        assert simple_agent_2 in system.entry_points
        assert simple_agent_3 in system.finish_points

    def test_workflow_nodes(self, simple_agent_1, simple_agent_2):
        """Test custom workflow nodes."""

        def preprocess_step(state):
            """Custom preprocessing step."""
            return {"processed": True}

        def validation_step(state):
            """Custom validation step."""
            return {"validated": True}

        workflow_nodes = {"preprocess": preprocess_step, "validate": validation_step}

        system = MultiAgentBase(
            agents=[simple_agent_1, simple_agent_2], workflow_nodes=workflow_nodes
        )

        assert len(system.workflow_nodes) == 2
        assert "preprocess" in system.workflow_nodes
        assert "validate" in system.workflow_nodes
        assert system.workflow_nodes["preprocess"] == preprocess_step

    def test_create_missing_nodes_parameter(self, simple_agent_1):
        """Test create_missing_nodes parameter (matches base_graph2)."""
        system = MultiAgentBase(agents=[simple_agent_1], create_missing_nodes=True)

        assert system.create_missing_nodes == True

        system2 = MultiAgentBase(
            agents=[simple_agent_1], create_missing_nodes=False  # Default
        )

        assert system2.create_missing_nodes == False

    def test_custom_state_schema(self, simple_agent_1, simple_agent_2):
        """Test using custom state schema."""
        system = MultiAgentBase(
            agents=[simple_agent_1, simple_agent_2], state_schema=PlanExecuteState
        )

        assert system.state_schema == PlanExecuteState
        assert system.state_schema_override == PlanExecuteState


class TestConvenienceFunctions:
    """Test convenience functions for creating common patterns."""

    def test_create_sequential_multi_agent(
        self, simple_agent_1, simple_agent_2, simple_agent_3
    ):
        """Test creating sequential multi-agent system."""
        system = create_sequential_multi_agent(
            agents=[simple_agent_1, simple_agent_2, simple_agent_3],
            name="Sequential Test",
        )

        assert system.name == "Sequential Test"
        assert len(system.agents) == 3
        assert system.schema_build_mode == BuildMode.SEQUENCE
        assert system.conditional_edges == []  # No branches for sequential

    def test_create_branching_multi_agent(self, simple_agent_1, simple_agent_2):
        """Test creating branching multi-agent system."""

        def test_condition(state) -> str:
            return "next"

        branches = [(simple_agent_1, test_condition, {"next": simple_agent_2})]

        system = create_branching_multi_agent(
            agents=[simple_agent_1, simple_agent_2],
            branches=branches,
            name="Branching Test",
        )

        assert system.name == "Branching Test"
        assert len(system.conditional_edges) == 1

    def test_create_plan_execute_multi_agent(
        self, simple_agent_1, simple_agent_2, simple_agent_3
    ):
        """Test creating Plan and Execute multi-agent system."""
        system = create_plan_execute_multi_agent(
            planner_agent=simple_agent_1,
            executor_agent=simple_agent_2,
            replanner_agent=simple_agent_3,
            name="Plan Execute Test",
        )

        assert system.name == "Plan Execute Test"
        assert len(system.agents) == 3
        assert len(system.conditional_edges) == 2  # Two routing conditions

        # Check that routing functions are properly set
        assert system.conditional_edges[0]["source_agent"] == simple_agent_2  # executor
        assert (
            system.conditional_edges[1]["source_agent"] == simple_agent_3
        )  # replanner


class TestMultiAgentBaseExecution:
    """Test actual execution of MultiAgentBase systems."""

    def test_sequential_execution(self, simple_agent_1, simple_agent_2):
        """Test executing a sequential multi-agent system."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])
        graph = system.build_graph()

        # Test that graph builds successfully
        assert graph is not None
        assert len(graph.nodes) == 2

        # Test initial state creation
        input_data = {"messages": [HumanMessage(content="Test input")]}
        prepared_input = system._prepare_input(input_data)

        assert prepared_input is not None
        assert hasattr(prepared_input, "messages") or "messages" in prepared_input

    def test_state_schema_fields(self, simple_agent_1, simple_agent_2):
        """Test that state schema has expected fields."""
        system = MultiAgentBase(agents=[simple_agent_1, simple_agent_2])

        # Check state schema fields
        state_fields = system.state_schema.model_fields
        assert "messages" in state_fields

        # Check that engines are included if agents have them
        if hasattr(simple_agent_1, "engines") and simple_agent_1.engines:
            assert "engines" in state_fields or "engine" in state_fields


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_agents_list(self):
        """Test that empty agents list raises error."""
        with pytest.raises(
            ValueError, match="MultiAgentBase requires at least one agent"
        ):
            MultiAgentBase(agents=[])

    def test_invalid_branch_format(self, simple_agent_1):
        """Test invalid branch format handling."""
        # Branch with wrong number of elements should be handled gracefully
        invalid_branches = [(simple_agent_1,)]  # Missing condition and destinations

        system = MultiAgentBase(agents=[simple_agent_1], branches=invalid_branches)

        # Should not crash, but might not add the invalid branch
        assert len(system.conditional_edges) == 0  # Invalid branch not added

    def test_normalization_methods(self, simple_agent_1):
        """Test agent and destination normalization methods."""
        system = MultiAgentBase(agents=[simple_agent_1])

        # Test string normalization
        assert system._get_agent_node_name("Agent1") == "Agent1"
        assert system._get_agent_node_name("START") == "START"
        assert system._get_agent_node_name("END") == "END"

        # Test agent object normalization
        node_name = system._get_agent_node_name(simple_agent_1)
        assert node_name == "Agent1"

        # Test destination normalization
        assert system._normalize_destination("END") == END
        assert system._normalize_destination(END) == END


if __name__ == "__main__":
    """Run tests if executed directly."""
    pytest.main([__file__, "-v", "--tb=short"])
