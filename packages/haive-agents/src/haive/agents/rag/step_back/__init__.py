"""Step-Back Prompting RAG Module

Implements step-back prompting for abstract reasoning and broader context retrieval.
Based on the pattern from rag-architectures-flows.md.
"""

from .agent import StepBackQueryGeneratorAgent, StepBackRAGAgent

__all__ = ["StepBackRAGAgent", "StepBackQueryGeneratorAgent"]
