"""Example usage of the Graph Database RAG Agent.

This module demonstrates various ways to use the GraphDBRAGAgent for querying
Neo4j databases with natural language. It includes basic usage, advanced
configurations, error handling, and different execution modes.

The examples cover:
    - Basic agent usage with default configuration
    - Custom domain configuration
    - Streaming execution with progress tracking
    - Batch query processing
    - Error handling and debugging
    - Performance monitoring

To run these examples:
    1. Ensure Neo4j is running and accessible
    2. Set environment variables for Neo4j connection
    3. Run: python example.py

Example:
    Basic execution::

        $ export NEO4J_URI="bolt://localhost:7687"
        $ export NEO4J_USER="neo4j"
        $ export NEO4J_PASSWORD="your-password"
        $ python example.py

Note:
    These examples assume you have a Neo4j database with movie data.
    Adjust the queries and domain configuration for your specific use case.
"""

import asyncio
import json
import logging
import time

from haive.agents.rag.db_rag.graph_db.agent import GraphDBRAGAgent
from haive.agents.rag.db_rag.graph_db.config import (
    ExampleConfig,
    GraphDBConfig,
    GraphDBRAGConfig,
)

# Configure logging for better debugging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def basic_example():
    """Demonstrate basic usage of GraphDBRAGAgent.

    This example shows the simplest way to use the agent with default
    configuration. It relies on environment variables for Neo4j connection.

    Example Output:
        >>> basic_example()
        🎬 Basic GraphDB RAG Agent Example
        =====================================

        Question: What is the movie with the highest rating?

        Processing...
        ✅ Answer: The highest rated movie is "The Shawshank Redemption" with a rating of 9.3.

        📊 Execution Details:
        - Cypher Query: MATCH (m:Movie) RETURN m.title, m.rating ORDER BY m.rating DESC LIMIT 1
        - Processing Time: 2.3 seconds
        - Steps: ['check_domain_relevance', 'generate_query', 'validate_query', 'execute_query', 'generate_answer']
    """

    try:
        # Create agent with default configuration
        agent = GraphDBRAGAgent(config=GraphDBRAGConfig())

        # Sample question
        question = "What is the movie with the highest rating?"

        # Track execution time
        start_time = time.time()

        # Invoke the agent
        result = agent.run({"question": question})

        # Calculate execution time
        execution_time = time.time() - start_time

        # Display results


    except Exception as e:
        logger.exception(f"Error in basic example: {e}")


def streaming_example():
    """Demonstrate streaming execution with progress tracking.

    This example shows how to use the streaming interface to monitor
    the agent's progress through each step of the workflow.

    Example Output:
        >>> streaming_example()
        🌊 Streaming GraphDB RAG Agent Example
        =====================================

        Question: Who directed The Matrix?

        📍 Step: check_domain_relevance
           ✓ Domain check passed

        📍 Step: generate_query
           ✓ Generated Cypher: MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'The Matrix'}) RETURN p.name

        📍 Step: validate_query
           ✓ Query validation passed

        📍 Step: execute_query
           ✓ Query executed successfully
           📊 Results: [{'p.name': 'Lana Wachowski'}, {'p.name': 'Lilly Wachowski'}]

        📍 Step: generate_answer
           ✓ Final answer generated

        ✅ Final Answer: The Matrix was directed by Lana Wachowski and Lilly Wachowski.
    """

    try:
        # Create agent
        agent = GraphDBRAGAgent(config=GraphDBRAGConfig())

        question = "Who directed The Matrix?"

        # Stream the execution
        for chunk in agent.stream(
            {"question": question},
            config={"configurable": {"thread_id": "example-stream"}},
        ):
            # Process each step
            for node_name, node_output in chunk.items():

                # Handle different node outputs
                if node_name == "check_domain_relevance":
                    if node_output.get("next_action") != "end":
                        pass")
                    else:
                        pass")

                elif node_name == "generate_query":
                    cypher = node_output.get("cypher_statement", "")
                    if cypher:
                        pass")

                elif node_name == "validate_query":
                    if node_output.get("next_action") == "execute_query":
                        pass")
                    else:
                        errors = node_output.get("cypher_errors", [])

                elif node_name == "execute_query":
                    records = node_output.get("database_records", [])
                    if records and records != "No results found":
                    else:
                        passnd")

                elif node_name == "generate_answer":
                    pass")


        # Get final result
        final_result = agent.run({"question": question})

    except Exception as e:
        logger.exception(f"Error in streaming example: {e}")


