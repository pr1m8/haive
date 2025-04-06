from __future__ import annotations
from typing import Any, Dict, List, Optional, Set, Union, Literal
from pydantic import BaseModel, Field, model_validator
from langchain_core.messages import BaseMessage
import uuid

# =============================================
# Reasoning Models
# =============================================

class ReasoningModule(BaseModel):
    """Reasoning module for self-discovery structured thinking."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(description="Name of the reasoning module")
    description: str = Field(description="Description of what the module does")
    is_selected: bool = Field(default=False, description="Whether this module is selected for the current task")
    adapted_description: Optional[str] = Field(default=None, description="Task-specific adaptation of the module")

# =============================================
# Planning Models
# =============================================

class PlanNodeInput(BaseModel):
    """Input structure for a plan node during creation."""
    description: str = Field(description="Human-readable description of this step")
    reasoning_module: Optional[str] = Field(default=None, description="Reasoning module applied in this step")
    tool: Optional[str] = Field(default=None, description="Tool to use for this step")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    dependencies: List[str] = Field(default_factory=list, description="IDs of nodes this node depends on")
    variable_name: Optional[str] = Field(default=None, description="Variable name if this node produces a variable (e.g., #E1)")
    is_join: bool = Field(default=False, description="Whether this node is a join point that requires all dependencies")

class PlanNode(BaseModel):
    """A node in the plan graph representing a single execution step."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str = Field(description="Human-readable description of this step")
    reasoning_module: Optional[str] = Field(default=None, description="Reasoning module applied in this step")
    tool: Optional[str] = Field(default=None, description="Tool to use for this step")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    dependencies: List[str] = Field(default_factory=list, description="IDs of nodes this node depends on")
    status: Literal["pending", "in_progress", "complete", "failed"] = Field(
        default="pending", description="Current status of this node"
    )
    result: Optional[Any] = Field(default=None, description="Result of executing this node")
    error: Optional[str] = Field(default=None, description="Error message if node failed")
    variable_name: Optional[str] = Field(default=None, description="Variable name if this node produces a variable (e.g., #E1)")
    is_join: bool = Field(default=False, description="Whether this node is a join point that requires all dependencies")
    
    @property
    def is_executable(self) -> bool:
        """Check if this node is executable (all dependencies are complete)."""
        return self.status == "pending"

