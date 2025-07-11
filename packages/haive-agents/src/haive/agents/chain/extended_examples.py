"""Examples using ExtendedChainAgent for super easy chain building."""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.chain.extended_chain import (
    ChainBuilder,
    ExtendedChainAgent,
    chain,
    chain_with_edges,
)
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


def example_simple_sequential():
    """Simplest possible chain - just list the nodes."""
    # Just list your nodes - that's it!
    my_chain = chain(
        lambda s: {"step": 1},
        lambda s: {"step": s.get("step", 0) + 1},
        lambda s: {"result": f"Final step: {s.get('step', 0)}"},
    )

    return my_chain


def example_with_agents_and_engines():
    """Mix different node types effortlessly."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Create different node types
    analyzer_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Analyze the query"), ("human", "{query}")]
        ),
        output_key="analysis",
    )

    docs = [Document(page_content="Test document")]
    rag_agent = SimpleRAGAgent.from_documents(docs, llm_config)

    def post_processor(s):
        return {"final": s.get("response", "")}

    # Just chain them together!
    my_chain = chain(
        analyzer_engine, rag_agent, post_processor  # Engine  # Agent  # Callable
    )

    return my_chain


def example_custom_edges():
    """Use custom edges with easy syntax."""
    nodes = [
        lambda s: {"value": 1},  # 0
        lambda s: {"value": 2},  # 1
        lambda s: {"value": 3},  # 2
        lambda s: {"sum": "all"},  # 3
    ]

    # Create non-sequential flow
    my_chain = chain_with_edges(
        nodes,
        "0->1",  # node 0 to node 1
        "0->2",  # node 0 also to node 2 (parallel)
        "1->3",  # node 1 to node 3
        "2->3",  # node 2 to node 3
    )

    return my_chain


def example_with_branching():
    """Easy branching syntax."""

    def classifier(s):
        return {"type": "complex" if len(s.get("input", "")) > 50 else "simple"}

    def simple_processor(s):
        return {"result": "Simple processing"}

    def complex_processor(s):
        return {"result": "Complex processing"}

    def finalizer(s):
        return {"output": s.get("result", "")}

    # Method 1: Using branch() method
    my_chain = (
        ExtendedChainAgent.from_list([classifier])
        .branch(
            lambda s: s.get("type", "simple"),
            simple=simple_processor,
            complex=complex_processor,
        )
        .add_edge("node_1->node_3")  # simple to finalizer
        .add_edge("node_2->node_3")  # complex to finalizer
        .node_list.append(finalizer)
    )

    # Method 2: Using edge tuples
    my_chain = chain_with_edges(
        [classifier, simple_processor, complex_processor, finalizer],
        "0->1",  # Default path
        ("0", {"simple": "1", "complex": "2"}, lambda s: s.get("type")),
        "1->3",
        "2->3",
    )

    return my_chain


def example_with_loop():
    """Easy loop creation."""

    def counter(s):
        return {"count": s.get("count", 0) + 1}

    # Create a chain with a loop
    my_chain = ExtendedChainAgent.from_list([counter]).loop(
        condition=lambda s: s.get("count", 0) < 5, max_iterations=10
    )

    return my_chain


def example_rag_router_super_simple():
    """RAG router in the simplest possible way."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    docs = [Document(page_content="Test document")]

    # Create nodes
    analyzer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Classify query complexity as 'simple' or 'complex'"),
                ("human", "{query}"),
            ]
        ),
        output_key="complexity",
    )

    simple_rag = SimpleRAGAgent.from_documents(docs, llm_config)

    def complex_rag(s):
        return {"response": "Complex RAG response"}

    # Build the router
    router = chain_with_edges(
        [analyzer, simple_rag, complex_rag],
        ("0", {"simple": "1", "complex": "2"}, lambda s: s.get("complexity", "simple")),
    )

    return router


def example_start_and_end():
    """Using START and END explicitly."""
    nodes = [
        lambda s: {"initialized": True},
        lambda s: {"processed": True},
        lambda s: {"finalized": True},
    ]

    my_chain = chain_with_edges(
        nodes,
        "start->0",  # Explicit START connection
        "0->1",
        "1->2",
        "2->end",  # Explicit END connection
    )

    return my_chain


def example_operator_chaining():
    """Using operator syntax for chaining."""

    # This would need more implementation, but shows the idea
    def input_node(s):
        return {"data": s.get("input", "")}

    def process_node(s):
        return {"processed": True}

    def output_node(s):
        return {"result": "Done"}

    # Using >> operator
    my_chain = ChainBuilder(input_node) >> process_node >> output_node

    return my_chain.build()


def example_mixed_indices_and_names():
    """Mix numeric indices and node names."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Some nodes have names
    analyzer = SimpleAgent(
        engine=AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages([("human", "{input}")]),
            output_key="analysis",
        ),
        name="analyzer",  # Named node
    )

    def processor(s):
        return {"processed": True}  # Unnamed - will be node_1

    my_chain = chain_with_edges(
        [analyzer, processor], "analyzer->1", "1->end"  # Mix name and index
    )

    return my_chain
