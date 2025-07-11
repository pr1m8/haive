"""Updated test for PostgreSQL persistence with correct StateSnapshot handling.

Save as tests/agents/base/checkpointer/test_postgres_persistent_agent.py
"""

import logging
import sys
import time
import uuid
from typing import Any

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def print_step(message):
    """Print a clearly visible step header."""
    sys.stdout.flush()


# Add project root to path if needed


# Check for PostgreSQL dependencies
try:
    import psycopg
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg_pool import ConnectionPool

    POSTGRES_AVAILABLE = True
except ImportError as e:
    POSTGRES_AVAILABLE = False


from haive.agents.simple.factory import create_simple_agent

# Database connection parameters
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
CONNECTION_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}


def extract_messages_from_state(state: Any) -> list[Any]:
    """Extract messages from a state object, regardless of its type.
    Handles various state object formats.

    Args:
        state: The state object returned by agent.run()

    Returns:
        A list of messages, or an empty list if none found
    """
    if state is None:
        return []

    # Case 1: If it's a dictionary with messages
    if isinstance(state, dict) and "messages" in state:
        return state["messages"]

    # Case 2: If it has a channel_values attribute (StateSnapshot)
    if hasattr(state, "channel_values"):
        channel_values = state.channel_values
        if channel_values and "messages" in channel_values:
            return channel_values["messages"]

    # Case 3: If it has specific StateSnapshot attributes
    if hasattr(state, "values"):
        values = state.values
        if isinstance(values, dict) and "messages" in values:
            return values["messages"]

    # Case 4: Direct attribute check
    if hasattr(state, "messages"):
        return state.messages

    # Nothing found
    return []


def extract_message_content(message: Any) -> str:
    """Extract content from a message object, regardless of its type.

    Args:
        message: A message object

    Returns:
        The content as a string
    """
    if message is None:
        return ""

    # Case 1: Message has content attribute (LangChain messages)
    if hasattr(message, "content"):
        return str(message.content)

    # Case 2: Message is a tuple (type, content)
    if isinstance(message, tuple) and len(message) >= 2:
        return str(message[1])

    # Case 3: Message is a dictionary with content
    if isinstance(message, dict) and "content" in message:
        return str(message["content"])

    # Default: Convert to string
    return str(message)


def test_postgres_connection():
    """Test direct PostgreSQL connection."""
    print_step("Testing direct PostgreSQL connection")

    try:
        with psycopg.connect(DB_URI) as conn, conn.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")")
        assert True, "PostgreSQL connection successful"
    except Exception as e:
        raise AssertionError(f"PostgreSQL connection failed: {e}")


def test_memory_persistence():
    """Test SimpleAgent with MemorySaver persistence."""
    print_step("Testing SimpleAgent with MemorySaver")

    try:
        # Create a unique test name and thread ID
        test_name = f"memory_test_{uuid.uuid4().hex[:8]}"
        thread_id = f"memory_thread_{uuid.uuid4().hex[:8]}"

        # Create a simple agent
        agent = create_simple_agent(
            system_prompt="You are a test assistant with memory. Remember what the user tells you.",
            name=test_name,
        )

        # Replace the agent's checkpointer with an explicit MemorySaver
        memory_saver = MemorySaver()
        agent.checkpointer = memory_saver

        # Recompile the app with the new checkpointer
        agent.app = agent.graph.compile(checkpointer=memory_saver)

        # First message to establish fact - using LangGraph format
        # Use LangGraph format directly
        response1 = agent.run(
            {"messages": [("human", "Hello, my name is TestUser.")]},
            thread_id=thread_id,
        )

        # Print response info for debugging

        # Extract messages
        messages1 = extract_messages_from_state(response1)
        if messages1:
            last_message = messages1[-1]
            content = extract_message_content(last_message)

        # Wait briefly between messages
        time.sleep(1)

        # Second message to test memory
        # Use LangGraph format directly
        response2 = agent.run(
            {"messages": [("human", "What's my name?")]}, thread_id=thread_id
        )

        # Extract messages from second response
        messages2 = extract_messages_from_state(response2)

        # Get the last message's content
        if messages2:
            last_message = messages2[-1]
            content = extract_message_content(last_message)

            # Check for evidence of memory in response content
            # We accept either more messages (history retained) or the name in the content
            memory_success = False

            # Option 1: More messages than first response (retained history)
            if len(messages2) > len(messages1):
                memory_success = True

            # Option 2: Name is mentioned in response (context awareness)
            elif "testuser" in content.lower() or "test user" in content.lower():
                memory_success = True

            # Assertion
            assert (
                memory_success
            ), "Memory not working: response doesn't show evidence of persistence"
        else:
            raise AssertionError("No messages in second response")


    except Exception as e:
        import traceback

        traceback.print_exc()
        raise AssertionError(f"Test failed: {e}")


