#!/usr/bin/env python3
"""Check async support for PostgreSQL persistence."""

import asyncio
import os
import sys

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")


async def test_async_persistence():
    """Test async PostgreSQL persistence."""
    print("🔍 Testing Async PostgreSQL Support...")

    try:
        from haive.core.persistence.factory import acreate_postgres_checkpointer
        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
        from haive.core.persistence.store.connection import ConnectionManager

        # Check if async pool creation works
        print("\n1️⃣ Testing async pool creation...")

        conn_params = {
            "host": os.environ.get("PGHOST", "localhost"),
            "port": os.environ.get("PGPORT", 5432),
            "database": os.environ.get("PGDATABASE", "postgres"),
            "user": os.environ.get("PGUSER", "postgres"),
            "password": os.environ.get("PGPASSWORD", ""),
        }

        pool = await ConnectionManager.get_or_create_async_pool(
            connection_id="test_async",
            connection_params=conn_params,
            pool_config={"min_size": 1, "max_size": 2},
        )

        print(f"✅ Created async pool: {type(pool).__name__}")

        # Test async checkpointer
        print("\n2️⃣ Testing async checkpointer creation...")

        config = PostgresCheckpointerConfig(
            mode="async",
            prepare_threshold=None,
            connection_kwargs={
                "prepare_threshold": None,
                "application_name": "test_async_checkpointer",
            },
        )

        checkpointer = await acreate_postgres_checkpointer(config)
        print(f"✅ Created async checkpointer: {type(checkpointer).__name__}")

        # Check methods
        print("\n3️⃣ Checking async methods...")
        has_aput = hasattr(checkpointer, "aput")
        has_aget = hasattr(checkpointer, "aget")
        has_alist = hasattr(checkpointer, "alist")

        print(f"   aput method: {'✅' if has_aput else '❌'}")
        print(f"   aget method: {'✅' if has_aget else '❌'}")
        print(f"   alist method: {'✅' if has_alist else '❌'}")

        # Check ConnectionManager async support
        print("\n4️⃣ Checking ConnectionManager prepare_threshold...")

        # Read the connection.py file to verify
        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py",
            "r",
        ) as f:
            content = f.read()

        sync_count = content.count('"prepare_threshold": 0')
        none_count = content.count('"prepare_threshold": None')

        print(f"   prepare_threshold: 0 occurrences: {sync_count}")
        print(f"   prepare_threshold: None occurrences: {none_count}")

        if none_count > 0:
            print("   ✅ ConnectionManager updated to use prepare_threshold: None")
        else:
            print("   ❌ ConnectionManager still using prepare_threshold: 0")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


def check_langgraph_modifications():
    """Check if LangGraph files were modified."""
    print("\n🔍 Checking LangGraph modifications...")

    langgraph_files = [
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/__init__.py",
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/base.py",
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/_internal.py",
    ]

    for file_path in langgraph_files:
        if os.path.exists(file_path):
            print(f"\n📄 {os.path.basename(file_path)}:")

            # Check for prepare_threshold
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                if "prepare_threshold" in content:
                    # Find the line
                    for i, line in enumerate(content.split("\n")):
                        if "prepare_threshold" in line:
                            print(f"   Line {i+1}: {line.strip()}")

                            if "prepare_threshold=0" in line:
                                print("   ❌ Still using prepare_threshold=0")
                            elif "prepare_threshold=None" in line:
                                print("   ✅ Updated to prepare_threshold=None")
                else:
                    print("   ℹ️  No prepare_threshold found")

            except Exception as e:
                print(f"   ⚠️  Could not read: {e}")
        else:
            print(f"\n❌ File not found: {file_path}")


def main():
    """Run async support checks."""
    print("🧪 Async PostgreSQL Support Check")
    print("=" * 60)

    # Check async support
    asyncio.run(test_async_persistence())

    # Check LangGraph modifications
    check_langgraph_modifications()

    print("\n" + "=" * 60)
    print("✅ Check complete!")


if __name__ == "__main__":
    main()
