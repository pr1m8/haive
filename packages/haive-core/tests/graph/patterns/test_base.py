"""Tests for the graph pattern base classes.

This module tests the core base classes for the pattern system, including
ComponentRequirement, ParameterDefinition, PatternMetadata, GraphPattern, and BranchDefinition.
"""

from unittest.mock import Mock

import pytest

from haive.core.graph.patterns.base import (
    BranchDefinition,
    ComponentRequirement,
    GraphPattern,
    ParameterDefinition,
    PatternMetadata,
)


class TestComponentRequirement:
    """Tests for the ComponentRequirement class."""

    def test_initialization(self):
        """Test basic initialization."""
        req = ComponentRequirement(type="llm")
        assert req.type == "llm"
        assert req.count == 1
        assert req.optional is False
        assert req.capabilities == []
        assert req.name is None
        assert req.description is None

    def test_validation_with_matching_component(self):
        """Test validation of a matching component."""
        req = ComponentRequirement(type="llm")

        # Mock component with correct type
        component = Mock()
        component.engine_type.value = "llm"

        assert req.validate_component(component) is True

    def test_validation_with_non_matching_component(self):
        """Test validation of a non-matching component."""
        req = ComponentRequirement(type="llm")

        # Mock component with incorrect type
        component = Mock()
        component.engine_type.value = "retriever"

        assert req.validate_component(component) is False

    def test_validation_with_string_component(self):
        """Test validation with string component."""
        req = ComponentRequirement(type="llm")

        # String component
        assert req.validate_component("llm") is True
        assert req.validate_component("retriever") is False

    def test_validation_with_dict_component(self):
        """Test validation with dict component."""
        req = ComponentRequirement(type="llm")

        # Dict component
        assert req.validate_component({"type": "llm"}) is True
        assert req.validate_component({"type": "retriever"}) is False


class TestParameterDefinition:
    """Tests for the ParameterDefinition class."""

    def test_initialization(self):
        """Test basic initialization."""
        param = ParameterDefinition(type="str", description="A string parameter")
        assert param.type == "str"
        assert param.description == "A string parameter"
        assert param.default is None
        assert param.required is False
        assert param.choices is None
        assert param.min_value is None
        assert param.max_value is None

    def test_validation_with_required_parameter(self):
        """Test validation of a required parameter."""
        param = ParameterDefinition(
            type="str", description="A required parameter", required=True
        )

        # Missing required parameter
        is_valid, error = param.validate_value(None)
        assert is_valid is False
        assert "Required parameter missing" in error

    def test_validation_with_type_checking(self):
        """Test validation with type checking."""
        param = ParameterDefinition(type="str", description="A string parameter")

        # Correct type
        is_valid, error = param.validate_value("test")
        assert is_valid is True
        assert error is None

        # Incorrect type
        is_valid, error = param.validate_value(123)
        assert is_valid is False
        assert "Expected type" in error

    def test_validation_with_choices(self):
        """Test validation with choices."""
        param = ParameterDefinition(
            type="str",
            description="A parameter with choices",
            choices=["option1", "option2"],
        )

        # Valid choice
        is_valid, error = param.validate_value("option1")
        assert is_valid is True
        assert error is None

        # Invalid choice
        is_valid, error = param.validate_value("option3")
        assert is_valid is False
        assert "Value must be one of" in error

    def test_validation_with_numeric_constraints(self):
        """Test validation with numeric constraints."""
        param = ParameterDefinition(
            type="int", description="A numeric parameter", min_value=5, max_value=10
        )

        # Within range
        is_valid, error = param.validate_value(7)
        assert is_valid is True
        assert error is None

        # Below minimum
        is_valid, error = param.validate_value(3)
        assert is_valid is False
        assert "Value must be >=" in error

        # Above maximum
        is_valid, error = param.validate_value(12)
        assert is_valid is False
        assert "Value must be <=" in error


