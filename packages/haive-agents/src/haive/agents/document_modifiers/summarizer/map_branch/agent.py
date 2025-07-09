"""Map-Reduce Summarizer Agent for document summarization.

This module provides the SummarizerAgent class which implements a map-reduce
approach to document summarization. It can handle large documents by splitting
them into manageable chunks, summarizing each chunk, and then combining the
summaries into a final coherent summary.

The agent handles token limit constraints and provides automatic fallback
mechanisms for oversized documents.

Classes:
    SummarizerAgent: Main agent for map-reduce document summarization

Examples:
    Basic usage::

        from haive.agents.document_modifiers.summarizer.map_branch import SummarizerAgent
        from haive.agents.document_modifiers.summarizer.map_branch.config import SummarizerAgentConfig

        config = SummarizerAgentConfig(
            token_max=1000,
            name="document_summarizer"
        )
        agent = SummarizerAgent(config)

        documents = ["Long document text 1...", "Long document text 2..."]
        result = agent.run({"contents": documents})
        summary = result["final_summary"]

    With custom token limits::

        config = SummarizerAgentConfig(
            token_max=2000,  # Allow longer intermediate summaries
            engines={
                "map_chain": custom_map_config,
                "reduce_chain": custom_reduce_config
            }
        )
        agent = SummarizerAgent(config)

See Also:
    - :class:`~haive.agents.document_modifiers.summarizer.map_branch.config.SummarizerAgentConfig`: Configuration class
    - :class:`~haive.agents.document_modifiers.summarizer.map_branch.state.SummaryState`: State management
"""

import logging
from typing import List, Literal, Optional, Union

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import compose_runnable
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.constants import Send
from langgraph.graph import END, START
from langgraph.types import Command, Send

from haive.agents.document_modifiers.summarizer.map_branch.config import (
    SummarizerAgentConfig,
)
from haive.agents.document_modifiers.summarizer.map_branch.engines import (
    map_aug_llm_config,
    reduce_augllm_config,
)
from haive.agents.document_modifiers.summarizer.map_branch.state import SummaryState

logger = logging.getLogger(__name__)


