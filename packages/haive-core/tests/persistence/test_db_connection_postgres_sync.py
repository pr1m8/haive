import logging
import sys

from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

# Set up logging to see detailed connection information
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

# Database connection parameters (use environment variables or hardcode for testing)
DB_HOST = "localhost"  # e.g., "localhost" or "192.168.1.100"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_SSL_MODE = "disable"  # or "require" for secure connections


# Create config
postgres_config = PostgresCheckpointerConfig(
    db_host=DB_HOST,
    db_port=DB_PORT,
    db_name=DB_NAME,
    db_user=DB_USER,
    db_pass=DB_PASS,
    ssl_mode=DB_SSL_MODE,
    setup_needed=True,
)

# Try to create a checkpointer (this will test the connection)
try:
    checkpointer = postgres_config.create_checkpointer()

    # Test if we can actually execute a query (the ultimate test)
    with PostgresCheckpointerConfig.pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1 AS connection_test")
        result = cursor.fetchone()
        print(f"Query result: {result}")


    # Test registering a thread
    thread_id = "test-thread-connection"
    postgres_config.register_thread(thread_id)

    # Test writing and reading data
    config = {"configurable": {"thread_id": thread_id}}
    test_data = {"test_key": f"test_value_{thread_id}"}

    updated_config = postgres_config.put_checkpoint(config, test_data)

    retrieved_data = postgres_config.get_checkpoint(updated_config)

    if retrieved_data and retrieved_data.get("test_key") == test_data["test_key"]:
        pass")
    else:
        pass")

except Exception as e:
    import traceback

    traceback.print_exc()

finally:
    # Always close the connection
    if PostgresCheckpointerConfig.pool is not None:
        PostgresCheckpointerConfig.pool.close()
        PostgresCheckpointerConfig.pool = None
