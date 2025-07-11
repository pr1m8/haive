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




for i, msg in enumerate(RAG_QUERY_REFINEMENT.messages):
    if hasattr(msg, "prompt"):

config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2",
)


input_vars = config._get_input_variables()

input_fields = config.get_input_fields()


# Reproduce the logic step by step
all_vars = set()

# Direct input_variables attribute
if hasattr(config.prompt_template, "input_variables"):
    vars_list = getattr(config.prompt_template, "input_variables", [])
    all_vars.update(vars_list)

# Chat templates message variables
if isinstance(config.prompt_template, ChatPromptTemplate):
    # Get partial variables to exclude them from required inputs
    partial_vars = getattr(config.prompt_template, "partial_variables", {})

    for i, msg in enumerate(config.prompt_template.messages):
        if hasattr(msg, "prompt") and hasattr(msg.prompt, "input_variables"):
            # Only add variables that are NOT in partial_variables
            msg_vars = set(msg.prompt.input_variables) - set(partial_vars.keys())
            all_vars.update(msg_vars)

