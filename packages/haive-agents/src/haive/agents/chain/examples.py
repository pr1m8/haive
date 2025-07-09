"""Examples of using DeclarativeChainAgent to build complex RAG flows

Shows how to recreate our complex agents using declarative specifications.
"""

from typing import Any, Dict

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain.declarative_chain import (
    BranchSpec,
    ChainBuilder,
    ChainSpec,
    LoopSpec,
    NodeSpec,
    SequenceSpec,
)
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


# Example 1: Recreate Agentic RAG Router using declarative chain
def create_agentic_router_declarative(documents: list[Document]):
    """Create an agentic RAG router using declarative chain building."""

    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Strategy selection node
    class StrategyDecision(BaseModel):
        strategy: str = Field(description="Selected strategy")
        confidence: float = Field(description="Confidence")

    strategy_selector = SimpleAgent(
        engine=AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Select RAG strategy: simple, multi_query, or hyde"),
                    ("human", "{query}"),
                ]
            ),
            structured_output_model=StrategyDecision,
            output_key="strategy_decision",
        ),
        name="StrategySelector",
    )

    # RAG strategy agents
    simple_rag = SimpleRAGAgent.from_documents(documents, llm_config)
    multi_query_rag = MultiQueryRAGAgent.from_documents(documents, llm_config)
    hyde_rag = HyDERAGAgentV2.from_documents(documents, llm_config)

    # Synthesis node
    synthesizer = SimpleAgent(
        engine=AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [("system", "Synthesize the results"), ("human", "{response}")]
            ),
            output_key="final_response",
        ),
        name="Synthesizer",
    )

    # Build declaratively
    chain = (
        ChainBuilder("Agentic RAG Router")
        # Add all nodes
        .add_node("select_strategy", strategy_selector)
        .add_node("simple_rag", simple_rag)
        .add_node("multi_query_rag", multi_query_rag)
        .add_node("hyde_rag", hyde_rag)
        .add_node("synthesize", synthesizer)
        # Define the flow
        .add_sequence("select_strategy")  # Start with strategy selection
        # Branch based on selected strategy
        .add_branch(
            from_node="select_strategy",
            condition=lambda state: state.get("strategy_decision", {}).get(
                "strategy", "simple"
            ),
            branches={
                "simple": "simple_rag",
                "multi_query": "multi_query_rag",
                "hyde": "hyde_rag",
            },
            default="simple_rag",
        )
        # All strategies flow to synthesis
        .add_sequence("simple_rag", "synthesize")
        .add_sequence("multi_query_rag", "synthesize")
        .add_sequence("hyde_rag", "synthesize")
        .build()
    )

    return chain


