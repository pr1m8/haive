from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import *
from langgraph.graph import END
from langgraph.types import Command

from haive.agents.planning.plan_and_execute.config import PlanAndExecuteConfig
from haive.agents.planning.plan_and_execute.engines import *
from haive.agents.planning.plan_and_execute.models import *
from haive.agents.planning.plan_and_execute.state import *
from haive.agents.react_agent.agent import create_react_agent


@register_agent(PlanAndExecuteConfig)
class PlanAndExecuteAgent(Agent[PlanAndExecuteConfig]):
    def __init__(self, config: PlanAndExecuteConfig = PlanAndExecuteConfig()):
        self.config = config

        self.planner_runnable = compose_runnable(self.config.aug_llm_configs["planner"])
        self.agent_executor_runnable = create_react_agent(
            self.config.agent_executor_config
        ).app
        self.replanner_runnable = compose_runnable(
            self.config.aug_llm_configs["replanner"]
        )
        super().__init__(config)

    async def planner(self, state: PlanAndExecuteState):
        plan = await self.planner_runnable.ainvoke(
            {"messages": [("user", state.input)]}
        )
        return Command(
            update={"plan": plan}, goto="execute_step", resume={"plan": plan.steps}
        )

    def setup_workflow(self):
        self.graph.add_node("planner", self.planner)
        self.graph.add_node("execute_step", self.execute_step)
        self.graph.add_node("replan_step", self.replan_step)
        self.graph.add_edge("planner", "execute_step")
        self.graph.set_entry_point("planner")

        self.graph.add_edge("execute_step", "replan_step")
        self.graph.add_conditional_edges(
            "replan_step",
            # Next, we pass in the function that will determine which node is called next.
            self.should_end,
            ["execute_step", END],
        )

    async def execute_step(self, state: PlanAndExecuteState):
        """Executes the next step in the plan."""
        if not state.plan or not state.plan.steps:
            state.response = "No steps available to execute."
            return Command(update={"response": state.response}, goto=END)

        # Find the last incomplete step (either 'not_started' or 'in_progress')
        next_step = state.get_next_step()

        if not next_step:
            state.response = "All steps completed."
            return Command(update={"response": state.response}, goto=END)

        # If the step is still in progress, complete it before moving on
        if next_step.status == "in_progress" and next_step.result is None:
            state.response = f"Continuing step {next_step.id}: {next_step.description}."
            return Command(update={"response": state.response}, goto="replan_step")

        # Format the task description
        task_formatted = f"""For the following plan:
        {state.plan.description}

        You are tasked with executing step {next_step.id}: {next_step.description}.
        """

        # Invoke the agent executor to process the task
        agent_response = await self.agent_executor_runnable.ainvoke(
            {"messages": [("user", task_formatted)]}
        )

        # Ensure agent response contains valid output
        if "messages" not in agent_response or not agent_response["messages"]:
            raise ValueError("Agent executor did not return a valid response.")

        response_content = agent_response["messages"][-1].content

        # Update step status and result
        next_step.add_result(response_content)

        # Move completed step to past_steps
        state.update_past_steps(next_step)

        return Command(
            update={
                "past_steps": state.past_steps,
                "plan": state.plan,
                "response": response_content,
            },
            goto="replan_step",
        )

    async def replan_step(self, state: PlanAndExecuteState):
        """Replans the steps based on completed progress."""
        # If all steps are complete, return the final response
        if all(step.status == "complete" for step in state.plan.steps):
            state.response = f"Final response: {state.past_steps[-1].result}"  # ✅ Uses last step's result
            return Command(update={"response": state.response}, goto=END)

        output = await self.replanner_runnable.ainvoke(
            {
                "input": state.input,
                "plan": state.plan if state.plan else None,
                "past_steps": state.past_steps,
            }
        )

        if isinstance(output.action, Response):
            state.response = output.action.response
            return Command(update={"response": state.response}, goto=END)

        # Otherwise, continue replanning
        state.plan.steps.extend(
            [
                Step(id=i + 1, description=step.description, status="not_started")
                for i, step in enumerate(output.action.steps)
            ]
        )

        return Command(
            update={"plan": state.plan, "response": state.response}, goto="execute_step"
        )

    def should_end(self, state: PlanAndExecuteState):
        """Determines if the process should end.

        Args:
            state (PlanAndExecuteState): The current state.

        Returns:
            str: "END" if finished, otherwise continue to the next node.
        """
        if state.response:
            return END
        if state.plan and any(
            step.status == "not_started" for step in state.plan.steps
        ):
            return "execute_step"
        return "replan_step"

    async def arun(
        self, input_text: str | None = None, input_dict: dict[str, Any] | None = None
    ):
        if not self.graph:
            raise RuntimeError("Workflow graph is not set up.")
        if not self.app:
            if self.memory:
                self.app = self.compile_graph(checkpointer=self.memory)
            else:
                self.app = self.compile_graph()

        inputs = {"input": input_text} if input_text else input_dict

        if not inputs:
            raise ValueError("Either input_text or input_dict must be provided")

        async for output in self.app.astream(
            inputs, stream_mode="values", config=self.runnable_config
        ):
            if "messages" in output:
                output["messages"][-1]

            # Ensure update includes required fields
            if not any(
                key in output for key in ["input", "plan", "past_steps", "response"]
            ):
                raise ValueError("🚨 Missing required update fields:", output)
        self.save_state_history()


# async def main():


# if __name__ == "__main__":
