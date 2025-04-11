from typing import TypedDict, Optional, List
from src.haive.agents.contract_analysis.models import ContractInfo, ReviewPlan, Modification
import operator
from typing import Annotated
from pydantic import BaseModel, Field
    
class ContractReviewState(BaseModel):
    contract_text: str = Field(description="The text of the contract to review.")
    primary_objective: str = Field(description="The primary objective of the contract.")
    specific_focus: Optional[str] = Field(description="The specific focus of the contract.")
    contract_info: ContractInfo = Field(description="The information about the contract.")
    review_plan: ReviewPlan = Field(description="The plan for the review.")
    current_step: int = Field(description="The current step in the review process.")
    modifications: Annotated[List[Modification], operator.add] = Field(description="The modifications to the contract.")
    clause_modifications: Annotated[List[Modification], operator.add] = Field(description="The modifications to the clauses of the contract.")
    sections: Annotated[List[str], operator.add] = Field(description="The sections of the contract.")
    clause_analysis: Annotated[List[str], operator.add] = Field(description="The analysis of the clauses of the contract.")
    clauses: Annotated[List[str], operator.add] = Field(description="The clauses of the contract.")
    final_report: str = Field(description="The final report on the contract.")