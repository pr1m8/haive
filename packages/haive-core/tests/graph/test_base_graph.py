"""
Test suite for BaseGraph and SerializableGraph.

Provides comprehensive tests for all major functionality without using mocks.
"""

import json
import unittest

import pytest

from haive.core.graph.branches import Branch, BranchMode, ComparisonType
from haive.core.graph.branches.dynamic import DynamicMapping
from haive.core.graph.state_graph.base_graph import (
    END_NODE,
    START_NODE,
    BaseGraph,
    Node,
    NodeType,
)
from haive.core.graph.state_graph.serializable import SerializableGraph


# State fixture for condition testing
@pytest.fixture
def state():
    """Provide a simple test state for condition testing."""
    return {"flag": True, "counter": 0, "messages": []}


# Define node functions at module level for proper serialization
def node1_func(state):
    """Test node function 1."""
    return state


def node2_func(state):
    """Test node function 2."""
    return state


def node3_func(state):
    """Test node function 3."""
    return state


# To this:
def condition_func(state):
    """Condition function used as utility."""
    return state.get("flag", False)


# Add a separate test function specifically for pytest
def test_condition_pytest(state):
    """Test the condition function as a pytest test."""
    # Use assert instead of return
    assert state.get("flag", False), "Flag should be True"


def dynamic_branch_func(state):
    """Test dynamic branch function."""
    return state.get("route_type", "default")


