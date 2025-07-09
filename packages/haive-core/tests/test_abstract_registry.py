# tests/test_registry.py

import logging
import os
import sys
from typing import Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the registry components
from haive.core.registry.registy import (
    AbstractRegistry,
    register_graph,
    register_node,
    register_schema,
    register_tool,
    registry_manager,
)


# Test basic registry functionality
def test_basic_registry():
    """Test basic registry operations."""
    print("\n=== Testing Basic Registry Operations ===")

    # Create a new registry
    registry = AbstractRegistry[str, Any](
        name="test_registry", description="Registry for testing"
    )

    # Register some items
    registry.register("item1", "Value 1", tags=["test", "example"])
    registry.register("item2", {"name": "Value 2"}, tags=["test", "dict"])
    registry.register(
        "item3",
        lambda x: x * 2,
        tags=["function"],
        metadata={"description": "Doubles input"},
    )

    # Verify registration
    assert registry.has("item1")
    assert registry.has("item2")
    assert registry.has("item3")

    # Get items
    assert registry.get("item1") == "Value 1"
    assert registry.get("item2")["name"] == "Value 2"
    assert registry.get("item3")(5) == 10

    # Get by tag
    tag_results = registry.get_by_tag("test")
    print(f"Items with 'test' tag: {list(tag_results.keys())}")
    assert len(tag_results) == 2
    assert "item1" in tag_results
    assert "item2" in tag_results

    # Get by multiple tags
    multi_tag = registry.get_by_tags(["test", "dict"])
    print(f"Items with 'test' OR 'dict' tags: {list(multi_tag.keys())}")
    assert len(multi_tag) == 2

    # With require_all=True
    strict_tag = registry.get_by_tags(["test", "dict"], require_all=True)
    print(f"Items with 'test' AND 'dict' tags: {list(strict_tag.keys())}")
    assert len(strict_tag) == 1
    assert "item2" in strict_tag

    # Get metadata
    metadata = registry.get_metadata("item3")
    print(f"Metadata for item3: {metadata}")
    assert metadata["description"] == "Doubles input"

    # Update an item
    registry.update(
        "item1",
        "Updated Value 1",
        update_metadata={"updated": True},
        add_tags=["updated"],
        remove_tags=["example"],
    )

    # Verify update
    assert registry.get("item1") == "Updated Value 1"
    assert registry.get_metadata("item1")["updated"] == True
    updated_tags = registry.get_by_tag("updated")
    assert "item1" in updated_tags
    example_tags = registry.get_by_tag("example")
    assert "item1" not in example_tags

    # Remove an item
    removed = registry.remove("item2")
    print(f"Removed item2: {removed}")
    assert not registry.has("item2")

    # Item description
    description = registry.describe("item3")
    print(f"Description of item3:\n{description}")

    # Statistics
    stats = registry.get_statistics()
    print(f"Registry statistics: {stats}")

    return registry


# Test dependencies
def test_registry_dependencies():
    """Test registry dependency tracking."""
    print("\n=== Testing Registry Dependencies ===")

    registry = AbstractRegistry[str, Any](name="dependency_test")

    # Register items with dependencies
    registry.register("base", "Base item")
    registry.register("dependent1", "Depends on base", dependencies=["base"])
    registry.register("dependent2", "Depends on base", dependencies=["base"])
    registry.register("nested", "Depends on dependent1", dependencies=["dependent1"])

    # Check dependencies
    base_deps = registry.get_dependencies("base")
    print(f"Dependencies of 'base': {base_deps}")
    assert len(base_deps) == 0

    dep1_deps = registry.get_dependencies("dependent1")
    print(f"Dependencies of 'dependent1': {dep1_deps}")
    assert "base" in dep1_deps

    # Check dependents
    base_dependents = registry.get_dependents("base")
    print(f"Dependents of 'base': {base_dependents}")
    assert "dependent1" in base_dependents
    assert "dependent2" in base_dependents

    dep1_dependents = registry.get_dependents("dependent1")
    print(f"Dependents of 'dependent1': {dep1_dependents}")
    assert "nested" in dep1_dependents

    # Try removing with dependents
    registry.remove("base")  # This should log a warning about dependents

    return registry


