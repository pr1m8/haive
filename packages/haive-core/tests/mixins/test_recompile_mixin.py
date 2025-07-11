"""Test RecompileMixin functionality."""

from datetime import datetime

import pytest
from pydantic import BaseModel, Field

from haive.core.mixins.recompile_mixin import RecompileMixin


class MockComponent(BaseModel, RecompileMixin):
    """Mock component that uses RecompileMixin."""

    name: str = Field(default="test_component")
    version: int = Field(default=1)

    def _trigger_auto_recompile(self) -> None:
        """Override to test auto-recompile behavior."""
        self.version += 1
        self.resolve_recompile(success=True)


class TestRecompileMixin:
    """Test suite for RecompileMixin."""

    def test_initial_state(self):
        """Test initial recompilation state."""
        component = MockComponent()

        assert component.needs_recompile is False
        assert component.recompile_reasons == []
        assert component.recompile_count == 0
        assert component.recompile_history == []
        assert component.auto_recompile is False
        assert component.recompile_threshold == 10

    def test_mark_for_recompile(self):
        """Test marking component for recompilation."""
        component = MockComponent()

        # Mark for recompile
        component.mark_for_recompile("Test reason")

        assert component.needs_recompile is True
        assert "Test reason" in component.recompile_reasons
        assert len(component.recompile_history) == 1

        # Check history entry
        entry = component.recompile_history[0]
        assert entry["reason"] == "Test reason"
        assert entry["action"] == "marked_for_recompile"
        assert entry["resolved"] is False
        assert "timestamp" in entry

    def test_multiple_reasons(self):
        """Test multiple recompilation reasons."""
        component = MockComponent()

        component.mark_for_recompile("Reason 1")
        component.mark_for_recompile("Reason 2")
        component.mark_for_recompile("Reason 1")  # Duplicate

        assert component.needs_recompile is True
        assert len(component.recompile_reasons) == 2
        assert "Reason 1" in component.recompile_reasons
        assert "Reason 2" in component.recompile_reasons
        assert len(component.recompile_history) == 3  # All attempts recorded

    def test_resolve_recompile(self):
        """Test resolving recompilation."""
        component = MockComponent()

        # Mark for recompile
        component.mark_for_recompile("Test reason")
        assert component.needs_recompile is True

        # Resolve
        component.resolve_recompile(success=True)

        assert component.needs_recompile is False
        assert component.recompile_reasons == []
        assert component.recompile_count == 1
        assert len(component.recompile_history) == 2  # Mark + resolve

        # Check resolve entry
        resolve_entry = component.recompile_history[1]
        assert resolve_entry["action"] == "resolved_recompile"
        assert resolve_entry["success"] is True
        assert resolve_entry["recompile_count"] == 1
        assert "resolved_reasons" in resolve_entry

    def test_resolve_recompile_failure(self):
        """Test resolving recompilation with failure."""
        component = MockComponent()

        component.mark_for_recompile("Test reason")
        component.resolve_recompile(success=False)

        assert component.needs_recompile is False
        assert component.recompile_count == 0  # No increment on failure

        resolve_entry = component.recompile_history[1]
        assert resolve_entry["success"] is False

    def test_resolve_without_marking(self):
        """Test resolving when not marked for recompile."""
        component = MockComponent()

        # Should not raise error but should log warning
        component.resolve_recompile()

        assert component.needs_recompile is False
        assert component.recompile_count == 0

    def test_auto_recompile_threshold(self):
        """Test automatic recompilation when threshold is reached."""
        component = MockComponent()
        component.recompile_threshold = 2

        initial_version = component.version

        # First reason - should not trigger
        component.mark_for_recompile("Reason 1")
        assert component.version == initial_version
        assert component.needs_recompile is True

        # Second reason - should trigger auto recompile
        component.mark_for_recompile("Reason 2")
        assert component.version == initial_version + 1
        assert component.needs_recompile is False  # Resolved

    def test_auto_recompile_enabled(self):
        """Test automatic recompilation when enabled."""
        component = MockComponent()
        component.auto_recompile = True

        initial_version = component.version

        # Should trigger immediately
        component.mark_for_recompile("Test reason")
        assert component.version == initial_version + 1
        assert component.needs_recompile is False

    def test_force_recompile(self):
        """Test forcing recompilation."""
        component = MockComponent()

        initial_version = component.version

        component.force_recompile("Forced recompile")

        assert component.version == initial_version + 1
        assert component.needs_recompile is False
        assert component.recompile_count == 1

    def test_get_recompile_status(self):
        """Test getting recompilation status."""
        component = MockComponent()

        # Initial status
        status = component.get_recompile_status()
        assert status["needs_recompile"] is False
        assert status["pending_reasons"] == []
        assert status["reason_count"] == 0
        assert status["total_recompiles"] == 0
        assert status["auto_recompile"] is False
        assert status["last_recompile"] is None

        # After marking
        component.mark_for_recompile("Test reason")
        status = component.get_recompile_status()
        assert status["needs_recompile"] is True
        assert status["reason_count"] == 1

        # After resolving
        component.resolve_recompile()
        status = component.get_recompile_status()
        assert status["needs_recompile"] is False
        assert status["total_recompiles"] == 1
        assert status["last_recompile"] is not None

    def test_clear_recompile_history(self):
        """Test clearing recompilation history."""
        component = MockComponent()

        # Create some history
        for i in range(5):
            component.mark_for_recompile(f"Reason {i}")

        assert len(component.recompile_history) == 5

        # Clear keeping 2 recent
        component.clear_recompile_history(keep_recent=2)
        assert len(component.recompile_history) == 2

        # Clear all
        component.clear_recompile_history(keep_recent=0)
        assert len(component.recompile_history) == 0

    def test_add_recompile_trigger(self):
        """Test adding conditional recompile triggers."""
        component = MockComponent()

        # Condition that returns True
        def condition_true():
            return True

        # Condition that returns False
        def condition_false():
            return False

        # Test true condition
        component.add_recompile_trigger(condition_true, "Condition met")
        assert component.needs_recompile is True
        assert "Condition met" in component.recompile_reasons

        # Reset
        component.resolve_recompile()

        # Test false condition
        component.add_recompile_trigger(condition_false, "Won't trigger")
        assert component.needs_recompile is False
        assert "Won't trigger" not in component.recompile_reasons

    def test_check_recompile_conditions(self):
        """Test checking recompilation conditions."""
        component = MockComponent()

        # Default implementation just returns needs_recompile
        assert component.check_recompile_conditions() is False

        component.mark_for_recompile("Test")
        assert component.check_recompile_conditions() is True

        component.resolve_recompile()
        assert component.check_recompile_conditions() is False

    def test_recompile_with_agent_like_usage(self):
        """Test recompilation in agent-like scenario."""
        component = MockComponent()

        # Simulate updating tools
        component.mark_for_recompile("Tools updated")

        # Simulate schema change
        component.mark_for_recompile("Schema changed")

        # Check status
        status = component.get_recompile_status()
        assert status["needs_recompile"] is True
        assert status["reason_count"] == 2

        # Simulate rebuild
        if component.needs_recompile:
            # Perform rebuild logic here
            component.resolve_recompile(success=True)

        # Verify resolved
        assert component.needs_recompile is False
        assert component.recompile_count == 1

        # Check history tracks everything
        assert len(component.recompile_history) == 3  # 2 marks + 1 resolve
