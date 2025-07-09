# from haive.core.agent_architecture.base import AgentState
from haive.core.engine.agent.agent import Agent, register_agent
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START

# from haive.core.engine.agent.agent import AgentConfig
from langgraph.types import Command

# Initial summary
from haive.agents.document_modifiers.summarizer.iterative_refinement.config import (
    IterativeSummarizerConfig,
)
from haive.agents.document_modifiers.summarizer.iterative_refinement.state import (
    IterativeSummarizerState,
)


@register_agent(IterativeSummarizerConfig)
class IterativeSummarizer(Agent[IterativeSummarizerConfig]):
    """An agent that summarizes a document iteratively."""

    def __init__(self, config: IterativeSummarizerConfig = IterativeSummarizerConfig()):
        super().__init__(config)

    # We define functions for each node, including a node that generates
    # the initial summary:
    async def generate_initial_summary(
        self, state: IterativeSummarizerState, config: RunnableConfig
    ):
        summary = await self.engines["initial_summary"].ainvoke(
            state.contents[0],
            config,
        )
        return Command(update={"summary": summary, "index": 1})

    # And a node that refines the summary based on the next document
    async def refine_summary(
        self, state: IterativeSummarizerState, config: RunnableConfig
    ):
        content = state.contents[state.index]
        summary = await self.engines["refine_summary"].ainvoke(
            {"existing_answer": state.summary, "context": content},
            config,
        )

        return Command(update={"summary": summary, "index": state.index + 1})

    def setup_workflow(self):
        self.graph.add_node("generate_initial_summary", self.generate_initial_summary)
        self.graph.add_node("refine_summary", self.refine_summary)

        self.graph.add_edge(START, "generate_initial_summary")
        self.graph.add_conditional_edges(
            "generate_initial_summary", self.state_schema.should_refine
        )
        self.graph.add_conditional_edges(
            "refine_summary", self.state_schema.should_refine
        )
