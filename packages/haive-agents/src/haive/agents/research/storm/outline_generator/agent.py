generate_outline_direct = direct_gen_outline_prompt | fast_llm.with_structured_output(
    Outline
)
