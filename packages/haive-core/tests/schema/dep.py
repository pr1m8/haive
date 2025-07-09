# tests/core/schema/test_state_schema_manager.py

import logging
from collections.abc import Sequence
from typing import Annotated

import pytest
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from haive.core.schema.schema_manager import StateSchemaManager
from haive.core.schema.state_schema import StateSchema

# Set up logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Test fixtures
@pytest.fixture
def simple_model_class():
    """Create a simple BaseModel class for testing."""

    class SimpleModel(BaseModel):
        name: str
        value: int = 0
        items: list[str] = Field(default_factory=list)
        description: str | None = Field(default=None, description="A description field")

    return SimpleModel


@pytest.fixture
def state_schema_class():
    """Create a StateSchema subclass for testing."""

    class TestState(StateSchema):
        text: str = "default"
        count: int = 0
        flag: bool = False
        messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
            default_factory=list
        )

    TestState.__shared_fields__ = ["count"]
    TestState.__reducer_fields__ = {"messages": add_messages}

    return TestState


@pytest.fixture
def sample_dict():
    """Return a sample dictionary for testing."""
    return {
        "text": "sample text",
        "number": 42,
        "flag": True,
        "nested": {"key": "value"},
    }


@pytest.fixture
def command_sample():
    """Return a sample Command object for testing."""
    return Command(update={"result": "success"}, goto="next_node")


# Tests for StateSchemaManager initialization
class TestStateSchemaManagerInit:

    def test_init_empty(self):
        """Test initializing an empty manager."""
        logger.info("Testing empty initialization")

        manager = StateSchemaManager()
        logger.debug(f"Created manager with name: {manager.name}")

        assert manager.name == "UnnamedSchema"
        assert manager.fields == {}
        assert manager.locked is False

    def test_init_with_name(self):
        """Test initializing with a custom name."""
        logger.info("Testing initialization with name")

        manager = StateSchemaManager(name="CustomSchema")
        logger.debug(f"Created manager with name: {manager.name}")

        assert manager.name == "CustomSchema"

    def test_init_from_dict(self, sample_dict):
        """Test initializing from a dictionary."""
        logger.info("Testing initialization from dict")

        manager = StateSchemaManager(sample_dict, name="DictSchema")
        logger.debug(f"Created manager with fields: {list(manager.fields.keys())}")

        assert "text" in manager.fields
        assert "number" in manager.fields
        assert "flag" in manager.fields
        assert "nested" in manager.fields

        # Check inferred types
        text_type, _ = manager.fields["text"]
        assert text_type == str

        number_type, _ = manager.fields["number"]
        assert number_type == int

        flag_type, _ = manager.fields["flag"]
        assert flag_type == bool

    def test_init_from_model(self, simple_model_class):
        """Test initializing from a BaseModel class."""
        logger.info("Testing initialization from BaseModel class")

        manager = StateSchemaManager(simple_model_class)
        logger.debug(f"Created manager with fields: {list(manager.fields.keys())}")

        assert manager.name == "SimpleModel"
        assert "name" in manager.fields
        assert "value" in manager.fields
        assert "items" in manager.fields
        assert "description" in manager.fields

        # Check description is captured
        assert "description" in manager.field_descriptions

    def test_init_from_state_schema(self, state_schema_class):
        """Test initializing from a StateSchema class."""
        logger.info("Testing initialization from StateSchema class")

        manager = StateSchemaManager(state_schema_class)
        logger.debug(f"Created manager with fields: {list(manager.fields.keys())}")

        assert "text" in manager.fields
        assert "count" in manager.fields
        assert "flag" in manager.fields
        assert "messages" in manager.fields


