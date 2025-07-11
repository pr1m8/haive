#!/usr/bin/env python3

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Same exact setup as the failing notebook
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

print("🔍 COMPARISON: SimpleAgentV2 vs BaseRAGAgent")
print("=" * 60)

print("\n1️⃣ Testing BaseRAGAgent with same config...")
try:
    # Create vector store config (BaseRAGAgent needs this)
    vectorstore_config = VectorStoreConfig(
        name="test_vectorstore",
        documents=["test document"],  # Minimal docs
    )
    
    # Create BaseRAGAgent 
    rag_agent = BaseRAGAgent(
        name="rag_test",
        engine=vectorstore_config
    )
    
    print("✅ BaseRAGAgent created successfully")
    
    # Test with same input
    print("Testing BaseRAGAgent with input...")
    rag_result = rag_agent.run({"query": "what is the tallest building in france"}, debug=True)
    print("✅ BaseRAGAgent execution SUCCESSFUL")
    
except Exception as e:
    print(f"❌ BaseRAGAgent failed: {e}")
    print("Let me check what BaseRAGAgent schema looks like...")
    
    try:
        rag_agent = BaseRAGAgent(
            name="rag_test", 
            engine=vectorstore_config
        )
        if hasattr(rag_agent, 'composer'):
            schema_class = rag_agent.composer.build()
            print(f"BaseRAGAgent schema: {schema_class}")
            
            # Check critical fields
            for name in ['engine', 'context', 'query']:
                if name in schema_class.model_fields:
                    field_info = schema_class.model_fields[name]
                    print(f"  {name}: required={field_info.is_required()}, default={repr(field_info.default)}")
                else:
                    print(f"  {name}: NOT FOUND")
    except Exception as e2:
        print(f"❌ BaseRAGAgent schema check failed: {e2}")

print("\n2️⃣ Let's trace the state base classes...")

print("\n📋 Checking what base classes are being used:")

try:
    # Import the states that could be involved
    from haive.core.schema.prebuilt.messages_state import MessagesState
    from haive.core.schema.prebuilt.meta_state import MetaStateSchema
    from haive.core.schema.prebuilt.messages.messages_with_token_usage import MessagesStateWithTokenUsage
    
    print("Available base states:")
    print(f"  MessagesState: {MessagesState}")
    print(f"  MetaStateSchema: {MetaStateSchema}")
    print(f"  MessagesStateWithTokenUsage: {MessagesStateWithTokenUsage}")
    
    # Check their fields
    for state_name, state_class in [
        ("MessagesState", MessagesState),
        ("MetaStateSchema", MetaStateSchema), 
        ("MessagesStateWithTokenUsage", MessagesStateWithTokenUsage)
    ]:
        print(f"\n{state_name} fields:")
        for name, field_info in state_class.model_fields.items():
            if name in ['engine', 'context', 'query', 'messages']:
                print(f"  {name}: required={field_info.is_required()}, type={field_info.annotation}")
    
except Exception as e:
    print(f"❌ Error checking base states: {e}")

print("\n3️⃣ Check what base class SimpleAgentV2 actually uses...")

try:
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    
    config = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2"
    )
    
    agent = SimpleAgentV2(engine=config)
    
    # Get the base classes 
    print("SimpleAgentV2 MRO (Method Resolution Order):")
    for i, cls in enumerate(SimpleAgentV2.__mro__):
        print(f"  {i}: {cls}")
    
    # Try to access the composer's detected base class
    if hasattr(agent, 'composer'):
        print(f"\nComposer detected base class: {agent.composer.detected_base_class}")
        print(f"Base class fields: {getattr(agent.composer, 'base_class_fields', 'Not found')}")
    
except Exception as e:
    print(f"❌ Error checking SimpleAgentV2 base classes: {e}")
    import traceback
    traceback.print_exc()