"""
Debug the validation node V2 setup and tool routing.
"""

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression, {"__builtins__": {}}, {})

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

def debug_validation_node_v2():
    """Debug how V2 validation nodes handle tool routing."""
    print("=== DEBUG: Validation Node V2 Tool Routing ===\n")
    
    # Create agent with initial tool
    engine = AugLLMConfig(
        tools=[calculate],
        system_message="You are a helpful assistant."
    )
    agent = SimpleAgent(name="test_agent", engine=engine)
    
    print("1. Agent setup:")
    print(f"   Agent type: {type(agent)}")
    print(f"   Engine type: {type(agent.engine)}")
    print(f"   Engine tool routes: {agent.engine.tool_routes}")
    
    # Build graph and examine nodes
    graph = agent.build_graph()
    
    print("\n2. Graph structure:")
    print(f"   Nodes: {list(graph.nodes.keys())}")
    
    # Look at each node
    for node_name, node in graph.nodes.items():
        print(f"\n   Node '{node_name}':")
        print(f"     Type: {type(node)}")
        print(f"     Node type: {getattr(node, 'node_type', 'N/A')}")
        
        # Check if it has a config
        if hasattr(node, 'config'):
            config = node.config
            print(f"     Config type: {type(config)}")
            if hasattr(config, 'tool_routes'):
                print(f"     Tool routes in config: {config.tool_routes}")
        
        # Check metadata
        if hasattr(node, 'metadata'):
            metadata = node.metadata
            print(f"     Metadata: {metadata}")
            if 'callable' in metadata:
                callable_func = metadata['callable']
                print(f"     Callable type: {type(callable_func)}")
    
    # Check if we can create a ValidationNodeConfigV2 directly
    print("\n3. Creating ValidationNodeConfigV2 directly:")
    try:
        validation_config = ValidationNodeConfigV2(
            name="test_validation",
            tool_routes=agent.engine.tool_routes
        )
        print(f"   Config created: {validation_config}")
        print(f"   Config tool routes: {validation_config.tool_routes}")
        
        # Try to call the validation node
        validation_node = validation_config.create_runnable()
        print(f"   Validation node callable: {validation_node}")
        
    except Exception as e:
        print(f"   Error creating validation config: {e}")
    
    # Add a tool and rebuild
    print("\n4. Adding search tool and rebuilding:")
    engine.add_tool(search)
    print(f"   Engine tool routes after addition: {engine.tool_routes}")
    
    new_graph = agent.build_graph()
    
    # Check validation node again
    if 'validation' in new_graph.nodes:
        validation_node = new_graph.nodes['validation']
        print(f"   New validation node type: {type(validation_node)}")
        
        if hasattr(validation_node, 'config'):
            config = validation_node.config
            print(f"   New config type: {type(config)}")
            if hasattr(config, 'tool_routes'):
                print(f"   New tool routes in config: {config.tool_routes}")
    
    # Test tool call processing
    print("\n5. Testing tool call processing:")
    
    # Create mock state with tool call
    mock_state = {
        'messages': [
            HumanMessage(content="Calculate 2+2"),
            AIMessage(content="I'll calculate that.", tool_calls=[
                {
                    'name': 'calculate',
                    'args': {'expression': '2+2'},
                    'id': 'test_call_1'
                }
            ])
        ],
        'tool_routes': engine.tool_routes  # Add tool routes to state
    }
    
    # Try to process with validation node
    if 'validation' in new_graph.nodes:
        validation_node = new_graph.nodes['validation']
        
        # Get the actual callable
        if hasattr(validation_node, 'metadata') and 'callable' in validation_node.metadata:
            callable_func = validation_node.metadata['callable']
            print(f"   Calling validation function: {callable_func}")
            
            try:
                result = callable_func(mock_state)
                print(f"   Validation result: {result}")
            except Exception as e:
                print(f"   Error calling validation: {e}")
    
    # Test with search tool call
    print("\n6. Testing search tool call:")
    
    search_state = {
        'messages': [
            HumanMessage(content="Search for information"),
            AIMessage(content="I'll search for that.", tool_calls=[
                {
                    'name': 'search',
                    'args': {'query': 'test query'},
                    'id': 'test_call_2'
                }
            ])
        ],
        'tool_routes': engine.tool_routes
    }
    
    if 'validation' in new_graph.nodes:
        validation_node = new_graph.nodes['validation']
        
        if hasattr(validation_node, 'metadata') and 'callable' in validation_node.metadata:
            callable_func = validation_node.metadata['callable']
            
            try:
                result = callable_func(search_state)
                print(f"   Search validation result: {result}")
            except Exception as e:
                print(f"   Error calling validation with search: {e}")

if __name__ == "__main__":
    debug_validation_node_v2()