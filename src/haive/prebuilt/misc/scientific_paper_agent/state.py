from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from src.haive.utils.message_utils import add_messages
from pydantic import BaseModel,Field


class ScientificPaperAgentState(BaseModel):
    """The state of the agent during the paper research process."""
    requires_research: bool = Field(description="Whether the user query requires research or not.")
    num_feedback_requests: int = Field(description="The number of feedback requests made to the user.")
    is_good_answer: bool = Field(description="Whether the answer is good or not.")
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(description="The messages to send to the user")