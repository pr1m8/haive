"""Tests for the graph pattern registry.

This module tests the GraphPatternRegistry class, which manages patterns and branches
for the framework.
"""

import os
import tempfile

from haive.core.graph.patterns.base import (
    BranchDefinition,
    GraphPattern,
    ParameterDefinition,
    PatternMetadata,
)
from haive.core.graph.patterns.registry import (
    GraphPatternRegistry,
    register_branch,
    register_pattern,
)


class TestGraphPatternRegistry:
    """Tests for the GraphPatternRegistry class."""

    def setup_method(self):
        """Set up test environment."""
        # Clear the registry before each test
        registry = GraphPatternRegistry.get_instance()
        registry.clear()

    def test_singleton_instance(self):
        """Test that the registry is a singleton."""
        registry1 = GraphPatternRegistry.get_instance()
        registry2 = GraphPatternRegistry.get_instance()

        assert registry1 is registry2

    def test_register_pattern_with_object(self):
        """Test registering a pattern with a GraphPattern object."""
        registry = GraphPatternRegistry.get_instance()

        # Create pattern
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        pattern = GraphPattern(metadata=metadata)

        # Register pattern
        registered = registry.register_pattern(pattern)

        # Check registration
        assert registered is pattern
        assert registry.get_pattern("test_pattern") is pattern
        assert "test_pattern" in registry.list_patterns()
        assert "test" in registry.list_pattern_types()
        assert "test_pattern" in registry.pattern_categories["test"]

    def test_register_pattern_with_dict(self):
        """Test registering a pattern with a dictionary."""
        registry = GraphPatternRegistry.get_instance()

        # Create pattern dict
        pattern_dict = {
            "metadata": {
                "name": "dict_pattern",
                "description": "A pattern from dict",
                "pattern_type": "dict_type",
            }
        }

        # Register pattern
        registered = registry.register_pattern(pattern_dict)

        # Check registration
        assert isinstance(registered, GraphPattern)
        assert registry.get_pattern("dict_pattern") is registered
        assert "dict_pattern" in registry.list_patterns()
        assert "dict_type" in registry.list_pattern_types()
        assert "dict_pattern" in registry.pattern_categories["dict_type"]

    def test_register_pattern_with_function(self):
        """Test registering a pattern with a function."""
        registry = GraphPatternRegistry.get_instance()

        # Create a function
        def test_function(graph, param1="default"):
            """Test function docstring."""
            return graph

        # Register pattern
        registered = registry.register_pattern(
            test_function,
            name="func_pattern",
            pattern_type="func_type",
            description="Function pattern",
        )

        # Check registration
        assert isinstance(registered, GraphPattern)
        assert registry.get_pattern("func_pattern") is registered
        assert registered.apply_func is test_function
        assert "func_pattern" in registry.list_patterns()
        assert "func_type" in registry.list_pattern_types()

        # Check parameter extraction
        assert "param1" in registered.metadata.parameters
        param_def = registered.metadata.parameters["param1"]
        assert param_def.default == "default"

    def test_register_branch_with_object(self):
        """Test registering a branch with a BranchDefinition object."""
        registry = GraphPatternRegistry.get_instance()

        # Create branch
        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
        )

        # Register branch
        registered = registry.register_branch(branch)

        # Check registration
        assert registered is branch
        assert registry.get_branch("test_branch") is branch
        assert "test_branch" in registry.list_branches()
        assert "test" in registry.list_branch_types()
        assert "test_branch" in registry.branch_categories["test"]

    def test_register_branch_with_dict(self):
        """Test registering a branch with a dictionary."""
        registry = GraphPatternRegistry.get_instance()

        # Create branch dict
        branch_dict = {
            "name": "dict_branch",
            "description": "A branch from dict",
            "condition_type": "dict_type",
            "routes": {"condition1": "node1"},
        }

        # Register branch
        registered = registry.register_branch(branch_dict)

        # Check registration
        assert isinstance(registered, BranchDefinition)
        assert registry.get_branch("dict_branch") is registered
        assert "dict_branch" in registry.list_branches()
        assert "dict_type" in registry.list_branch_types()
        assert "dict_branch" in registry.branch_categories["dict_type"]

    def test_register_branch_with_function(self):
        """Test registering a branch with a function."""
        registry = GraphPatternRegistry.get_instance()

        # Create a function
        def test_function(state, param1="default"):
            """Test function docstring."""
            return "result"

        # Register branch
        registered = registry.register_branch(
            test_function,
            name="func_branch",
            condition_type="func_type",
            description="Function branch",
            routes={"result": "target_node"},
        )

        # Check registration
        assert isinstance(registered, BranchDefinition)
        assert registry.get_branch("func_branch") is registered
        assert registered.condition_func is test_function
        assert "func_branch" in registry.list_branches()
        assert "func_type" in registry.list_branch_types()

        # Check parameter extraction
        assert "param1" in registered.parameters
        param_def = registered.parameters["param1"]
        assert param_def.default == "default"

    def test_find_patterns(self):
        """Test finding patterns with filtering."""
        registry = GraphPatternRegistry.get_instance()

        # Create patterns
        pattern1 = GraphPattern(
            metadata=PatternMetadata(
                name="pattern1",
                description="First pattern",
                pattern_type="type1",
                tags=["tag1", "tag2"],
            )
        )

        pattern2 = GraphPattern(
            metadata=PatternMetadata(
                name="pattern2",
                description="Second pattern",
                pattern_type="type2",
                tags=["tag2", "tag3"],
            )
        )

        # Register patterns
        registry.register_pattern(pattern1)
        registry.register_pattern(pattern2)

        # Find by type
        results = registry.find_patterns(pattern_type="type1")
        assert len(results) == 1
        assert results[0] is pattern1

        # Find by tag
        results = registry.find_patterns(tags=["tag2"])
        assert len(results) == 2

        # Find by multiple tags
        results = registry.find_patterns(tags=["tag1", "tag2"])
        assert len(results) == 1
        assert results[0] is pattern1

        # Find by search term
        results = registry.find_patterns(search_term="Second")
        assert len(results) == 1
        assert results[0] is pattern2

    def test_find_branches(self):
        """Test finding branches with filtering."""
        registry = GraphPatternRegistry.get_instance()

        # Create branches
        branch1 = BranchDefinition(
            name="branch1",
            description="First branch",
            condition_type="type1",
            routes={"condition1": "node1"},
            tags=["tag1", "tag2"],
        )

        branch2 = BranchDefinition(
            name="branch2",
            description="Second branch",
            condition_type="type2",
            routes={"condition2": "node2"},
            tags=["tag2", "tag3"],
        )

        # Register branches
        registry.register_branch(branch1)
        registry.register_branch(branch2)

        # Find by type
        results = registry.find_branches(condition_type="type1")
        assert len(results) == 1
        assert results[0] is branch1

        # Find by tag
        results = registry.find_branches(tags=["tag2"])
        assert len(results) == 2

        # Find by multiple tags
        results = registry.find_branches(tags=["tag1", "tag2"])
        assert len(results) == 1
        assert results[0] is branch1

        # Find by search term
        results = registry.find_branches(search_term="Second")
        assert len(results) == 1
        assert results[0] is branch2

    def test_get_pattern_documentation(self):
        """Test getting structured documentation for a pattern."""
        registry = GraphPatternRegistry.get_instance()

        # Create a parameter definition
        param_def = ParameterDefinition(
            type="str", description="A parameter", default="default"
        )

        # Create a requirement
        requirement = {"type": "llm", "count": 1, "optional": False}

        # Create pattern
        pattern = GraphPattern(
            metadata=PatternMetadata(
                name="doc_pattern",
                description="Pattern with documentation",
                pattern_type="doc_type",
                parameters={"param1": param_def},
                required_components=[requirement],
                examples=[{"example": "value"}],
            )
        )

        # Register pattern
        registry.register_pattern(pattern)

        # Get documentation
        doc = registry.get_pattern_documentation("doc_pattern")

        # Check documentation
        assert doc["name"] == "doc_pattern"
        assert doc["description"] == "Pattern with documentation"
        assert doc["type"] == "doc_type"
        assert len(doc["required_components"]) == 1
        assert doc["required_components"][0]["type"] == "llm"
        assert "param1" in doc["parameters"]
        assert len(doc["examples"]) == 1

    def test_get_branch_documentation(self):
        """Test getting structured documentation for a branch."""
        registry = GraphPatternRegistry.get_instance()

        # Create a parameter definition
        param_def = ParameterDefinition(
            type="str", description="A parameter", default="default"
        )

        # Create branch
        branch = BranchDefinition(
            name="doc_branch",
            description="Branch with documentation",
            condition_type="doc_type",
            routes={"condition1": "node1", "condition2": "node2"},
            default_route="default_node",
            tags=["tag1", "tag2"],
            parameters={"param1": param_def},
        )

        # Register branch
        registry.register_branch(branch)

        # Get documentation
        doc = registry.get_branch_documentation("doc_branch")

        # Check documentation
        assert doc["name"] == "doc_branch"
        assert doc["description"] == "Branch with documentation"
        assert doc["type"] == "doc_type"
        assert doc["routes"] == {"condition1": "node1", "condition2": "node2"}
        assert doc["default_route"] == "default_node"
        assert "param1" in doc["parameters"]
        assert "tag1" in doc["tags"]

    def test_save_and_load(self):
        """Test saving and loading registry to/from file."""
        registry = GraphPatternRegistry.get_instance()

        # Create pattern with simple apply function
        def apply_func(graph):
            return graph

        apply_func.__name__ = "apply_func"
        apply_func.__module__ = __name__

        pattern = GraphPattern(
            metadata=PatternMetadata(
                name="save_pattern",
                description="Pattern for saving",
                pattern_type="save_type",
            ),
            apply_func=apply_func,
        )

        # Create branch with simple condition function
        def condition_func(state):
            return "result"

        condition_func.__name__ = "condition_func"
        condition_func.__module__ = __name__

        branch = BranchDefinition(
            name="save_branch",
            description="Branch for saving",
            condition_type="save_type",
            routes={"result": "node1"},
            condition_func=condition_func,
        )

        # Register pattern and branch
        registry.register_pattern(pattern)
        registry.register_branch(branch)

        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Save registry to file
            registry.save_to_file(temp_path)

            # Clear registry
            registry.clear()
            assert len(registry.patterns) == 0
            assert len(registry.branches) == 0

            # Define function resolver
            def func_resolver(module_name, func_name):
                if module_name == __name__:
                    if func_name == "apply_func":
                        return apply_func
                    if func_name == "condition_func":
                        return condition_func
                return None

            # Load registry from file
            registry.load_from_file(temp_path, func_resolver)

            # Check loaded pattern
            loaded_pattern = registry.get_pattern("save_pattern")
            assert loaded_pattern is not None
            assert loaded_pattern.metadata.name == "save_pattern"
            assert loaded_pattern.metadata.pattern_type == "save_type"
            assert loaded_pattern.apply_func is apply_func

            # Check loaded branch
            loaded_branch = registry.get_branch("save_branch")
            assert loaded_branch is not None
            assert loaded_branch.name == "save_branch"
            assert loaded_branch.condition_type == "save_type"
            assert loaded_branch.condition_func is condition_func

        finally:
            # Clean up temp file
            os.unlink(temp_path)


