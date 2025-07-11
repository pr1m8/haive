expand_chain = gen_related_topics_prompt | fast_llm.with_structured_output(
    RelatedSubjects
)
