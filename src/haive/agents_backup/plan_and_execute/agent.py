from haive.agents.plan_and_execute.aug_llms import *
from src.haive.agents.plan_and_execute.models import *
from src.haive.agents.plan_and_execute.state import *
from src.haive.core.aug_llm.base import *
from src.haive.agents.base import AgentArchitectureConfig,AgentArchitecture
from langchain_core.tools import BaseTool,StructuredTool
from langchain_core.tools import Tool
from src.haive.core.tools.search_tools import tavily_search_tool
from typing import Optional,Dict,List,Union
import uuid
from pydantic import BaseModel,Field
from langchain_core.runnables import RunnableConfig
from src.haive.agents.react_agent.agent import ReactAgentConfig,create_react_agent
from langgraph.types import Command
from langgraph.graph import END

import asyncio
from typing import Type
class PlanAndExecteConfig(AgentArchitectureConfig):
    aug_llm_configs:Dict[str,AugLLMConfig] =\
    {"planner":planner_aug_llm_config,
     #"agent_executor":agent_executor_aug_llm_config,
     "replanner":replanner_aug_llm_config}
    agent_executor_config:ReactAgentConfig = ReactAgentConfig(
        #llm_config=agent_executor_aug_llm_config,
        #tools=[],
        #state_schema=PlanAndExecuteState
    )
    #models:List[BaseModel] = [Plan,Act,Response,Step,Status]
    state_schema:Union[Type[BaseModel],List[BaseModel]] = PlanAndExecuteState
    default_input_schema:Dict[str,List] = {"input": [("user", "{}")]}
    
class PlanAndExecuteAgent(AgentArchitecture):
    def __init__(self,config:PlanAndExecteConfig):
        self.config = config
        #self.runnables = create_runnables_dict(config.runnables)
        #self.runnables = compose_runnables_from_dict(self.runnables)
        
        self.planner_runnable = compose_runnable(self.config.aug_llm_configs["planner"])
        #print(self.planner_runnable)
        self.agent_executor_runnable = create_react_agent(self.config.agent_executor_config).app
        self.replanner_runnable = compose_runnable(self.config.aug_llm_configs["replanner"])
        super().__init__(config)
    async def planner(self,state:PlanAndExecuteState):
        #print(state['input'])
        plan = await self.planner_runnable.ainvoke({"messages": [("user", state["input"])]})
        #print(plan)
        return Command(update={"plan":plan},goto="execute_step",resume={"plan":plan.steps})
    
    
    def setup_workflow(self):
        self.graph.add_node("planner",self.planner)
        self.graph.add_node("execute_step",self.execute_step)
        self.graph.add_node("replan_step",self.replan_step)
        self.graph.add_edge("planner","execute_step")
        self.graph.set_entry_point("planner")

        self.graph.add_edge("execute_step","replan_step")
        #self.graph.add_edge("replan_step","planner")
        #self.graph.add_edge("replan_step","execute_step")
        #self.graph.add_edge("execute_step","replan_step")
        self.graph.add_conditional_edges(
        "replan_step",
        # Next, we pass in the function that will determine which node is called next.
        self.should_end,
        ["execute_step", END],
        )
    async def execute_step(self, state: PlanAndExecuteState):
        """
        Executes the next step in the plan.
        """
        plan = state.get("plan")
        if not plan or not plan.steps:
            raise ValueError("No plan or steps available to execute.")

        # Ensure `past_steps` is initialized to avoid NoneType errors
        state.setdefault("past_steps", [])

        # Identify the next step to execute
        next_step = next((step for step in plan.steps if step.status == "not_started"), None)
        
        if not next_step:
            state["response"] = "All steps completed."
            return Command(update={"response": state["response"]}, goto=END)

        # Format the task description
        task_formatted = f"""For the following plan:
        {plan.description}

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

        # Append completed step to past_steps list
        state["past_steps"].append(next_step)  # ✅ `past_steps` is guaranteed to be a list

        return Command(update={"past_steps": state["past_steps"], "plan": state["plan"], "response": response_content}, goto="replan_step")

    async def replan_step(self, state: PlanAndExecuteState):
        """
        Replans the steps based on completed progress.
        """
        # If all steps are complete, return the final response
        if all(step.status == "complete" for step in state["plan"].steps):
            state["response"] = f"Final response: {state['past_steps'][-1].result}"  # ✅ Uses last step's result
            return Command(update={"response": state["response"]}, goto=END)

        output = await self.replanner_runnable.ainvoke({
            "input": state['input'],
            "plan": state['plan'] if state['plan'] else None,
            "past_steps": state['past_steps']
        })

        if isinstance(output.action, Response):
            state["response"] = output.action.response
            return Command(update={"response": state["response"]}, goto=END)

        # Otherwise, continue replanning
        state["plan"].steps.extend([
            Step(id=i + 1, description=step.description, status="not_started")
            for i, step in enumerate(output.action.steps)
        ])

        return Command(update={"plan": state["plan"], "response": state["response"]}, goto="execute_step")

    def should_end(self,state: PlanAndExecuteState):
        """
        Determines if the process should end.

        Args:
            state (PlanAndExecuteState): The current state.

        Returns:
            str: "END" if finished, otherwise continue to the next node.
        """
        if state.get('response'):
            return END
        elif state.get('plan') and any(step.status == "not_started" for step in state.get('plan').steps):
            return "execute_step"
        else:
            return "replan_step"
    async def arun(self, input_text: str = None, input_dict: Dict[str, Any] = None):
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

        #print("🔍 Debug Inputs:", inputs)  # Debugging line
        
        async for output in self.app.astream(inputs, stream_mode="values", config=self.runnable_config):
            print("📝 Output:", output)  # Debugging line
            if "messages" in output:
                message = output["messages"][-1]
                #print("💬 Message:", message)

            # Ensure update includes required fields
            if not any(key in output for key in ["input", "plan", "past_steps", "response"]):
                raise ValueError("🚨 Missing required update fields:", output)
        self.save_state_history()
    
import asyncio

async def main():
    a = PlanAndExecuteAgent(PlanAndExecteConfig())
    await a.arun(input_text="Find a github repo relating to autonomous agents - autogpt,auto-dev,  and find the sitemap to langgraph.")

if __name__ == "__main__":
    asyncio.run(main())