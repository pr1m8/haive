# test_node_simple.py

import logging
import uuid
from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field
from rich.console import Console

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.registry import NodeTypeRegistry
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create console for rich output
console = Console()


# Create a class to hold the test state
class TestState:
    embedding_model = None
    vector_store = None
    retriever = None
    analysis_llm = None
    summary_llm = None
    retrieval_node = None
    analysis_node = None
    summary_node = None
    graph = None


state = TestState()


def setup_registry():
    """Initialize and configure the node registry."""
    console.print("Step 1: Initialize Registry", style="bold")
    registry = NodeTypeRegistry.get_instance()

    # Test Command object
    from langgraph.types import Command

    test_cmd = Command(update={"test": "value"}, goto="next")
    console.print(f"Command test: {test_cmd}")
    console.print(f"Command attributes: {dir(test_cmd)}")

    # Force register default processors
    registry.register_default_processors()
    return registry


def create_test_components():
    """Create test components including engines."""
    console.print("\nStep 2: Create Test Components", style="bold")

    # Create embedding model
    state.embedding_model = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    console.print("[green]✓[/green] Created embedding model")

    # Create sample documents
    sample_documents = [
        Document(
            page_content="Machine learning is a subset of artificial intelligence that focuses on data-based learning.",
            metadata={"source": "ML Basics", "date": "2023-01-15"},
        ),
        Document(
            page_content="Neural networks simulate the way the human brain works with interconnected neurons.",
            metadata={"source": "Neural Networks", "date": "2023-02-20"},
        ),
        Document(
            page_content="Deep learning uses multiple layers in neural networks to process complex patterns.",
            metadata={"source": "Deep Learning", "date": "2023-03-10"},
        ),
        Document(
            page_content="Natural language processing enables computers to understand and generate human language.",
            metadata={"source": "NLP", "date": "2023-04-05"},
        ),
    ]

    # Create vector store
    state.vector_store = VectorStoreConfig(
        name="test_vector_store",
        documents=sample_documents,
        vector_store_provider=VectorStoreProvider.FAISS,
        embedding_model=state.embedding_model,
        k=2,
    )
    console.print("[green]✓[/green] Created vector store with sample documents")

    # Create retriever
    state.retriever = VectorStoreRetrieverConfig(
        name="test_retriever",
        id=uuid.uuid4().hex,
        vector_store_config=state.vector_store,
        k=2,
    )
    console.print("[green]✓[/green] Created retriever")

    # Create analysis LLM
    analysis_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You analyze documents and extract key information."),
            (
                "human",
                """
        Please analyze the following documents based on this query: {query}
        
        Context documents:
        {context}
        
        Provide an analysis including:
        - Main topics discussed
        - Key points
        - Sentiment analysis
        - Areas for further research
        """,
            ),
        ]
    )

    # Define the structured output model
    class AnalysisOutput(BaseModel):
        topic: str = Field(description="Main topic of the documents")
        key_points: List[str] = Field(
            description="Key points extracted from the documents"
        )
        sentiment: str = Field(description="Overall sentiment analysis")
        questions: List[str] = Field(description="Questions for further research")

    state.analysis_llm = AugLLMConfig(
        name="document_analyzer",
        id="analysis-llm",
        prompt_template=analysis_prompt,
        structured_output_model=AnalysisOutput,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )
    console.print("[green]✓[/green] Created analysis LLM with structured output model")

    # Create summary LLM
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You summarize technical analyses into concise reports."),
            (
                "human",
                """
        Create a summary report based on this analysis:
        
        Topic: {topic}
        Key Points: {key_points}
        Sentiment: {sentiment}
        Questions: {questions}
        References: {references}
        
        Provide a concise summary of the information.
        """,
            ),
        ]
    )

    state.summary_llm = AugLLMConfig(
        name="summarizer",
        id="summary-llm",
        prompt_template=summary_prompt,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )
    console.print("[green]✓[/green] Created summary LLM")


