#!/usr/bin/env python3

from typing import List

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

**Analysis Required:**
1. Analyze the current query's strengths and weaknesses
2. Classify the query type and complexity
3. Provide multiple refinement suggestions
4. Recommend the best refined query
5. Suggest optimal search strategies

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""",
        ),
    ]
).partial(context="")


class QueryRefinementSuggestion(BaseModel):
    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(description="Type of improvement made")
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(
        description="Expected improvement in retrieval or answering"
    )


class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(
        description="Analysis of the original query's strengths and weaknesses"
    )
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(
        description="List of suggested query improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: list[str] = Field(
        description="Recommendations for search strategy"
    )




config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2",
)



# Patch the schema composer to add debug logging
import haive.core.schema.schema_composer as schema_composer_module

original_add_engine = schema_composer_module.SchemaComposer.add_engine


def debug_add_engine(self, engine):

    if hasattr(engine, "prompt_template"):

    result = original_add_engine(self, engine)

    if hasattr(self, "input_fields"):
        pass

    return result


schema_composer_module.SchemaComposer.add_engine = debug_add_engine

# Also patch the engine registration
from haive.core.engine.base.engine_registry import EngineRegistry

original_register = EngineRegistry.register


def debug_register(self, engine):

    if hasattr(engine, "prompt_template"):
        prompt = engine.prompt_template

    result = original_register(self, engine)
    return result


EngineRegistry.register = debug_register

agent = SimpleAgentV2(engine=config)

engine_name = next(iter(agent.engines.keys()))
engine = agent.engines[engine_name]


state_schema = agent.state_schema()
for field_name, field_info in state_schema.model_fields.items():
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        extra = field_info.json_schema_extra
        if isinstance(extra, dict) and any("input" in str(v) for v in extra.values()):
            pass

