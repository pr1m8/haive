"""Enhanced SimpleRAG V3 using Enhanced MultiAgent V3.

This package provides SimpleRAG implementation using the Enhanced MultiAgent V3 pattern
with performance tracking, debug support, and adaptive routing capabilities.

Classes:
    - SimpleRAGV3: Main SimpleRAG implementation with Enhanced MultiAgent V3
    - RetrieverAgent: Specialized agent for document retrieval
    - AnswerGeneratorAgent: Specialized agent for answer generation
    - SimpleRAGState: Enhanced state schema for SimpleRAG pipeline

Examples:
    Basic usage::

        from haive.agents.rag.simple.enhanced_v3 import SimpleRAGV3

        rag = SimpleRAGV3.from_documents(
            documents=documents,
            embedding_config=embedding_config,
            performance_mode=True
        )

        result = await rag.arun("What is machine learning?")

    With performance tracking::

        rag = SimpleRAGV3(
            name="qa_system",
            vector_store_config=vs_config,
            performance_mode=True,
            debug_mode=True
        )

        result = await rag.arun("Complex query")

        # Monitor performance
        analysis = rag.analyze_agent_performance()
        print(f"Retriever success rate: {analysis['agents']['retriever']['success_rate']}")
"""

from .agent import SimpleRAGV3
from .answer_generator_agent import SimpleAnswerAgent
from .retriever_agent import RetrieverAgent
from .state import SimpleRAGState

__all__ = ["RetrieverAgent", "SimpleAnswerAgent", "SimpleRAGState", "SimpleRAGV3"]
