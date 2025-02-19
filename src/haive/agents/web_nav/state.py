from src.haive.agents.web_nav.models import BBox,Prediction
from langchain_core.messages import BaseMessage, SystemMessage
from playwright.async_api import Page
from typing_extensions import List,TypedDict
from pydantic import Field
class WebNavState(TypedDict):
    """Web Navigation State"""
    page: Page = Field(...,description="The Playwright web page lets us interact with the web environment")
    input: str = Field(...,description="User request")
    img: str = Field(...,description="b64 encoded screenshot")
    bboxes: List[BBox] = Field(...,description="The bounding boxes from the browser annotation function")
    prediction: Prediction = Field(...,description="The Agent's output")
    # A system message (or messages) containing the intermediate steps
    scratchpad: List[BaseMessage] = Field(...,description="A system message (or messages) containing the intermediate steps")
    observation: str = Field(...,description="The most recent response from a tool")

    