"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    LATSAgentConfig: LATSAgentConfig implementation.
    LATSAgent: LATSAgent implementation.

Functions:
    from_scratch: From Scratch functionality.
    setup_workflow: Setup Workflow functionality.
    reflection_chain: Reflection Chain functionality.
"""

# src/haive/agents/lats/tree_agent.py

import logging
from datetime import datetime
from typing import Any

from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import chain as as_runnable
from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.agents.reasoning_and_critique.lats.models import Node, Reflection
from haive.agents.reasoning_and_critique.lats.state import TreeState

# Set up logging
logger = logging.getLogger(__name__)

# =============================================
# LATS Agent Config
# =============================================


class LATSAgentConfig(AgentConfig):
    """Configuration for a Look-Ahead Tree Search (LATS) agent.
    This agent uses tree search to explore multiple response candidates
    and select the best one based on reflections.
    """

    # LLM settings
    model: str = Field(default="gpt-4o", description="Model to use for the agent")
    temperature: float = Field(default=0.7, description="Temperature for generation")

    # LATS settings
    candidates_per_expansion: int = Field(
        default=5, description="Number of candidates to generate per expansion"
    )
    max_tree_height: int = Field(default=5, description="Maximum height of the tree")
    exploration_weight: float = Field(
        default=1.0, description="Exploration weight for UCB1"
    )

    # Tools
    tools: list[Any] = Field(default_factory=list, description="Tools for the agent")

    # Prompts
    system_prompt: str = Field(
        default="You are an AI assistant that provides accurate, helpful responses.",
        description="System prompt for generation",
    )

    reflection_prompt: str = Field(
        default="Reflect and grade the assistant response to the user question below.",
        description="Prompt for the reflection step",
    )

    # State schema
    state_schema: type[BaseModel] = Field(
        default=TreeState, description="Schema for the agent state"
    )

    @classmethod
    def from_scratch(
        cls,
        system_prompt: str | None = None,
        tools: list[Any] | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        candidates_per_expansion: int = 5,
        max_tree_height: int = 5,
        name: str | None = None,
        **kwargs,
    ) -> "LATSAgentConfig":
        """Create a LATSAgentConfig from scratch.

        Args:
            system_prompt: Optional system prompt
            tools: Optional tools to use
            model: Model name to use
            temperature: Temperature for generation
            candidates_per_expansion: Number of candidates per expansion
            max_tree_height: Maximum tree height
            name: Optional agent name
            **kwargs: Additional kwargs for the config

        Returns:
            LATSAgentConfig instance
        """
        # Use provided tools or empty list
        tools = tools or []

        # Use provided system prompt or default
        system_prompt = (
            system_prompt
            or "You are an AI assistant that provides accurate, helpful responses."
        )

        return cls(
            name=name or f"lats_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            system_prompt=system_prompt,
            tools=tools,
            model=model,
            temperature=temperature,
            candidates_per_expansion=candidates_per_expansion,
            max_tree_height=max_tree_height,
            **kwargs,
        )


# =============================================
# LATS Agent Implementation
# =============================================


@register_agent(LATSAgentConfig)
class LATSAgent(Agent[LATSAgentConfig]):
    """A Look-Ahead Tree Search (LATS) agent that uses tree search to
    explore multiple response candidates and find optimal solutions.

    This agent builds a tree of possible responses and evaluates them
    using reflection to select the best path.
    """

    def setup_workflow(self) -> None:
        """Set up the LATS agent workflow graph."""
        logger.debug(f"Setting up workflow for LATSAgent {self.config.name}")

        # Create prompt templates
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.config.system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )

        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.config.reflection_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="candidate"),
            ]
        )

        # Initialize LLM
        llm_config = AzureLLMConfig(
            model=self.config.model, parameters={"temperature": self.config.temperature}
        )
        self.llm = llm_config.instantiate()

        # Create tool node if tools are provided
        if self.config.tools:
            from langgraph.prebuilt import ToolNode

            self.tool_node = ToolNode(tools=self.config.tools)
        else:
            self.tool_node = None

        # Set up chains
        self.initial_answer_chain = prompt_template | self.llm.bind_tools(
            tools=self.config.tools
        ).with_config(run_name="GenerateInitialCandidate")

        # Tool parser
        self.parser = JsonOutputToolsParser(return_id=True)

        # Reflection chain
        self.reflection_llm_chain = (
            reflection_prompt
            | self.llm.bind_tools(
                tools=[Reflection], tool_choice="Reflection"
            ).with_config(run_name="Reflection")
            | PydanticToolsParser(tools=[Reflection])
        )

        # Define the reflection chain
        @as_runnable
        def reflection_chain(inputs) -> Reflection:
            tool_choices = self.reflection_llm_chain.invoke(inputs)
            reflection = tool_choices[0]
            if not isinstance(inputs["candidate"][-1], AIMessage):
                reflection.found_solution = False
            return reflection

        self.reflection_chain = reflection_chain

        # Define the candidate generation function
        def generate_candidates(messages: ChatPromptValue, config: RunnableConfig):
            n = config["configurable"].get("N", self.config.candidates_per_expansion)
            bound_kwargs = self.llm.bind_tools(tools=self.config.tools).kwargs
            chat_result = self.llm.generate(
                [messages.to_messages()],
                n=n,
                callbacks=config["callbacks"],
                run_name="GenerateCandidates",
                **bound_kwargs,
            )
            return [gen.message for gen in chat_result.generations[0]]

        # Create expansion chain
        self.expansion_chain = prompt_template | generate_candidates

        # Define the node functions for the graph
        def generate_initial_response(state: TreeState) -> dict[str, Any]:
            """Generate the initial candidate response."""
            # Get the input
            user_input = state["input"]

            # Generate initial response
            res = self.initial_answer_chain.invoke({"input": user_input})

            # Parse tool calls if any
            parsed = self.parser.invoke(res)
            tool_responses = []

            # Execute tools if needed and if tool_node exists
            if self.tool_node and parsed:
                tool_responses = [
                    self.tool_node.invoke(
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
                    for r in parsed
                ]

            # Collect messages including tool responses
            output_messages = [res]
            if tool_responses:
                output_messages += [tr["messages"][0] for tr in tool_responses]

            # Generate reflection
            reflection = self.reflection_chain.invoke(
                {"input": user_input, "candidate": output_messages}
            )

            # Create the root node
            root = Node(
                output_messages,
                reflection=reflection,
                exploration_weight=self.config.exploration_weight,
            )

            # Update state
            return {
                **state,
                "root": root,
                "iterations": 0,
            }

        def expand(state: TreeState, config: RunnableConfig) -> dict[str, Any]:
            """Expand the tree by generating candidates from the best node."""
            root = state["root"]
            iterations = state["iterations"]
            user_input = state["input"]

            # Select the best leaf node to expand
            best_candidate: Node = self._select(root)

            # Get the messages from the node trajectory
            messages = best_candidate.get_trajectory()

            # Generate new candidates
            new_candidates = self.expansion_chain.invoke(
                {"input": user_input, "messages": messages},
                config={"configurable": {"N": self.config.candidates_per_expansion}},
            )

            # Process tool calls if any
            parsed = self.parser.batch(new_candidates)

            # Handle tool executions
            output_messages = []
            if self.tool_node:
                # Flatten the tool calls
                flattened = [
                    (i, tool_call)
                    for i, tool_calls in enumerate(parsed)
                    for tool_call in tool_calls
                ]

                # Execute tools
                tool_responses = []
                for i, tool_call in flattened:
                    try:
                        response = self.tool_node.invoke(
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
                        tool_responses.append((i, response))
                    except Exception as e:
                        logger.exception(f"Error executing tool: {e}")
                        # Create an error message
                        tool_responses.append(
                            (
                                i,
                                {
                                    "messages": [
                                        AIMessage(content=f"Error executing tool: {e}")
                                    ]
                                },
                            )
                        )

                # Collect tool responses by candidate index
                from collections import defaultdict

                collected_responses = defaultdict(list)
                for i, resp in tool_responses:
                    collected_responses[i].append(resp["messages"][0])

                # Combine candidate messages with tool responses
                for i, candidate in enumerate(new_candidates):
                    output_messages.append([candidate] + collected_responses[i])
            else:
                # No tools, just use the candidate messages
                output_messages = [[candidate] for candidate in new_candidates]

            # Reflect on each candidate
            reflections = self.reflection_chain.batch(
                [{"input": user_input, "candidate": msges} for msges in output_messages]
            )

            # Create and add child nodes
            child_nodes = [
                Node(
                    cand,
                    parent=best_candidate,
                    reflection=reflection,
                    exploration_weight=self.config.exploration_weight,
                )
                for cand, reflection in zip(output_messages, reflections, strict=False)
            ]
            best_candidate.children.extend(child_nodes)

            # Increment iterations
            return {
                **state,
                "iterations": iterations + 1,
            }

        def should_continue(state: TreeState) -> str:
            """Determine whether to continue searching or finish."""
            root = state["root"]
            iterations = state["iterations"]

            # Check if solution found
            if self._is_solved(root):
                logger.info(f"Solution found after {iterations} iterations")
                return END

            # Check max iterations
            if iterations >= self.config.max_tree_height:
                logger.info(f"Reached max iterations ({self.config.max_tree_height})")
                return END

            # Continue searching
            return "expand"

        def get_best_response(state: TreeState) -> dict[str, Any]:
            """Get the best response from the tree search."""
            root = state["root"]

            # Find the best path
            best_node = self._get_best_node(root)
            best_messages = best_node.get_trajectory()

            # Update state with best messages and reflection
            updated_state = {
                **state,
                "best_node": best_node,
                "output": best_messages[-1].content if best_messages else "",
                "messages": (
                    [*state.get("messages", []), best_messages[-1]]
                    if best_messages
                    else []
                ),
            }

            return updated_state

        # Build the graph
        from langgraph.graph import START, StateGraph

        graph = StateGraph(TreeState)

        # Add nodes
        graph.add_node("start", generate_initial_response)
        graph.add_node("expand", expand)
        graph.add_node("finish", get_best_response)

        # Add edges
        graph.add_edge(START, "start")
        graph.add_conditional_edges("start", should_continue, ["expand", "finish"])
        graph.add_conditional_edges("expand", should_continue, ["expand", "finish"])
        graph.add_edge("finish", END)

        # Set graph
        self.graph = graph

    def _select(self, root: Node) -> Node:
        """Select the best leaf node for expansion using UCB1."""
        if not root.children:
            return root

        node = root
        while node.children:
            # Select child with highest UCB
            max_child = max(
                node.children, key=lambda child: child.upper_confidence_bound()
            )
            node = max_child

        return node

    def _is_solved(self, root: Node) -> bool:
        """Check if a solution has been found in the tree."""
        # Check if root itself is solved
        if root.is_solved:
            return True

        # Recursively check all nodes
        def check_node(node) -> Any:
            if node.is_solved:
                return True
            return any(check_node(child) for child in node.children)

        return check_node(root)

    def _get_best_node(self, root: Node) -> Node:
        """Get the best node in the tree based on reflections."""
        # Collect all nodes
        all_nodes = []

        def collect_nodes(node) -> None:
            all_nodes.append(node)
            for child in node.children:
                collect_nodes(child)

        collect_nodes(root)

        # Find the node with highest reflection score
        return max(
            all_nodes, key=lambda node: node.reflection.score if node.reflection else 0
        )

    def run(self, input_text: str | dict[str, Any]) -> dict[str, Any]:
        """Run the LATS agent with the given input."""
        # If input is a string, convert to dict
        if isinstance(input_text, str):
            input_data = {
                "input": input_text,
                "messages": [HumanMessage(content=input_text)],
            }
        else:
            input_data = input_text

        # Make sure input field exists
        if "input" not in input_data and "messages" in input_data:
            # Extract input from last human message
            for msg in reversed(input_data["messages"]):
                if isinstance(msg, HumanMessage):
                    input_data["input"] = msg.content
                    break

        # Make sure messages field exists
        if "messages" not in input_data and "input" in input_data:
            input_data["messages"] = [HumanMessage(content=input_data["input"])]

        # Run the agent
        result = super().run(input_data)

        return result

    def stream(self, input_text: str | dict[str, Any]):
        """Stream the LATS agent execution with the given input."""
        # If input is a string, convert to dict
        if isinstance(input_text, str):
            input_data = {
                "input": input_text,
                "messages": [HumanMessage(content=input_text)],
            }
        else:
            input_data = input_text

        # Make sure input field exists
        if "input" not in input_data and "messages" in input_data:
            # Extract input from last human message
            for msg in reversed(input_data["messages"]):
                if isinstance(msg, HumanMessage):
                    input_data["input"] = msg.content
                    break

        # Make sure messages field exists
        if "messages" not in input_data and "input" in input_data:
            input_data["messages"] = [HumanMessage(content=input_data["input"])]

        # Stream the agent execution
        return super().stream(input_data)


# =============================================
# Helper Functions
# =============================================


def create_lats_agent(
    system_prompt: str | None = None,
    tools: list[Any] | None = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    candidates_per_expansion: int = 5,
    max_tree_height: int = 5,
    name: str | None = None,
    **kwargs,
) -> LATSAgent:
    """Create a LATS agent with the specified configuration.

    Args:
        system_prompt: Optional system prompt for generation
        tools: Optional tools to use
        model: Model to use
        temperature: Temperature for generation
        candidates_per_expansion: Number of candidates per expansion
        max_tree_height: Maximum tree height
        name: Optional agent name
        **kwargs: Additional configuration parameters

    Returns:
        LATSAgent instance
    """
    # Create config
    config = LATSAgentConfig.from_scratch(
        system_prompt=system_prompt,
        tools=tools,
        model=model,
        temperature=temperature,
        candidates_per_expansion=candidates_per_expansion,
        max_tree_height=max_tree_height,
        name=name or f"lats_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()
