import uuid
from collections.abc import Callable
from typing import Any

from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig, AugLLMFactory
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.utils.visualize_graph_utils import render_and_display_graph
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import SystemMessage, filter_messages
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool, Tool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from pydantic import BaseModel, Field, field_validator

from haive.agents.react_class.react_agent.aug_llms import (
    default_react_llm_runnable_config,
)
from haive.agents.react_class.react_agent.state import ReactAgentState


# Utility function to determine whether to continue execution
def should_continue(state: ReactAgentState) -> str:
    messages = filter_messages(state["messages"], exclude_types=[SystemMessage])
    last_message = messages[-1]
    if last_message.tool_calls:
        return "continue"
    return "end"


default_react_should_continue_output_dict = {"continue": "tool_node", "end": END}


# ==============================
# 🚀 ReactAgentConfig (Fixed & Improved)
# ==============================
class ReactAgentConfig(AgentConfig):
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4o")),
        description="LLM configuration for the ReactAgent.",
    )
    aug_llm_config: AugLLMConfig = Field(
        default=default_react_llm_runnable_config,
        description="The AugLLM configuration for the agent.",
    )
    tools: list[Tool | BaseTool | StructuredTool] = Field(
        default_factory=list,  # Ensure it's never `None`
        description="The tools available to the agent.",
    )
    runnable_config: RunnableConfig = Field(
        default_factory=lambda: {"configurable": {"thread_id": str(uuid.uuid4())}},
        description="Configuration for the agent's runnable execution.",
    )
    tool_node_tools: list[Tool | BaseTool | StructuredTool] = Field(
        default_factory=lambda: [tavily_search_tool],
        description="Tools used in the ToolNode of the agent.",
    )
    state_schema: type[BaseModel] | dict[str, Any] | Any = Field(
        default=ReactAgentState, description="State schema defining the agent's state."
    )
    core_routing_function: Callable = Field(
        default=should_continue,
        description="Function that determines whether to continue execution.",
    )
    conditional_routing_function_output_dict: dict[str, Any] = Field(
        default=default_react_should_continue_output_dict,
        description="Dictionary defining routing behavior.",
    )
    node_name: str = Field(
        default="agent_node", description="The name of the agent node."
    )
    should_setup_workflow: bool = Field(
        default=True, description="Whether to set up the workflow."
    )
    should_compile: bool = Field(
        default=True, description="Whether to compile the graph."
    )
    should_visualize_graph: bool = Field(
        default=False, description="Whether to visualize the graph."
    )
    visualize_graph_output_name: str | None = Field(
        default=None, description="Output file for graph visualization."
    )
    structured_output_model: BaseModel | None = Field(
        default=None, description="Schema for structured output."
    )
    default_agent_node: Callable | None = Field(
        default=None, description="The default agent node function."
    )

    # ==============================
    # 🛠 Validators & Pre-processing
    # ==============================

    @field_validator("engine", mode="after")
    @classmethod
    def validate_engine(cls, v):
        """Ensure `engine` is always provided and valid."""
        if not v:
            raise ValueError(
                "An 'engine' must be provided (AugLLMConfig or another AgentArchitectureConfig)."
            )
        return v

    @field_validator("tools", "tool_node_tools", mode="before")
    @classmethod
    def ensure_list(cls, v):
        """Ensure tools are always a list."""
        if v is None:
            return []
        if not isinstance(v, list):
            raise TypeError(f"Expected a list, but got {type(v).__name__}.")
        return v

    @field_validator("structured_output_model", mode="before")
    def ensure_serializable(self, v):
        """Ensure structured output schema is serializable."""
        if v is not None and not isinstance(v, type) and not issubclass(v, BaseModel):
            raise TypeError(
                "structured_output_model must be a subclass of Pydantic BaseModel."
            )
        return v

    def build_agent(self) -> "ReactAgent":
        return ReactAgent(config=self)


