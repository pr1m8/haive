"""Taxonomy generation agent implementation.

This module implements an agent that generates taxonomies from conversation histories
through an iterative process of document summarization, clustering, and refinement.
It uses LLM-based processing at each step to generate high-quality taxonomies.

The agent follows these main steps:
1. Document summarization
2. Minibatch creation
3. Initial taxonomy generation
4. Iterative taxonomy refinement
5. Final taxonomy review

Example:
    Basic usage of the taxonomy agent::

        config = TaxonomyAgentConfig(
            state_schema=TaxonomyGenerationState,
            visualize=True,
            name="TaxonomyAgent"
        )
        agent = TaxonomyAgent(config)
        result = agent.run(input_data={"documents": [...]})
"""

import random
from typing import Any

from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.runnables import (
    RunnableConfig,
    RunnableLambda,
    RunnablePassthrough,
)

# from haive_agents.tnt.utils import invoke_taxonomy_chain
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field

from haive.agents.document_modifiers.tnt.branches import should_review
from haive.agents.document_modifiers.tnt.engines import (
    summary_aug_llm_config,
    taxonomy_generation_aug_llm_config,
    taxonomy_review_aug_llm_config,
    taxonomy_update_aug_llm_config,
)
from haive.agents.document_modifiers.tnt.state import TaxonomyGenerationState
from haive.agents.document_modifiers.tnt.utils import format_docs, format_taxonomy


# FR
class TaxonomyAgentConfig(AgentConfig):
    """Agent configuration for generating a taxonomy from conversation history."""

    state_schema: TaxonomyGenerationState = Field(
        default=TaxonomyGenerationState,
        description="The state of the taxonomy generation.",
    )
    visualize: bool = Field(default=True, description="Whether to visualize the agent.")
    name: str = Field(default="TaxonomyAgent", description="The name of the agent.")
    # TODO: This should be a RunnableConfig
    runtime_config: dict[str, Any] = Field(
        default_factory=lambda: {
            "configurable": {
                "use_case": (
                    "Generate a taxonomy for labeling user intent and identifying required documentation "
                    "(references, how-tos, etc.) that benefit the user."
                ),
                "batch_size": 400,
                "suggestion_length": 30,
                "cluster_name_length": 10,
                "cluster_description_length": 30,
                "explanation_length": 20,
                "max_num_clusters": 25,
                "num_minibatches": 10,
                "thread_id": "thread-1",
            },
            "max_concurrency": 2,
        },
        description="The runtime configuration of the agent.",
    )


