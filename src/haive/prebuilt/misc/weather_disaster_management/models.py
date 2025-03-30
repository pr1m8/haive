from pydantic import BaseModel, Field
from typing import Literal

# --- 2. Output Model ---
class DisasterOutput(BaseModel):
    disaster_type: Literal["flood", "hurricane", "tornado", \
                           "earthquake", "wildfire", "tsunami", \
                            "volcano", "drought", "storm", "other"] = Field(..., description="The type of disaster to manage")



# --- 2. Structured Output Model ---
class SeverityAssessment(BaseModel):
    severity: Literal["Critical", "High", "Medium", "Low"]\
        = Field(..., description="The severity of the disaster")