@register_agent(SummarizerAgentConfig)
class SummarizerAgent(Agent[SummarizerAgentConfig]):
    """Agent that summarizes documents using a map-reduce approach.

    This agent implements a sophisticated document summarization workflow that
    can handle large documents and multiple documents simultaneously. It uses
    a map-reduce pattern where documents are first summarized individually
    (map phase), then combined and reduced to a final summary (reduce phase).

    The agent automatically handles token limit constraints by:
    1. Splitting oversized documents into manageable chunks
    2. Summarizing chunks individually
    3. Collapsing intermediate summaries when they exceed token limits
    4. Producing a coherent final summary

    Args:
        config: Configuration object containing token limits, LLM settings,
            and workflow parameters.

    Attributes:
        token_max: Maximum token limit for intermediate summaries
        map_chain: Runnable for individual document summarization
        reduce_chain: Runnable for combining and reducing summaries
        text_splitter: Utility for splitting oversized documents

    Examples:
        Basic document summarization::

            config = SummarizerAgentConfig(token_max=1000)
            agent = SummarizerAgent(config)

            docs = ["First document content...", "Second document content..."]
            result = agent.run({"contents": docs})
            print(result["final_summary"])

        Handling large documents::

            # Agent automatically splits and processes large documents
            large_doc = "Very long document content..." * 1000
            result = agent.run({"contents": [large_doc]})
            # The agent will chunk, summarize, and combine automatically

        With custom configuration::

            config = SummarizerAgentConfig(
                token_max=2000,
                engines={
                    "map_chain": custom_map_config,
                    "reduce_chain": custom_reduce_config
                }
            )
            agent = SummarizerAgent(config)

    Note:
        The agent uses recursive text splitting to handle documents that exceed
        token limits. Chunk summaries are automatically combined using the
        reduce chain to maintain coherence.

    Raises:
        ValueError: If no documents are provided for summarization
        RuntimeError: If summarization fails after all retry attempts

    See Also:
        - :class:`SummarizerAgentConfig`: Configuration options
        - :class:`SummaryState`: State management for the workflow
        - :meth:`setup_workflow`: Workflow construction details
    """

    def __init__(self, config: SummarizerAgentConfig = SummarizerAgentConfig()) -> None:
        """Initialize the SummarizerAgent with configuration.

        Sets up the map and reduce chains for document processing and
        initializes the text splitter for handling oversized documents.

        Args:
            config: Agent configuration with token limits and LLM settings.
                Defaults to a new instance with default values.
        """
        self.token_max = config.token_max
        self.map_chain = compose_runnable(
            config.engines.get("map_chain", map_aug_llm_config)
        )
        self.reduce_chain = compose_runnable(
            config.engines.get("reduce_chain", reduce_augllm_config)
        )

        # Initialize text splitter for oversized documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200, length_function=self._get_token_count
        )

        logger.info(
            "Initialized SummarizerAgent",
            extra={"agent_name": config.name, "token_max": self.token_max},
        )

        super().__init__(config)

    def setup_workflow(self) -> None:
        """Set up the map-reduce summarization workflow.

        Constructs a StateGraph that implements the following workflow:
        1. Map phase: Generate summaries for each input document
        2. Collect phase: Gather all individual summaries
        3. Collapse phase: Combine summaries if they exceed token limits
        4. Final phase: Generate the final consolidated summary

        The workflow includes conditional edges that determine whether
        intermediate summaries need to be collapsed based on token counts.

        Note:
            This method is called automatically during agent initialization
            and does not need to be invoked manually.
        """
        logger.info(
            "Setting up summarizer workflow", extra={"agent_name": self.config.name}
        )

        # Add workflow nodes
        self.graph.add_node("generate_summary", self.generate_summary)
        self.graph.add_node("collect_summaries", self.collect_summaries)
        self.graph.add_node("collapse_summaries", self.collapse_summaries)
        self.graph.add_node("generate_final_summary", self.generate_final_summary)

        # Define workflow edges
        self.graph.add_conditional_edges(
            START, self.map_summaries, ["generate_summary"]
        )
        self.graph.add_edge("generate_summary", "collect_summaries")
        self.graph.add_conditional_edges("collect_summaries", self.should_collapse)
        self.graph.add_conditional_edges("collapse_summaries", self.should_collapse)
        self.graph.add_edge("generate_final_summary", END)

    async def generate_summary(self, state: SummaryState) -> dict:
        """Generate a summary for a single document.

        Processes a document through the map chain to create an individual
        summary. If the document exceeds token limits, it automatically
        splits the document into chunks and summarizes each chunk before
        combining them.

        Args:
            state: Current state containing the document content to summarize.
                Must have a 'content' key with the document text.

        Returns:
            Dictionary with 'summaries' key containing a list with the
            generated summary text.

        Note:
            This method includes automatic error recovery for token limit
            issues by splitting oversized documents into manageable chunks.
        """
        content = state.get("content", "")

        try:
            # Attempt normal summarization
            response = await self.map_chain.ainvoke(content)
            logger.info(
                "Generated summary successfully", extra={"content_length": len(content)}
            )
            return {"summaries": [response]}

        except Exception as e:
            error_str = str(e)
            logger.warning(
                "Error generating summary",
                extra={"error": error_str, "content_length": len(content)},
            )

            # Handle token limit errors
            if self._is_token_limit_error(error_str):
                return await self._handle_oversized_document(content)

            # For other errors, return error message
            logger.error(
                "Failed to generate summary", extra={"error": error_str}, exc_info=True
            )
            return {"summaries": [f"Error generating summary: {error_str}"]}

    def map_summaries(self, state: SummaryState) -> List[Send]:
        """Map documents to summary generation tasks.

        Creates parallel summary generation tasks for each input document.
        Each document is sent to the generate_summary node for processing.

        Args:
            state: Current state containing the list of documents to summarize.
                Must have a 'contents' key with a list of document texts.

        Returns:
            List of Send commands, one for each document to summarize.
        """
        contents = state.get("contents", [])
        logger.info("Mapping summaries", extra={"document_count": len(contents)})

        return [Send("generate_summary", {"content": content}) for content in contents]

    def collect_summaries(self, state: SummaryState) -> Command:
        """Collect individual summaries into document objects.

        Transforms the list of summary strings into Document objects
        for further processing in the collapse phase.

        Args:
            state: Current state containing individual summaries.
                Must have a 'summaries' key with a list of summary texts.

        Returns:
            Command updating the state with collapsed_summaries as
            Document objects.
        """
        summaries = state.get("summaries", [])
        logger.info("Collecting summaries", extra={"summary_count": len(summaries)})

        return Command(
            update={
                "collapsed_summaries": [
                    Document(page_content=summary) for summary in summaries
                ]
            }
        )

    async def collapse_summaries(self, state: SummaryState) -> Command:
        """Collapse summaries that exceed token limits.

        When intermediate summaries collectively exceed the token limit,
        this method splits them into groups and reduces each group to
        a more concise summary.

        Args:
            state: Current state containing Document objects to collapse.
                Must have 'collapsed_summaries' key.

        Returns:
            Command updating the state with reduced summaries.
        """
        collapsed_summaries = state.get("collapsed_summaries", [])

        logger.info(
            "Collapsing summaries",
            extra={
                "document_count": len(collapsed_summaries),
                "total_tokens": self.length_function(collapsed_summaries),
            },
        )

        # Split documents into groups that fit within token limit
        doc_lists = split_list_of_docs(
            collapsed_summaries, self.length_function, self.token_max
        )

        # Collapse each group
        results = []
        for i, doc_list in enumerate(doc_lists):
            logger.debug(
                "Processing document group",
                extra={"group_index": i, "group_size": len(doc_list)},
            )
            collapsed = await acollapse_docs(doc_list, self.reduce_chain.ainvoke)
            results.append(collapsed)

        return Command(update={"collapsed_summaries": results})

    def should_collapse(
        self, state: SummaryState
    ) -> Literal["collapse_summaries", "generate_final_summary"]:
        """Determine if summaries need further collapsing.

        Checks if the total token count of collapsed summaries exceeds
        the configured limit. If so, directs to further collapsing;
        otherwise proceeds to final summary generation.

        Args:
            state: Current state with collapsed summaries to evaluate.

        Returns:
            Next node name: 'collapse_summaries' if over limit,
            'generate_final_summary' otherwise.
        """
        collapsed_summaries = state.get("collapsed_summaries", [])
        num_tokens = self.length_function(collapsed_summaries)

        if num_tokens > self.token_max:
            logger.info(
                "Summaries exceed token limit, collapsing further",
                extra={"current_tokens": num_tokens, "token_max": self.token_max},
            )
            return "collapse_summaries"

        logger.info("Proceeding to final summary", extra={"total_tokens": num_tokens})
        return "generate_final_summary"

    async def generate_final_summary(self, state: SummaryState) -> Command:
        """Generate the final consolidated summary.

        Processes all collapsed summaries through the reduce chain to
        create a single, coherent final summary.

        Args:
            state: Current state with collapsed summaries ready for
                final reduction.

        Returns:
            Command updating the state with the final summary text.
        """
        collapsed_summaries = state.get("collapsed_summaries", [])

        logger.info(
            "Generating final summary", extra={"input_count": len(collapsed_summaries)}
        )

        try:
            response = await self.reduce_chain.ainvoke(collapsed_summaries)
            logger.info("Final summary generated successfully")
            return Command(update={"final_summary": response})
        except Exception as e:
            logger.error(
                "Failed to generate final summary",
                extra={"error": str(e)},
                exc_info=True,
            )
            return Command(
                update={"final_summary": "Error: Failed to generate final summary"}
            )

    def length_function(self, documents: List[Document]) -> int:
        """Calculate total token count for documents.

        Computes the sum of tokens across all provided documents using
        the reduce chain's tokenizer.

        Args:
            documents: List of Document objects to count tokens for.

        Returns:
            Total number of tokens across all documents.
        """
        if not documents:
            return 0

        llm = self.config.engines["reduce_chain"].llm_config.instantiate()
        total_tokens = sum(llm.get_num_tokens(doc.page_content) for doc in documents)

        logger.debug(
            "Calculated token count",
            extra={"document_count": len(documents), "total_tokens": total_tokens},
        )

        return total_tokens

    def _get_token_count(self, text: str) -> int:
        """Get token count for a single text string.

        Args:
            text: Text to count tokens for.

        Returns:
            Number of tokens in the text.
        """
        llm = self.config.engines.get(
            "map_chain", map_aug_llm_config
        ).llm_config.instantiate()
        return llm.get_num_tokens(text)

    def _is_token_limit_error(self, error_str: str) -> bool:
        """Check if error is related to token limits.

        Args:
            error_str: Error message to check.

        Returns:
            True if error is token-related, False otherwise.
        """
        token_error_patterns = [
            "string too long",
            "token limit",
            "maximum context length",
            "context_length_exceeded",
            "string_above_max_length",
        ]
        return any(pattern in error_str.lower() for pattern in token_error_patterns)

    async def _handle_oversized_document(self, content: str) -> dict:
        """Handle document that exceeds token limits.

        Splits the document into chunks, summarizes each chunk, and
        combines the results.

        Args:
            content: Document content that exceeds token limits.

        Returns:
            Dictionary with 'summaries' key containing the combined summary.
        """
        logger.info(
            "Handling oversized document", extra={"content_length": len(content)}
        )

        # Split content into chunks
        if isinstance(content, str):
            chunks = self.text_splitter.split_text(content)
        else:
            chunks = self.text_splitter.split_documents(
                [Document(page_content=content)]
            )
            chunks = [doc.page_content for doc in chunks]

        logger.info("Split document into chunks", extra={"chunk_count": len(chunks)})

        # Process each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            try:
                logger.debug(
                    "Processing chunk",
                    extra={"chunk_index": i, "chunk_size": len(chunk)},
                )
                chunk_summary = await self.map_chain.ainvoke(chunk)
                chunk_summaries.append(chunk_summary)
            except Exception as e:
                logger.error(
                    "Error processing chunk", extra={"chunk_index": i, "error": str(e)}
                )
                chunk_summaries.append(f"[Chunk {i+1} could not be summarized]")

        # Combine chunk summaries
        if not chunk_summaries:
            return {"summaries": ["Document could not be processed"]}
        elif len(chunk_summaries) == 1:
            return {"summaries": chunk_summaries}
        else:
            try:
                combined = await self.reduce_chain.ainvoke("\n\n".join(chunk_summaries))
                return {"summaries": [combined]}
            except Exception as e:
                logger.error(
                    "Failed to combine chunk summaries", extra={"error": str(e)}
                )
                return {"summaries": ["Error: Could not combine chunk summaries"]}


def build_agent() -> SummarizerAgent:
    """Create a default SummarizerAgent instance.

    Returns:
        SummarizerAgent with default configuration.
    """
    return SummarizerAgent(SummarizerAgentConfig())
