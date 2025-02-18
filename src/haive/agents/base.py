from datetime import date
from typing import Callable, List, Union, Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
# Diff between the two 
from langchain_core.messages import SystemMessage, AIMessage,BaseMessage,AnyMessage
from langgraph.graph import StateGraph, END
from langgraph.types import Command,Send
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from src.haive.core.models.llm.base import LLMConfig

from src.haive.core.tools.search_tools import tavily_search_tool
#from src.haive.core.agents.react_agent.state_schema import ReactAgentState
from src.haive.utils.visualize_graph_utils import render_and_display_graph
from langchain_core.messages import filter_messages
from src.haive.core.models.embeddings.base import EmbeddingsConfig
from src.haive.core.aug_llm.base import AugLLMConfig,compose_runnable
#from src.agents.base import BaseAgentConfig

"""
class BaseGraphNode(BaseModel):
    runnable_config: CustomRunnableConfig
    agent_node:Callable 
    state_schema: Type[BaseModel]
    name:str = CustomRunnableConfig.name
    invoke_field:Field(default=messages)
    state_update:Union[Type[Command],Type[Send]]
    

class BaseAgent(BaseAgentConfig):
    def __init__(self, runnable_config  : CustomRunnableConfig):
        self.runnable_config = runnable_config
        #self.runnable=compose_runnable(self.runnable_config)
        #self.agent_node = self.create_agent_node
        self.runnable=None
        self.agent_node=None
    def create_runnable(self):
        self.runnable=compose_runnable(self.runnable_config)
    """
    #def create_agent_node(self, state: ReactAgentState) -> Command:
    #    """
    #    Default implementation of the agent node.
    #    """
    #    response = self.runnable.invoke(state["messages"])
    #    return Command(update={"messages": state["messages"] + [response]})
    
        #def __init__(self, runnable_config: CustomRunnableConfig):

#class BaseAgentArchitecureConfig(BaseAgentConfig)
#    state_schema: Type[BaseModel]

#class BaseAgentArchitecture(BaseAgentConfig):




from langgraph.graph import StateGraph
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import END
from langchain_core.messages import SystemMessage,HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from src.haive.core.tools.search_tools import tavily_search_tool
from langchain_core.messages import filter_messages
# Need to change
from src.haive.core.aug_llm.base import compose_runnable
from langchain_core.messages import AIMessage
from src.haive.core.aug_llm.base import AugLLMConfig
from typing import Union
from langchain_core.tools import BaseTool,StructuredTool

import uuid
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from typing import Callable,Dict,Any,List,Union,Type
from pydantic import field_validator



class AgentArchitectureConfig(BaseModel):
    aug_llm_config: Optional[AugLLMConfig] = Field(default=None,description="The configuration for the agent")
    aug_llm_configs: Optional[Dict[str,AugLLMConfig]] = Field(default=None,description="The configuration for the agent")
    runnable_config: RunnableConfig = Field(default={"configurable": {"thread_id": str(uuid.uuid4())}},description="The configuration for the agent")
    #add_model_runnable:bool=Field(default=False,description="Whether to add the model runnable")
    #tool_node_tools: Optional[List[Union[Tool,BaseTool,StructuredTool]]] = Field(default=[tavily_search_tool],description="The tools for the agent")
    state_schema: Union[Type[BaseModel],Dict[str,Any]] = Field(default=None,description="The state schema for the agent")
    should_setup_workflow:bool=Field(default=True,description="Whether to setup the workflow")
    should_compile_workflow:bool=Field(default=True,description="Whether to compile the graph")
    should_visualize_graph:bool=Field(default=False,description="Whether to visualize the graph")
    visualize_graph_output_name:Optional[str]=Field(default="agent_architecture_graph.png",description="The name of the output file for the graph")
    embeddings_config:Optional[EmbeddingsConfig]=Field(default=None,description="The configuration for the embeddings")
    default_input_dict:Optional[Dict[str,List]]=Field(default={"messages": [("user", "{}")]},description="The default input dictionary for the agent")
    default_input_schema:Union[Optional[BaseModel],Dict[str,Any]]=Field(default={"messages": [("user", "{}")]},description="The default input schema for the agent")
    # default ouput schema
    @field_validator("visualize_graph_output_name")
    def validate_visualize_graph_output_name(cls,v):
        if not v:
            raise ValueError("visualize_graph_output_name must be provided")
    @field_validator("aug_llm_config")
    def check_aug_llm_config_dependency(cls, v, values):
        if v and not values.get("aug_llm_configs"):
            raise ValueError("aug_llm_configs must be provided if aug_llm_config is set")
        return v
    def get_runnables(self):
        if self.llm_runnable_configs:
            return self.llm_runnable_configs
        elif self.llm_runnable_config:
            return {self.llm_runnable_config.name: self.llm_runnable_config}
        else:
            raise ValueError("No runnables provided")
        
    


