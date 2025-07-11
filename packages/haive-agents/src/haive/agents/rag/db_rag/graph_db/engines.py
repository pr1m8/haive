r"""LLM engine configurations for the Graph Database RAG Agent.

This module defines the prompt templates and AugLLMConfig instances for each
step in the Graph DB RAG workflow. Each engine is specialized for a specific
task in the Cypher query generation and execution pipeline.

The engines defined here are:
    - **guardrails**: Domain relevance checking
    - **text2cypher**: Natural language to Cypher conversion
    - **validate_cypher**: Cypher query validation
    - **correct_cypher**: Cypher error correction
    - **generate_final_answer**: Natural language response generation

Example:
    Using the engines in an agent::

        >>> from haive.agents.rag.db_rag.graph_db.engines import text2cypher_aug_llm_config
        >>>
        >>> # Use the text2cypher engine
        >>> cypher = text2cypher_aug_llm_config.invoke({
        ...     "question": "Who directed The Matrix?",
        ...     "fewshot_examples": "Question: Who acted in Movie X?\\nCypher: MATCH..."
        ... })
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.rag.db_rag.graph_db.models import (
    CypherQueryOutput,
    GuardrailsOutput,
    ValidateCypherOutput,
)

# ============================================================================
# CYPHER CORRECTION ENGINE
# ============================================================================

CORRECT_CYPHER_SYSTEM_PROMPT = """You are a Cypher expert reviewing a statement written by a junior developer.
You need to correct the Cypher statement based on the provided errors. No pre-amble.
Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!"""

CORRECT_CYPHER_USER_PROMPT = """Check for invalid syntax or semantics and return a corrected Cypher statement.

Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not wrap the response in any backticks or anything else.
Respond with a Cypher statement only!

Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.

The question is:
{question}

The Cypher statement is:
{cypher}

The errors are:
{errors}"""

CORRECT_CYPHER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [("system", CORRECT_CYPHER_SYSTEM_PROMPT), ("human", CORRECT_CYPHER_USER_PROMPT)]
)

correct_cypher_aug_llm_config = AugLLMConfig(
    prompt_template=CORRECT_CYPHER_PROMPT_TEMPLATE,
    structured_output_model=CypherQueryOutput,
)
"""Engine for correcting Cypher queries based on validation errors.

This engine takes a Cypher statement with identified errors and produces
a corrected version that should be valid against the schema.

Input Variables:
    - schema: The Neo4j database schema
    - question: The original natural language question
    - cypher: The Cypher statement with errors
    - errors: List of identified errors

Output:
    CypherQueryOutput with corrected query
"""


# ============================================================================
# CYPHER VALIDATION ENGINE
# ============================================================================

VALIDATE_CYPHER_SYSTEM_PROMPT = (
    """You are a Cypher expert reviewing a statement written by a junior developer."""
)

VALIDATE_CYPHER_USER_PROMPT = """You must check the following:
* Are there any syntax errors in the Cypher statement?
* Are there any missing or undefined variables in the Cypher statement?
* Are any node labels missing from the schema?
* Are any relationship types missing from the schema?
* Are any of the properties not included in the schema?
* Does the Cypher statement include enough information to answer the question?

Examples of good errors:
* Label (:Foo) does not exist, did you mean (:Bar)?
* Property bar does not exist for label Foo, did you mean baz?
* Relationship FOO does not exist, did you mean FOO_BAR?

Schema:
{schema}

The question is:
{question}

The Cypher statement is:
{cypher}

Make sure you don't make any mistakes!"""

validate_cypher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", VALIDATE_CYPHER_SYSTEM_PROMPT),
        ("human", VALIDATE_CYPHER_USER_PROMPT),
    ]
)

validate_cypher_aug_llm_config = AugLLMConfig(
    prompt_template=validate_cypher_prompt, structured_output_model=ValidateCypherOutput
)
"""Engine for validating Cypher queries against the database schema.

This engine checks for syntax errors, schema mismatches, and logical issues
in generated Cypher queries.

Input Variables:
    - schema: The Neo4j database schema
    - question: The original question for context
    - cypher: The Cypher statement to validate

Output:
    ValidateCypherOutput with validation results
"""


# ============================================================================
# TEXT TO CYPHER ENGINE
# ============================================================================

TEXT2CYPHER_SYSTEM_PROMPT = """You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run.
Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!"""

TEXT2CYPHER_USER_PROMPT = """Below are a number of examples of questions and their corresponding Cypher queries.

{fewshot_examples}

User input: {question}
Cypher query:"""

TEXT2CYPHER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", TEXT2CYPHER_SYSTEM_PROMPT),
        ("human", TEXT2CYPHER_USER_PROMPT),
    ]
)

text2cypher_aug_llm_config = AugLLMConfig(
    prompt_template=TEXT2CYPHER_PROMPT_TEMPLATE, output_parser=StrOutputParser()
)
"""Engine for converting natural language questions to Cypher queries.

Uses few-shot examples to learn the mapping between questions and Cypher
for the specific domain and schema.

Input Variables:
    - question: The natural language question
    - fewshot_examples: Examples of question-to-Cypher mappings

Output:
    String containing the generated Cypher query
"""


# ============================================================================
# GUARDRAILS ENGINE
# ============================================================================

GUARDRAILS_SYSTEM_PROMPT = """As an intelligent assistant, your primary objective is to decide whether a given question is related to the {domain_name} domain or not.
If the question is related to {domain_name}, output "{category}". Otherwise, output "end".
To make this decision, assess the content of the question and determine if it refers to any topics in the {domain_name} domain.
Provide only the specified output: "{category}" or "end"."""

GUARDRAILS_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", GUARDRAILS_SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)

guardrails_aug_llm_config = AugLLMConfig(
    prompt_template=GUARDRAILS_PROMPT_TEMPLATE, structured_output_model=GuardrailsOutput
)
"""Engine for checking domain relevance of user questions.

This engine acts as a guardrail to ensure questions are within the
configured domain before attempting to generate Cypher queries.

Input Variables:
    - domain_name: The configured domain (e.g., "movies")
    - category: The default category for the domain
    - question: The user's question to check

Output:
    GuardrailsOutput with routing decision
"""


# ============================================================================
# FINAL ANSWER GENERATION ENGINE
# ============================================================================

GENERATE_FINAL_HUMAN_PROMPT = """Use the following results retrieved from a database to provide
a succinct, definitive answer to the user's question.

Respond as if you are answering the question directly.

Results: {results}
Question: {question}"""

GENERATE_FINAL_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", GENERATE_FINAL_HUMAN_PROMPT),
    ]
)

generate_final_aug_llm_config = AugLLMConfig(
    prompt_template=GENERATE_FINAL_PROMPT_TEMPLATE, output_parser=StrOutputParser()
)
"""Engine for generating natural language answers from query results.

Takes raw database results and converts them into a human-friendly
response that directly answers the user's question.

Input Variables:
    - results: The database query results (list of records)
    - question: The original user question for context

Output:
    String containing the natural language answer
"""