def test_postgres_persistence():
    """Test SimpleAgent with PostgreSQL persistence."""
    print_step("Testing SimpleAgent with PostgreSQL persistence")

    try:
        # Create a unique test name and thread ID
        test_name = f"postgres_test_{uuid.uuid4().hex[:8]}"
        thread_id = f"postgres_thread_{uuid.uuid4().hex[:8]}"

        # Create LangGraph style config
        config = {"configurable": {"thread_id": thread_id}}

        # First create and set up the pool outside the agent
        pool = ConnectionPool(conninfo=DB_URI, max_size=5, kwargs=CONNECTION_KWARGS)

        # Open the pool explicitly
        pool.open()

        # Create PostgreSQL saver with the open pool
        postgres_saver = PostgresSaver(pool)

        # Initialize tables
        postgres_saver.setup()

        # Pre-register the thread in the database
        with pool.connection() as conn, conn.cursor() as cursor:
            # First check the actual schema of the threads table
            cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name='threads'"
            )
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Threads table columns: {columns}")

            # Insert using only the thread_id column
            cursor.execute(
                "INSERT INTO threads (thread_id) VALUES (%s) ON CONFLICT DO NOTHING",
                (thread_id,),
            )

        # Create agent
        agent = create_simple_agent(
            system_prompt="You are a test assistant with memory. Remember what the user tells you.",
            name=test_name,
        )

        # Replace the agent's checkpointer with our PostgreSQL saver
        agent.checkpointer = postgres_saver

        # Recompile the app with the new checkpointer
        agent.app = agent.graph.compile(checkpointer=postgres_saver)

        # First message using proper HumanMessage format
        from langchain_core.messages import HumanMessage

        input_message = HumanMessage(content="Hello, my name is PostgresUser.")
        response1 = agent.run({"messages": [input_message]}, config=config)

        # Print response info

        # Extract messages
        messages1 = extract_messages_from_state(response1)
        if messages1:
            last_message = messages1[-1]
            content = extract_message_content(last_message)

        # Verify state was saved
        try:
            saved_state = agent.app.get_state(config)
            if saved_state and hasattr(saved_state, "values"):
                pass
        except Exception:
            pass

        # Wait briefly between messages
        time.sleep(1)

        # Second message - using the same config
        input_message2 = HumanMessage(content="What's my name?")
        response2 = agent.run({"messages": [input_message2]}, config=config)

        # Print response info

        # Extract messages
        messages2 = extract_messages_from_state(response2)

        # Get the last message's content
        if messages2:
            last_message = messages2[-1]
            content = extract_message_content(last_message)

            # Check for evidence of memory in response content
            # We accept either more messages (history retained) or the name in the content
            memory_success = False

            # Option 1: More messages than first response (retained history)
            if len(messages2) > len(messages1):
                memory_success = True

            # Option 2: Name is mentioned in response (context awareness)
            elif (
                "postgresuser" in content.lower() or "postgres user" in content.lower()
            ):
                memory_success = True

            # Assertion
            assert (
                memory_success
            ), "Memory not working: response doesn't show evidence of persistence"
        else:
            raise AssertionError("No messages in second response")


        # Close the pool after the test
        pool.close()

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise AssertionError(f"Test failed: {e}")


def test_memory_persistence():
    """Test SimpleAgent with MemorySaver persistence."""
    print_step("Testing SimpleAgent with MemorySaver")

    try:
        # Create a unique test name and thread ID
        test_name = f"memory_test_{uuid.uuid4().hex[:8]}"
        thread_id = f"memory_thread_{uuid.uuid4().hex[:8]}"

        # Create a simple agent
        agent = create_simple_agent(
            system_prompt="You are a test assistant with memory. Remember what the user tells you.",
            name=test_name,
        )

        # Replace the agent's checkpointer with an explicit MemorySaver
        memory_saver = MemorySaver()
        agent.checkpointer = memory_saver

        # Recompile the app with the new checkpointer
        agent.app = agent.graph.compile(checkpointer=memory_saver)

        # Create LangGraph config format with thread_id
        config = {"configurable": {"thread_id": thread_id}}

        # First message using proper HumanMessage format
        from langchain_core.messages import HumanMessage

        # Use proper LangGraph message format for input
        input_message = HumanMessage(content="Hello, my name is TestUser.")
        response1 = agent.run({"messages": [input_message]}, config=config)

        # Print response info for debugging

        # Extract messages
        messages1 = extract_messages_from_state(response1)

        # Wait briefly between messages
        time.sleep(1)

        # Verify state was saved
        try:
            saved_state = agent.app.get_state(config)
            if saved_state and hasattr(saved_state, "values"):
                pass
        except Exception:
            pass

        # Second message to test memory - using the SAME config
        input_message2 = HumanMessage(content="What's my name?")
        response2 = agent.run({"messages": [input_message2]}, config=config)

        # (rest of the test remains the same)

        # Extract messages from second response
        messages2 = extract_messages_from_state(response2)

        # Get the last message's content
        if messages2:
            last_message = messages2[-1]
            content = extract_message_content(last_message)

            # Check for evidence of memory in response content
            # We accept either more messages (history retained) or the name in the content
            memory_success = False

            # Option 1: More messages than first response (retained history)
            if len(messages2) > len(messages1):
                memory_success = True

            # Option 2: Name is mentioned in response (context awareness)
            elif "testuser" in content.lower() or "test user" in content.lower():
                memory_success = True

            # Assertion
            assert (
                memory_success
            ), "Memory not working: response doesn't show evidence of persistence"
        else:
            raise AssertionError("No messages in second response")


    except Exception as e:
        import traceback

        traceback.print_exc()
        raise AssertionError(f"Test failed: {e}")