def custom_domain_example():
    """Demonstrate agent configuration for a custom domain.

    This example shows how to configure the agent for a specific domain
    with custom examples and categories.

    Example Output:
        >>> custom_domain_example()
        🏥 Custom Domain (Healthcare) Example
        =====================================

        Configuring agent for healthcare domain...

        Testing domain relevance:
        - ✅ "Which patients have diabetes?" - Accepted
        - ❌ "What's the weather today?" - Rejected (out of domain)

        Processing healthcare query...
        Answer: The following patients have been diagnosed with diabetes: John Smith, Mary Johnson, and Robert Williams.
    """

    try:
        # Configure for healthcare domain

        # Create custom examples for few-shot learning
        healthcare_examples = [
            {
                "question": "Which patients have diabetes?",
                "query": "MATCH (p:Patient)-[:HAS_CONDITION]->(c:Condition {name: 'Diabetes'}) RETURN p.name",
            },
            {
                "question": "What medications treat hypertension?",
                "query": "MATCH (m:Medication)-[:TREATS]->(c:Condition {name: 'Hypertension'}) RETURN m.name",
            },
            {
                "question": "List all cardiologists",
                "query": "MATCH (d:Doctor {specialty: 'Cardiology'}) RETURN d.name",
            },
        ]

        # Create configuration
        config = GraphDBRAGConfig(
            domain_name="healthcare",
            domain_categories=[
                "patient",
                "doctor",
                "medication",
                "condition",
                "treatment",
            ],
            example_config=ExampleConfig(
                examples=healthcare_examples, k=2  # Use 2 most similar examples
            ),
            graph_db_config=GraphDBConfig(
                # Assuming healthcare database
                graph_db_database="healthcare"
            ),
        )

        # Create agent
        agent = GraphDBRAGAgent(config)

        # Test domain relevance

        # Should pass
        healthcare_question = "Which patients have diabetes?"
        result = agent.run({"question": healthcare_question})
        if "answer" in result and "not about healthcare" not in result["answer"]:
            pass')
        else:
            pass')

        # Should fail
        weather_question = "What's the weather today?"
        result = agent.run({"question": weather_question})
        if "not about healthcare" in result.get("answer", ""):
            pass')
        else:
            pass')

        # Process a real healthcare query
        result = agent.run({"question": healthcare_question})

    except Exception as e:
        logger.exception(f"Error in custom domain example: {e}")


def batch_processing_example():
    """Demonstrate batch processing of multiple queries.

    This example shows how to efficiently process multiple queries
    and collect statistics about the execution.

    Example Output:
        >>> batch_processing_example()
        📦 Batch Processing Example
        =====================================

        Processing 5 queries...

        1. "What are the top 5 rated movies?"
           ✅ Success (2.1s)

        2. "Who acted in The Godfather?"
           ✅ Success (1.8s)

        3. "What's the weather?"
           ❌ Out of domain (0.5s)

        📊 Batch Statistics:
        - Total Queries: 5
        - Successful: 4 (80%)
        - Failed: 1 (20%)
        - Average Time: 1.7s
        - Total Time: 8.5s
    """

    try:
        # Create agent
        agent = GraphDBRAGAgent(config=GraphDBRAGConfig())

        # Define batch of queries
        queries = [
            "What are the top 5 rated movies?",
            "Who acted in The Godfather?",
            "Which movies were released in 2023?",
            "What's the weather today?",  # This should fail domain check
            "Who directed Inception?",
        ]


        # Track statistics
        results = []
        successful = 0
        failed = 0
        total_time = 0

        # Process each query
        for i, question in enumerate(queries, 1):
            start_time = time.time()

            try:
                result = agent.run({"question": question})
                execution_time = time.time() - start_time

                # Check if successful
                if "not about" in result.get("answer", "").lower():
                    failed += 1
                else:
                    successful += 1

                results.append(
                    {
                        "question": question,
                        "answer": result.get("answer"),
                        "time": execution_time,
                        "success": "not about" not in result.get("answer", "").lower(),
                    }
                )

                total_time += execution_time

            except Exception as e:
                execution_time = time.time() - start_time
                failed += 1
                total_time += execution_time

        # Display statistics

        # Save results to file
        with open("batch_results.json", "w") as f:
            json.dump(results, f, indent=2)

    except Exception as e:
        logger.exception(f"Error in batch processing: {e}")