# ============================
# 🚀 ReactAgent Implementation
# ============================
@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    def __init__(self, config: ReactAgentConfig = ReactAgentConfig()):

        # ✅ Initialize Tools
        self.llm_tools = config.tools or []
        self.tool_node_tools = config.tool_node_tools or self.llm_tools
        self.create_tool_node = bool(self.tool_node_tools)

        # ✅ Initialize Agent Node
        self.agent_node_fn = config.default_agent_node or self.default_agent_node
        self.aug_llm_model = AugLLMFactory(config.engine).runnable
        # ✅ Initialize Graph Components
        self.node_name = config.node_name
        self.core_routing_function = config.core_routing_function
        self.conditional_routing_function_output_dict = (
            config.conditional_routing_function_output_dict
        )
        self.tool_node = None
        self._initialize_tool_node()

        # ✅ Setup Graph
        super().__init__(config)

    def _initialize_tool_node(self):
        """Initialize ToolNode if required."""
        if self.create_tool_node:
            self.tool_node = ToolNode(self.tool_node_tools)

    def default_agent_node(self, state: ReactAgentState) -> Command:
        """Default implementation of the agent node."""
        response = self.aug_llm_model.invoke(
            {"messages": state["messages"]}, config=self.runnable_config
        )
        return Command(update={"messages": state["messages"] + [response]})

    def default_agent_node_without_tool_node(self, state: ReactAgentState) -> Command:
        """Agent node implementation when ToolNode is not used."""
        response = self.aug_llm_model.invoke(state["messages"])
        return Command(update={"messages": state["messages"] + [response]})

    def replace_agent_node(self, new_agent_node: Callable):
        """Replace the agent node function."""
        self.agent_node_fn = new_agent_node
        if self.graph:
            self.graph.remove_node(self.node_name)
            self.graph.add_node(self.node_name, new_agent_node)

    def structured_output_agent_node(self, state: ReactAgentState) -> Command:
        """Agent node implementation when structured output is required."""
        response = self.aug_llm_model.invoke(
            {"messages": state["messages"]}, config=self.runnable_config
        )
        return Command(update={"messages": state["messages"] + [response]})

    def setup_workflow(self):
        """Configure the workflow graph."""
        if self.create_tool_node:
            self.graph.add_node("tool_node", self.tool_node)
        self.graph.add_node(self.node_name, self.agent_node_fn)

        self.graph.set_entry_point(self.node_name)

        if self.create_tool_node:
            self.graph.add_conditional_edges(
                self.node_name,
                self.core_routing_function,
                self.conditional_routing_function_output_dict,
            )
            self.graph.add_edge("tool_node", self.node_name)
        else:
            self.graph.add_edge(self.node_name, END)

    def visualize_graph(self, output_name: str = "react_agent_graph.png"):
        """Visualize the workflow graph."""
        if self.graph and self.app:
            render_and_display_graph(self.app, output_name=output_name)

    def run(self, input_text: str):
        """Run the agent."""
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            self.compile_graph()
        inputs = {"messages": [("user", input_text)]}
        for output in self.app.stream(
            inputs, stream_mode="values", config=self.runnable_config
        ):
            output["messages"][-1]

    def chat(self):
        """Interactive chat loop."""
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    break
                self.run(user_input)
            except KeyboardInterrupt:
                break
            except Exception:
                pass


# ============================
# 🚀 Factory Methods for Usage
# ============================
def create_react_agent(config: ReactAgentConfig = ReactAgentConfig()) -> ReactAgent:
    """Factory function to create a ReactAgent."""
    return ReactAgent(config=config)


def run_react_agent(input_text: str, config: ReactAgentConfig = ReactAgentConfig()):
    """Execute ReactAgent with a given input."""
    return create_react_agent(config).app.invoke(
        {"messages": [("user", input_text)]}, config=config.runnable_config
    )


def chat_react_agent(config: ReactAgentConfig = ReactAgentConfig()):
    """Start a chat session with ReactAgent."""
    return create_react_agent(config).chat()


def chat_react_agent_with_tool_node(config: ReactAgentConfig = ReactAgentConfig()):
    """Start a chat session with ReactAgent."""
    return create_react_agent(config).chat()
