# tests/test_graph.py

import uuid
from typing import Annotated, Any, Dict, List, Optional, Sequence

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, add_messages
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.branches.branch import Branch, BranchMode
from haive.core.graph.common.types import NodeType
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.state_graph.schema_graph import SchemaGraph
from haive.core.schema.state_schema import StateSchema


# Define the Plan model for tools and validation
class Plan(BaseModel):
    """Model for creating a plan"""

    steps: List[str] = Field(description="List of steps to complete")


# Define a state schema with messages
class PlanState(StateSchema):
    """State schema for plan generation"""

    messages: Sequence[Annotated[BaseMessage, add_messages]] = Field(
        default_factory=list
    )
    query: str = Field(default="")
    plan: Optional[Plan] = Field(default=None)
    validated: bool = Field(default=False)
    tools_result: Optional[Dict[str, Any]] = Field(default=None)


# Test basic graph functionality
def test_basic_graph():
    # Create a simple graph
    graph = BaseGraph(name="Test Graph")

    # Define nodes as functions
    def router(state: Dict[str, Any]) -> Dict[str, Any]:
        """Route based on query"""
        return {"query": state.get("query", "")}

    def execute(state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute query"""
        return {"result": f"Executed: {state.get('query', '')}"}

    # Add nodes
    graph.add_node("router", router)
    graph.add_node("execute", execute)

    # Add edges
    graph.add_edge(START, "router")
    graph.add_edge("router", "execute")
    graph.add_edge("execute", END)

    # Validate graph structure
    assert len(graph.nodes) == 2

    assert len(graph.edges) == 3
    assert graph.check_graph_validity() == []  # No validation issues

    # Test path analysis
    paths = graph.find_all_paths(START, END)
    assert len(paths) == 1
    assert paths[0].nodes == [START, "router", "execute", END]
    assert paths[0].reaches_end


# Test conditional branching
def test_conditional_branching():
    # Create a graph with branches
    graph = BaseGraph(name="Branch Test")

    # Define nodes
    def router(state: Dict[str, Any]) -> Dict[str, Any]:
        """Route based on query type"""
        return {"query": state.get("query", "")}

    def search(state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search queries"""
        return {"result": f"Searched for: {state.get('query', '')}"}

    def answer(state: Dict[str, Any]) -> Dict[str, Any]:
        """Answer general questions"""
        return {"result": f"Answered: {state.get('query', '')}"}

    # Add nodes
    graph.add_node("router", router)
    graph.add_node("search", search)
    graph.add_node("answer", answer)

    # Add basic edges
    graph.add_edge(START, "router")

    # Define branch logic
    def route_by_type(state: Dict[str, Any]) -> str:
        query = state.get("query", "").lower()
        if "search" in query or "find" in query:
            return "search"
        return "answer"

    # Create Branch object
    # Create Branch object
    route_branch = Branch(
        function=route_by_type,
        destinations={"search": "search", "answer": "answer"},
        mode=BranchMode.FUNCTION,
    )

    # Add the branch to the graph using add_conditional_edges
    graph.add_conditional_edges(
        "router",  # source node
        route_branch,  # branch object (or function)
        {"search": "search", "answer": "answer"},  # destinations
    )

    # Connect to END

    graph.add_edge("search", END)
    graph.add_edge("answer", END)
    # print(graph.edges)
    print("--------------------------------")
    print(graph.conditional_edges)
    print(len(graph.conditional_edges))
    print(graph.edges)
    print(len(graph.edges))
    print("--------------------------------")
    # Validate graph
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 3
    assert len(graph.conditional_edges) == 1

    # Ensure all nodes have a path to END
    assert graph.find_nodes_without_end_path() == []

    # Find paths from START to END
    paths = graph.find_all_paths(START, END)
    assert len(paths) == 2  # Two possible paths through the conditional
    assert all(path.contains_conditional for path in paths)  # Both use conditional


# Test subgraph functionality
def test_subgraph():
    # Create a subgraph
    subgraph = BaseGraph(name="Tool Subgraph")

    # Define subgraph nodes
    def tool_router(state: Dict[str, Any]) -> Dict[str, Any]:
        """Route to specific tool"""
        return {"tool_request": state.get("query", "")}

    def calculator(state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculator tool"""
        return {"result": "42"}

    # Build subgraph
    subgraph.add_node("tool_router", tool_router)
    subgraph.add_node("calculator", calculator)
    subgraph.add_edge(START, "tool_router")
    subgraph.add_edge("tool_router", "calculator")
    subgraph.add_edge("calculator", END)

    # Create parent graph
    graph = BaseGraph(name="Main Graph")

    # Define parent graph nodes
    def main_router(state: Dict[str, Any]) -> Dict[str, Any]:
        """Main router"""
        return {"query": state.get("query", "")}

    def formatter(state: Dict[str, Any]) -> Dict[str, Any]:
        """Format results"""
        return {"formatted": f"Result: {state.get('result', '')}"}

    # Build parent graph
    graph.add_node("main_router", main_router)
    graph.add_subgraph("tools", subgraph)  # Add subgraph as a node
    graph.add_node("formatter", formatter)

    # Connect nodes
    graph.add_edge(START, "main_router")
    graph.add_edge("main_router", "tools")  # Route to subgraph
    graph.add_edge("tools", "formatter")  # From subgraph to formatter
    graph.add_edge("formatter", END)

    # Verify structure
    assert "tools" in graph.nodes
    assert graph.node_types["tools"] == NodeType.SUBGRAPH
    assert "tools" in graph.subgraphs

    # Validate
    assert not graph.find_unreachable_nodes()
    assert not graph.find_nodes_without_end_path()


# Test graph extension
def test_graph_extension():
    # Create base graph
    base_graph = BaseGraph(name="Base Graph")

    # Define base nodes
    def query_parser(state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse query"""
        return {"parsed_query": state.get("query", "")}

    def router(state: Dict[str, Any]) -> Dict[str, Any]:
        """Route query"""
        return state

    # Build base graph
    base_graph.add_node("query_parser", query_parser)
    base_graph.add_node("router", router)
    base_graph.add_edge(START, "query_parser")
    base_graph.add_edge("query_parser", "router")

    # Create extension graph
    extension_graph = BaseGraph(name="Extension Graph")

    # Define extension nodes
    def tool(state: Dict[str, Any]) -> Dict[str, Any]:
        """Tool execution"""
        return {"tool_result": "Data"}

    def formatter(state: Dict[str, Any]) -> Dict[str, Any]:
        """Format results"""
        return {"response": state.get("tool_result", "")}

    # Build extension
    extension_graph.add_node("tool", tool)
    extension_graph.add_node("formatter", formatter)
    extension_graph.add_edge("tool", "formatter")
    extension_graph.add_edge("formatter", END)

    # Now extend the base graph
    base_graph.extend_from(extension_graph)

    # Connect the graphs
    base_graph.add_edge("router", "tool")

    # Verify structure
    assert len(base_graph.nodes) == 4  # All nodes combined
    assert "tool" in base_graph.nodes
    assert "formatter" in base_graph.nodes

    # Validate
    assert not base_graph.find_unreachable_nodes()
    assert not base_graph.find_nodes_without_end_path()

    # Check paths
    paths = base_graph.find_all_paths(START, END)
    assert len(paths) == 1
    assert paths[0].nodes == [START, "query_parser", "router", "tool", "formatter", END]


# Test schema graph with NodeConfig objects
def test_node_config_graph():
    """Test a graph constructed with NodeConfig objects and branching logic."""
    # STEP 1: Create the core components

    # Create AugLLMConfig
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are tasked with coming up with a plan for the following {task}",
            )
        ]
    )

    llm_config = AugLLMConfig(
        name="planner",
        prompt_template=prompt_template,
        structured_output_model=Plan,
        structured_output_version="v2",
    )

    # Create validation node config
    val_node = ValidationNodeConfig(
        name="validate_plan",
        validation_status_key="validated",
        command_goto="execute_plan",
        schemas=[Plan],
    )

    # Create tool node config
    tool_node = ToolNodeConfig(name="planning_tools", tools=[Plan])

    # Create engine node config
    engine_node = EngineNodeConfig(name="planner_agent", engine=llm_config)

    # STEP 2: Create the execution function
    def execute_plan(state: PlanState) -> Dict[str, Any]:
        """Execute the validated plan"""
        print(f"DEBUG: Executing plan with state: {state}")
        steps = state.plan.steps if state.plan else []
        return {"execution_result": f"Executed {len(steps)} steps"}

    # STEP 3: Define the route validation function
    def route_by_validation(state: Dict[str, Any]) -> str:
        """Route based on validation status"""
        print(f"DEBUG: Routing with validation status: {state.get('validated', False)}")
        if state.get("validated", False):
            print("DEBUG: Routing to 'execute'")
            return "execute"
        else:
            print("DEBUG: Routing to 'tools'")
            return "tools"

    # STEP 4: Create the graph
    print("\n=== BUILDING GRAPH ===")
    graph = SchemaGraph(
        name="Planning Flow",
        state_schema=PlanState,
    )

    # STEP 5: Add nodes
    print("\n--- Adding Nodes ---")
    graph.add_node("agent", engine_node)
    print(f"Added node: 'agent' (type: {graph.node_types.get('agent')})")

    graph.add_node("validate", val_node)
    print(f"Added node: 'validate' (type: {graph.node_types.get('validate')})")

    graph.add_node("tools", tool_node)
    print(f"Added node: 'tools' (type: {graph.node_types.get('tools')})")

    graph.add_node("execute_plan", execute_plan)
    print(f"Added node: 'execute_plan' (type: {graph.node_types.get('execute_plan')})")

    # STEP 6: Add direct edges
    print("\n--- Adding Direct Edges ---")
    graph.add_edge(START, "agent")
    print(f"Added edge: {START} → agent")

    graph.add_edge("agent", "validate")
    print("Added edge: agent → validate"e")

    graph.add_edge("tools", "agent")  # Loop back to agent
    print("Added edge: tools → agent"t")

    graph.add_edge("execute_plan", END)
    print(f"Added edge: execute_plan → {END}")

    # STEP 7: Add conditional branch
    print("\n--- Adding Conditional Branch ---")

    branch = Branch(
        id=str(uuid.uuid4()),
        name="validation_branch",
        source_node="validate",
        function=route_by_validation,
        destinations={"execute": "execute_plan", "tools": "tools"},
        default="END",  # Make sure default is set correctly
        mode=BranchMode.FUNCTION,
    )

    # Add the branch directly
    graph.branches[branch.id] = branch
    print(f"Added branch from 'validate' with destinations: {branch.destinations}")

    # STEP 8: Validate graph structure
    print("\n=== GRAPH STRUCTURE ===")
    print(f"Nodes ({len(graph.nodes)}): {list(graph.nodes.keys())}")
    print(f"Edges ({len(graph.edges)}): {graph.edges}")
    print(
        f"Branches ({len(graph.branches)}): {[(b.source_node, dict(b.destinations)) for b in graph.branches.values()]}"
    )

    # STEP 9: Test nodes have correct type
    print("\n=== NODE TYPES ===")
    assert (
        graph.node_types["agent"] == NodeType.ENGINE
    ), f"Expected ENGINE, got {graph.node_types['agent']}"
    print("✓ agent is ENGINE")

    assert (
        graph.node_types["validate"] == NodeType.VALIDATION
    ), f"Expected VALIDATION, got {graph.node_types['validate']}"
    print("✓ validate is VALIDATION")

    assert (
        graph.node_types["tools"] == NodeType.TOOL
    ), f"Expected TOOL, got {graph.node_types['tools']}"
    print("✓ tools is TOOL")

    assert (
        graph.node_types["execute_plan"] == NodeType.CALLABLE
    ), f"Expected CALLABLE, got {graph.node_types['execute_plan']}"
    print("✓ execute_plan is CALLABLE")

    # STEP 10: Test segment by segment
    print("\n=== TESTING PATH SEGMENTS ===")

    # Test START to agent
    print("\nTesting START → agent:")
    start_to_agent = graph.find_all_paths(START, "agent")
    print(f"- Found {len(start_to_agent)} paths")
    assert len(start_to_agent) >= 1, "No path found from START to agent"

    # Test agent to validate
    print("\nTesting agent → validate:")
    agent_to_validate = graph.find_all_paths("agent", "validate")
    print(f"- Found {len(agent_to_validate)} paths")
    assert len(agent_to_validate) >= 1, "No path found from agent to validate"

    # Test validate to execute_plan (through branch)
    print("\nTesting validate → execute_plan:")
    # Direct manual check for branch connection
    branch_connects = False
    for branch in graph.branches.values():
        if branch.source_node == "validate" and "execute" in branch.destinations:
            if branch.destinations["execute"] == "execute_plan":
                branch_connects = True
                break

    print(f"- Branch connection exists: {branch_connects}")
    assert branch_connects, "Branch doesn't connect validate to execute_plan"

    # Test execute_plan to END
    print("\nTesting execute_plan → END:")
    execute_to_end = graph.find_all_paths("execute_plan", END)
    print(f"- Found {len(execute_to_end)} paths")
    assert len(execute_to_end) >= 1, "No path found from execute_plan to END"

    # STEP 11: Manual path validation
    print("\n=== MANUAL PATH VALIDATION ===")

    def verify_full_path():
        """Manually verify the complete path exists from START to END."""
        # Check START to agent
        if not any(e for e in graph.edges if e[0] == START and e[1] == "agent"):
            print("❌ No edge from START to agent")
            return False

        # Check agent to validate
        if not any(e for e in graph.edges if e[0] == "agent" and e[1] == "validate"):
            print("❌ No edge from agent to validate")
            return False

        # Check branch from validate
        validate_branch = None
        for branch in graph.branches.values():
            if branch.source_node == "validate":
                validate_branch = branch
                break

        if not validate_branch:
            print("❌ No branch from validate node")
            return False

        # Check branch destinations
        if "execute" not in validate_branch.destinations:
            print("❌ Branch missing 'execute' condition")
            return False

        if validate_branch.destinations["execute"] != "execute_plan":
            print(
                f"❌ 'execute' condition points to {validate_branch.destinations['execute']}, not execute_plan"
            )
            return False

        # Check execute_plan to END
        if not any(e for e in graph.edges if e[0] == "execute_plan" and e[1] == END):
            print("❌ No edge from execute_plan to END")
            return False

        print(
            "✅ Complete path exists from START → agent → validate → execute_plan → END"
        )
        return True

    # Run manual validation
    path_exists = verify_full_path()
    assert path_exists, "No complete path from START to END"

    # STEP 12: Test complete path with find_all_paths
    print("\n=== TESTING COMPLETE PATH ===")

    # Try with various path-finding options
    print("Trying default path finding:")
    paths = graph.find_all_paths(START, END)
    print(f"- Found {len(paths)} paths from START to END")

    # Debug the path details if any exist
    if paths:
        for i, path in enumerate(paths):
            print(f"Path {i+1}: {path.nodes}")
            print(f"  Conditional: {path.contains_conditional}")
            print(f"  Reaches end: {path.reaches_end}")

    # If no paths found, try more debug options
    if not paths:
        print("\nTrying with include_loops=True:")
        paths = graph.find_all_paths(START, END, include_loops=True)
        print(f"- Found {len(paths)} paths with loops included")

        print("\nTrying with higher depth limit:")
        paths = graph.find_all_paths(START, END, max_depth=1000)
        print(f"- Found {len(paths)} paths with increased depth")

    # Final assertion - we expect exactly 1 path from START to END
    assert len(paths) == 1, f"Expected 1 path from START to END, found {len(paths)}"

    # STEP 13: Test the looping path to agent
    print("\n=== TESTING LOOPS ===")

    # Test the loop: agent → validate → tools → agent
    loop_exists = False

    # Manual loop validation
    if (
        any(e for e in graph.edges if e[0] == "agent" and e[1] == "validate")
        and any(
            b
            for b in graph.branches.values()
            if b.source_node == "validate"
            and "tools" in b.destinations
            and b.destinations["tools"] == "tools"
        )
        and any(e for e in graph.edges if e[0] == "tools" and e[1] == "agent")
    ):

        loop_exists = True
        print("✅ Loop exists: agent → validate → tools → agent")
    else:
        print("❌ Loop not fully connected")

    assert loop_exists, "Loop path not fully connected"

    # Find paths back to agent including loops
    print("\nTesting paths to agent with loops:")
    agent_paths = graph.find_all_paths(START, "agent", include_loops=True, max_depth=10)
    print(f"- Found {len(agent_paths)} paths to agent (including loops)")

    # We expect at least 2 paths to agent:
    # 1. Direct: START → agent
    # 2. Loop: START → agent → validate → tools → agent
    assert (
        len(agent_paths) >= 2
    ), f"Expected at least 2 paths to agent, found {len(agent_paths)}"

    print("\n=== TEST COMPLETED SUCCESSFULLY ===")


# Test React pattern
def test_react_pattern():
    """Test implementing a React pattern in a graph"""

    # Create agent configuration
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", "You are a React agent that thinks step by step.")]
    )

    llm_config = AugLLMConfig(name="react_agent", prompt_template=prompt_template)

    # Create tool configuration
    tool_node = ToolNodeConfig(
        name="react_tools", tools=[Plan]  # Using Plan as a sample tool
    )

    # Create the base graph
    graph = SchemaGraph(
        name="React Pattern",
        state_schema=PlanState,
    )

    # Add nodes
    graph.add_node("agent", EngineNodeConfig(name="agent", engine=llm_config))
    graph.add_node("tools", tool_node)

    # Add edges
    graph.add_edge(START, "agent")

    # Create branch logic for React pattern
    def react_router(state: Dict[str, Any]) -> str:
        """Route based on agent output"""
        # Check if latest message has tool calls
        messages = state.get("messages", [])
        if not messages:
            return "end"

        last_message = messages[-1]

        # If AI message with tool calls, route to tools
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            return "tools"

        # Otherwise, we're done
        return "end"

    # Create Branch
    react_branch = Branch(
        function=react_router, destinations={"tools": "tools", "end": END}
    )

    # Add conditional edge
    graph.add_conditional_edges("agent", react_branch, {"tools": "tools", "end": END})

    # Connect tools back to agent to complete the loop
    graph.add_edge("tools", "agent")

    # Verify structure
    assert len(graph.nodes) == 2
    assert len(graph.conditional_edges) == 1

    # The graph should be valid
    assert not graph.check_graph_validity()

    # Display the graph
    graph.display()  # Uncomment for debugging