# Tests for StateSchemaManager field operations
class TestStateSchemaManagerFields:

    def test_add_field_basic(self):
        """Test adding a basic field."""
        logger.info("Testing basic field addition")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("name", str, default="default name")

        logger.debug(f"Added field with type: {manager.fields['name'][0]}")
        assert "name" in manager.fields

        field_type, field_info = manager.fields["name"]
        assert field_type == str
        assert field_info.default == "default name"

    def test_add_field_with_description(self):
        """Test adding a field with description."""
        logger.info("Testing field addition with description")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("count", int, default=0, description="A counter field")

        logger.debug(
            f"Added field with description: {manager.field_descriptions.get('count')}"
        )
        assert "count" in manager.fields
        assert "count" in manager.field_descriptions
        assert manager.field_descriptions["count"] == "A counter field"

    def test_add_field_with_default_factory(self):
        """Test adding a field with a default factory."""
        logger.info("Testing field addition with default_factory")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("items", list[str], default_factory=list)

        logger.debug("Added field with default_factory")
        assert "items" in manager.fields

        # Create model to check default value
        model = manager.get_model()
        instance = model()
        assert instance.items == []

    def test_add_field_with_shared(self):
        """Test adding a shared field."""
        logger.info("Testing field addition with shared=True")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("counter", int, default=0, shared=True)

        logger.debug("Added shared field")
        assert "counter" in manager.fields

        # Check that shared field is tracked
        assert hasattr(manager, "_shared_fields")
        assert "counter" in manager._shared_fields

    def test_add_field_with_reducer(self):
        """Test adding a field with a reducer."""
        logger.info("Testing field addition with reducer")

        def add_numbers(a, b):
            return a + b

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("sum", int, default=0, reducer=add_numbers)

        logger.debug("Added field with reducer")
        assert "sum" in manager.fields

        # Check that reducer is tracked
        assert hasattr(manager, "_reducer_fields")
        assert "sum" in manager._reducer_fields
        assert manager._reducer_fields["sum"] == add_numbers

    def test_add_field_optional(self):
        """Test adding an optional field."""
        logger.info("Testing field addition with optional=True")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("maybe", str, optional=True)

        logger.debug(f"Added optional field with type: {manager.fields['maybe'][0]}")
        assert "maybe" in manager.fields

        field_type, _ = manager.fields["maybe"]
        # Check that the type is Optional[str]
        assert "Optional" in str(field_type)

        # Create model and check default is None
        model = manager.get_model()
        instance = model()
        assert instance.maybe is None

    def test_remove_field(self):
        """Test removing a field."""
        logger.info("Testing field removal")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("field1", str)
        manager.add_field("field2", int)

        logger.debug(f"Initial fields: {list(manager.fields.keys())}")
        assert "field1" in manager.fields
        assert "field2" in manager.fields

        # Remove a field
        manager.remove_field("field1")
        logger.debug(f"Fields after removal: {list(manager.fields.keys())}")

        assert "field1" not in manager.fields
        assert "field2" in manager.fields

    def test_modify_field(self):
        """Test modifying a field."""
        logger.info("Testing field modification")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("count", int, default=0)

        logger.debug(f"Initial field default: {manager.fields['count'][1].default}")
        assert manager.fields["count"][1].default == 0

        # Modify the field
        manager.modify_field("count", new_default=10, new_description="Modified count")

        logger.debug(f"Modified field default: {manager.fields['count'][1].default}")
        logger.debug(
            f"Modified field description: {manager.field_descriptions.get('count')}"
        )

        assert manager.fields["count"][1].default == 10
        assert manager.field_descriptions["count"] == "Modified count"

    def test_has_field(self):
        """Test has_field method."""
        logger.info("Testing has_field method")

        manager = StateSchemaManager(name="TestSchema")
        manager.add_field("existing", str)

        logger.debug(f"Checking existing field: {manager.has_field('existing')}")
        logger.debug(f"Checking nonexistent field: {manager.has_field('nonexistent')}")

        assert manager.has_field("existing") is True
        assert manager.has_field("nonexistent") is False


