"""Utility functions for SQL RAG Agent.

This module provides helper functions for database operations, toolkit creation,
error handling, and schema exploration. These utilities support the main agent
workflow with reusable functionality.

Example:
    Creating SQL toolkit::

        >>> from haive.agents.rag.db_rag.sql_rag.utils import create_sql_toolkit
        >>> from haive.agents.rag.db_rag.sql_rag.config import SQLDatabaseConfig
        >>>
        >>> db_config = SQLDatabaseConfig(db_uri="sqlite:///example.db")
        >>> toolkit = create_sql_toolkit(db_config)
        >>> tools = toolkit.get_tools()
        >>> print(f"Available tools: {[tool.name for tool in tools]}")
        Available tools: ['sql_db_query', 'sql_db_schema', 'sql_db_list_tables', ...]
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langchain_core.tools import BaseTool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import ToolNode

from haive.agents.rag.db_rag.sql_rag.config import SQLDatabaseConfig


def create_sql_toolkit(
    db_config: SQLDatabaseConfig,
    llm_config: AugLLMConfig | LLMConfig | None = None,
) -> SQLDatabaseToolkit:
    """Create a SQL Database Toolkit using the provided configuration.

    This function creates a LangChain SQLDatabaseToolkit that provides
    various tools for interacting with SQL databases including query
    execution, schema inspection, and table listing.

    Args:
        db_config (SQLDatabaseConfig): Configuration for the SQL database connection.
        llm_config (Optional[AugLLMConfig]): Configuration for the LLM to use
            with the toolkit. If None, defaults to OpenAI GPT-4.

    Returns:
        SQLDatabaseToolkit: Configured toolkit instance with database tools.

    Raises:
        ValueError: If database connection fails or is invalid.

    Example:
        Creating toolkit with custom LLM::

            >>> from haive.core.engine.aug_llm import AugLLMConfig
            >>>
            >>> llm_config = AugLLMConfig(
            ...     model="gpt-4",
            ...     temperature=0.1  # Low temperature for SQL generation
            ... )
            >>>
            >>> toolkit = create_sql_toolkit(db_config, llm_config)
            >>>
            >>> # Use toolkit to query schema
            >>> schema_tool = next(t for t in toolkit.get_tools() if t.name == "sql_db_schema")
            >>> schema = schema_tool.invoke({"table_names": "customers"})
    """
    # Get database instance
    db = db_config.get_sql_db()
    if not db:
        raise ValueError("Failed to initialize SQL database connection")

    # Initialize LLM
    if llm_config and isinstance(llm_config, LLMConfig):
        llm = llm_config.instantiate()
    elif llm_config and isinstance(llm_config, AugLLMConfig):
        llm = llm_config.instantiate_llm()
    else:
        # Default to OpenAI
        llm = AzureChatOpenAI()

    # Create and return toolkit
    return SQLDatabaseToolkit(db=db, llm=llm)


def get_all_toolkit_tools(toolkit: SQLDatabaseToolkit) -> list[BaseTool]:
    """Get all tools from a SQLDatabaseToolkit.

    Args:
        toolkit (SQLDatabaseToolkit): The toolkit instance to extract tools from.

    Returns:
        List[BaseTool]: List of all available tools in the toolkit.

    Example:
        >>> toolkit = create_sql_toolkit(db_config)
        >>> tools = get_all_toolkit_tools(toolkit)
        >>> for tool in tools:
        ...     print(f"Tool: {tool.name} - {tool.description}")
        Tool: sql_db_query - Execute a SQL query against the database
        Tool: sql_db_schema - Get the schema of specific tables
        Tool: sql_db_list_tables - List all tables in the database
    """
    return toolkit.get_tools()


def create_tool_node_with_fallback(
    tools: BaseTool | list[BaseTool],
) -> RunnableWithFallbacks:
    """Create a ToolNode with a fallback to handle errors gracefully.

    This function wraps tools in a ToolNode with error handling that
    surfaces errors back to the agent for correction rather than failing.

    Args:
        tools (Union[BaseTool, List[BaseTool]]): Tool or list of tools
            to create a node for.

    Returns:
        RunnableWithFallbacks: ToolNode wrapped with fallback error handling.

    Example:
        >>> query_tool = toolkit.get_tool("sql_db_query")
        >>> safe_tool_node = create_tool_node_with_fallback(query_tool)
        >>>
        >>> # If query fails, error is captured and returned
        >>> result = safe_tool_node.invoke({
        ...     "messages": [AIMessage(tool_calls=[{"name": "sql_db_query", "args": {"query": "INVALID SQL"}}])]
        ... })
    """
    # Convert single tool to list if needed
    if not isinstance(tools, list):
        tools = [tools]

    # Create tool node with fallback
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def handle_tool_error(state: dict[str, Any]) -> dict[str, Any]:
    r"""Handle tool execution errors by surfacing them to the agent.

    This function processes tool execution errors and formats them
    for the agent to understand and potentially correct.

    Args:
        state (Dict[str, Any]): Current state with error information.

    Returns:
        Dict[str, Any]: Modified state with formatted error messages.

    Example:
        >>> state = {
        ...     "error": ValueError("Table 'users' does not exist"),
        ...     "messages": [AIMessage(tool_calls=[{"id": "123", "name": "sql_db_query"}])]
        ... }
        >>> result = handle_tool_error(state)
        >>> print(result["messages"][0].content)
        'Error: ValueError("Table \'users\' does not exist")\\nPlease fix your mistakes.'
    """
    error = state.get("error")

    # Check if there are tool calls in the last message
    tool_calls = []
    if state.get("messages"):
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls"):
            tool_calls = last_message.tool_calls

    # If we have tool calls, create tool messages for each
    if tool_calls:
        from langchain_core.messages import ToolMessage

        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {error!r}\nPlease fix your mistakes.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }

    # Otherwise, just add error to state
    return {"sql_errors": [f"Error: {error!r}"]}


def explore_database_schema(db: SQLDatabase) -> dict[str, Any]:
    """Explore the database schema thoroughly to get comprehensive information.

    This function performs a deep exploration of the database schema,
    including tables, columns, sample data, and potential relationships.
    It's used to provide context for SQL generation.

    Args:
        db (SQLDatabase): SQLDatabase instance to explore.

    Returns:
        Dict[str, Any]: Detailed schema information including:
            - tables: List of table names
            - table_info: Detailed schema for each table
            - table_samples: Sample rows from each table
            - relationships: Detected foreign key relationships
            - dialect: SQL dialect being used

    Example:
        >>> db = SQLDatabase.from_uri("sqlite:///northwind.db")
        >>> schema_info = explore_database_schema(db)
        >>>
        >>> print(f"Found {len(schema_info['tables'])} tables")
        Found 8 tables
        >>>
        >>> print(f"Dialect: {schema_info['dialect']}")
        Dialect: sqlite
        >>>
        >>> # Show detected relationships
        >>> for rel in schema_info['relationships']:
        ...     print(f"{rel['from_table']}.{rel['column']} -> {rel['to_table']}")
        orders.customer_id -> customers
        order_details.product_id -> products

    Note:
        Relationship detection uses heuristics based on naming conventions
        and may not catch all foreign keys. For production use, consider
        querying database metadata directly.
    """
    schema_info = {
        "tables": db.get_usable_table_names(),
        "table_info": {},
        "table_samples": {},
        "relationships": [],
        "dialect": str(db.dialect),
    }

    # Get detailed information for each table
    for table in schema_info["tables"]:
        # Get schema for this table
        schema_info["table_info"][table] = db.get_table_info([table])

        # Get sample data
        try:
            samples = db.run(f"SELECT * FROM {table} LIMIT 3")
            schema_info["table_samples"][table] = samples
        except Exception as e:
            schema_info["table_samples"][table] = f"Error fetching samples: {e!s}"

    # Try to detect relationships between tables
    try:
        # This is a simplified approach - won't work for all DB types
        # For a production system, this should be adapted to the specific DB dialect
        for table1 in schema_info["tables"]:
            for table2 in schema_info["tables"]:
                if table1 != table2:
                    # Look for potential foreign keys based on naming conventions
                    t1_info = schema_info["table_info"][table1]
                    schema_info["table_info"][table2]

                    # Look for columns with names like "{table}Id" in the other table
                    for col_line in t1_info.split("\n"):
                        if (
                            f"{table2.lower()}id" in col_line.lower()
                            or f"{table2.lower()}_id" in col_line.lower()
                        ):
                            schema_info["relationships"].append(
                                {
                                    "from_table": table1,
                                    "to_table": table2,
                                    "relationship": "potential_foreign_key",
                                    "column": col_line.strip(),
                                }
                            )
    except Exception as e:
        # Relationship detection is best-effort
        schema_info["relationship_detection_error"] = str(e)

    return schema_info
