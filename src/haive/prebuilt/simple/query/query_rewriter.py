# src/haive/prebuilt/simple/query_rewriter.py
"""
Agent Name: QueryRewriter
Description: Improves or reformulates a user query to be clearer or more suitable for retrieval.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig
from src.haive.prebuilt.simple.query_models import QueryInput
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are a query rewriting assistant.
Rewrite the query to improve clarity, precision, and search effectiveness while preserving the original intent.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class RewrittenQuery(BaseModel):
    rewritten: str = Field(..., description="A clearer or improved version of the original query.")

config = AugLLMConfig(
    name="query_rewriter",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=RewrittenQuery,
)
