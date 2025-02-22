"""State for the summarizer agent"""
from typing import List,Annotated
from langchain_core.documents import Document
import operator
from pydantic import BaseModel,Field
from typing_extensions import TypedDict

class SummaryState(TypedDict):
    """State for the summarizer agent - we use the operator.add to combine the summaries"""
    contents: List[str] = Field(default_factory=list,description="The contents of the documents")
    summaries: Annotated[list, operator.add] = Field(default_factory=list,description="The summaries of the documents")
    collapsed_summaries: List[Document] = Field(default_factory=list,description="The collapsed summaries of the documents")
    final_summary: str = Field(default="",description="The final summary of the documents")