# test_node_diagnostic.py
import logging

from rich.console import Console
from rich.panel import Panel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
console = Console()

# Display header
console.print(Panel("Node System Diagnostic", expand=False))

# Test registry
from haive.core.graph.node.registry import NodeTypeRegistry

registry = NodeTypeRegistry.get_instance()
registry.register_default_processors()

console.print("Registered processors:")
for processor_type, processor in registry.node_processors.items():
    console.print(f"  {processor_type}: {processor.__class__.__name__}")

from langgraph.graph import END

# Create basic test components
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory


# Create a simple test function
def test_function(input_data):
    return {"processed": f"Processed: {input_data}"}


# Create node config
node_config = NodeConfig(
    name="test_node", engine=test_function, command_goto=END, debug=True
)

# Create node function
node_func = NodeFactory.create_node_function(node_config)

# Test the node
result = node_func("test input")
console.print("\nTest result:")
console.print(result)

# Check if Command pattern worked correctly
if hasattr(result, "update"):
    console.print("\nCommand update attribute:")
    console.print(result.update)

if hasattr(result, "goto"):
    console.print("\nCommand goto attribute:")
    console.print(result.goto)
