"""Answer_Generator package.

This package provides answer generator functionality for the Haive framework.

Modules:
    models: Models implementation.
    prompts: Prompts implementation.
"""

#!/usr/bin/env python3
"""Answer generator components for SimpleRAG."""

from .models import RAGAnswer
from .prompts import RAG_CHAT_TEMPLATE

__all__ = ["RAG_CHAT_TEMPLATE", "RAGAnswer"]
