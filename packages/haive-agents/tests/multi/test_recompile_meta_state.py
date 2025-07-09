"""Test extending MetaStateSchema with recompilation support"""

from typing import Dict, Any, List, Set, Optional
from pydantic import Field, model_validator
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

class RecompileMetaState(MetaStateSchema):
    """Meta state with recompilation support (extending existing MetaStateSchema)"""
    
    # Add recompilation tracking fields
    needs_recompile: bool = Field(default=False, description="Whether agent needs recompilation")
    recompile_reason: Optional[str] = Field(default=None, description="Reason for recompilation")
    recompile_count: int = Field(default=0, description="Number of recompilations")
    
    # Don't override model_validator - let parent handle it
    # Add recompile logic in a separate method if needed

def test_recompile_meta_state():
    """Test that RecompileMetaState works with any agent"""
    
    try:
        # Create any agent
        config = AugLLMConfig()
        agent = SimpleAgent(engine=config)
        
        # Create meta state with the agent
        meta_state = RecompileMetaState(agent=agent)
        
        print(f"✓ RecompileMetaState created successfully")
        print(f"✓ Agent: {meta_state.agent_name}")
        print(f"✓ Agent type: {meta_state.agent_type}")
        print(f"✓ Needs recompile: {meta_state.needs_recompile}")
        print(f"✓ Recompile fields added: needs_recompile={meta_state.needs_recompile}, recompile_count={meta_state.recompile_count}")
        
        return meta_state
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    meta_state = test_recompile_meta_state()
    print("✓ RecompileMetaState created successfully")