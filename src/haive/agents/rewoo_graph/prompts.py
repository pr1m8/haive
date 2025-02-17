"""Pro"""
from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.aug_llm.base import AugLLMConfig,compose_runnable



map_prompt = ChatPromptTemplate.from_messages([('human',"Write a concise summary of the following:\\n\\n{context}")])
#map_prompt_template_config = PromptTemplateConfig(chat_prompt_template=map_prompt)
#map_augllm_config = AugLLMConfig(
#    name='summarizer_map',
#    prompt_template_config=map_prompt
#)
reduce_prompt = """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary
of the main themes.
"""
reduce_prompt = ChatPromptTemplate.from_messages([('human',reduce_prompt.strip())])
