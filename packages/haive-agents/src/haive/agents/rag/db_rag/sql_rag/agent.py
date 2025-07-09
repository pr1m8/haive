"""SQL RAG Agent for natural language database querying.

This module implements a sophisticated SQL Retrieval-Augmented Generation (RAG) agent
that enables natural language querying of SQL databases. The agent uses a multi-step
workflow to analyze queries, generate SQL, validate results, and produce accurate answers.

Example:
    Basic usage of the SQL RAG Agent::

        >>> from haive.agents.rag.db_rag.sql_rag import SQLRAGAgent, SQLRAGConfig
        >>>
        >>> # Create configuration
        >>> config = SQLRAGConfig(
        ...     domain_name="sales",
        ...     db_config=SQLDatabaseConfig(
        ...         db_type="postgresql",
        ...         db_name="sales_db"
        ...     )
        ... )
        >>>
        >>> # Initialize agent
        >>> agent = SQLRAGAgent(config)
        >>>
        >>> # Query the database
        >>> result = agent.invoke({
        ...     "question": "What were the total sales last quarter?"
        ... })
        >>> print(result["answer"])
        'Total sales last quarter were $1.2M across 450 transactions...'

Attributes:
    logger (logging.Logger): Module-level logger for debugging and monitoring.

Note:
    This agent requires proper database credentials and connection details
    to be configured either through environment variables or explicit configuration.
"""

import logging

import sqlparse
from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.branches import Branch
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.rag.db_rag.sql_rag.config import SQLRAGConfig
from haive.agents.rag.db_rag.sql_rag.engines import default_sql_engines
from haive.agents.rag.db_rag.sql_rag.state import OverallState
from haive.agents.rag.db_rag.sql_rag.utils import (
    create_sql_toolkit,
    create_tool_node_with_fallback,
    explore_database_schema,
    get_all_toolkit_tools,
)

logger = logging.getLogger(__name__)


