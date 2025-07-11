"""Examples of using the flexible ChainAgent.

Shows different ways to create chains from various node types.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.chain.chain_agent import (
    ChainAgent,
    conditional_chain,
    sequential_chain,
)
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


# Example 1: Simple sequential chain from mixed node types
def example_sequential_mixed():
    """Create a chain from different node types."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Different types of nodes

    # 1. An engine (will be wrapped in SimpleAgent)
    summarizer_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Summarize the following"), ("human", "{text}")]
        ),
        output_key="summary",
    )

    # 2. A callable function
    def process_summary(state):
        summary = state.get("summary", "")
        return {"processed_summary": f"[PROCESSED] {summary}"}

    # 3. An existing agent
    docs = [Document(page_content="Test document")]
    rag_agent = SimpleRAGAgent.from_documents(docs, llm_config)

    # Create chain - ChainAgent figures out how to handle each type
    chain = sequential_chain(
        summarizer_engine,  # Engine -> wrapped in SimpleAgent
        process_summary,  # Callable -> used directly
        rag_agent,  # Agent -> used directly
        name="Mixed Sequential Chain",
    )

    return chain


# Example 2: Using from_mapping for more complex flows
def example_mapped_flow():
    """Create a complex flow using mapping syntax."""
    # Define nodes
    nodes = {
        "input": lambda s: {"processed_input": s.get("input", "")},
        "analyze": lambda s: {
            "complexity": "high" if len(s.get("processed_input", "")) > 50 else "low"
        },
        "simple_process": lambda s: {"result": "Simple processing done"},
        "complex_process": lambda s: {"result": "Complex processing done"},
        "finalize": lambda s: {"final_output": s.get("result", "")},
    }

    # Define flow with mixed syntax
    flow = [
        "input->analyze",  # String syntax for sequential
        (
            "analyze",
            {"low": "simple_process", "high": "complex_process"},
            lambda s: s.get("complexity", "low"),
        ),  # Tuple syntax for conditional
        ("simple_process", "finalize"),  # Tuple syntax for sequential
        ("complex_process", "finalize"),
    ]

    chain = ChainAgent.from_mapping(nodes=nodes, flow=flow, name="Mapped Flow Example")

    return chain


# Example 3: Building a chain incrementally
def example_incremental_building():
    """Build a chain step by step."""
    chain = ChainAgent(name="Incremental Chain")

    # Add nodes one by one
    chain.add_node("start", lambda s: {"step": 1})
    chain.add_node("middle", lambda s: {"step": s.get("step", 0) + 1})
    chain.add_node("branch_a", lambda s: {"result": "Went to A"})
    chain.add_node("branch_b", lambda s: {"result": "Went to B"})
    chain.add_node("end", lambda s: {"final": s.get("result", "")})

    # Add links
    chain.add_link("start", "middle")

    # Add conditional branch
    chain.add_conditional(
        "middle",
        {"a": "branch_a", "b": "branch_b"},
        lambda s: "a" if s.get("step", 0) % 2 == 0 else "b",
    )

    chain.add_link("branch_a", "end")
    chain.add_link("branch_b", "end")

    # Set entry point
    chain.entry_node = "start"

    return chain


# Example 4: Nested chains
def example_nested_chains():
    """Create chains that contain other chains."""
    # Create a sub-chain for processing
    processing_chain = sequential_chain(
        lambda s: {"preprocessed": True},
        lambda s: {"validated": True},
        name="Processing Sub-chain",
    )

    # Create main chain that uses the sub-chain
    main_chain = ChainAgent.from_mapping(
        nodes={
            "input": lambda s: {"data": s.get("input", "")},
            "process": processing_chain,  # Nested chain!
            "output": lambda s: {"result": "Done"},
        },
        flow=["input->process", "process->output"],
        name="Main Chain with Nested Chain",
    )

    return main_chain


# Example 5: RAG Router using ChainAgent
def example_rag_router_simplified():
    """Create a RAG router using the simplified ChainAgent approach."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    docs = [Document(page_content="Test document")]

    # Create strategy selector engine
    strategy_selector = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Analyze query complexity"), ("human", "{query}")]
        ),
        output_key="strategy",
    )

    # Create RAG agents
    simple_rag = SimpleRAGAgent.from_documents(docs, llm_config)

    # Create complex RAG (mock)
    def complex_rag(s):
        return {"response": "Complex RAG response"}

    # Use conditional_chain helper
    router = conditional_chain(
        decider=strategy_selector,
        branches={"simple": simple_rag, "complex": complex_rag},
        condition=lambda s: s.get("strategy", "simple"),
        name="RAG Router",
    )

    return router


# Example 6: Using engines directly
def example_engines_as_nodes():
    """Show how engines can be used directly as nodes."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Create multiple engines
    analyzer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Analyze the input"), ("human", "{input}")]
        ),
        output_key="analysis",
    )

    generator = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Generate response based on analysis"), ("human", "{analysis}")]
        ),
        output_key="response",
    )

    # ChainAgent will automatically wrap these engines
    chain = sequential_chain(analyzer, generator, name="Engine Chain")

    return chain
