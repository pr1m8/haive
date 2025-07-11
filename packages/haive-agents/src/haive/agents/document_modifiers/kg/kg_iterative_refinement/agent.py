"""Iterative Knowledge Graph Transformer Agent.

This module provides the IterativeGraphTransformer class which builds knowledge
graphs iteratively from a sequence of documents. It processes documents one by one,
starting with an initial graph and refining it with each subsequent document.

The agent is particularly useful for building comprehensive knowledge graphs from
multiple related documents where later documents may add detail or context to
earlier information.

Classes:
    IterativeGraphTransformer: Main agent for iterative knowledge graph construction

Examples:
    Basic usage::

        from haive.agents.document_modifiers.kg.kg_iterative_refinement import IterativeGraphTransformer
        from haive.agents.document_modifiers.kg.kg_iterative_refinement.config import IterativeGraphTransformerConfig

        config = IterativeGraphTransformerConfig()
        agent = IterativeGraphTransformer(config)

        documents = [
            "Marie Curie was a physicist born in Poland.",
            "She won two Nobel Prizes in different fields.",
            "Her daughter Irène also won a Nobel Prize."
        ]
        result = agent.run({"contents": documents})
        graph = result["graph_doc"]

    With custom configuration::

        config = IterativeGraphTransformerConfig(
            name="research_graph_builder",
            engines={"transformer": custom_llm_config}
        )
        agent = IterativeGraphTransformer(config)

See Also:
    - :class:`~haive.agents.document_modifiers.kg.kg_iterative_refinement.config.IterativeGraphTransformerConfig`: Configuration class
    - :class:`~haive.agents.document_modifiers.kg.kg_iterative_refinement.state.IterativeGraphTransformerState`: State management
"""

import logging
from typing import Any, Dict, Optional

from haive.core.engine.agent.agent import Agent, register_agent
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START
from langgraph.types import Command

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.agents.document_modifiers.kg.kg_iterative_refinement.config import (
    IterativeGraphTransformerConfig,
)
from haive.agents.document_modifiers.kg.kg_iterative_refinement.state import (
    IterativeGraphTransformerState,
)
from haive.agents.document_modifiers.kg.kg_iterative_refinement.utils import (
    replace_empty_placeholders,
)

logger = logging.getLogger(__name__)


