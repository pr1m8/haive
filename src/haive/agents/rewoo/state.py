from typing_extensions import TypedDict,Dict
from src.haive.agents.rewoo.models import RewooPlan
from pydantic import BaseModel,Field

class ReWOOState(TypedDict):
    """State management for ReWOO agent"""
    task: str = Field(default=None,description="The task to be accomplished")
    plan: RewooPlan = Field(default=None,description="The plan to be executed")
    results: Dict[str, str] = Field(default=None,description="The results of the plan")
    result: str = Field(default=None,description="The result of the plan")
