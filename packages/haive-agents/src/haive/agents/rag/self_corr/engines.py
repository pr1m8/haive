from langchain_core.prompts import PromptTemplate

REWRITER_PROMPT = """
Look at the input and try to reason about the underlying semantic intent / meaning.\n
Here is the initial question:\n
------- \n
{question}\n
------- \n
Formulate an improved question:
"""

REWRITER_PROMPT_TEMPLATE = PromptTemplate.from_template(REWRITER_PROMPT)


GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context}"
)

GENERATE_PROMPT_TEMPLATE = PromptTemplate.from_template(GENERATE_PROMPT)


GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
)

GRADE_PROMPT_TEMPLATE = PromptTemplate.from_template(GRADE_PROMPT)
