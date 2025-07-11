from typing import List, TypedDict

from pydantic import BaseModel, Field, computed_field

from haive.agents.research.storm.generate_perspectives.models import Editor
from haive.agents.research.storm.interview.models import InterviewState
from haive.agents.research.storm.outline_generator.models import Outline
from haive.agents.research.storm.section_writer.models import WikiSection


class TopicState(BaseModel):
    topic: str = Field(..., description="The topic of the research")


class ArticleState(BaseModel):
    article: str = Field(..., description="The final article of the research")


class ResearchState(TopicState, ArticleState):
    topic: TopicState = Field(..., description="The topic of the research")
    outline: Outline = Field(..., description="The outline of the research")
    editors: list[Editor] = Field(..., description="The editors of the research")
    interview_results: list[InterviewState] = Field(
        ..., description="The interview results of the research"
    )
    # The final sections output
    sections: list[WikiSection] = Field(
        ..., description="The final sections of the research"
    )

    @computed_field
    @property
    def draft(self) -> str:
        return "\n\n".join([section.as_str for section in self.sections])
