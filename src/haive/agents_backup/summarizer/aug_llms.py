from src.haive.core.engine.aug_llm import AugLLMConfig,compose_runnable
#from src.haive.core.runnables.runnable import CustomRunnableConfig,RunnableFactory,compose_runnable
#from src.haive.core.prompts.base import PromptTemplateFactory,PromptTemplateConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
map_prompt = ChatPromptTemplate.from_messages([('human',"Write a concise summary of the following:\\n\\n{context}")])
#map_prompt_template_config = PromptTemplateConfig(chat_prompt_template=map_prompt)
map_aug_llm_config = AugLLMConfig(
    name='summarizer_map',
    prompt_template=map_prompt,
    output_parser = StrOutputParser()
)
#map_prompt_runnable = compose_runnable(map_prompt_runnable_config)
from langchain_core.output_parsers import StrOutputParser

reduce_prompt = """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary
of the main themes.
"""
reduce_prompt = ChatPromptTemplate.from_messages([('human',reduce_prompt.strip())])
#reduce_prompt_messages = [('human',reduce_prompt.strip())]
#   reduce_prompt_template_config = PromptTemplateConfig(chat_prompt_template=reduce_prompt_messages)
reduce_augllm_config = AugLLMConfig(
    name='summarizer_reduce',
    prompt_template=reduce_prompt,
    output_parser = StrOutputParser()
)
#reduce_runnable = compose_runnable(reduce_runnable_config)