@register_agent(SQLRAGConfig)
class SQLRAGAgent(Agent[SQLRAGConfig]):
    """SQL RAG Agent for querying SQL databases with natural language.

    This agent implements a sophisticated workflow for converting natural language
    questions into SQL queries, executing them safely, and generating accurate
    natural language responses. The workflow includes:

    1. **Domain Relevance Check**: Validates if the query is database-related
    2. **Schema Retrieval**: Gets relevant database schema information
    3. **Query Analysis**: Determines required tables, columns, and operations
    4. **SQL Generation**: Creates syntactically correct SQL from natural language
    5. **Validation & Correction**: Ensures SQL is safe and correct
    6. **Execution**: Runs the query safely with proper error handling
    7. **Answer Generation**: Produces natural language answers from results

    Attributes:
        sql_db (SQLDatabase): Connected database instance
        db_schema (Dict[str, Any]): Complete database schema information
        dialect (str): SQL dialect being used (postgresql, mysql, etc.)
        toolkit (SQLDatabaseToolkit): LangChain SQL toolkit instance
        tools (List[BaseTool]): Available database tools
        tool_nodes (Dict[str, ToolNode]): Tool nodes for workflow
        engines (Dict[str, AugLLMConfig]): LLM engines for each step

    Example:
        Creating and using a SQL RAG Agent::

            >>> # Configure for a PostgreSQL database
            >>> config = SQLRAGConfig(
            ...     domain_name="e-commerce",
            ...     db_config=SQLDatabaseConfig(
            ...         db_type="postgresql",
            ...         db_host="localhost",
            ...         db_name="shop_db",
            ...         include_tables=["orders", "products", "customers"]
            ...     ),
            ...     hallucination_check=True,
            ...     max_iterations=3
            ... )
            >>>
            >>> # Create agent
            >>> agent = SQLRAGAgent(config)
            >>>
            >>> # Ask questions in natural language
            >>> response = agent.invoke({
            ...     "question": "Which products had the highest sales last month?"
            ... })
            >>>
            >>> # Access results
            >>> print(f"Answer: {response['answer']}")
            >>> print(f"SQL Used: {response['sql_statement']}")

    Note:
        The agent includes safety features like SQL validation, hallucination
        detection, and query result verification to ensure accurate responses.
    """

    def __init__(self, config: SQLRAGConfig):
        """Initialize the SQL RAG Agent with the given configuration.

        Args:
            config (SQLRAGConfig): Configuration object containing database
                connection details, LLM settings, and workflow parameters.

        Raises:
            ValueError: If database connection fails or required engines
                are missing from the configuration.

        Example:
            >>> config = SQLRAGConfig(
            ...     db_config=SQLDatabaseConfig(db_uri="sqlite:///sales.db")
            ... )
            >>> agent = SQLRAGAgent(config)
        """
        self._initialize_config(config)
        super().__init__(config)

    def _initialize_config(self, config: SQLRAGConfig) -> None:
        """Initialize the configuration and components.

        This method sets up the database connection, explores the schema,
        creates necessary tools, and configures all LLM engines.

        Args:
            config (SQLRAGConfig): The configuration object to initialize from.

        Raises:
            ValueError: If database connection fails or is invalid.

        Note:
            This method is called automatically during agent initialization
            and should not be called directly.
        """
        try:
            # Initialize database connection
            self.sql_db = config.db_config.get_sql_db()
            if not self.sql_db:
                raise ValueError(
                    f"Failed to connect to {config.db_config.db_type} database"
                )

            # Explore the database schema thoroughly
            self.db_schema = explore_database_schema(self.sql_db)
            self.dialect = self.db_schema["dialect"]
            self.no_results = "No results found"

            # Create toolkit and get all tools
            self.toolkit = create_sql_toolkit(
                config.db_config, config.llm_config if config.llm_config else None
            )
            self.tools = get_all_toolkit_tools(self.toolkit)

            # Create tool nodes for each tool
            self.tool_nodes = {}
            for tool in self.tools:
                self.tool_nodes[tool.name] = create_tool_node_with_fallback(tool)

            # Map engines from config
            self.engines = {}
            if hasattr(config, "engines") and config.engines:
                # Start with default engines
                self.engines = {**default_sql_engines}
                # Override with any provided in config
                for key, engine in config.engines.items():
                    if engine is not None:
                        self.engines[key] = engine
            else:
                # Use default engines
                self.engines = default_sql_engines

            logger.info(
                f"SQL RAG Agent initialized with {len(self.db_schema['tables'])} tables"
            )

        except Exception as e:
            logger.error(f"Error initializing SQLRAGAgent: {e}")
            raise

    def check_domain_relevance(self, state: OverallState) -> Command:
        """Determine if the query is relevant to databases.

        This method uses a guardrails LLM to check if the user's question
        is about querying the database or if it's an unrelated question
        that should be rejected.

        Args:
            state (OverallState): Current state containing the question.

        Returns:
            Command: Update command with next_action set to either
                'end' (if irrelevant) or continue to schema retrieval.

        Example:
            >>> state = OverallState(question="What tables are in the database?")
            >>> command = agent.check_domain_relevance(state)
            >>> print(command.update["next_action"])
            'retrieve_schema'

        Note:
            Questions like "What's the weather?" or "Tell me a joke" will
            be rejected with an appropriate message.
        """
        try:
            # Get domain information
            domain_name = self.config.domain_name
            domain_categories = self.config.domain_categories

            # If no categories defined, default to domain name
            if not domain_categories:
                domain_categories = [domain_name]

            # Default category to use
            domain_categories[0] if domain_categories else domain_name

            # Use the guardrails engine
            if "guardrails" not in self.engines:
                raise ValueError("Missing 'guardrails' engine in configuration")

            # Pass the required variables to the guardrails engine
            guardrails_output = self.engines["guardrails"].invoke(
                {
                    "question": state.question,
                    "schema": self.db_schema,
                    "tables": self.db_schema.get("tables", []),
                }
            )

            database_records = None

            # Handle the output - it might be an AIMessage or a structured output
            if hasattr(guardrails_output, "decision"):
                # It's a structured GuardrailsOutput
                decision = guardrails_output.decision
            elif hasattr(guardrails_output, "content"):
                # It's an AIMessage - try to parse the content
                try:
                    # If it's JSON content, parse it
                    import json

                    content = guardrails_output.content
                    if isinstance(content, str):
                        parsed = json.loads(content)
                        decision = parsed.get("decision", "continue")
                    else:
                        decision = "continue"  # Default if we can't parse
                except:
                    # If parsing fails, default to continue
                    decision = "continue"
            else:
                # Unknown output type, default to continue
                decision = "continue"

            if decision == "end":
                database_records = f"This question is not about {domain_name}. I can only answer questions about databases."

            return Command(
                update={
                    "next_action": decision,
                    "database_records": database_records,
                    "steps": ["check_domain_relevance"],
                }
            )
        except Exception as e:
            logger.error(f"Error in check_domain_relevance: {e}")
            return Command(
                update={
                    "error": f"Error checking domain relevance: {e!s}",
                    "next_action": "end",
                }
            )

    def retrieve_schema(self, state: OverallState) -> Command:
        """Retrieve database schema information for context.

        This method gathers detailed schema information about all relevant
        tables in the database, including column names, types, and relationships.

        Args:
            state (OverallState): Current state of the workflow.

        Returns:
            Command: Update command with schema information and instruction
                to proceed to query analysis.

        Example:
            Schema retrieval for a sales database::

                >>> state = OverallState(question="Show me all orders")
                >>> command = agent.retrieve_schema(state)
                >>> schema_info = command.update["schema_info"]
                >>> print(f"Found {len(schema_info)} tables")
                Found 5 tables

        Note:
            For large databases, this method limits schema retrieval to the
            first 10 tables to avoid overwhelming the LLM context.
        """
        try:
            # Find the get_schema tool
            get_schema_tool = next(
                (tool for tool in self.tools if tool.name == "sql_db_schema"), None
            )

            schema_info = {}
            # Get schema for all tables (or limit to a subset for very large databases)
            if get_schema_tool:
                for table in self.db_schema["tables"][
                    :10
                ]:  # Limit to first 10 tables if there are many
                    try:
                        schema_info[table] = get_schema_tool.invoke(
                            {"table_names": table}
                        )
                    except Exception as e:
                        schema_info[table] = f"Error retrieving schema: {e!s}"
            else:
                # Fallback if tool not available
                for table in self.db_schema["tables"][:10]:
                    schema_info[table] = self.db_schema["table_info"].get(
                        table, "Schema not available"
                    )

            # Format schema information
            schema_message = "Database Schema Information:\n\n"
            for table, info in schema_info.items():
                schema_message += f"Table: {table}\n{info}\n\n"

            return Command(
                update={
                    "schema_info": schema_info,
                    "database_schema": schema_message,
                    "next_action": "analyze_query",
                    "steps": state.steps + ["retrieve_schema"],
                    "messages": state.messages + [AIMessage(content=schema_message)],
                }
            )
        except Exception as e:
            logger.error(f"Error in retrieve_schema: {e}")
            return Command(
                update={
                    "error": f"Error retrieving database schema: {e!s}",
                    "next_action": "end",
                }
            )

    def analyze_query(self, state: OverallState) -> Command:
        """Analyze the query to determine relevant tables and fields.

        This method uses an LLM to understand the user's natural language
        question and identify which database tables, columns, joins, and
        aggregations will be needed to answer it.

        Args:
            state (OverallState): Current state containing the question
                and schema information.

        Returns:
            Command: Update command with query analysis including:
                - relevant_tables: Tables needed for the query
                - needed_columns: Specific columns to select
                - constraints: WHERE clause conditions
                - aggregations: GROUP BY/aggregate functions needed
                - joins_needed: Required table joins

        Example:
            Analyzing a complex query::

                >>> state = OverallState(
                ...     question="Show me top 5 customers by total order value"
                ... )
                >>> command = agent.analyze_query(state)
                >>> analysis = command.update["query_analysis"]
                >>> print(analysis.relevant_tables)
                ['customers', 'orders', 'order_items']
                >>> print(analysis.aggregations)
                ['SUM(order_items.price * order_items.quantity)']

        Note:
            The analysis helps the SQL generation step create more accurate
            queries by understanding the semantic intent.
        """
        try:
            if "analyze_query" not in self.engines:
                raise ValueError("Missing 'analyze_query' engine in configuration")

            analysis = self.engines["analyze_query"].invoke(
                {
                    "question": state.question,
                    "schema": self.db_schema,
                    "dialect": self.dialect,
                }
            )

            # Store analysis in a way that works with different return types
            query_analysis = analysis
            tables_needed = []

            # Try to extract tables_needed based on the return type
            if hasattr(analysis, "relevant_tables"):
                tables_needed = analysis.relevant_tables
            elif isinstance(analysis, dict) and "relevant_tables" in analysis:
                tables_needed = analysis["relevant_tables"]

            return Command(
                update={
                    "query_analysis": query_analysis,
                    "tables_needed": tables_needed,
                    "next_action": "generate_query",
                    "steps": state.steps + ["analyze_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in analyze_query: {e}")
            return Command(
                update={
                    "error": f"Error analyzing query: {e!s}",
                    "next_action": "end",
                }
            )

    def generate_query(self, state: OverallState) -> Command:
        """Generate an SQL query from the natural language question.

        This method converts the user's natural language question into
        a syntactically correct SQL query, using the analysis results
        and database schema information.

        Args:
            state (OverallState): Current state containing question,
                schema, and query analysis.

        Returns:
            Command: Update command with the generated SQL query,
                formatted for readability.

        Example:
            SQL generation from natural language::

                >>> state = OverallState(
                ...     question="What were the total sales by category last month?"
                ... )
                >>> command = agent.generate_query(state)
                >>> print(command.update["sql_query"])
                '''
                SELECT
                    c.category_name,
                    SUM(oi.quantity * oi.price) as total_sales
                FROM categories c
                JOIN products p ON c.category_id = p.category_id
                JOIN order_items oi ON p.product_id = oi.product_id
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
                GROUP BY c.category_name
                ORDER BY total_sales DESC
                '''

        Note:
            The method includes special handling for metadata queries like
            "what tables are in the database" that don't require complex SQL.
        """
        try:
            if "generate_sql" not in self.engines:
                raise ValueError("Missing 'generate_sql' engine in configuration")

            # For "what tables" questions, create a direct response based on schema
            question_lower = state.question.lower()
            if (
                "what tables" in question_lower
                or "list tables" in question_lower
                or "show tables" in question_lower
                or "which tables" in question_lower
            ):
                # Extract table names directly from the schema
                tables = self.db_schema.get("tables", [])

                # Create a simple and safe query for this specific use case
                tables_list = ", ".join(tables)
                return Command(
                    update={
                        "sql_query": f"-- Database contains tables: {tables_list}",
                        "next_action": "generate_answer",  # Skip to answer generation
                        "steps": state.steps + ["generate_query"],
                        "query_result": f"The database contains the following tables: {tables_list}",
                    }
                )

            # Access query_analysis safely
            query_analysis = getattr(state, "query_analysis", None)

            # Get examples for few-shot learning if available
            examples = []
            if (
                hasattr(self.config, "domain_examples")
                and self.config.domain_name in self.config.domain_examples
            ):
                examples = self.config.domain_examples[self.config.domain_name]

            # Format examples
            fewshot_examples = ""
            if examples:
                fewshot_examples = "\n\n".join(
                    [
                        f"Question: {example['question']}\nSQL query: {example['query']}"
                        for example in examples
                    ]
                )

            # Use consistent variable names matching prompt template
            sql_query = self.engines["generate_sql"].invoke(
                {
                    "question": state.question,
                    "schema": self.db_schema,
                    "dialect": self.dialect,
                    "query_analysis": query_analysis,  # Changed from analysis to query_analysis
                    "fewshot_examples": fewshot_examples,
                }
            )

            logger.info(f"Generated SQL query: {sql_query}")

            # Handle if it already returns an SQLQueryOutput
            if hasattr(sql_query, "query"):
                formatted_query = sql_query
            else:
                # Format query with sqlparse
                try:
                    formatted_query = sqlparse.format(
                        sql_query, reindent=True, keyword_case="UPPER"
                    )
                except Exception as e:
                    logger.warning(f"Error formatting SQL query: {e}")
                    formatted_query = sql_query

            return Command(
                update={
                    "sql_query": formatted_query,
                    "next_action": "validate_query",
                    "steps": state.steps + ["generate_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in generate_query: {e}")
            return Command(
                update={
                    "error": f"Error generating SQL query: {e!s}",
                    "next_action": "end",
                }
            )

    def validate_query(self, state: OverallState) -> Command:
        """Validate the SQL query for syntax and schema correctness.

        This method performs comprehensive validation of the generated SQL
        including syntax checking, table/column name verification, join
        validation, and security checks.

        Args:
            state (OverallState): Current state containing the SQL query
                to validate.

        Returns:
            Command: Update command with either:
                - next_action="execute_query" if valid
                - next_action="correct_query" if errors found
                - sql_errors list containing any validation errors

        Example:
            Validating a query with an error::

                >>> state = OverallState(
                ...     sql_query="SELECT * FROM non_existent_table"
                ... )
                >>> command = agent.validate_query(state)
                >>> print(command.update["sql_errors"])
                ["Table 'non_existent_table' does not exist in the schema"]
                >>> print(command.update["next_action"])
                'correct_query'

        Note:
            The validation prevents SQL injection and ensures only safe
            SELECT queries are executed.
        """
        try:
            if "validate_sql" not in self.engines:
                raise ValueError("Missing 'validate_sql' engine in configuration")

            # Handle case where sql_query might be empty
            if not state.sql_query:
                return Command(
                    update={
                        "sql_errors": ["Query not provided."],
                        "next_action": "end",
                        "steps": state.steps + ["validate_query"],
                    }
                )

            # Extract query string if it's an object
            sql_str = state.sql_query
            if hasattr(state.sql_query, "query"):
                sql_str = state.sql_query.query

            # Use consistent variable names matching prompt template
            validation_result = self.engines["validate_sql"].invoke(
                {
                    "question": state.question,
                    "sql_query": sql_str,  # Changed from sql to sql_query
                    "schema": self.db_schema,
                    "dialect": self.dialect,
                }
            )

            # Check validation result
            is_valid = True
            errors = []
            if hasattr(validation_result, "is_valid"):
                is_valid = validation_result.is_valid

            if hasattr(validation_result, "errors"):
                errors = validation_result.errors

            if not is_valid:
                return Command(
                    update={
                        "next_action": "correct_query",
                        "sql_errors": errors,
                        "steps": state.steps + ["validate_query"],
                    }
                )
            return Command(
                update={
                    "next_action": "execute_query",
                    "steps": state.steps + ["validate_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in validate_query: {e}")
            return Command(
                update={
                    "error": f"Error validating SQL query: {e!s}",
                    "next_action": "end",
                }
            )

    def correct_query(self, state: OverallState) -> Command:
        """Correct the SQL query based on validation errors.

        This method takes a query with validation errors and attempts to
        fix them, learning from the specific issues identified.

        Args:
            state (OverallState): Current state containing the invalid query
                and the list of errors.

        Returns:
            Command: Update command with corrected SQL query and instruction
                to re-validate.

        Example:
            Correcting a query with a missing GROUP BY::

                >>> state = OverallState(
                ...     sql_query="SELECT category, SUM(amount) FROM sales",
                ...     sql_errors=["Missing GROUP BY clause for 'category'"]
                ... )
                >>> command = agent.correct_query(state)
                >>> print(command.update["sql_query"])
                'SELECT category, SUM(amount) FROM sales GROUP BY category'

        Note:
            The correction process may iterate multiple times based on the
            max_iterations configuration setting.
        """
        try:
            if "correct_sql" not in self.engines:
                raise ValueError("Missing 'correct_sql' engine in configuration")

            corrected_sql = self.engines["correct_sql"].invoke(
                {
                    "question": state.question,
                    "sql_query": state.sql_query,
                    "errors": state.sql_errors,
                    "schema": self.db_schema,
                    "dialect": self.dialect,
                }
            )

            # Format query with sqlparse
            try:
                formatted_query = sqlparse.format(
                    corrected_sql, reindent=True, keyword_case="upper"
                )
            except Exception as e:
                logger.warning(f"Error formatting corrected SQL query: {e}")
                formatted_query = corrected_sql

            return Command(
                update={
                    "sql_query": formatted_query,
                    "next_action": "validate_query",
                    "steps": state.steps + ["correct_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in correct_query: {e}")
            return Command(
                update={
                    "error": f"Error correcting SQL query: {e!s}",
                    "next_action": "end",
                }
            )

    def execute_query(self, state: OverallState) -> Command:
        r"""Execute the SQL query against the database.

        This method safely executes the validated SQL query and captures
        the results. It includes error handling and timeout protection.

        Args:
            state (OverallState): Current state containing the validated
                SQL query to execute.

        Returns:
            Command: Update command with query results or error message.

        Example:
            Executing a query and handling results::

                >>> state = OverallState(
                ...     sql_query="SELECT COUNT(*) as total FROM orders"
                ... )
                >>> command = agent.execute_query(state)
                >>> print(command.update["query_result"])
                'total\n-----\n1234'

        Warning:
            Only SELECT queries are executed. Any DML operations (INSERT,
            UPDATE, DELETE) are rejected during validation.
        """
        try:
            # Find the run_query tool
            run_query_tool = next(
                (tool for tool in self.tools if tool.name == "sql_db_query"), None
            )

            # Check if sql_query is present
            if not state.sql_query:
                return Command(
                    update={
                        "query_result": "No SQL query to execute",
                        "next_action": "generate_answer",
                        "steps": state.steps + ["execute_query"],
                    }
                )

            # Extract query string if it's an object
            sql_query_str = state.sql_query
            if hasattr(state.sql_query, "query"):
                sql_query_str = state.sql_query

            if run_query_tool:
                try:
                    # Use the tool to execute the query string
                    result = run_query_tool.invoke({"query": sql_query_str})

                    if not result or (isinstance(result, str) and result.strip() == ""):
                        result = self.no_results
                except Exception as e:
                    logger.error(f"Error executing SQL query: {e}")
                    result = f"Error executing query: {e!s}"
            else:
                # Execute directly if tool not available
                try:
                    result = self.sql_db.run(sql_query_str)
                    if not result:
                        result = self.no_results
                except Exception as e:
                    logger.error(f"Error executing SQL query directly: {e}")
                    result = f"Error executing query: {e!s}"

            return Command(
                update={
                    "query_result": result,
                    "next_action": "generate_answer",
                    "steps": state.steps + ["execute_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in execute_query: {e}")
            return Command(
                update={
                    "error": f"Error executing SQL query: {e!s}",
                    "next_action": "end",
                }
            )

    def generate_answer(self, state: OverallState) -> Command:
        r"""Generate the final answer based on the query results.

        This method converts the raw SQL query results into a natural
        language answer that directly addresses the user's question.
        It includes optional hallucination checking to ensure accuracy.

        Args:
            state (OverallState): Current state containing the question,
                SQL query, and query results.

        Returns:
            Command: Update command with the final answer and optional
                hallucination check results.

        Example:
            Generating an answer with hallucination checking::

                >>> state = OverallState(
                ...     question="Who is our top customer?",
                ...     query_result="customer_name | total_spent\\n-----------\\nAcme Corp | 50000"
                ... )
                >>> command = agent.generate_answer(state)
                >>> print(command.update["answer"])
                'Your top customer is Acme Corp with total spending of $50,000.'
                >>> print(command.update["hallucination_check"])
                'no'  # No hallucinations detected

        Note:
            If hallucination checking is enabled and detects issues, a
            warning is appended to the answer.
        """
        try:
            if "generate_final_answer" not in self.engines:
                raise ValueError(
                    "Missing 'generate_final_answer' engine in configuration"
                )

            # Extract sql query string if it's an object
            sql_str = state.sql_query
            if hasattr(state.sql_query, "query"):
                sql_str = state.sql_query.query

            # For special case of listing tables
            if isinstance(sql_str, str) and sql_str.startswith(
                "-- Database contains tables:"
            ):
                tables_list = sql_str.replace(
                    "-- Database contains tables:", ""
                ).strip()
                return Command(
                    update={
                        "answer": f"The database contains the following tables: {tables_list}",
                        "next_action": "end",
                        "steps": state.steps + ["generate_answer"],
                    }
                )

            # Generate the final answer
            answer = self.engines["generate_final_answer"].invoke(
                {
                    "question": state.question,
                    "sql_query": sql_str,
                    "query_result": state.query_result,
                }
            )

            # Proceed with the usual workflow
            result = {
                "answer": answer,
                "final_sql": sql_str,
                "next_action": "end",
                "steps": state.steps + ["generate_answer"],
            }

            # Run hallucination check if required
            if (
                self.config.hallucination_check
                and "hallucination_check" in self.engines
            ):
                try:
                    hallucination_result = self.engines["hallucination_check"].invoke(
                        {
                            "question": state.question,
                            "answer": answer,
                            "query_result": state.query_result,
                        }
                    )

                    result["hallucination_check"] = hallucination_result

                    # If hallucinations detected, provide a warning
                    if (
                        hasattr(hallucination_result, "hallucination_detected")
                        and hallucination_result.hallucination_detected
                    ):
                        warning = f"\n\nWarning: The answer may contain information not supported by the data. Areas of concern: {hallucination_result.problem_areas}"
                        result["answer"] = answer + warning

                except Exception as e:
                    logger.warning(f"Error in hallucination check: {e}")
                    # Continue with generated answer even if hallucination check fails

            return Command(update=result)
        except Exception as e:
            logger.error(f"Error in generate_answer: {e}")
            return Command(
                update={
                    "error": f"Error generating answer: {e!s}",
                    "answer": f"An error occurred while generating the answer: {e!s}",
                    "next_action": "end",
                }
            )

    def domain_router(self, state: OverallState) -> str:
        """Route based on domain relevance check.

        Args:
            state (OverallState): Current state with next_action field.

        Returns:
            str: Next node name - either END or "retrieve_schema".
        """
        if state.next_action == "end":
            return END
        return "retrieve_schema"

    def validation_router(self, state: OverallState) -> str:
        """Route based on query validation results.

        Args:
            state (OverallState): Current state with next_action field.

        Returns:
            str: Next node name - END, "correct_query", or "execute_query".
        """
        if state.next_action == "end":
            return END
        if state.next_action == "correct_query":
            return "correct_query"
        return "execute_query"

    def setup_workflow(self) -> None:
        """Set up the SQL RAG workflow graph.

        This method constructs the workflow graph with all necessary nodes
        and edges, including conditional routing based on validation results.

        The workflow follows this path:
        1. START -> check_domain_relevance
        2. Domain routing (end if irrelevant)
        3. retrieve_schema -> analyze_query -> generate_query
        4. validate_query with correction loop if needed
        5. execute_query -> generate_answer -> END

        Note:
            This method is called automatically during agent initialization
            and should not be called directly.
        """
        # Add nodes for the workflow
        self.graph.add_node("check_domain_relevance", self.check_domain_relevance)
        self.graph.add_node("retrieve_schema", self.retrieve_schema)
        self.graph.add_node("analyze_query", self.analyze_query)
        self.graph.add_node("generate_query", self.generate_query)
        self.graph.add_node("validate_query", self.validate_query)
        self.graph.add_node("correct_query", self.correct_query)
        self.graph.add_node("execute_query", self.execute_query)
        self.graph.add_node("generate_answer", self.generate_answer)

        # Connect nodes
        self.graph.add_edge(START, "check_domain_relevance")

        # Add conditional edges using Branch directly
        domain_branch = Branch(
            key="next_action",
            destinations={"end": END, "retrieve_schema": "retrieve_schema"},
            default="retrieve_schema",
        )

        self.graph.add_conditional_edges(
            "check_domain_relevance",
            domain_branch,  # Branch object can be called directly
            domain_branch.destinations,  # Pass the destinations mapping
        )

        # Linear flow
        self.graph.add_edge("retrieve_schema", "analyze_query")
        self.graph.add_edge("analyze_query", "generate_query")
        self.graph.add_edge("generate_query", "validate_query")

        # Validation branch
        validation_branch = Branch(
            key="next_action",
            destinations={
                "correct_query": "correct_query",
                "execute_query": "execute_query",
                "end": END,
            },
            default="execute_query",
        )

        self.graph.add_conditional_edges(
            "validate_query", validation_branch, validation_branch.destinations
        )

        # Complete the flow
        self.graph.add_edge("correct_query", "validate_query")
        self.graph.add_edge("execute_query", "generate_answer")
        self.graph.add_edge("generate_answer", END)

        logger.info("SQL RAG workflow setup complete")
