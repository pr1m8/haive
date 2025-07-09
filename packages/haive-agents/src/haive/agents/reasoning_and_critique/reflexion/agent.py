from collections.abc import Callable

from agents.reflexion.config import ReflexionConfig
from agents.reflexion.responder_with_retries import ResponderWithRetries

# from haive_agents.reflexion.aug_llms import initial_answer_chain,revision_chain
from agents.reflexion.utils import _get_num_iterations
from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.branches import Branch
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph import END, START
from langgraph.prebuilt import ToolNode
from langgraph.types import Command


@register_agent(ReflexionConfig)
class ReflexionAgent(Agent[ReflexionConfig]):
    """Agent that uses Reflexion to answer questions."""

    config: ReflexionConfig

    def __init__(self, config: ReflexionConfig = ReflexionConfig()):
        self.config = config
        self.responder = ResponderWithRetries(
            config.engines["responder"], config.attempts, name="responder"
        )
        self.revisor = ResponderWithRetries(
            config.engines["revisor"], config.attempts, name="revisor"
        )
        self.answer_writer = AugLLMConfig(model="gpt-4o", name="answer_writer")
        self.tool_node = self.create_tool_node(config.tools)
        self.event_loop_branch = Branch(
            function=lambda state: _get_num_iterations(state)
            > self.config.max_iterations,
            destinations={True: "end", False: "execute_tools"},
        )
        # self.tool_node_tools = []
        super().__init__(config)

    def create_tool_node(self, tools: list[BaseTool | Callable]) -> ToolNode:
        """Create a tool node from a list of tools.

        Args:
            tools: list of tools to create a tool node from
        Returns:
           ToolNode: a tool node from the list of tools
        """
        tool_node_tools = []
        for tool in self.config.tools:
            for model in self.config.models:
                tool_node_tools.append(
                    StructuredTool.from_function(tool, name=model.__name__)
                )
                print(f"Tool {model.__name__} added to tool node")
        return ToolNode(tools=tool_node_tools)

    def final_answer(self, state: dict):
        """Final answer tool."""
        prompt = PromptTemplate.from_template(
            """Given the folllowing converstaion, and user request, write out the final response.
            Conversation:
            {conversation}
            """
        )
        self.answer_writer.prompt_template = prompt
        aug_llm = self.answer_writer.create_runnable()
        response = aug_llm.invoke(input={"conversation": state.model_dump()})

        return Command(update={"answer": response})

    def setup_workflow(self) -> None:
        self.graph.add_node("draft", self.responder.respond)
        self.graph.add_edge(START, "draft")
        self.graph.add_node("tools", self.tool_node)
        self.graph.add_edge("draft", "tools")
        self.graph.add_node("revision", self.revisor.respond)
        # self.graph.add_edge("revision","draft")
        # self.graph.add_edge("draft","end")
        # self.graph.add_edge("revision","end")
        self.graph.add_node("final_answer", self.final_answer)
        self.graph.add_edge("tools", "revision")
        # return super().setup_workflow()
        self.graph.add_edge("final_answer", END)
        self.graph.add_conditional_edges(
            "revision",
            self.event_loop_branch.evaluate,
            {"execute_tools": "tools", "end": "final_answer"},
        )
