# src/haive/prebuilt/simple/query_batch.py
"""
Agent Name: QueryBatcher
Description: Converts a single query into multiple variations or batched forms for ensemble retrieval or multi-agent use.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.prebuilt.simple.query.models import QueryModel
from pydantic import BaseModel, Field
from typing import List
from src.haive.agents.simple.factory import create_simple_agent
SYSTEM_PROMPT = """
You are a query expansion assistant.
Generate multiple rephrasings or variations of the input query that preserve its intent but differ in structure.
"""

query_batch_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class QueryBatch(BaseModel):
    variations: List[QueryModel] = Field(..., description="A list of semantically equivalent but syntactically varied versions of the query.")

query_batch_config = AugLLMConfig(
    name="query_batch",
    llm_config=AzureLLMConfig(),
    prompt_template=query_batch_prompt,
    structured_output_model=QueryBatch,
)

query_batch = create_simple_agent(
    engine=query_batch_config,
    name="query_batch"
)

a = query_batch.invoke(input_data={"query":"Generate some queries to do kyc on bitfinex"})
print(a)