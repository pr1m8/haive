from typing import Dict, Any, Callable, Union
from src.haive.core.graph.branches import Branch

def create_schedule_execution_branch() -> Branch:
    """Create a branch for routing after scheduling execution."""
    
    def routing_function(state: Any) -> str:
        """Determine where to route after scheduling execution."""
        # First check if we have any current executions
        has_executions = False
        if isinstance(state, dict):
            has_executions = bool(state.get("current_executions", {}))
        else:
            has_executions = bool(getattr(state, "current_executions", {}))
            
        if has_executions:
            return "execute_tasks"
            
        # If no executions but plan is complete or failed, go to reflect
        plan_complete = False
        if isinstance(state, dict):
            plan = state.get("plan")
            if plan and hasattr(plan, "status") and plan.status in ["complete", "failed"]:
                plan_complete = True
        elif hasattr(state, "plan") and state.plan:
            if state.plan.status in ["complete", "failed"]:
                plan_complete = True
                
        if plan_complete:
            return "reflect"
            
        # Otherwise go to check execution
        return "check_execution"
    
    # Create branch with proper destination names
    branch = Branch(
        function=routing_function,
        destinations={
            "execute_tasks": "execute_tasks",
            "reflect": "reflect",
            "check_execution": "check_execution"
        },
        default="check_execution"
    )
    
    return branch

def create_check_execution_branch() -> Branch:
    """Create a branch for routing after checking execution."""
    
    def routing_function(state: Any) -> str:
        """Determine where to route after checking execution."""
        # If plan is complete or failed, go to reflect
        plan_status = None
        
        if isinstance(state, dict):
            plan = state.get("plan")
            if plan and hasattr(plan, "status"):
                plan_status = plan.status
        elif hasattr(state, "plan") and state.plan:
            plan_status = state.plan.status
            
        if plan_status in ["complete", "failed"]:
            return "reflect"
            
        # Otherwise continue scheduling
        return "schedule_execution"
    
    # Create branch with proper destination names
    branch = Branch(
        function=routing_function,
        destinations={
            "reflect": "reflect",
            "schedule_execution": "schedule_execution"
        },
        default="schedule_execution"
    )
    
    return branch

def create_reflection_branch(max_iterations: int) -> Branch:
    """
    Create a branch for routing after reflection.
    
    Args:
        max_iterations: Maximum number of planning iterations
    """
    
    def routing_function(state: Any) -> str:
        """Determine where to route after reflection."""
        # If should replan and not reached max iterations, go to replan
        should_replan = False
        current_iteration = 0
        
        if isinstance(state, dict):
            should_replan = state.get("should_replan", False)
            current_iteration = state.get("current_iteration", 0)
        else:
            should_replan = getattr(state, "should_replan", False)
            current_iteration = getattr(state, "current_iteration", 0)
            
        if should_replan and current_iteration < max_iterations:
            return "replan"
            
        # Otherwise generate final answer
        return "generate_answer"
    
    # Create branch with proper destination names
    branch = Branch(
        function=routing_function,
        destinations={
            "replan": "replan",
            "generate_answer": "generate_answer"
        },
        default="generate_answer"
    )
    
    return branch