def create_node_configs():
    """Create the node configurations."""
    console.print("\nStep 3: Create Node Configurations", style="bold")

    # Create retrieval node config
    state.retrieval_config = NodeConfig(
        name="retrieve",
        engine=state.retriever,
        input_mapping={"query": "query"},
        output_mapping={"documents": "context"},
        command_goto="analyze",
        debug=True,
    )
    console.print("[green]✓[/green] Created retrieval node config")

    # Create analysis node config
    state.analysis_config = NodeConfig(
        name="analyze",
        engine=state.analysis_llm,
        input_mapping={"query": "query", "context": "context"},
        output_mapping={
            "analysisoutput.topic": "topic",
            "analysisoutput.key_points": "key_points",
            "analysisoutput.sentiment": "sentiment",
            "analysisoutput.questions": "questions",
        },
        command_goto="summarize",
        debug=True,
    )
    console.print("[green]✓[/green] Created analysis node config")

    # Create summary node config
    state.summary_config = NodeConfig(
        name="summarize", engine=state.summary_llm, command_goto=END, debug=True
    )
    console.print("[green]✓[/green] Created summary node config")


def create_node_functions(registry):
    """Create the node functions from the configurations."""
    console.print("\nStep 4: Create Node Functions", style="bold")

    # Create node functions
    NodeFactory.set_registry(registry)

    # Debug each node creation separately
    state.retrieval_node = create_node_function_safe("retrieve", state.retrieval_config)
    if state.retrieval_node:
        console.print("[green]✓[/green] Created retrieval node function")

    state.analysis_node = create_node_function_safe("analyze", state.analysis_config)
    if state.analysis_node:
        console.print("[green]✓[/green] Created analysis node function")

    state.summary_node = create_node_function_safe("summarize", state.summary_config)
    if state.summary_node:
        console.print("[green]✓[/green] Created summary node function")


def create_node_function_safe(name, config):
    """Safely create a node function with error handling."""
    try:
        return NodeFactory.create_node_function(config)
    except Exception as e:
        console.print(f"[red]Error creating {name} node function: {e}[/red]")
        return None


def create_graph():
    """Create the document analysis graph."""
    console.print("\nStep 5: Create Dynamic Graph", style="bold")

    # Create graph
    state.graph = DynamicGraph(
        name="document_analysis_workflow",
        components=[state.retriever, state.analysis_llm, state.summary_llm],
    )

    # Add nodes
    state.graph.add_node("retrieve", state.retrieval_node)
    state.graph.add_node("analyze", state.analysis_node)
    state.graph.add_node("summarize", state.summary_node)

    # Add edges
    state.graph.add_edge(START, "retrieve")
    state.graph.add_edge("retrieve", "analyze")
    state.graph.add_edge("analyze", "summarize")
    state.graph.add_edge("summarize", END)

    console.print("[green]✓[/green] Created complete analysis graph")

    # Display graph structure
    console.print("\nGraph Structure:")
    console.print("document_analysis_workflow")
    console.print("└── START")
    console.print("    └── retrieve")
    console.print("        └── analyze")
    console.print("            └── summarize")
    console.print("                └── END")


