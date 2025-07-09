"""Agentic RAG Router

Intelligent RAG routing with ReAct patterns for dynamic agent selection and coordination.
Provides autonomous decision-making for optimal RAG strategy selection.
"""

from .agent import (
    AgenticRAGRouterAgent,
    create_agentic_rag_router_agent,
    get_agentic_rag_router_io_schema,
)

__all__ = [
    "AgenticRAGRouterAgent",
    "create_agentic_rag_router_agent",
    "get_agentic_rag_router_io_schema",
]