def error_handling_example():
    """Demonstrate error handling and recovery strategies.

    This example shows how the agent handles various error conditions
    including invalid queries, connection issues, and schema mismatches.

    Example Output:
        >>> error_handling_example()
        🛡️ Error Handling Example
        =====================================

        Testing various error scenarios...

        1. Invalid Cypher syntax:
           Initial query had errors: ['Syntax error at line 1']
           ✅ Successfully corrected and executed

        2. Non-existent labels:
           ⚠️  Handled gracefully: Label 'NonExistentNode' not in schema

        3. Complex nested query:
           ✅ Successfully validated and executed
    """

    try:
        # Create agent with debug configuration
        config = GraphDBRAGConfig(domain_name="movies")
        agent = GraphDBRAGAgent(config)


        # Test 1: Query that might generate invalid Cypher
        complex_question = (
            "Show me all actors who have worked with directors who have won an Oscar"
        )

        # Use streaming to see the correction process
        for chunk in agent.stream({"question": complex_question}):
            if "validate_query" in chunk:
                if chunk["validate_query"].get("cypher_errors"):
                    pass
            elif "correct_query" in chunk:
                pass")

        # Test 2: Query with non-existent entities
        result = agent.run(
            {
                "question": "List all SpaceShips in the database"  # Assuming no SpaceShip label
            }
        )
        if "not about movies" in result.get("answer", "").lower():
            passin")
        else:
            pass

        # Test 3: Very complex query
        complex_result = agent.run(
            {
                "question": "What is the average rating of movies directed by people who have also acted?"
            }
        )
        if complex_result.get("answer"):

    except Exception as e:
        logger.exception(f"Error in error handling example: {e}")


def performance_monitoring_example():
    """Demonstrate performance monitoring and optimization.

    This example shows how to monitor agent performance and identify
    bottlenecks in the workflow.

    Example Output:
        >>> performance_monitoring_example()
        ⚡ Performance Monitoring Example
        =====================================

        Running performance analysis...

        📊 Performance Metrics:

        Step                    | Time (s) | % of Total
        -------------------------|----------|------------
        check_domain_relevance   |   0.3    |   12%
        generate_query           |   1.2    |   48%
        validate_query           |   0.4    |   16%
        execute_query            |   0.3    |   12%
        generate_answer          |   0.3    |   12%
        -------------------------|----------|------------
        Total                    |   2.5    |   100%

        🎯 Optimization Suggestions:
        - Query generation is the bottleneck (48% of time)
        - Consider caching frequent queries
        - Use more specific examples for faster generation
    """

    try:
        # Create agent
        agent = GraphDBRAGAgent(config=GraphDBRAGConfig())


        # Track timing for each step
        step_times = {}
        total_start = time.time()

        # Use streaming to measure each step
        question = "What are the top 10 highest grossing movies?"

        for chunk in agent.stream({"question": question}):
            for node_name, _node_output in chunk.items():
                if node_name not in step_times:
                    step_times[node_name] = {
                        "start": time.time(),
                        "end": None,
                        "duration": None,
                    }
                else:
                    step_times[node_name]["end"] = time.time()
                    step_times[node_name]["duration"] = (
                        step_times[node_name]["end"] - step_times[node_name]["start"]
                    )

        total_time = time.time() - total_start

        # Display performance metrics

        # Calculate and display metrics
        for step, timing in step_times.items():
            if timing["duration"]:
                percentage = (timing["duration"] / total_time) * 100


        # Identify bottlenecks
        bottleneck = max(step_times.items(), key=lambda x: x[1]["duration"] or 0)


        if bottleneck[0] == "generate_query":
        elif bottleneck[0] == "execute_query":
        elif bottleneck[0] == "validate_query":

    except Exception as e:
        logger.exception(f"Error in performance monitoring: {e}")