def execute_graph():
    """Execute the graph with a test query."""
    console.print("\nStep 6: Compile and Execute Graph", style="bold")

    # Compile the graph
    compiled_graph = state.graph.compile()
    console.print("[green]✓[/green] Graph compiled successfully")

    # Execute with a test query
    query = "What are the main aspects of AI and machine learning discussed in these documents?"
    console.print(f"\nExecuting with query: {query}")

    try:
        result = compiled_graph.invoke({"query": query})
        console.print("\n[bold green]Execution Result:[/bold green]")
        console.print(result)

        # Show topics
        if result and isinstance(result, dict) and "topic" in result:
            console.print(f"[bold]Topic:[/bold] {result['topic']}")

        # Show key points
        if result and isinstance(result, dict) and "key_points" in result:
            console.print("[bold]Key Points:[/bold]")
            for point in result["key_points"]:
                console.print(f"  • {point}")

        # Show sentiment
        if result and isinstance(result, dict) and "sentiment" in result:
            console.print(f"[bold]Sentiment:[/bold] {result['sentiment']}")

        # Show questions
        if result and isinstance(result, dict) and "questions" in result:
            console.print("[bold]Further Research Questions:[/bold]")
            for question in result["questions"]:
                console.print(f"  • {question}")

        return result
    except Exception as e:
        console.print(f"[red]Error during execution: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return None


def test_individual_nodes():
    """Test each node function individually."""
    console.print("\nStep 7: Test Individual Node Functions", style="bold")

    # Test retrieval node
    console.print("\n[bold]Testing Retrieval Node:[/bold]")
    retrieval_input = {"query": "What is machine learning?"}

    try:
        retrieval_result = state.retrieval_node(retrieval_input)
        console.print("[green]✓[/green] Retrieval successful")

        # Safely examine the retrieval result
        examine_retrieval_result(retrieval_result)
    except Exception as e:
        console.print(f"[red]Retrieval error: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")

    # Test analysis node
    console.print("\n[bold]Testing Analysis Node:[/bold]")

    # Create a sample context for analysis
    sample_context = [
        Document(
            page_content="Machine learning is a branch of AI focused on building systems that learn from data.",
            metadata={"source": "ML Book"},
        ),
        Document(
            page_content="Neural networks consist of layers of interconnected nodes, mimicking the human brain.",
            metadata={"source": "Neural Networks Article"},
        ),
    ]

    analysis_input = {
        "query": "Analyze the key concepts in these documents.",
        "context": sample_context,
    }

    try:
        analysis_result = state.analysis_node(analysis_input)
        console.print("[green]✓[/green] Analysis successful")

        # Safely examine the analysis result
        examine_analysis_result(analysis_result)
    except Exception as e:
        console.print(f"[red]Analysis error: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")

    # Test summary node
    console.print("\n[bold]Testing Summary Node:[/bold]")

    summary_input = {
        "topic": "Machine Learning and Neural Networks",
        "key_points": [
            "Machine learning is a subset of AI",
            "Neural networks mimic the human brain structure",
            "Deep learning uses multiple neural network layers",
        ],
        "sentiment": "Neutral, informative",
        "questions": [
            "How are neural networks trained?",
            "What are the applications of deep learning?",
        ],
        "references": "ML Book, Neural Networks Article",
    }

    try:
        summary_result = state.summary_node(summary_input)
        console.print("[green]✓[/green] Summary successful")

        # Safely examine the summary result
        examine_summary_result(summary_result)
    except Exception as e:
        console.print(f"[red]Summary error: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")


def examine_retrieval_result(retrieval_result):
    """Safely examine a retrieval result."""
    from langgraph.types import Command

    console.print(f"[dim]Result type: {type(retrieval_result)}[/dim]")

    # Handle Command objects
    if isinstance(retrieval_result, Command):
        console.print(f"[dim]Command goto: {retrieval_result.goto}[/dim]")

        # Check update attribute
        console.print(
            f"[dim]Command has update: {hasattr(retrieval_result, 'update')}[/dim]"
        )

        # Handle update as attribute or method
        if hasattr(retrieval_result, "update"):
            is_callable = callable(retrieval_result.update)
            console.print(f"[dim]Update is callable: {is_callable}[/dim]")

            if is_callable:
                # Try to call update() method
                try:
                    update_data = retrieval_result.update()
                    console.print(
                        f"[dim]Update() returned type: {type(update_data)}[/dim]"
                    )
                except Exception as e:
                    console.print(f"[red]Error calling update(): {e}[/red]")
                    update_data = {}
            else:
                # Access as regular attribute
                update_data = retrieval_result.update

            # Display context documents
            if isinstance(update_data, dict) and "context" in update_data:
                docs = update_data["context"]
                console.print(f"[bold]Retrieved {len(docs)} documents[/bold]")
                for i, doc in enumerate(docs):
                    source = doc.metadata.get("source", "Unknown")
                    content = (
                        doc.page_content[:50] + "..."
                        if len(doc.page_content) > 50
                        else doc.page_content
                    )
                    console.print(f"  {i}. [italic]{source}[/italic]: {content}")
    else:
        # Not a Command object
        console.print("[dim]Result is not a Command object[/dim]")
        console.print(f"[dim]Result attributes: {dir(retrieval_result)}[/dim]")


def examine_analysis_result(analysis_result):
    """Safely examine an analysis result."""
    from langgraph.types import Command

    console.print(f"[dim]Result type: {type(analysis_result)}[/dim]")

    # Handle Command objects
    if isinstance(analysis_result, Command):
        console.print(f"[dim]Command goto: {analysis_result.goto}[/dim]")

        # Check update attribute
        console.print(
            f"[dim]Command has update: {hasattr(analysis_result, 'update')}[/dim]"
        )

        # Handle update as attribute or method
        if hasattr(analysis_result, "update"):
            is_callable = callable(analysis_result.update)
            console.print(f"[dim]Update is callable: {is_callable}[/dim]")

            if is_callable:
                # Try to call update() method
                try:
                    update_data = analysis_result.update()
                    console.print(
                        f"[dim]Update() returned type: {type(update_data)}[/dim]"
                    )
                except Exception as e:
                    console.print(f"[red]Error calling update(): {e}[/red]")
                    update_data = {}
            else:
                # Access as regular attribute
                update_data = analysis_result.update

            # Display analysis results
            if isinstance(update_data, dict):
                console.print("[bold]Analysis Results:[/bold]")
                for key, value in update_data.items():
                    if isinstance(value, str):
                        display_value = (
                            value[:100] + "..." if len(value) > 100 else value
                        )
                        console.print(f"  [italic]{key}[/italic]: {display_value}")
                    elif isinstance(value, list):
                        console.print(f"  [italic]{key}[/italic]:")
                        for item in value[:3]:  # Show first 3 items
                            display_item = (
                                str(item)[:80] + "..."
                                if len(str(item)) > 80
                                else str(item)
                            )
                            console.print(f"    • {display_item}")
                        if len(value) > 3:
                            console.print(f"    • ... ({len(value) - 3} more)")
                    else:
                        console.print(
                            f"  [italic]{key}[/italic]: {str(value)[:100]}..."
                        )
    else:
        # Not a Command object
        console.print("[dim]Result is not a Command object[/dim]")
        console.print(f"[dim]Result attributes: {dir(analysis_result)}[/dim]")


def examine_summary_result(summary_result):
    """Safely examine a summary result."""
    from langgraph.types import Command

    console.print(f"[dim]Result type: {type(summary_result)}[/dim]")

    # Handle Command objects
    if isinstance(summary_result, Command):
        console.print(f"[dim]Command goto: {summary_result.goto}[/dim]")

        # Check update attribute
        console.print(
            f"[dim]Command has update: {hasattr(summary_result, 'update')}[/dim]"
        )

        # Handle update as attribute or method
        if hasattr(summary_result, "update"):
            is_callable = callable(summary_result.update)
            console.print(f"[dim]Update is callable: {is_callable}[/dim]")

            if is_callable:
                # Try to call update() method
                try:
                    update_data = summary_result.update()
                    console.print(
                        f"[dim]Update() returned type: {type(update_data)}[/dim]"
                    )
                except Exception as e:
                    console.print(f"[red]Error calling update(): {e}[/red]")
                    update_data = {}
            else:
                # Access as regular attribute
                update_data = summary_result.update

            # Display summary results
            if isinstance(update_data, dict):
                console.print("[bold]Summary Results:[/bold]")
                for key, value in update_data.items():
                    if isinstance(value, str):
                        display_value = (
                            value[:150] + "..." if len(value) > 150 else value
                        )
                        console.print(f"  [italic]{key}[/italic]: {display_value}")
                    else:
                        console.print(
                            f"  [italic]{key}[/italic]: {str(value)[:100]}..."
                        )
    else:
        # Not a Command object
        console.print("[dim]Result is not a Command object[/dim]")
        console.print(f"[dim]Result attributes: {dir(summary_result)}[/dim]")


# Main execution
console.print("╭───────────────────────────╮")
console.print("│ Advanced Node System Test │")
console.print("╰───────────────────────────╯")

# Run test steps
registry = setup_registry()
create_test_components()
create_node_configs()
create_node_functions(registry)
create_graph()
execute_graph()
test_individual_nodes()

console.print("\nAdvanced Testing Complete", style="bold green")
