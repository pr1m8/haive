from typing import Union, Optional, Sequence, Literal, Dict, Any
from pydantic import BaseModel, Field
from src.haive.core.models.llm.base import LLMConfig,AzureLLMConfig
from langchain_core.tools import BaseTool,StructuredTool
from langchain.tools import Tool, StructuredTool
from src.haive.core.engine.agent.agent import AgentArchitectureConfig
from langgraph.prebuilt import ToolExecutor,ToolNode
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import StructuredResponseSchema,StateSchemaType,AgentState,_should_bind_tools
from langgraph.types import Checkpointer
#from src.haive.core.agents.react_agent.ReactAgent_v4 import create_react_agent
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.base import BaseStore
from langgraph.managed import IsLastStep, RemainingSteps
#from langgraph.types import  $
from langgraph.checkpoint.base import BaseCheckpointSaver
src.haive.core.engine.aug_llm import compose_runnable
from src.config.config import * 
#from langgraph.checkpoint import Checkpointer
from langgraph.prebuilt.chat_agent_executor import AgentState
from pydantic import Field,ConfigDict

class ReactAgentConfig(BaseModel):
    """Serializable config for the React Agent, using LLMConfig for the model."""
    
    model: LLMConfig = Field(default_factory=lambda: AzureLLMConfig(model_name="gpt-4o", parameters={"temperature": 0.7}))
    tools: Sequence[Union[BaseTool, StructuredTool, Tool]] = Field(default_factory=list)
    state_schema: Optional[StateSchemaType] = Field(default_factory=AgentState)  # Ensure this remains a model
    prompt: Optional[str] = None
    response_format: Optional[Union[StructuredResponseSchema, tuple[str, StructuredResponseSchema]]] = None
    debug: bool = False
    version: Literal["v1", "v2"] = "v1"
    name: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)  # Fixes Pydantic V2 warning

    def create_agent(self, store: Optional[BaseStore] = None, checkpointer: Optional[BaseCheckpointSaver] = None) -> CompiledGraph:
        """Create a react agent from the current config."""
        model_instance = self.model.instantiate_llm()  # Ensure model instance is created

        # 🔹 Fix: Ensure `state_schema` is NOT a dictionary
        if isinstance(self.state_schema, dict):
            raise TypeError("`state_schema` should be a Pydantic model, not a dict. Check serialization.")

        return create_react_agent(
            model=model_instance,
            tools=self.tools,  # Use instance attribute
            state_schema=self.state_schema,  # Ensure it's passed as a Pydantic model
            prompt=self.prompt,
            checkpointer=checkpointer,
            response_format=self.response_format,
            store=store,
            debug=self.debug,
            version=self.version,
            name=self.name
        )

# ✅ Create an instance of ReactAgentConfig
config = ReactAgentConfig(
    tools=[],  # Ensuring an empty list is valid
    prompt="Help with planning",
    debug=True
)

try:
    # ✅ Serialize the config to JSON
    json_output = config.model_dump_json(indent=2)
    print(json_output)

    # ✅ Correctly call create_agent() on the instance
    agent = config.create_agent()
    response = agent.invoke('hi how are you')
    print(f"Agent Response: {response}")

except Exception as e:
    print(f"Error: {e}")