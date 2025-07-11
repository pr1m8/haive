import logging
from typing import Any

from haive.core.engine.agent.agent import register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.llm_rag.config import LLMRAGConfig

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(LLMRAGConfig)
class LLMRAGAgent(BaseRAGAgent):
    """LLM-enhanced RAG agent that retrieves documents and generates answers.

    This agent extends the base RAG workflow:
    1. Receive a query
    2. Retrieve relevant documents (handled by BaseRAGAgent)
    3. Check if the documents are relevant to the query
    4. Generate an answer based on the documents if relevant
    """

    def setup_workflow(self) -> None:
        """Set up the dynamic workflow for the LLM RAG agent.

        Creates a graph that extends the base RAG workflow with additional
        functionality for checking relevance and generating answers.
        """
        # Get engines from the config
        retriever_engine = self.config.retriever_config
        llm_engine = self.config.llm_config
        relevance_checker = self.config.relevance_checker_config

        # Debug: Log component details
        logger.info("Setting up LLM RAG workflow with components:")
        logger.info(f"- Retriever: {retriever_engine.name}")
        logger.info(f"- LLM: {llm_engine.name}")
        logger.info(
            f"- Relevance Checker: {relevance_checker.name if relevance_checker else 'None'}"
        )

        # Create a dynamic graph builder with all components
        components = [retriever_engine, llm_engine]
        if relevance_checker:
            components.append(relevance_checker)

        graph_builder = DynamicGraph(
            name=f"{self.config.name}_workflow",
            components=components,
            state_schema=self.config.state_schema,
            input_schema=self.config.input_schema,
            output_schema=self.config.output_schema,
        )

        # Use the base RAG agent as a subgraph
        # This leverages the parent's create_runnable method to create the retrieval functionality
        base_rag_subgraph = super().create_runnable()

        # Define function to invoke the base RAG subgraph
        def retrieve_documents(state):
            logger.info(
                f"Invoking base RAG for document retrieval with query: '{state.query}'"
            )
            try:
                # Invoke the base RAG agent as a subgraph
                result = base_rag_subgraph.invoke(state)
                logger.info(
                    f"Retrieved {len(result.get('retrieved_documents', []))} documents"
                )

                # Pass the result to the relevance checker
                return Command(
                    # No need to update state since the subgraph already did that
                    goto="check_relevance"
                )
            except Exception as e:
                logger.exception(f"Error in document retrieval: {e}")
                return Command(
                    update={"error": str(e)},
                    goto="check_relevance",  # Still try to proceed
                )

        # Define a function to check document relevance
        def check_relevance(state):
            logger.info(
                f"Checking relevance of {len(state.retrieved_documents)} documents"
            )

            # If no documents retrieved, mark as not relevant
            if not state.retrieved_documents:
                logger.info("No documents retrieved, marking as not relevant")
                return Command(update={"is_relevant": False}, goto="generate_answer")

            try:
                # Format documents for relevance check
                documents_text = format_documents(state.retrieved_documents)

                # Prepare the input for the relevance checker
                relevance_input = {"query": state.query, "documents": documents_text}

                # Invoke the relevance checker LLM
                result = relevance_checker.invoke(relevance_input)

                # Parse the result to determine relevance
                is_relevant = parse_relevance_result(result)
                logger.info(f"Relevance check result: {is_relevant}")

                return Command(
                    update={"is_relevant": is_relevant}, goto="generate_answer"
                )
            except Exception as e:
                logger.exception(f"Error in relevance checker: {e}")
                return Command(
                    update={"is_relevant": False, "error": str(e)},
                    goto="generate_answer",
                )

        # Define a function to generate an answer
        def generate_answer(state):
            logger.info(f"Generating answer with relevance: {state.is_relevant}")

            try:
                # If documents aren't relevant, provide a standard response
                if not state.is_relevant:
                    return Command(
                        update={
                            "answer": "The retrieved documents are not relevant to the question."
                        },
                        goto=END,
                    )

                # Format documents for the LLM
                context = format_documents(state.retrieved_documents)

                # Prepare the input for the LLM
                llm_input = {"query": state.query, "context": context}

                # Invoke the LLM
                result = llm_engine.invoke(llm_input)

                # Extract the answer from the result
                answer = extract_answer(result)
                logger.info(f"Generated answer: {answer[:100]}...")

                return Command(update={"answer": answer}, goto=END)
            except Exception as e:
                logger.exception(f"Error in answer generation: {e}")
                return Command(
                    update={
                        "answer": f"Error generating answer: {e!s}",
                        "error": str(e),
                    },
                    goto=END,
                )

        # Add nodes to the graph
        graph_builder.add_node("retrieve_documents", retrieve_documents)

        if relevance_checker:
            graph_builder.add_node("check_relevance", check_relevance)
        else:
            # If no relevance checker, add a passthrough node
            def default_relevance(state):
                return Command(
                    update={"is_relevant": bool(state.retrieved_documents)},
                    goto="generate_answer",
                )

            graph_builder.add_node("check_relevance", default_relevance)

        graph_builder.add_node("generate_answer", generate_answer)

        # Set workflow edges
        graph_builder.add_edge(START, "retrieve_documents")
        graph_builder.add_edge("retrieve_documents", "check_relevance")

        # Build the graph
        self.graph = graph_builder.build()

        logger.info(f"LLM RAG workflow set up for {self.config.name}")


# Utility functions


def format_documents(documents: list[Any]) -> str:
    """Format a list of documents into a text string for LLM input.
    Handles both Document objects and strings.
    """
    formatted_texts = []

    for i, doc in enumerate(documents):
        if hasattr(doc, "page_content"):
            # Handle Document objects
            text = doc.page_content
        elif isinstance(doc, str):
            # Handle string documents
            text = doc
        else:
            # Try to convert to string
            text = str(doc)

        # Clean up the text
        text = text.replace("\n\n", " ").replace("  ", " ").strip()
        formatted_texts.append(f"[{i+1}] {text}")

    return "\n\n".join(formatted_texts)


def parse_relevance_result(result: Any) -> bool:
    """Parse the output from the relevance checker to determine if documents are relevant."""
    if isinstance(result, dict):
        # Check for various possible response formats
        if "output" in result:
            result = result["output"]
        elif "answer" in result:
            result = result["answer"]
        elif "text" in result:
            result = result["text"]
        elif "content" in result:
            result = result["content"]

    # Convert to string if needed
    if not isinstance(result, str):
        result = str(result)

    # Parse the response text
    result = result.strip().lower()

    # Check for explicit yes/no
    if result == "yes" or result.startswith("yes,"):
        return True
    if result == "no" or result.startswith("no,"):
        return False

    # Look for yes/no in the text
    if "yes" in result[:20]:  # Check beginning of response
        return True
    if "no" in result[:20]:
        return False

    # Default to true if we can't determine
    return True


def extract_answer(result: Any) -> str:
    """Extract the answer string from an LLM result, which could be in various formats."""
    if isinstance(result, str):
        return result.strip()

    if isinstance(result, dict):
        # Check for various possible response formats
        if "output" in result:
            return result["output"].strip()
        if "answer" in result:
            return result["answer"].strip()
        if "text" in result:
            return result["text"].strip()
        if "content" in result:
            return result["content"].strip()

    # If all else fails, convert to string
    return str(result).strip()
