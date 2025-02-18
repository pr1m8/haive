
from langchain.prompts import PromptTemplate
from src.haive.agents.tot.models import Candidate
solution_generator_prompt = """
Generate up to {k} solutions for the problem: {problem:description}
"""
solution_generator_prompt_template = PromptTemplate.from_template(solution_generator_prompt)
solution_generator_aug_llm_config = AugLLMConfig(
    name="solution_generator",
    prompt_template=solution_generator_prompt_template,
    structured_output_model=List[Candidate],
)
