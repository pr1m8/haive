"""Multi-Agent RAG System.

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


__all__ = [
    "SIMPLE_RAG_AGENT",
    "SIMPLE_RAG_ANSWER_AGENT",
    "AdaptiveRAGMultiAgent",
    "AgentCompatibilityReport",
    # Multi-Agent RAG Workflows
    "BaseRAGMultiAgent",
    "CompatibilityLevel",
    "ConditionalRAGMultiAgent",
    "DocumentGradingAgent",
    "DocumentGradingResult",
    "EnhancedRAGConditionalAgent",
    "EnhancedRAGParallelAgent",
    # Enhanced Multi-Agent with Built-in Compatibility
    "EnhancedRAGSequentialAgent",
    "EnhancedRAGState",
    "IterativeDocumentGradingAgent",
    "IterativeRAGMultiAgent",
    "MultiAgentCompatibilityReport",
    # State Management
    "MultiAgentRAGState",
    "ParallelRAGMultiAgent",
    "QueryStatus",
    "RAGOperationType",
    "RAGState",
    "RAGStep",
    # Compatibility Testing
    "SafeCompatibilityTester",
    # Core RAG Agents
    "SimpleRAGAgent",
    "SimpleRAGAnswerAgent",
    "SmartRAGFactory",
    "agent_list",
    "base_rag_agent",
    "create_conditional_rag_system",
    "create_document_grading_agent",
    "create_iterative_grading_agent",
    "create_iterative_rag_system",
    "create_rag_answer_agent",
    "create_sequential_rag_system",
    "create_simple_rag_agent",
    "demonstrate_enhanced_rag_compatibility",
    "enhanced_agent_list",
    "enhanced_base_rag_agent",
    "enhanced_simple_rag_agent",
    "enhanced_simple_rag_answer_agent",
    "quick_agent_compatibility_check",
    "safe_test_rag_compatibility",
    "test_agent_compatibility",
    "test_custom_agent_workflow",
    "validate_multi_agent_compatibility",
]