class TestBaseGraph(unittest.TestCase):
    """Test cases for BaseGraph implementation."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test graph
        self.graph = BaseGraph(
            name="test_graph", description="Test graph for unit tests"
        )

        # Add test nodes with defined functions
        self.graph.add_node("node1", node1_func, node_type=NodeType.CALLABLE)
        self.graph.add_node("node2", node2_func, node_type=NodeType.CALLABLE)
        self.graph.add_node("node3", node3_func, node_type=NodeType.CALLABLE)

        # Add test edges
        self.graph.add_edge(START_NODE, "node1")
        self.graph.add_edge("node1", "node2")
        self.graph.add_edge("node2", "node3")
        self.graph.add_edge("node3", END_NODE)

    def test_node_management(self):
        """Test node management methods."""

        # Test add_node with a properly defined function
        def test_node_func(state):
            return state

        self.graph.add_node("test_node", test_node_func)
        self.assertIn("test_node", self.graph.nodes)

        # Test update_node
        self.graph.update_node("test_node", description="Updated description")
        self.assertEqual(
            self.graph.nodes["test_node"].description, "Updated description"
        )

        # Test get_node
        node = self.graph.get_node("test_node")
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "test_node")

        # Test replace_node
        new_node = Node(
            name="new_node",
            node_type=NodeType.CALLABLE,
            metadata={
                "callable": node1_func
            },  # Use predefined function for serialization
        )
        self.graph.replace_node("test_node", new_node)
        self.assertIn("test_node", self.graph.nodes)  # Name stays the same
        self.assertEqual(
            self.graph.nodes["test_node"].id, new_node.id
        )  # But content is from new_node

        # Test remove_node
        self.graph.remove_node("test_node")
        self.assertNotIn("test_node", self.graph.nodes)

    def test_edge_management(self):
        """Test edge management methods."""
        # Test add_edge
        self.graph.add_edge("node1", "node3")
        self.assertIn(("node1", "node3"), self.graph.edges)

        # Test get_edges
        edges = self.graph.get_edges(source="node1")
        self.assertIn(("node1", "node2"), edges)
        self.assertIn(("node1", "node3"), edges)

        # Test remove_edge
        self.graph.remove_edge("node1", "node3")
        self.assertNotIn(("node1", "node3"), self.graph.edges)

        # Test remove all edges from source
        self.graph.remove_edge("node1")
        edges = self.graph.get_edges(source="node1")
        self.assertEqual(len(edges), 0)

    def test_branch_management(self):
        """Test branch management methods."""
        # Create test branch
        branch = Branch(
            name="test_branch",
            source_node="node1",
            key="test_key",
            value=True,
            comparison=ComparisonType.EQUALS,
            destinations={True: "node3", False: "node2"},
        )

        # Test add_branch
        self.graph.add_branch(branch)
        self.assertIn(branch.id, self.graph.branches)

        # Test get_branch
        retrieved_branch = self.graph.get_branch(branch.id)
        self.assertEqual(retrieved_branch.name, "test_branch")

        # Test update_branch
        self.graph.update_branch(branch.id, default="END")
        self.assertEqual(self.graph.branches[branch.id].default, "END")

        # Test add_function_branch with a module-level function for serialization
        self.graph.add_function_branch(
            source_node="node2",
            condition=test_condition_pytest,  # Use predefined function
            routes={True: "node3", False: "END"},
            name="function_branch",
        )

        # Find function branch by name
        function_branch = self.graph.get_branch_by_name("function_branch")
        self.assertIsNotNone(function_branch)
        self.assertEqual(function_branch.mode, BranchMode.FUNCTION)

        # Test remove_branch
        self.graph.remove_branch(branch.id)
        self.assertNotIn(branch.id, self.graph.branches)

    def test_advanced_node_operations(self):
        """Test advanced node operations."""
        # Insert a node after with a module-level function
        self.graph.insert_node_after("node1", "inserted_after", node1_func)
        self.assertIn("inserted_after", self.graph.nodes)
        edges = self.graph.get_edges()
        self.assertIn(("node1", "inserted_after"), edges)
        self.assertIn(("inserted_after", "node2"), edges)
        self.assertNotIn(("node1", "node2"), edges)

        # Insert a node before with a module-level function
        self.graph.insert_node_before("node3", "inserted_before", node2_func)
        self.assertIn("inserted_before", self.graph.nodes)
        edges = self.graph.get_edges()
        self.assertIn(("node2", "inserted_before"), edges)
        self.assertIn(("inserted_before", "node3"), edges)
        self.assertNotIn(("node2", "node3"), edges)

        # Add prelude node with a module-level function
        self.graph.add_prelude_node("prelude", node3_func)
        self.assertIn("prelude", self.graph.nodes)
        edges = self.graph.get_edges()
        self.assertIn((START_NODE, "prelude"), edges)
        self.assertIn(("prelude", "node1"), edges)
        self.assertNotIn((START_NODE, "node1"), edges)

        # Add postlude node with a module-level function
        self.graph.add_postlude_node("postlude", node1_func)
        self.assertIn("postlude", self.graph.nodes)
        edges = self.graph.get_edges()
        self.assertIn(("node3", "postlude"), edges)
        self.assertIn(("postlude", END_NODE), edges)
        self.assertNotIn(("node3", END_NODE), edges)

    def test_analysis_methods(self):
        """Test graph analysis methods."""
        # Test get_node_dependencies
        deps = self.graph.get_node_dependencies("node2")
        self.assertIn("node1", deps["in"])
        self.assertIn("node3", deps["out"])

        # Test has_path
        self.assertTrue(self.graph.has_path("node1", "node3"))
        self.assertTrue(self.graph.has_path(START_NODE, END_NODE))

        # Test get_start_nodes
        start_nodes = self.graph.get_start_nodes()
        self.assertIn("node1", start_nodes)

        # Test get_end_nodes
        end_nodes = self.graph.get_end_nodes()
        self.assertIn("node3", end_nodes)

        # Test validate method
        self.assertTrue(self.graph.validate())

        # Get orphan nodes (should be none)
        orphans = self.graph.get_orphan_nodes()
        self.assertEqual(len(orphans), 0)

        # Create orphan and test detection
        self.graph.add_node("orphan_node", node1_func)
        orphans = self.graph.get_orphan_nodes()
        self.assertIn("orphan_node", orphans)

    def test_sequence_and_parallel(self):
        """Test adding sequences and parallel branches."""
        # Define sequence node dictionaries with module-level functions
        sequence = [
            {
                "name": "seq1",
                "node_type": NodeType.CALLABLE,
                "metadata": {"callable": node1_func},
            },
            {
                "name": "seq2",
                "node_type": NodeType.CALLABLE,
                "metadata": {"callable": node2_func},
            },
            {
                "name": "seq3",
                "node_type": NodeType.CALLABLE,
                "metadata": {"callable": node3_func},
            },
        ]
        self.graph.add_sequence(sequence, connect_start=True, connect_end=True)

        # Verify nodes added
        self.assertIn("seq1", self.graph.nodes)
        self.assertIn("seq2", self.graph.nodes)
        self.assertIn("seq3", self.graph.nodes)

        # Verify connections
        edges = self.graph.get_edges()
        self.assertIn((START_NODE, "seq1"), edges)
        self.assertIn(("seq1", "seq2"), edges)
        self.assertIn(("seq2", "seq3"), edges)
        self.assertIn(("seq3", END_NODE), edges)

        # Test add_parallel_branches
        source = "parallel_source"
        join = "parallel_join"

        # Add source node
        self.graph.add_node(source, node1_func)

        # Define branches with module-level functions
        branches = [
            [
                {
                    "name": "branch1_1",
                    "node_type": NodeType.CALLABLE,
                    "metadata": {"callable": node1_func},
                },
                {
                    "name": "branch1_2",
                    "node_type": NodeType.CALLABLE,
                    "metadata": {"callable": node2_func},
                },
            ],
            [
                {
                    "name": "branch2_1",
                    "node_type": NodeType.CALLABLE,
                    "metadata": {"callable": node3_func},
                },
                {
                    "name": "branch2_2",
                    "node_type": NodeType.CALLABLE,
                    "metadata": {"callable": node1_func},
                },
            ],
        ]

        self.graph.add_parallel_branches(
            source,
            branches,
            join_node={
                "name": join,
                "node_type": NodeType.CALLABLE,
                "metadata": {"callable": node2_func},
            },
        )

        # Verify all nodes added
        self.assertIn("branch1_1", self.graph.nodes)
        self.assertIn("branch1_2", self.graph.nodes)
        self.assertIn("branch2_1", self.graph.nodes)
        self.assertIn("branch2_2", self.graph.nodes)
        self.assertIn(join, self.graph.nodes)

    def test_to_from_dict(self):
        """Test serialization to/from dictionary."""
        # Create a graph with module-level functions
        graph = BaseGraph(name="dict_test_graph", description="Test dict serialization")

        # Add nodes with predefined functions
        graph.add_node("node1", node1_func)
        graph.add_node("node2", node2_func)

        # Add edges
        graph.add_edge(START_NODE, "node1")
        graph.add_edge("node1", "node2")
        graph.add_edge("node2", END_NODE)

        # Convert to dictionary
        graph_dict = graph.to_dict()

        # Verify dictionary has expected structure
        self.assertEqual(graph_dict["name"], "dict_test_graph")
        self.assertEqual(graph_dict["description"], "Test dict serialization")
        self.assertIn("nodes", graph_dict)
        self.assertIn("direct_edges", graph_dict)

        # Reconstruct from dictionary
        reconstructed = BaseGraph.from_dict(graph_dict)

        # Verify reconstructed graph
        self.assertEqual(reconstructed.name, graph.name)
        self.assertEqual(reconstructed.description, graph.description)
        self.assertEqual(len(reconstructed.nodes), len(graph.nodes))
        self.assertEqual(len(reconstructed.edges), len(graph.edges))

    def test_to_from_json(self):
        """Test serialization to/from JSON string."""
        # Create a test graph with predefined functions only
        graph = BaseGraph(name="json_test_graph", description="Test JSON serialization")

        # Add nodes with predefined functions
        graph.add_node("node1", node1_func)
        graph.add_node("node2", node2_func)

        # Add edges
        graph.add_edge(START_NODE, "node1")
        graph.add_edge("node1", "node2")
        graph.add_edge("node2", END_NODE)

        try:
            # Convert to JSON - may raise an exception if serialization is not properly handled
            json_str = graph.to_json()

            # Verify valid JSON
            json_obj = json.loads(json_str)
            self.assertEqual(json_obj["name"], "json_test_graph")

            # Reconstruct from JSON
            reconstructed = BaseGraph.from_json(json_str)

            # Verify reconstructed graph
            self.assertEqual(reconstructed.name, graph.name)
            self.assertEqual(len(reconstructed.nodes), len(graph.nodes))
        except (TypeError, ValueError) as e:
            self.fail(f"Serialization failed: {str(e)}")

    def test_to_mermaid(self):
        """Test Mermaid diagram generation."""
        mermaid = self.graph.to_mermaid()

        # Check if it contains basic elements
        self.assertIn("graph TD;", mermaid)
        self.assertIn("node1", mermaid)
        self.assertIn("node2", mermaid)
        self.assertIn("node3", mermaid)
        self.assertIn(f"{START_NODE}", mermaid)
        self.assertIn(f"{END_NODE}", mermaid)

        # Check if edges are represented
        self.assertIn(f"{START_NODE} --> node1", mermaid)
        self.assertIn("node1 --> node2", mermaid)
        self.assertIn("node2 --> node3", mermaid)
        self.assertIn(f"node3 --> {END_NODE}", mermaid)

    def test_from_langgraph(self):
        """Test conversion from LangGraph StateGraph."""
        try:
            # Try importing StateGraph
            from langgraph.graph import END, START, StateGraph

            # Create a simple StateGraph
            sg = StateGraph(dict)  # Use positional argument, not keyword

            # Define a node function
            def test_node_func(state):
                return state

            # Add node and edges
            sg.add_node("test_node", test_node_func)
            sg.add_edge(START, "test_node")
            sg.add_edge("test_node", END)

            # Convert to BaseGraph
            result = BaseGraph.from_langgraph(sg, name="converted_graph")

            # Verify conversion
            self.assertEqual(result.name, "converted_graph")
            self.assertIn("test_node", result.nodes)
            self.assertIn((START_NODE, "test_node"), result.get_edges())
            self.assertIn(("test_node", END_NODE), result.get_edges())

        except ImportError:
            self.skipTest("langgraph not installed")

    def test_to_langgraph(self):
        """Test conversion to LangGraph StateGraph."""
        try:
            # Try importing StateGraph
            from langgraph.graph import END, START, StateGraph

            # Convert to StateGraph
            result = self.graph.to_langgraph()

            # Verify basic structure
            self.assertIsInstance(result, StateGraph)
            self.assertIn("node1", result.nodes)
            self.assertIn("node2", result.nodes)
            self.assertIn("node3", result.nodes)

            # Check edges
            self.assertIn((START, "node1"), result.edges)
            self.assertIn(("node1", "node2"), result.edges)
            self.assertIn(("node2", "node3"), result.edges)
            self.assertIn(("node3", END), result.edges)

        except ImportError:
            self.skipTest("langgraph not installed")


class TestSerializableGraph(unittest.TestCase):
    """Test cases for SerializableGraph implementation."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test BaseGraph
        self.base_graph = BaseGraph(
            name="test_serializable", description="Test graph for serialization"
        )

        # Add test nodes with properly defined functions
        self.base_graph.add_node("node1", node1_func, node_type=NodeType.CALLABLE)
        self.base_graph.add_node("node2", node2_func, node_type=NodeType.CALLABLE)

        # Add test edges
        self.base_graph.add_edge(START_NODE, "node1")
        self.base_graph.add_edge("node1", "node2")
        self.base_graph.add_edge("node2", END_NODE)

        # Add a test branch with properly defined function
        self.base_graph.add_function_branch(
            source_node="node1",
            condition=test_condition_pytest,  # Use predefined function
            routes={True: "node2", False: "END"},
            name="test_branch",
        )

        # Create serializable from BaseGraph
        self.serializable = SerializableGraph.from_graph(self.base_graph)

    def test_from_graph(self):
        """Test conversion from BaseGraph to SerializableGraph."""
        # Verify basic properties
        self.assertEqual(self.serializable.name, self.base_graph.name)
        self.assertEqual(self.serializable.description, self.base_graph.description)

        # Verify nodes were converted
        self.assertEqual(len(self.serializable.nodes), len(self.base_graph.nodes))
        for name, node in self.base_graph.nodes.items():
            self.assertIn(name, self.serializable.nodes)
            ser_node = self.serializable.nodes[name]
            self.assertEqual(ser_node.name, node.name)
            self.assertEqual(ser_node.node_type, node.node_type.value)

        # Verify edges were converted
        self.assertEqual(
            len(self.serializable.direct_edges), len(self.base_graph.edges)
        )
        for edge in self.base_graph.edges:
            self.assertIn(edge, self.serializable.direct_edges)

        # Verify branches were converted
        self.assertEqual(len(self.serializable.branches), len(self.base_graph.branches))
        for branch_id in self.base_graph.branches:
            self.assertIn(branch_id, self.serializable.branches)

    def test_function_references(self):
        """Test serialization and deserialization of function references."""
        # Create a graph with function references
        graph = BaseGraph(name="function_test")

        # Add nodes with properly defined function
        graph.add_node("node1", node1_func)

        # Add a branch with the module-level function
        graph.add_function_branch(
            source_node="node1",
            condition=condition_func,
            routes={True: "END", False: "END"},
            name="func_branch",
        )

        # Serialize and deserialize
        serialized = SerializableGraph.from_graph(graph)
        deserialized = serialized.to_graph()

        # Check branch
        branch = deserialized.get_branch_by_name("func_branch")
        self.assertIsNotNone(branch)

        # Since we can't compare function objects directly, check function_ref
        self.assertIsNotNone(branch.function_ref)

        # Check if the function reference contains our function's name
        self.assertEqual(branch.function_ref.name, "condition_func")

        # Check module path matches this test module
        self.assertEqual(branch.function_ref.module_path, __name__)

    def test_complex_branch_serialization(self):
        """Test serialization of complex branches."""
        # Create a graph with complex branch types
        graph = BaseGraph(name="complex_branch_test")

        # Add nodes with properly defined functions
        graph.add_node("start_node", node1_func)
        graph.add_node("target1", node2_func)
        graph.add_node("target2", node3_func)
        # Add a "continue" node to satisfy the destination requirement
        graph.add_node("continue", node1_func)

        # Add direct edge
        graph.add_edge(START_NODE, "start_node")

        # Add dynamic mapping branch
        mapping = DynamicMapping(
            key="route_type",
            mappings={
                "type1": {"target": "target1", "mapping": '{"input": "value"}'},
                "type2": {"target": "target2", "mapping": '{"input": "value"}'},
            },
        )

        dynamic_branch = Branch(
            name="dynamic_branch",
            source_node="start_node",
            mode=BranchMode.DYNAMIC,
            dynamic_mapping=mapping,
            # Use default destinations which reference the "continue" node we've now added
            destinations={True: "continue", False: "END"},
            default="END",
        )

        graph.add_branch(dynamic_branch)

        # Create chain of branches
        branch1 = Branch(
            name="chain_branch1",
            source_node="start_node",
            key="field1",
            value=True,
            comparison=ComparisonType.EQUALS,
            destinations={True: "target1", False: "target2"},
        )

        branch2 = Branch(
            name="chain_branch2",
            source_node="start_node",
            key="field2",
            value=True,
            comparison=ComparisonType.EQUALS,
            destinations={True: "target1", False: "target2"},
        )

        # Create a chain branch
        chain_branch = Branch(
            name="master_chain",
            source_node="start_node",
            mode=BranchMode.CHAIN,
            chain_branches=[branch1, branch2],
            default="END",
        )

        graph.add_branch(branch1)
        graph.add_branch(branch2)
        graph.add_branch(chain_branch)

        # Serialize and deserialize
        serializable = SerializableGraph.from_graph(graph)
        deserialized = serializable.to_graph()

        # Check dynamic branch
        dyn_branch = deserialized.get_branch_by_name("dynamic_branch")
        self.assertIsNotNone(dyn_branch)
        self.assertEqual(dyn_branch.mode, BranchMode.DYNAMIC)
        self.assertIsNotNone(dyn_branch.dynamic_mapping)
        self.assertEqual(dyn_branch.dynamic_mapping.key, "route_type")
        self.assertGreaterEqual(len(dyn_branch.dynamic_mapping.mappings), 2)

        # Check chain branch
        chain = deserialized.get_branch_by_name("master_chain")
        self.assertIsNotNone(chain)
        self.assertEqual(chain.mode, BranchMode.CHAIN)

    def test_to_dict_from_dict(self):
        """Test to_dict and from_dict methods."""
        # Convert to dictionary
        dict_data = self.serializable.to_dict()

        # Verify dictionary structure
        self.assertEqual(dict_data["name"], "test_serializable")
        self.assertIn("nodes", dict_data)
        self.assertIn("direct_edges", dict_data)
        self.assertIn("branches", dict_data)

        # Reconstruct from dictionary
        reconstructed = SerializableGraph.from_dict(dict_data)

        # Verify reconstructed serializable
        self.assertEqual(reconstructed.name, self.serializable.name)
        self.assertEqual(len(reconstructed.nodes), len(self.serializable.nodes))
        self.assertEqual(
            len(reconstructed.direct_edges), len(self.serializable.direct_edges)
        )
        self.assertEqual(len(reconstructed.branches), len(self.serializable.branches))

    def test_to_json_from_json(self):
        """Test to_json and from_json methods."""
        # Create a new clean serializable graph with module-level functions
        clean_graph = BaseGraph(
            name="json_graph", description="Test JSON serialization"
        )

        # Add nodes with top-level functions, not lambdas
        clean_graph.add_node("node1", node1_func)
        clean_graph.add_node("node2", node2_func)

        # Add a simple edge
        clean_graph.add_edge(START_NODE, "node1")
        clean_graph.add_edge("node1", "node2")
        clean_graph.add_edge("node2", END_NODE)

        # Add a branch with a top-level function
        clean_graph.add_function_branch(
            source_node="node1",
            condition=condition_func,
            routes={True: "node2", False: "END"},
            name="json_branch",
        )

        try:
            # Generate clean serializable version
            clean_serializable = SerializableGraph.from_graph(clean_graph)

            # Convert to JSON
            json_str = clean_serializable.to_json()

            # Verify valid JSON
            json_obj = json.loads(json_str)
            self.assertEqual(json_obj["name"], "json_graph")

            # Reconstruct from JSON
            reconstructed = SerializableGraph.from_json(json_str)

            # Verify reconstructed serializable
            self.assertEqual(reconstructed.name, clean_serializable.name)
            self.assertEqual(len(reconstructed.nodes), len(clean_serializable.nodes))
            self.assertEqual(
                len(reconstructed.direct_edges), len(clean_serializable.direct_edges)
            )

            # Verify specific branch data
            self.assertIn(
                "json_branch", [b.name for b in reconstructed.branches.values()]
            )
        except (TypeError, ValueError) as e:
            self.fail(f"JSON serialization failed: {str(e)}")

    def test_round_trip_serialization(self):
        """Test complete round-trip serialization."""
        # Create a graph with proper module-level functions
        original = BaseGraph(
            name="round_trip", description="Test round-trip serialization"
        )

        # Add nodes with top-level functions
        original.add_node("node1", node1_func)
        original.add_node("node2", node2_func)

        # Add edges
        original.add_edge(START_NODE, "node1")
        original.add_edge("node1", "node2")
        original.add_edge("node2", END_NODE)

        # Add a branch with a top-level function
        original.add_function_branch(
            source_node="node1",
            condition=condition_func,
            routes={True: "node2", False: "END"},
            name="roundtrip_branch",
        )

        try:
            # Convert to SerializableGraph
            serializable = SerializableGraph.from_graph(original)

            # Convert to JSON
            json_str = serializable.to_json()

            # Convert back from JSON to SerializableGraph
            deserialized_serializable = SerializableGraph.from_json(json_str)

            # Convert back to BaseGraph
            final = deserialized_serializable.to_graph()

            # Verify round-trip
            self.assertEqual(final.name, original.name)
            self.assertEqual(final.description, original.description)
            self.assertEqual(len(final.nodes), len(original.nodes))
            self.assertEqual(len(final.edges), len(original.edges))
            self.assertEqual(len(final.branches), len(original.branches))

            # Check node names
            for name in original.nodes:
                self.assertIn(name, final.nodes)

            # Check edges
            for edge in original.edges:
                self.assertIn(edge, final.edges)

            # Check branch
            self.assertIn("roundtrip_branch", [b.name for b in final.branches.values()])
        except (TypeError, ValueError) as e:
            self.fail(f"Round-trip serialization failed: {str(e)}")


if __name__ == "__main__":
    unittest.main()
