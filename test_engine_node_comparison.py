#!/usr/bin/env python3
"""
Test script to compare original vs test engine node behavior.

This shows the difference between:
1. Original: Only extracts 'messages' field for LLM engines  
2. Test: Uses engine's derived input fields (messages, query, context)
"""

import sys
import os
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-core/src')
sys.path.insert(0, '/home/will/Projects/haive/backend/haive/packages/haive-agents/src')

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig as OriginalEngineNode
from haive.core.graph.node.engine_node_test import EngineNodeConfig as TestEngineNode
from langchain_core.prompts import ChatPromptTemplate

# Create the same prompt from test_basic.py
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert. Analyze query: {query} with context: {context}"),
    ("human", "Process: {query}")
])

# Create AugLLMConfig with this prompt
engine = AugLLMConfig(
    name="test_engine",
    prompt_template=RAG_QUERY_REFINEMENT
)

print("🔍 COMPARISON: Original vs Test Engine Node")
print("=" * 60)

print(f"Engine derived input fields: {list(engine.get_input_fields().keys())}")
print()

# Test original engine node
print("📊 ORIGINAL ENGINE NODE (messages only):")
original_node = OriginalEngineNode(name="original", engine=engine)
print(f"  Input field defs: {[f.name for f in original_node.input_field_defs]}")
print()

# Test new engine node
print("📊 TEST ENGINE NODE (engine-derived fields):")
test_node = TestEngineNode(name="test", engine=engine)
print(f"  Input field defs: {[f.name for f in test_node.input_field_defs]}")
print()

print("🎯 EXPECTED BEHAVIOR:")
print("  Original: Only 'messages' -> missing 'query' -> KeyError")
print("  Test: 'messages', 'query', 'context' -> should work!")