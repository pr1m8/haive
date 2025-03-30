# src/haive/prebuilt/simple/query_batch.py
"""
Agent Name: QueryBatcher
Description: Converts a single query into multiple variations or batched forms for ensemble retrieval or multi-agent use.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig
from src.haive.prebuilt.simple.query_models import QueryInput
from pydantic import BaseModel, Field
from typing import List

SYSTEM_PROMPT = """
You are a query expansion assistant.
Generate multiple rephrasings or variations of the input query that preserve its intent but differ in structure.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class QueryBatch(BaseModel):
    variations: List[str] = Field(..., description="A list of semantically equivalent but syntactically varied versions of the query.")

config = AugLLMConfig(
    name="query_batch",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QueryBatch,
)
