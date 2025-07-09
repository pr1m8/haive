"""
Test unified validation node with Command/Send routing and dynamic tool addition.

This tests the unified validation approach that combines validation and routing
in one step, avoiding the artificial separation of the original ValidationNodeV2.
"""

import sys
import os
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')

from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command, Send

from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.node.unified_validation_node import UnifiedValidationNodeConfig

# ============================================================================
# TEST TOOLS AND MODELS
# ============================================================================

@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression, {"__builtins__": {}}, {})

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

@tool
def analyze_data(data: str) -> str:
    """Analyze data and return insights."""
    return f"Analysis of: {data}"

class UserQuery(BaseModel):
    """Structured user query model."""
    question: str = Field(description="The user's question")
    category: str = Field(description="Category of the question")
    priority: int = Field(description="Priority level 1-5")

class SearchRequest(BaseModel):
    """Structured search request model."""
    query: str = Field(description="Search query")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Search filters")
    max_results: int = Field(default=10, description="Maximum number of results")

# ============================================================================
# RECOMPILABLE AGENT WITH UNIFIED VALIDATION
# ============================================================================

class RecompilableAgentWithUnifiedValidation:
    """
    Agent wrapper that uses unified validation and tracks recompilation needs.
    """
    
    def __init__(self, base_agent, name: str):
        self.base_agent = base_agent
        self.name = name
        self.tool_route_hash = None
        self.last_recompiled = None
        self.recompilation_needed = False
        
        # Track initial state
        self._update_tool_route_hash()
    
    def _update_tool_route_hash(self):
        """Update the hash of current tool routes."""
        import hashlib
        if hasattr(self.base_agent.engine, 'tool_routes'):
            route_str = str(sorted(self.base_agent.engine.tool_routes.items()))
            self.tool_route_hash = hashlib.md5(route_str.encode()).hexdigest()
    
    def needs_recompilation(self) -> bool:
        """Check if agent needs recompilation."""
        current_hash = self._compute_current_hash()
        return current_hash != self.tool_route_hash
    
    def _compute_current_hash(self) -> str:
        """Compute current hash of tool routes."""
        import hashlib
        if hasattr(self.base_agent.engine, 'tool_routes'):
            route_str = str(sorted(self.base_agent.engine.tool_routes.items()))
            return hashlib.md5(route_str.encode()).hexdigest()
        return ""
    
    def add_tool_dynamically(self, tool, route: str = "langchain_tool"):
        """Add tool and mark for recompilation."""
        print(f"Adding tool {tool.name} to agent {self.name}")
        
        # Add to engine
        if hasattr(self.base_agent.engine, 'add_tool'):
            self.base_agent.engine.add_tool(tool, route)
            print(f"Tool routes now: {self.base_agent.engine.tool_routes}")
            
        # Mark for recompilation
        self.recompilation_needed = True
    
    def build_graph_with_unified_validation(self) -> BaseGraph:
        """Build graph using unified validation node."""
        graph = BaseGraph(name=f"{self.name}_graph")
        
        # Create unified validation node
        validation_node = UnifiedValidationNodeConfig(
            name="unified_validation",
            engine_name="main_engine",
            parallel_execution=True,
            create_tool_messages=True
        )
        
        # Add nodes
        graph.add_node("agent_node", self.base_agent.create_runnable())
        graph.add_node("unified_validation", validation_node)
        graph.add_node("tool_node", self._create_tool_executor())
        graph.add_node("parse_output", self._create_output_parser())
        
        # Add edges
        graph.add_edge("__start__", "agent_node")
        graph.add_edge("agent_node", "unified_validation")
        graph.add_edge("tool_node", "agent_node")
        graph.add_edge("parse_output", "agent_node")
        
        return graph
    
    def _create_tool_executor(self):
        """Create tool execution function."""
        def tool_executor(state: Dict[str, Any]) -> Dict[str, Any]:
            """Execute langchain tools."""
            print(f"Tool executor called with state keys: {list(state.keys())}")
            
            # Get tool call info
            tool_call = state.get("tool_call", {})
            tool_name = tool_call.get("name", "")
            tool_args = tool_call.get("args", {})
            
            print(f"Executing tool: {tool_name} with args: {tool_args}")
            
            # Find and execute tool
            if hasattr(self.base_agent.engine, 'tools'):
                for tool in self.base_agent.engine.tools:
                    if hasattr(tool, 'name') and tool.name == tool_name:
                        try:
                            result = tool.invoke(tool_args)
                            return {"tool_result": result}
                        except Exception as e:
                            return {"tool_error": str(e)}
            
            return {"tool_error": f"Tool {tool_name} not found"}
        
        return tool_executor
    
    def _create_output_parser(self):
        """Create output parsing function."""
        def output_parser(state: Dict[str, Any]) -> Dict[str, Any]:
            """Parse structured output."""
            print(f"Output parser called with state keys: {list(state.keys())}")
            
            # Get tool call info
            tool_call = state.get("tool_call", {})
            tool_name = tool_call.get("name", "")
            
            print(f"Parsing output for model: {tool_name}")
            
            return {"parsed_output": f"Parsed {tool_name}"}
        
        return output_parser
    
    def recompile_if_needed(self):
        """Recompile if needed."""
        if self.needs_recompilation():
            print(f"Recompiling agent {self.name}")
            self.graph = self.build_graph_with_unified_validation()
            self._update_tool_route_hash()
            self.last_recompiled = datetime.now()
            self.recompilation_needed = False
            return True
        return False

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_unified_validation_simple_agent():
    """Test unified validation with SimpleAgent."""
    print("=== Testing Unified Validation with SimpleAgent ===\n")
    
    # Create engine with initial tools
    engine = AugLLMConfig(
        tools=[calculate],
        structured_output_model=UserQuery,
        structured_output_version="v2",
        system_message="You are a helpful assistant."
    )
    
    # Create agent
    simple_agent = SimpleAgent(name="simple_agent", engine=engine)
    
    # Wrap with recompilable functionality
    recompilable_agent = RecompilableAgentWithUnifiedValidation(simple_agent, "simple_agent")
    
    print("1. Initial state:")
    print(f"   Tool routes: {engine.tool_routes}")
    print(f"   Needs recompilation: {recompilable_agent.needs_recompilation()}")
    
    # Build initial graph
    graph = recompilable_agent.build_graph_with_unified_validation()
    print(f"   Graph nodes: {list(graph.nodes.keys())}")
    
    # Add tool dynamically
    print("\n2. Adding search_web tool...")
    recompilable_agent.add_tool_dynamically(search_web, "langchain_tool")
    print(f"   Tool routes after addition: {engine.tool_routes}")
    print(f"   Needs recompilation: {recompilable_agent.needs_recompilation()}")
    
    # Recompile
    print("\n3. Recompiling...")
    was_recompiled = recompilable_agent.recompile_if_needed()
    print(f"   Was recompiled: {was_recompiled}")
    print(f"   Needs recompilation: {recompilable_agent.needs_recompilation()}")
    
    # Test validation node directly
    print("\n4. Testing unified validation node...")
    validation_node = UnifiedValidationNodeConfig(
        name="test_validation",
        engine_name="main_engine",
        parallel_execution=True
    )
    
    # Create test state with tool calls
    test_state = {
        "messages": [
            HumanMessage(content="Calculate 2+2"),
            AIMessage(content="I'll calculate that for you.", tool_calls=[
                {
                    "name": "calculate",
                    "args": {"expression": "2+2"},
                    "id": "call_1"
                }
            ])
        ],
        "main_engine": engine
    }
    
    # Test validation
    validator = validation_node.create_runnable()
    result = validator(test_state)
    
    print(f"   Validation result type: {type(result)}")
    print(f"   Validation result: {result}")
    
    return recompilable_agent

