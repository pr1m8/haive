"""State schemas for SQL RAG Agent.

This module defines the state schemas used throughout the SQL RAG workflow.
It includes input, output, and intermediate state representations that flow
through the agent's graph nodes.

The state pattern enables tracking of all intermediate steps, results, and
metadata throughout the query generation and execution process.

Example:
    Working with agent states::

        >>> from haive.agents.rag.db_rag.sql_rag.state import OverallState
        >>>
        >>> # Initialize state with a question
        >>> state = OverallState(question="Show me top customers by revenue")
        >>>
        >>> # State updates through workflow
        >>> state.steps.append("analyze_query")
        >>> state.analysis = {"relevant_tables": ["customers", "orders"]}
        >>> state.sql_query = "SELECT c.name, SUM(o.total) FROM customers c..."
        >>>
        >>> # Final output
        >>> state.answer = "The top customers by revenue are..."
"""

from typing import Any

from pydantic import BaseModel, Field


class InputState(BaseModel):
    """Input state for the SQL database agent.

    This represents the initial input to the agent - just the natural
    language question to be answered.

    Attributes:
        question (str): The natural language question to ask the SQL database.

    Example:
        >>> input_state = InputState(
        ...     question="What were the total sales last month?"
        ... )
    """

    question: str = Field(description="The question to ask the SQL database")


class OutputState(BaseModel):
    """Output state for the SQL database agent.

    This represents the final output from the agent including the answer
    and any validation results.

    Attributes:
        answer (str): The natural language answer to the question.
        sql_statement (str): The SQL query that was executed.
        hallucination_check (Optional[str]): Result of hallucination detection.
        answer_grade (Optional[str]): Result of answer quality grading.

    Example:
        >>> output = OutputState(
        ...     answer="Total sales last month were $125,000 across 350 orders.",
        ...     sql_statement="SELECT SUM(total), COUNT(*) FROM orders WHERE date >= '2024-01-01'",
        ...     hallucination_check="no",
        ...     answer_grade="yes"
        ... )
    """

    answer: str = Field(description="The answer to the question")
    sql_statement: str = Field(
        default="", description="The SQL statement that was executed"
    )
    hallucination_check: str | None = Field(
        default=None, description="Result of hallucination check"
    )
    answer_grade: str | None = Field(
        default=None, description="Result of answer grading"
    )


class OverallState(InputState, OutputState):
    r"""Overall state for the SQL database agent workflow.

    This comprehensive state class tracks all information throughout the
    agent's execution, including inputs, intermediate results, and outputs.
    It inherits from both InputState and OutputState to provide a complete view.

    Attributes:
        Input (inherited from InputState):
            question (str): The question to ask the SQL database.

        Intermediate:
            steps (List[str]): Workflow steps executed.
            next_action (str): The next action to take in the workflow.
            analysis (Dict[str, Any]): Query analysis results.
            sql_errors (List[str]): SQL validation errors.
            sql_query (str): The generated SQL query.
            query_result (str): Raw results from database query.
            database_records (Any): Parsed database query results.
            messages (List[Any]): Conversation messages.

        Output (inherited from OutputState):
            answer (str): The final answer.
            hallucination_check (Optional[str]): Hallucination detection result.
            answer_grade (Optional[str]): Answer quality grade.

    Example:
        Tracking workflow state::

            >>> state = OverallState(question="Show revenue by product category")
            >>>
            >>> # After analysis
            >>> state.analysis = {
            ...     "relevant_tables": ["products", "orders", "order_items"],
            ...     "aggregations": ["SUM(price * quantity)"]
            ... }
            >>> state.steps.append("analyze_query")
            >>>
            >>> # After SQL generation
            >>> state.sql_query = "SELECT p.category, SUM(oi.price * oi.quantity) as revenue..."
            >>> state.steps.append("generate_query")
            >>>
            >>> # After execution
            >>> state.query_result = "Electronics|50000\\nClothing|30000\\n..."
            >>> state.steps.append("execute_query")
            >>>
            >>> # Final answer
            >>> state.answer = "Revenue by category: Electronics ($50,000), Clothing ($30,000)..."
            >>> state.steps.append("generate_answer")

    Note:
        The steps list provides an audit trail of the workflow execution,
        useful for debugging and understanding the agent's decision process.
    """

    # Input - inherited from InputState
    # question: str

    # Intermediary fields
    steps: list[str] = Field(
        default_factory=list, description="Steps executed in the agent workflow"
    )
    next_action: str = Field(
        default="", description="The next action to take in the workflow"
    )
    analysis: dict[str, Any] = Field(
        default_factory=dict,
        description="Analysis of the query structure and requirements",
    )
    sql_errors: list[str] = Field(
        default_factory=list,
        description="Errors found in the SQL statement during validation",
    )
    sql_query: str = Field(default="", description="The SQL query to execute")
    query_result: str = Field(
        default=None, description="Raw text results from the database query"
    )
    database_records: Any = Field(
        default=None, description="Structured results from the database query"
    )
    messages: list[Any] = Field(
        default_factory=list, description="Messages in the conversation for context"
    )

    # Output - inherited from OutputState
    # answer: str
    # hallucination_check: Optional[str]
    # answer_grade: Optional[str]
