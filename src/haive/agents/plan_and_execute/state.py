from pydantic import BaseModel
from src.haive.agents.plan_and_execute.models import *
from typing import List, Dict, Any,TypedDict,Annotated
import operator 
from langgraph.graph import add_messages
class PlanAndExecuteState(TypedDict):
    """
    Represents the state for the PlanAndExecuteAgent.

    Attributes:
        input (str): The original user query or objective.
        plan (Plan): The current plan, including tasks and subtasks.
        past_steps (List[Dict[str, Any]]): A list of completed steps or actions.
        response (str): The current response or output from the agent.
    """
    #messages: Annotated[list, add_messages]
    input: str = Field(default=None,description="The original user query or objective.")
    plan: Plan = Field(default=None,description="The current plan, including tasks and subtasks.")
    past_steps: List[Step] = Field(default_factory=list,description="A list of completed steps or actions.")
    response: str = Field(default=None,description="The current response or output from the agent.")