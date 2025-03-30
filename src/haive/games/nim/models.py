from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate       



class NimMove(BaseModel):
    """Represents a move in Nim."""
    pile_index: int = Field(..., description="Index of the pile to take from")
    stones_taken: int = Field(..., description="Number of stones to take")
    
class NimAnalysis(BaseModel):
    """Analysis of a Nim position."""
    nim_sum: int = Field(..., description="Binary XOR sum of pile sizes (relevant for optimal play)")
    position_evaluation: str = Field(..., description="Whether position is winning, losing, or unclear")
    recommended_move: NimMove = Field(..., description="Recommended move")
    explanation: str = Field(..., description="Explanation of the analysis")

    def __str__(self):
        return f"Take {self.stones_taken} stones from pile {self.pile_index}"
    