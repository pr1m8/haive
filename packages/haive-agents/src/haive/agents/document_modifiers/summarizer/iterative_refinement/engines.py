from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initial summary
summarize_prompt = ChatPromptTemplate(
    [
        ("human", "Write a concise summary of the following: {context}"),
    ]
)
initial_summary_aug_llm = AugLLMConfig(
    # model="gpt-4o-mini",
    prompt_template=summarize_prompt,
    output_parser=StrOutputParser(),
)

# Refining the summary with new docs
refine_template = """
Produce a final summary.

Existing summary up to this point:
{existing_answer}

New context:
------------
{context}
------------

Given the new context, refine the original summary.
"""
refine_prompt = ChatPromptTemplate([("human", refine_template)])

refine_summary_aug_llm = AugLLMConfig(
    prompt_template=refine_prompt,
    output_parser=StrOutputParser(),
)

print(initial_summary_aug_llm.prompt_template)
