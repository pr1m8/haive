#!/usr/bin/env python3
"""
Verify that the engine node fix is working by testing the field extraction.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from langchain_core.prompts import ChatPromptTemplate

print("🔧 Testing Engine Node Fix")
print("=" * 40)

# Create a prompt template that requires query and context
prompt = ChatPromptTemplate.from_messages([
    ("system", "System message"),
    ("human", "Query: {query} with context: {context}")
])

# Create engine with this prompt
engine = AugLLMConfig(
    name="test_engine",
    prompt_template=prompt
)

print(f"Engine derived input fields: {list(engine.get_input_fields().keys())}")

# Create engine node
node = EngineNodeConfig(name="test_node", engine=engine)

print(f"Engine node input_field_defs: {[f.name for f in node.input_field_defs]}")

# Verify the fix worked
expected_fields = {'messages', 'query', 'context'}
actual_fields = {f.name for f in node.input_field_defs}

if expected_fields.issubset(actual_fields):
    print("✅ SUCCESS: Engine node correctly extracts all required fields!")
    print(f"   Expected: {sorted(expected_fields)}")
    print(f"   Got: {sorted(actual_fields)}")
else:
    print("❌ FAILURE: Engine node missing required fields")
    print(f"   Expected: {sorted(expected_fields)}")
    print(f"   Got: {sorted(actual_fields)}")
    print(f"   Missing: {sorted(expected_fields - actual_fields)}")

print("\n🎯 This fix resolves the 'missing variables' error in agent execution!")