#!/usr/bin/env python3
"""Simple test to check memory agent functionality quickly."""

from __future__ import annotations

import asyncio

from haive.agents.memory.core.classifier import MemoryClassifier, MemoryClassifierConfig
from haive.core.engine.aug_llm import AugLLMConfig


async def test_memory_classifier_basic():
    """Test basic memory classifier functionality."""
    print('Testing Memory Classifier...')

    config = MemoryClassifierConfig(
        llm_config=AugLLMConfig(temperature=0.1),
        confidence_threshold=0.6,
    )
    classifier = MemoryClassifier(config)

    # Test classification
    result = classifier.classify_memory(
        'I learned Python programming yesterday')
    print(f"Memory types: {result.memory_types}")
    print(f"Importance: {result.importance}")
    print(f"Confidence: {result.confidence}")

    # Test query intent
    intent = classifier.classify_query_intent(
        'What programming languages do I know?')
    print(f"Query intent strategy: {intent.preferred_retrieval_strategy}")
    print(f"Query memory types: {intent.memory_types}")

    print('✅ Memory Classifier test passed!')


async def test_store_manager():
    """Test store manager functionality."""
    print('\nTesting Store Manager...')

    from haive.core.persistence.store.types import StoreType
    from haive.core.tools.store_manager import StoreManager

    # Create store manager
    store_manager = StoreManager(
        store_config={'type': StoreType.MEMORY},
        default_namespace=('test', 'simple'),
    )

    # Store a memory
    memory_id = store_manager.store_memory(
        content='Test memory content',
        category='test',
        importance=0.8,
    )
    print(f"Stored memory ID: {memory_id}")

    # Retrieve the memory
    memory = store_manager.retrieve_memory(memory_id)
    print(f"Retrieved memory: {memory.content}")

    # Search memories
    results = store_manager.search_memories('test', limit=5)
    print(f"Search results: {len(results)} memories found")

    print('✅ Store Manager test passed!')


async def main():
    """Run all tests."""
    print('🧪 Running Simple Memory Tests...')

    await test_memory_classifier_basic()
    await test_store_manager()

    print('\n🎉 All tests passed!')


if __name__ == '__main__':
    asyncio.run(main())