def test_unified_validation_react_agent():
    """Test unified validation with ReactAgent."""
    print("\n=== Testing Unified Validation with ReactAgent ===\n")
    
    # Create engine with tools and structured output
    engine = AugLLMConfig(
        tools=[search_web, analyze_data],
        structured_output_model=SearchRequest,
        structured_output_version="v2",
        system_message="You are a research assistant."
    )
    
    # Create agent
    react_agent = ReactAgent(name="react_agent", engine=engine)
    
    # Wrap with recompilable functionality
    recompilable_agent = RecompilableAgentWithUnifiedValidation(react_agent, "react_agent")
    
    print("1. Initial state:")
    print(f"   Tool routes: {engine.tool_routes}")
    print(f"   Needs recompilation: {recompilable_agent.needs_recompilation()}")
    
    # Add multiple tools
    print("\n2. Adding multiple tools...")
    recompilable_agent.add_tool_dynamically(calculate, "langchain_tool")
    print(f"   Tool routes: {engine.tool_routes}")
    
    # Test with structured output
    print("\n3. Testing with structured output...")
    test_state = {
        "messages": [
            HumanMessage(content="Search for information about AI"),
            AIMessage(content="I'll search for that.", tool_calls=[
                {
                    "name": "SearchRequest",
                    "args": {
                        "query": "artificial intelligence",
                        "filters": {"category": "technology"},
                        "max_results": 5
                    },
                    "id": "call_1"
                }
            ])
        ],
        "main_engine": engine
    }
    
    validation_node = UnifiedValidationNodeConfig(
        name="test_validation",
        engine_name="main_engine",
        parallel_execution=True
    )
    
    validator = validation_node.create_runnable()
    result = validator(test_state)
    
    print(f"   Validation result: {result}")
    
    return recompilable_agent

