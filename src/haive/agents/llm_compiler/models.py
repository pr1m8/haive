from typing import TypedDict,Optional,Dict,List,Union,Iterable
from langchain_core.tools import BaseTool
from pydantic import Field,BaseModel
from langchain_core.messages import BaseMessage
class Task(TypedDict):
    """A task is a single step in the plan"""
    idx: int = Field(...,description="The index of the task")
    tool: BaseTool = Field(...,description="The tool to use")
    args: list = Field(...,description="The arguments to the tool")
    dependencies: Dict[str, list] = Field(...,description="The dependencies of the task")
    thought: Optional[str] = Field(...,description="The thought behind the task")

class ExecuteCode(BaseModel):
    """The input to the numexpr.evaluate() function."""

    reasoning: str = Field(
        ...,
        description="The reasoning behind the code expression, including how context is included, if applicable.",
    )

    code: str = Field(
        ...,
        description="The simple code expression to execute by numexpr.evaluate().",
    )


class SchedulerInput(TypedDict):
    """The input to the scheduler."""
    messages: List[BaseMessage] = Field(...,description="The messages from the user and the LLM")
    tasks: Iterable[Task] = Field(...,description="The tasks to schedule")

class SchedulerOutput(TypedDict):
    """The output of the scheduler."""
    tasks: List[Task] = Field(...,description="The tasks to schedule")
    messages: List[BaseMessage] = Field(...,description="The messages from the user and the LLM")
class FinalResponse(BaseModel):
    """The final response/answer."""

    response: str = Field(...,description="The final response/answer")

class Replan(BaseModel):
    feedback: str = Field(
        description="Analysis of the previous attempts and recommendations on what needs to be fixed."
    )


class JoinOutputs(BaseModel):
    """Decide whether to replan or whether you can return the final response."""

    thought: str = Field(
        description="The chain of thought reasoning for the selected action"
    )
    action: Union[FinalResponse, Replan]