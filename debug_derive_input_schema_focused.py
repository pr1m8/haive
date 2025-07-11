#!/usr/bin/env python3

import traceback

from haive.agents.simple.agent_v2 import SimpleAgentV2
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


try:
    aug_llm_input_schema = config.derive_input_schema()

    # Test creating an instance
    try:
        test_input = aug_llm_input_schema(query="test query")
    except Exception as e:
        pass")

except Exception as e:
    traceback.print_exc()

try:
    agent = SimpleAgentV2(engine=config)
except Exception as e:
    traceback.print_exc()
    exit()

try:
    state_schema_class = agent.state_schema()

    # Check which fields are marked as required
    required_fields = []
    optional_fields = []
    for field_name, field_info in state_schema_class.model_fields.items():
        if field_info.is_required():
            required_fields.append(field_name)
        else:
            optional_fields.append(field_name)


except Exception as e:
    traceback.print_exc()

try:
    agent_input_schema = agent.input_schema()

    # Check which fields are marked as required
    required_fields = []
    optional_fields = []
    for field_name, field_info in agent_input_schema.model_fields.items():
        if field_info.is_required():
            required_fields.append(field_name)
        else:
            optional_fields.append(field_name)


    # Test creating an input instance
    try:
        test_input = agent_input_schema(query="test query")
    except Exception as e:

except Exception as e:
    traceback.print_exc()

try:
    state_schema_class = agent.state_schema()

    # Try the state schema's derive_input_schema method
    state_derived_input = state_schema_class.derive_input_schema()

    # Check which fields are marked as required
    required_fields = []
    for field_name, field_info in state_derived_input.model_fields.items():
        if field_info.is_required():
            required_fields.append(field_name)


    # Test creating an instance
    try:
        test_input = state_derived_input(query="test query")
    except Exception as e:
        pass")

except Exception as e:
    traceback.print_exc()

try:
    result = agent.run({"query": "what is the tallest building in france"}, debug=True)
except Exception as e:
    traceback.print_exc()
