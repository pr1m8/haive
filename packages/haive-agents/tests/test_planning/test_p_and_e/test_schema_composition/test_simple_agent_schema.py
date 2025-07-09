"""Test script to debug SimpleAgent schema generation."""

import sys

sys.path.append("/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.append("/home/will/Projects/haive/backend/haive/packages/haive-agents/src")

from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field

from haive.agents.simple.agent import SimpleAgent


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create engine
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

# Create agent
simple_agent = SimpleAgent(engine=plan_aug)

# Check the state schema

# Check model fields
if hasattr(simple_agent.state_schema, "model_fields"):
    for field_name, field_info in simple_agent.state_schema.model_fields.items():
        pass

# Create state instance
state_instance = simple_agent.state_schema()

# Check for engine fields

if hasattr(state_instance, "engine"):
    pass

if hasattr(state_instance, "engines"):

# Check if schema has class-level engines
if hasattr(simple_agent.state_schema, "engines"):
    pass
if hasattr(simple_agent.state_schema, "engines_by_type"):
    pass
