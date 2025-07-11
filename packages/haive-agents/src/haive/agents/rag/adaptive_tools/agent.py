"""Adaptive RAG with Tools Integration Agents.

Implementation of adaptive RAG with tool integration and ReAct patterns.
Includes Google Search integration, tool selection, and dynamic routing based on query needs.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from haive.core.schema.prebuilt.rag_state import RAGState
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ConditionalAgent, SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class ToolType(str, Enum):
    """Available tool types for adaptive RAG."""

    GOOGLE_SEARCH = "google_search"
    LOCAL_RETRIEVAL = "local_retrieval"
    WIKIPEDIA = "wikipedia"
    ARXIV = "arxiv"
    DIRECT_ANSWER = "direct_answer"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"


class QueryNeed(str, Enum):
    """Query need categories for tool selection."""

    CURRENT_EVENTS = "current_events"
    FACTUAL_LOOKUP = "factual_lookup"
    TECHNICAL_RESEARCH = "technical_research"
    COMMON_KNOWLEDGE = "common_knowledge"
    COMPLEX_REASONING = "complex_reasoning"
    DOCUMENT_SPECIFIC = "document_specific"


class ToolSelection(BaseModel):
    """Tool selection analysis and recommendations."""

    primary_tool: ToolType = Field(description="Primary tool to use")
    fallback_tools: list[ToolType] = Field(
        description="Fallback tools if primary fails"
    )

    query_need: QueryNeed = Field(description="Category of query need")
    urgency: float = Field(
        ge=0.0, le=1.0, description="Urgency of getting current information"
    )
    specificity: float = Field(ge=0.0, le=1.0, description="How specific the query is")

    tool_justification: str = Field(description="Why these tools were selected")
    search_terms: list[str] = Field(
        description="Optimized search terms for external tools"
    )
    expected_result_type: str = Field(description="Expected type of results")

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in tool selection"
    )
    react_strategy: str = Field(description="ReAct strategy to use")


class SearchResult(BaseModel):
    """Results from search tools."""

    tool_used: ToolType = Field(description="Tool that generated the result")
    query_used: str = Field(description="Query used for search")

    # Search metrics
    results_count: int = Field(description="Number of results found")
    search_quality: float = Field(
        ge=0.0, le=1.0, description="Quality of search results"
    )
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Relevance to original query"
    )

    # Content
    documents: list[Document] = Field(description="Retrieved documents")
    source_urls: list[str] = Field(description="Source URLs for web results")
    search_metadata: dict[str, Any] = Field(description="Additional search metadata")

    # Analysis
    content_freshness: float = Field(
        ge=0.0, le=1.0, description="How recent the content is"
    )
    authority_score: float = Field(ge=0.0, le=1.0, description="Authority of sources")
    completeness: float = Field(
        ge=0.0, le=1.0, description="Completeness of answer coverage"
    )


class AdaptiveToolsResult(BaseModel):
    """Complete result from adaptive tools RAG."""

    original_query: str = Field(description="Original query")
    final_response: str = Field(description="Final generated response")

    # Tool usage analytics
    tools_used: list[ToolType] = Field(description="All tools used")
    primary_tool_success: bool = Field(description="Whether primary tool succeeded")
    fallback_used: bool = Field(description="Whether fallback tools were needed")

    # Search analytics
    total_searches: int = Field(description="Total number of searches performed")
    external_sources: int = Field(description="Number of external sources used")
    local_sources: int = Field(description="Number of local sources used")

    # Quality metrics
    response_confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in final response"
    )
    information_freshness: float = Field(
        ge=0.0, le=1.0, description="How current the information is"
    )
    source_diversity: float = Field(
        ge=0.0, le=1.0, description="Diversity of information sources"
    )

    # ReAct tracking
    react_iterations: int = Field(description="Number of ReAct cycles")
    reasoning_steps: list[str] = Field(description="Reasoning steps taken")

    processing_metadata: dict[str, Any] = Field(description="Processing statistics")


# Enhanced prompts for tool-integrated adaptive RAG
TOOL_SELECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at selecting the optimal tools for query processing in an adaptive RAG system.

**AVAILABLE TOOLS:**
1. **Google Search**: Current events, recent information, web-scale factual lookup
2. **Local Retrieval**: Document-specific queries, known corpus information
3. **Wikipedia**: General factual information, encyclopedic knowledge
4. **ArXiv**: Academic research, scientific papers, technical information
5. **Direct Answer**: Common knowledge that doesn't require external lookup
6. **Multi-Query**: Complex queries needing multiple perspectives
7. **HyDE**: Abstract or hypothetical queries needing conceptual expansion

**QUERY NEED ANALYSIS:**
- **Current Events**: Recent news, today's information, trending topics
- **Factual Lookup**: Specific facts, dates, numbers, definitions
- **Technical Research**: Scientific information, academic concepts, expert knowledge
- **Common Knowledge**: Generally known information, simple facts
- **Complex Reasoning**: Multi-step reasoning, synthesis across topics
- **Document Specific**: Information from specific known documents

**REACT STRATEGIES:**
- **Direct**: Single tool usage for straightforward queries
- **Sequential**: Multiple tools in sequence for comprehensive coverage
- **Parallel**: Multiple tools simultaneously for speed and redundancy
- **Iterative**: Tool usage based on previous results, adaptive approach

Select tools strategically based on query characteristics and information needs.""",
        ),
        (
            """human""",
            """Analyze this query and select optimal tools:

**Query:** {query}

**Context:** {context}

**Available Local Documents:** {available_docs_summary}

Analyze the query and provide:
1. Primary tool recommendation with justification
2. Fallback tools for redundancy
3. Query need categorization
4. Search optimization strategies
5. ReAct approach for tool coordination

Focus on maximizing information quality while minimizing tool usage overhead.""",
        ),
    ]
)