def test_command_send_routing():
    """Test Command and Send routing patterns."""
    print("\n=== Testing Command/Send Routing Patterns ===\n")
    
    # Create engine with mixed tools
    engine = AugLLMConfig(
        tools=[calculate, search_web, analyze_data],
        structured_output_model=UserQuery,
        structured_output_version="v2",
        system_message="You are a multi-purpose assistant."
    )
    
    # Test state with multiple tool calls
    test_state = {
        "messages": [
            HumanMessage(content="Calculate 2+2 and search for AI info"),
            AIMessage(content="I'll do both tasks.", tool_calls=[
                {
                    "name": "calculate",
                    "args": {"expression": "2+2"},
                    "id": "call_1"
                },
                {
                    "name": "search_web",
                    "args": {"query": "artificial intelligence"},
                    "id": "call_2"
                },
                {
                    "name": "UserQuery",
                    "args": {
                        "question": "What is AI?",
                        "category": "technology",
                        "priority": 3
                    },
                    "id": "call_3"
                }
            ])
        ],
        "main_engine": engine
    }
    
    # Test parallel execution
    print("1. Testing parallel execution...")
    validation_node = UnifiedValidationNodeConfig(
        name="parallel_validation",
        engine_name="main_engine",
        parallel_execution=True
    )
    
    validator = validation_node.create_runnable()
    result = validator(test_state)
    
    print(f"   Result type: {type(result)}")
    print(f"   Result: {result}")
    
    # Test single execution
    print("\n2. Testing single execution...")
    validation_node_single = UnifiedValidationNodeConfig(
        name="single_validation",
        engine_name="main_engine",
        parallel_execution=False
    )
    
    validator_single = validation_node_single.create_runnable()
    result_single = validator_single(test_state)
    
    print(f"   Result type: {type(result_single)}")
    print(f"   Result: {result_single}")

def main():
    """Run all tests."""
    print("Starting Unified Validation Testing...\n")
    
    try:
        # Test with SimpleAgent
        simple_agent = test_unified_validation_simple_agent()
        
        # Test with ReactAgent
        react_agent = test_unified_validation_react_agent()
        
        # Test Command/Send routing
        test_command_send_routing()
        
        print("\n=== All Tests Completed Successfully! ===")
        
        return {
            "simple_agent": simple_agent,
            "react_agent": react_agent,
            "success": True
        }
        
    except Exception as e:
        print(f"\n=== Test Failed: {e} ===")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    main()