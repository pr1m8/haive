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

print(f"Attempting to connect to PostgreSQL at {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"Using credentials: {DB_USER}/{'*' * len(DB_PASS)}")

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
    print("Creating connection pool...")
    checkpointer = postgres_config.create_checkpointer()

    # Test if we can actually execute a query (the ultimate test)
    print("Testing database connection with a simple query...")
    with PostgresCheckpointerConfig.pool.connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS connection_test")
            result = cursor.fetchone()
            print(f"Query result: {result}")

    print("✅ Successfully connected to the database!")

    # Test registering a thread
    thread_id = "test-thread-connection"
    print(f"Registering thread: {thread_id}")
    postgres_config.register_thread(thread_id)
    print(f"✅ Successfully registered thread: {thread_id}")

    # Test writing and reading data
    print("Testing data write/read...")
    config = {"configurable": {"thread_id": thread_id}}
    test_data = {"test_key": f"test_value_{thread_id}"}

    print(f"Writing data: {test_data}")
    updated_config = postgres_config.put_checkpoint(config, test_data)

    print("Reading data back...")
    retrieved_data = postgres_config.get_checkpoint(updated_config)

    print(f"Retrieved data: {retrieved_data}")
    if retrieved_data and retrieved_data.get("test_key") == test_data["test_key"]:
        print("✅ Data write/read test successful!")
    else:
        print("❌ Data write/read test failed!")

except Exception as e:
    print(f"❌ Failed to connect to the database: {e}")
    import traceback

    traceback.print_exc()

finally:
    # Always close the connection
    print("Closing connection...")
    if PostgresCheckpointerConfig.pool is not None:
        PostgresCheckpointerConfig.pool.close()
        PostgresCheckpointerConfig.pool = None
        print("Connection closed.")
