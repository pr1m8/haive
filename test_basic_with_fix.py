#!/usr/bin/env python3
"""
Test the actual test_basic.py scenario but using the fixed engine node.
"""

import sys
import os
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

# Monkey patch to use the test engine node
import haive.core.graph.node.engine_node as engine_node_module
from haive.core.graph.node.engine_node_test import EngineNodeConfig as TestEngineNodeConfig

# Replace the original with the test version
engine_node_module.EngineNodeConfig = TestEngineNodeConfig

print("🔧 Monkey-patched engine_node to use test version")
print("🚀 Running test_basic.py scenario...")

# Now run the same code from test_basic.py
from typing import Literal, Optional, List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert query optimization specialist for RAG systems..."""),
    ("human", """Analyze and refine the following user query.

**Original Query:** {query}

**Context (if provided):** {context}

Focus on improvements that will lead to better document retrieval.""")
]).partial(context="")

class QueryRefinementSuggestion(BaseModel):
    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(description="Type of improvement made")
    rationale: str = Field(description="Why this refinement improves the query")

class QueryRefinementResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(description="Analysis of the original query")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(description="List of suggested improvements")
    best_refined_query: str = Field(description="The recommended best refined query")

from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig

def agent_tester(prompt, model, test_prompt):
    print(f"📝 Creating agent with prompt template and structured output...")
    agent = SimpleAgentV2(
        engine=AugLLMConfig(
            prompt_template=prompt,
            structured_output_model=model,
            structured_output_version='v2'
        )
    )
    print(f"✅ Agent created successfully")
    
    print(f"🏃 Running agent with test input: {test_prompt}")
    try:
        result = agent.run(test_prompt, debug=True)
        print(f"✅ SUCCESS: Agent run completed!")
        print(f"📤 Result type: {type(result)}")
        return result
    except Exception as e:
        print(f"❌ FAILED: {e}")
        raise

# Run the test
try:
    result = agent_tester(
        RAG_QUERY_REFINEMENT, 
        QueryRefinementResponse, 
        {"query": "what is the tallest building in france"}
    )
    print("🎉 END-TO-END TEST PASSED!")
except Exception as e:
    print(f"💥 END-TO-END TEST FAILED: {e}")
    import traceback
    traceback.print_exc()