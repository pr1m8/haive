from pydantic import BaseModel, Field

class ApproachState(BaseModel):
    plan: str = Field(description="detailed workflow of the approach")
    style: str = Field(description="style description of the approach")
    task: str = Field(description="user's input of task")
    details: str = Field(description="internet retrieval of task specs")
    history: str = Field(description="description of history approaches")



