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


# Test 1: SimpleRAGAgent
try:
    simple_agent = SimpleRAGAgent.from_documents(documents=test_documents)
except Exception as e:
    pass")

# Test 2: CorrectiveRAGAgentV2
try:
    corrective_agent = CorrectiveRAGAgentV2.from_documents(
        documents=test_documents, relevance_threshold=0.7
    )
except Exception as e:
    pass")

# Test 3: HyDERAGAgentV2
try:
    hyde_agent = HyDERAGAgentV2.from_documents(documents=test_documents)
except Exception as e:
    pass")

# Test 4: MultiQueryRAGAgent
try:
    multi_agent = MultiQueryRAGAgent.from_documents(documents=test_documents)
except Exception as e:
    pass")