@register_agent(IterativeGraphTransformerConfig)
class IterativeGraphTransformer(Agent[IterativeGraphTransformerConfig]):
    """Agent that builds knowledge graphs iteratively from documents.

    This agent processes a sequence of documents to build a comprehensive
    knowledge graph. It starts by creating an initial graph from the first
    document, then iteratively refines and expands the graph with information
    from subsequent documents.

    The iterative approach allows the agent to:
    1. Build context progressively
    2. Resolve entity references across documents
    3. Accumulate relationships and properties
    4. Maintain graph coherence throughout the process

    Args:
        config: Configuration object containing agent settings and LLM
            configuration for the graph transformer.

    Attributes:
        llm_graph_transformer: The underlying GraphTransformer instance
            used to convert documents to graph representations.

    Examples:
        Processing a series of related documents::

            agent = IterativeGraphTransformer()
            docs = [
                "Einstein developed the theory of relativity.",
                "The theory of relativity revolutionized physics.",
                "Einstein received the Nobel Prize in 1921."
            ]
            result = agent.run({"contents": docs})

            # Access the final knowledge graph
            graph = result["graph_doc"]
            nodes = graph.nodes  # List of entities
            relationships = graph.relationships  # List of connections

        With strict mode for validation::

            config = IterativeGraphTransformerConfig(
                strict_mode=True,  # Enforce schema validation
                ignore_tool_usage=False  # Allow tool-based extraction
            )
            agent = IterativeGraphTransformer(config)

    Note:
        The agent processes documents sequentially, so document order can
        affect the final graph structure. Consider ordering documents from
        general to specific for best results.

    Raises:
        ValueError: If no documents are provided for processing
        TypeError: If document content is not in a supported format

    See Also:
        - :class:`GraphTransformer`: The underlying graph transformation engine
        - :meth:`generate_initial_summary`: Initial graph creation
        - :meth:`refine_summary`: Graph refinement process
    """

    def __init__(
        self,
        config: IterativeGraphTransformerConfig = IterativeGraphTransformerConfig(),
    ) -> None:
        """Initialize the iterative graph transformer.

        Sets up the graph transformer instance that will be used to
        process documents into knowledge graph representations.

        Args:
            config: Agent configuration with transformer settings.
                Defaults to a new instance with default values.
        """
        self.llm_graph_transformer = GraphTransformer()

        logger.info(
            "Initialized IterativeGraphTransformer", extra={"agent_name": config.name}
        )

        super().__init__(config)

    def generate_initial_summary(
        self, state: IterativeGraphTransformerState, config: RunnableConfig
    ) -> Command:
        """Generate the initial knowledge graph from the first document.

        Creates the foundational graph structure from the first document
        in the sequence. This graph will be iteratively refined with
        subsequent documents.

        Args:
            state: Current state containing the list of documents to process.
                Must have at least one document in the 'contents' field.
            config: Runtime configuration for the operation.

        Returns:
            Command updating the state with the initial graph_doc and
            incrementing the index to 1.

        Note:
            The state normalizes various input formats (str, dict, Document)
            to Document objects before processing.
        """
        if not state.contents:
            logger.error("No documents provided for graph generation")
            raise ValueError("At least one document is required")

        doc = state.contents[0]

        logger.info(
            "Generating initial knowledge graph",
            extra={
                "document_length": (
                    len(doc.page_content) if hasattr(doc, "page_content") else 0
                )
            },
        )

        # Transform first document to graph
        graph_docs = self.llm_graph_transformer.transform_documents(
            documents=[doc],
            strict_mode=True,
            ignore_tool_usage=True,
        )

        if not graph_docs:
            logger.warning("No graph generated from initial document")
            return Command(update={"graph_doc": None, "index": 1})

        graph_doc = graph_docs[0]
        logger.info(
            "Initial graph generated",
            extra={
                "node_count": (
                    len(graph_doc.nodes) if hasattr(graph_doc, "nodes") else 0
                ),
                "relationship_count": (
                    len(graph_doc.relationships)
                    if hasattr(graph_doc, "relationships")
                    else 0
                ),
            },
        )

        return Command(update={"graph_doc": graph_doc, "index": 1})

    def refine_summary(
        self, state: IterativeGraphTransformerState, config: RunnableConfig
    ) -> Command:
        """Refine the knowledge graph with information from the next document.

        Takes the existing graph and integrates new information from the
        current document. The refinement process preserves existing knowledge
        while adding new entities, relationships, and properties.

        Args:
            state: Current state containing the existing graph and remaining
                documents. Must have a valid index pointing to the next document.
            config: Runtime configuration for the operation.

        Returns:
            Command updating the state with the refined graph_doc and
            incrementing the index.

        Raises:
            IndexError: If the index is out of bounds for the contents list.
            TypeError: If the content at the current index is not a valid type.
        """
        if state.index >= len(state.contents):
            logger.error(
                "Index out of bounds",
                extra={"index": state.index, "content_length": len(state.contents)},
            )
            raise IndexError(f"Index {state.index} out of bounds")

        content = state.contents[state.index]

        logger.info(
            "Refining knowledge graph",
            extra={
                "document_index": state.index,
                "current_graph_nodes": (
                    len(state.graph_doc.nodes)
                    if state.graph_doc and hasattr(state.graph_doc, "nodes")
                    else 0
                ),
            },
        )

        # Create refinement prompt
        refine_template = PromptTemplate.from_template(
            """\
        Produce a refined knowledge graph by integrating new information.

        Existing graph:
        {existing_answer}

        New context:
        ------------
        {context}
        ------------

        Given the new context, refine and expand the original graph.
        Preserve existing valid information while adding new entities and relationships.
        """
        ).format(
            existing_answer=str(state.graph_doc) if state.graph_doc else "Empty graph",
            context=content.page_content,
        )

        # Clean up template
        refine_template = replace_empty_placeholders(refine_template)

        # Transform with refinement instructions
        try:
            graph_docs = self.llm_graph_transformer.transform_documents(
                documents=[content],
                strict_mode=True,
                ignore_tool_usage=True,
                additional_instructions=refine_template,
            )

            if not graph_docs:
                logger.warning(
                    "No graph generated during refinement",
                    extra={"document_index": state.index},
                )
                # Keep existing graph and move to next document
                return Command(update={"index": state.index + 1})

            refined_graph = graph_docs[0]
            logger.info(
                "Graph refined successfully",
                extra={
                    "new_node_count": (
                        len(refined_graph.nodes)
                        if hasattr(refined_graph, "nodes")
                        else 0
                    ),
                    "new_relationship_count": (
                        len(refined_graph.relationships)
                        if hasattr(refined_graph, "relationships")
                        else 0
                    ),
                },
            )

            return Command(
                update={"graph_doc": refined_graph, "index": state.index + 1}
            )

        except Exception as e:
            logger.error(
                "Failed to refine graph",
                extra={"error": str(e), "document_index": state.index},
                exc_info=True,
            )
            # Keep existing graph and move to next document
            return Command(update={"index": state.index + 1})

    def setup_workflow(self) -> None:
        """Set up the iterative graph building workflow.

        Constructs a StateGraph that implements the following workflow:
        1. Generate initial graph from the first document
        2. Iteratively refine the graph with each subsequent document
        3. Continue until all documents have been processed

        The workflow uses conditional edges to determine when to stop
        refining based on the number of documents processed.

        Note:
            This method is called automatically during agent initialization
            and does not need to be invoked manually.
        """
        logger.info(
            "Setting up iterative graph transformer workflow",
            extra={"agent_name": self.config.name},
        )

        # Add workflow nodes
        self.graph.add_node("generate_initial_summary", self.generate_initial_summary)
        self.graph.add_node("refine_summary", self.refine_summary)

        # Define workflow edges
        self.graph.add_edge(START, "generate_initial_summary")

        # Conditional routing based on remaining documents
        self.graph.add_conditional_edges(
            "generate_initial_summary", self.state_schema.should_refine
        )
        self.graph.add_conditional_edges(
            "refine_summary", self.state_schema.should_refine
        )


def build_agent() -> IterativeGraphTransformer:
    """Create a default IterativeGraphTransformer instance.

    Returns:
        IterativeGraphTransformer with default configuration.
    """
    return IterativeGraphTransformer(IterativeGraphTransformerConfig())