class ExecutionPlan(BaseModel):
    """A complete execution plan with DAG structure."""
    task: str = Field(description="The task this plan is designed to solve")
    nodes: Dict[str, PlanNode] = Field(default_factory=dict, description="All nodes in the plan")
    entry_points: List[str] = Field(default_factory=list, description="IDs of nodes with no dependencies")
    join_points: List[str] = Field(default_factory=list, description="IDs of nodes that are join points")
    exit_points: List[str] = Field(default_factory=list, description="IDs of nodes with no dependents")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Variables for substitution")
    status: Literal["not_started", "in_progress", "complete", "failed"] = Field(
        default="not_started", description="Overall plan status"
    )
    
    def add_node(self, node: PlanNode) -> None:
        """Add a node to the plan."""
        self.nodes[node.id] = node
        
        # Update entry points if node has no dependencies
        if not node.dependencies:
            self.entry_points.append(node.id)
        
        # Update join points if node is a join
        if node.is_join:
            self.join_points.append(node.id)
    
    def get_executable_nodes(self) -> List[PlanNode]:
        """Get nodes that are ready for execution (all dependencies complete)."""
        result = []
        for node_id, node in self.nodes.items():
            if node.status != "pending":
                continue
                
            # Check if all dependencies are complete
            dependencies_complete = True
            for dep_id in node.dependencies:
                dep_node = self.nodes.get(dep_id)
                if not dep_node or dep_node.status != "complete":
                    dependencies_complete = False
                    break
            
            if dependencies_complete:
                result.append(node)
        
        return result
    
    def update_status(self) -> None:
        """Update the overall plan status based on node statuses."""
        # Check if any nodes failed
        for node in self.nodes.values():
            if node.status == "failed":
                self.status = "failed"
                return
        
        # Check if all nodes are complete
        if all(node.status == "complete" for node in self.nodes.values()):
            self.status = "complete"
            return
        
        # Check if any nodes are in progress
        if any(node.status == "in_progress" for node in self.nodes.values()):
            self.status = "in_progress"
            return
        
        # Otherwise, not started
        self.status = "not_started"
    
    def resolve_variable(self, var_ref: str) -> Any:
        """
        Resolve a variable reference like #E1.
        Returns the variable value or the original reference if not found.
        """
        if not var_ref or not isinstance(var_ref, str):
            return var_ref
            
        if var_ref.startswith('#E') and var_ref[2:].isdigit():
            var_name = var_ref
            return self.variables.get(var_name, var_ref)
        
        return var_ref
    
    def resolve_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve all variable references in a dict of arguments."""
        resolved = {}
        for key, value in args.items():
            if isinstance(value, str):
                # Check for variable references in strings
                resolved_value = self.resolve_variable(value)
            elif isinstance(value, dict):
                # Recursively resolve nested dicts
                resolved_value = self.resolve_args(value)
            elif isinstance(value, list):
                # Resolve lists
                resolved_value = [
                    self.resolve_variable(item) if isinstance(item, str)
                    else item for item in value
                ]
            else:
                # Use as-is for other types
                resolved_value = value
                
            resolved[key] = resolved_value
        
        return resolved

# =============================================
# Planning Output Models
# =============================================

class PlannerOutput(BaseModel):
    """Output from the planner."""
    plan: ExecutionPlan
    reasoning: str = Field(description="Reasoning behind the plan structure")
    estimated_steps: int = Field(description="Estimated number of steps to complete the task")
    parallelizable: bool = Field(description="Whether parts of the plan can be executed in parallel")

# =============================================
# Execution Models
# =============================================

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskExecution(BaseModel):
    """Information about a task execution."""
    node_id: str = Field(description="ID of the node being executed")
    tool: Optional[str] = Field(default="", description="Tool being used (empty string if no tool specified)")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    start_time: Optional[str] = Field(default=None, description="ISO timestamp when execution started")
    end_time: Optional[str] = Field(default=None, description="ISO timestamp when execution completed")
    result: Optional[Any] = Field(default=None, description="Result of the execution")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
class ExecutorOutput(BaseModel):
    """Output from the executor."""
    node_id: str = Field(description="ID of the executed node")
    success: bool = Field(description="Whether execution was successful")
    result: Optional[Any] = Field(default=None, description="Result of the execution")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    reasoning: str = Field(description="Reasoning process used during execution")
    tool_used: Optional[str] = Field(default=None, description="Tool used during execution")

# =============================================
# Reflection Models
# =============================================

from typing import Dict, List
from pydantic import BaseModel, Field, model_validator

class Reflection(BaseModel):
    """A reflection on a plan's execution."""
    strengths: List[str] = Field(default_factory=list, description="Strengths of the plan")
    weaknesses: List[str] = Field(default_factory=list, description="Weaknesses of the plan")
    improvements: List[str] = Field(default_factory=list, description="Potential improvements")

class ReflectionOutput(BaseModel):
    """Output from the reflection process."""
    reflection: Reflection = Field(
        description="The reflection on the plan and execution"
    )
    should_replan: bool = Field(
        default=True,  # Default to true to encourage replanning
        description="Whether to create a new plan"
    )
    reasoning: str = Field(
        default="Based on identified weaknesses, the plan should be refined.",
        description="Reasoning about the reflection and replanning decision"
    )
    
    @model_validator(mode='after')
    def validate_reflection_content(self) -> 'ReflectionOutput':
        """Ensure the reflection has at least some content."""
        # Add default content if empty
        if not self.reflection.strengths and not self.reflection.weaknesses:
            self.reflection.strengths = ["The plan addresses the core requirements of the task"]
            self.reflection.weaknesses = ["The plan lacks sufficient detail in execution steps"]
            self.reflection.improvements = ["Add more explicit execution steps with tool usage"]
            
        # Make sure reasoning is present
        if not self.reasoning:
            self.reasoning = "Based on identified weaknesses, the plan should be refined."
            
        return self

# =============================================
# Final Answer Model
# =============================================

class FinalAnswer(BaseModel):
    """Final answer to the user's task."""
    answer: str = Field(description="The final answer to the user's task")
    confidence: float = Field(description="Confidence in the answer (0-1)")
    reasoning: str = Field(description="Reasoning behind the answer")

from typing import Dict, List
from pydantic import BaseModel, Field, model_validator

class ModuleSelectionOutput(BaseModel):
    """Output model for the module selection process."""
    selected_modules: List[str] = Field(
        description="List of selected reasoning module names"
    )
    justifications: Dict[str, str] = Field(
        description="Justifications for each selected module"
    )
    
    @model_validator(mode='after')
    def validate_justifications(self) -> 'ModuleSelectionOutput':
        """Ensure all selected modules have justifications."""
        # Initialize justifications if missing
        if not hasattr(self, 'justifications') or self.justifications is None:
            self.justifications = {}
            
        # Create default justifications for any module missing them
        for module in self.selected_modules:
            if module not in self.justifications:
                self.justifications[module] = f"Selected for relevance to the task"
                
        return self