#!/usr/bin/env python3

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.schema_composer import SchemaComposer
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

composer = SchemaComposer(name="TestState")

composer.add_fields_from_engine(config)

schema_class = composer.build()


for field_name, field_info in schema_class.model_fields.items():
    if field_name in ["query", "context", "engine"]:

try:
    test_data = {"query": "test"}
    instance = schema_class.model_validate(test_data)
except Exception as e:
    pass

try:
    empty_data = {}
    instance = schema_class.model_validate(empty_data)
except Exception as e:
    pass

for name, info in schema_class.model_fields.items():
    if name in ["query", "context", "engine"]:
        pass
