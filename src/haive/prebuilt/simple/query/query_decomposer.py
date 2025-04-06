# src/haive/prebuilt/simple/query_decomposer.py
"""
Agent Name: QueryDecomposer
Description: Breaks down a complex query into smaller, logically ordered sub-queries.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.aug_llm import AugLLMConfig
from src.haive.prebuilt.simple.query.models import QueryModel
from pydantic import BaseModel, Field
from typing import List
from src.haive.agents.simple.factory import create_simple_agent

SYSTEM_PROMPT = """
You are an expert query planner. Given a complex question, break it down into smaller, logical sub-questions that can be answered independently.
List them in the order they should be answered.
"""

query_decomposer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class DecomposedQuery(BaseModel):
    subqueries: List[str] = Field(..., description="Ordered list of sub-questions extracted from the input query.")

query_decomposer_config = AugLLMConfig(
    name="query_decomposer",
    llm_config=AzureLLMConfig(),
    prompt_template=query_decomposer_prompt,
    structured_output_model=DecomposedQuery,
)

query_decomposer = create_simple_agent(
    engine=query_decomposer_config,
    name="query_decomposer"
)
