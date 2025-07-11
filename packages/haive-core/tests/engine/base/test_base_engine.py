# tests/test_engine_base.py


import pytest
from pydantic import BaseModel

from haive.core.engine.base import (
    Engine,
    EngineRegistry,
    EngineType,
    InvokableEngine,
    NonInvokableEngine,
)


class TestModel(BaseModel):
    value: str


class TestEngine(Engine[str, str]):
    engine_type: EngineType = EngineType.LLM
    test_param: str = "default"

    def create_runnable(self, runnable_config=None):
        params = self.apply_runnable_config(runnable_config) or {}
        test_param = params.get("test_param", self.test_param)
        return lambda x: f"{test_param}: {x}"


class TestInvokableEngine(InvokableEngine[str, str]):
    engine_type = EngineType.LLM
    test_param: str = "default"

    def create_runnable(self, runnable_config=None):
        params = self.apply_runnable_config(runnable_config) or {}
        test_param = params.get("test_param", self.test_param)
        return lambda x: f"{test_param}: {x}"


class TestNonInvokableEngine(NonInvokableEngine[str, str]):
    engine_type = EngineType.EMBEDDINGS
    test_param: str = "default"

    def create_runnable(self, runnable_config=None):
        params = self.apply_runnable_config(runnable_config) or {}
        test_param = params.get("test_param", self.test_param)
        return lambda x: f"{test_param}: {x}"


def test_engine_creation():
    """Test basic engine creation."""
    engine = TestEngine(name="test_engine")
    assert engine.name == "test_engine"
    assert engine.engine_type == EngineType.LLM
    assert engine.test_param == "default"
    assert engine.id is not None


def test_invokable_engine():
    """Test InvokableEngine functionality."""
    engine = TestInvokableEngine(name="test_engine")

    # Test invoke method
    result = engine.invoke("hello")
    assert result == "default: hello"

    # Test invoke with config
    config = {"configurable": {"test_param": "custom"}}
    result = engine.invoke("hello", config)
    assert result == "custom: hello"


def test_non_invokable_engine():
    """Test NonInvokableEngine functionality."""
    engine = TestNonInvokableEngine(name="test_engine")

    # Test instantiate method
    instance = engine.instantiate()
    assert callable(instance)
    assert instance("hello") == "default: hello"

    # Test instantiate with config
    config = {"configurable": {"test_param": "custom"}}
    instance = engine.instantiate(config)
    assert instance("hello") == "custom: hello"


def test_engine_registry():
    """Test engine registry operations."""
    # Clear registry
    registry = EngineRegistry.get_instance()
    registry.clear()

    # Create and register engines
    engine1 = TestEngine(name="engine1", id="id1").register()
    engine2 = TestEngine(name="engine2", id="id2").register()

    # Test get by type and name
    assert registry.get(EngineType.LLM, "engine1") is engine1
    assert registry.get(EngineType.LLM, "engine2") is engine2

    # Test get by ID
    assert registry.find_by_id("id1") is engine1
    assert registry.find_by_id("id2") is engine2

    # Test find by name or ID
    assert registry.find("engine1") is engine1
    assert registry.find("id2") is engine2

    # Test list engines
    assert set(registry.list(EngineType.LLM)) == {"engine1", "engine2"}

    # Test get all engines
    all_engines = registry.get_all(EngineType.LLM)
    assert len(all_engines) == 2
    assert all_engines["engine1"] is engine1
    assert all_engines["engine2"] is engine2


def test_apply_runnable_config():
    """Test that runnable config is applied correctly."""
    engine = TestEngine(name="test_engine")

    # Simple config
    config = {"configurable": {"test_param": "custom"}}
    params = engine.apply_runnable_config(config)
    assert params == {"test_param": "custom"}

    # Config with engine ID targeting
    config = {"configurable": {"engine_configs": {engine.id: {"test_param": "by_id"}}}}
    params = engine.apply_runnable_config(config)
    assert params == {"test_param": "by_id"}

    # Config with engine name targeting
    config = {
        "configurable": {"engine_configs": {"test_engine": {"test_param": "by_name"}}}
    }
    params = engine.apply_runnable_config(config)
    assert params == {"test_param": "by_name"}

    # Config with engine type targeting
    config = {
        "configurable": {"engine_configs": {"llm_config": {"test_param": "by_type"}}}
    }
    params = engine.apply_runnable_config(config)
    assert params == {"test_param": "by_type"}

    # Test priority (ID > name > type > global)
    config = {
        "configurable": {
            "test_param": "global",
            "engine_configs": {
                "llm_config": {"test_param": "by_type"},
                "test_engine": {"test_param": "by_name"},
                engine.id: {"test_param": "by_id"},
            },
        }
    }
    params = engine.apply_runnable_config(config)
    assert params == {"test_param": "by_id"}


def test_with_config_overrides():
    """Test creating a new engine with config overrides."""
    engine = TestEngine(name="test_engine", test_param="original")

    # Create new engine with overrides
    new_engine = engine.with_config_overrides({"test_param": "overridden"})

    # Original should be unchanged
    assert engine.test_param == "original"

    # New engine should have override applied
    assert new_engine.test_param == "overridden"
    assert new_engine.name == "test_engine"  # Other params unchanged
    assert new_engine.id == engine.id  # ID should be preserved


def test_serialization():
    """Test engine serialization and deserialization."""
    engine = TestEngine(name="test_engine", test_param="test")

    # Convert to dict
    data = engine.to_dict()
    assert data["name"] == "test_engine"
    assert data["test_param"] == "test"
    assert "engine_class" in data

    # Convert to JSON
    json_str = engine.to_json()
    assert isinstance(json_str, str)

    # Deserialize from dict
    new_engine = Engine.from_dict(data)
    assert isinstance(new_engine, TestEngine)
    assert new_engine.name == "test_engine"
    assert new_engine.test_param == "test"

    # Deserialize from JSON
    new_engine = TestEngine.from_json(json_str)
    assert isinstance(new_engine, TestEngine)
    assert new_engine.name == "test_engine"
    assert new_engine.test_param == "test"


def test_registry_serialization():
    """Test registry serialization and deserialization."""
    # Clear registry
    registry = EngineRegistry.get_instance()
    registry.clear()

    # Create and register engines
    TestEngine(name="engine1", test_param="test1").register()
    TestEngine(name="engine2", test_param="test2").register()

    # Serialize registry
    registry_dict = registry.to_dict()
    assert EngineType.LLM in registry_dict
    assert "engine1" in registry_dict[EngineType.LLM]
    assert "engine2" in registry_dict[EngineType.LLM]

    # Serialize to JSON
    registry_json = registry.to_json()
    assert isinstance(registry_json, str)

    # Clear registry and restore from dict
    registry.clear()
    assert len(registry.list(EngineType.LLM)) == 0

    registry.from_dict(registry_dict)
    assert len(registry.list(EngineType.LLM)) == 2
    assert registry.get(EngineType.LLM, "engine1") is not None
    assert registry.get(EngineType.LLM, "engine2") is not None

    # Clear registry and restore from JSON
    registry.clear()
    registry.from_json(registry_json)
    assert len(registry.list(EngineType.LLM)) == 2
    assert registry.get(EngineType.LLM, "engine1") is not None
    assert registry.get(EngineType.LLM, "engine2") is not None


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
