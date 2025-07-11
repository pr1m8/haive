"""Prompt templates for SQL RAG Agent.

This module contains all the prompt templates used throughout the SQL RAG
workflow. Each prompt is carefully crafted to guide the LLM through specific
tasks while maintaining consistency and accuracy.

The prompts follow a structured format with clear system instructions and
user templates that include necessary context variables.

Example:
    Using prompts with LangChain::

        >>> from langchain_core.prompts import ChatPromptTemplate
        >>> from haive.agents.rag.db_rag.sql_rag.prompts import GENERATE_SQL_PROMPT
        >>>
        >>> # Format prompt with variables
        >>> messages = GENERATE_SQL_PROMPT.format_messages(
        ...     schema=db_schema,
        ...     dialect="postgresql",
        ...     question="Show top products",
        ...     query_analysis=analysis_result
        ... )
        >>>
        >>> # Use with LLM
        >>> llm = ChatOpenAI()
        >>> response = llm.invoke(messages)
"""

from langchain_core.prompts import ChatPromptTemplate

# Prompt for analyzing a natural language query
ANALYZE_QUERY_SYSTEM_PROMPT = """
You are a SQL expert who analyzes user questions to determine what tables and columns are needed to answer them.

Given a natural language question and a database schema, your task is to:
1. Identify which tables are relevant to answering the question
2. Determine which columns from those tables will be needed
3. Identify any constraints (WHERE clauses) implied by the question
4. Detect any aggregations needed (COUNT, AVG, SUM, etc.)
5. Identify required joins between tables
6. Assess the complexity of the query

Return your analysis in a structured format WITHOUT writing the actual SQL query.
"""

ANALYZE_QUERY_USER_PROMPT = """
Database Schema:
{schema}

Database Dialect: {dialect}

Question: {question}

Provide a detailed analysis of what's needed to answer this question with SQL.
"""

ANALYZE_QUERY_PROMPT = ChatPromptTemplate.from_messages(
    [("system", ANALYZE_QUERY_SYSTEM_PROMPT), ("human", ANALYZE_QUERY_USER_PROMPT)]
)
"""Prompt for analyzing natural language queries.

This prompt guides the LLM to break down user questions into SQL components
without generating the actual query. It helps identify:
- Required tables and columns
- JOIN operations needed
- WHERE clause constraints
- Aggregation functions
- Query complexity

Variables:
    schema: Database schema information
    dialect: SQL dialect (postgresql, mysql, etc.)
    question: User's natural language question

Returns:
    SQLAnalysisOutput with structured analysis
"""

# Prompt for generating SQL
GENERATE_SQL_SYSTEM_PROMPT = """
You are a SQL expert with a strong attention to detail.

Given an input question, a database schema, and a query analysis, your task is to generate a syntactically correct SQL query for the specified dialect.

Follow these guidelines:
- Generate only the SQL query without explanations
- Use the exact table and column names from the schema
- Be mindful of types and use appropriate comparisons
- Use proper joins with correct ON conditions
- Limit results to 10 rows unless specified otherwise in the question
- Use appropriate aggregation functions when needed
- Sort results in a meaningful way
- Do not include any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
"""

GENERATE_SQL_USER_PROMPT = """
Database Schema:
{schema}

Database Dialect: {dialect}

Question: {question}

Query Analysis: {query_analysis}

Please generate a SQL query to answer this question:
"""

GENERATE_SQL_PROMPT = ChatPromptTemplate.from_messages(
    [("system", GENERATE_SQL_SYSTEM_PROMPT), ("human", GENERATE_SQL_USER_PROMPT)]
)
"""Prompt for generating SQL queries.

This prompt converts natural language questions into executable SQL queries
based on the analysis and schema information. It ensures:
- Correct syntax for the specific dialect
- Safe queries (SELECT only)
- Proper use of JOINs and aggregations
- Result limiting for safety
- Meaningful result ordering

Variables:
    schema: Database schema information
    dialect: SQL dialect
    question: User's question
    query_analysis: Analysis from previous step

Returns:
    SQLQueryOutput with generated query
"""

# Prompt for validating SQL
VALIDATE_SQL_SYSTEM_PROMPT = """
You are a SQL expert who validates queries for correctness and best practices.

Review the provided SQL query and check for:
1. Syntax errors
2. Incorrect table or column names
3. Improper joins
4. Inappropriate use of aggregate functions
5. Missing GROUP BY clauses
6. Inefficient query patterns
7. Potential issues with NULL values
8. Type mismatches in comparisons
9. Logic errors in the WHERE clause
10. Any other issues that could cause the query to fail or return incorrect results

If there are errors, explain each one clearly and provide suggestions for fixing them.
"""

VALIDATE_SQL_USER_PROMPT = """
Database Schema:
{schema}

Database Dialect: {dialect}

Question: {question}

SQL Query:
{sql_query}

Please validate this SQL query and identify any issues.
"""