GOOGLE_SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at Google search optimization and result processing for RAG systems.

**SEARCH OPTIMIZATION PRINCIPLES:**
1. **Query Refinement**: Transform natural questions into effective search terms
2. **Result Processing**: Extract and structure information from search results
3. **Quality Assessment**: Evaluate source authority and information freshness
4. **Relevance Filtering**: Focus on results most relevant to the original query

**SEARCH STRATEGIES:**
- Use specific keywords rather than full questions
- Include temporal qualifiers for time-sensitive queries
- Add domain-specific terms for technical queries
- Use quote marks for exact phrase matching
- Combine broad and specific terms

Process search results to create structured, relevant information for the RAG system.""",
        ),
        (
            """human""",
            """Optimize search and process results for this query:

**Original Query:** {query}
**Optimized Search Terms:** {search_terms}
**Raw Search Results:** {search_results}

**Task:**
1. Assess the quality and relevance of each result
2. Extract key information relevant to the query
3. Create structured documents from the best results
4. Evaluate information freshness and authority
5. Provide relevance scores and source metadata

Focus on extracting factual, current, and authoritative information.""",
        ),
    ]
)


ADAPTIVE_SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at synthesizing information from multiple tools and sources in an adaptive RAG system.

**SYNTHESIS PRINCIPLES:**
1. **Source Prioritization**: Weight information based on source authority and freshness
2. **Conflict Resolution**: Handle contradictory information across sources
3. **Completeness**: Ensure comprehensive coverage of the query
4. **Transparency**: Indicate source types and confidence levels

**INFORMATION INTEGRATION:**
- Combine local document knowledge with external search results
- Prioritize recent information for time-sensitive queries
- Use authoritative sources for factual claims
- Cross-reference information across multiple sources
- Maintain appropriate uncertainty when information conflicts

Create responses that optimally blend all available information sources.""",
        ),
        (
            """human""",
            """Synthesize information from multiple sources to answer the query:

**Original Query:** {query}

**Local Document Results:** {local_results}
**Google Search Results:** {search_results}
**Tool Selection Analysis:** {tool_analysis}

**Source Quality Metrics:**
- Local Documents: {local_quality}
- External Sources: {external_quality}
- Information Freshness: {freshness_score}

**Task:**
1. Integrate information from all sources intelligently
2. Resolve any conflicts or contradictions
3. Highlight the most authoritative and current information
4. Provide a comprehensive, well-sourced response
5. Include appropriate confidence levels and source attribution

Focus on creating the most accurate and complete response possible.""",
        ),
    ]
)


