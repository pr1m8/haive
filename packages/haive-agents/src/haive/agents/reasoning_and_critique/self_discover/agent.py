from haive.core.engine.agent.agent import AgentArchitecture, AgentArchitectureConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langgraph.graph import END, START
from langgraph.types import Command

# from haive.agents.reasoning_and_critique.self_discover.models import #Plan
from pydantic import Field

from haive.agents.reasoning_and_critique.self_discover.aug_llms import (
    adapt_chain,
    select_chain,
    step_reasoning_chain,
    structured_chain,
)
from haive.agents.reasoning_and_critique.self_discover.models import (
    AdaptedModule,
    AdaptedModules,
)
from haive.agents.reasoning_and_critique.self_discover.state import SelfDiscoverState


class SelfDiscoverAgentConfig(AgentArchitectureConfig):
    """Configuration for the Self Discover Agent"""

    # task_description: str = Field(description="Task description")
    aug_llm_configs: dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            "step_reasoning": step_reasoning_chain,
            "select": select_chain,
            "adapt": adapt_chain,
            "structured": structured_chain,
        },
        description="Aug LLM configurations",
    )
    # selected_modules: Optional[str] = Field(description="Selected modules")
    # plan:Plan = Field(description="Plan to solve the problem with reasonsing ste-s")
    state_schema: SelfDiscoverState = Field(
        default=SelfDiscoverState, description="State schema"
    )


class SelfDiscoverAgent(AgentArchitecture):
    """Self Discover Agent"""

    def __init__(self, config: SelfDiscoverAgentConfig = SelfDiscoverAgentConfig()):
        super().__init__(config)
        # print(self.aug_llm_model_runnables_dict)

    def select(self, inputs):
        """Selects relevant reasoning modules based on the task description."""
        selected_modules = self.aug_llm_model_runnables_dict["select"].invoke(inputs)
        return Command(update={"selected_modules": selected_modules})

    def adapt(self, inputs):
        """Adapts the selected reasoning modules to be more specific to the task."""
        adapted_modules = self.aug_llm_model_runnables_dict["adapt"].invoke(inputs)

        if isinstance(adapted_modules, str):
            adapted_modules = AdaptedModules(
                adapted_modules=[
                    AdaptedModule(adapted_module=mod.name)
                    for mod in inputs["selected_modules"].modules
                ]
            )

        return Command(update={"adapted_modules": adapted_modules})

    def structure(self, inputs):
        """Structures the reasoning process and ensures the reasoning plan is carried over."""
        reasoning_plan = self.aug_llm_model_runnables_dict["structured"].invoke(inputs)
        return Command(
            update={"reasoning_structure": reasoning_plan, "plan": reasoning_plan}
        )

    async def reason(self, state: SelfDiscoverState):
        """Processes the next step in the reasoning structure sequentially."""
        plan = state["plan"]
        if not plan or not plan.steps:
            raise ValueError("No steps available in the reasoning plan.")

        # Identify next step that is not started
        next_step = next(
            (step for step in plan.steps if step.status == "not_started"), None
        )

        if not next_step:
            return {"response": "All steps completed."}

        # Format reasoning input
        reasoning_input = {
            "step_id": next_step.id,
            "step_description": next_step.description,
            "task_description": state["task_description"],
            "reasoning_modules": "\n".join(
                [
                    f"- {mod.name}: {mod.description}"
                    for mod in next_step.reasoning_modules
                ]
            ),
        }

        # Invoke the reasoning model
        reasoning_response = await self.aug_llm_model_runnables_dict[
            "step_reasoning"
        ].ainvoke(reasoning_input)

        # Update step with response
        next_step.add_response(reasoning_response)

        return {"response": reasoning_response}

    def setup_workflow(self):
        """Sets up the execution workflow."""
        self.graph.add_node("select", self.select)
        self.graph.add_node("adapt", self.adapt)
        self.graph.add_node("structure", self.structure)
        self.graph.add_node("reason", self.reason)

        self.graph.add_edge(START, "select")
        self.graph.add_edge("select", "adapt")
        self.graph.add_edge("adapt", "structure")
        self.graph.add_edge("structure", "reason")
        self.graph.add_edge("reason", END)

    async def run(self, task_description: str):
        """Executes the self-discovery process."""
        async for s in self.app.astream(
            {"task_description": task_description}, config=self.runnable_config
        ):
            print(s)


import asyncio


def main():
    # Example Run
    a = SelfDiscoverAgent()
    task_example = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon(H) rectangle (I) sector (J) triangle"""

    asyncio.run(a.run(task_example))


if __name__ == "__main__":
    main()
