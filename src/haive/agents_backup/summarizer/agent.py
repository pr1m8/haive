from typing import Annotated, List, Literal, TypedDict,Dict
from src.haive.core.engine.agent.agent import AgentArchitectureConfig,AgentArchitecture
from src.haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel,Field
from src.haive.agents.summarizer.state import SummaryState
from src.haive.agents.summarizer.aug_llms import *
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
import operator
import openai
from src.haive.agents.summarizer.aug_llms import *

from langgraph.types import Command,Send

"""
1638, in _request
    raise self._make_status_error_from_response(err.response) from None
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid 'messages[0].content': string too long. Expected a string with maximum length 1048576, but got a string with length 1123800 instead.", 'type': 'invalid_request_error', 'param': 'messages[0].content', 'code': 'string_above_max_length'}}
During task with name 'generate_summary' and id '45f607c2-df38-a452-2686-e432a7583e3f'
(.venv) will@Williams-Air-2 hive_v8 % xxxxxxxxxc
"""


class SummarizerAgentConfig(AgentArchitectureConfig):
    aug_llm_configs: Dict[str,AugLLMConfig] = Field(default_factory=lambda: {"map_chain": map_aug_llm_config,"reduce_chain": reduce_augllm_config},description="The configuration for the LLM")
    token_max: int = Field(default=1000,description="The maximum number of tokens to use for the summarizer")
    state_schema: SummaryState = Field(default=SummaryState)

class SummarizerAgent(AgentArchitecture):
    """SummarizerAgent is a class that summarizes a list of documents."""
    def __init__(self, config: SummarizerAgentConfig=SummarizerAgentConfig()):
        super().__init__(config)
        """Initialize the SummarizerAgent with model and token constraints."""
        #self.llm = AzureChatOpenAI(model="gpt-4o")
        self.token_max = config.token_max  
        self.map_chain = compose_runnable(map_aug_llm_config)
        self.reduce_chain = compose_runnable(reduce_augllm_config)
        #self.graph = None

        # Initialize prompts and chains
        #self.initialize_prompts()
        #self.initialize_chains()
        self.setup_workflow()

    

    

    def setup_workflow(self):
        """Construct the StateGraph for the summarizer workflow."""
        #graph = StateGraph(SummaryState)
        self.graph = StateGraph(self.state_schema)
        self.graph.add_node("generate_summary", self.generate_summary)
        self.graph.add_node("collect_summaries", self.collect_summaries)
        self.graph.add_node("collapse_summaries", self.collapse_summaries)
        self.graph.add_node("generate_final_summary", self.generate_final_summary)

        self.graph.add_conditional_edges(START, self.map_summaries, ["generate_summary"])
        self.graph.add_edge("generate_summary", "collect_summaries")
        self.graph.add_conditional_edges("collect_summaries", self.should_collapse)
        self.graph.add_conditional_edges("collapse_summaries", self.should_collapse)
        self.graph.add_edge("generate_final_summary", END)

        #self.graph = graph

    async def generate_summary(self, state: SummaryState):
        """Generate a summary for a single document."""
        try:
            response = await self.map_chain.ainvoke(state["content"])
            return {"summaries": [response]}
        except openai.BadRequestError.response.data.error.message as e:
            print(e)
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            content = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100).split_documents(state["content"])
            return Command(update={"summaries": [""]})

    def map_summaries(self, state: SummaryState):
        """Map out over documents to generate summaries."""
        return [
            Send("generate_summary", {"content": content})
            for content in state["contents"]
        ]

    def collect_summaries(self, state: SummaryState):
        """Collect summaries into a list of documents."""
        print(state["summaries"])
        return Command(update={"collapsed_summaries": [
                Document(summary) for summary in state["summaries"]
            ]})

    async def collapse_summaries(self, state: SummaryState):
        """Collapse summaries if their total token count exceeds the limit."""
        doc_lists = split_list_of_docs(
            state["collapsed_summaries"], self.length_function, self.token_max
        )
        results = []
        for doc_list in doc_lists:
            results.append(await acollapse_docs(doc_list, self.reduce_chain.ainvoke))

        return Command(update={"collapsed_summaries": results})

    def should_collapse(self, state: SummaryState) -> Literal["collapse_summaries", "generate_final_summary"]:
        """Determine whether to collapse summaries further."""
        num_tokens = self.length_function(state["collapsed_summaries"])
        if num_tokens > self.token_max:
            return "collapse_summaries"
        else:
            return "generate_final_summary"

    async def generate_final_summary(self, state: SummaryState):
        """Generate the final summary from collapsed summaries."""
        response = await self.reduce_chain.ainvoke(state["collapsed_summaries"])
        return Command(update={"final_summary": response})

    def length_function(self, documents: List[Document]) -> int:
        """Calculate the total token count for a set of documents."""
        #llm = self.aug_llm_configs["reduce_chain"].llm_config.instantiate_llm()
        #print(llm)
        return sum(self.config.aug_llm_configs["reduce_chain"].llm_config.instantiate_llm(model="gpt-4o").get_num_tokens(doc.page_content) for doc in documents)

    async def arun(self, contents: List[str]) -> str:
            """Run the summarization workflow and return the final summary."""
            #app = self.graph.compile()
            async for output in self.app.astream({"contents": contents},config=self.runnable_config,debug=True):
                print(output)
            return self.app


import asyncio

async def main():
    summarizer = SummarizerAgent(SummarizerAgentConfig())
    #summarizer.setup_workflow()
    response = await summarizer.arun(["Hello, world!", "This is a test."])
    print(response)

if __name__ == "__main__":
    asyncio.run(main()) 

