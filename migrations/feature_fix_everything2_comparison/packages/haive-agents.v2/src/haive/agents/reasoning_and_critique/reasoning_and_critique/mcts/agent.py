"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    MCTSAgent: MCTSAgent implementation.
    run: run implementation.

Functions:
    setup_workflow: Setup Workflow functionality.
    reflection_chain: Reflection Chain functionality.
"""

# src/haive/agents/mcts/agent.py

import logging
from collections import defaultdict
from typing import Any

from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import chain as as_runnable
from langgraph.graph import END
from langgraph.prebuilt import ToolNode

from haive.agents.base.agent import Agent
from haive.agents.reasoning_and_critique.mcts.models import Reflection, TreeNode
from haive.agents.reasoning_and_critique.mcts.state import TreeState

# Set up logging
logger = logging.getLogger(__name__)


class MCTSAgent(Agent):
    """Monte Carlo Tree Search Agent implementation.

    This agent uses a Monte Carlo Tree Search approach to iteratively explore
    and find the best solution path.
    """

    def setup_workflow(self) -> None:
        """Set up the workflow graph for the MCTS agent."""
        logger.debug(f"Setting up workflow for MCTSAgent {self.config.name}")

        # Create a DynamicGraph with our state schema
        gb = DynamicGraph(
            components=[self.config.state_schema], state_schema=self.state_schema
        )

        # Configure LLM with tools
        llm = self.config.llm_config.instantiate()
        self.llm_with_tools = llm.bind_tools(tools=self.config.tools)

        # Create a tool node
        self.tool_node = ToolNode(tools=self.config.tools)

        # Set up chains
        self._setup_chains()

        # Add nodes to the graph
        gb.add_node(
            name="generate_initial_response", config=self._generate_initial_response
        )

        gb.add_node(name="expand", config=self._expand)

        # Add conditional edges
        gb.add_conditional_edges(
            "generate_initial_response",
            self._should_continue,
            {"end": END, "expand": "expand"},
        )

        gb.add_conditional_edges(
            "expand", self._should_continue, {"end": END, "expand": "expand"}
        )

        # Set the entry point
        gb.set_entry_point("generate_initial_response")

        # Build the graph
        self.graph = gb.build()
        logger.info(f"Set up MCTS agent workflow for {self.config.name}")

    def _setup_chains(self):
        """Set up the chains used by the agent."""
        llm = self.config.llm_config.instantiate()
        llm_with_tools = self.llm_with_tools

        # Initial response chain
        self.initial_answer_chain = (
            self.config.initial_prompt_template
            | llm_with_tools.with_config(run_name="GenerateInitialCandidate")
        )

        # Tool response parser
        self.parser = JsonOutputToolsParser(return_id=True)

        # Reflection chain
        reflection_llm_chain = (
            self.config.reflection_prompt_template
            | llm.bind_tools(tools=[Reflection], tool_choice="Reflection").with_config(
                run_name="Reflection"
            )
            | PydanticToolsParser(tools=[Reflection])
        )

        @as_runnable
        def reflection_chain(inputs) -> Reflection:
            tool_choices = reflection_llm_chain.invoke(inputs)
            reflection = tool_choices[0]
            if not isinstance(inputs["candidate"][-1], AIMessage):
                reflection.found_solution = False
            return reflection

        self.reflection_chain = reflection_chain

        # Expansion chain
        def generate_candidates(messages: list[dict[str, Any]], config: RunnableConfig):
            n = config["configurable"].get("N", self.config.candidates_per_rollout)
            bound_kwargs = llm_with_tools.kwargs
            chat_result = llm.generate(
                [messages.to_messages()],
                n=n,
                callbacks=config["callbacks"],
                run_name="GenerateCandidates",
                **bound_kwargs,
            )
            return [gen.message for gen in chat_result.generations[0]]

        self.expansion_chain = (
            self.config.expansion_prompt_template | generate_candidates
        )

    def _generate_initial_response(self, state: TreeState) -> dict[str, Any]:
        """Generate the initial candidate response."""
        try:
            # Extract input
            input_text = state.input

            # Invoke the initial answer chain
            res = self.initial_answer_chain.invoke({"input": input_text})

            # Parse tool calls
            parsed = self.parser.invoke(res)

            # Execute tools
            tool_responses = []
            for r in parsed:
                tool_resp = self.tool_node.invoke(
                    {
                        "messages": [
                            AIMessage(
                                content="",
                                tool_calls=[
                                    {
                                        "name": r["type"],
                                        "args": r["args"],
                                        "id": r["id"],
                                    }
                                ],
                            )
                        ]
                    }
                )
                tool_responses.append(tool_resp["messages"][0])

            # Combine messages
            output_messages = [res, *tool_responses]

            # Perform reflection
            reflection = self.reflection_chain.invoke(
                {"input": input_text, "candidate": output_messages}
            )

            # Create root node
            node_data = TreeNode(
                messages=state.nodes.serialize_messages(output_messages),
                reflection=reflection.model_dump(),
                is_solved=reflection.found_solution,
            )

            # Update nodes store
            updated_nodes = state.nodes
            updated_nodes.add_node(node_data)

            # Mark tree as solved if solution found
            if reflection.found_solution:
                updated_nodes.mark_tree_as_solved(node_data.node_id)

            # Create updated state
            updated_state = {
                "nodes": updated_nodes,
                "messages": output_messages,
                "current_step": 1,
                "status": "searching",
                "solved": reflection.found_solution,
            }

            return updated_state

        except Exception as e:
            logger.exception(f"Error in generate_initial_response: {e!s}")
            return {
                "error": f"Error generating initial response: {e!s}",
                "status": "error",
            }

    def _expand(self, state: TreeState, config: RunnableConfig) -> dict[str, Any]:
        """Expand the search tree by generating new candidates from the best node."""
        try:
            # Get current nodes store
            nodes_store = state.nodes

            # Get new step count
            new_step = state.current_step + 1

            # Select best node to expand
            best_node_id = nodes_store.select_best_node()
            if not best_node_id:
                # No node to expand
                return {"error": "No node found to expand", "status": "errof"}

            best_node = nodes_store.get_node_by_id(best_node_id)
            if not best_node:
                return {
                    "error": f"Selected node {best_node_id} not found",
                    "status": "error",
                }

            # Get trajectory messages
            trajectory_messages = nodes_store.deserialize_messages(
                nodes_store.get_trajectory(best_node_id, include_reflections=False)
            )

            # Set N in config for number of candidates
            config_with_n = dict(config)
            if "configurable" not in config_with_n:
                config_with_n["configurable"] = {}
            config_with_n["configurable"]["N"] = self.config.candidates_per_rollout

            # Generate candidate expansions
            new_candidates = self.expansion_chain.invoke(
                {"input": state.input, "messages": trajectory_messages}, config_with_n
            )

            # Parse tool calls from candidates
            parsed = self.parser.batch(new_candidates)

            # Organize tool calls by candidate index
            flattened = []
            for i, tool_calls in enumerate(parsed):
                for tool_call in tool_calls:
                    flattened.append((i, tool_call))

            # Execute tools
            tool_responses = []
            for i, tool_call in flattened:
                resp = self.tool_node.invoke(
                    {
                        "messages": [
                            AIMessage(
                                content="",
                                tool_calls=[
                                    {
                                        "name": tool_call["type"],
                                        "args": tool_call["args"],
                                        "id": tool_call["id"],
                                    }
                                ],
                            )
                        ]
                    }
                )
                tool_responses.append((i, resp["messages"][0]))

            # Group tool responses by candidate index
            collected_responses = defaultdict(list)
            for i, resp in tool_responses:
                collected_responses[i].append(resp)

            # Organize output messages
            output_messages = []
            for i, candidate in enumerate(new_candidates):
                output_messages.append([candidate] + collected_responses[i])

            # Reflect on each candidate
            reflection_inputs = [
                {"input": state.input, "candidate": msges} for msges in output_messages
            ]
            reflections = self.reflection_chain.batch(reflection_inputs, config)

            # Create child nodes
            updated_nodes = nodes_store
            found_solution = state.solved

            for candidate_msgs, reflection in zip(
                output_messages, reflections, strict=False
            ):
                # Create node
                node_data = TreeNode(
                    messages=updated_nodes.serialize_messages(candidate_msgs),
                    reflection=reflection.model_dump(),
                    parent_id=best_node_id,
                    depth=best_node.depth + 1,
                    is_solved=reflection.found_solution,
                )

                # Add to nodes store
                updated_nodes.add_node(node_data)

                # Update parent's children
                best_node.children_ids.append(node_data.node_id)

                # Backpropagate score
                updated_nodes.backpropagate(
                    node_data.node_id, reflection.normalized_score
                )

                # Mark tree as solved if solution found
                if reflection.found_solution:
                    updated_nodes.mark_tree_as_solved(node_data.node_id)
                    found_solution = True

            # Find best solution so far
            best_solution = updated_nodes.get_best_solution()

            # Create updated state dictionary
            updated_state = {
                "nodes": updated_nodes,
                "current_step": new_step,
                "solved": found_solution,
            }

            # If we found a solution, update the messages and output
            if best_solution and best_solution.is_solved:
                # Update messages with best solution
                solution_messages = updated_nodes.deserialize_messages(
                    updated_nodes.get_trajectory(
                        best_solution.node_id, include_reflections=False
                    )
                )
                updated_state["messages"] = solution_messages

                # Get the last message as output
                if solution_messages and isinstance(solution_messages[-1], AIMessage):
                    updated_state["output"] = solution_messages[-1].content

            return updated_state

        except Exception as e:
            logger.exception(f"Error in expand node: {e!s}")
            return {"error": f"Error expanding search tree: {e!s}", "status": "error"}

    def _should_continue(self, state: TreeState) -> str:
        """Determine whether to continue the tree search or exit."""
        # Check for error
        if state.error:
            return "end"

        # Check if solution found
        if state.solved:
            return "end"

        # Check max steps
        if state.current_step >= state.max_steps:
            return "end"

        # Check tree height
        tree_height = state.nodes.get_tree_height()
        if tree_height > self.config.max_rollouts:
            return "end"

        # Continue search
        return "expand"

    # def run(self, input_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    # """Run the agent with the provided input."""
    # if isinstance(input_data, str):

    # Initialize nodes store if needed
    # if "nodes" not in input_data:

    # Call superclass run method