VALIDATE_SQL_PROMPT = ChatPromptTemplate.from_messages(
    [("system", VALIDATE_SQL_SYSTEM_PROMPT), ("human", VALIDATE_SQL_USER_PROMPT)]
)
"""Prompt for validating SQL queries.

This prompt performs comprehensive validation including:
- Syntax correctness
- Schema compliance
- JOIN validity
- Aggregation rules
- Performance considerations
- Security checks

Variables:
    schema: Database schema
    dialect: SQL dialect
    question: Original question
    sql_query: Query to validate

Returns:
    SQLValidationOutput with errors and suggestions
"""

# Prompt for guardrails
GUARDRAILS_SYSTEM_PROMPT = """
You are an intelligent assistant that determines whether a question is about querying a SQL database.

Given a question, your task is to determine if it:
1. Is attempting to query database information
2. Could be answered using SQL queries
3. Is asking for information that would typically be stored in a database

Return "database" if the question is about database information, and "end" otherwise.
"""

GUARDRAILS_USER_PROMPT = """
Database Schema:
{schema}

Available Tables: {tables}

Question: {question}

Is this question about querying the database?
"""

GUARDRAILS_PROMPT = ChatPromptTemplate.from_messages(
    [("system", GUARDRAILS_SYSTEM_PROMPT), ("human", GUARDRAILS_USER_PROMPT)]
)
"""Prompt for domain relevance checking (guardrails).

This prompt filters out irrelevant questions that aren't about
database queries, preventing the agent from attempting to answer
questions outside its scope.

Variables:
    schema: Database schema
    tables: List of table names
    question: User's question

Returns:
    GuardrailsOutput with decision and reason
"""

# Prompt for generating the final answer
GENERATE_FINAL_ANSWER_SYSTEM_PROMPT = """
You are a helpful assistant answering questions about data from a SQL database.

Based on the query results provided, form a comprehensive, accurate answer to the user's question.
Your answer should be:
- Clear and concise
- Directly addressing the user's question
- Highlighting key insights from the data
- Properly formatted for readability

If the query returned no results, explain that the data doesn't contain the information requested.
Never make up information not present in the query results.
"""

GENERATE_FINAL_ANSWER_USER_PROMPT = """
Question: {question}

SQL Query: {sql_query}

Query Results: {query_result}

Please provide a detailed answer based on these results:
"""

GENERATE_FINAL_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", GENERATE_FINAL_ANSWER_SYSTEM_PROMPT),
        ("human", GENERATE_FINAL_ANSWER_USER_PROMPT),
    ]
)
"""Prompt for generating natural language answers.

This prompt converts raw SQL query results into user-friendly
answers that directly address the original question.

Variables:
    question: Original user question
    sql_query: Executed SQL query
    query_result: Raw query results

Returns:
    String with natural language answer
"""

# Prompt for hallucination checking
HALLUCINATION_CHECK_SYSTEM_PROMPT = """
You are an evaluator assessing whether an answer contains hallucinations (information not supported by the provided data).

Given:
1. A question
2. Database query results
3. An answer to the question

Determine if the answer contains any information not present in or directly inferable from the query results.
"""

HALLUCINATION_CHECK_USER_PROMPT = """
Question: {question}
Query Results: {query_result}
Answer: {answer}

Does this answer contain only information supported by the query results?
Answer with 'yes' if there are no hallucinations, or 'no' if there are hallucinations.
"""

HALLUCINATION_CHECK_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", HALLUCINATION_CHECK_SYSTEM_PROMPT),
        ("human", HALLUCINATION_CHECK_USER_PROMPT),
    ]
)
"""Prompt for detecting hallucinations in answers.

This prompt ensures answers are grounded in actual query results
and don't include fabricated information.

Variables:
    question: Original question
    query_result: Actual data returned
    answer: Generated answer to check

Returns:
    GradeHallucinations with binary score
"""

# Prompt for answer grading
ANSWER_GRADING_SYSTEM_PROMPT = """
You are an evaluator assessing whether an answer properly addresses the original question.

Given:
1. A question
2. An answer to the question

Determine if the answer directly and fully addresses what was asked in the question.
"""

ANSWER_GRADING_USER_PROMPT = """
Question: {question}
Answer: {answer}

Does this answer properly address the question?
Answer with 'yes' or 'no'.
"""

ANSWER_GRADING_PROMPT = ChatPromptTemplate.from_messages(
    [("system", ANSWER_GRADING_SYSTEM_PROMPT), ("human", ANSWER_GRADING_USER_PROMPT)]
)
"""Prompt for grading answer relevance.

This prompt evaluates whether the generated answer actually
addresses what the user asked, ensuring quality responses.

Variables:
    question: Original question
    answer: Generated answer

Returns:
    GradeAnswer with binary score
"""
