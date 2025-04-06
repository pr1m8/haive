# src/haive/prebuilt/simple/query_to_sql.py
"""
Agent Name: QueryToSQL
Description: Converts a natural language query into an SQL SELECT statement (assuming schema knowledge).
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.aug_llm import AugLLMConfig
from src.haive.prebuilt.simple.query.models import QueryModel
from src.haive.agents.simple.factory import create_simple_agent

SYSTEM_PROMPT = """
You are a SQL generator. Given a natural language query and access to a table schema, write the equivalent SQL SELECT statement.
Only output the SQL. Assume table and column names are obvious or provided separately.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class SQLQuery(BaseModel):
    sql: str = Field(..., description="The generated SQL SELECT query.")

query_to_sql_config = AugLLMConfig(
    name="query_to_sql",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=SQLQuery,
)

query_to_sql = create_simple_agent(
    engine=query_to_sql_config,
    name="query_to_sql"
)
