#!/usr/bin/env python3

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Exact notebook setup
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert query optimization specialist for RAG systems..."""),
    ("human", """Analyze and refine the following user query to improve retrieval and answer quality.

**Original Query:** {query}

**Context (if provided):** {context}

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""")
]).partial(context="")

class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")

print("🔍 AGENT SCHEMA CREATION DEBUG")
print("=" * 50)

print("\n1️⃣ Create AugLLMConfig like the agent does...")
config = AugLLMConfig(
    prompt_template=RAG_QUERY_REFINEMENT,
    structured_output_model=QueryRefinementResponse,
    structured_output_version="v2"
)

print("\n2️⃣ Test what happen when we pass this to agent constructor...")
print("First, let's see what SimpleAgentV2 expects:")

try:
    # Try to import and see class definition
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    print("✅ SimpleAgentV2 imported successfully")
    
    print("\n3️⃣ Check SimpleAgentV2 model_fields...")
    for name, field_info in SimpleAgentV2.model_fields.items():
        if name in ['engine', 'structured_output_model', 'prompt_template']:
            print(f"  {name}:")
            print(f"    required: {field_info.is_required()}")
            print(f"    default: {field_info.default}")
            print(f"    default_factory: {field_info.default_factory}")
    
    print("\n4️⃣ Try creating agent with our config...")
    agent = SimpleAgentV2(engine=config)
    print("✅ Agent created successfully")
    
    print("\n5️⃣ Check agent's final state schema...")
    if hasattr(agent, 'composer'):
        schema_class = agent.composer.build()
        print(f"Final schema: {schema_class}")
        
        # Check the problematic fields
        for name in ['engine', 'context', 'query']:
            if name in schema_class.model_fields:
                field_info = schema_class.model_fields[name]
                print(f"  {name}: required={field_info.is_required()}, default={repr(field_info.default)}")
            else:
                print(f"  {name}: NOT FOUND in schema")
    else:
        print("❌ Agent has no composer attribute")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()