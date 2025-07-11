#!/usr/bin/env python3

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Exact notebook setup
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query optimization specialist for RAG systems...""",
        ),
        (
            "human",
            """Analyze and refine the following user query to improve retrieval and answer quality.

**Original Query:** {query}

**Context (if provided):** {context}

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""",
        ),
    ]
).partial(context="")


class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")



config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2",
)

computed_fields = config._compute_input_fields()
for field_name, field_def in computed_fields.items():
    field_type, field_info = field_def
    if hasattr(field_info, "default"):
        pass
    if hasattr(field_info, "default_factory"):
        pass

input_fields = config.get_input_fields()
for field_name, field_def in input_fields.items():
    field_type, field_info = field_def
    if hasattr(field_info, "default"):
        pass
    if hasattr(field_info, "default_factory"):
        pass

for field_name, field_def in input_fields.items():
    field_type, field_info = field_def
    if hasattr(field_info, "default") and field_info.default is ...:
        pass")
    elif hasattr(field_info, "default"):
        pass")
    elif hasattr(field_info, "default_factory"):
        pass")
    else:
        pass")
