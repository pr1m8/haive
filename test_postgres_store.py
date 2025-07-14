#!/usr/bin/env python3
"""Test script for PostgreSQL store implementation."""

import asyncio
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_sync_postgres_store():
    """Test synchronous PostgreSQL store."""
    try:
        from haive.core.persistence.store.factory import create_store
        from haive.core.persistence.store.types import StoreType
        
        # Get connection string from environment or use default
        connection_string = os.getenv(
            "POSTGRES_CONNECTION_STRING", 
            "postgresql://postgres:postgres@localhost:5432/postgres"
        )
        
        logger.info("Creating synchronous PostgreSQL store...")
        store = create_store(
            store_type=StoreType.POSTGRES_SYNC,
            connection_string=connection_string
        )
        
        logger.info(f"Created store: {type(store).__name__}")
        
        # Test basic operations
        namespace = ("test", "namespace")
        key = "test_key"
        value = {"message": "Hello from PostgreSQL store!", "count": 42}
        
        logger.info("Testing put operation...")
        store.put(namespace, key, value)
        
        logger.info("Testing get operation...")
        retrieved = store.get(namespace, key)
        logger.info(f"Retrieved value: {retrieved}")
        
        # Extract value from Item object if needed
        if hasattr(retrieved, 'value'):
            retrieved_value = retrieved.value
        else:
            retrieved_value = retrieved
            
        assert retrieved_value == value, f"Retrieved value doesn't match: {retrieved_value} != {value}"
        
        logger.info("Testing delete operation...")
        store.delete(namespace, key)
        
        logger.info("Verifying deletion...")
        deleted_value = store.get(namespace, key)
        assert deleted_value is None, f"Value not deleted: {deleted_value}"
        
        logger.info("✅ Synchronous PostgreSQL store test passed!")
        
    except Exception as e:
        logger.error(f"❌ Synchronous PostgreSQL store test failed: {e}")
        raise


async def test_async_postgres_store():
    """Test asynchronous PostgreSQL store."""
    try:
        from haive.core.persistence.store.factory import create_store
        from haive.core.persistence.store.types import StoreType
        
        # Get connection string from environment or use default
        connection_string = os.getenv(
            "POSTGRES_CONNECTION_STRING", 
            "postgresql://postgres:postgres@localhost:5432/postgres"
        )
        
        logger.info("Creating asynchronous PostgreSQL store...")
        store = create_store(
            store_type=StoreType.POSTGRES_ASYNC,
            connection_string=connection_string
        )
        
        logger.info(f"Created store: {type(store).__name__}")
        
        # Test basic operations
        namespace = ("test", "async", "namespace")
        key = "test_async_key"
        value = {"message": "Hello from async PostgreSQL store!", "async": True}
        
        logger.info("Testing async put operation...")
        await store.aput(namespace, key, value)
        
        logger.info("Testing async get operation...")
        retrieved = await store.aget(namespace, key)
        logger.info(f"Retrieved value: {retrieved}")
        
        # Extract value from Item object if needed
        if hasattr(retrieved, 'value'):
            retrieved_value = retrieved.value
        else:
            retrieved_value = retrieved
            
        assert retrieved_value == value, f"Retrieved value doesn't match: {retrieved_value} != {value}"
        
        logger.info("Testing async delete operation...")
        await store.adelete(namespace, key)
        
        logger.info("Verifying deletion...")
        deleted_value = await store.aget(namespace, key)
        assert deleted_value is None, f"Value not deleted: {deleted_value}"
        
        logger.info("✅ Asynchronous PostgreSQL store test passed!")
        
    except Exception as e:
        logger.error(f"❌ Asynchronous PostgreSQL store test failed: {e}")
        raise


def test_memory_store_fallback():
    """Test that memory store fallback works when PostgreSQL is not available."""
    try:
        from haive.core.persistence.store.factory import create_store
        from haive.core.persistence.store.types import StoreType
        
        # Use an invalid connection string to trigger fallback
        logger.info("Testing memory store fallback...")
        store = create_store(
            store_type=StoreType.POSTGRES_SYNC,
            connection_string="postgresql://invalid:invalid@nonexistent:5432/invalid"
        )
        
        logger.info(f"Created store: {type(store).__name__}")
        
        # Should have fallen back to memory store
        assert "Memory" in type(store).__name__, f"Expected memory store, got {type(store).__name__}"
        
        logger.info("✅ Memory store fallback test passed!")
        
    except Exception as e:
        logger.error(f"❌ Memory store fallback test failed: {e}")
        raise


async def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("PostgreSQL Store Implementation Tests")
    logger.info("=" * 60)
    
    # Test synchronous store
    logger.info("\n1. Testing synchronous PostgreSQL store...")
    test_sync_postgres_store()
    
    # Test asynchronous store
    logger.info("\n2. Testing asynchronous PostgreSQL store...")
    await test_async_postgres_store()
    
    # Test memory fallback
    logger.info("\n3. Testing memory store fallback...")
    test_memory_store_fallback()
    
    logger.info("\n" + "=" * 60)
    logger.info("All tests completed successfully! 🎉")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())