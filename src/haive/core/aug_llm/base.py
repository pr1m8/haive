from pydantic import BaseModel, Field
from typing import Optional, List, Type, Dict, Any,Union
from langchain_core.tools import BaseTool
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BasePromptTemplate
from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig
from langchain_core.tools import StructuredTool
class AugLLMConfig(BaseModel):
    """
    Configuration for creating a runnable pipeline.
    """
    name: Optional[str] = Field(default="runnable", description="The name of the runnable")
    llm_config: Optional[LLMConfig] = Field(
        default=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        description="Configuration for the LLM",
    )  
    prompt_template: Optional[BasePromptTemplate] = None  
    tools: Optional[List[Type[Union[BaseTool,BaseModel,StructuredTool]]]] = None  # Tools must be classes (structured tools)
    structured_output_model: Optional[Type[BaseModel]] = None  
    output_parser: Optional[BaseOutputParser] = None  
    tool_kwargs: Optional[Dict[str, Dict[str, Any]]] = Field(default_factory=dict, description="Tool instantiation kwargs")
    bind_tools_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Kwargs for binding tools")
    bind_tools_config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Configuration for bind_tools")

class AugLLMFactory:
    """
    Factory for creating runnables.
    """
    def __init__(self, aug_config: AugLLMConfig):
        self.aug_config = aug_config
        self.llm_config = aug_config.llm_config
        self.prompt_template = aug_config.prompt_template
        self.tools = aug_config.tools or []
        self.structured_output_model = aug_config.structured_output_model
        self.output_parser = aug_config.output_parser
        self.tool_kwargs = aug_config.tool_kwargs
        self.bind_tools_kwargs = aug_config.bind_tools_kwargs
        self.bind_tools_config = aug_config.bind_tools_config

        self.runnable_llm = self.initialize_llm()
        self.runnable_llm = self.initialize_llm_with_tools() if self.tools else self.runnable_llm
        self.runnable_llm = self.initialize_llm_with_structured_output() if self.structured_output_model else self.runnable_llm
        self.runnable_llm = self.initialize_llm_with_output_parser() if self.output_parser else self.runnable_llm

        self.runnable = self.create_runnable()

    def initialize_llm(self):
        return self.llm_config.instantiate_llm()

    def initialize_llm_with_tools(self):
        """
        Bind tools with instantiation kwargs, bind_tools kwargs, and bind_tools config.
        """
        instantiated_tools = []
        for tool_cls in self.tools:
            tool_name = tool_cls.__name__
            tool_kwargs = self.tool_kwargs.get(tool_name, {})
            instantiated_tool = tool_cls(**tool_kwargs) if tool_kwargs else tool_cls()
            instantiated_tools.append(instantiated_tool)

        return self.runnable_llm.bind_tools(
            instantiated_tools, 
            **self.bind_tools_kwargs
        ).with_config(**self.bind_tools_config)

    def initialize_llm_with_structured_output(self):
        return self.runnable_llm.with_structured_output(self.structured_output_model)

    def initialize_llm_with_output_parser(self):
        return self.runnable_llm | self.output_parser

    def create_runnable(self):
        if self.prompt_template:
            return self.prompt_template | self.runnable_llm
        return self.runnable_llm

def compose_runnable(runnable_config: AugLLMConfig):
    try:
        return AugLLMFactory(runnable_config).runnable
    except Exception as e:
        print("Error composing runnable:", e)
        return None

def create_runnables_dict(runnables: List[AugLLMConfig]) -> Dict[str, AugLLMConfig]:
    return {runnable.name: runnable for runnable in runnables}

def compose_runnables_from_dict(runnables: Dict[str, AugLLMConfig]) -> Dict[str, AugLLMConfig]:
    for key, aug_runnable_config in runnables.items():
        if isinstance(aug_runnable_config, AugLLMConfig):
            runnables[key] = compose_runnable(aug_runnable_config)
    return runnables
