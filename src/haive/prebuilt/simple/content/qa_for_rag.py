# src/haive/prebuilt/simple/qa_for_rag.py
"""
Agent Name: QAForRAGGenerator
Description: Generates QA pairs from documents suitable for fine-tuning or retrieval-augmented generation.
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig

SYSTEM_PROMPT = """
You are a question-answer pair generator for retrieval-augmented generation (RAG).
Your goal is to extract useful facts from the text and generate realistic, natural questions that could retrieve these facts.
Each QA pair should be precise, grounded in the source, and framed as a standalone example.
Prefer factual answers over subjective interpretation.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Document: {input}")
])

class QAPair(BaseModel):
    question: str = Field(..., description="A natural language question generated from the document.")
    answer: str = Field(..., description="A concise, accurate answer to the question based on the document.")

class QAForRAGOutput(BaseModel):
    qa_pairs: List[QAPair] = Field(..., description="A list of question-answer pairs suitable for RAG or QA tasks.")

config = AugLLMConfig(
    name="qa_for_rag_generator",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QAForRAGOutput,
)