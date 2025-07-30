"""Enhanced ReactAgent with Retriever Node and Routing for Agentic RAG.

This agent extends ReactAgent to add a dedicated retrieval node to the graph,
with intelligent routing between tool calls and retrieval based on the query.
"""

import contextlib

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage
from langchain_core.tools import Tool
from langgraph.graph import END
from pydantic import Field

from haive.agents.react import ReactAgent


class ReactRAGAgent(ReactAgent):
    """Enhanced ReactAgent with a dedicated retrieval node and intelligent routing.

    This agent extends ReactAgent by adding a retrieval node to the graph that works
    alongside regular tool nodes. The agent can route between:
    1. Regular tool execution (calculator, web search, etc.)
    2. Retrieval from vector store/knowledge base
    3. Both in combination

    The routing is handled by the LLM through a special retriever tool that triggers
    the retrieval node when called.

    Example:
        .. code-block:: python

            # Create ReactRAG agent with both types of tools
            agent = ReactRAGAgent.create_default(
            name="react_rag",
            retriever_config=vector_store_config,
            tools=[calculator_tool, web_search_tool],
            temperature=0.1
            )

            # The agent will intelligently decide whether to:
            # 1. Use retriever for knowledge queries
            # 2. Use tools for computational/action queries
            # 3. Use both when needed

            result = await agent.arun("What is the capital of France?")  # Uses retriever
            result = await agent.arun("Calculate 15 * 23")  # Uses calculator tool
            result = await agent.arun("Search for Python tutorials")  # Uses web search

    """

    # Retriever configuration
    retriever_config: BaseRetrieverConfig | VectorStoreConfig | None = Field(
        default=None, description="Retriever configuration for RAG functionality"
    )

    # Routing configuration
    use_retriever_for_knowledge: bool = Field(
        default=True, description="Whether to use retriever for knowledge-based queries"
    )

    routing_strategy: str = Field(
        default="auto",
        description="Routing strategy: 'auto', 'retriever_first', 'tools_first', 'parallel'",
    )

    @classmethod
    def create_default(cls, **kwargs) -> "ReactRAGAgent":
        """Create a default ReactRAG agent with retriever and tools.

        Args:
            **kwargs: Configuration options
                - name: Agent name
                - retriever_config: Retriever or vector store config
                - tools: List of regular tools
                - temperature: LLM temperature
                - routing_strategy: How to route between retriever and tools
                - engine: Custom AugLLMConfig if needed

        Returns:
            ReactRAGAgent configured for RAG with tools
        """
        # Extract config params
        name = kwargs.pop("name", "react_rag_agent")
        temperature = kwargs.pop("temperature", 0.1)
        retriever_config = kwargs.pop("retriever_config", None)
        tools = kwargs.pop("tools", [])
        routing_strategy = kwargs.pop("routing_strategy", "auto")

        # Create retriever tool if config provided
        all_tools = list(tools) if tools else []
        if retriever_config:
            retriever_tool = cls._create_retriever_tool(retriever_config)
            all_tools.append(retriever_tool)

        # Create engine if not provided
        engine = kwargs.pop("engine", None)
        if engine is None:
            engine = AugLLMConfig(
                temperature=temperature,
                system_message=(
                    "You are an intelligent assistant with access to both a knowledge base and various tools.\n\n"
                    "Decision Guidelines:\n"
                    "1. For factual/knowledge questions, use the retriever tool first\n"
                    "2. For calculations, use the calculator tool\n"
                    "3. For current information, use the web search tool\n"
                    "4. For complex queries, combine multiple tools as needed\n\n"
                    "Always think step-by-step about which tool(s) to use and why."
                ),
            )

        return cls(
            name=name,
            engine=engine,
            tools=all_tools,
            retriever_config=retriever_config,
            routing_strategy=routing_strategy,
            **kwargs,
        )

    @staticmethod
    def _create_retriever_tool(
        retriever_config: BaseRetrieverConfig | VectorStoreConfig,
    ) -> Tool:
        """Create a retriever tool that triggers the retrieval node.

        This tool doesn't actually perform retrieval - it just signals
        that retrieval should happen via the dedicated retrieval node.

        Args:
            retriever_config: The retriever or vector store configuration

        Returns:
            Tool that triggers the retrieval node
        """

        def trigger_retrieval(query: str) -> str:
            """Trigger retrieval from the knowledge base.

            This is a placeholder that signals the graph to route to the retrieval node.
            The actual retrieval happens in the dedicated node.
            """
            return f"Searching knowledge base for: {query}"

        return Tool(
            name="retriever",
            description=(
                "Search the knowledge base for relevant information. "
                "Use this for factual questions, background information, "
                "or when you need to look up specific knowledge. "
                "This tool triggers a dedicated retrieval process."
            ),
            func=trigger_retrieval,
        )

    @classmethod
    def from_vectorstore(
        cls, vector_store_config: VectorStoreConfig, **kwargs
    ) -> "ReactRAGAgent":
        """Create ReactRAG agent from a vector store configuration.

        Args:
            vector_store_config: Vector store configuration
            **kwargs: Additional agent configuration

        Returns:
            ReactRAGAgent with retriever tool
        """
        kwargs["retriever_config"] = vector_store_config
        return cls.create_default(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build the enhanced React graph with retrieval node."""
        # Start with the base React graph
        graph = super().build_graph()

        # Add retrieval node if we have a retriever config
        if self.retriever_config:
            # Create retrieval node using EngineNodeConfig
            retrieval_node = EngineNodeConfig(
                engine=self.retriever_config, name="retrieval_node"
            )

            # Add the retrieval node to the graph
            graph.add_node("retrieval_node", retrieval_node)

            # Remove existing routing from agent_node if it exists
            # React already adds routing, we need to replace it
            if "agent_node" in graph.nodes:
                # Get existing edges from agent_node
                existing_edges = []
                for edge in graph.edges:
                    if edge[0] == "agent_node":
                        existing_edges.append(edge)

                # Remove existing edges
                for edge in existing_edges:
                    with contextlib.suppress(Exception):
                        graph.remove_edge(edge[0], edge[1])

                # Add new conditional routing
                graph.add_conditional_edges(
                    "agent_node",
                    self._route_to_retrieval_or_tools,
                    {
                        "retrieval": "retrieval_node",
                        "tools": "tool_node" if self._needs_tool_node() else END,
                        "end": END,
                    },
                )

            # Route from retrieval_node back to agent_node (React loop)
            graph.add_edge("retrieval_node", "agent_node")

        return graph

    def _route_to_retrieval_or_tools(self, state) -> str:
        """Route to retrieval node, tool node, or end based on agent output."""
        if not hasattr(state, "messages") or not state.messages:
            return "end"

        last_msg = state.messages[-1]
        if not isinstance(last_msg, AIMessage):
            return "end"

        # Check for tool calls
        tool_calls = getattr(last_msg, "tool_calls", [])
        if not tool_calls:
            return "end"

        # Check if any tool call is for the retriever
        for tool_call in tool_calls:
            if tool_call.get("name") == "retriever":
                return "retrieval"

        # Otherwise route to regular tools
        return "tools" if self._needs_tool_node() else "end"

    def add_retriever_tool(
        self, retriever_config: BaseRetrieverConfig | VectorStoreConfig
    ) -> None:
        """Add or update the retriever tool and rebuild graph.

        Args:
            retriever_config: New retriever configuration
        """
        self.retriever_config = retriever_config

        # Create new retriever tool
        retriever_tool = self._create_retriever_tool(retriever_config)

        # Update tools list
        if self.tools is None:
            self.tools = []

        # Remove existing retriever tool if any
        self.tools = [t for t in self.tools if t.name != "retriever"]

        # Add new retriever tool
        self.tools.append(retriever_tool)

        # Mark for recompilation to rebuild graph
        if hasattr(self, "mark_for_recompile"):
            self.mark_for_recompile("Retriever configuration changed")
