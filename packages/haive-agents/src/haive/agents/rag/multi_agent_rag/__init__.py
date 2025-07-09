"""Multi-Agent RAG System

A comprehensive RAG implementation using the multi-agent framework with
document grading, conditional routing, advanced state management, and
built-in compatibility checking.

This module provides:
- RAG-specific state schemas with document management
- Specialized RAG agents (retrieval, grading, answer generation)
- Multi-agent RAG workflows (sequential, conditional, parallel)
- Built-in compatibility checking and automatic adaptation
- Safe RAG system creation with validation
"""

# State Management
# Core RAG Agents
from .agents import (
    SIMPLE_RAG_AGENT,
    SIMPLE_RAG_ANSWER_AGENT,
    DocumentGradingAgent,
    IterativeDocumentGradingAgent,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
    create_document_grading_agent,
    create_iterative_grading_agent,
    create_rag_answer_agent,
    create_simple_rag_agent,
)

# Multi-Agent RAG Workflows
from .multi_rag import (
    AdaptiveRAGMultiAgent,
    BaseRAGMultiAgent,
    ConditionalRAGMultiAgent,
    IterativeRAGMultiAgent,
    ParallelRAGMultiAgent,
    agent_list,
    base_rag_agent,
    create_conditional_rag_system,
    create_iterative_rag_system,
    create_sequential_rag_system,
    test_agent_compatibility,
    validate_multi_agent_compatibility,
)
from .state import (
    DocumentGradingResult,
    EnhancedRAGState,
    MultiAgentRAGState,
    QueryStatus,
    RAGOperationType,
    RAGState,
    RAGStep,
)

# Compatibility Testing - temporarily disabled due to import issues
# from .compatibility import (
#     AgentCompatibilityReport,
#     CompatibilityLevel,
#     MultiAgentCompatibilityReport,
#     SafeCompatibilityTester,
#     quick_agent_compatibility_check,
#     safe_test_rag_compatibility,
#     test_custom_agent_workflow,
# )

# Enhanced Multi-Agent with Built-in Compatibility - temporarily disabled
# from .enhanced_multi_rag import (
#     EnhancedRAGConditionalAgent,
#     EnhancedRAGParallelAgent,
#     EnhancedRAGSequentialAgent,
#     SmartRAGFactory,
#     demonstrate_enhanced_rag_compatibility,
#     enhanced_agent_list,
#     enhanced_base_rag_agent,
#     enhanced_simple_rag_agent,
#     enhanced_simple_rag_answer_agent,
# )


__all__ = [
    # State Management
    "MultiAgentRAGState",
    "RAGState",
    "EnhancedRAGState",
    "RAGOperationType",
    "QueryStatus",
    "DocumentGradingResult",
    "RAGStep",
    # Core RAG Agents
    "SimpleRAGAgent",
    "SimpleRAGAnswerAgent",
    "DocumentGradingAgent",
    "IterativeDocumentGradingAgent",
    "SIMPLE_RAG_AGENT",
    "SIMPLE_RAG_ANSWER_AGENT",
    "create_simple_rag_agent",
    "create_rag_answer_agent",
    "create_document_grading_agent",
    "create_iterative_grading_agent",
    # Multi-Agent RAG Workflows
    "BaseRAGMultiAgent",
    "ConditionalRAGMultiAgent",
    "IterativeRAGMultiAgent",
    "ParallelRAGMultiAgent",
    "AdaptiveRAGMultiAgent",
    "base_rag_agent",
    "agent_list",
    "create_sequential_rag_system",
    "create_conditional_rag_system",
    "create_iterative_rag_system",
    "test_agent_compatibility",
    "validate_multi_agent_compatibility",
    # Compatibility Testing
    "SafeCompatibilityTester",
    "CompatibilityLevel",
    "AgentCompatibilityReport",
    "MultiAgentCompatibilityReport",
    "safe_test_rag_compatibility",
    "test_custom_agent_workflow",
    "quick_agent_compatibility_check",
    # Enhanced Multi-Agent with Built-in Compatibility
    "EnhancedRAGSequentialAgent",
    "EnhancedRAGConditionalAgent",
    "EnhancedRAGParallelAgent",
    "SmartRAGFactory",
    "enhanced_simple_rag_agent",
    "enhanced_simple_rag_answer_agent",
    "enhanced_base_rag_agent",
    "enhanced_agent_list",
    "demonstrate_enhanced_rag_compatibility",
]
