#!/usr/bin/env python3
"""Test script for enhanced Supabase integration with auth.users."""

import os
import uuid
import asyncio
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add the package to the path
import sys
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-core" / "src"))

from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig


def test_enhanced_supabase_config():
    """Test the enhanced Supabase configuration with auth integration."""
    
    print("🧪 Testing Enhanced Supabase Integration")
    print("=" * 50)
    
    # Test 1: Create config with auth integration enabled
    print("1. Creating SupabaseCheckpointerConfig with auth integration...")
    
    config = SupabaseCheckpointerConfig(
        connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
        user_id="test-user-123",
        enable_auth_integration=True,
        auto_register_users=True,
        enforce_rls=True,
        setup_needed=True
    )
    
    print(f"   ✓ Config created with auth integration: {config.enable_auth_integration}")
    print(f"   ✓ User ID: {config.user_id}")
    print(f"   ✓ Auto register users: {config.auto_register_users}")
    print(f"   ✓ Enforce RLS: {config.enforce_rls}")
    
    # Test 2: Create checkpointer (this should set up tables)
    print("\n2. Creating checkpointer and setting up tables...")
    
    try:
        checkpointer = config.create_checkpointer()
        print(f"   ✓ Checkpointer created: {type(checkpointer).__name__}")
        print("   ✓ Tables should be set up (check logs above)")
        
    except Exception as e:
        print(f"   ❌ Failed to create checkpointer: {e}")
        return False
    
    # Test 3: Test user/thread registration
    print("\n3. Testing user and thread registration...")
    
    test_user_id = "00000000-0000-0000-0000-000000000000"  # Default test user
    test_thread_id = f"test-thread-{uuid.uuid4()}"
    
    try:
        thread_uuid = config.register_user_thread(
            user_id=test_user_id,
            thread_id=test_thread_id,
            agent_name="Test Agent",
            name="Test Thread",
            metadata={"test": True, "created_by": "test_script"}
        )
        print(f"   ✓ Registered thread: {test_thread_id} -> {thread_uuid}")
        
    except Exception as e:
        print(f"   ❌ Failed to register user/thread: {e}")
        return False
    
    # Test 4: Test store creation
    print("\n4. Testing store creation...")
    
    try:
        store = config.create_store()
        print(f"   ✓ Store created: {type(store).__name__}")
        
    except Exception as e:
        print(f"   ❌ Failed to create store: {e}")
        return False
    
    # Test 5: Test combined creation
    print("\n5. Testing combined checkpointer and store creation...")
    
    try:
        checkpointer, store = config.create_checkpointer_and_store()
        print(f"   ✓ Combined creation successful")
        print(f"   ✓ Checkpointer: {type(checkpointer).__name__}")
        print(f"   ✓ Store: {type(store).__name__}")
        
    except Exception as e:
        print(f"   ❌ Failed to create combined: {e}")
        return False
    
    print("\n🎉 All tests passed! Enhanced Supabase integration is working.")
    return True


async def test_async_supabase():
    """Test async Supabase functionality."""
    
    print("\n🔄 Testing Async Supabase Integration")
    print("=" * 50)
    
    config = SupabaseCheckpointerConfig(
        connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
        user_id="test-user-async",
        enable_auth_integration=True,
        setup_needed=False  # Already set up above
    )
    
    # Test async checkpointer
    print("1. Creating async checkpointer...")
    try:
        async_checkpointer = await config.create_async_checkpointer()
        print(f"   ✓ Async checkpointer created: {type(async_checkpointer).__name__}")
    except Exception as e:
        print(f"   ❌ Failed to create async checkpointer: {e}")
        return False
    
    # Test async store
    print("\n2. Creating async store...")
    try:
        async_store = await config.create_async_store()
        print(f"   ✓ Async store created: {type(async_store).__name__}")
    except Exception as e:
        print(f"   ❌ Failed to create async store: {e}")
        return False
    
    # Test combined async creation
    print("\n3. Testing combined async creation...")
    try:
        async_checkpointer, async_store = await config.create_async_checkpointer_and_store()
        print(f"   ✓ Combined async creation successful")
        print(f"   ✓ Async Checkpointer: {type(async_checkpointer).__name__}")
        print(f"   ✓ Async Store: {type(async_store).__name__}")
    except Exception as e:
        print(f"   ❌ Failed to create combined async: {e}")
        return False
    
    print("\n🎉 Async tests passed!")
    return True


def main():
    """Main test function."""
    
    print("🚀 Enhanced Supabase Integration Test Suite")
    print("=" * 60)
    
    # Check environment
    postgres_conn = os.getenv("POSTGRES_CONNECTION_STRING")
    if not postgres_conn or "[YOUR-PASSWORD]" in postgres_conn:
        print("❌ POSTGRES_CONNECTION_STRING not set or contains placeholder")
        print("Please set a valid PostgreSQL connection string for Supabase")
        return False
    
    print(f"✓ Using connection: {postgres_conn[:50]}...")
    
    # Run sync tests
    sync_success = test_enhanced_supabase_config()
    
    if sync_success:
        # Run async tests
        async_success = asyncio.run(test_async_supabase())
        
        if async_success:
            print(f"\n🎊 SUCCESS: All enhanced Supabase integration tests passed!")
            print("✓ Auth.users integration working")
            print("✓ Enhanced tables set up")
            print("✓ User/thread registration working")
            print("✓ PostgreSQL checkpointer and store working")
            print("✓ Async functionality working")
            return True
    
    print(f"\n❌ Some tests failed. Check the output above.")
    return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)