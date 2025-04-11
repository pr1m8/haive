from typing import Annotated, Sequence, Optional, Union, Callable, Type, List, Dict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph.message import add_messages
from langgraph.managed import RemainingSteps, IsLastStep
from langgraph.graph import END
from langgraph.prebuilt.tool_node import ToolNode, convert_pydantic_model_to_tool

from src.haive.agents.simple.agent import SimpleAgent, SimpleAgentConfig, register_agent
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.core.graph.GraphBuilder import DynamicGraph

# ================================
# ReactAgent State Schema
# ================================
class ReactAgentSchema(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(default=[])
    remaining_steps: RemainingSteps = Field(default=25)
    is_last_step: IsLastStep = False
    structured_response: Optional[BaseModel] = None
    final_output: Optional[str] = None
    tool_results: Dict[str, str] = Field(default_factory=dict)

# ================================
# ReactAgent Config
# ================================
class ReactAgentConfig(SimpleAgentConfig):
    tools: Optional[Union[
        List[Union[BaseTool, StructuredTool, Callable, Type[BaseModel]]],
        Dict[str, List[Union[BaseTool, StructuredTool, Callable, Type[BaseModel]]]]
    ]] = Field(default_factory=list)

    structured_output_model: Optional[Type[BaseModel]] = None
    state_schema: Type[BaseModel] = Field(default=ReactAgentSchema)

    @classmethod
    def from_aug_llm_with_tools(cls, aug_llm, tools, **kwargs):
        return cls(engine=aug_llm, tools=tools, **kwargs)

# ================================
# Tool Utility Helpers
# ================================
def normalize_tools_input(tools) -> Dict[str, List[BaseTool]]:
    if isinstance(tools, list):
        return {"default": [_normalize_tool(t) for t in tools]}
    return {k: [_normalize_tool(t) for t in v] for k, v in tools.items()}

def _normalize_tool(tool) -> BaseTool:
    if isinstance(tool, (BaseTool, StructuredTool)):
        return tool
    if isinstance(tool, type) and issubclass(tool, BaseModel):
        return convert_pydantic_model_to_tool(tool)
    if callable(tool):
        return StructuredTool.from_function(tool)
    raise ValueError(f"Unsupported tool type: {type(tool)}")

def create_tool_router(tool_map: Dict[str, List[BaseTool]]) -> Callable:
    tool_name_to_group = {}
    for group, tools in tool_map.items():
        for tool in tools:
            tool_name_to_group[tool.name] = group

    def router(state):
        last_msg = state["messages"][-1]
        if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
            return tool_name_to_group.get(last_msg.tool_calls[0]["name"], "default")
        return END

    return router

# ================================
# ReactAgent Class
# ================================
@register_agent(ReactAgentConfig)
class ReactAgent(SimpleAgent):
    def setup_workflow(self):
        gb = DynamicGraph(
            components=[self.config.engine],
            state_schema=self.config.state_schema
        )

        # Add core reasoning node
        gb.add_node(
            name=self.config.node_name,
            config=self.config.engine,
            command_goto=self._get_tool_entrypoint(),
        )

        # Add tool routing logic if tools exist
        if self.config.tools:
            tool_groups = normalize_tools_input(self.config.tools)
            router_fn = create_tool_router(tool_groups)

            for group_name, tools in tool_groups.items():
                gb.add_node(group_name, ToolNode(tools), command_goto=self.config.node_name)

            gb.add_conditional_router(
                from_node=self.config.node_name,
                condition=router_fn,
                path_map=list(tool_groups.keys()) + self._get_final_routes()
            )

        # Add structured output node if needed
        if self.config.structured_output_model:
            from langchain_core.output_parsers.openai_tools import PydanticToolsParser
            structured = AugLLMConfig(
                name="structured_output",
                llm_config=self.config.engine.llm_config,
                prompt_template=self.config.engine.prompt_template,
                structured_output_model=self.config.structured_output_model,
                output_parser=PydanticToolsParser(tools=[self.config.structured_output_model])
            )
            gb.add_node("structured_output_node", structured, command_goto=END)

        self.graph = gb.build()
        self.app = self.graph.compile(checkpointer=self.memory)

    def _get_tool_entrypoint(self) -> str:
        if self.config.tools:
            return "TOOL_ROUTER"  # placeholder for dynamic router resolution
        elif self.config.structured_output_model:
            return "structured_output_node"
        return END

    def _get_final_routes(self) -> List[str]:
        return ["structured_output_node"] if self.config.structured_output_model else [END]  
