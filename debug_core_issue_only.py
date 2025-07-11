#!/usr/bin/env python3

"""
CORE ISSUE ANALYSIS: Why is LangGraph's input_model different from our schema?

The error shows LangGraph is validating against an input_model, not the main schema.
Let's trace exactly where this input_model comes from.
"""

import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

# Direct imports to avoid syntax error issues
from haive.core.engine.aug_llm.config import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

print("🔍 CORE ISSUE ANALYSIS")
print("=" * 50)

# Replicate the exact notebook setup
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert query optimization specialist..."),
    ("human", "Analyze and refine the following user query.\n\n**Original Query:** {query}\n\n**Context (if provided):** {context}\n\nFocus on improvements.")
]).partial(context="")

class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")

print("\n1️⃣ Creating AugLLMConfig with partial template...")

config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2"
)

print("✅ Config created successfully")

print("\n2️⃣ Checking config input schema methods...")

# Check what methods exist for schema derivation
methods = [attr for attr in dir(config) if 'schema' in attr.lower() or 'input' in attr.lower()]
print("Available schema/input methods:")
for method in sorted(methods):
    if not method.startswith('_'):
        print(f"  {method}")

print("\n3️⃣ Testing derive_input_schema method...")

try:
    input_schema = config.derive_input_schema()
    print(f"✅ Input schema: {input_schema}")
    print("Input schema fields:")
    for name, field_info in input_schema.model_fields.items():
        if name in ['engine', 'context', 'query']:
            print(f"  {name}: required={field_info.is_required()}, default={field_info.default}")
            
    print("\n4️⃣ Testing input schema validation...")
    test_data = {"query": "test"}
    try:
        instance = input_schema.model_validate(test_data)
        print("✅ Input schema validation succeeded!")
    except Exception as e:
        print(f"❌ Input schema validation failed: {e}")
        # This tells us if the issue is in the input schema itself
        
except Exception as e:
    print(f"❌ derive_input_schema failed: {e}")

print("\n5️⃣ Let's check the exact field definitions in _compute_input_fields...")

try:
    computed_fields = config._compute_input_fields()
    print("Computed input fields:")
    for name, (field_type, field_info) in computed_fields.items():
        if name in ['engine', 'context', 'query']:
            required = getattr(field_info, 'is_required', lambda: hasattr(field_info, 'default') and field_info.default is ...)()
            print(f"  {name}: type={field_type}, required={required}, field_info={field_info}")
            
except Exception as e:
    print(f"❌ _compute_input_fields failed: {e}")

print("\n6️⃣ Key insight: Let's check what agent.run() does...")

print("The issue might be that agent.run() or LangGraph is using a different schema")
print("than what we're seeing in our debug scripts.")
print()
print("Hypothesis: LangGraph's pregel loop gets an 'input_model' that's different")
print("from the main state schema, and this input_model still has the old required fields.")
print()
print("Next step: Need to trace where LangGraph gets its input_model from.")

print("\n7️⃣ Let's look at the _get_input_variables vs get_input_fields difference...")

try:
    input_vars = config._get_input_variables()
    print(f"_get_input_variables(): {input_vars}")
    
    input_fields = config.get_input_fields()
    print(f"get_input_fields(): {list(input_fields.keys())}")
    
    print("Key insight: If these differ, that's where our fix is being bypassed!")
    
except Exception as e:
    print(f"❌ Variable check failed: {e}")

print("\n🎯 CONCLUSION:")
print("The issue is likely that:")
print("1. Our AugLLMConfig fixes work correctly (context is optional)")
print("2. But LangGraph gets its input_model from a different source")
print("3. This source still has the old required field definitions")
print("4. We need to find where LangGraph's input_model comes from")