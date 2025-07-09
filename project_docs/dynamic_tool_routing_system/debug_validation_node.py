"""
Debug the validation node to understand how it handles tool routing.
"""

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
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

def debug_validation_node():
    """Debug how validation node handles tool routing."""
    print("=== DEBUG: Validation Node Tool Routing ===\n")
    
    # Create agent with initial tool
    engine = AugLLMConfig(
        tools=[calculate],
        system_message="You are a helpful assistant."
    )
    agent = SimpleAgent(name="test_agent", engine=engine)
    
    # Build graph and get validation node
    graph = agent.build_graph()
    
    print("1. Graph structure:")
    print(f"   Nodes: {list(graph.nodes.keys())}")
    
    # Find validation node
    validation_node = None
    for node_name, node in graph.nodes.items():
        if node_name == 'validation':
            validation_node = node
            break
    
    if validation_node:
        print(f"   Validation node type: {type(validation_node)}")
        print(f"   Validation node: {validation_node}")
        
        # Check if it has config
        if hasattr(validation_node, 'config'):
            print(f"   Validation config: {validation_node.config}")
        
        # Check if it has metadata
        if hasattr(validation_node, 'metadata'):
            print(f"   Validation metadata: {validation_node.metadata}")
    
    # Add a tool and rebuild
    print("\n2. Adding search tool...")
    engine.add_tool(search)
    new_graph = agent.build_graph()
    
    new_validation_node = None
    for node_name, node in new_graph.nodes.items():
        if node_name == 'validation':
            new_validation_node = node
            break
    
    if new_validation_node:
        print(f"   New validation node type: {type(new_validation_node)}")
        
        # Check if the validation node changed
        print(f"   Same validation node? {validation_node is new_validation_node}")
        
        # Check tool routes in validation node
        if hasattr(new_validation_node, 'config'):
            config = new_validation_node.config
            if hasattr(config, 'tool_routes'):
                print(f"   Tool routes in validation config: {config.tool_routes}")
        
        # Check if validation node has access to engine tool routes
        if hasattr(new_validation_node, 'metadata'):
            metadata = new_validation_node.metadata
            if 'tool_routes' in metadata:
                print(f"   Tool routes in validation metadata: {metadata['tool_routes']}")
    
    # Test with a mock tool call
    print("\n3. Testing tool call routing...")
    
    # Create a mock state with tool call
    mock_state = {
        'messages': [
            HumanMessage(content="Calculate 2+2"),
            AIMessage(content="I'll help you calculate that.", tool_calls=[
                {
                    'name': 'calculate',
                    'args': {'expression': '2+2'},
                    'id': 'test_call_1'
                }
            ])
        ]
    }
    
    print(f"   Mock state: {mock_state}")
    
    # Try to call validation node
    try:
        if callable(new_validation_node):
            result = new_validation_node(mock_state)
            print(f"   Validation result: {result}")
        else:
            print("   Validation node is not callable")
    except Exception as e:
        print(f"   Error calling validation node: {e}")
    
    # Test with search tool call
    print("\n4. Testing search tool call...")
    
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
        ]
    }
    
    try:
        if callable(new_validation_node):
            result = new_validation_node(search_state)
            print(f"   Search validation result: {result}")
        else:
            print("   Validation node is not callable")
    except Exception as e:
        print(f"   Error calling validation node with search: {e}")

if __name__ == "__main__":
    debug_validation_node()