async def async_example():
    """Demonstrate asynchronous execution of the agent.

    This example shows how to use the agent asynchronously for
    better performance in async applications.

    Example Output:
        >>> asyncio.run(async_example())
        🔄 Async Execution Example
        =====================================

        Processing 3 queries concurrently...

        ✅ Query 1 completed: "What are the top rated movies?"
        ✅ Query 2 completed: "Who directed The Godfather?"
        ✅ Query 3 completed: "Which actors have won an Oscar?"

        Total time: 2.8s (vs ~7s sequential)
    """

    try:
        # Create agent
        agent = GraphDBRAGAgent(config=GraphDBRAGConfig())

        # Define queries to process concurrently
        queries = [
            "What are the top rated movies?",
            "Who directed The Godfather?",
            "Which actors have won multiple Oscars?",
        ]


        # Define async task
        async def process_query(agent, question, index):
            start_time = time.time()
            try:
                # Note: This is a simplified example
                # In practice, you'd use agent.ainvoke() if available
                result = await asyncio.to_thread(agent.invoke, {"question": question})
                execution_time = time.time() - start_time
                return {
                    "index": index,
                    "question": question,
                    "answer": result.get("answer", "No answer"),
                    "time": execution_time,
                    "success": True,
                }
            except Exception as e:
                return {
                    "index": index,
                    "question": question,
                    "error": str(e),
                    "time": time.time() - start_time,
                    "success": False,
                }

        # Process all queries concurrently
        start_time = time.time()
        tasks = [
            process_query(agent, question, i) for i, question in enumerate(queries, 1)
        ]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Display results
        for result in sorted(results, key=lambda x: x["index"]):
            if result["success"]:
            else:

        # Compare with sequential time
        sequential_time = sum(r["time"] for r in results)

    except Exception as e:
        logger.exception(f"Error in async example: {e}")


def main():
    """Run all examples with a menu interface.

    This function provides an interactive menu to run different examples
    demonstrating various features of the GraphDBRAGAgent.

    Example:
        Running the main function::

            $ python example.py

            🎯 GraphDB RAG Agent Examples
            =============================

            Select an example to run:
            1. Basic Usage
            2. Streaming Execution
            3. Custom Domain Configuration
            4. Batch Processing
            5. Error Handling
            6. Performance Monitoring
            7. Async Execution
            8. Run All Examples
            0. Exit

            Enter your choice (0-8):
    """

    examples = {
        "1": basic_example,
        "2": streaming_example,
        "3": custom_domain_example,
        "4": batch_processing_example,
        "5": error_handling_example,
        "6": performance_monitoring_example,
        "7": lambda: asyncio.run(async_example()),
        "8": lambda: run_all_examples(),
    }

    while True:
        try:
            choice = input("\nEnter your choice (0-8): ").strip()

            if choice == "0":
                break
            if choice in examples:
                examples[choice]()
                input("\nPress Enter to continue...")
            else:
                pass")

        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.exception(f"Error in main menu: {e}")


def run_all_examples():
    """Run all examples in sequence.

    This function executes all example functions to demonstrate
    the full capabilities of the GraphDBRAGAgent.
    """

    examples = [
        ("Basic Usage", basic_example),
        ("Streaming Execution", streaming_example),
        ("Custom Domain", custom_domain_example),
        ("Batch Processing", batch_processing_example),
        ("Error Handling", error_handling_example),
        ("Performance Monitoring", performance_monitoring_example),
        ("Async Execution", lambda: asyncio.run(async_example())),
    ]

    for i, (name, func) in enumerate(examples, 1):

        try:
            func()
        except Exception as e:
            logger.exception(f"Error running {name}: {e}")

        if i < len(examples):
            time.sleep(2)



if __name__ == "__main__":
    """Entry point for the example script.

    Runs the main menu when executed directly.
    """
    try:
        main()
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        exit(1)
