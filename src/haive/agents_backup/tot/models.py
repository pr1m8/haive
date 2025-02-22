
from typing_extensions import Optional
from pydantic import BaseModel,Field

# Problem description model
class Problem(BaseModel):
    """Problem description model"""
    description: str = Field(description="Description of the problem")


# Candidate and ScoredCandidate models
class Candidate(BaseModel):
    """Candidate solution (e.g., text or data)"""
    candidate: str = Field(description="Candidate solution (e.g., text or data)")
    


class ScoredCandidate(BaseModel):
    """Scored candidate solution"""
    candidate: Candidate = Field(description="Candidate solution (e.g., text or data)")
    score: float = Field(description="Score of the candidate solution")
    feedback: str = Field(description="Feedback on the candidate solution")