class TestPatternMetadata:
    """Tests for the PatternMetadata class."""

    def test_initialization(self):
        """Test basic initialization."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )
        assert metadata.name == "test_pattern"
        assert metadata.description == "A test pattern"
        assert metadata.pattern_type == "test"
        assert metadata.version == "1.0.0"
        assert metadata.required_components == []
        assert metadata.parameters == {}
        assert metadata.dependencies == []
        assert metadata.constraints == {}
        assert metadata.examples == []
        assert metadata.tags == []

    def test_check_required_components_with_missing_components(self):
        """Test checking required components with missing ones."""
        requirement = ComponentRequirement(type="llm", count=2)

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            required_components=[requirement],
        )

        # Mock component with correct type
        component = Mock()
        component.engine_type.value = "llm"

        # Only one llm component, but two required
        components = [component]

        missing = metadata.check_required_components(components)
        assert len(missing) == 1
        assert "llm" in missing[0]
        assert "need 2" in missing[0]

    def test_check_required_components_with_sufficient_components(self):
        """Test checking required components with sufficient ones."""
        requirement = ComponentRequirement(type="llm", count=2)

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            required_components=[requirement],
        )

        # Mock component with correct type
        component1 = Mock()
        component1.engine_type.value = "llm"
        component2 = Mock()
        component2.engine_type.value = "llm"

        # Two llm components, meeting the requirement
        components = [component1, component2]

        missing = metadata.check_required_components(components)
        assert len(missing) == 0

    def test_validate_parameters_with_valid_params(self):
        """Test validating parameters with valid values."""
        param_def = ParameterDefinition(
            type="str", description="A string parameter", required=True
        )

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            parameters={"param1": param_def},
        )

        is_valid, errors = metadata.validate_parameters({"param1": "test_value"})
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_parameters_with_invalid_params(self):
        """Test validating parameters with invalid values."""
        param_def = ParameterDefinition(
            type="str", description="A string parameter", required=True
        )

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            parameters={"param1": param_def},
        )

        # Missing required parameter
        is_valid, errors = metadata.validate_parameters({})
        assert is_valid is False
        assert len(errors) == 1
        assert "param1" in errors[0]

    def test_validate_parameters_with_unknown_params(self):
        """Test validating parameters with unknown values."""
        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            parameters={},
        )

        # Unknown parameter
        is_valid, errors = metadata.validate_parameters({"unknown_param": "value"})
        assert is_valid is False
        assert len(errors) == 1
        assert "Unknown parameters" in errors[0]


class TestGraphPattern:
    """Tests for the GraphPattern class."""

    def test_initialization(self):
        """Test basic initialization."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        pattern = GraphPattern(metadata=metadata)

        assert pattern.metadata == metadata
        assert pattern.apply_func is None

    def test_property_accessors(self):
        """Test property accessors."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        pattern = GraphPattern(metadata=metadata)

        assert pattern.name == "test_pattern"
        assert pattern.description == "A test pattern"
        assert pattern.pattern_type == "test"

    def test_validate_for_application_with_invalid_components(self):
        """Test validation for application with invalid components."""
        requirement = ComponentRequirement(type="llm", count=1)

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            required_components=[requirement],
        )

        pattern = GraphPattern(metadata=metadata)

        # No components
        is_valid, errors = pattern.validate_for_application([], {})
        assert is_valid is False
        assert len(errors) == 1
        assert "Missing required components" in errors[0]

    def test_validate_for_application_with_invalid_parameters(self):
        """Test validation for application with invalid parameters."""
        param_def = ParameterDefinition(
            type="str", description="A string parameter", required=True
        )

        metadata = PatternMetadata(
            name="test_pattern",
            description="A test pattern",
            pattern_type="test",
            parameters={"param1": param_def},
        )

        pattern = GraphPattern(metadata=metadata)

        # Missing required parameter
        is_valid, errors = pattern.validate_for_application([], {})
        assert is_valid is False
        assert len(errors) >= 1

    def test_apply_without_implementation(self):
        """Test applying a pattern without implementation."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        pattern = GraphPattern(metadata=metadata)

        # Mock graph
        graph = Mock()
        graph.components = []

        # Should raise ValueError because no apply_func
        with pytest.raises(ValueError) as excinfo:
            pattern.apply(graph)

        assert "has no implementation" in str(excinfo.value)

    def test_apply_with_implementation(self):
        """Test applying a pattern with implementation."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        # Mock apply function
        apply_func = Mock(return_value="result")

        pattern = GraphPattern(metadata=metadata, apply_func=apply_func)

        # Mock graph with required components
        graph = Mock()
        component = Mock()
        component.engine_type.value = "llm"
        graph.components = [component]
        graph.applied_patterns = []

        # Apply the pattern
        result = pattern.apply(graph)

        # Check result
        assert result == "result"
        assert apply_func.called
        assert apply_func.call_args[0][0] == graph

    def test_to_dict_serialization(self):
        """Test serialization to dictionary."""
        metadata = PatternMetadata(
            name="test_pattern", description="A test pattern", pattern_type="test"
        )

        # Mock apply function
        def apply_func(graph, **kwargs):
            return graph

        apply_func.__name__ = "apply_func"
        apply_func.__module__ = "test_module"

        pattern = GraphPattern(metadata=metadata, apply_func=apply_func)

        # Convert to dict
        data = pattern.to_dict()

        # Check serialization
        assert "metadata" in data
        assert data["metadata"]["name"] == "test_pattern"
        assert "apply_func_name" in data
        assert data["apply_func_name"] == "apply_func"
        assert data["apply_func_module"] == "test_module"


class TestBranchDefinition:
    """Tests for the BranchDefinition class."""

    def test_initialization(self):
        """Test basic initialization."""
        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1", "condition2": "node2"},
        )

        assert branch.name == "test_branch"
        assert branch.description == "A test branch"
        assert branch.condition_type == "test"
        assert branch.routes == {"condition1": "node1", "condition2": "node2"}
        assert branch.default_route == "END"
        assert branch.parameters == {}
        assert branch.condition_factory is None
        assert branch.condition_func is None

    def test_create_condition_without_implementation(self):
        """Test creating a condition without implementation."""
        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
        )

        # Should raise ValueError because no implementation
        with pytest.raises(ValueError) as excinfo:
            branch.create_condition()

        assert "has no implementation" in str(excinfo.value)

    def test_create_condition_with_factory(self):
        """Test creating a condition with factory."""
        # Mock condition factory
        condition_factory = Mock(return_value="factory_condition")

        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
            condition_factory=condition_factory,
        )

        # Create condition
        condition = branch.create_condition(param1="value1")

        # Check result
        assert condition == "factory_condition"
        assert condition_factory.called
        assert condition_factory.call_args[1]["param1"] == "value1"

    def test_create_condition_with_function(self):
        """Test creating a condition with function."""
        # Mock condition function
        condition_func = Mock(return_value="condition_result")

        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
            condition_func=condition_func,
        )

        # Create condition
        condition = branch.create_condition()

        # Check result
        assert condition == condition_func

    def test_validate_parameters(self):
        """Test parameter validation."""
        param_def = ParameterDefinition(
            type="str", description="A string parameter", required=True
        )

        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
            parameters={"param1": param_def},
        )

        # Valid parameters
        is_valid, errors = branch.validate_parameters({"param1": "value1"})
        assert is_valid is True
        assert len(errors) == 0

        # Invalid parameters
        is_valid, errors = branch.validate_parameters({})
        assert is_valid is False
        assert len(errors) == 1
        assert "param1" in errors[0]

    def test_apply_to_graph(self):
        """Test applying a branch to a graph."""
        # Mock condition function
        condition_func = Mock(return_value="condition_result")

        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1", "condition2": "END"},
            condition_func=condition_func,
        )

        # Mock graph
        graph = Mock()
        graph.add_conditional_edges = Mock()

        # Apply the branch
        result = branch.apply_to_graph(graph, "source_node")

        # Check result
        assert result == graph
        assert graph.add_conditional_edges.called

        # Check that the END constant was properly handled
        call_args = graph.add_conditional_edges.call_args
        assert call_args[0][0] == "source_node"  # source node
        assert call_args[0][1] == condition_func  # condition function

        routes = call_args[0][2]  # routes dict
        assert "condition1" in routes
        assert routes["condition1"] == "node1"
        assert "condition2" in routes
        # END should be passed as the actual constant, not a string
        assert routes["condition2"] != "END"

    def test_to_dict_serialization(self):
        """Test serialization to dictionary."""

        # Mock condition function
        def condition_func(state):
            return "result"

        condition_func.__name__ = "condition_func"
        condition_func.__module__ = "test_module"

        branch = BranchDefinition(
            name="test_branch",
            description="A test branch",
            condition_type="test",
            routes={"condition1": "node1"},
            condition_func=condition_func,
        )

        # Convert to dict
        data = branch.to_dict()

        # Check serialization
        assert data["name"] == "test_branch"
        assert data["description"] == "A test branch"
        assert data["condition_type"] == "test"
        assert data["routes"] == {"condition1": "node1"}
        assert "condition_func_name" in data
        assert data["condition_func_name"] == "condition_func"
        assert data["condition_func_module"] == "test_module"
