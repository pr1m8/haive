from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.models.llm.llm_config import AugLLMConfig, wiki_writer_aug_llm
from langchain_core.output_parsers import StrOutputParser

from haive.agents.research.storm.wiki_writer.prompt import writer_prompt

graph = BaseGraph(name="wiki_writer")

writer = writer_prompt | long_context_llm | StrOutputParser()
