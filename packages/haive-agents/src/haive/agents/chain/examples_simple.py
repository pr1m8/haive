"""Simple examples of using ChainAgent.

Shows how easy it is to build chains.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.chain import ChainAgent, flow, flow_with_edges
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


# Example 1: Simplest possible - just functions
def example_basic():
    """Just list your nodes."""
    chain = flow(
        lambda s: {"step": 1},
        lambda s: {"step": s.get("step", 0) + 1},
        lambda s: {"result": f"Final: {s.get('step')}"},
    )

    return chain


# Example 2: Mix agents and engines
def example_mixed():
    """Mix different node types."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # An engine
    summarizer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Summarize the text"), ("human", "{text}")]
        ),
        output_key="summary",
    )

    # An agent
    docs = [Document(page_content="Test document")]
    rag = SimpleRAGAgent.from_documents(docs, llm_config)

    # A function
    def formatter(s):
        return {"output": f"Summary: {s.get('summary', '')}"}

    # Just chain them!
    chain = flow(summarizer, rag, formatter)

    return chain


# Example 3: Custom routing
def example_routing():
    """Custom edges for complex flows."""
    nodes = [
        lambda s: {
            "type": "A" if len(s.get("input", "")) > 10 else "B"
        },  # 0: classifier
        lambda s: {"result": "Process A"},  # 1: process_a
        lambda s: {"result": "Process B"},  # 2: process_b
        lambda s: {"final": s.get("result", "")},  # 3: finalizer
    ]

    chain = flow_with_edges(
        nodes,
        # Conditional routing from classifier
        (0, {"A": 1, "B": 2}, lambda s: s.get("type", "B")),
        "1->3",  # process_a to finalizer
        "2->3",  # process_b to finalizer
    )

    return chain


# Example 4: Using ChainAgent directly
def example_direct():
    """Using ChainAgent class directly."""
    # Initialize with nodes
    chain = ChainAgent(
        lambda s: {"value": 1},
        lambda s: {"value": s.get("value", 0) * 2},
        lambda s: {"value": s.get("value", 0) + 10},
    )
    # Auto-creates edges: 0->1->2

    return chain


# Example 5: Building incrementally
def example_incremental():
    """Build step by step."""
    chain = ChainAgent()  # Empty chain

    # Add nodes one by one
    chain.add(lambda s: {"count": 0})
    chain.add(lambda s: {"count": s.get("count", 0) + 1})

    # Branch based on count
    chain.branch(
        lambda s: "high" if s.get("count", 0) > 5 else "low",
        high=lambda s: {"result": "Count is high"},
        low=lambda s: {"result": "Count is low"},
    )

    return chain


# Example 6: RAG router in 5 lines
def example_rag_router():
    """Complete RAG router - super simple."""
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    docs = [Document(page_content="Test document")]

    # That's it - a complete router!
    router = flow_with_edges(
        [
            # 0: Classify query
            AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ChatPromptTemplate.from_messages(
                    [
                        ("system", "Output 'simple' or 'complex' based on query"),
                        ("human", "{query}"),
                    ]
                ),
                output_key="type",
            ),
            # 1: Simple RAG
            SimpleRAGAgent.from_documents(docs, llm_config),
            # 2: Complex processing (mock)
            lambda s: {"response": "Complex processing done"},
        ],
        # Route based on classification
        (0, {"simple": 1, "complex": 2}, lambda s: s.get("type", "simple")),
    )

    return router
