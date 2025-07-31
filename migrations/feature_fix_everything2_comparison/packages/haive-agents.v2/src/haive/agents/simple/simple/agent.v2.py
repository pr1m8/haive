"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    SimpleAgent: SimpleAgent implementation.
    Story: Story implementation.

Functions:
    has_tool_calls: Has Tool Calls functionality.
    check_if_should_use_tool: Check If Should Use Tool functionality.
    placeholder_node: Placeholder Node functionality.
"""

# src/haive/agents/simple/clean_agent.py

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field, field_validator

# Import the base Agent from the correct location
from haive.agents.base import Agent

logger = logging.getLogger(__name__)


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================


def has_tool_calls(state: dict[str, Any]) -> Literal["true", "false"]:
    """Check if the last message has tool calls."""
    messages = state.get("messages", [])
    if not messages:
        return "false"

    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "true"
    return "false"


def check_if_should_use_tool(state: dict[str, Any]) -> bool:
    """Check if the last message has tool calls."""
    last_msg = state.get("messages", [])[-1] if state.get("messages") else None
    if not last_msg:
        return False

    tool_calls = getattr(last_msg, "tool_calls", None)
    return bool(tool_calls)


def placeholder_node(state: dict[str, Any]):
    """Placeholder node that does nothing."""
    return Command(update={})


# ========================================================================
# SIMPLE AGENT - A minimal Agent implementation with AugLLMConfig
# ========================================================================


class SimpleAgent(Agent):
    """Simple agent that uses AugLLMConfig as its primary engine.

    This is the clean, minimal implementation that leverages the base Agent.
    All the complex logic is handled by the base Agent class - this just provides
    the SimpleAgent-specific convenience fields and graph building.

    The SimpleAgent is designed to be the most basic functional agent - essentially
    just Agent[AugLLMConfig] with convenience fields for common LLM parameters.

    Attributes:
        temperature: Optional temperature for the LLM (0.0-2.0). Syncs to engine.
        max_tokens: Optional max tokens for responses. Syncs to engine.
        model_name: Optional model name override. Syncs to engine.model.
        force_tool_use: Optional flag to force tool usage. Syncs to engine.
        structured_output_model: Optional Pydantic model for structured output.
        system_message: Optional system message override. Syncs to engine.
        llm_config: Optional LLM configuration dict or object.
        output_parser: Optional parser for processing LLM output.
        prompt_template: Optional custom prompt template.

    Examples:
        Basic usage::

            from haive.agents.simple import SimpleAgent
            from haive.core.engine.aug_llm import AugLLMConfig

            # Create with defaults
            agent = SimpleAgent(name="assistant")
            result = agent.run("Hello, how are you?")

        With configuration::

            agent = SimpleAgent(
                name="creative_writer",
                temperature=0.9,
                max_tokens=1000,
                system_message="You are a creative writer."
            )

        With structured output::

            from pydantic import BaseModel, Field

            class Story(BaseModel):
                title: str = Field(description="Story title")
                content: str = Field(description="Story content")
                genre: str = Field(description="Story genre")

            agent = SimpleAgent(
                name="story_writer",
                structured_output_model=Story
            )
            story = agent.run("Write a short sci-fi story")
            # story will be a Story instance

        With tools::

            from langchain_core.tools import tool

            @tool
            def calculator(expression: str) -> str:
                '''Calculate mathematical expressions.'''
                return str(eval(expression))

            config = AugLLMConfig(tools=[calculator])
            agent = SimpleAgent(name="math_assistant", engine=config)
            result = agent.run("What is 15 * 23?")

    Note:
        SimpleAgent always expects an AugLLMConfig engine. If none is provided,
        it creates one with default settings. The convenience fields (temperature,
        max_tokens, etc.) are synced to the engine during setup_agent().

    See Also:
        haive.agents.react.ReactAgent: For agents that need reasoning loops
        haive.agents.multi.MultiAgent: For coordinating multiple agents
        haive.core.engine.aug_llm.AugLLMConfig: The engine configuration
    """

    # ========================================================================
    # CONVENIENCE FIELDS (specific to SimpleAgent)
    # ========================================================================

    # These fields sync to the engine for convenience
    temperature: float | None = Field(
        default=None, description="Temperature for the LLM (syncs to engine)"
    )
    max_tokens: int | None = Field(
        default=None, description="Max tokens for the LLM (syncs to engine)"
    )
    model_name: str | None = Field(
        default=None, description="Model name for the LLM (syncs to engine.model)"
    )
    force_tool_use: bool | None = Field(
        default=None, description="Force tool use (syncs to engine)"
    )
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model (syncs to engine)"
    )
    system_message: str | None = Field(
        default=None, description="System message (syncs to engine)"
    )
    llm_config: LLMConfig | dict[str, Any] | None = Field(
        default=None, description="LLM config (syncs to engine)"
    )

    # SimpleAgent specific fields
    output_parser: BaseOutputParser | None = Field(
        default=None, description="Optional output parser"
    )
    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None, description="Optional prompt template"
    )

    # ========================================================================
    # ENGINE REQUIREMENT - SimpleAgent expects AugLLMConfig
    # ========================================================================

    @field_validator("engine", mode="before")
    @classmethod
    def ensure_aug_llm_config(cls, v):
        """Ensure engine is AugLLMConfig or create one."""
        if v is None:
            return AugLLMConfig()
        if isinstance(v, dict):
            return AugLLMConfig(**v)
        if not isinstance(v, AugLLMConfig):
            raise ValueError(f"SimpleAgent requires AugLLMConfig, got {type(v)}")
        return v

    # ========================================================================
    # SETUP - Sync convenience fields to engine
    # ========================================================================

    def setup_agent(self) -> None:
        """Sync convenience fields to engine and basic setup.

        This method is called during agent initialization to:
        1. Add the engine to the engines dict
        2. Sync all convenience fields to the engine
        3. Enable automatic schema generation

        The convenience fields (temperature, max_tokens, etc.) are copied
        to the engine configuration if they have non-None values.
        """
        if self.engine:
            # Add engine to engines dict
            self.engines["main"] = self.engine

            # Sync convenience fields to engine
            self._sync_convenience_fields()

            # Set schema flag for auto-generation
            self.set_schema = True

    def _sync_convenience_fields(self) -> None:
        """Sync convenience fields to engine."""
        if not self.engine:
            return

        # Sync all the convenience fields
        if self.temperature is not None:
            self.engine.temperature = self.temperature
        if self.max_tokens is not None:
            self.engine.max_tokens = self.max_tokens
        if self.model_name is not None:
            self.engine.model = self.model_name
        if self.force_tool_use is not None:
            self.engine.force_tool_use = self.force_tool_use
        if self.structured_output_model is not None:
            self.engine.structured_output_model = self.structured_output_model
        if self.system_message is not None:
            self.engine.system_message = self.system_message
        if self.llm_config is not None:
            self.engine.llm_config = self.llm_config

    # ========================================================================
    # GRAPH BUILDING - Simple graph for LLM + tools + parsing
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the simple agent graph.

        Creates a graph with the following structure based on agent configuration:

        1. Basic (no tools/parsing): START → agent_node → END
        2. With tools: START → agent_node → validation → tool_node → agent_node
        3. With parsing: START → agent_node → validation → parse_output → END
        4. With both: Combines tool and parsing flows

        The validation node routes between tools, parsing, or END based on
        the LLM output (tool calls, structured output needs, etc.).

        Returns:
            BaseGraph: The compiled agent graph ready for execution.

        Note:
            This method is called automatically during agent initialization.
            The graph structure adapts based on the presence of tools,
            structured output models, or output parsers.
        """
        graph = BaseGraph(name=self.name)

        # Add main agent node
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")

        # Check what additional nodes we need
        needs_tools = self._has_tools()
        needs_parsing = self._has_structured_output() or self.output_parser

        # Simple case - just LLM
        if not needs_tools and not needs_parsing:
            graph.add_edge("agent_node", END)
            return graph

        # Add tool node if needed
        if needs_tools:
            tool_config = ToolNodeConfig(name="tool_node", engine_name=self.engine.name)
            graph.add_node("tool_node", tool_config)

        # Add parser node if needed
        if needs_parsing:
            parser_config = ParserNodeConfigV2(
                name="parse_output", engine_name=self.engine.name
            )
            graph.add_node("parse_output", parser_config)

        # Add validation/routing if we have tools or parsing
        if needs_tools or needs_parsing:
            validation_config = ValidationNodeConfigV2(
                name="validation",
                engine_name=self.engine.name,
                tool_node="tool_node" if needs_tools else None,
                parser_node="parse_output" if needs_parsing else None,
            )
            graph.add_node("validation", validation_config)

            # Route from agent to validation
            if self.force_tool_use or self._always_needs_validation():
                graph.add_edge("agent_node", "validation")
            else:
                graph.add_conditional_edges(
                    "agent_node", has_tool_calls, {True: "validation", False: END}
                )

        return graph

    def _has_tools(self) -> bool:
        """Check if agent has tools."""
        return bool(self.engine and getattr(self.engine, "tools", None))

    def _has_structured_output(self) -> bool:
        """Check if agent has structured output."""
        return bool(
            self.structured_output_model
            or (self.engine and getattr(self.engine, "structured_output_model", None))
        )

    def _always_needs_validation(self) -> bool:
        """Check if we always need validation (structured output or parser)."""
        return self._has_structured_output() or bool(self.output_parser)
