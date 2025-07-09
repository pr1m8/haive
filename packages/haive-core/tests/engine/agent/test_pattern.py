from unittest.mock import MagicMock, patch

import pytest

from haive.core.engine.agent.pattern import PatternConfig, PatternManager


class TestPatternConfig:
    """Tests for the PatternConfig class."""

    def test_initialization(self):
        """Test basic initialization of pattern config."""
        pattern = PatternConfig(
            name="test_pattern",
            parameters={"param1": "value1"},
            order=1,
            condition="context.ready == True",
            enabled=True,
            metadata={"author": "test"},
        )

        assert pattern.name == "test_pattern"
        assert pattern.parameters["param1"] == "value1"
        assert pattern.order == 1
        assert pattern.condition == "context.ready == True"
        assert pattern.enabled is True
        assert pattern.metadata["author"] == "test"

    def test_merge_with(self):
        """Test merging pattern configurations."""
        pattern1 = PatternConfig(
            name="test_pattern",
            parameters={"param1": "value1", "common": "original"},
            order=1,
        )

        pattern2 = PatternConfig(
            name="test_pattern",
            parameters={"param2": "value2", "common": "override"},
            condition="x > 0",
        )

        # Merge patterns
        merged = pattern1.merge_with(pattern2)

        # Check results
        assert merged.name == "test_pattern"
        assert merged.parameters["param1"] == "value1"  # From pattern1
        assert merged.parameters["param2"] == "value2"  # From pattern2
        assert merged.parameters["common"] == "override"  # Overridden by pattern2
        assert merged.order == 1  # From pattern1
        assert merged.condition == "x > 0"  # From pattern2


