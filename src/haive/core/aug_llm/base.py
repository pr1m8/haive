from pydantic import BaseModel
from typing import Optional,List,Type
from langchain_core.tools import BaseTool
from src.haive.core.models.llm.base import LLMConfig,AzureLLMConfig

#from src.haive.core.prompts.base import PromptTemplateConfig,PromptTemplateFactory
from langchain_core.runnables import     Runnable
from pydantic import Field
from typing import Dict
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BasePromptTemplate
from src.config.config import *
# Add output parser 
class AugLLMConfig(BaseModel):
    """
    Configuration for creating a runnable pipeline.
    """
    name: Optional[str] = Field(description="The name of the runnable",default="runnable")
    llm_config: Optional[LLMConfig] = Field(description="Configuration for the LLM",default=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})) # Configuration for the LLM
    prompt_template: Optional[BasePromptTemplate] = None  # Configuration for the prompt template
    tools: Optional[List[BaseTool]] = None  # Optional tools to bind to the LLM
    structured_output_model: Optional[Type[BaseModel]] = None  # Optional structured output model
    output_parser: Optional[BaseOutputParser] = None  # Optional output parser
    
    
class AugLLMFactory:
    """
    Factory for creating runnables
    """
    aug_config: AugLLMConfig

    def __init__(self, aug_config: AugLLMConfig):
        self.aug_config = aug_config
        self.llm_config = aug_config.llm_config
        self.prompt_template = aug_config.prompt_template
        self.tools = aug_config.tools
        self.structured_output_model = aug_config.structured_output_model
        self.output_parser = aug_config.output_parser

        self.runnable_llm = self.initialize_llm()
        self.runnable_llm = self.initialize_llm_with_tools() if self.tools else self.runnable_llm
        self.runnable_llm = self.initialize_llm_with_structured_output() if self.structured_output_model else self.runnable_llm
        self.runnable_llm = self.initialize_llm_with_output_parser() if self.output_parser else self.runnable_llm
        #self.prompt_template = s

        self.runnable = self.create_runnable()

    def initialize_llm(self):
        return self.llm_config.instantiate_llm()

    #def initialize_prompt_template(self):
        #return PromptTemplateFactory(self.prompt_template_config).create_prompt()

    def initialize_llm_with_tools(self):
        #print("tools:",self.tools)
        return self.runnable_llm.bind_tools(self.tools)

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
        #print("runnable_config:",runnable_config)
        return AugLLMFactory(runnable_config).runnable
    except Exception as e:
        print("Error composing runnable:",e)
        return None
def create_runnables_dict(runnables: List[AugLLMConfig]) -> Dict[str,AugLLMConfig]:
    return {runnable.name: runnable for runnable in runnables}

def compose_runnables_from_dict(runnables: Dict[str,AugLLMConfig]) -> Dict[str,AugLLMConfig]:
    for aug_runnable_config in runnables:
        if isinstance(aug_runnable_config,AugLLMConfig):
            aug_runnable_config['runnable'] = compose_runnable(aug_runnable_config)
        #elif isinstance(llm_runnable_config,ReactAgentConfig):
            #llm_runnable_config['runnable'] = create_react_agent(llm_runnable_config)
    return runnables
