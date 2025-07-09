"""Corrective RAG Module

Self-correcting retrieval with quality assessment.
"""

try:
    from .agent import CorrectiveRAGAgent
except ImportError:
    CorrectiveRAGAgent = None

from .agent_v2 import CorrectiveRAGAgentV2

__all__ = ["CorrectiveRAGAgent", "CorrectiveRAGAgentV2"]
