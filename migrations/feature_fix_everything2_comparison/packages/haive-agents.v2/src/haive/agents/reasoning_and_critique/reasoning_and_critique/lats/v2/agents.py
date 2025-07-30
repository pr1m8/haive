"""Agents core module.

This module provides agents functionality for the Haive framework.

Functions:
    process_initial_response: Process Initial Response functionality.
    execute_tool_calls: Execute Tool Calls functionality.
    process_expansion: Process Expansion functionality.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.types import Send

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.reasoning_and_critique.lats.v2.models import (
    CandidateActions,
    Reflection,
    SelectionDecision,
    TreeNode,
)
from haive.agents.reasoning_and_critique.lats.v2.prompts import (
    expansion_prompt,
    initial_prompt,
    reflection_prompt,
    selection_prompt,
)
from haive.agents.reasoning_and_critique.lats.v2.state import LATSState
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)

# Create engines
initial_engine = AugLLMConfig(
    name="lats_initial_engine",
    prompt_template=initial_prompt,
    temperature=0.7,
    tools=["tavily_search_results_json"],  # Example tool
)

expansion_engine = AugLLMConfig(
    name="lats_expansion_engine",
    prompt_template=expansion_prompt,
    structured_output_model=CandidateActions,
    structured_output_model_version="v2",
    temperature=0.9,  # Higher for diversity
)

reflection_engine = AugLLMConfig(
    name="lats_reflection_engine",
    prompt_template=reflection_prompt,
    structured_output_model=Reflection,
    structured_output_model_version="v2",
    temperature=0.3,  # Lower for consistent evaluation
)

selection_engine = AugLLMConfig(
    name="lats_selection_engine",
    prompt_template=selection_prompt,
    structured_output_model=SelectionDecision,
    structured_output_model_version="v2",
    temperature=0.2,
)

# Create agents
initial_agent = SimpleAgent(name="initial", engine=initial_engine)
expansion_agent = SimpleAgent(name="expander", engine=expansion_engine)
reflection_agent = SimpleAgent(name="reflector", engine=reflection_engine)
selection_agent = SimpleAgent(name="selector", engine=selection_engine)

# Tool node for executing tool calls
tool_node = ToolNode(tools=["tavily_search_results_json"])


# Workflow nodes
def process_initial_response(state: LATSState) -> dict[str, Any]:
    """Process initial response and create root node."""
    # Get the last message (initial response)
    if state.messages:
        last_msg = state.messages[-1]

        # Create root node
        root = TreeNode(
            messages=[{"role": "assistant", "content": last_msg.content}],
            action=(
                last_msg.tool_calls[0]
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls
                else None
            ),
            depth=1,
        )

        return {
            "nodes": {root.id: root},
            "root_id": root.id,
            "current_node_id": root.id,
        }

    return {}


def execute_tool_calls(state: LATSState) -> dict[str, Any] | list[Send]:
    """Execute tool calls for nodes that need them."""
    sends = []

    # Check current node for tool calls
    if state.current_node_id:
        node = state.get_node(state.current_node_id)
        if node and node.action and not node.tool_response:
            # Send to tool node
            sends.append(
                Send(
                    "tool_node",
                    {**state.dict(), "messages": [{"tool_calls": [node.action]}]},
                )
            )

    # Check candidate nodes
    for candidate in state.candidate_nodes:
        if candidate.action and not candidate.tool_response:
            sends.append(
                Send(
                    "tool_node",
                    {
                        **state.dict(),
                        "current_node_id": candidate.id,
                        "messages": [{"tool_calls": [candidate.action]}],
                    },
                )
            )

    return sends if sends else {}


def process_expansion(state: LATSState) -> dict[str, Any]:
    """Process expansion results into new nodes."""
    if not state.messages:
        return {}

    # Get expansion results from last message
    last_msg = state.messages[-1]
    if hasattr(last_msg, "content") and isinstance(last_msg.content, dict):
        result = last_msg.content

        # Create new candidate nodes
        parent_id = state.current_node_id
        parent = state.get_node(parent_id) if parent_id else None
        parent_depth = parent.depth if parent else 0

        new_nodes = {}
        candidate_nodes = []

        for _i, candidate_data in enumerate(result.get("candidates", [])):
            node = TreeNode(
                parent_id=parent_id,
                messages=[{"role": "assistant", "content": str(candidate_data)}],
                action=(
                    candidate_data
                    if isinstance(candidate_data, dict) and "tool" in candidate_data
                    else None
                ),
                depth=parent_depth + 1,
            )

            new_nodes[node.id] = node
            candidate_nodes.append(node)

            # Update parent's children
            if parent:
                parent.children_ids.append(node.id)
                new_nodes[parent.id] = parent

        return {
            "nodes": new_nodes,
            "candidate_nodes": candidate_nodes,
            "rollouts_completed": 1,
        }

    return {}


def evaluate_candidates(state: LATSState) -> list[Send]:
    """Send candidates for reflection."""
    sends = []

    for candidate in state.candidate_nodes:
        # Prepare evaluation context
        response_to_evaluate = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in candidate.messages]
        )

        if candidate.tool_response:
            response_to_evaluate += f"\nTool Response: {candidate.tool_response}"

        evaluation_state = {
            **state.dict(),
            "current_node_id": candidate.id,
            "response_to_evaluate": response_to_evaluate,
        }

        sends.append(Send("reflector", evaluation_state))

    return sends


def process_reflection(state: LATSState) -> dict[str, Any]:
    """Process reflection results and update node scores."""
    if not state.messages or not state.current_node_id:
        return {}

    # Get reflection from last message
    last_msg = state.messages[-1]
    if hasattr(last_msg, "content") and isinstance(last_msg.content, dict):
        reflection = Reflection(**last_msg.content)

        # Update node with reflection
        node = state.get_node(state.current_node_id)
        if node:
            node.reflection_score = reflection.normalized_score
            node.reflection_text = reflection.reflections
            node.is_solved = reflection.found_solution

            # Backpropagate score
            updated_nodes = backpropagate(
                state.nodes, node.id, reflection.normalized_score
            )

            # Check for best solution
            best_id = state.best_solution_id
            best_node = state.get_node(best_id) if best_id else None

            if node.is_solved and (not best_node or node.value > best_node.value):
                return {
                    "nodes": updated_nodes,
                    "best_solution_id": node.id,
                    "candidate_nodes": [],  # Clear candidates
                }

            return {"nodes": updated_nodes, "candidate_nodes": []}

    return {}


def backpropagate(
    nodes: dict[str, TreeNode], node_id: str, reward: float
) -> dict[str, TreeNode]:
    """Backpropagate reward up the tree."""
    updated = {}
    current_id = node_id

    while current_id:
        node = nodes.get(current_id)
        if not node:
            break

        # Update node statistics
        node.visits += 1
        node.value = (node.value * (node.visits - 1) + reward) / node.visits
        updated[current_id] = node

        current_id = node.parent_id

    return updated


# Routing functions
def should_execute_tools(state: LATSState) -> str:
    """Check if any nodes need tool execution."""
    needs_tools = False

    if state.current_node_id:
        node = state.get_node(state.current_node_id)
        if node and node.action and not node.tool_response:
            needs_tools = True

    for candidate in state.candidate_nodes:
        if candidate.action and not candidate.tool_response:
            needs_tools = True

    return "execute_tools" if needs_tools else "evaluate"


def should_continue_search(state: LATSState) -> str:
    """Decide whether to continue search or terminate."""
    if not state.should_continue_search:
        return END

    # Check if we have a good enough solution
    if state.best_solution_id:
        best = state.get_node(state.best_solution_id)
        if best and best.value > 0.9:
            return END

    return "selector"


# Create LATS system
def create_lats(
    tools: list[Any],
    max_depth: int = 5,
    max_rollouts: int = 10,
    n_candidates: int = 5,
    **kwargs,
) -> MultiAgentBase:
    """Create a Language Agent Tree Search system."""
    # Create tool node with provided tools
    tool_node = ToolNode(tools=tools)

    branches = [
        # Initial response flow
        (
            initial_agent,
            lambda s: "process_initial",
            {"process_initial": "process_initial"},
        ),
        ("process_initial", lambda s: "reflectof", {"reflector": reflection_agent}),
        # After reflection of initial response
        (
            reflection_agent,
            lambda s: (
                "selector" if s.current_node_id == s.root_id else "process_reflection"
            ),
            {"selector": selection_agent, "process_reflection": "process_reflection"},
        ),
        # Selection leads to expansion
        (
            selection_agent,
            lambda s: "expandef" if not s.should_terminate else END,
            {"expander": expansion_agent, END: END},
        ),
        # Expansion leads to processing
        (
            expansion_agent,
            lambda s: "process_expansion",
            {"process_expansion": "process_expansion"},
        ),
        (
            "process_expansion",
            should_execute_tools,
            {"execute_tools": "execute_tools", "evaluate": "evaluate"},
        ),
        # Tool execution
        ("execute_tools", lambda s: "tool_node", {"tool_node": tool_node}),
        (tool_node, lambda s: "evaluate", {"evaluate": "evaluate"}),
        # Evaluation sends to reflection
        (
            "evaluate",
            lambda s: sends if (sends := evaluate_candidates(s)) else "selectof",
            {"reflector": reflection_agent, "selector": selection_agent},
        ),
        # After processing reflections
        (
            "process_reflection",
            should_continue_search,
            {"selectof": selection_agent, END: END},
        ),
    ]

    workflow_nodes = {
        "process_initial": process_initial_response,
        "execute_tools": execute_tool_calls,
        "process_expansion": process_expansion,
        "evaluate": lambda s: {},  # Just a pass-through
        "process_reflection": process_reflection,
    }

    system = MultiAgentBase(
        name="LATS",
        agents=[initial_agent, expansion_agent, reflection_agent, selection_agent],
        branches=branches,
        state_schema_override=LATSState,
        schema_build_mode=BuildMode.SEQUENCE,
        workflow_nodes=workflow_nodes,
        **kwargs,
    )

    # Set initial parameters
    system.initial_state = {
        "max_depth": max_depth,
        "max_rollouts": max_rollouts,
        "n_candidates": n_candidates,
        "tools": [{"name": t.name, "description": t.description} for t in tools],
    }

    return system