def create_tool_selector_callable(llm_config: LLMConfig):
    """Create callable function for tool selection."""
    selection_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=TOOL_SELECTION_PROMPT,
        structured_output_model=ToolSelection,
        output_key="tool_selection",
    )

    def select_tools(state: dict[str, Any]) -> dict[str, Any]:
        """Select optimal tools for the query."""
        query = getattr(state, "query", "")
        context = getattr(state, "context", "")

        # Analyze available documents
        retrieved_documents = getattr(state, "retrieved_documents", [])
        available_docs_summary = f"{len(retrieved_documents)} documents available"
        if retrieved_documents:
            # Create summary of available documents
            doc_topics = [
                doc.page_content[:100] + "..." for doc in retrieved_documents[:3]
            ]
            available_docs_summary += f": {', '.join(doc_topics)}"

        # Perform tool selection
        tool_selection = selection_engine.invoke(
            {
                "query": query,
                "context": context,
                "available_docs_summary": available_docs_summary,
            }
        )

        logger.info(
            f"Tool selection: Primary={tool_selection.primary_tool}, Need={tool_selection.query_need}"
        )

        return {
            "tool_selection": tool_selection,
            "primary_tool": tool_selection.primary_tool,
            "fallback_tools": tool_selection.fallback_tools,
            "query_need": tool_selection.query_need,
            "search_terms": tool_selection.search_terms,
            "react_strategy": tool_selection.react_strategy,
            "tool_confidence": tool_selection.confidence,
        }

    return select_tools


def create_google_search_callable(llm_config: LLMConfig):
    """Create callable function for Google search integration."""
    search_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=GOOGLE_SEARCH_PROMPT,
        structured_output_model=SearchResult,
        output_key="search_result",
    )

    def perform_google_search(state: dict[str, Any]) -> dict[str, Any]:
        """Perform Google search and process results."""
        query = getattr(state, "query", "")
        search_terms = getattr(state, "search_terms", [query])

        # Mock Google search for now (in real implementation, integrate with Google Search API)
        mock_search_results = f"""
        Search Results for "{search_terms[0]}":

        1. Recent article from authoritative source about {query}
        2. Wikipedia entry providing background information
        3. News article with current developments
        4. Academic paper with technical details
        5. Expert blog post with analysis
        """

        # Process search results
        search_result = search_engine.invoke(
            {
                "query": query,
                "search_terms": ", ".join(search_terms),
                "search_results": mock_search_results,
            }
        )

        logger.info(
            f"Google search completed: {search_result.results_count} results, quality={search_result.search_quality}"
        )

        return {
            "search_result": search_result,
            "search_documents": search_result.documents,
            "search_quality": search_result.search_quality,
            "search_relevance": search_result.relevance_score,
            "content_freshness": search_result.content_freshness,
            "source_urls": search_result.source_urls,
            "external_sources_used": True,
        }

    return perform_google_search


def create_adaptive_synthesis_callable(llm_config: LLMConfig):
    """Create callable function for adaptive synthesis."""
    synthesis_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ADAPTIVE_SYNTHESIS_PROMPT,
        structured_output_model=AdaptiveToolsResult,
        output_key="adaptive_result",
    )

    def synthesize_adaptive_response(state: dict[str, Any]) -> dict[str, Any]:
        """Synthesize final response from all sources."""
        query = getattr(state, "query", "")

        # Gather local results
        retrieved_documents = getattr(state, "retrieved_documents", [])
        local_results = (
            "\n".join(
                [
                    f"Doc {i+1}: {doc.page_content[:200]}..."
                    for i, doc in enumerate(retrieved_documents[:3])
                ]
            )
            if retrieved_documents
            else "No local documents"
        )

        # Gather search results
        search_result = getattr(state, "search_result", None)
        search_results = "No external search performed"
        if search_result:
            search_results = f"Search Quality: {search_result.search_quality}, Relevance: {search_result.relevance_score}"

        # Tool analysis
        tool_selection = getattr(state, "tool_selection", None)
        tool_analysis = "No tool analysis available"
        if tool_selection:
            tool_analysis = f"Primary Tool: {tool_selection.primary_tool}, Confidence: {tool_selection.confidence}"

        # Quality metrics
        local_quality = len(retrieved_documents) / 10.0 if retrieved_documents else 0.0
        external_quality = search_result.search_quality if search_result else 0.0
        freshness_score = search_result.content_freshness if search_result else 0.5

        # Synthesize response
        adaptive_result = synthesis_engine.invoke(
            {
                "query": query,
                "local_results": local_results,
                "search_results": search_results,
                "tool_analysis": tool_analysis,
                "local_quality": local_quality,
                "external_quality": external_quality,
                "freshness_score": freshness_score,
            }
        )

        logger.info(
            f"Adaptive synthesis completed: confidence={adaptive_result.response_confidence}"
        )

        return {
            "adaptive_result": adaptive_result,
            "final_response": adaptive_result.final_response,
            "response_confidence": adaptive_result.response_confidence,
            "tools_used": adaptive_result.tools_used,
            "information_freshness": adaptive_result.information_freshness,
            "source_diversity": adaptive_result.source_diversity,
        }

    return synthesize_adaptive_response


