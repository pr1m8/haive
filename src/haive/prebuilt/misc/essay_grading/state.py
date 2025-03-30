from pydantic import BaseModel, Field


class EssayGradingInputState(BaseModel):
    """Represents the input state of the essay grading process."""
    essay: str = Field(description="The essay to grade")
class EssayGradingOutputState(BaseModel):
    relevance_score: float = Field(description="The relevance score of the essay")
    grammar_score: float = Field(description="The grammar score of the essay")
    structure_score: float = Field(description="The structure score of the essay")
    depth_score: float = Field(description="The depth score of the essay")
    final_score: float = Field(description="The final score of the essay")
class EssayGradingState(BaseModel,EssayGradingInputState,EssayGradingOutputState):
    """Represents the state of the essay grading process."""
    pass