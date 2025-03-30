# src/haive/prebuilt/simple/document_extractor.py
"""
Agent Name: DocumentExtractor
Description: Extracts structured data or targeted fields (e.g. dates, names, numbers, places) from freeform text.
Useful for indexing, templating, and semantic metadata extraction.
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig

SYSTEM_PROMPT = """
You are a structured information extractor.
Given a passage, extract relevant information and return it in a structured form. Prioritize named entities (e.g. person, organization, date, location) and key metadata.
Make sure values are clean, normalized, and non-redundant.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Text: {input}")
])

class ExtractedInfo(BaseModel):
    title: Optional[str] = Field(None, description="Document or passage title, if present.")
    person: Optional[str] = Field(None, description="Main person mentioned in the passage, if any.")
    organization: Optional[str] = Field(None, description="Mentioned organization or institution.")
    location: Optional[str] = Field(None, description="Relevant place or location.")
    date: Optional[str] = Field(None, description="Mentioned date or time period.")
    summary: Optional[str] = Field(None, description="A brief abstract of the passage, if appropriate.")

config = AugLLMConfig(
    name="document_extractor",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=ExtractedInfo,
)