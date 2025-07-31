"""Enhanced ReactAgent implementation using Agent[AugLLMConfig].

ReactAgent = Agent[AugLLMConfig] + reasoning loop with tools.
"""

import logging
from typing import Any, Literal

from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END
from pydantic import Field, model_validator

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
# For now, using a minimal base
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase as Agent

logger = logging.getLogger(__name__)


class ReactAgent(Agent):  # Will be Agent[AugLLMConfig] when imports fixed
    """Enhanced ReactAgent with reasoning and action loop.

    ReactAgent = Agent[AugLLMConfig] + reasoning loop with tools.

    The ReAct pattern (Reasoning and Acting) allows the agent to:
    1. Reason about what action to take
    2. Take the action (use a tool)
    3. Observe the result
    4. Reason again based on the observation
    5. Continue until task is complete

    Attributes:
        max_iterations: Maximum reasoning iterations (default: 10)
        tools: List of tools available to the agent
        react_prompt: Optional custom prompt for ReAct pattern

    Examples:
        Basic usage::

            from langchain_core.tools import tool

            @tool
            def calculator(expression: str) -> str:
                '''Calculate math expressions'''
                return str(eval(expression))

            agent = ReactAgent(
                name="math_agent",
                tools=[calculator],
                engine=AugLLMConfig()
            )

            result = agent.run("What is 15 * 23 + 7?")

        With multiple tools::

            agent = ReactAgent(
                name="research_agent",
                tools=[web_search, calculator, file_reader],
                max_iterations=15,
                react_prompt="You are a research assistant..."
            )
    """

    # Tool configuration
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools available to the agent"
    )

    # Iteration control
    max_iterations: int = Field(
        default=10, description="Maximum number of reasoning iterations", ge=1, le=50
    )

    # Prompting
    react_prompt: str | None = Field(
        default=None, description="Custom prompt for ReAct pattern"
    )

    # Execution mode
    execution_mode: Literal["react", "tool-calling", "hybrid"] = Field(
        default="react", description="How to execute the reasoning loop"
    )

    # Tracking
    reasoning_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of reasoning steps"
    )

    @model_validator(mode="after")
    def validate_react_config(self) -> "ReactAgent":
        """Validate ReactAgent configuration."""
        # Ensure we have an engine
        if not hasattr(self, "engine") or self.engine is None:
            raise ValueError("ReactAgent requires an engine (AugLLMConfig)")

        # Validate tools
        if not self.tools:
            logger.warning("ReactAgent created without tools - limited functionality")

        return self

    def build_graph(self) -> BaseGraph:
        """Build the ReAct reasoning graph.

        Creates a graph with:
        1. Reasoning node - decides what action to take
        2. Tool node - executes the selected tool
        3. Observation node - processes tool results
        4. Decision routing - continue or finish
        """
        graph = BaseGraph(
            name=f"{self.name}_react_graph", state_schema=self.state_schema
        )

        # Add reasoning node
        reasoning_config = EngineNodeConfig(
            engines={"reasoner": self.engine}, system_message=self._get_react_prompt()
        )
        graph.add_node("reason", reasoning_config)

        # Add tool node if tools available
        if self.tools:
            tool_config = ToolNodeConfig(tools=self.tools)
            graph.add_node("act", tool_config)

        # Add observation processing
        observation_config = EngineNodeConfig(
            engines={"observer": self.engine},
            system_message="Process the tool output and decide next steps.",
        )
        graph.add_node("observe", observation_config)

        # Set up routing
        graph.set_entry_point("reason")

        # Reasoning can go to action or end
        def should_act(state: dict[str, Any]) -> str:
            """Decide whether to use a tool or finish."""
            messages = state.get("messages", [])
            if not messages:
                return "act" if self.tools else END

            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content.lower()

                # Check if task is complete
                if any(
                    word in content for word in ["final answer", "complete", "finished"]
                ):
                    return END

                # Check if tool use is needed
                if self.tools and any(
                    word in content for word in ["use", "call", "need"]
                ):
                    return "act"

                # Check iteration limit
                if len(self.reasoning_history) >= self.max_iterations:
                    return END

            return "act" if self.tools else END

        graph.add_conditional_edges("reason", should_act)

        # Action goes to observation
        if self.tools:
            graph.add_edge("act", "observe")

        # Observation goes back to reasoning or ends
        def should_continue(state: dict[str, Any]) -> str:
            """Decide whether to continue reasoning."""
            # Check iteration limit
            if len(self.reasoning_history) >= self.max_iterations:
                return END

            # Check if we have a final answer
            messages = state.get("messages", [])
            if messages and isinstance(messages[-1], AIMessage):
                if "final answer" in messages[-1].content.lower():
                    return END

            return "reason"

        graph.add_conditional_edges("observe", should_continue)

        return graph

    def _get_react_prompt(self) -> str:
        """Get the ReAct system prompt."""
        if self.react_prompt:
            return self.react_prompt

        tool_descriptions = ""
        if self.tools:
            tool_descriptions = "\n\nAvailable tools:\n"
            for tool in self.tools:
                tool_descriptions += f"- {tool.name}: {tool.description}\n"

        return f"""You are a ReAct (Reasoning and Acting) agent.

Follow this pattern:
1. Thought: Analyze what you need to do
2. Action: Decide which tool to use (if any)
3. Observation: Process the tool output
4. ... (repeat as needed)
5. Final Answer: Provide the complete response

{tool_descriptions}

Always think step-by-step and explain your reasoning.
When you have enough information, provide a clear "Final Answer:".

Execution mode: {self.execution_mode}
Maximum iterations: {self.max_iterations}
"""

    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to the agent's toolkit.

        Args:
            tool: The tool to add
        """
        self.tools.append(tool)
        logger.info(f"Added tool '{tool.name}' to {self.name}")

    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool by name.

        Args:
            tool_name: Name of the tool to remove

        Returns:
            bool: True if tool was removed, False if not found
        """
        for i, tool in enumerate(self.tools):
            if tool.name == tool_name:
                self.tools.pop(i)
                logger.info(f"Removed tool '{tool_name}' from {self.name}")
                return True
        return False

    def get_tool_names(self) -> list[str]:
        """Get list of available tool names."""
        return [tool.name for tool in self.tools]

    def record_reasoning_step(
        self,
        thought: str,
        action: str | None = None,
        observation: str | None = None,
    ) -> None:
        """Record a reasoning step.

        Args:
            thought: The reasoning thought
            action: The action taken (if any)
            observation: The observation made (if any)
        """
        step = {
            "step": len(self.reasoning_history) + 1,
            "thought": thought,
            "action": action,
            "observation": observation,
        }
        self.reasoning_history.append(step)

    def get_reasoning_summary(self) -> str:
        """Get a summary of the reasoning process."""
        if not self.reasoning_history:
            return "No reasoning steps recorded yet."

        summary = f"Reasoning Summary ({len(self.reasoning_history)} steps):\n"
        for step in self.reasoning_history:
            summary += f"\nStep {step['step']}:\n"
            summary += f"  Thought: {step['thought'][:100]}...\n"
            if step["action"]:
                summary += f"  Action: {step['action']}\n"
            if step["observation"]:
                summary += f"  Observation: {step['observation'][:100]}...\n"

        return summary

    def reset_reasoning(self) -> None:
        """Reset the reasoning history."""
        self.reasoning_history.clear()
        logger.info(f"Reset reasoning history for {self.name}")
