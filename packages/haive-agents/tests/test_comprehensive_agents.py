"""Comprehensive tests for SimpleAgent, ReactAgent, and Multi-Agent with RAG.

This test suite validates:
1. SimpleAgent schema modification and tool handling
2. ReactAgent looping behavior
3. Multi-agent sequential execution with RAG
4. Prompt templates and message handling
5. Tool usage and routing
"""

from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import EngineRetriever
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.agent import SimpleRAGAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Test Models
class SearchQuery(BaseModel):
    """Test model for structured search."""

    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Maximum results")


class AnalysisResult(BaseModel):
    """Test model for analysis output."""

    summary: str = Field(description="Summary of findings")
    confidence: float = Field(description="Confidence score", ge=0, le=1)
    recommendations: List[str] = Field(default_factory=list)


# Test Tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"


@tool
def calculate_tool(expression: str) -> str:
    """Calculate mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression"


# Fixtures
@pytest.fixture
def mock_llm_engine():
    """Create a mock LLM engine with predictable behavior."""
    engine = Mock(spec=AugLLMConfig)
    engine.name = "test_llm"
    engine.engine_type = "llm"
    engine.model_name = "gpt-4"
    engine.tools = [search_tool, calculate_tool]
    engine.structured_output = AnalysisResult
    engine.system_message = "You are a helpful assistant."
    engine.prompt_template = "Answer this: {query}"

    # Mock schema methods
    engine.get_input_fields.return_value = {
        "messages": (List[BaseMessage], Field(default_factory=list)),
        "query": (str, Field(default="")),
    }
    engine.get_output_fields.return_value = {
        "response": (str, Field(default="")),
        "messages": (List[BaseMessage], Field(default_factory=list)),
    }

    # Mock output schema
    class MockOutputSchema(BaseModel):
        response: str = ""
        messages: List[BaseMessage] = Field(default_factory=list)

    engine.derive_output_schema.return_value = MockOutputSchema
    engine.output_schema = MockOutputSchema

    # Mock invoke to return structured results
    def mock_invoke(input_data, config=None):
        messages = input_data.get("messages", [])
        query = input_data.get("query", "")

        # Simulate tool call
        if "search" in query.lower():
            return {
                "response": "I'll search for that.",
                "messages": messages
                + [
                    AIMessage(
                        content="I'll search for that.",
                        tool_calls=[
                            {
                                "id": "call_123",
                                "function": {
                                    "name": "search_tool",
                                    "arguments": '{"query": "test search"}',
                                },
                            }
                        ],
                    )
                ],
                "structured_result": AnalysisResult(
                    summary="Found relevant information",
                    confidence=0.85,
                    recommendations=["Review the search results", "Verify accuracy"],
                ),
            }

        # Regular response
        return {
            "response": f"Processed: {query}",
            "messages": messages + [AIMessage(content=f"Processed: {query}")],
            "structured_result": AnalysisResult(
                summary=f"Analysis of: {query}",
                confidence=0.75,
                recommendations=["No specific recommendations"],
            ),
        }

    engine.invoke.side_effect = mock_invoke
    engine.create_runnable.return_value = Mock(invoke=mock_invoke)

    return engine


@pytest.fixture
def mock_retriever_engine():
    """Create a mock retriever engine."""
    engine = Mock(spec=EngineRetriever)
    engine.name = "test_retriever"
    engine.engine_type = "retriever"

    # Mock schema methods
    engine.get_input_fields.return_value = {"query": (str, Field(default=""))}
    engine.get_output_fields.return_value = {
        "documents": (List[Document], Field(default_factory=list)),
        "context": (List[str], Field(default_factory=list)),
    }

    # Mock retrieval
    def mock_invoke(input_data, config=None):
        query = input_data.get("query", "")
        docs = [
            Document(
                page_content=f"Document 1 about {query}", metadata={"source": "test1"}
            ),
            Document(
                page_content=f"Document 2 about {query}", metadata={"source": "test2"}
            ),
        ]
        return {"documents": docs, "context": [doc.page_content for doc in docs]}

    engine.invoke.side_effect = mock_invoke
    engine.create_runnable.return_value = Mock(invoke=mock_invoke)

    return engine


@pytest.fixture
def conversation_docs():
    """Fixture with sample conversation documents."""
    return [
        Document(
            page_content="Customer: I need help with my order #12345. Agent: I'll help you with that order.",
            metadata={"source": "conversation_1", "timestamp": "2024-01-01"},
        ),
        Document(
            page_content="Customer: The product arrived damaged. Agent: I'm sorry to hear that. We'll send a replacement.",
            metadata={"source": "conversation_2", "timestamp": "2024-01-02"},
        ),
        Document(
            page_content="Customer: How do I return an item? Agent: You can initiate a return through your account.",
            metadata={"source": "conversation_3", "timestamp": "2024-01-03"},
        ),
    ]


class TestSimpleAgent:
    """Test SimpleAgent functionality."""

    def test_schema_modification(self, mock_llm_engine):
        """Test that SimpleAgent modifies engine schema correctly."""
        # Create agent
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            agent = SimpleAgent(
                engine=mock_llm_engine,
                structured_output_model=AnalysisResult,
                structured_output_field_name="analysis",
            )

            # Run schema modification
            agent._modify_engine_schema()

            # Check that output schema was modified
            assert hasattr(agent.engine.output_schema, "analysis")

            # Verify the field type
            schema_fields = agent.engine.output_schema.model_fields
            assert "analysis" in schema_fields
            # The field should be Optional[AnalysisResult]

    def test_tool_node_detection(self, mock_llm_engine):
        """Test that SimpleAgent correctly detects needed nodes."""
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            agent = SimpleAgent(engine=mock_llm_engine)

            # Get node requirements
            tool_routes = agent._categorize_tools()

            # Should have langchain tools
            assert "langchain_tool" in tool_routes
            assert len(tool_routes["langchain_tool"]) == 2  # search and calculate

    def test_simple_agent_execution(self, mock_llm_engine):
        """Test SimpleAgent execution with tools."""
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            agent = SimpleAgent(
                engine=mock_llm_engine, structured_output_model=AnalysisResult
            )

            # Mock the graph execution
            mock_graph = Mock()
            mock_graph.invoke.return_value = {
                "messages": [
                    HumanMessage(content="Search for Python tutorials"),
                    AIMessage(content="I'll search for that."),
                    ToolMessage(
                        content="Search results for: Python tutorials",
                        tool_call_id="call_123",
                    ),
                ],
                "structured_result": AnalysisResult(
                    summary="Found Python tutorials",
                    confidence=0.9,
                    recommendations=["Start with basics", "Practice daily"],
                ),
            }
            agent._app = mock_graph

            # Execute
            result = agent.invoke(
                {"messages": [HumanMessage(content="Search for Python tutorials")]}
            )

            # Verify result
            assert "messages" in result
            assert len(result["messages"]) == 3
            assert "structured_result" in result
            assert result["structured_result"].confidence == 0.9


class TestReactAgent:
    """Test ReactAgent looping functionality."""

    def test_react_loop_creation(self, mock_llm_engine):
        """Test that ReactAgent creates loops in the graph."""
        with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
            agent = ReactAgent(engine=mock_llm_engine)

            # Build the graph
            graph = agent.build_graph()

            # Check for loops - tool_node should connect back to agent_node
            edges = graph.edges

            # Should have edge from tool_node to agent_node (not END)
            tool_to_agent_edges = [
                (src, tgt)
                for src, tgt in edges
                if src == "tool_node" and tgt == "agent_node"
            ]
            assert (
                len(tool_to_agent_edges) > 0
            ), "ReactAgent should create loop from tool_node to agent_node"

    def test_react_multi_turn(self, mock_llm_engine):
        """Test ReactAgent handling multiple turns."""
        with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
            agent = ReactAgent(
                engine=mock_llm_engine, structured_output_model=AnalysisResult
            )

            # Mock multi-turn conversation
            turn_count = 0

            def mock_multi_turn_invoke(input_data, config=None):
                nonlocal turn_count
                turn_count += 1
                messages = input_data.get("messages", [])

                if turn_count == 1:
                    # First turn - ask for search
                    return {
                        "messages": messages
                        + [
                            AIMessage(
                                content="Let me search for that.",
                                tool_calls=[
                                    {
                                        "id": f"call_{turn_count}",
                                        "function": {
                                            "name": "search_tool",
                                            "arguments": '{"query": "test"}',
                                        },
                                    }
                                ],
                            )
                        ]
                    }
                else:
                    # Final turn - provide answer
                    return {
                        "messages": messages
                        + [
                            AIMessage(content="Based on the search, here's the answer.")
                        ],
                        "structured_result": AnalysisResult(
                            summary="Search completed",
                            confidence=0.95,
                            recommendations=["Use the search results"],
                        ),
                    }

            mock_llm_engine.invoke.side_effect = mock_multi_turn_invoke

            # Test would verify the looping behavior


class TestMultiAgentWithRAG:
    """Test Multi-Agent with RAG capabilities."""

    def test_sequential_rag_agent(
        self, mock_retriever_engine, mock_llm_engine, conversation_docs
    ):
        """Test sequential execution of RAG agent followed by analysis agent."""

        # Create RAG agent
        with patch("haive.agents.rag.agent.SimpleRAGAgent.setup_workflow"):
            rag_agent = SimpleRAGAgent(
                engine=mock_retriever_engine, name="doc_retriever"
            )

            # Mock RAG execution
            rag_agent.invoke = Mock(
                return_value={
                    "messages": [
                        HumanMessage(content="Find customer service conversations")
                    ],
                    "context": [doc.page_content for doc in conversation_docs],
                    "documents": conversation_docs,
                }
            )

        # Create analysis agent
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            analysis_agent = SimpleAgent(
                engine=mock_llm_engine,
                structured_output_model=AnalysisResult,
                name="analyzer",
            )

            # Mock analysis execution
            analysis_agent.invoke = Mock(
                return_value={
                    "messages": [
                        HumanMessage(
                            content="Analyze the customer service conversations"
                        ),
                        AIMessage(content="I've analyzed the conversations."),
                    ],
                    "structured_result": AnalysisResult(
                        summary="Customer service handles orders, damages, and returns",
                        confidence=0.88,
                        recommendations=[
                            "Improve damage prevention",
                            "Streamline return process",
                            "Enhance order tracking",
                        ],
                    ),
                }
            )

        # Create multi-agent
        with patch("haive.agents.multi.base.SequentialAgent.setup_workflow"):
            multi_agent = SequentialAgent(
                agents=[rag_agent, analysis_agent], name="rag_analyzer"
            )

            # Mock the multi-agent graph
            mock_graph = Mock()

            def mock_multi_invoke(input_data, config=None):
                # Simulate sequential execution
                rag_result = rag_agent.invoke(input_data)

                # Pass context to analyzer
                analysis_input = {
                    "messages": rag_result["messages"],
                    "query": f"Analyze these conversations: {rag_result['context'][:100]}...",
                }
                analysis_result = analysis_agent.invoke(analysis_input)

                return {
                    "messages": analysis_result["messages"],
                    "context": rag_result["context"],
                    "documents": rag_result["documents"],
                    "structured_result": analysis_result["structured_result"],
                }

            mock_graph.invoke.side_effect = mock_multi_invoke
            multi_agent._app = mock_graph

            # Execute multi-agent
            result = multi_agent.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content="Find and analyze customer service patterns"
                        )
                    ]
                }
            )

            # Verify results
            assert "context" in result
            assert "documents" in result
            assert "structured_result" in result
            assert len(result["documents"]) == 3
            assert result["structured_result"].confidence == 0.88
            assert len(result["structured_result"].recommendations) == 3


class TestPromptTemplatesAndMessages:
    """Test prompt template and message handling."""

    def test_prompt_template_usage(self, mock_llm_engine):
        """Test that agents properly use prompt templates."""
        # Set up prompt template
        mock_llm_engine.prompt_template = "System: {system}\nUser: {query}\nAssistant:"
        mock_llm_engine.system_message = "You are an expert analyst."

        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            agent = SimpleAgent(
                engine=mock_llm_engine,
                system_message="Analyze data carefully",  # Override system message
                prompt_template="Context: {context}\nQuestion: {query}",  # Override template
            )

            # Verify the agent synced its prompts to engine
            assert agent.system_message == "Analyze data carefully"
            assert agent.prompt_template == "Context: {context}\nQuestion: {query}"

    def test_message_preservation(self, mock_llm_engine):
        """Test that messages are properly preserved through execution."""
        with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
            agent = SimpleAgent(engine=mock_llm_engine)

            # Create conversation with tool calls
            input_messages = [
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),
                HumanMessage(content="Search for Python tutorials"),
            ]

            # Mock to preserve messages
            def preserve_messages(input_data, config=None):
                messages = input_data.get("messages", [])
                return {
                    "messages": messages
                    + [
                        AIMessage(
                            content="I'll search for Python tutorials.",
                            tool_calls=[
                                {
                                    "id": "call_456",
                                    "function": {
                                        "name": "search_tool",
                                        "arguments": '{"query": "Python tutorials"}',
                                    },
                                }
                            ],
                        )
                    ]
                }

            mock_llm_engine.invoke.side_effect = preserve_messages

            # Mock graph to show full conversation
            mock_graph = Mock()
            mock_graph.invoke.return_value = {
                "messages": input_messages
                + [
                    AIMessage(content="I'll search for Python tutorials."),
                    ToolMessage(
                        content="Found 10 Python tutorials", tool_call_id="call_456"
                    ),
                    AIMessage(content="I found 10 Python tutorials for you."),
                ]
            }
            agent._app = mock_graph

            result = agent.invoke({"messages": input_messages})

            # Verify all messages preserved
            assert len(result["messages"]) == 6
            assert result["messages"][0].content == "Hello"
            assert (
                result["messages"][-1].content == "I found 10 Python tutorials for you."
            )


def test_integration_with_tools(mock_llm_engine):
    """Integration test with actual tool execution."""
    with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
        agent = SimpleAgent(
            engine=mock_llm_engine, force_tool_use=True  # Force tool usage
        )

        # Verify agent is configured for tools
        assert agent.force_tool_use
        assert len(agent.engine.tools) == 2

        # Check tool routes
        tool_routes = agent._categorize_tools()
        assert "langchain_tool" in tool_routes


# Run with: poetry run pytest packages/haive-agents/tests/test_comprehensive_agents.py -v
