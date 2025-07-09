# test_node_factory.py

import uuid
from typing import List

from langchain_core.messages import HumanMessage
from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.schema.schema_composer import SchemaComposer


# Define a test output schema
class Plan(BaseModel):
    Steps: List[str] = Field(description="A list of steps to complete the task")


# Create an AugLLM engine
aug_llm = AugLLMConfig(
    id=f"engine_{uuid.uuid4().hex[:8]}",
    name="test_engine",
    system_prompt="You are a helpful assistant that can help me plan my day.",
    structured_output_model=Plan,
)

# Create a test state schema using SchemaComposer
schema = SchemaComposer.from_components([aug_llm])
state_schema = schema
input_schema = schema.create_input_schema()
output_schema = schema.create_output_schema()

# Create a node config
node_config = NodeConfig(
    name="plan_generator",
    engine=aug_llm,
    state_schema=state_schema,
    input_schema=input_schema,
    output_schema=output_schema,
    command_goto=END,
)

# Create a node function
node_function = NodeFactory.create_node_function(node_config)

# Create a test state
test_state = {"messages": [HumanMessage(content="Write a plan for building a website")]}

# Invoke the node function
result = node_function(test_state)

# Print the result
print("Result type:", type(result))
print("Command goto:", result.goto)
print("Command update:", result.update)

# Check if plan was generated
if "plan" in result.update:
    plan = result.update["plan"]
    print("\nGenerated Plan:")
    print("Steps:", plan.Steps if hasattr(plan, "Steps") else plan)
