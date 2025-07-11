# tests/test_reference.py

from typing import Any, Dict

import pytest

from haive.core.engine.base import Engine, EngineRegistry, EngineType
from haive.core.engine.base.reference import ComponentRef


class TestRunnable:
    """Test runnable for reference testing."""

    def __init__(self, config: dict[str, Any]):
        self.config = config

    def invoke(self, input_data: Any, **kwargs):
        return f"Processed with {self.config.get('param', 'default')}: {input_data}"


class TestEngine(Engine[str, str]):
    """Test engine for reference testing."""

    engine_type: EngineType = EngineType.LLM
    param: str = "default"

    def create_runnable(self, runnable_config=None):
        params = self.apply_runnable_config(runnable_config) or {}
        config = {"param": params.get("param", self.param)}
        return TestRunnable(config)


def setup_function():
    """Setup for each test."""
    # Clear registry
    registry = EngineRegistry.get_instance()
    registry.clear()


def test_reference_creation():
    """Test creating references."""
    # Create reference with ID
    ref = ComponentRef(id="test_id")
    assert ref.id == "test_id"
    assert ref.name is None
    assert ref.type is None

    # Create reference with name and type
    ref = ComponentRef(name="test_name", type=EngineType.LLM)
    assert ref.id is None
    assert ref.name == "test_name"
    assert ref.type == EngineType.LLM

    # Create reference with string type
    ref = ComponentRef(name="test_name", type="llm")
    assert ref.type == EngineType.LLM  # Should convert to enum


def test_from_engine():
    """Test creating reference from engine."""
    # Create engine
    engine = TestEngine(id="test_id", name="test_engine", engine_type=EngineType.LLM)

    # Create reference from engine
    ref = ComponentRef.from_engine(engine)

    # Check reference properties
    assert ref.id == "test_id"
    assert ref.name == "test_engine"
    assert ref.type == EngineType.LLM


def test_resolve_by_id():
    """Test resolving reference by ID."""
    # Create and register engine
    TestEngine(id="test_id", name="test_engine", param="engine_param").register()

    # Create reference by ID
    ref = ComponentRef(id="test_id")

    # Resolve reference
    component = ref.resolve()

    # Check component
    assert component is not None
    result = component.invoke("test")
    assert result == "Processed with engine_param: test"


def test_resolve_by_name_and_type():
    """Test resolving reference by name and type."""
    # Create and register engine
    TestEngine(name="test_engine", param="engine_param").register()

    # Create reference by name and type
    ref = ComponentRef(name="test_engine", type=EngineType.LLM)

    # Resolve reference
    component = ref.resolve()

    # Check component
    assert component is not None
    result = component.invoke("test")
    assert result == "Processed with engine_param: test"


def test_resolve_with_config_overrides():
    """Test resolving reference with config overrides."""
    # Create and register engine
    TestEngine(name="test_engine", param="engine_param").register()

    # Create reference with config overrides
    ref = ComponentRef(
        name="test_engine",
        type=EngineType.LLM,
        config_overrides={"param": "override_param"},
    )

    # Resolve reference
    component = ref.resolve()

    # Check component with overrides applied
    assert component is not None
    result = component.invoke("test")
    assert result == "Processed with override_param: test"


def test_reference_caching():
    """Test that references cache resolved components."""
    # Create and register engine
    engine = TestEngine(name="test_engine").register()

    # Create reference
    ref = ComponentRef.from_engine(engine)

    # Resolve multiple times
    component1 = ref.resolve()
    component2 = ref.resolve()

    # Should be the same instance
    assert component1 is component2


def test_invalidate_cache():
    """Test invalidating reference cache."""
    # Create and register engine
    engine = TestEngine(name="test_engine").register()

    # Create reference
    ref = ComponentRef.from_engine(engine)

    # Resolve once
    component1 = ref.resolve()

    # Invalidate cache
    ref.invalidate_cache()

    # Resolve again
    component2 = ref.resolve()

    # Should be different instances
    assert component1 is not component2


def test_resolve_nonexistent():
    """Test resolving nonexistent reference."""
    # Create reference to nonexistent engine
    ref = ComponentRef(id="nonexistent")

    # Resolve should return None
    component = ref.resolve()
    assert component is None


def test_reference_serialization():
    """Test reference serialization."""
    # Create reference
    ref = ComponentRef(
        id="test_id",
        name="test_name",
        type=EngineType.LLM,
        config_overrides={"param": "override"},
    )

    # Resolve (to test cache is not serialized)
    TestEngine(id="test_id", name="test_name").register()
    ref.resolve()

    # Serialize to dict
    data = ref.model_dump()

    # Check serialized data
    assert data["id"] == "test_id"
    assert data["name"] == "test_name"
    assert data["type"] == "llm"  # Enum converted to string
    assert data["config_overrides"]["param"] == "override"
    assert "_resolved" not in data  # Cache not serialized

    # Deserialize
    new_ref = ComponentRef.model_validate(data)
    assert new_ref.id == "test_id"
    assert new_ref.name == "test_name"
    assert new_ref.type == EngineType.LLM
    assert new_ref.config_overrides["param"] == "override"
    assert new_ref._resolved is None  # Cache not restored


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
