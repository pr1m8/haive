# Additional simple agents

# src/haive/prebuilt/simple/query_intent_classifier.py
"""
Agent Name: QueryIntentClassifier
Description: Classifies the intent behind a query, such as definition, comparison, fact-checking, opinion, etc.
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig
from src.haive.prebuilt.simple.query_models import QueryInput

SYSTEM_PROMPT = """
You are a query intent classifier.
Determine the user's intent from the query and output it as a descriptive label (e.g. fact-checking, comparison, explanation, definition, opinion, hypothetical).
Also give a confidence score.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class QueryIntent(BaseModel):
    intent: str = Field(..., description="The classified intent behind the query.")
    confidence: float = Field(..., description="Confidence score between 0 and 1.")

config = AugLLMConfig(
    name="query_intent_classifier",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QueryIntent,
)