class TestDecorators:
    """Tests for the registry decorators."""

    def setup_method(self):
        """Set up test environment."""
        # Clear the registry before each test
        registry = GraphPatternRegistry.get_instance()
        registry.clear()

    def test_register_pattern_decorator(self):
        """Test the register_pattern decorator."""

        # Define a function with the decorator
        @register_pattern(
            name="decorator_pattern",
            pattern_type="decorator_type",
            description="Pattern from decorator",
        )
        def pattern_func(graph, param1="default"):
            """Function docstring."""
            return graph

        # Check registration
        registry = GraphPatternRegistry.get_instance()
        pattern = registry.get_pattern("decorator_pattern")

        assert pattern is not None
        assert pattern.metadata.name == "decorator_pattern"
        assert pattern.metadata.pattern_type == "decorator_type"
        assert pattern.apply_func is pattern_func
        assert "param1" in pattern.metadata.parameters

    def test_register_branch_decorator(self):
        """Test the register_branch decorator."""

        # Define a function with the decorator
        @register_branch(
            name="decorator_branch",
            condition_type="decorator_type",
            routes={"result": "target_node"},
            default_route="default_node",
        )
        def branch_func(state, param1="default"):
            """Function docstring."""
            return "result"

        # Check registration
        registry = GraphPatternRegistry.get_instance()
        branch = registry.get_branch("decorator_branch")

        assert branch is not None
        assert branch.name == "decorator_branch"
        assert branch.condition_type == "decorator_type"
        assert branch.routes == {"result": "target_node"}
        assert branch.default_route == "default_node"
        assert branch.condition_func is branch_func
        assert "param1" in branch.parameters
