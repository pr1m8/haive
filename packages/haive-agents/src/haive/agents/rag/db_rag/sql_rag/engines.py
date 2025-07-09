"""LLM engine configurations for SQL RAG Agent.

This module defines pre-configured AugLLMConfig instances for each step
in the SQL RAG workflow. Each engine is optimized for its specific task
with appropriate prompts and output models.

Example:
    Using default engines::

        >>> from haive.agents.rag.db_rag.sql_rag.engines import default_sql_engines
        >>>
        >>> # Access a specific engine
        >>> sql_generator = default_sql_engines["generate_sql"]
        >>> print(sql_generator.name)
        'generate_sql_config'

    Customizing engines::

        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>> from haive.agents.rag.db_rag.sql_rag.engines import default_sql_engines
        >>>
        >>> # Create custom SQL generator with different model
        >>> custom_sql_gen = AugLLMConfig(
        ...     name="custom_sql_generator",
        ...     model="gpt-4",
        ...     temperature=0.1,
        ...     prompt_template=GENERATE_SQL_PROMPT,
        ...     structured_output_model=SQLQueryOutput
        ... )
        >>>
        >>> # Use with custom engines dict
        >>> custom_engines = {
        ...     **default_sql_engines,
        ...     "generate_sql": custom_sql_gen
        >>> }
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import StrOutputParser

from haive.agents.rag.db_rag.sql_rag.models import (
    GradeAnswer,
    GradeHallucinations,
    GuardrailsOutput,
    SQLAnalysisOutput,
    SQLQueryOutput,
    SQLValidationOutput,
)
from haive.agents.rag.db_rag.sql_rag.prompts import (
    ANALYZE_QUERY_PROMPT,
    ANSWER_GRADING_PROMPT,
    GENERATE_FINAL_ANSWER_PROMPT,
    GENERATE_SQL_PROMPT,
    GUARDRAILS_PROMPT,
    HALLUCINATION_CHECK_PROMPT,
    VALIDATE_SQL_PROMPT,
)

# Engine for analyzing queries
analyze_query_aug_llm_config = AugLLMConfig(
    name="analyze_query_config",
    prompt_template=ANALYZE_QUERY_PROMPT,
    structured_output_model=SQLAnalysisOutput,
)
"""Engine for analyzing natural language queries.

This engine breaks down user questions to identify:
- Relevant database tables
- Required columns
- Necessary joins
- Aggregations needed
- WHERE clause constraints

Returns:
    SQLAnalysisOutput: Structured analysis of query requirements.

Example:
    >>> engine = analyze_query_aug_llm_config
    >>> result = engine.invoke({
    ...     "question": "Top 5 customers by total purchase amount",
    ...     "schema": db_schema,
    ...     "dialect": "postgresql"
    ... })
    >>> print(result.relevant_tables)
    ['customers', 'orders']
"""

# Engine for generating SQL
generate_sql_aug_llm_config = AugLLMConfig(
    name="generate_sql_config",
    prompt_template=GENERATE_SQL_PROMPT,
    structured_output_model=SQLQueryOutput,
)
"""Engine for generating SQL queries from natural language.

This engine converts analyzed queries into syntactically correct SQL,
considering the database dialect and schema constraints.

Returns:
    SQLQueryOutput: Generated SQL query with optional parameters.

Example:
    >>> engine = generate_sql_aug_llm_config
    >>> result = engine.invoke({
    ...     "question": "Show all orders from last month",
    ...     "schema": db_schema,
    ...     "dialect": "mysql",
    ...     "query_analysis": analysis_output
    ... })
    >>> print(result.query)
    'SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)'
"""

# Engine for validating SQL
validate_sql_aug_llm_config = AugLLMConfig(
    name="validate_sql_config",
    prompt_template=VALIDATE_SQL_PROMPT,
    structured_output_model=SQLValidationOutput,
)
"""Engine for validating generated SQL queries.

This engine checks SQL queries for:
- Syntax errors
- Invalid table/column references
- Missing GROUP BY clauses
- Potential performance issues
- Security concerns

Returns:
    SQLValidationOutput: Validation results with errors and suggestions.

Example:
    >>> engine = validate_sql_aug_llm_config
    >>> result = engine.invoke({
    ...     "sql_query": "SELECT category, SUM(amount) FROM sales",
    ...     "schema": db_schema,
    ...     "dialect": "postgresql"
    ... })
    >>> print(result.errors)
    ['Missing GROUP BY clause for non-aggregated column: category']
