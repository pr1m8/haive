from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator
from langchain_core.messages import BaseMessage

from src.haive.agents.rec_plan.models import (
    ReasoningModule, ExecutionPlan, TaskExecution, Reflection
)

class RecursiveTreePlannerState(BaseModel):
    """State for the recursive tree planner agent."""
    # Input
    messages: List[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    task: str = Field(default="", description="Current task")
    
    # Reasoning modules
    reasoning_modules: List[ReasoningModule] = Field(default_factory=list, description="Available reasoning modules")
    selected_modules: List[str] = Field(default_factory=list, description="Selected module names for current task")
    
    # Planning
    plan: Optional[ExecutionPlan] = Field(default=None, description="Current execution plan")
    
    # Execution
    current_executions: Dict[str, TaskExecution] = Field(default_factory=dict, description="Currently executing tasks")
    completed_nodes: List[str] = Field(default_factory=list, description="IDs of completed nodes")
    waiting_for_join: Dict[str, Set[str]] = Field(default_factory=dict, description="Join points waiting for dependencies")
    
    # Tools and variables
    available_tools: List[str] = Field(default_factory=list, description="Names of available tools")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Variables from execution")
    
    # Reflection and learning
    reflections: List[Reflection] = Field(default_factory=list, description="Reflections on plans and executions")
    should_replan: bool = Field(default=False, description="Whether to create a new plan")
    
    # State tracking
    current_iteration: int = Field(default=0, description="Current iteration count")
    max_iterations: int = Field(default=3, description="Maximum number of iterations")
    error: Optional[str] = Field(default=None, description="Error message if any")
    
    # Output
    final_answer: Optional[str] = Field(default=None, description="Final answer to the task")
    
    @model_validator(mode='after')
    def ensure_defaults(self) -> 'RecursiveTreePlannerState':
        """Ensure required fields have defaults."""
        # Ensure waiting_for_join is a dictionary of sets
        if not self.waiting_for_join:
            self.waiting_for_join = {}
        
        # Extract task from messages if not provided
        if not self.task and self.messages:
            for message in self.messages:
                if message.type == "human":
                    self.task = message.content
                    break
        
        # Ensure should_replan has a default
        if not hasattr(self, 'should_replan'):
            self.should_replan = False
        
        return self
    
    def extract_task(self) -> str:
        """Extract the task from messages if not set explicitly."""
        if self.task:
            return self.task
            
        # Look for the first user message
        for message in self.messages:
            if message.type == "human":
                return message.content
                
        return "No task specified"