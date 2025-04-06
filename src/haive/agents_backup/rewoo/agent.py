from src.haive.core.engine.agent.agent import AgentArchitectureConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.agents.rewoo.state import ReWOOState
from pydantic import Field,model_validator
from src.haive.core.engine.agent.agent import AgentArchitecture,AgentArchitectureConfig
from typing import Optional
from src.haive.agents.rewoo.state import ReWOOState
from langgraph.types import Command
from langgraph.graph import START,END
from langchain_core.tools import BaseTool,StructuredTool
from pydantic import BaseModel
from typing import List,Union
from src.haive.agents.rewoo.aug_llms import rewoo_aug_llm_config,solve_aug_llm_config
from src.haive.core.utils.tool_utils import _format_tool_descriptions
from src.haive.core.tools.search_tools import tavily_search_tool,tavily_search_context,tavily_qna,tavily_extract
src.haive.core.engine.aug_llm import compose_runnable

class RewooAgentConfig(AgentArchitectureConfig):
    """Configuration for the ReWOO Agent with automatic prompt formatting."""

    planner: AugLLMConfig = Field(default=rewoo_aug_llm_config, description="The configuration for the planner LLM")
    solver: AugLLMConfig = Field(default=solve_aug_llm_config, description="The configuration for the solver LLM")
    tools: List[Union[BaseTool, StructuredTool, BaseModel]] = Field(
        default=[tavily_search_tool, tavily_search_context, tavily_qna, tavily_extract],
        description="The tools available for the agent",
    )
    state_schema: ReWOOState = Field(default=ReWOOState)
    should_visualize_graph: bool = Field(default=True, description="Enable graph visualization")
    visualize_graph_output_name: str = Field(default="rewoo_graph.png", description="Graph output file name")

    @model_validator(mode="after")
    def format_planning_prompt_with_tools(self):
        """Ensures `formatted_prompt` is updated based on the available tools."""
        self.planner.prompt_template = self.planner.prompt_template.partial(
            tools=_format_tool_descriptions(self.tools)
        )
        return self

class RewooAgent(AgentArchitecture):
    def __init__(self,config:RewooAgentConfig):
        self.planner = compose_runnable(config.planner)
        self.solver = compose_runnable(config.solver)
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
        result = self.planner.invoke({"task": state["task"]})
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
    def run(self,task:str):
        for s in self.app.stream({"task": task},config=self.runnable_config):
            print(s)
            print("---")
a = RewooAgent(RewooAgentConfig())
a.run("Find the sitemap for langgraph")