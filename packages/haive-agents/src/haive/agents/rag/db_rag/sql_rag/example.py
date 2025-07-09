"""Example usage of SQL RAG Agent.

This module demonstrates various usage patterns for the SQL RAG Agent,
from basic queries to advanced configurations. It includes examples for
different database types, error handling, and customization options.

Running the Examples:
    Basic example::

        $ python example.py

    With specific database::

        $ SQL_DB_TYPE=mysql SQL_DB_NAME=mydb python example.py

    With custom query::

        $ python example.py --query "Show me top products by revenue"

Examples Included:
    1. Basic usage with default configuration
    2. PostgreSQL with specific tables
    3. SQLite with local file
    4. MySQL with authentication
    5. Complex queries with joins
    6. Error handling and validation
    7. Custom LLM engines
    8. Batch processing

Note:
    Ensure you have proper database credentials configured either
    through environment variables or in the code before running.
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.rag.db_rag.sql_rag.agent import SQLRAGAgent
from haive.agents.rag.db_rag.sql_rag.config import SQLDatabaseConfig, SQLRAGConfig
from haive.agents.rag.db_rag.sql_rag.engines import default_sql_engines

# For backward compatibility
SQLDatabaseAgent = SQLRAGAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def basic_example() -> dict[str, Any]:
    """Run a basic example with default configuration.

    This example demonstrates the simplest usage of the SQL RAG Agent
    with minimal configuration, relying on environment variables.

    Returns:
        Dict[str, Any]: Query result including answer and SQL used.

    Example Output:
        >>> result = basic_example()
        ✅ Connected to postgresql database
        >>> print(result["answer"])
        'The database contains the following tables: customers, orders, products...'
    """
    print("\n" + "=" * 50)
    print("BASIC EXAMPLE - Default Configuration")
    print("=" * 50)

    # Create a sample configuration using defaults
    config = SQLRAGConfig()

    # Initialize the agent
    agent = SQLRAGAgent(config)

    # Run a sample query
    result = agent.run({"question": "What tables are in this database?"})

    print("\nQuestion: What tables are in this database?")
    print(f"Answer: {result.get('answer', 'No answer generated')}")
    print(f"SQL Used: {result.get('sql_statement', 'No SQL generated')}")

    return result


def postgresql_example() -> dict[str, Any]:
    """Example with PostgreSQL configuration and specific tables.

    This example shows how to configure the agent for a PostgreSQL
    database with specific table inclusion and custom domain settings.

    Returns:
        Dict[str, Any]: Query result from PostgreSQL database.

    Example:
        >>> result = postgresql_example()
        Configuring PostgreSQL connection...
        ✅ Connected to postgresql database
        >>> print(result["answer"])
        'Your top 5 customers by total order value are...'
    """
    print("\n" + "=" * 50)
    print("POSTGRESQL EXAMPLE - Custom Configuration")
    print("=" * 50)

    # Configure PostgreSQL connection
    db_config = SQLDatabaseConfig(
        db_type="postgresql",
        db_host="localhost",
        db_port="5432",
        db_name="northwind",
        db_user="postgres",
        db_password="postgres",
        include_tables=["customers", "orders", "order_details", "products"],
        sample_rows_in_table_info=5,
    )

    # Configure agent for e-commerce domain
    agent_config = SQLRAGConfig(
        domain_name="e-commerce",
        domain_categories=["sales", "customers", "products"],
        db_config=db_config,
        hallucination_check=True,
        max_iterations=3,
    )

    # Create agent
    agent = SQLRAGAgent(agent_config)

    # Run a complex query
    result = agent.run({"question": "Who are my top 5 customers by total order value?"})

    print("\nQuestion: Who are my top 5 customers by total order value?")
    print(f"Answer: {result.get('answer', 'No answer generated')}")
    print(f"SQL Used: {result.get('sql_statement', 'No SQL generated')}")

    return result


def sqlite_example() -> dict[str, Any]:
    """Example with SQLite database file.

    This example demonstrates using a local SQLite database file,
    which is useful for development and testing.

    Returns:
        Dict[str, Any]: Query result from SQLite database.

    Example:
        >>> result = sqlite_example()
        Using SQLite database: ./data/sample.db
        ✅ Connected to sqlite database
        >>> print(result["answer"])
        'The total number of active users is 1,234...'
    """
    print("\n" + "=" * 50)
    print("SQLITE EXAMPLE - Local File Database")
    print("=" * 50)

    # Configure SQLite connection
    db_config = SQLDatabaseConfig(
        db_type="sqlite", db_name="./data/sample.db"  # Path to SQLite file
    )

    # Simple configuration
    config = SQLRAGConfig(domain_name="sample_data", db_config=db_config)

    # Create agent
    agent = SQLRAGAgent(config)

    # Run query
    result = agent.run({"question": "How many active users do we have?"})

    print("\nQuestion: How many active users do we have?")
    print(f"Answer: {result.get('answer', 'No answer generated')}")

    return result


def mysql_example() -> dict[str, Any]:
    """Example with MySQL database and authentication.

    This example shows MySQL configuration with full authentication
    and custom few-shot examples for better SQL generation.

    Returns:
        Dict[str, Any]: Query result from MySQL database.

    Example:
        >>> result = mysql_example()
        Connecting to MySQL database...
        ✅ Connected to mysql database
        >>> print(result["answer"])
        'Product sales trend shows 15% growth...'
    """
    print("\n" + "=" * 50)
    print("MYSQL EXAMPLE - With Authentication")
    print("=" * 50)

    # Configure MySQL connection
    db_config = SQLDatabaseConfig(
        db_type="mysql",
        db_host="mysql.example.com",
        db_port="3306",
        db_name="analytics",
        db_user="analyst",
        db_password="secure_password",
    )

    # Configure with examples
    config = SQLRAGConfig(
        domain_name="analytics",
        db_config=db_config,
        domain_examples={
            "analytics": [
                {
                    "question": "Show product sales trend",
                    "query": "SELECT DATE_FORMAT(order_date, '%Y-%m') as month, SUM(quantity * unit_price) as revenue FROM order_details od JOIN orders o ON od.order_id = o.order_id GROUP BY month ORDER BY month",
                },
                {
                    "question": "Customer retention rate",
                    "query": "SELECT COUNT(DISTINCT customer_id) as returning_customers FROM orders WHERE customer_id IN (SELECT customer_id FROM orders WHERE order_date < DATE_SUB(NOW(), INTERVAL 1 YEAR))",
                },
            ]
        },
    )

    # Create agent
    agent = SQLRAGAgent(config)

    # Run trend analysis
    result = agent.run(
        {"question": "What's the product sales trend for the last 6 months?"}
    )

    print("\nQuestion: What's the product sales trend for the last 6 months?")
    print(f"Answer: {result.get('answer', 'No answer generated')}")

    return result


def error_handling_example() -> None:
    """Demonstrate error handling and validation features.

    This example shows how the agent handles various error conditions
    including invalid queries, non-existent tables, and SQL errors.

    Example:
        >>> error_handling_example()
        Testing error handling...
        Query 1 - Invalid domain: This question is not about database...
        Query 2 - SQL error corrected successfully
        Query 3 - No results found: The database doesn't contain any orders...
    """
    print("\n" + "=" * 50)
    print("ERROR HANDLING EXAMPLE")
    print("=" * 50)

    config = SQLRAGConfig()
    agent = SQLRAGAgent(config)

    # Test various error conditions
    test_queries = [
        "What's the weather like?",  # Out of domain
        "SELECT * FROM non_existent_table",  # Invalid table
        "Show me orders from year 3000",  # No results
    ]

    for i, question in enumerate(test_queries, 1):
        print(f"\nTest {i}: {question}")
        try:
            result = agent.run({"question": question})
            print(f"Result: {result.get('answer', 'No answer')[:100]}...")
        except Exception as e:
            print(f"Error handled: {e!s}")


def custom_llm_example() -> dict[str, Any]:
    """Example with custom LLM configuration.

    This example demonstrates how to customize the LLM engines
    used for different steps in the workflow.

    Returns:
        Dict[str, Any]: Query result using custom LLM configuration.

    Example:
        >>> result = custom_llm_example()
        Using custom LLM configuration...
        >>> print(result["answer"])
        'Based on the analysis with custom temperature settings...'
    """
    print("\n" + "=" * 50)
    print("CUSTOM LLM EXAMPLE")
    print("=" * 50)

    # Create custom SQL generation engine with low temperature
    custom_sql_engine = AugLLMConfig(
        name="precise_sql_generator",
        model="gpt-4",
        temperature=0.1,  # Very low temperature for consistent SQL
        prompt_template=default_sql_engines["generate_sql"].prompt_template,
        structured_output_model=default_sql_engines[
            "generate_sql"
        ].structured_output_model,
    )

    # Custom engines configuration
    custom_engines = {
        **default_sql_engines,  # Keep all defaults
        "generate_sql": custom_sql_engine,  # Override SQL generator
    }

    # Configure agent with custom engines
    config = SQLRAGConfig(engines=custom_engines)

    agent = SQLRAGAgent(config)

    result = agent.run({"question": "Calculate the average order value by month"})

    print("\nQuestion: Calculate the average order value by month")
    print(f"Answer: {result.get('answer', 'No answer generated')}")

    return result


def batch_processing_example() -> list[dict[str, Any]]:
    """Example of processing multiple queries in batch.

    This example shows how to efficiently process multiple queries
    using the same agent instance, with performance timing.

    Returns:
        List[Dict[str, Any]]: Results for all queries.

    Example:
        >>> results = batch_processing_example()
        Processing 5 queries...
        Query 1: ✓ (1.2s)
        Query 2: ✓ (0.8s)
        ...
        Total time: 5.5s, Average: 1.1s per query
    """
    print("\n" + "=" * 50)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 50)

    config = SQLRAGConfig()
    agent = SQLRAGAgent(config)

    # List of queries to process
    queries = [
        "How many customers do we have?",
        "What's the total revenue this year?",
        "List top 5 products by sales",
        "Show customer distribution by country",
        "What's the average order size?",
    ]

    results = []
    start_time = datetime.now()

    print(f"Processing {len(queries)} queries...\n")

    for i, question in enumerate(queries, 1):
        query_start = datetime.now()

        try:
            result = agent.run({"question": question})
            query_time = (datetime.now() - query_start).total_seconds()

            results.append(
                {
                    "question": question,
                    "answer": result.get("answer", "No answer"),
                    "sql": result.get("sql_statement", ""),
                    "time": query_time,
                    "success": True,
                }
            )

            print(f"Query {i}: ✓ ({query_time:.1f}s)")

        except Exception as e:
            results.append({"question": question, "error": str(e), "success": False})
            print(f"Query {i}: ✗ (Error: {str(e)[:50]}...)")

    total_time = (datetime.now() - start_time).total_seconds()
    avg_time = total_time / len(queries)

    print(f"\nTotal time: {total_time:.1f}s, Average: {avg_time:.1f}s per query")
    print(f"Success rate: {sum(1 for r in results if r['success'])}/{len(queries)}")

    return results


def interactive_mode():
    """Run the agent in interactive mode.

    This function starts an interactive session where users can
    continuously ask questions about the database.

    Example:
        >>> interactive_mode()
        SQL RAG Agent - Interactive Mode
        Type 'exit' to quit, 'help' for commands

        SQL> What tables do we have?
        Answer: The database contains tables: customers, orders, products...

        SQL> Show me total sales
        Answer: Total sales amount to $1,234,567...

        SQL> exit
        Goodbye!
    """
    print("\n" + "=" * 50)
    print("SQL RAG Agent - Interactive Mode")
    print("Type 'exit' to quit, 'help' for commands")
    print("=" * 50 + "\n")

    config = SQLRAGConfig()
    agent = SQLRAGAgent(config)

    while True:
        try:
            # Get user input
            question = input("\nSQL> ").strip()

            # Check for commands
            if question.lower() == "exit":
                print("Goodbye!")
                break
            if question.lower() == "help":
                print("\nCommands:")
                print("  exit - Quit the program")
                print("  help - Show this help")
                print("  clear - Clear the screen")
                print("\nOr type any question about the database.")
                continue
            if question.lower() == "clear":
                import os

                os.system("clear" if os.name == "posix" else "cls")
                continue
            if not question:
                continue

            # Process the query
            print("\nProcessing...")
            result = agent.run({"question": question})

            # Display results
            print(f"\nAnswer: {result.get('answer', 'No answer generated')}")

            # Optionally show SQL
            if input("\nShow SQL? (y/n): ").lower() == "y":
                print(f"\nSQL: {result.get('sql_statement', 'No SQL generated')}")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"\nError: {e!s}")


def main():
    """Main function to run examples.

    This function provides a command-line interface for running
    different examples or custom queries.

    Command-line Arguments:
        --example: Which example to run (basic, postgresql, sqlite, mysql, error, custom, batch, interactive)
        --query: Custom query to run
        --config: Path to JSON config file

    Examples:
        Run basic example::

            $ python example.py --example basic

        Run custom query::

            $ python example.py --query "Show me revenue by product category"

        Run interactive mode::

            $ python example.py --example interactive

        Use custom config::

            $ python example.py --config my_config.json --query "Top customers"
    """
    parser = argparse.ArgumentParser(description="SQL RAG Agent Examples")
    parser.add_argument(
        "--example",
        choices=[
            "basic",
            "postgresql",
            "sqlite",
            "mysql",
            "error",
            "custom",
            "batch",
            "interactive",
        ],
        default="basic",
        help="Which example to run",
    )
    parser.add_argument("--query", type=str, help="Custom query to run")
    parser.add_argument("--config", type=str, help="Path to JSON configuration file")

    args = parser.parse_args()

    try:
        # If custom query is provided
        if args.query:
            print(f"\nRunning custom query: {args.query}")

            # Load config from file if provided
            if args.config:
                with open(args.config) as f:
                    config_data = json.load(f)
                config = SQLRAGConfig(**config_data)
            else:
                config = SQLRAGConfig()

            agent = SQLRAGAgent(config)
            result = agent.run({"question": args.query})

            print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
            print(f"\nSQL: {result.get('sql_statement', 'No SQL generated')}")

        # Run selected example
        elif args.example == "basic":
            basic_example()
        elif args.example == "postgresql":
            postgresql_example()
        elif args.example == "sqlite":
            sqlite_example()
        elif args.example == "mysql":
            mysql_example()
        elif args.example == "error":
            error_handling_example()
        elif args.example == "custom":
            custom_llm_example()
        elif args.example == "batch":
            batch_processing_example()
        elif args.example == "interactive":
            interactive_mode()

    except Exception as e:
        logger.error(f"Example failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
