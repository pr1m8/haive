from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Union, Optional, Type, Dict, ClassVar
from langchain_core.tools import BaseTool, StructuredTool
from src.haive.agents.plan_and_execute.models import Step, Plan

class ToolCall(BaseModel):
    """Represents a tool call referencing LangChain tools or structured tools."""
    
    name: str = Field(description="Name of the tool to use")
    input: Optional[Union[str, Dict[str, Union[str, int, float]]]] = Field(
        description="Input to pass to the tool", default=None
    )
    tool: Optional[Union[BaseTool, StructuredTool, BaseModel]] = None  # Supports multiple tool types

    available_tools: ClassVar[Dict[str, Union[Type[BaseTool], Type[StructuredTool], Type[BaseModel]]]] = {}

    @classmethod
    def set_available_tools(cls, tools: List[Union[BaseTool, StructuredTool, BaseModel]]):
        """Stores available tool instances for validation."""
        cls.available_tools = {tool.name: tool for tool in tools}

    @field_validator("name")
    def validate_tool_name(cls, v):
        """Ensures the tool name exists in the available tool list."""
        if v not in cls.available_tools:
            raise ValueError(f"Invalid tool name '{v}'. Must be one of {list(cls.available_tools.keys())}")
        return v

    @field_validator("input", mode="before")
    def validate_tool_input(cls, v, values):
        """Ensures the input format matches the expected tool input structure (if applicable)."""
        if "name" in values and values["name"] in cls.available_tools:
            tool = cls.available_tools[values["name"]]
            
            # If tool has an args schema (StructuredTool), validate input
            if hasattr(tool, "args_schema") and tool.args_schema:
                try:
                    return tool.args_schema(**v)  # Validate input against tool's schema
                except ValidationError as e:
                    raise ValueError(f"Invalid input for tool '{values['name']}': {e}")

        return v

class RewooStep(Step):
    """Extends Step to include evidence references and tool calls with validation."""
    
    evidence_ref: str = Field(description="Reference ID for this evidence (e.g., #E1)")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="List of tool calls involved in this step")

    @field_validator("evidence_ref")
    def validate_evidence_ref(cls, v):
        if not v.startswith("#E"):
            raise ValueError("Evidence reference must start with #E")
        return v

class RewooPlan(Plan):
    """Extends Plan to integrate Rewoo-style steps."""
    
    steps: List[RewooStep] = Field(default_factory=list, description="Rewoo-style steps in the plan")

    def add_rewoo_step(self, step: RewooStep):
        """Adds a new RewooStep to the plan."""
        self.steps.append(step)

    def remove_completed_steps(self):
        """Removes completed steps from the plan."""
        self.steps = [step for step in self.steps if not step.is_complete()]
