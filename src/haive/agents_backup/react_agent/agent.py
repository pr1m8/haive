from datetime import date
from typing import Callable, List, Union, Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
#from src.haive.core.models.llm import 
#from src.haive.core.models.llm.base import create_llm
from src.haive.core.tools.search_tools import tavily_search_tool
#from src.haive.agents.react_agent_v2.state_schema import ReactAgentState
#from src.haive.core.utils.visualize_graph_utils import render_and_display_graph
from langchain_core.messages import filter_messages
from src.haive.core.engine.agent.agent import AgentArchitectureConfig,AgentArchitecture
from src.haive.core.engine.aug_llm import AugLLMConfig
from typing import Dict,Any
from langchain_core.tools import BaseTool,StructuredTool
from src.haive.agents.react_agent.aug_llms import default_react_llm_runnable_config
from langgraph.checkpoint.postgres import PostgresSaver
import uuid
from langchain_core.runnables import RunnableConfig
from src.haive.agents.react_agent.state import ReactAgentState
from src.haive.utils.visualize_graph_utils import render_and_display_graph
# Utility function to decide whether to continue
def should_continue(state: ReactAgentState, tool_node_name: str = "tools",) -> str:
    messages = filter_messages(state["messages"], exclude_types=[SystemMessage])
    last_message = messages[-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

default_react_should_continue_output_dict = {"continue": "tool_node", "end": END}

class ReactAgentConfig(AgentArchitectureConfig):
    aug_llm_config: AugLLMConfig = Field(default=default_react_llm_runnable_config,description="The configuration for the agent")
    #llm_config: LLMConfig  = Field(default=LLMConfig(),description="The configuration for the LLM")
    # Check tool - there is a better definition for this. 
    #llm_runnable_config: LLMRunnableConfig = Field(default=default_react_llm_runnable_config,description="The configuration for the agent")
    tools: Optional[Union[List[Tool],List[BaseTool],List[StructuredTool]]] = Field(default=None,description="The tools for the agent")
    #role: str = Field(default="agent",description="The role of the agent")
    runnable_config: Optional[RunnableConfig] = Field(default={"configurable": {"thread_id": str(uuid.uuid4())}},description="The configuration for the agent")
    # Get the prompt to use - you can modify this!
    tool_node_tools: Optional[List[Union[Tool,BaseTool,StructuredTool]]] = Field(default=[tavily_search_tool],description="The tools for the agent")
    state_schema: Union[BaseModel,Dict[str,Any],Any] = Field(default=ReactAgentState,description="The state schema for the agent")
    #chekpointer: Union[MemorySaver,PostgresSaver] = Field(default=MemorySaver(),description="The checkpoint for the agent")
    core_routing_function: Callable = Field(default=should_continue,description="The continue function for the agent")
    #node_name:str=Field(default="agent_node",description="The name of the agent node")

    conditional_routing_function_output_dict: Dict[str,Any] = Field(default={"continue": "tool_node", "end": END},description="The conditional routing function for the agent")
    node_name:str=Field(default="agent_node",description="The name of the agent node")
    should_setup_workflow:bool=Field(default=False,         description="Whether to setup the workflow")
    should_compile_workflow:bool=Field(default=False,description="Whether to compile the graph")
    # Update this 
    should_visualize_graph:bool=Field(default=False,description="Whether to visualize the graph")
    visualize_graph_output_name:Optional[str]=Field(default=None,description="The name of the output file for the graph")
    structured_output_schema:Optional[BaseModel]=Field(default=None,description="The structured output schema for the agent")
    # Memory ? 
    default_agent_node:Optional[Callable]=Field(default=None,description="The default agent node for the agent")
    # Add uuid to this as well as model. 
    

class ReactAgent(AgentArchitecture):
    #memory: MemorySaver = Field(default=MemorySaver(),description="The memory for the agent")
    def __init__(
        self,
        config: ReactAgentConfig = ReactAgentConfig(),   
        #llm_config: LLMConfig = LLMConfig(),
        #tools: Optional[List[Tool]] = None, 
        #llm_tools: Optional[List] = None,
        #tool_node_tools: Optional[List[Tool]] = None,
        ##create_tool_node: bool = True,  # Dynamically decide based on llm_tools
        #config: dict = {"configurable": {"thread_id": "49"}},
        #state_schema: Type[ReactAgentState] = ReactAgentState,
        #system_prompt: str = "You are a helpful AI assistant, capable of using tools and escalating tasks as needed. You can invoke tools multiple times if prompted to perform a task, and continue on prompting yourself until the task is done.",
        #memory: MemorySaver = MemorySaver(),
        #node_name: str = "agent_node",
        #setup_workflow: bool = True,
        #compile_workflow: bool = True,
        #agent_node: Optional[Callable] = None,
        #structured_output_schema: Optional[BaseModel] = None,
        #core_routing_function: Optional[Callable] = should_continue,
        #conditional_routing_function_output_dict: Optional[dict] = {"continue": "tool_node", "end": END},
    ):
        # Handle tool parsing. 
        if config.tools:
            config.aug_llm_config.tools.append(tool for tool in config.tools if tool not in config.aug_llm_config.tools)
        
        #self.setup_workflow=config.setup_workflow
        #super().__init__(config=config)
        #self.aug_llm_runnable = compose_runnable(config.aug_llm_config)

        # Shared tools logic
        self.llm_tools = config.tools or []  # If tools provided, use for both llm_tools and tool_node_tools
        
        self.tool_node_tools =  config.tool_node_tools if config.tool_node_tools else self.llm_tools  # If tools provided, use for both llm_tools and tool_node_tools
        #stools = self.runnable_config.tools or []  # If tools provided, use for both llm_tools and tool_node_tools
        #llm_tools = self.llm_runnable_config.tools or tools  # Default llm_tools to tools
        #tool_node_tools = self.tool_node_tools or tools  # Default tool_node_tools to tools

        # Set create_tool_node based on presence of tools
        self.create_tool_node = True if self.tool_node_tools else False
        #self.llm = create_llm(llm_config)
        
        #self.llm_tools = llm_tools or []
        ##print("llm_tools:",self.llm_tools)
        #self.tool_node_tools = tool_node_tools
        #self.create_tool_node = create_tool_node if create_tool_node is not None else bool(self.llm_tools)
        
        #self.tools = tools or []
        #self.memory = MemorySaver()
        # memory  =self.me
        #self.state_schema = config.state_schema
        #self.runnable_config = config.runnable_config    
        self.node_name = config.node_name
        #self.system_prompt = self._initialize_system_prompt(system_prompt)
        #self.system_message = SystemMessage(self.system_prompt)
        self.agent_node_fn = config.default_agent_node if config.default_agent_node else self.default_agent_node
        #self.structured_output_schema = structured_output_schema
        #self.graph = None
        #self.app = None
        self.tool_node = None
        self.core_routing_function = config.core_routing_function
        # Handle
        self.conditional_routing_function_output_dict = config.conditional_routing_function_output_dict
        self._initialize_tool_node()
        #self.runnable = compose_runnable(self.llm_runnable_config)
        self.system_prompt_init = False
        #if config.setup_workflow:
        #    self.setup_workflow()
        #    #print("Workflow setup")
        #    #print(self.graph)
        #if config.compile_workflow and self.graph:
        #     self.compile_graph()
        super().__init__(config=config)
        #print(self.aug_llm_runnable)
        self.setup_workflow()
        self.compile_graph()
        #self.aug_llm_runnable_input = self.aug_llm_runnable.get_input_schema().model_fields.keys()
        ##print("Model Runnable Input:",self.model_runnable_input)
   
    def _initialize_tool_node(self):
        """
        Initialize tools for ToolNode and bind tools to the LLM.
        """
        # Configure ToolNode if required
        if self.create_tool_node:
            if self.tool_node_tools:
                self.tool_node = ToolNode(self.tool_node_tools)
            elif self.llm_tools:  # Use llm_tools if tool_node_tools is not defined
                self.tool_node = ToolNode(self.llm_tools)
        else:
            self.tool_node = None

       

    def default_agent_node(self, state: ReactAgentState) -> Command:
        """
        Default implementation of the agent node.
        """
        ##print(dir(self.model_runnable.json))
        ##print(self.model_runnable.get_input_schema().model_fields)
        ##print(dir(self.model_runnable.get_input_schema()))
        # Use runnable config with above to get the input schema. 
        # We should look into multi llm chians 
        # We shoudl also look into async optins. 
        #print(self.aug_llm_runnable)
        ##print(state)
        response = self.aug_llm_runnable.invoke({"messages":state["messages"]}, config=self.runnable_config,debug=True)
        return Command(update={"messages": state["messages"] + [response]})
    
    # Structured output needs to be fixed. 
    def default_agent_node_without_tool_node(self, state: ReactAgentState) -> Command:
        """
        Default implementation of the agent node when ToolNode is NOT present.
        Handles multiple tool calls directly.
        """
        response = self.aug_llm_runnable.invoke(state["messages"], self.runnable_config)

        # Check if there are multiple tool calls
        if response.tool_calls:
            updated_messages = state["messages"] + [response]
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["input"]

                # Find and execute each tool
                tool = next((t for t in self.llm_tools if t.name == tool_name), None)
                if tool:
                    try:
                        tool_result = tool.func(tool_input)

                        # Append tool result to messages
                        tool_result_message = AIMessage(
                            content=f"Result from tool '{tool_name}': {tool_result}"
                        )
                        updated_messages.append(tool_result_message)
                    except Exception as e:
                        # Handle tool execution errors
                        error_message = AIMessage(
                            content=f"Tool '{tool_name}' encountered an error: {str(e)}"
                        )
                        updated_messages.append(error_message)

            # Return the updated state
            return Command(update={"messages": updated_messages})

        # Return the original response if no tool was invoked
        return Command(update={"messages": state["messages"] + [response]})



    def replace_agent_node(self, new_agent_node: Callable):
        """
        Replace the agent node function and update the workflow graph.
        """
        self.agent_node_fn = new_agent_node
        if self.graph:
            self.graph.remove_node(self.node_name)
            self.graph.add_node(self.node_name, new_agent_node)
    #def add_structured_output_schema(self,schema:BaseModel):

    #def structure_output(self,schema:BaseModel):
    #    """
    #    Structure the output of the agent.
     #   """
     #   response = self.model_runnable.invoke({"messages": state["messages"]}, config=self.runnable_config).with_structured_output(schema)
     #   Command(update={"messages": state["messages"] + [response]})
    
    def setup_workflow(self):
        """
        Configure the workflow graph.
        """
        if self.llm_tools and not self.create_tool_node:
            self.graph.add_node(self.node_name, self.default_agent_node_without_tool_node)
        elif self.llm_tools and self.create_tool_node:
            self.graph.add_node(self.node_name, self.default_agent_node)
        else:
            self.graph.add_node(self.node_name, self.agent_node_fn)
        self.graph.set_entry_point(self.node_name)
        
        if self.create_tool_node:
            self.graph.add_node("tool_node", self.tool_node)
            self.graph.add_conditional_edges(
                self.node_name,
                self.core_routing_function,
                self.conditional_routing_function_output_dict,
            )
            self.graph.add_edge("tool_node", self.node_name)
        else:
            self.graph.add_edge(self.node_name, END)

    

    def visualize_graph(self,output_name:str="react_agent_graph.png"):
        """
        Visualize the workflow graph.
        """
        if self.graph and self.app:
            render_and_display_graph(self.app, output_name=output_name)
        else:
            print("Graph is not set up.")
    def system_message_run(self,):
        """
        Run the agent with the given input text.
        """
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            self.app = self.compile_graph()
        inputs = {"messages": [self.system_message]}
        ##print("Inputs:",inputs)
        for output in self.app.stream(inputs, stream_mode="values", config=self.runnable_config):
            message = output["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
        self.system_prompt_init = True
    
    
    def run(self, input_text: str,config:Optional[RunnableConfig]=None):
        """
        Run the agent with the given input text.
        """
        if not config:
            config = self.runnable_config
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            if self.memory:
                self.app = self.compile_graph(checkpointer=self.memory)
            else:
                self.app = self.compile_graph()
        # self.system_message, 
        inputs = {"messages": [("user", input_text)]}
        ##print("Inputs:",inputs)
        for output in self.app.stream(inputs, stream_mode="values", config=config,debug=True):
            message = output["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
        ##print("State:",self.app.get_state(self.runnable_config))
        ##print("Messages:",self.app.get_state_history(self.runnable_config))
        ##print("Prompts:",self.app.get_prompts(self.runnable_config))
            ##print(output["messages"][-1].get("content", ""))

    def chat(self):
        """
        Interactive chat loop.
        """
        while True:
            #self.system_message_run()
            #self.run()
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    #print("Goodbye!")
                    break
                ##print(self.app.get_state(self.runnable_config))
                #self.run({"messages": [("user", user_input)]}, config=self.runnable_config, stream_mode="values")
                self.run(user_input)
            except KeyboardInterrupt:
                #print("\nGoodbye!")
                break
            except Exception as e:
                print("Error:",e)
                #print("State:",self.app.get_state(self.runnable_config))
                #print("Messages:",self.app.get_state_history(self.runnable_config))
                #print("Prompts:",self.app.get_prompts(self.runnable_config))
    @classmethod
    def create_react_agent(cls, config: ReactAgentConfig = ReactAgentConfig()):
        return cls(config=config)

def create_react_agent(config: ReactAgentConfig = ReactAgentConfig()):
    return ReactAgent(config=config)

def run_react_agent(input_text: str, config: ReactAgentConfig = ReactAgentConfig()):
    return create_react_agent(config).app.invoke({"messages": [("user", input_text)]}, config=config.runnable_config)
def chat_react_agent(config: ReactAgentConfig = ReactAgentConfig()):
    return create_react_agent(config).chat()
# Example Usage
#config = ReactAgentConfig(tools=[tavily_search_tool])
#config = ReactAgentConfig(llm_runnable_config=react_llm_runnable_config,tools=[tavily_search_tool])
#gent = ReactAgent(
    #llm_config=,
    #tools=[tavily_search_tool],
    #state_schema=ReactAgentState,
    #setup_workflow=True,
    #config=ReactAgentConfig(tools=[tavily_search_tool])
 #   )
#agent = ReactAgent()
#agent.system_message_run()
#agent.system_message_run()
#agent.chat()
#agent.run(input_text="Resarch langgraph you can use multiple tool calls and agent calls")