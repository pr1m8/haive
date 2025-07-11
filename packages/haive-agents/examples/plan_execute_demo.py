#!/usr/bin/env python3
"""
Demo of Plan and Execute Multi-Agent System using Enhanced MultiAgentBase.

This shows:
1. How branches create conditional routing (NOT parallel execution)
2. The actual graph structure being built
3. How BuildMode affects schema composition, not execution flow
"""

import json

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END

from haive.agents.multi.enhanced_base import (
    MultiAgentBase,
    create_plan_execute_multi_agent,
)
from haive.agents.planning.p_and_e.models import Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


def visualize_graph_structure(system):
    """Helper to visualize the graph structure."""
    print("\n" + "="*60)
    print("GRAPH STRUCTURE ANALYSIS")
    print("="*60)
    
    # Build the graph
    try:
        graph = system.build_graph()
        
        # Get nodes
        if hasattr(graph, '_nodes'):
            print(f"\nNodes: {list(graph._nodes.keys())}")
        elif hasattr(graph, 'nodes'):
            print(f"\nNodes: {list(graph.nodes.keys())}")
        else:
            print("\nCould not access nodes")
            
        # Get edges
        if hasattr(graph, 'edges'):
            print(f"\nEdges:")
            for edge in graph.edges:
                if hasattr(edge, 'source') and hasattr(edge, 'target'):
                    print(f"  {edge.source} -> {edge.target}")
                else:
                    print(f"  {edge}")
            
        # Get branches (conditional routing)
        if hasattr(graph, 'branches'):
            print(f"\nBranches (Conditional Routing):")
            for branch_name, branch in graph.branches.items():
                print(f"  Branch '{branch_name}':")
                if hasattr(branch, 'condition'):
                    print(f"    Condition: {branch.condition}")
                if hasattr(branch, 'destinations'):
                    print(f"    Destinations: {branch.destinations}")
                if hasattr(branch, 'default'):
                    print(f"    Default: {branch.default}")
                    
        return graph
    except Exception as e:
        print(f"\nError building graph: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("Plan and Execute Multi-Agent System Demo")
    print("="*60)
    
    # Create configuration
    config = AugLLMConfig(
        name="demo_llm",
        system_message="You are a helpful assistant.",
        temperature=0.7
    )
    
    # Create agents
    planner = SimpleAgent(
        name="planner",
        engine=config
    )
    
    executor = SimpleAgent(
        name="executor", 
        engine=config
    )
    
    replanner = SimpleAgent(
        name="replanner",
        engine=config
    )
    
    print("\n1. Using create_plan_execute_multi_agent convenience function:")
    print("-" * 60)
    
    # Create Plan & Execute system using convenience function
    pe_system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL  # This affects schema composition, NOT execution flow!
    )
    
    print(f"System name: {pe_system.name}")
    print(f"Agents: {[a.name for a in pe_system.agents]}")
    print(f"Number of branches: {len(pe_system.branches) if pe_system.branches else 0}")
    print(f"Schema build mode: {pe_system.schema_build_mode}")
    print(f"State schema: {pe_system.state_schema_override.__name__}")
    
    # Show the branches
    if pe_system.branches:
        print("\nBranch Configuration:")
        for i, branch in enumerate(pe_system.branches):
            source, condition, destinations = branch[:3]
            source_name = source.name if hasattr(source, 'name') else str(source)
            print(f"  Branch {i+1}: {source_name} -> {condition.__name__} -> {destinations}")
    
    # Visualize the graph
    graph = visualize_graph_structure(pe_system)
    
    # Try to compile and see the actual runnable graph
    if graph:
        print("\nCompiling graph to see actual execution flow...")
        try:
            compiled = graph.compile()
            print("✓ Graph compiled successfully!")
            
            # Show the actual execution graph structure
            if hasattr(compiled, 'get_graph'):
                exec_graph = compiled.get_graph()
                print(f"\nCompiled graph nodes: {exec_graph.nodes}")
                print(f"Compiled graph edges: {exec_graph.edges}")
        except Exception as e:
            print(f"✗ Could not compile graph: {e}")
    
    print("\n2. Manual configuration showing what's really happening:")
    print("-" * 60)
    
    # Define routing functions
    def route_after_execution(state) -> str:
        """Routing logic after executor runs."""
        print(f"  [ROUTING] After execution - checking state...")
        if hasattr(state, 'plan') and state.plan:
            if state.plan.is_complete:
                print(f"  [ROUTING] Plan complete -> going to replanner")
                return "replanner"
            elif hasattr(state, 'should_replan') and state.should_replan:
                print(f"  [ROUTING] Should replan -> going to replanner")
                return "replanner" 
            else:
                print(f"  [ROUTING] Continue execution -> going back to executor")
                return "executor"
        print(f"  [ROUTING] No plan -> going to replanner")
        return "replanner"
    
    def route_after_replan(state) -> str:
        """Routing logic after replanner runs."""
        print(f"  [ROUTING] After replan - checking state...")
        if hasattr(state, 'final_answer') and state.final_answer:
            print(f"  [ROUTING] Final answer found -> END")
            return END
        elif hasattr(state, 'plan') and state.plan:
            print(f"  [ROUTING] New plan created -> going to executor")
            return "executor"
        print(f"  [ROUTING] No plan or final answer -> END")
        return END
    
    # Manual system creation
    manual_system = MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=[
            # After executor runs, route based on plan status
            (executor, route_after_execution, {
                "executor": executor,
                "replanner": replanner
            }),
            # After replanner runs, route based on decision
            (replanner, route_after_replan, {
                "executor": executor,
                END: END
            })
        ],
        entry_points=[planner],  # Start with planner
        finish_points=[],  # No default finish points - handled by routing to END
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,  # Again, this is for schema, not execution!
        name="Manual Plan & Execute"
    )
    
    print(f"\nManual system created: {manual_system.name}")
    print(f"Entry points: {[e.name if hasattr(e, 'name') else str(e) for e in manual_system.entry_points]}")
    print(f"Finish points: {manual_system.finish_points}")
    
    # Visualize manual graph
    manual_graph = visualize_graph_structure(manual_system)
    
    print("\n3. Understanding BuildMode.PARALLEL vs execution flow:")
    print("-" * 60)
    print("BuildMode.PARALLEL means:")
    print("  - Schema fields from all agents are composed in PARALLEL (separate)")
    print("  - Each agent gets its own namespace in the state")
    print("  - Does NOT mean agents execute in parallel!")
    print("\nExecution flow is determined by:")
    print("  - Branches (conditional edges)")
    print("  - Entry points")  
    print("  - Routing functions")
    print("\nIn Plan & Execute:")
    print("  1. START -> planner (entry point)")
    print("  2. planner -> executor (implicit edge)")
    print("  3. executor -> route_after_execution() -> executor OR replanner")
    print("  4. replanner -> route_after_replan() -> executor OR END")
    
    # Demo routing logic
    print("\n4. Demo routing with sample state:")
    print("-" * 60)
    
    # Create sample states
    incomplete_plan = Plan(
        objective="Test task",
        total_steps=2,
        steps=[
            PlanStep(step_id=1, description="Step 1", expected_output="Result 1", status="completed"),
            PlanStep(step_id=2, description="Step 2", expected_output="Result 2", status="pending")
        ]
    )
    
    complete_plan = Plan(
        objective="Test task", 
        total_steps=1,
        steps=[
            PlanStep(step_id=1, description="Step 1", expected_output="Result 1", status="completed")
        ]
    )2
    
    # Test incomplete plan state
    print("\nRouting with incomplete plan:")
    state1 = PlanExecuteState(plan=incomplete_plan, messages=[])
    route = route_after_execution(state1)
    
    # Test complete plan state  
    print("\nRouting with complete plan:")
    state2 = PlanExecuteState(plan=complete_plan, messages=[])
    route = route_after_execution(state2)
    
    # Test final answer state
    print("\nRouting with final answer:")
    state3 = PlanExecuteState(final_answer="Task completed!", messages=[])
    route = route_after_replan(state3)
    
    print("\n" + "="*60)
    print("SUMMARY: Plan & Execute is SEQUENTIAL with CONDITIONAL routing")
    print("NOT parallel execution! The agents run one at a time based on routing.")
    print("="*60)


if __name__ == "__main__":
    main()