from src.haive.agents.base import AgentConfig
from pydantic import Field
from typing import Optional
from src.haive.agents.contract_analysis.models import ContractInfo, ReviewPlan
from src.haive.agents.base import AgentArchitecture, AgentArchitectureConfig
from src.haive.agents.contract_analysis.state import ContractReviewState
from langgraph.graph import START, END

class ContractAnalysisAgentConfig(AgentArchitectureConfig):
    state_schema: ContractReviewState = Field(default=ContractReviewState,description="The state schema for the contract analysis agent.")

class ContractAnalysisAgent(AgentArchitecture):
    config: ContractAnalysisAgentConfig
    state: ContractReviewState

    def run(self):
        pass
    def setup_workflow(self):
        self.graph.add_node("classify_contract", classify_contract)
        self.graph.add_node("retrieve_clauses", retrieve_clauses)
        self.graph.add_node("execute_step_clause", execute_step_clause)
        self.graph.add_node("create_review_plan", create_review_plan)
        self.graph.add_node("execute_step", execute_step)
        self.graph.add_node("generate_final_report", generate_final_report)

        # Add edges
        self.graph.add_edge(START, "classify_contract")
        self.graph.add_edge("classify_contract", "retrieve_clauses")

        self.graph.add_conditional_edges("retrieve_clauses", continue_to_clauses_check_execute, ["execute_step_clause"])
        self.graph.add_edge("execute_step_clause", "create_review_plan")

        self.graph.add_conditional_edges("create_review_plan", continue_to_plan_check_execute, ["execute_step"])
        self.graph.add_edge("execute_step", "generate_final_report")

        self.graph.add_edge("generate_final_report", END)

        # Compile the graph