class ToolSelectionAgent(Agent):
    """Agent that selects optimal tools based on query analysis."""

    name: str = "Tool Selection"
    llm_config: LLMConfig = Field(description="LLM configuration for tool selection")

    def build_graph(self) -> BaseGraph:
        """Build tool selection graph."""
        graph = BaseGraph(name="ToolSelection")

        # Create callable function using the Pydantic field
        tool_selector = create_tool_selector_callable(self.llm_config)

        # Add callable node to graph
        graph.add_node("select_tools", tool_selector)
        graph.add_edge(START, "select_tools")
        graph.add_edge("select_tools", END)

        return graph


class SearchIntegrationAgent(Agent):
    """Agent that integrates external search tools."""

    name: str = "Search Integration"
    llm_config: LLMConfig = Field(description="LLM configuration for search processing")

    def build_graph(self) -> BaseGraph:
        """Build search integration graph."""
        graph = BaseGraph(name="SearchIntegration")

        # Create callable function using the Pydantic field
        google_searcher = create_google_search_callable(self.llm_config)

        # Add callable node to graph
        graph.add_node("google_search", google_searcher)
        graph.add_edge(START, "google_search")
        graph.add_edge("google_search", END)

        return graph


class AdaptiveToolsRAGAgent(SequentialAgent):
    """Complete Adaptive RAG agent with tools integration and ReAct patterns."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        enable_google_search: bool = True,
        enable_local_retrieval: bool = True,
        **kwargs,
    ):
        """Create Adaptive Tools RAG agent from documents.

        Args:
            documents: Documents to index for local retrieval
            llm_config: LLM configuration
            enable_google_search: Whether to enable Google Search integration
            enable_local_retrieval: Whether to enable local document retrieval
            **kwargs: Additional arguments

        Returns:
            AdaptiveToolsRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        agents = []

        # Step 1: Tool selection with structured output
        tool_selector = ToolSelectionAgent(llm_config=llm_config, name="Tool Selector")
        agents.append(tool_selector)

        # Step 2: Local retrieval (if enabled)
        if enable_local_retrieval and documents:
            local_retriever = BaseRAGAgent.from_documents(
                documents=documents, llm_config=llm_config, name="Local Retriever"
            )
            agents.append(local_retriever)

        # Step 3: External search integration (if enabled)
        if enable_google_search:
            search_integrator = SearchIntegrationAgent(
                llm_config=llm_config, name="Search Integrator"
            )
            agents.append(search_integrator)

        # Step 4: Adaptive synthesis
        adaptive_synthesizer = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ADAPTIVE_SYNTHESIS_PROMPT,
                structured_output_model=AdaptiveToolsResult,
                output_key="adaptive_result",
            ),
            name="Adaptive Synthesizer",
        )
        agents.append(adaptive_synthesizer)

        # Remove name from kwargs to avoid conflict
        agent_name = kwargs.pop("name", "Adaptive Tools RAG Agent")

        return cls(agents=agents, name=agent_name, **kwargs)


# Factory function
def create_adaptive_tools_rag_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    tools_mode: str = "full",
    **kwargs,
) -> AdaptiveToolsRAGAgent:
    """Create an Adaptive Tools RAG agent.

    Args:
        documents: Documents for local retrieval
        llm_config: LLM configuration
        tools_mode: Tools mode ("full", "search_only", "local_only")
        **kwargs: Additional arguments

    Returns:
        Configured Adaptive Tools RAG agent
    """
    # Configure based on tools mode
    if tools_mode == "search_only":
        kwargs.setdefault("enable_local_retrieval", False)
        kwargs.setdefault("enable_google_search", True)
    elif tools_mode == "local_only":
        kwargs.setdefault("enable_local_retrieval", True)
        kwargs.setdefault("enable_google_search", False)
    else:  # full
        kwargs.setdefault("enable_local_retrieval", True)
        kwargs.setdefault("enable_google_search", True)

    return AdaptiveToolsRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_adaptive_tools_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Adaptive Tools RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "tool_selection",
            "primary_tool",
            "fallback_tools",
            "query_need",
            "search_terms",
            "react_strategy",
            "tool_confidence",
            "search_result",
            "search_documents",
            "search_quality",
            "external_sources_used",
            "adaptive_result",
            "final_response",
            "response_confidence",
            "tools_used",
            "information_freshness",
            "source_diversity",
            "retrieved_documents",
            "response",
            "messages",
        ],
    }
