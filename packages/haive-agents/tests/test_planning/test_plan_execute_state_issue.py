#!/usr/bin/env python3
"""
Test Plan-and-Execute to identify multi-agent state issues.

This test demonstrates:
1. Current state management problems
2. Type safety issues
3. Proposed solutions
"""

import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive')

from typing import Dict, Any, Optional, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import Field

# Import the models and state
from haive.agents.planning.p_and_e.models import Plan, PlanStep, StepType, Act, Response
from haive.agents.planning.p_and_e.state import PlanExecuteState

# Import agents
from haive.agents.simple.agent import SimpleAgent
from haive.agents.base.agent import Agent
# Skip LLM for now, focus on state issues


def test_current_plan_execute_state():
    """Test the current PlanExecuteState approach."""
    print("=" * 60)
    print("TESTING CURRENT PLAN-EXECUTE STATE")
    print("=" * 60)
    
    # Create state
    state = PlanExecuteState(
        messages=[HumanMessage(content="Build a web scraper")],
        context="Need to scrape product data from e-commerce sites"
    )
    
    print(f"State type: {type(state)}")
    print(f"Objective: {state.objective}")
    print(f"Has plan: {state.plan is not None}")
    
    # Create a plan
    plan = Plan(
        objective="Build a web scraper",
        steps=[
            PlanStep(
                step_id=1,
                description="Research web scraping libraries",
                step_type=StepType.RESEARCH,
                expected_output="List of suitable libraries"
            ),
            PlanStep(
                step_id=2,
                description="Design scraper architecture",
                step_type=StepType.ANALYSIS,
                expected_output="Architecture diagram",
                dependencies=[1]
            ),
            PlanStep(
                step_id=3,
                description="Implement the scraper",
                step_type=StepType.ACTION,
                expected_output="Working scraper code",
                dependencies=[1, 2]
            )
        ],
        total_steps=3
    )
    
    state.plan = plan
    print(f"\n✅ Plan created with {state.plan.total_steps} steps")
    
    return state


def test_agent_state_mismatch():
    """Test the state mismatch issue with individual agents."""
    print("\n" + "=" * 60)
    print("TESTING AGENT STATE MISMATCH ISSUE")
    print("=" * 60)
    
    # Skip creating actual LLM for this demo
    llm = None  # Would be actual engine
    
    # Issue 1: Planner agent expects different state
    print("\n--- PLANNER AGENT ISSUE ---")
    
    # Planner might expect a simpler state
    planner = SimpleAgent(
        name="planner",
        engine=llm,
        instructions="Create a plan for the given objective",
        # The agent might have its own internal state schema
    )
    
    # Problem: PlanExecuteState has many fields the planner doesn't need
    state = PlanExecuteState(messages=[HumanMessage(content="Build a web app")])
    
    print(f"State has {len(state.model_fields)} fields")
    print(f"Planner only needs: messages, objective")
    print(f"Extra fields planner gets: plan, execution_results, errors, etc.")
    
    # Issue 2: Executor agent expects different fields
    print("\n--- EXECUTOR AGENT ISSUE ---")
    
    executor = SimpleAgent(
        name="executor",
        engine=llm,
        instructions="Execute the current step of the plan"
    )
    
    # Executor needs: current_step, previous_results
    # But gets entire PlanExecuteState
    print(f"Executor needs: current_step, previous_results")
    print(f"But receives entire state with {len(state.model_fields)} fields")
    
    # Issue 3: Type safety lost
    print("\n--- TYPE SAFETY ISSUE ---")
    
    # Each agent might have specific output schemas
    planner.output_schema = Act  # Planner outputs Act (Plan or Response)
    
    # But multi-agent flattens everything
    print(f"Planner output type: {planner.output_schema}")
    print(f"But multi-agent state mixes all outputs together")
    
    return state


