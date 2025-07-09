"""State definitions for the Graph Database RAG Agent.

This module defines the state schemas used throughout the Graph DB RAG workflow,
including input, output, and overall state management for Cypher query generation
and execution.

Example:
    Basic usage of the state classes::

        >>> from haive.agents.rag.db_rag.graph_db.state import InputState, OverallState
        >>>
        >>> # Create input state
        >>> input_state = InputState(question="What movies were released in 2023?")
        >>>
        >>> # Create overall state for workflow
        >>> state = OverallState(
        ...     question="What movies were released in 2023?",
        ...     next_action="generate_query"
        ... )

Note:
    The state classes use Pydantic v2 for validation and serialization.
    All fields have sensible defaults to support partial state updates.
"""

from pydantic import BaseModel, Field


class InputState(BaseModel):
    """Input state for the graph database agent.

    This class defines the initial input structure for queries to the
    Graph DB RAG agent. It contains only the user's natural language question.

    Attributes:
        question: The user's natural language question to be converted to Cypher
            and executed against the Neo4j database.

    Example:
        >>> input_state = InputState(question="Who directed The Matrix?")
        >>> print(input_state.question)
        Who directed The Matrix?
    """

    question: str = Field(description="The user's question in natural language")


class OutputState(BaseModel):
    """Output state for the graph database agent.

    This class defines the final output structure returned by the Graph DB RAG
    agent after processing a query. It includes the answer, execution steps,
    and the generated Cypher statement.

    Attributes:
        answer: The natural language answer generated from the query results.
            Defaults to empty string if no answer has been generated yet.
        steps: List of workflow steps executed during query processing.
            Useful for debugging and understanding the agent's reasoning.
        cypher_statement: The final Cypher query that was executed.
            Useful for learning and debugging purposes.

    Example:
        >>> output = OutputState(
        ...     answer="The Wachowskis directed The Matrix.",
        ...     steps=["check_domain", "generate_query", "execute_query"],
        ...     cypher_statement="MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'The Matrix'}) RETURN p.name"
        ... )
    """

    answer: str = Field(
        default="", description="The final answer to the user's question"
    )
    steps: list[str] = Field(
        default_factory=list,
        description="The workflow steps taken to reach the current state",
    )
    cypher_statement: str = Field(
        default="",
        description="The generated Cypher statement used to query the database",
    )


class OverallState(InputState, OutputState):
    """Complete state for the graph database agent workflow.

    This class combines input and output states with additional fields needed
    for the internal workflow execution. It tracks the current state of query
    processing including errors, validation results, and database records.

    Attributes:
        next_action: The next workflow step to execute. Used for routing
            decisions in the graph. Common values include:
            - "generate_query": Generate Cypher from natural language
            - "validate_query": Validate the generated Cypher
            - "correct_cypher": Fix errors in the Cypher statement
            - "execute_query": Run the query against Neo4j
            - "end": Terminate the workflow
        cypher_errors: List of validation errors found in the Cypher statement.
            Used by the correction step to fix issues.
        database_records: Records retrieved from the Neo4j database.
            Can be a list of dictionaries or a string message if no results.

    Example:
        >>> state = OverallState(
        ...     question="What are the top rated movies?",
        ...     next_action="generate_query",
        ...     cypher_statement="MATCH (m:Movie) RETURN m.title, m.rating ORDER BY m.rating DESC LIMIT 5",
        ...     database_records=[
        ...         {"m.title": "The Shawshank Redemption", "m.rating": 9.3},
        ...         {"m.title": "The Godfather", "m.rating": 9.2}
        ...     ]
        ... )

    Note:
        This state is passed between all nodes in the workflow graph,
        accumulating information as the query is processed.
    """

    next_action: str = Field(
        default="", description="The next action/node to execute in the workflow"
    )
    cypher_errors: list[str] = Field(
        default=[], description="Validation errors found in the Cypher statement"
    )
    database_records: list[dict] = Field(
        default=[], description="Records retrieved from the Neo4j database query"
    )