# Example 2: Recreate Query Planning RAG using declarative chain
def create_query_planning_declarative(documents: list[Document]):
    """Create a query planning RAG using declarative chain building."""

    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Define nodes as callables
    def create_plan(state: Dict[str, Any]) -> Dict[str, Any]:
        """Create query execution plan."""
        # Simplified - would use LLM to decompose query
        return {
            "sub_queries": ["What is X?", "How does Y work?", "Compare X and Y"],
            "current_index": 0,
        }

    def execute_sub_query(state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one sub-query."""
        sub_queries = state.get("sub_queries", [])
        current_index = state.get("current_index", 0)

        if current_index < len(sub_queries):
            # Execute the sub-query (simplified)
            result = f"Answer to: {sub_queries[current_index]}"

            # Update state
            results = state.get("sub_results", [])
            results.append(result)

            return {
                "sub_results": results,
                "current_index": current_index + 1,
                "continue_loop": current_index + 1 < len(sub_queries),
            }

        return {"continue_loop": False}

    def synthesize_results(state: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all sub-query results."""
        sub_results = state.get("sub_results", [])
        return {
            "final_response": f"Synthesized answer from {len(sub_results)} sub-queries"
        }

    # Build declaratively with a loop
    chain = (
        ChainBuilder("Query Planning RAG")
        # Add nodes
        .add_node("create_plan", create_plan, node_type="callable")
        .add_node("execute_sub_query", execute_sub_query, node_type="callable")
        .add_node("synthesize", synthesize_results, node_type="callable")
        # Define the flow with a loop
        .add_sequence("create_plan", "execute_sub_query")
        # Loop to execute all sub-queries
        .add_loop(
            start_node="execute_sub_query",
            end_node="execute_sub_query",
            condition="continue_loop",  # Check state.continue_loop
            max_iterations=10,
        )
        # After loop completes, synthesize
        .add_sequence("execute_sub_query", "synthesize")
        .build()
    )

    return chain


# Example 3: Recreate Self-Reflective RAG using declarative chain
def create_self_reflective_declarative(documents: list[Document]):
    """Create a self-reflective RAG using declarative chain building."""

    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Initial answer generator
    initial_generator = SimpleAgent(
        engine=AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [("system", "Generate initial answer"), ("human", "{query}")]
            ),
            output_key="current_answer",
        ),
        name="InitialGenerator",
    )

    # Reflection nodes
    def reflect_and_critique(state: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on answer quality."""
        # Simplified - would use LLM to critique
        quality_score = 0.7  # Mock score
        iterations = state.get("iterations", 0)

        return {
            "quality_score": quality_score,
            "iterations": iterations + 1,
            "needs_improvement": quality_score < 0.85 and iterations < 3,
        }

    def improve_answer(state: Dict[str, Any]) -> Dict[str, Any]:
        """Improve the answer based on critique."""
        # Simplified - would use LLM to improve
        current = state.get("current_answer", "")
        return {"current_answer": f"{current} [Improved]", "improvement_made": True}

    def finalize_answer(state: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize the answer."""
        return {
            "final_response": state.get("current_answer", ""),
            "total_iterations": state.get("iterations", 0),
        }

    # Build with reflection loop
    chain = (
        ChainBuilder("Self-Reflective RAG")
        # Add nodes
        .add_node("generate_initial", initial_generator)
        .add_node("reflect", reflect_and_critique, node_type="callable")
        .add_node("improve", improve_answer, node_type="callable")
        .add_node("finalize", finalize_answer, node_type="callable")
        # Define flow
        .add_sequence("generate_initial", "reflect")
        # Branch based on reflection
        .add_branch(
            from_node="reflect",
            condition="needs_improvement",
            branches={True: "improve", False: "finalize"},
        )
        # Loop back from improve to reflect
        .add_sequence("improve", "reflect")
        .build()
    )

    return chain


# Example 4: Using raw ChainSpec for maximum control
def create_complex_flow_from_spec():
    """Create a complex flow using raw ChainSpec."""

    # Define nodes
    nodes = [
        NodeSpec(
            name="input_processor",
            node=lambda s: {"processed": True},
            node_type="callable",
        ),
        NodeSpec(
            name="analyzer",
            node=lambda s: {"analysis": "complete"},
            node_type="callable",
        ),
        NodeSpec(
            name="branch_decider", node=lambda s: {"path": "A"}, node_type="callable"
        ),
        NodeSpec(
            name="path_a", node=lambda s: {"result": "A done"}, node_type="callable"
        ),
        NodeSpec(
            name="path_b", node=lambda s: {"result": "B done"}, node_type="callable"
        ),
        NodeSpec(name="merger", node=lambda s: {"merged": True}, node_type="callable"),
    ]

    # Define sequences
    sequences = [
        SequenceSpec(nodes=["input_processor", "analyzer", "branch_decider"]),
        SequenceSpec(nodes=["path_a", "merger"]),
        SequenceSpec(nodes=["path_b", "merger"]),
    ]

    # Define branches
    branches = [
        BranchSpec(
            from_node="branch_decider",
            condition=lambda state: state.get("path", "A"),
            branches={"A": "path_a", "B": "path_b"},
            default="path_a",
        )
    ]

    # Create spec
    spec = ChainSpec(
        nodes=nodes,
        sequences=sequences,
        branches=branches,
        entry_point="START",
        exit_points=["END"],
    )

    # Create agent
    return DeclarativeChainAgent(name="Complex Flow", chain_spec=spec)


# Example 5: Simplified syntax with method chaining
def create_rag_with_fallback():
    """Create a RAG with fallback strategies."""

    return (
        ChainBuilder("RAG with Fallback")
        # Try primary RAG
        .add_node("primary_rag", lambda s: {"success": False, "response": ""})
        .add_node("check_success", lambda s: s)
        .add_node("fallback_rag", lambda s: {"response": "Fallback answer"})
        .add_node("use_primary", lambda s: s)
        # Flow
        .add_sequence("primary_rag", "check_success")
        # Branch on success
        .add_branch(
            "check_success", "success", {True: "use_primary", False: "fallback_rag"}
        )
        .build()
    )