class AgentArchitecture:
    def __init__(self,config:AgentArchitectureConfig):
        self.config = config
        #self.llm_runnable_configs = config.llm_runnable_configs
        #print(self.config)
        #print(config)
        if config.aug_llm_configs:
            self.aug_llm_configs = config.aug_llm_configs
            self.aug_llm_model_runnables_dict = config.aug_llm_configs
            self.aug_llm_model_runnables_dict = {k: compose_runnable(v) for k, v in self.aug_llm_model_runnables_dict.items()}
            #self.runnables = compose_runnables_from_dict(self.runnables)
            #pass # TODO: Implement this
            #self.runnables = config.llm_runnable_configs
            #if config.add_model_runnable:
                #self.model_runnable=compose_runnable(config.llm_runnable_config)
        elif config.aug_llm_config:
            self.aug_llm_runnable=compose_runnable(config.aug_llm_config)
        self.memory = MemorySaver()
        self.state_schema = config.state_schema
        self.runnable_config = config.runnable_config  
        self.graph = StateGraph(self.state_schema)
        self.input_dict = config.default_input_schema
        self.app = None  
        if config.should_setup_workflow:
            print("Setting up workflow")
            #print(self.model_runnable)
            self.setup_workflow()
            if config.should_compile_workflow and self.graph:
                self.compile_graph(checkpointer=self.memory)
            if config.should_visualize_graph:
                self.visualize_graph(config.visualize_graph_output_name)
    
    def setup_workflow(self):
        """ Overload this function in the child class """
        raise NotImplementedError("This function must be overloaded in the child class")
    
    def compile_workflow(self):
        if self.graph:
            if self.memory:
                self.app = self.graph.compile(checkpointer=self.memory)
            else:
                self.app = self.graph.compile()
        else:
            raise RuntimeError("Graph is not set up.")
    def visualize_graph(self,output_name:str="react_agent_graph.png"):
        if self.graph and self.app:
            render_and_display_graph(self.app, output_name=output_name)
        else:
            print("Graph is not set up.")
    
    def run(self, input_text: str):
        """
        Run the agent with the given input text.
        """
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            if self.memory:
                self.app = self.compile_graph(checkpointer=self.memory)
            else:
                self.app = self.compile_graph()
        
        # self.system_message, 
        inputs = {"messages": [("user", input)]}
        #print("Inputs:",inputs)
        if 'messages' in inputs:
            for output in self.app.stream(inputs, stream_mode="values", config=self.runnable_config,debug=True):
                message = output["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()
        else:
            for output in self.app.stream(inputs, stream_mode="values", config=self.runnable_config,debug=True):
                for k, v in output.items():
                    if k != "__end__":
                        print(v)
        #return output
    def format_input_dict(self,input_text:str): 
        if isinstance(self.input_dict,BaseModel):
            return self.input_dict.model_dump()
        elif isinstance(self.input_dict,Dict):
            return self.input_dict["messages"][0][-1].format(input_text)
        else:
            raise ValueError("Invalid input schema")
    def compile_graph(self,checkpointer:Union[MemorySaver,PostgresSaver]=None):
        """
        Compile the workflow graph.
        """
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        
        #print(self.graph)
        self.app=self.graph.compile(checkpointer=self.memory)
    async def arun(self, input_text: str=None,input_dict:Dict[str,Any]=None):
        """
        Run the agent with the given input text.
        """
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            if self.memory:
                self.app = self.compile_graph(checkpointer=self.memory)
            else:
                self.app = self.compile_graph()
        
        # self.system_message, 
        if input_text:
            inputs = {"messages": [("user", input_text)]}
        elif input_dict:
            inputs = input_dict
        else:
            raise ValueError("Either input_text or input_dict must be provided")
        #print("Inputs:",inputs)
        if 'messages' in inputs:
            async for output in self.app.astream(inputs, stream_mode="values", config=self.runnable_config):
                message = output["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()
                #return self.app.aget_state(self.runnable_config)
        else:
            async for output in self.app.astream(inputs, stream_mode="values", config=self.runnable_config,debug=True):
                for k, v in output.items():
                    if k != "__end__":
                        print(k)
                        print(v)
                        #print(self.app.get_state(self.runnable_config))
                        
        #return output
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
                    print("Goodbye!")
                    break
                #print(self.app.get_state(self.runnable_config))
                #self.run({"messages": [("user", user_input)]}, config=self.runnable_config, stream_mode="values")
                self.run(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print("Error:",e)
                print("State:",self.app.get_state(self.runnable_config))
                print("Messages:",self.app.get_state_history(self.runnable_config))
                print("Prompts:",self.app.get_prompts(self.runnable_config))
                if self.app.checkpointer:
                    print("checkpointer:",self.app.checkpointer)
        #self.node_name = config.node_name
        #self.core_routing_function = config.core_routing_function
        #self.conditional_routing_function_output_dict = config.conditional_routing_function_output_dict
        #self._initialize_tool_node()

