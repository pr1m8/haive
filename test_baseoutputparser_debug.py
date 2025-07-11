"""Debug BaseOutputParser and PydanticUndefined issues."""

import logging
from pydantic import BaseModel, Field
from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.agents.simple.agent_v2 import SimpleAgentV2
from langchain_core.prompts import ChatPromptTemplate

# Set up logging to see details
logging.basicConfig(level=logging.DEBUG)

class SimpleResponse(BaseModel):
    """Simple response model."""
    answer: str = Field(description="The answer")

# Create a simple prompt
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{query}")
])

def test_basic_case():
    """Test the most basic case."""
    print("=== Testing Basic Case ===")
    
    try:
        # Create AugLLMConfig
        engine = AugLLMConfig(
            prompt_template=simple_prompt,
            structured_output_model=SimpleResponse,
            structured_output_version='v2'
        )
        
        print(f"Engine created successfully: {engine}")
        print(f"Engine fields: {list(engine.model_fields.keys())}")
        
        # Check for PydanticUndefined
        from pydantic_core import PydanticUndefined
        for field_name, field_info in engine.model_fields.items():
            if hasattr(field_info, 'default') and field_info.default is PydanticUndefined:
                print(f"❌ FOUND PydanticUndefined in engine field: {field_name}")
            elif hasattr(field_info, 'default'):
                print(f"✅ Field {field_name} has default: {field_info.default}")
        
        # Create agent
        agent = SimpleAgentV2(engine=engine)
        print(f"Agent created successfully: {agent}")
        
        # Try to get state schema
        state_schema = agent.state_schema
        print(f"State schema: {state_schema}")
        
        # Check state schema for PydanticUndefined
        if state_schema and hasattr(state_schema, 'model_fields'):
            for field_name, field_info in state_schema.model_fields.items():
                if hasattr(field_info, 'default') and field_info.default is PydanticUndefined:
                    print(f"❌ FOUND PydanticUndefined in state schema field: {field_name}")
                elif hasattr(field_info, 'default'):
                    print(f"✅ State field {field_name} has default: {field_info.default}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_run_attempt():
    """Test actually running the agent."""
    print("\n=== Testing Agent Run ===")
    
    try:
        engine = AugLLMConfig(
            prompt_template=simple_prompt,
            structured_output_model=SimpleResponse,
            structured_output_version='v2'
        )
        
        agent = SimpleAgentV2(engine=engine)
        
        # Try to run
        result = agent.run("What is 2+2?", debug=True)
        print(f"✅ Agent run successful: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error in run test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting BaseOutputParser and PydanticUndefined debug...")
    
    basic_ok = test_basic_case()
    if basic_ok:
        test_run_attempt()
    else:
        print("❌ Basic test failed, skipping run test") 