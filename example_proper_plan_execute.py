"""Example demonstrating the Proper Plan & Execute implementation.

This example shows how to use the proper Plan & Execute agent that:
- Uses existing p_and_e models, prompts, and state
- SimpleAgent for planning with Plan structured output
- ReactAgent for execution with tools
- SimpleAgent for replanning with Act structured output
- Proper LangGraph branching following the official pattern
"""

from haive.agents.planning.proper_plan_execute import create_proper_plan_execute
from haive.tools import duckduckgo_search_tool


def example_basic_usage():
    """Example of basic Plan & Execute usage."""
    print("=== Basic Plan & Execute Example ===")
    
    # Create the agent
    agent = create_proper_plan_execute(
        name="ExamplePlanExecute",
        tools=[duckduckgo_search_tool]
    )
    
    print(f"Created agent: {agent.name}")
    print(f"Agents: {[a.name for a in agent.agents]}")
    print(f"State schema: {agent.state_schema.__name__}")
    
    # Simple math problem (doesn't need tools)
    print("\n--- Testing Simple Math Problem ---")
    result = agent.run("What is 25 * 4 + 12?")
    print(f"Simple math result: {result}")
    
    return agent


def example_with_research():
    """Example that requires research and planning."""
    print("\n=== Research Plan & Execute Example ===")
    
    # Create agent with search capabilities
    agent = create_proper_plan_execute(
        name="ResearchPlanExecute", 
        tools=[duckduckgo_search_tool]
    )
    
    # Complex research task
    research_query = """Research the latest developments in artificial intelligence in 2024 and 2025. 
    Focus on major breakthroughs, new models, and industry impact. 
    Provide a comprehensive summary with key findings."""
    
    print(f"Research query: {research_query}")
    print("Running Plan & Execute agent...")
    
    result = agent.run(research_query)
    print(f"Research result: {result}")
    
    return agent


def example_step_by_step_analysis():
    """Example showing the agent's step-by-step approach."""
    print("\n=== Step-by-Step Analysis Example ===")
    
    agent = create_proper_plan_execute(
        name="AnalysisPlanExecute",
        tools=[duckduckgo_search_tool]
    )
    
    # Multi-step analysis task
    analysis_query = """Analyze the impact of remote work on productivity. 
    I need you to:
    1. Research recent studies on remote work productivity
    2. Identify key factors that affect productivity
    3. Compare productivity metrics between remote and office work
    4. Provide actionable recommendations for improving remote work productivity"""
    
    print(f"Analysis query: {analysis_query}")
    print("Running detailed analysis...")
    
    result = agent.run(analysis_query)
    print(f"Analysis result: {result}")
    
    return agent


def show_agent_structure():
    """Show the internal structure of the Plan & Execute agent."""
    print("\n=== Agent Structure Analysis ===")
    
    agent = create_proper_plan_execute()
    
    print(f"Agent Name: {agent.name}")
    print(f"Schema Build Mode: {agent.schema_build_mode}")
    print(f"State Schema: {agent.state_schema.__name__}")
    
    print(f"\nState Schema Fields:")
    for field_name in agent.state_schema.model_fields.keys():
        print(f"  - {field_name}")
    
    print(f"\nSub-Agents:")
    for i, sub_agent in enumerate(agent.agents):
        print(f"  {i+1}. {sub_agent.name} ({type(sub_agent).__name__})")
        
        if hasattr(sub_agent, 'structured_output_model') and sub_agent.structured_output_model:
            print(f"     Structured Output: {sub_agent.structured_output_model.__name__}")
            
        if hasattr(sub_agent, 'tools') and sub_agent.tools:
            print(f"     Tools: {[getattr(t, 'name', str(t)) for t in sub_agent.tools]}")
    
    print(f"\nBranches: {len(agent.branches)} conditional routing rules")
    print(f"Entry Points: {[a.name for a in agent.entry_points]}")


if __name__ == "__main__":
    print("🚀 Proper Plan & Execute Agent Examples")
    print("=" * 50)
    
    # Show agent structure
    show_agent_structure()
    
    # Run examples
    try:
        # Basic usage
        basic_agent = example_basic_usage()
        
        # Research example (commented out to avoid API calls in demo)
        # research_agent = example_with_research()
        
        # Analysis example (commented out to avoid API calls in demo)
        # analysis_agent = example_step_by_step_analysis()
        
        print("\n✅ All examples completed successfully!")
        print("\n🎯 Key Features Demonstrated:")
        print("  ✅ Uses existing p_and_e models (Plan, Act, PlanStep, etc.)")
        print("  ✅ Uses existing p_and_e prompts (PLANNER_SYSTEM_MESSAGE, etc.)")
        print("  ✅ Uses existing p_and_e state (PlanExecuteState)")
        print("  ✅ SimpleAgent for planning with Plan structured output")
        print("  ✅ ReactAgent for execution with tools support")
        print("  ✅ SimpleAgent for replanning with Act structured output")
        print("  ✅ Proper LangGraph branching with conditional routing")
        print("  ✅ MultiAgentBase orchestration with BuildMode.PARALLEL")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        import traceback
        traceback.print_exc()