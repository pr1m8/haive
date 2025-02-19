from src.haive.agents.base import AgentArchitectureConfig
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.agents.rewoo.state import ReWOOState
from pydantic import Field
from src.haive.agents.base import AgentArchitecture,AgentArchitectureConfig
from typing import Optional
from src.haive.agents.rewoo.state import ReWOOState
from langgraph.types import Command
from langgraph.graph import START,END
class RewooAgentConfig(AgentArchitectureConfig):
    aug_llm_config: AugLLMConfig = Field(default=AugLLMConfig(name="rewoo_agent",llm_config=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})),description="The configuration for the LLM")
    state_schema: ReWOOState = Field(default=ReWOOState)
    should_visualize_graph: bool = Field(default=True,description="Whether to visualize the graph")
    visualize_graph_output_name: str = Field(default="rewoo_graph.png",description="The name of the visualization file")
    
class RewooAgent(AgentArchitecture):
    def __init__(self,config:RewooAgentConfig):
        super().__init__(config)
        #self.setup_workflow()

    def setup_workflow(self):
        pass

    def _get_current_task(self, state: ReWOOState) -> Optional[int]:
        if not state.get("results"):
            return 1
        if len(state["results"]) == len(state["plan"].steps):
            return None
        return len(state["results"]) + 1
    def plan(self, state: ReWOOState) -> ReWOOState:
        """Generate a plan for the given task"""
        result = self.planner.invoke({"task": state["task"], "tools": self.tools})
        return Command(update={"plan": result})
    
    def tool_execution(self, state: ReWOOState) -> ReWOOState:
        """Execute the current step's tool"""
        step_num = self._get_current_task(state)
        #print(state)
        #print(state['plan'])
        current_step = state['plan'].steps[step_num - 1]
        
        # Get the appropriate tool
        tool = next((t for t in self.tools if t.name == current_step.tool), None)
        if not tool:
            raise ValueError(f"Unknown tool: {current_step.tool}")

        # Prepare tool input by replacing any evidence references
        tool_input = current_step.tool_input
        for ref, value in state["results"].items():
            tool_input = tool_input.replace(ref, value)

        # Execute tool
        result = tool.invoke(tool_input)
        
        # Update results
        results = state.get("results", {})
        results[current_step.evidence_ref] = str(result)
        
        return Command(update={"results": results})
    
    def should_end(self, state: ReWOOState) -> bool:
        """Check if the task is complete"""
        return state["plan"].steps[-1].is_complete()
    
    def solve(self, state: ReWOOState) -> ReWOOState:
        """
        Generate the final solution using the collected evidence and the task plan.
        """
        task = state["task"]
        plan = state["plan"]
        results = state["results"]
        final_solution = []

        for step in plan.steps:
            evidence = results.get(step.evidence_ref, "No evidence collected")
            step_prompt = f"""
            Task: {task}
            Step {step.step_number}: {step.description}
            Evidence: {evidence}

        Solve the step and provide the result.
        """
        step_result = self.model.invoke(step_prompt).content
        final_solution.append({
            "step_number": step.step_number,
            "description": step.description,
            "result": step_result,
        })
    
        # state["result"] = final_solution
        return Command(update={"result": final_solution})

    def _route(self, state: ReWOOState) -> str:
        """Determine next step in execution"""
        task_index = self._get_current_task(state)
        if task_index is None:
            return "solving_phase"
        return "tool_execution"
    
    def setup_workflow(self):
        """Set up the execution graph"""
        #graph = StateGraph(ReWOOState)
        
        self.graph.add_node("planning_phase", self.plan)
        self.graph.add_node("tool_execution", self.tool_execution)
        self.graph.add_node("solving_phase", self.solve)
        
        self.graph.add_edge("planning_phase", "tool_execution")
        self.graph.add_edge("solving_phase", END)
        self.graph.add_conditional_edges("tool_execution", self._route)
        self.graph.add_edge(START, "planning_phase")
        
        return self.graph
a = RewooAgent(RewooAgentConfig())