from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate

rag_base_prompt = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know. Use three sentences
maximum and keep the answer concise.
Question: {query}
Context: {context}
Answer:
"""
rag_prompt_template = ChatPromptTemplate.from_template(rag_base_prompt)
rag_aug_llm = AugLLMConfig(prompt_template=rag_prompt_template)
