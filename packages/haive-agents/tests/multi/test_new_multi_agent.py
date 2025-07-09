#!/usr/bin/env python3
"""Test the new multi-agent implementation with RAG agents and branching.

This demonstrates:
- Sequential multi-agent with RAG + Answer agents
- Conditional multi-agent with branching based on document relevance
- Parallel multi-agent execution
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.fixtures.documents import conversation_documents
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import ConditionalAgent, ParallelAgent, SequentialAgent
from haive.agents.rag.base.agent import SimpleRAGAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Define prompts
RAG_ANSWER_SYSTEM_PROMPT = """
You are part of a RAG workflow where your job is to answer whether the documents 
retrieved answer the original query.
"""

RAG_ANSWER_HUMAN_PROMPT = """
Query: {query}
Retrieved Documents: {retrieved_documents}
"""

RAG_ANSWER_BASE_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [("system", RAG_ANSWER_SYSTEM_PROMPT), ("human", RAG_ANSWER_HUMAN_PROMPT)]
)

# Additional prompts for branching
VALIDATION_PROMPT = """
Based on the retrieved documents, determine if they are relevant to the query.
Return "relevant" if the documents answer the query, "not_relevant" if they don't.
"""

REFINE_QUERY_PROMPT = """
The retrieved documents were not relevant to the original query.
Please refine the query to be more specific.

Original query: {query}
Retrieved documents: {retrieved_documents}

