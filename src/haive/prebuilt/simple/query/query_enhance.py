# src/haive/prebuilt/simple/query_enhancer.py
"""
Agent Name: QueryEnhancer
Description: Enriches a query by adding relevant context, assumptions, or metadata.
Useful for boosting reasoning or LLM effectiveness.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig
from src.haive.prebuilt.simple.query_models import QueryInput
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are a semantic enhancer.
Given a query, enrich it by adding relevant implicit information, assumptions, and metadata to make it more complete and self-contained.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class EnhancedQuery(BaseModel):
    enriched_query: str = Field(..., description="The enriched version of the query with added implicit information or assumptions.")

config = AugLLMConfig(
    name="query_enhancer",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=EnhancedQuery,
)