class TestPatternManager:
    """Tests for the PatternManager class."""

    @pytest.fixture
    def pattern_manager(self):
        """Create a PatternManager for testing."""
        return PatternManager()

    def test_add_pattern(self, pattern_manager):
        """Test adding patterns to the manager."""
        # Add a simple pattern
        pattern_manager.add_pattern(
            pattern_name="test_pattern", parameters={"param1": "value1"}, order=1
        )

        # Add a second pattern
        pattern_manager.add_pattern(
            pattern_name="second_pattern", parameters={"param2": "value2"}, order=2
        )

        # Verify patterns were added
        assert len(pattern_manager.patterns) == 2
        assert pattern_manager.patterns[0].name == "test_pattern"
        assert pattern_manager.patterns[1].name == "second_pattern"

    def test_update_existing_pattern(self, pattern_manager):
        """Test updating an existing pattern."""
        # Add initial pattern
        pattern_manager.add_pattern(
            pattern_name="test_pattern", parameters={"param1": "value1"}, order=1
        )

        # Update the same pattern
        pattern_manager.add_pattern(
            pattern_name="test_pattern",
            parameters={"param2": "value2"},
            condition="x > 0",
        )

        # Should have merged the configurations
        assert len(pattern_manager.patterns) == 1
        pattern = pattern_manager.patterns[0]
        assert pattern.name == "test_pattern"
        assert pattern.parameters["param1"] == "value1"
        assert pattern.parameters["param2"] == "value2"
        assert pattern.order == 1
        assert pattern.condition == "x > 0"

    def test_set_pattern_parameters(self, pattern_manager):
        """Test setting global pattern parameters."""
        # Add a pattern
        pattern_manager.add_pattern(
            pattern_name="test_pattern", parameters={"specific": "value"}
        )

        # Set global parameters
        pattern_manager.set_pattern_parameters(
            "test_pattern", global_param="global_value", override="global_override"
        )

        # Add another pattern with specific parameter that overrides global
        pattern_manager.add_pattern(
            pattern_name="test_pattern_2",
            parameters={"specific": "value2", "override": "specific_override"},
        )

        # Set global parameters for the second pattern too
        pattern_manager.set_pattern_parameters(
            "test_pattern_2", global_param="global_value2", override="global_override"
        )

        # Check global parameters
        assert (
            pattern_manager.pattern_parameters["test_pattern"]["global_param"]
            == "global_value"
        )
        assert (
            pattern_manager.pattern_parameters["test_pattern"]["override"]
            == "global_override"
        )

        # Check combined parameters
        params1 = pattern_manager.get_pattern_parameters("test_pattern")
        assert params1["specific"] == "value"
        assert params1["global_param"] == "global_value"
        assert params1["override"] == "global_override"

        params2 = pattern_manager.get_pattern_parameters("test_pattern_2")
        assert params2["specific"] == "value2"
        assert params2["global_param"] == "global_value2"
        assert params2["override"] == "specific_override"  # Specific overrides global

    def test_pattern_ordering(self, pattern_manager):
        """Test pattern ordering based on order property."""
        # Add patterns out of order
        pattern_manager.add_pattern("p3", order=3)
        pattern_manager.add_pattern("p1", order=1)
        pattern_manager.add_pattern("p2", order=2)
        pattern_manager.add_pattern("no_order")  # No order specified

        # Get order
        order = pattern_manager.get_pattern_order()

        # Should be ordered by the order property
        assert order == ["p1", "p2", "p3", "no_order"]

    def test_disable_enable_patterns(self, pattern_manager):
        """Test disabling and enabling patterns."""
        # Add patterns
        pattern_manager.add_pattern("p1", order=1)
        pattern_manager.add_pattern("p2", order=2)
        pattern_manager.add_pattern("p3", order=3)

        # Check all are enabled
        order = pattern_manager.get_pattern_order()
        assert len(order) == 3
        assert "p1" in order
        assert "p2" in order

        # Disable one
        pattern_manager.disable_pattern("p2")

        # Check it's excluded from order
        order = pattern_manager.get_pattern_order()
        assert len(order) == 2
        assert "p1" in order
        assert "p2" not in order
        assert "p3" in order

        # Re-enable it
        pattern_manager.enable_pattern("p2")

        # Should be back in the order
        order = pattern_manager.get_pattern_order()
        assert len(order) == 3
        assert "p2" in order

    def test_applied_patterns_tracking(self, pattern_manager):
        """Test tracking of applied patterns."""
        # Initially no patterns applied
        assert len(pattern_manager._applied_patterns) == 0

        # Mark pattern as applied
        pattern_manager.mark_pattern_applied("test_pattern")

        # Check it's tracked
        assert pattern_manager.is_pattern_applied("test_pattern")
        assert not pattern_manager.is_pattern_applied("other_pattern")

        # Get all applied patterns
        applied = pattern_manager.applied_patterns_as_set()
        assert applied == {"test_pattern"}

    def test_serialization(self, pattern_manager):
        """Test serialization to/from dictionary."""
        # Add patterns
        pattern_manager.add_pattern(
            "test_pattern", parameters={"param1": "value1"}, order=1
        )
        pattern_manager.add_pattern(
            "second_pattern", parameters={"param2": "value2"}, order=2
        )

        # Set global parameters
        pattern_manager.set_pattern_parameters(
            "test_pattern", global_param="global_value"
        )

        # Mark applied
        pattern_manager.mark_pattern_applied("test_pattern")

        # Convert to dict
        data = pattern_manager.to_dict()

        # Check structure
        assert "patterns" in data
        assert "pattern_parameters" in data
        assert "applied_patterns" in data
        assert len(data["patterns"]) == 2
        assert data["applied_patterns"] == ["test_pattern"]

        # Create new manager from dict
        new_manager = PatternManager.from_dict(data)

        # Verify contents
        assert len(new_manager.patterns) == 2
        assert new_manager.patterns[0].name == "test_pattern"
        assert (
            new_manager.pattern_parameters["test_pattern"]["global_param"]
            == "global_value"
        )
        assert new_manager.is_pattern_applied("test_pattern")

    @patch("haive.core.graph.patterns.registry.GraphPatternRegistry")
    def test_validate_patterns(self, mock_registry, pattern_manager):
        """Test pattern validation against registry."""
        # Mock registry behavior
        registry_instance = MagicMock()
        mock_registry.get_instance.return_value = registry_instance

        # Mock get_pattern to return True for valid_pattern and False for invalid_pattern
        def mock_get_pattern(name):
            return name == "valid_pattern"

        registry_instance.get_pattern.side_effect = mock_get_pattern

        # Add patterns
        pattern_manager.add_pattern("valid_pattern")
        pattern_manager.add_pattern("invalid_pattern")

        # Validate
        invalid = pattern_manager.validate_patterns()

        # Should identify invalid pattern
        assert len(invalid) == 1
        assert "invalid_pattern" in invalid

    @patch("haive.core.graph.patterns.registry.GraphPatternRegistry")
    def test_get_required_components(self, mock_registry, pattern_manager):
        """Test getting components required by patterns."""
        # Mock registry behavior
        registry_instance = MagicMock()
        mock_registry.get_instance.return_value = registry_instance

        # Mock pattern with requirements
        pattern = MagicMock()
        pattern.metadata.required_components = ["component1", "component2"]
        registry_instance.get_pattern.return_value = pattern

        # Add a pattern
        pattern_manager.add_pattern("test_pattern")

        # Get required components
        components = pattern_manager.get_required_components()

        # Should return requirements
        assert len(components) == 2
        assert "component1" in components
        assert "component2" in components