# Test registry decorator
def test_registry_decorator():
    """Test registry decorator functionality."""
    print("\n=== Testing Registry Decorators ===")

    registry = AbstractRegistry[str, Any](name="decorator_test")

    # Create a decorator
    register = registry.register_decorator(tags=["function"])

    # Use the decorator
    @register
    def add_numbers(a, b):
        """Add two numbers together."""
        return a + b

    @register
    def multiply_numbers(a, b):
        """Multiply two numbers."""
        return a * b

    # Verify registration
    assert registry.has("add_numbers")
    assert registry.has("multiply_numbers")

    # Test functions
    assert registry.get("add_numbers")(3, 4) == 7
    assert registry.get("multiply_numbers")(3, 4) == 12

    # Get by tag
    functions = registry.get_by_tag("function")
    print(f"Registered functions: {list(functions.keys())}")
    assert len(functions) == 2

    # Test function introspection
    add_desc = registry.describe("add_numbers")
    print(f"Function description:\n{add_desc}")
    assert "parameters" in add_desc["item_info"]
    assert "doc" in add_desc["item_info"]

    return registry


# Test specialized registries
def test_specialized_registries():
    """Test the specialized registry types."""
    print("\n=== Testing Specialized Registries ===")

    # Test tool registry
    @register_tool("calculator", tags=["math"])
    def calculator(expression):
        """Evaluate a mathematical expression."""
        return eval(expression)

    # Test schema registry
    @register_schema("user_schema", tags=["user"])
    class UserSchema:
        """Schema for user data."""

        def __init__(self):
            self.fields = {"name": str, "email": str, "age": int}

    # Test node registry
    @register_node("process_node", tags=["process"])
    def process_data(state):
        """Process data in a graph node."""
        return {"processed": True}

    # Test graph registry
    @register_graph("linear_workflow", tags=["workflow"])
    def create_linear_workflow():
        """Create a linear workflow graph."""
        return ["node1", "node2", "node3"]

    # Verify registrations
    print(
        f"Tool registry items: {list(registry_manager.get_registry('tools').get_all().keys())}"
    )
    print(
        f"Schema registry items: {list(registry_manager.get_registry('schemas').get_all().keys())}"
    )
    print(
        f"Node registry items: {list(registry_manager.get_registry('nodes').get_all().keys())}"
    )
    print(
        f"Graph registry items: {list(registry_manager.get_registry('graphs').get_all().keys())}"
    )

    # Test registry manager
    all_registries = registry_manager.list_registries()
    print(f"Available registries: {all_registries}")

    # Get items from registries
    calculator_fn = registry_manager.get_registry("tools").get("calculator")
    assert calculator_fn("2 + 3 * 4") == 14

    # Get tags
    workflow_items = registry_manager.get_registry("graphs").get_by_tag("workflow")
    assert "linear_workflow" in workflow_items

    return registry_manager


# Test registry events with listeners
def test_registry_events():
    """Test registry event listeners."""
    print("\n=== Testing Registry Events ===")

    registry = AbstractRegistry[str, Any](name="event_test")
    events = []

    # Add a listener
    def event_listener(event_type, key, item):
        events.append((event_type, key))
        print(f"Event: {event_type} - {key}")

    registry.add_listener(event_listener)

    # Perform operations
    registry.register("item1", "Test item")
    registry.update("item1", "Updated item")
    registry.remove("item1")

    # Check events
    print(f"Recorded events: {events}")
    assert len(events) == 3
    assert events[0][0] == "register"
    assert events[1][0] == "update"
    assert events[2][0] == "remove"

    # Remove listener
    registry.remove_listener(event_listener)

    # Perform another operation (should not be recorded)
    registry.register("item2", "Another item")
    assert len(events) == 3  # Still 3 events, not 4

    return registry


if __name__ == "__main__":
    # Run all tests
    basic_registry = test_basic_registry()
    dependency_registry = test_registry_dependencies()
    decorator_registry = test_registry_decorator()
    specialized_registries = test_specialized_registries()
    event_registry = test_registry_events()

    print("\n=== All registry tests completed successfully ===")
