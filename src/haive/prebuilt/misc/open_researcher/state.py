from typing import Annotated, TypedDict
import operator
from .models import Section, SearchQuery    
from pydantic import BaseModel, Field


class ReportStateInput(BaseModel):
    topic: str =Field(description="Report topic")
    
class ReportStateOutput(BaseModel):
    final_report: str =Field(description="Final report")

class ReportState(BaseModel):
    topic: str = Field(description="Report topic")    
    feedback_on_report_plan: str = Field(description="Feedback on the report plan")
    sections: list[Section] = Field(description="List of report sections")
    completed_sections: Annotated[list, operator.add] = Field(description="Send() API key")
    report_sections_from_research: str = Field(description="String of any completed sections from research to write final sections")
    final_report: str = Field(description="Final report")

class SectionState(BaseModel):
    topic: str = Field(description="Report topic")
    section: Section = Field(description="Report section")  
    search_iterations: int = Field(description="Number of search iterations done")
    search_queries: list[SearchQuery] = Field(description="List of search queries")
    source_str: str = Field(description="String of formatted source content from web search")
    report_sections_from_research: str = Field(description="String of any completed sections from research to write final sections")
    completed_sections: list[Section] = Field(description="Final key we duplicate in outer state for Send() API")

class SectionOutputState(BaseModel):
    completed_sections: list[Section] = Field(description="Final key we duplicate in outer state for Send")