# Tests for StateSchemaManager merging
class TestStateSchemaManagerMerge:

    def test_merge_with_manager(self):
        """Test merging with another manager."""
        logger.info("Testing merge with another manager")

        manager1 = StateSchemaManager(name="First")
        manager1.add_field("field1", str, default="first")
        manager1.add_field("common", int, default=1)

        manager2 = StateSchemaManager(name="Second")
        manager2.add_field("field2", int, default=2)
        manager2.add_field(
            "common", str, default="second"
        )  # Will be ignored due to first occurrence

        logger.debug(f"Manager1 fields: {list(manager1.fields.keys())}")
        logger.debug(f"Manager2 fields: {list(manager2.fields.keys())}")

        # Merge the managers
        merged = manager1.merge(manager2)
        logger.debug(f"Merged fields: {list(merged.fields.keys())}")

        assert "field1" in merged.fields
        assert "field2" in merged.fields
        assert "common" in merged.fields

        # First occurrence should be preserved
        common_type, common_default = merged.fields["common"]
        assert common_type == int
        assert common_default.default == 1

    def test_merge_with_model(self, simple_model_class):
        """Test merging with a BaseModel class."""
        logger.info("Testing merge with BaseModel class")

        manager = StateSchemaManager(name="Base")
        manager.add_field("extra", bool, default=True)

        logger.debug(f"Initial fields: {list(manager.fields.keys())}")

        # Merge with model class
        merged = manager.merge(simple_model_class)
        logger.debug(f"Merged fields: {list(merged.fields.keys())}")

        assert "extra" in merged.fields
        assert "name" in merged.fields
        assert "value" in merged.fields
        assert "items" in merged.fields
        assert "description" in merged.fields

    def test_merge_with_state_schema(self, state_schema_class):
        """Test merging with a StateSchema class."""
        logger.info("Testing merge with StateSchema class")

        manager = StateSchemaManager(name="Base")
        manager.add_field("extra", bool, default=True)

        logger.debug(f"Initial fields: {list(manager.fields.keys())}")

        # Merge with StateSchema class
        merged = manager.merge(state_schema_class)
        logger.debug(f"Merged fields: {list(merged.fields.keys())}")

        assert "extra" in merged.fields
        assert "text" in merged.fields
        assert "count" in merged.fields
        assert "flag" in merged.fields
        assert "messages" in merged.fields

        # Check that shared fields are merged
        assert hasattr(merged, "_shared_fields")
        assert "count" in merged._shared_fields

        # Check that reducer fields are merged
        assert hasattr(merged, "_reducer_fields")
        assert "messages" in merged._reducer_fields
        assert merged._reducer_fields["messages"] == add_messages


# Tests for StateSchemaManager model creation
class TestStateSchemaManagerModel:

    def test_get_model_basic(self):
        """Test basic model creation."""
        logger.info("Testing basic model creation")

        manager = StateSchemaManager(name="TestModel")
        manager.add_field("name", str, default="test")
        manager.add_field("value", int, default=42)

        logger.debug(f"Creating model from fields: {list(manager.fields.keys())}")
        model_cls = manager.get_model()

        logger.debug(f"Created model class: {model_cls.__name__}")
        assert model_cls.__name__ == "TestModel"

        # Create an instance
        instance = model_cls()
        logger.debug(f"Model instance: {instance.model_dump()}")

        assert instance.name == "test"
        assert instance.value == 42

    def test_get_model_as_state_schema(self):
        """Test creating a model as StateSchema."""
        logger.info("Testing model creation as StateSchema")

        manager = StateSchemaManager(name="StateTest")
        manager.add_field("text", str, default="test")
        manager.add_field("shared_field", int, default=0, shared=True)

        # Add a reducer
        def add_numbers(a, b):
            return a + b

        manager.add_field("sum", int, default=0, reducer=add_numbers)

        logger.debug("Creating StateSchema model")
        model_cls = manager.get_model(as_state_schema=True)

        # Check it's a StateSchema
        assert issubclass(model_cls, StateSchema)

        # Check shared fields are set
        logger.debug(f"Model shared fields: {model_cls.__shared_fields__}")
        assert "shared_field" in model_cls.__shared_fields__

        # Check reducer fields are set
        logger.debug(f"Model reducer fields: {model_cls.__reducer_fields__}")
        assert "sum" in model_cls.__reducer_fields__

        # Create instance and check method availability
        instance = model_cls()
        assert hasattr(instance, "update")
        assert hasattr(instance, "to_dict")

    def test_get_model_not_state_schema(self):
        """Test creating a model not as StateSchema."""
        logger.info("Testing model creation not as StateSchema")

        manager = StateSchemaManager(name="PlainModel")
        manager.add_field("field", str, default="test")

        logger.debug("Creating plain BaseModel")
        model_cls = manager.get_model(as_state_schema=False)

        # Check it's not a StateSchema
        assert not issubclass(model_cls, StateSchema)
        assert issubclass(model_cls, BaseModel)

        # Create instance and check method availability
        instance = model_cls()
        assert not hasattr(instance, "update")
        assert not hasattr(instance, "to_dict")

    def test_get_model_with_lock(self):
        """Test creating a model with lock."""
        logger.info("Testing model creation with lock")

        manager = StateSchemaManager(name="LockedModel")
        manager.add_field("field", str, default="test")

        assert manager.locked is False

        logger.debug("Creating model with lock=True")
        manager.get_model(lock=True)

        # Check it's locked
        assert manager.locked is True

        # Try to add a field - should raise an error
        with pytest.raises(ValueError) as excinfo:
            manager.add_field("another", int)

        logger.debug(f"Expected error: {excinfo.value}")
        assert "locked" in str(excinfo.value)

    def test_get_model_with_computed_property(self):
        """Test creating a model with computed property."""
        logger.info("Testing model creation with computed property")

        manager = StateSchemaManager(name="PropertyModel")
        manager.add_field("first_name", str, default="John")
        manager.add_field("last_name", str, default="Doe")

        # Add a computed property
        def get_full_name(self):
            return f"{self.first_name} {self.last_name}"

        def set_full_name(self, value):
            parts = value.split()
            if len(parts) >= 2:
                self.first_name = parts[0]
                self.last_name = " ".join(parts[1:])

        manager.add_computed_property("full_name", get_full_name, set_full_name)

        logger.debug("Creating model with computed property")
        model_cls = manager.get_model()

        # Create instance and check property
        instance = model_cls()
        logger.debug(f"Instance property value: {instance.full_name}")

        assert instance.full_name == "John Doe"

        # Test setter
        instance.full_name = "Jane Smith"
        logger.debug(
            f"After setting property: {instance.first_name} {instance.last_name}"
        )

        assert instance.first_name == "Jane"
        assert instance.last_name == "Smith"


