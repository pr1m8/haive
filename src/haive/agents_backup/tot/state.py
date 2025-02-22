from pydantic import BaseModel,Field
from typing_extensions import Optional,List,TypedDict
from src.haive.agents.tot.models import Problem,Candidate,ScoredCandidate

class ToTState(TypedDict):
    """State for the ToT agent"""
    problem: Problem = Field(description="Problem description")
    candidates: List[Candidate] = Field(description="List of candidates")
    scored_candidates: List[ScoredCandidate] = Field(description="List of scored candidates")
    depth: int = Field(description="Depth of the ToT tree")
    best_candidate: Optional[ScoredCandidate] = Field(default=None,description="Best candidate")
