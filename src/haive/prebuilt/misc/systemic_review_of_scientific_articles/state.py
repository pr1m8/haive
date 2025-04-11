from typing import TypedDict, List, Dict, Annotated
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableSequence
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence   
from pydantic import BaseModel, Field
import operator
from src.haive.utils.message_utils import reduce_messages


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], reduce_messages] = Field(description="The messages to send to the user"       )
    systematic_review_outline : str = Field(description="The systematic review outline")
    last_human_index : int = Field(description="The last human index")
    papers : Annotated[List[str], operator.add]  = Field(description="The papers downloaded")
    analyses: Annotated[List[Dict], operator.add]  = Field(description="The analysis results")
    combined_analysis: str  = Field(description="The final combined analysis")

    title: str = Field(description="The title of the systematic review")
    abstract : str = Field(description="The abstract of the systematic review")
    introduction : str = Field(description="The introduction of the systematic review")
    methods : str = Field(description="The methods of the systematic review")
    results : str = Field(description="The results of the systematic review")
    conclusion : str = Field(description="The conclusion of the systematic review")
    references : str = Field(description="The references of the systematic review")

    draft : str = Field(description="The draft of the systematic review")
    revision_num : int = Field(description="The revision number of the systematic review")
    max_revisions : int = Field(description="The maximum number of revisions of the systematic review")