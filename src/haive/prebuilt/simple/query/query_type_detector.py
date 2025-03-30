# src/haive/prebuilt/simple/query_type_detector.py
"""
Agent Name: QueryTypeDetector
Description: Labels the query as boolean, open-ended, multi-hop, numerical, or instruction.
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig
from src.haive.prebuilt.simple.query_models import QueryInput

SYSTEM_PROMPT = """
You are a query type detector.
Categorize the query into one of the following types:
- boolean
- open-ended
- multi-hop
- numerical
- instruction
Only return the most appropriate label.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class QueryType(BaseModel):
    type: str = Field(..., description="The query type label, such as boolean, multi-hop, or numerical.")

config = AugLLMConfig(
    name="query_type_detector",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QueryType,
)
