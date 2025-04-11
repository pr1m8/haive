from pydantic import BaseModel, Field
from typing import List

class QueryModel(BaseModel):
    """
    A model for a query.
    """
    query: str = Field(..., description="The query to be decomposed.")

    def __str__(self):
        return self.query
    
    def __repr__(self):
        return self.query
    
    