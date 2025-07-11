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


# Let's see what's inside the prompt template
for i, message in enumerate(config.prompt_template.messages):
    if hasattr(message, "prompt"):
        prompt = message.prompt

agent = SimpleAgentV2(engine=config)

engine_name = next(iter(agent.engines.keys()))
engine = agent.engines[engine_name]


# Let's see where the context requirement is coming from
state_schema = agent.state_schema()

for field_name, field_info in state_schema.model_fields.items():
    if field_name in ["query", "context", "engine"]:
        pass

try:
    input_schema = agent.input_schema()
    test_input = input_schema(query="test")
except Exception as e:
    pass")

try:
    state_class = agent.state_schema()
    test_state = state_class(query="test", messages=[])
except Exception as e:

    # Try with context
    try:
        test_state = state_class(query="test", context="", messages=[])
    except Exception as e2:
        pass")