# Tests for node creation and command helpers
class TestNodeAndCommand:

    def test_create_command(self):
        """Test creating a Command object."""
        logger.info("Testing create_command")

        manager = StateSchemaManager()
        command = manager.create_command(update={"result": "success"}, goto="next_node")

        logger.debug(f"Created command: {command}")
        assert isinstance(command, Command)
        assert command.update == {"result": "success"}
        assert command.goto == "next_node"

    def test_create_send(self):
        """Test creating a Send object."""
        logger.info("Testing create_send")

        manager = StateSchemaManager()
        send = manager.create_send("target_node", {"input": "value"})

        logger.debug(f"Created send: {send}")
        assert isinstance(send, Send)
        assert send.node == "target_node"
        assert send.arg == {"input": "value"}

    def test_create_node_function(self):
        """Test creating a node function with validation."""
        logger.info("Testing create_node_function")

        # Create a manager with a schema
        manager = StateSchemaManager(name="NodeSchema")
        manager.add_field("input", str, default="")
        manager.add_field("count", int, default=0)

        # Create a simple node function
        def my_node(state):
            return {"input": f"processed: {state.input}", "count": state.count + 1}

        # Wrap with validation
        node_func = manager.create_node_function(my_node, command_goto="next")

        # Call the node function
        test_state = {"input": "test", "count": 5}
        result = node_func(test_state)

        logger.debug(f"Node function result: {result}")
        assert isinstance(result, Command)
        assert result.update["input"] == "processed: test"
        assert result.update["count"] == 6
        assert result.goto == "next"

        # Test with invalid input to check validation
        invalid_state = {"invalid": "field"}
        with pytest.raises(Exception):
            node_func(invalid_state)


# Test for pretty_print
def test_pretty_print(capfd, simple_model_class):
    """Test pretty_print method."""
    logger.info("Testing pretty_print")

    manager = StateSchemaManager(simple_model_class)
    manager.add_field("extra", bool, default=True, description="An extra field")

    # Add a property
    def get_sample(self):
        return "sample value"

    manager.add_computed_property("sample", get_sample)

    # Call pretty_print
    manager.pretty_print()

    # Capture the printed output
    out, _ = capfd.readouterr()
    logger.debug(f"Pretty print output length: {len(out)}")

    # Check for key elements in the output
    assert "class SimpleModel(StateSchema):" in out
    assert "name: str" in out
    assert "value: int = 0" in out
    assert "items: List[str]" in out
    assert "# An extra field" in out
    assert "extra: bool = True" in out
    assert "@property" in out
    assert "def sample(self): ...  # Computed property" in out


if __name__ == "__main__":
    pytest.main(["-v"])
