# test_postgres_async.py

import asyncio
import logging
import os
import sys
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

from haive.core.engine.aug_llm import AugLLMConfig

# Import your AugLLMEngine and other necessary components
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig


async def test_postgres_with_augllm():
    """Test PostgreSQL connection using AugLLM engine."""

    # Get database connection details
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", "5432"))
    DB_NAME = os.environ.get("DB_NAME", "postgres")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

    print(f"Testing PostgreSQL connection with AugLLM at {DB_HOST}:{DB_PORT}/{DB_NAME}")

    try:
        # Create PostgreSQL config
        postgres_config = PostgresCheckpointerConfig(
            db_host=DB_HOST,
            db_port=DB_PORT,
            db_name=DB_NAME,
            db_user=DB_USER,
            db_pass=DB_PASSWORD,
            ssl_mode="disable",
            use_async=True,  # Use async mode
        )

        # Create checkpointer to test connection
        await postgres_config.acreate_checkpointer()
        print("✅ Successfully created async PostgreSQL checkpointer")

        # Create thread ID
        thread_id = f"augllm-test-{uuid.uuid4()}"

        # Create a simple AugLLMConfig (minimal example)
        azure_config = AzureLLMConfig(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY", "demo-key"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15"),
            api_base=os.environ.get(
                "AZURE_OPENAI_API_BASE", "https://example.azure.openai.com/"
            ),
            model="gpt-4o",
        )

        llm_config = AugLLMConfig(
            name="test-llm",
            llm_config=azure_config,
            # Add any additional parameters your AugLLMConfig requires
        )

        # Create a conversation config
        config = {
            "configurable": {
                "thread_id": thread_id,
                "engine_configs": {"test-llm": {"temperature": 0.7, "max_tokens": 500}},
            }
        }

        # Register thread
        print(f"Registering thread {thread_id}")
        await postgres_config.aregister_thread(
            thread_id,
            metadata={
                "engine": "AugLLM",
                "timestamp": datetime.now().isoformat(),
                "config": str(llm_config),
            },
        )
        print("✅ Thread registered")

        # Create test data
        test_data = {
            "timestamp": datetime.now().isoformat(),
            "engine_id": llm_config.name,
            "messages": [{"role": "user", "content": "Hello from PostgreSQL test"}],
        }

        # Store data
        print("Writing test data to PostgreSQL")
        updated_config = await postgres_config.aput_checkpoint(
            config=config, data=test_data
        )

        checkpoint_id = updated_config["configurable"].get("checkpoint_id")
        print(f"✅ Created checkpoint with ID: {checkpoint_id}")

        # Retrieve data
        print("Reading data back")
        retrieved = await postgres_config.aget_checkpoint(updated_config)

        # Verify data
        if retrieved and "messages" in retrieved:
            print(
                f"✅ Successfully retrieved data with {len(retrieved['messages'])} messages"
            )
            for msg in retrieved["messages"]:
                print(f"  - {msg.get('role')}: {msg.get('content')}")
        else:
            print("❌ Failed to retrieve data")

        # Close connection
        print("Closing connection")
        await postgres_config.aclose()
        print("✅ Connection closed")

        return True

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🔄 Testing PostgreSQL integration with AugLLM...")
    success = asyncio.run(test_postgres_with_augllm())
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed!")
        sys.exit(1)
