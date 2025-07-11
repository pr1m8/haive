#!/usr/bin/env python3
"""Test to understand the BaseOutputParser issue."""

import asyncio
from typing import Optional

# Test 1: Create AugLLMConfig with output_parser
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Create with an actual parser instance
str_parser = StrOutputParser()

config_with_parser = AugLLMConfig(output_parser=str_parser)

# Test 2: Create SimpleAgent v2 without output_parser
from haive.agents.simple.agent_v2 import SimpleAgentV2

agent = SimpleAgentV2(engine=AugLLMConfig())

# Test 3: Check state schema
for name, field in agent.state_schema.model_fields.items():
    # Check if this field has BaseOutputParser in its type
    if "BaseOutputParser" in str(field.annotation):
        passr!")

# Test 4: Check the engine field specifically
engine_field = agent.state_schema.model_fields.get("engine")
if engine_field:

    # Check if it's the actual class or a forward reference
    from typing import get_args, get_origin

    origin = get_origin(engine_field.annotation)
    args = get_args(engine_field.annotation)

# Test 5: Create agent with structured output


class TestOutput(BaseModel):
    answer: str = Field(description="The answer")
    confidence: float = Field(description="Confidence score")


prompt = ChatPromptTemplate.from_messages([("human", "{query}")])

agent_with_output = SimpleAgentV2(
    engine=AugLLMConfig(
        prompt_template=prompt,
        structured_output_model=TestOutput,
        structured_output_version="v2",
    )
)

# Test 6: Check if the issue is in graph compilation
try:
    graph = agent.build_graph()
    compiled = graph.compile()
except Exception as e:
    pass")

# Test 7: The actual invocation


async def test_invocation():
    try:
        # This is where the error occurs
        result = await agent.arun({"messages": [], "query": "test"})
    except NameError as e:
    except Exception as e:
        import traceback

        traceback.print_exc()


asyncio.run(test_invocation())

# Test 8: Check type hints evaluation
from typing import get_type_hints

try:
    # Try to get type hints for the state schema
    hints = get_type_hints(agent.state_schema)
    for name, hint in hints.items():
        pass
except NameError as e:
