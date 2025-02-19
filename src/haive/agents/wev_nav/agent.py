
from src.haive.agents.base import AgentArchitecture,AgentArchitectureConfig
from src.haive.agents.web_nav.state import WebNavState
from typing import List,Callable
from pydantic import Field
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.agents.web_nav.utils.utils import mark_page
from langgraph.types import Command
import re
from langchain_core.messages import SystemMessage
class WebNavAgentConfig(AgentArchitectureConfig):
    aug_llm_config: AugLLMConfig = Field(...,description="The LLM for the agent")
    state_schema: WebNavState = Field(...,description="The state schema for the agent")
    tools: List[Callable] = Field(...,description="The tools for the agent")
    #llm: BaseLLM = Field(...,description="The LLM for the agent")

class WebNavAgent(AgentArchitecture):
    def __init__(self, config: WebNavAgentConfig):
        super().__init__(config)
        self.tools = config.tools
        self.llm = config.llm
        self.state_schema = config.state_schema

    async def annotate(self,state:WebNavState):
        marked_page = await mark_page.with_retry().ainvoke(state["page"])
        # Check to fix 
        return Command(update={**state, **marked_page})
    
    def format_descriptions(self,state:WebNavState):
        labels = []
        for i, bbox in enumerate(state["bboxes"]):
            text = bbox.get("ariaLabel") or ""
            if not text.strip():
                text = bbox["text"]
            el_type = bbox.get("type")
            labels.append(f'{i} (<{el_type}/>): "{text}"')
        bbox_descriptions = "\nValid Bounding Boxes:\n" + "\n".join(labels)
        return Command(update={**state, "bbox_descriptions": bbox_descriptions})

  


    def update_scratchpad(self,state: WebNavState):
        """After a tool is invoked, we want to update
        the scratchpad so the agent is aware of its previous steps"""
        old = state.get("scratchpad")
        if old:
            txt = old[0].content
            last_line = txt.rsplit("\n", 1)[-1]
            step = int(re.match(r"\d+", last_line).group()) + 1
        else:
            txt = "Previous action observations:\n"
            step = 1
        txt += f"\n{step}. {state['observation']}"

        return Command(update={**state, "scratchpad": [SystemMessage(content=txt)]})
    def select_tool(self,state: WebNavState):
        # Any time the agent completes, this function
        # is called to route the output to a tool or
        # to the end user.
        action = state["prediction"]["action"]
        if action == "ANSWER":
            return END
        if action == "retry":
            return "agent"
        return action