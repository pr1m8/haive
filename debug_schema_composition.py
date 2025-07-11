#!/usr/bin/env python3
"""Debug schema composition issue with AugLLMConfig."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer
from langchain_core.prompts import ChatPromptTemplate

# Create a simple prompt template
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "{query}")
])

# Create AugLLMConfig
config = AugLLMConfig(
    prompt_template=simple_prompt,
    temperature=0.7
)

print("=== Debugging Schema Composition ===")
print(f"AugLLMConfig engine_type: {config.engine_type}")
print(f"AugLLMConfig has tools: {hasattr(config, 'tools') and config.tools}")

# Create composer and detect base class
composer = SchemaComposer(name="TestSchema")

# Add the config to components
print("\nAdding AugLLMConfig to composer...")
composer.add_fields_from_components([config])

# Check what base class was detected
print(f"\nDetected base class: {composer.detected_base_class}")
print(f"Has messages: {composer.has_messages}")
print(f"Has tools: {composer.has_tools}")

# Build the schema
print("\nBuilding schema...")
schema = composer.build()

print("\n=== Schema Fields ===")
for field_name, field_info in schema.__fields__.items():
    default_value = field_info.default
    if default_value is ...:
        print(f"❌ {field_name}: PydanticUndefined (...)")
    else:
        print(f"✓ {field_name}: {type(default_value).__name__} = {default_value}")

print("\n=== Schema MRO ===")
for cls in schema.__mro__:
    print(f"  - {cls.__name__}")

# Try to instantiate the schema
print("\n=== Creating Instance ===")
try:
    instance = schema()
    print("✓ Successfully created instance")
    
    # Check field values
    print("\n=== Instance Field Values ===")
    for field_name in schema.__fields__.keys():
        value = getattr(instance, field_name)
        if value is ...:
            print(f"❌ {field_name}: PydanticUndefined (...)")
        else:
            print(f"✓ {field_name}: {type(value).__name__}")
            
except Exception as e:
    print(f"❌ Failed to create instance: {e}")
    import traceback
    traceback.print_exc()

# Test the from_components class method
print("\n\n=== Testing from_components class method ===")
try:
    schema_class = SchemaComposer.from_components([config], name="DirectSchema")
    print(f"✓ Created schema class: {schema_class.__name__}")
    
    instance2 = schema_class()
    print("✓ Successfully created instance from from_components")
    
except Exception as e:
    print(f"❌ Failed with from_components: {e}")
    import traceback
    traceback.print_exc()