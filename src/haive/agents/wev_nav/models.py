from typing import List, Optional
from typing_extensions import TypedDict


from pydantic import Field
class BBox(TypedDict):
    """Bounding box for the action to take"""
    x: float = Field(...,description="The x coordinate of the bounding box")
    y: float = Field(...,description="The y coordinate of the bounding box")
    text: str = Field(...,description="The text of the bounding box")
    type: str = Field(...,description="The type of the bounding box")
    ariaLabel: str = Field(...,description="The aria label of the bounding box")


class Prediction(TypedDict):
    """Prediction for the action to take"""
    action: str = Field(default="click",description="The action to take")
    args: Optional[List[str]] = Field(...,description="The arguments to the action")


