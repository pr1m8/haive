#!/usr/bin/env python3
"""Trace the exact error location."""






from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# Recreate the notebook scenario
class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")


RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [("system", "You are a query optimizer"), ("human", "{query}")]
)

agent = SimpleAgentV2(
    engine=AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )
)

for name, field in agent.state_schema.model_fields.items():
    if name == "engine":



