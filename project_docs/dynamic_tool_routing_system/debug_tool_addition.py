"""
Debug script to understand tool addition and graph rebuilding.
"""

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
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

@tool
def analyze(data: str) -> str:
    """Analyze data."""
    return f"Analysis of: {data}"

def debug_tool_addition():
    """Debug tool addition to SimpleAgent."""
    print("=== DEBUG: Tool Addition to SimpleAgent ===\n")
    
    # Create initial engine with one tool
    engine = AugLLMConfig(
        tools=[calculate],
        system_message="You are a helpful assistant."
    )
    
    # Create agent
    agent = SimpleAgent(name="test_agent", engine=engine)
    
    print("1. Initial state:")
    print(f"   Engine tools: {list(engine.tools) if hasattr(engine, 'tools') else 'N/A'}")
    print(f"   Tool routes: {engine.tool_routes if hasattr(engine, 'tool_routes') else 'N/A'}")
    
    # Build initial graph
    print("\n2. Building initial graph...")
    initial_graph = agent.build_graph()
    print(f"   Initial graph nodes: {list(initial_graph.nodes.keys()) if hasattr(initial_graph, 'nodes') else 'N/A'}")
    
    # Add a tool dynamically
    print("\n3. Adding 'search' tool...")
    if hasattr(engine, 'add_tool'):
        engine.add_tool(search)
        print("   Tool added to engine")
    else:
        print("   Engine doesn't have add_tool method")
    
    print(f"   Engine tools after addition: {list(engine.tools) if hasattr(engine, 'tools') else 'N/A'}")
    print(f"   Tool routes after addition: {engine.tool_routes if hasattr(engine, 'tool_routes') else 'N/A'}")
    
    # Rebuild graph
    print("\n4. Rebuilding graph...")
    new_graph = agent.build_graph()
    print(f"   New graph nodes: {list(new_graph.nodes.keys()) if hasattr(new_graph, 'nodes') else 'N/A'}")
    
    # Check if nodes changed
    initial_nodes = set(initial_graph.nodes.keys()) if hasattr(initial_graph, 'nodes') else set()
    new_nodes = set(new_graph.nodes.keys()) if hasattr(new_graph, 'nodes') else set()
    
    print(f"\n5. Graph comparison:")
    print(f"   Nodes added: {new_nodes - initial_nodes}")
    print(f"   Nodes removed: {initial_nodes - new_nodes}")
    print(f"   Nodes unchanged: {initial_nodes & new_nodes}")
    
    # Add another tool
    print("\n6. Adding 'analyze' tool...")
    if hasattr(engine, 'add_tool'):
        engine.add_tool(analyze)
        print("   Tool added to engine")
    
    print(f"   Tool routes after second addition: {engine.tool_routes if hasattr(engine, 'tool_routes') else 'N/A'}")
    
    # Final rebuild
    print("\n7. Final rebuild...")
    final_graph = agent.build_graph()
    print(f"   Final graph nodes: {list(final_graph.nodes.keys()) if hasattr(final_graph, 'nodes') else 'N/A'}")
    
    # Check engine structure
    print(f"\n8. Engine structure:")
    print(f"   Engine type: {type(engine)}")
    print(f"   Engine dir: {[attr for attr in dir(engine) if not attr.startswith('_')]}")
    
    # Check if tools are in the right place
    if hasattr(engine, 'tools'):
        print(f"   Tools in engine.tools: {[t.name for t in engine.tools]}")
    
    if hasattr(engine, 'tool_routes'):
        print(f"   Tool routes: {engine.tool_routes}")

if __name__ == "__main__":
    debug_tool_addition()