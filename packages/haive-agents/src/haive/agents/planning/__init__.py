"""Planning - Agent planning and execution systems.

This module provides planning-based agents that can break down complex tasks
into manageable steps and execute them systematically.

The main components include:
- Plan and Execute agents that follow the LangChain pattern
- Models for representing plans, steps, and execution results
- State management for tracking execution progress

Example:
    Basic usage::

        from haive.agents.planning import PlanAndExecuteAgent
        from haive.core.engines.llm.aug_llm_engine import AugLLMEngine

        # Create individual agents
        planner = SimpleAgent(name="planner", engine=engine, instructions="...", output_schema=Act)
        executor = ReactAgent(name="executor", engine=engine, instructions="...")
        replanner = SimpleAgent(name="replanner", engine=engine, instructions="...", output_schema=Act)

        # Create plan and execute system
        agent = PlanAndExecuteAgent(
            planner=planner,
            executor=executor,
            replanner=replanner,
            tools=[tavily_search_tool],
            name="research_assistant"
        )

        # Execute complex task
        result = await agent.arun("Research quantum computing developments")

See Also:
    :mod:`haive.agents.planning.plan_and_execute`: Complete Plan and Execute agent
    :mod:`haive.agents.planning.p_and_e.models`: Data models for planning
    :mod:`haive.agents.planning.p_and_e.state`: State management for execution

"""

from haive.agents.planning.plan_and_execute_multi import PlanAndExecuteAgent

__all__ = [
    "PlanAndExecuteAgent",
]
