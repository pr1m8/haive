# tests/core/config/test_runnable_config_manager.py

import uuid
from typing import Any

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.base import EngineType, InvokableEngine


# Mock engine model for testing
class MockEngine(InvokableEngine):
    engine_type: EngineType = EngineType.LLM
    model_name: str = "test-model"
    temperature: float = 0.7
    max_tokens: int | None = 1024
    special_param: str | None = None

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        # Simple mock implementation
        return lambda x: {"result": f"Result from {self.model_name}"}


# Mock retriever engine to test different parameter sets
class MockRetrieverEngine(InvokableEngine):
    engine_type: EngineType = EngineType.RETRIEVER
    top_k: int = 3
    similarity_threshold: float = 0.8
    filter_criteria: dict[str, Any] | None = None

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        # Simple mock implementation
        return lambda x: {"documents": ["doc1", "doc2", "doc3"]}


# Define a custom Pydantic model for testing from_model
class TestConfig(BaseModel):
    user_id: str
    temperature: float = 0.5
    custom_setting: str | None = None


class TestRunnableConfigManager:
    """Test suite for the RunnableConfigManager."""

    def test_create_basic(self):
        """Test creating a basic RunnableConfig."""
        # Create with thread_id
        thread_id = str(uuid.uuid4())
        config = RunnableConfigManager.create(thread_id=thread_id)

        # Verify structure
        assert "configurable" in config
        assert "thread_id" in config["configurable"]
        assert config["configurable"]["thread_id"] == thread_id
        assert "engine_configs" in config["configurable"]
        assert isinstance(config["configurable"]["engine_configs"], dict)

        # Create with auto-generated thread_id
        config = RunnableConfigManager.create()
        assert "thread_id" in config["configurable"]
        assert isinstance(config["configurable"]["thread_id"], str)
        assert len(config["configurable"]["thread_id"]) > 0

    def test_create_with_additional_params(self):
        """Test creating a config with additional parameters."""
        config = RunnableConfigManager.create(
            user_id="test-user", temperature=0.8, custom_param="custom-value"
        )

        # Check additional parameters
        assert config["configurable"]["user_id"] == "test-user"
        assert config["configurable"]["temperature"] == 0.8
        assert config["configurable"]["custom_param"] == "custom-value"

    def test_create_with_engine_llm(self):
        """Test creating a config from an LLM engine."""
        # Create an LLM engine
        engine = MockEngine(
            id="test-engine-id",
            name="test-llm",
            model_name="gpt-4",
            temperature=0.5,
            special_param="special-value",
        )

        # Create config with engine
        config = RunnableConfigManager.create_with_engine(
            engine=engine, thread_id="test-thread", user_id="test-user"
        )

        # Check basic structure
        assert config["configurable"]["thread_id"] == "test-thread"
        assert config["configurable"]["user_id"] == "test-user"
        assert "engine_configs" in config["configurable"]

        # Check engine configs by ID
        assert engine.id in config["configurable"]["engine_configs"]
        assert (
            config["configurable"]["engine_configs"][engine.id]["model_name"] == "gpt-4"
        )
        assert config["configurable"]["engine_configs"][engine.id]["temperature"] == 0.5
        assert (
            config["configurable"]["engine_configs"][engine.id]["special_param"]
            == "special-value"
        )

        # Check engine configs by name
        assert "test-llm" in config["configurable"]["engine_configs"]

        # Check engine configs by type
        assert "llm_config" in config["configurable"]["engine_configs"]

    def test_create_with_engine_retriever(self):
        """Test creating a config from a retriever engine."""
        # Create a retriever engine
        engine = MockRetrieverEngine(
            id="retriever-id",
            name="test-retriever",
            top_k=5,
            similarity_threshold=0.75,
            filter_criteria={"category": "science"},
        )

        # Create config with engine
        config = RunnableConfigManager.create_with_engine(
            engine=engine, thread_id="test-thread"
        )

        # Check engine configs by ID
        assert engine.id in config["configurable"]["engine_configs"]
        assert config["configurable"]["engine_configs"][engine.id]["top_k"] == 5
        assert (
            config["configurable"]["engine_configs"][engine.id]["similarity_threshold"]
            == 0.75
        )
        assert config["configurable"]["engine_configs"][engine.id][
            "filter_criteria"
        ] == {"category": "science"}

        # Check engine configs by type
        assert "retriever_config" in config["configurable"]["engine_configs"]

    def test_create_with_metadata(self):
        """Test creating a config with metadata."""
        metadata = {
            "session_id": "test-session",
            "timestamp": "2023-01-01T12:00:00Z",
            "source": "test-application",
        }

        config = RunnableConfigManager.create_with_metadata(
            metadata=metadata, thread_id="test-thread", user_id="test-user"
        )

        # Check metadata
        assert "metadata" in config
        assert config["metadata"] == metadata

        # Check basic config
        assert config["configurable"]["thread_id"] == "test-thread"
        assert config["configurable"]["user_id"] == "test-user"

    def test_merge_configs(self):
        """Test merging two configs."""
        # Create base config
        base_config = RunnableConfigManager.create(
            thread_id="base-thread", user_id="base-user", base_param="base-value"
        )

        # Create override config
        override_config = RunnableConfigManager.create(
            thread_id="override-thread", override_param="override-value"
        )

        # Merge configs
        merged_config = RunnableConfigManager.merge(base_config, override_config)

        # Check merged values
        assert (
            merged_config["configurable"]["thread_id"] == "override-thread"
        )  # Override wins
        assert (
            merged_config["configurable"]["user_id"] == "base-user"
        )  # Preserved from base
        assert (
            merged_config["configurable"]["base_param"] == "base-value"
        )  # Preserved from base
        assert (
            merged_config["configurable"]["override_param"] == "override-value"
        )  # Added from override

    def test_merge_engine_configs(self):
        """Test merging engine configs when merging two configs."""
        # Create base config with engine config
        base_config = {
            "configurable": {
                "thread_id": "base-thread",
                "engine_configs": {
                    "engine1": {"param1": "base-value1", "param2": "base-value2"},
                    "engine2": {"param1": "engine2-value"},
                },
            }
        }

        # Create override config with engine config
        override_config = {
            "configurable": {
                "thread_id": "override-thread",
                "engine_configs": {
                    "engine1": {
                        "param1": "override-value1",
                        "param3": "override-value3",
                    },
                    "engine3": {"param1": "engine3-value"},
                },
            }
        }

        # Merge configs
        merged_config = RunnableConfigManager.merge(base_config, override_config)

        # Check engine configs
        engine_configs = merged_config["configurable"]["engine_configs"]

        # engine1 should be merged
        assert "engine1" in engine_configs
        assert engine_configs["engine1"]["param1"] == "override-value1"  # Override wins
        assert (
            engine_configs["engine1"]["param2"] == "base-value2"
        )  # Preserved from base
        assert (
            engine_configs["engine1"]["param3"] == "override-value3"
        )  # Added from override

        # engine2 should be preserved
        assert "engine2" in engine_configs
        assert engine_configs["engine2"]["param1"] == "engine2-value"

        # engine3 should be added
        assert "engine3" in engine_configs
        assert engine_configs["engine3"]["param1"] == "engine3-value"

    def test_extract_value(self):
        """Test extracting values from a config."""
        config = RunnableConfigManager.create(
            thread_id="test-thread", user_id="test-user", custom_param="custom-value"
        )

        # Extract values
        assert RunnableConfigManager.extract_value(config, "thread_id") == "test-thread"
        assert RunnableConfigManager.extract_value(config, "user_id") == "test-user"
        assert (
            RunnableConfigManager.extract_value(config, "custom_param")
            == "custom-value"
        )
        assert RunnableConfigManager.extract_value(config, "non_existent") is None
        assert (
            RunnableConfigManager.extract_value(config, "non_existent", "default")
            == "default"
        )

    def test_get_thread_id(self):
        """Test getting thread_id from a config."""
        thread_id = str(uuid.uuid4())
        config = RunnableConfigManager.create(thread_id=thread_id)

        assert RunnableConfigManager.get_thread_id(config) == thread_id

    def test_get_user_id(self):
        """Test getting user_id from a config."""
        config = RunnableConfigManager.create(user_id="test-user")

        assert RunnableConfigManager.get_user_id(config) == "test-user"

    def test_extract_engine_config(self):
        """Test extracting engine-specific configuration."""
        # Create a config with engine configs
        config = {
            "configurable": {
                "thread_id": "test-thread",
                "engine_configs": {
                    "engine1": {"param1": "value1", "param2": "value2"},
                    "engine2": {"param3": "value3"},
                },
            }
        }

        # Extract engine configs
        engine1_config = RunnableConfigManager.extract_engine_config(config, "engine1")
        assert engine1_config == {"param1": "value1", "param2": "value2"}

        engine2_config = RunnableConfigManager.extract_engine_config(config, "engine2")
        assert engine2_config == {"param3": "value3"}

        # Non-existent engine
        assert RunnableConfigManager.extract_engine_config(config, "non_existent") == {}

    def test_extract_engine_type_config(self):
        """Test extracting configuration for a specific engine type."""
        # Create a config with engine type configs
        config = {
            "configurable": {
                "thread_id": "test-thread",
                "engine_configs": {
                    "llm_config": {"model": "gpt-4", "temperature": 0.7},
                    "retriever_config": {"top_k": 5},
                },
            }
        }

        # Extract engine type configs
        llm_config = RunnableConfigManager.extract_engine_type_config(config, "llm")
        assert llm_config == {"model": "gpt-4", "temperature": 0.7}

        retriever_config = RunnableConfigManager.extract_engine_type_config(
            config, "retriever"
        )
        assert retriever_config == {"top_k": 5}

        # Non-existent engine type
        assert (
            RunnableConfigManager.extract_engine_type_config(config, "non_existent")
            == {}
        )

    def test_add_engine_config(self):
        """Test adding engine-specific configuration."""
        # Create a base config
        config = RunnableConfigManager.create(thread_id="test-thread")

        # Add engine config
        updated_config = RunnableConfigManager.add_engine_config(
            config,
            "test-engine",
            model="gpt-4",
            temperature=0.7,
            custom_param="custom-value",
        )

        # Check updated config
        assert "test-engine" in updated_config["configurable"]["engine_configs"]
        assert (
            updated_config["configurable"]["engine_configs"]["test-engine"]["model"]
            == "gpt-4"
        )
        assert (
            updated_config["configurable"]["engine_configs"]["test-engine"][
                "temperature"
            ]
            == 0.7
        )
        assert (
            updated_config["configurable"]["engine_configs"]["test-engine"][
                "custom_param"
            ]
            == "custom-value"
        )

        # Original config should not be modified
        assert "test-engine" not in config["configurable"]["engine_configs"]

    def test_add_engine(self):
        """Test adding an engine's parameters to the config."""
        # Create a base config
        config = RunnableConfigManager.create(thread_id="test-thread")

        # Create an engine
        engine = MockEngine(
            id="engine-id",
            name="test-engine",
            model_name="gpt-4",
            temperature=0.7,
            special_param="special-value",
        )

        # Add engine
        updated_config = RunnableConfigManager.add_engine(config, engine)

        # Check updated config - should have entries by ID, name, and type
        assert "engine-id" in updated_config["configurable"]["engine_configs"]
        assert "test-engine" in updated_config["configurable"]["engine_configs"]
        assert "llm_config" in updated_config["configurable"]["engine_configs"]

        # Check parameters
        assert (
            updated_config["configurable"]["engine_configs"]["engine-id"]["model_name"]
            == "gpt-4"
        )
        assert (
            updated_config["configurable"]["engine_configs"]["engine-id"]["temperature"]
            == 0.7
        )
        assert (
            updated_config["configurable"]["engine_configs"]["engine-id"][
                "special_param"
            ]
            == "special-value"
        )

    def test_from_dict(self):
        """Test creating a RunnableConfig from a dictionary."""
        # Create a simple dictionary
        input_dict = {
            "thread_id": "test-thread",
            "user_id": "test-user",
            "custom_param": "custom-value",
        }

        # Convert to RunnableConfig
        config = RunnableConfigManager.from_dict(input_dict)

        # Check structure
        assert "configurable" in config
        assert config["configurable"] == input_dict

        # Test with dictionary that already has configurable
        input_dict_with_configurable = {
            "configurable": {"thread_id": "test-thread", "user_id": "test-user"}
        }

        config = RunnableConfigManager.from_dict(input_dict_with_configurable)
        assert config == input_dict_with_configurable

    def test_from_model(self):
        """Test creating a RunnableConfig from a Pydantic model."""
        # Create a Pydantic model instance
        model = TestConfig(
            user_id="test-user", temperature=0.8, custom_setting="test-setting"
        )

        # Convert to RunnableConfig
        config = RunnableConfigManager.from_model(model)

        # Check structure
        assert "configurable" in config
        assert config["configurable"]["user_id"] == "test-user"
        assert config["configurable"]["temperature"] == 0.8
        assert config["configurable"]["custom_setting"] == "test-setting"

    def test_to_model(self):
        """Test converting a RunnableConfig to a Pydantic model."""
        # Create a config
        config = {
            "configurable": {
                "user_id": "test-user",
                "temperature": 0.8,
                "custom_setting": "test-setting",
            }
        }

        # Convert to model
        model = RunnableConfigManager.to_model(config, TestConfig)

        # Check model
        assert isinstance(model, TestConfig)
        assert model.user_id == "test-user"
        assert model.temperature == 0.8
        assert model.custom_setting == "test-setting"
