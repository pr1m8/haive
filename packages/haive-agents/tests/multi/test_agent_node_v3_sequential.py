"""Test AgentNodeV3 with MultiAgentState in sequential execution."""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config, create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import Field

# Import Agent for model_rebuild
from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

# Fix forward reference issue
MultiAgentState.model_rebuild()
AgentNodeV3Config.model_rebuild()


class PlannerState(StateSchema):
    """State for planner agent."""

    messages: list = Field(default_factory=list)
    plan: str = Field(default="")
    steps: list[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""

    messages: list = Field(default_factory=list)
    execution_result: str = Field(default="")
    success: bool = Field(default=False)


async def test_agent_node_v3_sequential():
    """Test AgentNodeV3 with sequential execution pattern."""

    # Step 1: Create agents with specific schemas
    planner = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(temperature=0.7),
        state_schema=PlannerState,
        use_prebuilt_base=True,
        debug=True,
    )

    executor = SimpleAgent(
        name="executor",
        engine=AugLLMConfig(temperature=0.7),
        state_schema=ExecutorState,
        use_prebuilt_base=True,
        debug=True,
    )


    # Step 2: Create MultiAgentState with agents
    state = MultiAgentState(
        agents=[planner, executor],
        messages=[HumanMessage(content="Plan and execute a simple task")],
    )


    # Step 3: Create AgentNodeV3 configurations

    planner_node = create_agent_node_v3(
        agent_name="planner", name="plan_step", command_goto="execute_step"
    )

    executor_node = create_agent_node_v3(
        agent_name="executor", name="execute_step", command_goto=None  # End of sequence
    )


    # Step 4: Execute planner node

    # Display state before execution
    state.display_debug_info("Before Planner Execution")

    try:
        # Execute with debug config
        debug_config = {"debug": True}
        planner_result = planner_node(state, config=debug_config)

        # Apply planner updates to state
        if hasattr(planner_result, "update") and planner_result.update:
            for key, value in planner_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)


    except Exception as e:
        return False

    # Step 5: Execute executor node

    # Display state after planner execution
    state.display_debug_info("After Planner Execution")

    try:
        # Execute with debug config
        debug_config = {"debug": True}
        executor_result = executor_node(state, config=debug_config)

        # Apply executor updates to state
        if hasattr(executor_result, "update") and executor_result.update:
            for key, value in executor_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)


    except Exception as e:
        return False

    # Step 6: Verify sequential execution results

    # Display final state
    state.display_debug_info("Final State After Both Agents")

    # Also display the agent table
    state.display_agent_table()

    # Check agent outputs
    planner_output = state.get_agent_output("planner")
    executor_output = state.get_agent_output("executor")


    # Check agent states
    planner_state = state.get_agent_state("planner")
    executor_state = state.get_agent_state("executor")


    # Check messages updated

    # Check execution order

    return True


if __name__ == "__main__":
    result = asyncio.run(test_agent_node_v3_sequential())
    if result:
        pass!")
    else:
        pass!")