"""

# Engine for guardrails
guardrails_aug_llm_config = AugLLMConfig(
    name="guardrails_config",
    prompt_template=GUARDRAILS_PROMPT,
    structured_output_model=GuardrailsOutput,
)
"""Engine for domain relevance checking (guardrails).

This engine determines if a user's question is about querying
the database or something unrelated that should be rejected.

Returns:
    GuardrailsOutput: Decision to proceed or end with reason.

Example:
    >>> engine = guardrails_aug_llm_config
    >>> result = engine.invoke({
    ...     "question": "What's the weather like?",
    ...     "schema": db_schema,
    ...     "tables": ["orders", "customers"]
    ... })
    >>> print(result.decision)
    'end'
    >>> print(result.reason)
    'Question is about weather, not database content'
"""

# Engine for generating final answer
generate_final_answer_aug_llm_config = AugLLMConfig(
    name="generate_final_answer_config",
    prompt_template=GENERATE_FINAL_ANSWER_PROMPT,
    output_parser=StrOutputParser(),
)
"""Engine for generating natural language answers.

This engine converts SQL query results into clear, comprehensive
answers that directly address the user's question.

Returns:
    str: Natural language answer based on query results.

Example:
    >>> engine = generate_final_answer_aug_llm_config
    >>> answer = engine.invoke({
    ...     "question": "Who are our top customers?",
    ...     "sql_query": "SELECT name, total_spent FROM customers ORDER BY total_spent DESC LIMIT 5",
    ...     "query_result": "John Doe|5000\\nJane Smith|4500\\n..."
    ... })
    >>> print(answer)
    'Your top customers are: 1. John Doe ($5,000), 2. Jane Smith ($4,500)...'
"""

# Engine for hallucination checking
hallucination_check_aug_llm_config = AugLLMConfig(
    name="hallucination_check_config",
    prompt_template=HALLUCINATION_CHECK_PROMPT,
    structured_output_model=GradeHallucinations,
)
"""Engine for detecting hallucinations in answers.

This engine verifies that generated answers only contain
information supported by the actual query results.

Returns:
    GradeHallucinations: Binary score for hallucination presence.

Example:
    >>> engine = hallucination_check_aug_llm_config
    >>> result = engine.invoke({
    ...     "question": "Total sales?",
    ...     "query_result": "total|1000",
    ...     "answer": "Total sales are $1000 with 50% growth"  # Growth not in data
    ... })
    >>> print(result.binary_score)
    'no'  # Hallucination detected
"""

# Engine for answer grading
answer_grading_aug_llm_config = AugLLMConfig(
    name="answer_grading_config",
    prompt_template=ANSWER_GRADING_PROMPT,
    structured_output_model=GradeAnswer,
)
"""Engine for grading answer relevance.

This engine evaluates whether the generated answer actually
addresses the user's original question.

Returns:
    GradeAnswer: Binary score for answer relevance.

Example:
    >>> engine = answer_grading_aug_llm_config
    >>> result = engine.invoke({
    ...     "question": "What's our best selling product?",
    ...     "answer": "We have 500 products in our catalog"  # Doesn't answer question
    ... })
    >>> print(result.binary_score)
    'no'  # Answer doesn't address question
"""

# Default engines configuration
default_sql_engines = {
    "analyze_query": analyze_query_aug_llm_config,
    "generate_sql": generate_sql_aug_llm_config,
    "validate_sql": validate_sql_aug_llm_config,
    "guardrails": guardrails_aug_llm_config,
    "generate_final_answer": generate_final_answer_aug_llm_config,
    "hallucination_check": hallucination_check_aug_llm_config,
    "answer_grading": answer_grading_aug_llm_config,
}
"""Default engine configuration dictionary.

This dictionary contains all the pre-configured engines needed
for the SQL RAG workflow. It can be used as-is or customized
by replacing specific engines.

Example:
    Using defaults::
    
        >>> config = SQLRAGConfig(engines=default_sql_engines)
        
    Customizing specific engine::
    
        >>> custom_engines = {
        ...     **default_sql_engines,
        ...     "generate_sql": my_custom_sql_generator
        ... }
        >>> config = SQLRAGConfig(engines=custom_engines)
"""
