#!/usr/bin/env python3
"""Check async support for PostgreSQL persistence."""

import asyncio
import os
import sys

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")


async def test_async_persistence():
    """Test async PostgreSQL persistence."""

    try:
        from haive.core.persistence.factory import acreate_postgres_checkpointer
        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
        from haive.core.persistence.store.connection import ConnectionManager

        # Check if async pool creation works

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


        # Test async checkpointer

        config = PostgresCheckpointerConfig(
            mode="async",
            prepare_threshold=None,
            connection_kwargs={
                "prepare_threshold": None,
                "application_name": "test_async_checkpointer",
            },
        )

        checkpointer = await acreate_postgres_checkpointer(config)

        # Check methods
        has_aput = hasattr(checkpointer, "aput")
        has_aget = hasattr(checkpointer, "aget")
        has_alist = hasattr(checkpointer, "alist")


        # Check ConnectionManager async support

        # Read the connection.py file to verify
        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py",
        ) as f:
            content = f.read()

        sync_count = content.count('"prepare_threshold": 0')
        none_count = content.count('"prepare_threshold": None')


        if none_count > 0:
            pass")
        else:
            pass")

    except Exception as e:
        import traceback

        traceback.print_exc()


def check_langgraph_modifications():
    """Check if LangGraph files were modified."""

    langgraph_files = [
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/__init__.py",
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/base.py",
        "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/checkpoint/postgres/_internal.py",
    ]

    for file_path in langgraph_files:
        if os.path.exists(file_path):

            # Check for prepare_threshold
            try:
                with open(file_path) as f:
                    content = f.read()

                if "prepare_threshold" in content:
                    # Find the line
                    for i, line in enumerate(content.split("\n")):
                        if "prepare_threshold" in line:

                            if "prepare_threshold=0" in line:
                                pass")
                            elif "prepare_threshold=None" in line:
                                pass")
                else:
                    passnd")

            except Exception as e:
                passe}")
        else:
            pass")


def main():
    """Run async support checks."""

    # Check async support
    asyncio.run(test_async_persistence())

    # Check LangGraph modifications
    check_langgraph_modifications()



if __name__ == "__main__":
    main()
