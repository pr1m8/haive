from typing import Annotated, List
import operator
from pydantic import BaseModel,Field
from typing import Annotated, List
class PodcastGeneratorState(BaseModel):
    topic: Annotated[str, operator.add] = Field(description="The overall topic of the podcast")
    keywords: List = Field(description="Keywords related to the podcast")
    max_analysts: int = Field(description="The maximum number of analysts to use")
    subtopics: List = Field(description="Subtopics related to the podcast")
    sections: Annotated[list, operator.add] = Field(description="The sections of the podcast")
    introduction: str = Field(description="The introduction of the podcast")
    content: str = Field(description="The content of the podcast")
    conclusion: str = Field(description="The conclusion of the podcast")
    final_report: str = Field(description="The final report of the podcast")