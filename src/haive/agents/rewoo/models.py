from pydantic import BaseModel,Field,field_validator
from typing import List,Union

class ToolCall(BaseModel):
    """Represents a tool call"""
    name: str = Field(description="Name of the tool to use")
    input: Union[str,None] = Field(description="Input to pass to the tool")


class Step(BaseModel):
    """Represents a single step in the plan"""
    step_number: int = Field(description="Order of this step in the plan")
    description: str = Field(description="Detailed description of what this step does")
    tool: str = Field(description="Name of the tool to use")
    tool_input: Union[str,None] = Field(description="Input to pass to the tool")
    evidence_ref: str = Field(description="Reference ID for this evidence (e.g., #E1)")
    
    @field_validator('evidence_ref')
    def validate_evidence_ref(cls, v):
        if not v.startswith('#E'):
            raise ValueError('Evidence reference must start with #E')
        return v

class Plan(BaseModel):
    """Represents a complete execution plan"""
    task: str = Field(description="The objective to be accomplished")
    steps: List[Step] = Field(description="Steps to accomplish the task")
