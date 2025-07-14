#!/usr/bin/env python3
"""Debug script to test prompt template variable handling."""

import asyncio
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Create the same prompt template from the test
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert query optimization specialist."),
    ("human", """Analyze and refine the following user query.

**Original Query:** {query}
**Context (if provided):** {context}

Provide analysis and suggestions."""),
]).partial(context="")

class QueryRefinementResponse(BaseModel):
    """Query refinement analysis."""
    original_query: str = Field(description="The original user query")
    refined_query: str = Field(description="The improved query")

def test_prompt_template_directly():
    """Test the prompt template directly to see what it expects."""
    print("🔍 Testing RAG_QUERY_REFINEMENT template directly...")
    
    # Check template properties
    print(f"Template type: {type(RAG_QUERY_REFINEMENT)}")
    print(f"Input variables: {RAG_QUERY_REFINEMENT.input_variables}")
    print(f"Optional variables: {getattr(RAG_QUERY_REFINEMENT, 'optional_variables', [])}")
    print(f"Partial variables: {RAG_QUERY_REFINEMENT.partial_variables}")
    
    # Test with proper variables
    try:
        formatted = RAG_QUERY_REFINEMENT.format(query="what is the tallest building in france")
        print(f"✅ Template formatting SUCCESS!")
        print(f"Formatted length: {len(formatted)} chars")
    except Exception as e:
        print(f"❌ Template formatting FAILED: {e}")

def test_augllm_config():
    """Test AugLLMConfig with the prompt template."""
    from haive.core.engine.aug_llm import AugLLMConfig
    
    print("\n🔍 Testing AugLLMConfig with custom prompt template...")
    
    config = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version='v2'
    )
    
    print(f"Config created: {config.name}")
    print(f"Template in config: {type(config.prompt_template)}")
    print(f"Template input_variables: {getattr(config.prompt_template, 'input_variables', [])}")
    
    # Test what happens when we provide input data as dict
    input_data = {"query": "what is the tallest building in france"}
    print(f"Input data: {input_data}")
    
    # Check if the engine can handle this
    print("✨ This is where the issue likely occurs - engine.invoke(input_data) doesn't map dict keys to template variables")

async def test_simple_agent():
    """Test SimpleAgent with debug output."""
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    
    print("\n🔍 Testing SimpleAgentV2 with custom prompt template...")
    
    try:
        agent = SimpleAgentV2(
            engine=AugLLMConfig(
                prompt_template=RAG_QUERY_REFINEMENT,
                structured_output_model=QueryRefinementResponse,
                structured_output_version='v2'
            ),
            persistence=None  # Disable persistence to avoid DB issues
        )
        print(f"Agent created: {agent.name}")
        
        # Check the input schema
        input_schema = agent.input_schema
        print(f"Agent input schema: {input_schema}")
        if hasattr(input_schema, 'model_fields'):
            print(f"Input schema fields: {list(input_schema.model_fields.keys())}")
        
        # This is where it will likely fail
        print("🚀 Attempting to run agent with debug=True...")
        result = await agent.arun({"query": "what is the tallest building in france"}, debug=True)
        
    except Exception as e:
        print(f"❌ Agent test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_template_directly()
    test_augllm_config()
    asyncio.run(test_simple_agent())