@register_agent(TaxonomyAgentConfig)
class TaxonomyAgent(Agent[TaxonomyAgentConfig]):
    """Agent that generates a taxonomy from a conversation history."""

    def __init__(self, config: TaxonomyAgentConfig):
        """Initialize the taxonomy agent."""
        self._setup_map_reduce_chain()
        super().__init__(config)
        # self.graph = StateGraph(TaxonomyGenerationState)

        # self.setup_workflow()

    def _setup_map_reduce_chain(self):
        """Sets up the map-reduce chain for summarization."""
        self.summary_chain = summary_aug_llm_config.create_runnable()

        def wrap_content(state: TaxonomyGenerationState):
            """Ensures correct input format for RunnablePassthrough."""
            return {"documents": [{"content": doc.content} for doc in state.documents]}

        def batch_summaries(input_dict: dict):
            """Ensure batch function receives a list."""
            return self.summary_chain.batch(input_dict["documents"])  # Fix: Passes list

        self.map_step = RunnableLambda(
            func=wrap_content
        ) | RunnablePassthrough.assign(  # Wraps content in a dictionary  # Assigns summaries key in dict
            summaries=RunnableLambda(func=batch_summaries)  # Fix: Uses wrapped function
        )

        self.map_reduce_chain = self.map_step | self.reduce_summaries

    def get_content(self, state: TaxonomyGenerationState):
        """Extracts document content for processing."""
        return [{"content": doc["content"]} for doc in state["documents"]]

    def reduce_summaries(self, combined: dict) -> TaxonomyGenerationState:
        """Reduces summarized documents into a structured format."""
        summaries = combined.get("summaries", [])
        documents = combined.get("documents", [])

        # DEBUG: Print types and values
        print(f"DEBUG: Type of summaries -> {type(summaries)}")
        print(f"DEBUG: Type of documents -> {type(documents)}")
        print(f"DEBUG: First summary -> {summaries[0] if summaries else 'EMPTY'}")
        print(f"DEBUG: First document -> {documents[0] if documents else 'EMPTY'}")

        return Command(
            update={
                "documents": [
                    {
                        "id": doc.get("id", "UNKNOWN_ID"),  # Handle missing key
                        "content": doc.get(
                            "content", "UNKNOWN_CONTENT"
                        ),  # Handle missing key
                        "summary": summ_info.get("summary", "NO_SUMMARY"),
                        "explanation": summ_info.get("explanation", "NO_EXPLANATION"),
                    }
                    for doc, summ_info in zip(documents, summaries, strict=False)
                ]
            }
        )

    def invoke_taxonomy_chain(
        self,
        chain_config: AugLLMConfig,
        state: TaxonomyGenerationState,
        config: RunnableConfig,
        mb_indices: list[int],
    ) -> TaxonomyGenerationState:
        """Invokes the taxonomy LLM to generate or refine taxonomies.

        Args:
            chain (Runnable): LLM pipeline for taxonomy generation.
            state (TaxonomyGenerationState): Current taxonomy state.
            config (RunnableConfig): Configurable parameters.
            mb_indices (List[int]): Indices of documents to process in this iteration.

        Returns:
            TaxonomyGenerationState: Updated state with new taxonomy clusters.
        """
        configurable = config["configurable"]
        docs = state.documents
        minibatch = [docs[idx] for idx in mb_indices]
        data_table_xml = format_docs(minibatch)

        previous_taxonomy = state.clusters[-1] if state.clusters else []
        cluster_table_xml = format_taxonomy(previous_taxonomy)
        chain = taxonomy_generation_aug_llm_config.create_runnable()
        updated_taxonomy = chain.invoke(
            {
                "data_xml": data_table_xml,
                "use_case": configurable["use_case"],
                "cluster_table_xml": cluster_table_xml,
                "suggestion_length": configurable.get("suggestion_length", 30),
                "cluster_name_length": configurable.get("cluster_name_length", 10),
                "cluster_description_length": configurable.get(
                    "cluster_description_length", 30
                ),
                "explanation_length": configurable.get("explanation_length", 20),
                "max_num_clusters": configurable.get("max_num_clusters", 25),
            }
        )

        return Command(
            update={
                "clusters": [updated_taxonomy["clusters"]],
            }
        )
        # Markdown(format_taxonomy_md(step["__end__"]["clusters"][-1]))

    def get_minibatches(self, state: TaxonomyGenerationState, config: RunnableConfig):
        """Splits documents into minibatches for iterative taxonomy generation.

        Args:
            state (TaxonomyGenerationState): The current state containing documents.
            config (RunnableConfig): Configuration object specifying batch size.

        Returns:
            dict: Dictionary with a 'minibatches' key containing grouped document indices.
        """
        batch_size = config["configurable"].get("batch_size", 200)
        indices = list(range(len(state.documents)))
        random.shuffle(indices)

        if len(indices) < batch_size:
            return Command(update={"minibatches": [indices]})

        num_full_batches = len(indices) // batch_size
        batches = [
            indices[i * batch_size : (i + 1) * batch_size]
            for i in range(num_full_batches)
        ]

        if leftovers := len(indices) % batch_size:
            last_batch = indices[num_full_batches * batch_size :]
            elements_to_add = batch_size - leftovers
            last_batch += random.sample(indices, elements_to_add)
            batches.append(last_batch)

        return Command(update={"minibatches": batches})

    def review_taxonomy(
        self, state: TaxonomyGenerationState, config: RunnableConfig
    ) -> TaxonomyGenerationState:
        """Evaluates the final taxonomy after all updates.

        Args:
            state (TaxonomyGenerationState): The current state with completed taxonomies.
            config (RunnableConfig): Configuration settings.

        Returns:
            TaxonomyGenerationState: Updated state with reviewed taxonomy.
        """
        batch_size = config["configurable"].get("batch_size", 200)
        indices = list(range(len(state.documents)))
        random.shuffle(indices)
        return self.invoke_taxonomy_chain(
            taxonomy_review_aug_llm_config, state, config, indices[:batch_size]
        )

    def update_taxonomy(
        self, state: TaxonomyGenerationState, config: RunnableConfig
    ) -> TaxonomyGenerationState:
        """Iteratively refines the taxonomy using new minibatches of data.

        Args:
            state (TaxonomyGenerationState): The current state containing previous taxonomies.
            config (RunnableConfig): Configuration settings.

        Returns:
            TaxonomyGenerationState: Updated state with revised taxonomy clusters.
        """
        print(f"DEBUG: Type of clusters -> {type(state.clusters)}")
        print(
            f"DEBUG: First cluster -> {state.clusters[0] if state.clusters else 'EMPTY'}"
        )

        # Ensure clusters is a list of lists
        if not isinstance(state.clusters, list):
            state.clusters = []
        elif isinstance(state.clusters, dict):
            state.clusters = [list(state.clusters.values())]  # Convert dict to list

        which_mb = len(state.clusters) % len(state.minibatches)
        return self.invoke_taxonomy_chain(
            taxonomy_update_aug_llm_config, state, config, state.minibatches[which_mb]
        )

    def generate_taxonomy(
        self, state: TaxonomyGenerationState, config: RunnableConfig
    ) -> TaxonomyGenerationState:
        """Generates an initial taxonomy from the first document minibatch.

        Args:
            state (TaxonomyGenerationState): The current state of the taxonomy process.
            config (RunnableConfig): Configuration for the taxonomy generation.

        Returns:
            TaxonomyGenerationState: Updated state with the initial taxonomy.
        """
        return self.invoke_taxonomy_chain(
            taxonomy_generation_aug_llm_config, state, config, state.minibatches[0]
        )

    def setup_workflow(self):
        """Sets up the taxonomy generation workflow in LangGraph."""
        self.graph.add_node("summarize", self.map_reduce_chain)
        self.graph.add_node("get_minibatches", self.get_minibatches)
        self.graph.add_node("generate_taxonomy", self.generate_taxonomy)
        self.graph.add_node("update_taxonomy", self.update_taxonomy)
        self.graph.add_node("review_taxonomy", self.review_taxonomy)

        self.graph.add_edge("summarize", "get_minibatches")
        self.graph.add_edge("get_minibatches", "generate_taxonomy")
        self.graph.add_edge("generate_taxonomy", "update_taxonomy")
        self.graph.add_conditional_edges(
            "update_taxonomy",
            should_review,
            {
                "update_taxonomy": "update_taxonomy",
                "review_taxonomy": "review_taxonomy",
            },
        )
        self.graph.add_edge("review_taxonomy", END)
        self.graph.add_edge(START, "summarize")
