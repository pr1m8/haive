#!/usr/bin/env python3
"""Test to see the exact BaseOutputParser error in LangGraph context."""


from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# Create the exact scenario from the notebook
class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")


RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [("system", "You are a query optimizer"), ("human", "{query}")]
)

# Import our components
from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent
agent = SimpleAgentV2(
    engine=AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )
)

# Check if BaseOutputParser is in the state schema's namespace

# Check the state schema

# Check the engine field
engine_field = agent.state_schema.model_fields.get("engine")
if engine_field:

# The key issue: when LangGraph compiles the graph, it evaluates type hints

from typing import get_type_hints

from langgraph.graph import StateGraph

# This is what LangGraph does internally
try:
    # First, build the graph
    graph = agent.build_graph()

    # Then compile it - this is where the error happens
    compiled = graph.compile()

except NameError as e:

except Exception as e:
    import traceback

    traceback.print_exc()

# Let's try to reproduce the exact type hints evaluation

# Import state schema to local namespace
state_schema = agent.state_schema

# This simulates what LangGraph does
try:
    # LangGraph does this: get_type_hints(schema, localns={schema.__name__: schema})
    localns = {state_schema.__name__: state_schema}
    hints = get_type_hints(state_schema, localns=localns)
except NameError as e:

# Test if we can make BaseOutputParser available
try:
    # Add BaseOutputParser to the namespace

    localns = {
        state_schema.__name__: state_schema,
        "BaseOutputParser": BaseOutputParser,
        "AugLLMConfig": AugLLMConfig,
    }
    hints = get_type_hints(state_schema, localns=localns)
except Exception as e:
    pass")