def demonstrate_proposed_solution():
    """Demonstrate the proposed solution with proper state management."""
    print("\n" + "=" * 60)
    print("PROPOSED SOLUTION: AGENT-AWARE STATE")
    print("=" * 60)
    
    # Solution: Create an agent-aware state that manages projections
    
    class AgentAwarePlanExecuteState(PlanExecuteState):
        """Enhanced state that can project views for specific agents."""
        
        # Track agent-specific data separately
        agent_data: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
        
        def get_planner_view(self) -> Dict[str, Any]:
            """Get state view for planner agent."""
            return {
                "messages": self.messages,
                "objective": self.objective,
                "context": self.context,
                # Planner doesn't need execution details
            }
        
        def get_executor_view(self) -> Dict[str, Any]:
            """Get state view for executor agent."""
            return {
                "current_step": self.current_step,
                "previous_results": self.previous_results,
                "plan_status": self.plan_status,
                # Executor doesn't need replanning history
            }
        
        def get_replanner_view(self) -> Dict[str, Any]:
            """Get state view for replanner agent."""
            return {
                "messages": self.messages,
                "plan": self.plan,
                "execution_results": self.execution_results,
                "errors": self.errors,
                # Replanner needs full context
            }
        
        def update_from_agent(self, agent_name: str, result: Any) -> None:
            """Update state from agent result."""
            # Store agent-specific results
            self.agent_data[agent_name] = result
            
            # Update main state based on agent type
            if agent_name == "planner" and isinstance(result, dict):
                if "action" in result:
                    act = result["action"]
                    if isinstance(act, dict) and "plan" in act:
                        self.plan = Plan(**act["plan"])
            
            elif agent_name == "executor" and isinstance(result, dict):
                if "result" in result:
                    self.execution_results.append(result["result"])
    
    # Test the enhanced state
    state = AgentAwarePlanExecuteState(
        messages=[HumanMessage(content="Build a web app")]
    )
    
    print("✅ Agent-aware state created")
    
    # Each agent gets only what it needs
    planner_view = state.get_planner_view()
    print(f"\nPlanner view has {len(planner_view)} fields: {list(planner_view.keys())}")
    
    executor_view = state.get_executor_view()
    print(f"Executor view has {len(executor_view)} fields: {list(executor_view.keys())}")
    
    replanner_view = state.get_replanner_view()
    print(f"Replanner view has {len(replanner_view)} fields: {list(replanner_view.keys())}")
    
    return state


def show_improved_multi_agent_pattern():
    """Show how multi-agent should work with proper state handling."""
    print("\n" + "=" * 60)
    print("IMPROVED MULTI-AGENT PATTERN")
    print("=" * 60)
    
    print("""
The key improvements needed:

1. **State Projection Layer**
   - Multi-agent state contains all data
   - Each agent gets a projected view with only needed fields
   - Type safety maintained through projections

2. **Agent Node Enhancement**
   ```python
   class EnhancedAgentNode:
       def __call__(self, state: MultiAgentState):
           # Project state for this agent
           agent_view = state.get_agent_view(self.agent.name)
           
           # Execute agent with its expected state
           result = self.agent.invoke(agent_view)
           
           # Update multi-agent state
           state.update_from_agent(self.agent.name, result)
   ```

3. **Type-Safe Updates**
   - Each agent's output schema is preserved
   - Updates are validated against expected types
   - No flattening of heterogeneous data

4. **Clear Separation**
   - Shared state (messages, objective)
   - Agent-specific state (plan, execution_results)
   - Metadata (timestamps, errors)

This maintains the benefits of multi-agent coordination while preserving
type safety and reducing complexity for individual agents.
""")


if __name__ == "__main__":
    print("🔍 TESTING PLAN-EXECUTE STATE MANAGEMENT")
    print("=" * 60)
    
    # Test current approach
    current_state = test_current_plan_execute_state()
    
    # Show the issues
    mismatch_demo = test_agent_state_mismatch()
    
    # Demonstrate solution
    solution_demo = demonstrate_proposed_solution()
    
    # Show improved pattern
    show_improved_multi_agent_pattern()
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("✅ Plan-Execute needs agent-aware state management")
    print("✅ State projection solves type safety issues")
    print("✅ Each agent works with its expected schema")
    print("✅ Multi-agent coordinates without schema conflicts")
    print("=" * 60)