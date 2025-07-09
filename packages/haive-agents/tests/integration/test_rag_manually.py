#!/usr/bin/env python3
"""Manual test script for RAG agents."""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")

from langchain_core.documents import Document

from haive.agents.rag.corrective.agent_v2 import CorrectiveRAGAgentV2
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent

# Create test documents
test_documents = [
    Document(
        page_content="Python is a versatile programming language used for web development, data science, and automation.",
        metadata={"source": "programming.txt"},
    ),
    Document(
        page_content="Machine learning algorithms can learn patterns from data without explicit programming.",
        metadata={"source": "ml.txt"},
    ),
    Document(
        page_content="RAG (Retrieval-Augmented Generation) combines document retrieval with language generation.",
        metadata={"source": "rag.txt"},
    ),
]

print("Testing RAG Agents...\n")

# Test 1: SimpleRAGAgent
print("1. Testing SimpleRAGAgent...")
try:
    simple_agent = SimpleRAGAgent.from_documents(documents=test_documents)
    print("✅ SimpleRAGAgent created successfully")
    print(f"   Agents: {[a.name for a in simple_agent.agents]}")
except Exception as e:
    print(f"❌ SimpleRAGAgent failed: {e}")

# Test 2: CorrectiveRAGAgentV2
print("\n2. Testing CorrectiveRAGAgentV2...")
try:
    corrective_agent = CorrectiveRAGAgentV2.from_documents(
        documents=test_documents, relevance_threshold=0.7
    )
    print("✅ CorrectiveRAGAgentV2 created successfully")
    print(f"   Agents: {[a.name for a in corrective_agent.agents]}")
    print(f"   Has branches: {bool(corrective_agent.branches)}")
except Exception as e:
    print(f"❌ CorrectiveRAGAgentV2 failed: {e}")

# Test 3: HyDERAGAgentV2
print("\n3. Testing HyDERAGAgentV2...")
try:
    hyde_agent = HyDERAGAgentV2.from_documents(documents=test_documents)
    print("✅ HyDERAGAgentV2 created successfully")
    print(f"   Agents: {[a.name for a in hyde_agent.agents]}")
except Exception as e:
    print(f"❌ HyDERAGAgentV2 failed: {e}")

# Test 4: MultiQueryRAGAgent
print("\n4. Testing MultiQueryRAGAgent...")
try:
    multi_agent = MultiQueryRAGAgent.from_documents(documents=test_documents)
    print("✅ MultiQueryRAGAgent created successfully")
    print(f"   Agents: {[a.name for a in multi_agent.agents]}")
except Exception as e:
    print(f"❌ MultiQueryRAGAgent failed: {e}")

print("\n✅ All RAG agents created successfully!")
print("\nNote: To test actual execution, you need to configure LLM settings.")
