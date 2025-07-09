"""Plan and Execute Agent Implementation.

Simple Plan and Execute agent using MultiAgentBase with proper configuration.
"""

from typing import List
from haive.agents.base.agent import Agent
from haive.agents.multi.enhanced_base import MultiAgentBase, BuildMode
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin


def create_plan_execute_branches(planner: Agent, executor: Agent, replanner: Agent):
    """Create default Plan & Execute branches."""
    def should_continue(state) -> str:
        if not hasattr(state, 'plan') or not state.plan:
            return "replanner"
        if state.plan.is_complete:
            return "replanner"
        if hasattr(state, 'should_replan') and state.should_replan:
            return "replanner"
        return "executor"
    
    def should_end(state) -> str:
        if hasattr(state, 'final_answer') and state.final_answer:
            return "END"
        if hasattr(state, 'plan') and state.plan and state.plan.next_step:
            return "executor"
        return "END"
    
    return [
        # planner → executor is implicit from agent order
        (executor, should_continue, {"executor": executor, "replanner": replanner}),
        (replanner, should_end, {"executor": executor, "END": "END"}),
    ]


def PlanAndExecuteAgent(
    planner: Agent,
    executor: Agent, 
    replanner: Agent,
    name: str = "Plan and Execute Agent",
    **kwargs
) -> MultiAgentBase:
    """Create a Plan and Execute multi-agent system.
    
    Args:
        planner: Agent that creates plans
        executor: Agent that executes plan steps  
        replanner: Agent that decides whether to continue or end
        name: Name for the agent system
        **kwargs: Additional arguments for MultiAgentBase
        
    Returns:
        MultiAgentBase: Configured Plan and Execute system
    """
    # Set up agents
    agents = [planner, executor, replanner]
    
    # Create branches
    branches = create_plan_execute_branches(planner, executor, replanner)
    
    # Create the MultiAgentBase with proper configuration
    return MultiAgentBase(
        agents=agents,
        branches=branches,
        entry_points=[planner],  # Start with planner
        name=name,
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,  # Engine serialization is now handled by field validators
        **kwargs
    )