Provide a refined query that might yield better results.
"""


def test_sequential_rag():
    """Test sequential RAG workflow."""
    print("=" * 80)
    print("TEST 1: Sequential RAG Agent")
    print("=" * 80)

    # Create agents
    rag_agent = SimpleRAGAgent.from_documents(conversation_documents)
    answer_agent = SimpleAgent(
        name="Answer Agent",
        engine=AugLLMConfig(prompt_template=RAG_ANSWER_BASE_PROMPT_TEMPLATE),
    )

    # Create sequential multi-agent
    seq_agent = SequentialAgent(
        name="RAG Answer Pipeline", agents=[rag_agent, answer_agent]
    )

    # Visualize structure
    seq_agent.visualize_structure()

    # Test execution
    try:
        seq_agent.compile()
        print("\n✅ Sequential agent compiled successfully!")

        # For sequential agents, we need to provide the correct input structure
        result = seq_agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="What restaurants were discussed in the conversation?"
                    )
                ],
                "query": "What restaurants were discussed in the conversation?",
            }
        )
        print("\nResult:", result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


def test_conditional_rag():
    """Test conditional RAG with branching based on relevance."""
    print("\n" + "=" * 80)
    print("TEST 2: Conditional RAG with Branching")
    print("=" * 80)

    # Create agents
    rag_agent = SimpleRAGAgent.from_documents(conversation_documents)

    # Validation agent to check relevance
    validation_agent = SimpleAgent(
        name="Validation Agent", engine=AugLLMConfig(system_message=VALIDATION_PROMPT)
    )

    # Answer agent for relevant docs
    answer_agent = SimpleAgent(
        name="Answer Agent",
        engine=AugLLMConfig(prompt_template=RAG_ANSWER_BASE_PROMPT_TEMPLATE),
    )

    # Query refinement agent for non-relevant docs
    refine_agent = SimpleAgent(
        name="Refine Query Agent",
        engine=AugLLMConfig(system_message=REFINE_QUERY_PROMPT),
    )

    # Create conditional multi-agent
    cond_agent = ConditionalAgent(
        name="Smart RAG Pipeline",
        agents=[rag_agent, validation_agent, answer_agent, refine_agent],
    )

    # Add conditional routing
    def check_relevance(state: dict[str, Any]) -> str:
        """Check if documents are relevant."""
        # In real implementation, this would parse validation agent output
        validation_result = state.get("agent_outputs", {}).get(validation_agent.id, {})

        # Simple heuristic for demo
        if isinstance(validation_result, dict):
            content = (
                validation_result.get("messages", [])[-1].content
                if validation_result.get("messages")
                else ""
            )
        else:
            content = str(validation_result)

        if "relevant" in content.lower() and "not" not in content.lower():
            return "answer"
        return "refine"

    # Configure branching
    cond_agent.add_conditional_edge(
        source_agent=validation_agent,
        condition=check_relevance,
        destinations={"answer": answer_agent, "refine": refine_agent},
    )

    # Visualize structure
    cond_agent.visualize_structure()

    # Test execution
    try:
        cond_agent.compile()
        print("\n✅ Conditional agent compiled successfully!")

        # For conditional agents, we need to provide the correct input structure
        result = cond_agent.run(
            {
                "messages": [HumanMessage(content="What restaurants were discussed?")],
                "query": "What restaurants were discussed?",
            }
        )
        print("\nResult:", result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


def test_parallel_agents():
    """Test parallel agent execution."""
    print("\n" + "=" * 80)
    print("TEST 3: Parallel Agent Execution")
    print("=" * 80)

    # Create tool for math operations
    @tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers"""
        return a + b

    @tool
    def multiply(a: int, b: int) -> int:
        """Returns the product of two numbers"""
        return a * b

    # Create multiple agents with different capabilities
    class Plan(BaseModel):
        steps: list[str] = Field(description="list of steps")

    planner_agent = SimpleAgent(
        name="Planner",
        engine=AugLLMConfig(
            structured_output_model=Plan, structured_output_version="v2"
        ),
    )

    calculator_agent = ReactAgent(
        name="Calculator", engine=AugLLMConfig(tools=[add, multiply])
    )

    summarizer_agent = SimpleAgent(
        name="Summarizer",
        engine=AugLLMConfig(system_message="Summarize the results from other agents"),
    )

    # Create parallel multi-agent
    parallel_agent = ParallelAgent(
        name="Parallel Processing System",
        agents=[planner_agent, calculator_agent, summarizer_agent],
    )

    # Visualize structure
    parallel_agent.visualize_structure()

    # Test execution
    try:
        parallel_agent.compile()
        print("\n✅ Parallel agent compiled successfully!")

        result = parallel_agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="Plan how to calculate (5 + 3) * 2 and then do it"
                    )
                ]
            }
        )
        print("\nResult:", result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


def test_custom_branching():
    """Test custom branching with loops."""
    print("\n" + "=" * 80)
    print("TEST 4: Custom Branching with Retry Logic")
    print("=" * 80)

    # This would demonstrate more complex routing patterns
    # Including loops, retries, and dynamic routing

    class CustomBranchingAgent(ConditionalAgent):
        """Custom agent with retry logic."""

        def build_custom_graph(self, graph):
            # Would implement custom graph building here
            # For now, use default conditional building
            return super()._build_conditional_graph(graph)

    # Create agents
    attempt_agent = SimpleAgent(
        name="Attempt Agent",
        engine=AugLLMConfig(system_message="Try to answer the query"),
    )

    validator_agent = SimpleAgent(
        name="Validator",
        engine=AugLLMConfig(system_message="Validate if the answer is complete"),
    )

    retry_agent = SimpleAgent(
        name="Retry Agent",
        engine=AugLLMConfig(system_message="Improve the previous answer"),
    )

    # Create custom agent
    custom_agent = CustomBranchingAgent(
        name="Retry Pipeline", agents=[attempt_agent, validator_agent, retry_agent]
    )

    # Add branching with potential loop back
    def check_complete(state: dict[str, Any]) -> str:
        """Check if answer is complete."""
        # Simple demo logic
        retry_count = state.get("meta_state", {}).get("error_count", 0)
        if retry_count >= 2:
            return "complete"
        return "retry"

    custom_agent.add_conditional_edge(
        source_agent=validator_agent,
        condition=check_complete,
        destinations={"complete": "END", "retry": retry_agent},
    )

    # Loop back from retry to attempt
    custom_agent.add_conditional_edge(
        source_agent=retry_agent,
        condition=lambda s: "attempt",
        destinations={"attempt": attempt_agent},
    )

    # Visualize structure
    custom_agent.visualize_structure()

    print("\n✅ Custom branching agent created with retry logic")


if __name__ == "__main__":
    # Run tests
    test_sequential_rag()
    test_conditional_rag()
    test_parallel_agents()
    test_custom_branching()

    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
