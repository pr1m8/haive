#!/usr/bin/env python3

"""
Focused debug: Trace exactly how the schema composer builds the final schema
and why engine/context fields are marked as required.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import logging

# Enable debug logging for schema composer
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Exact notebook setup
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert query optimization specialist..."""),
    ("human", """Analyze and refine the following user query.

**Original Query:** {query}
**Context (if provided):** {context}

Focus on improvements.""")
]).partial(context="")

class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")

print("🔍 FOCUSED SCHEMA COMPOSITION DEBUG")
print("=" * 60)

print("\n1️⃣ Create the AugLLMConfig...")
config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2"
)

print("\n2️⃣ Check what base class the schema composer detects...")

# Create composer like the agent does
composer = SchemaComposer(name="TestState")

# Add engine fields
composer.add_fields_from_engine(config)

print(f"Composer detected base class: {composer.detected_base_class}")
print(f"Base class fields: {getattr(composer, 'base_class_fields', {})}")

print("\n3️⃣ Check what happens with different base class scenarios...")

# Let's see what happens if we set tools
composer_with_tools = SchemaComposer(name="TestStateWithTools")
composer_with_tools.has_tools = True  # Force tool detection
composer_with_tools.add_fields_from_engine(config)

print(f"With tools - detected base class: {composer_with_tools.detected_base_class}")

print("\n4️⃣ Let's trace the field creation step by step...")

# Step-by-step field creation
print("Engine input fields:")
input_fields = config.get_input_fields()
for name, (field_type, field_info) in input_fields.items():
    if name in ['engine', 'context', 'query']:
        print(f"  {name}: type={field_type}, required={getattr(field_info, 'is_required', lambda: 'N/A')()}")

print("\n5️⃣ Check schema composer field processing...")

# Check composer fields before build
print("Composer fields before build:")
for name, field_def in composer.fields.items():
    if name in ['engine', 'context', 'query']:
        print(f"  {name}: {field_def}")

print("\n6️⃣ Build schema and check the result...")
final_schema = composer.build()

print("Final schema fields:")
for name, field_info in final_schema.model_fields.items():
    if name in ['engine', 'context', 'query']:
        print(f"  {name}: required={field_info.is_required()}, default={field_info.default}, type={field_info.annotation}")

print("\n7️⃣ Test the schema validation directly...")

# Test schema validation
test_data = {
    "query": "test query"
    # Missing context and engine intentionally
}

try:
    instance = final_schema.model_validate(test_data)
    print("✅ Schema validation succeeded!")
    print(f"Instance: {instance}")
except Exception as e:
    print(f"❌ Schema validation failed: {e}")
    
print("\n8️⃣ Test with full data...")
test_data_full = {
    "query": "test query",
    "context": "",
    "engine": config
}

try:
    instance = final_schema.model_validate(test_data_full)
    print("✅ Full schema validation succeeded!")
except Exception as e:
    print(f"❌ Full schema validation failed: {e}")

print("\n9️⃣ Check if the issue is in base class selection...")
# Let's check what the composer's _detect_base_class_requirements method is doing
print("Tracing base class detection...")
print(f"has_tools: {composer.has_tools}")
print(f"engines: {list(composer.engines.keys())}")
print(f"Number of LLM engines: {len([e for e in composer.engines.values() if hasattr(e, 'engine_type') and str(e.engine_type) == 'EngineType.LLM'])}")

# Call the base class detection explicitly
composer._detect_base_class_requirements()
print(f"After detection - base class: {composer.detected_base_class}")
print(f"After detection - base class fields: {composer.base_class_fields}")