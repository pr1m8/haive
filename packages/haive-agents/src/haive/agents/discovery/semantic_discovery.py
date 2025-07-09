"""Semantic Discovery Engine with Vector-Based Tool Selection

This module implements semantic discovery capabilities inspired by LangGraph's
many-tools pattern, using vector embeddings to match tools and components
based on query content and semantic similarity.

Key Features:
- Vector-based tool discovery and ranking
- Semantic capability matching
- Query analysis and tool recommendation
- Dynamic tool binding and selection
- Context-aware component matching
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union

from haive.core.registry import (
    CapabilityCategory,
    ComponentAnalyzer,
    ComponentMetadata,
    ComponentType,
    EnhancedComponentRegistry,
    create_component_registry,
)
from haive.core.utils.haive_discovery import (
    UnifiedHaiveDiscovery,
    discover_tools,
    get_all_tools,
)
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, Field, model_validator

from haive.agents.discovery.selection_strategies import (
    AdaptiveSelectionStrategy,
    BaseSelectionStrategy,
    CapabilityBasedStrategy,
    ContextualSelectionStrategy,
    EnsembleSelectionStrategy,
    SemanticSelectionStrategy,
)

logger = logging.getLogger(__name__)


class DiscoveryMode(str, Enum):
    """Different modes for semantic discovery."""

    SIMILARITY = "similarity"  # Pure similarity search
    CAPABILITY = "capability"  # Capability-based matching
    HYBRID = "hybrid"  # Combined similarity + capability
    CONTEXTUAL = "contextual"  # Context-aware selection
    MEMORY_ENHANCED = "memory_enhanced"  # Memory-informed discovery


class ToolSelectionStrategy(str, Enum):
    """Strategies for tool selection."""

    TOP_K = "top_k"  # Select top K most similar
    THRESHOLD = "threshold"  # Select above similarity threshold
    HYBRID = "hybrid"  # Combined strategy
    ADAPTIVE = "adaptive"  # Learns from usage
    CONTEXTUAL = "contextual"  # Context-aware selection


@dataclass
class QueryAnalysis:
    """Analysis of user query for tool selection."""

    original_query: str
    extracted_keywords: List[str]
    inferred_capabilities: List[str]
    domain_tags: List[str]
    complexity_score: float
    intent_classification: str
    suggested_tools: List[str] = field(default_factory=list)


class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents."""
        ...

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        ...


class VectorBasedToolSelector(BaseModel):
    """Selects tools using vector similarity search."""

    embedding_provider: EmbeddingProvider = Field(
        default_factory=lambda: OpenAIEmbeddings(),
        description="Embedding provider for vectorization",
    )
    vector_store: Optional[VectorStore] = Field(
        default=None, description="Vector store for tool embeddings"
    )
    similarity_threshold: float = Field(
        default=0.7, description="Minimum similarity score for tool selection"
    )
    max_tools: int = Field(default=5, description="Maximum number of tools to select")

    # Component registry for enhanced capabilities
    component_registry: Optional[EnhancedComponentRegistry] = Field(
        default=None, description="Enhanced component registry"
    )

    @model_validator(mode="after")
    def setup_vector_store(self) -> "VectorBasedToolSelector":
        """Setup vector store if not provided."""
        if self.vector_store is None:
            self.vector_store = Chroma(
                embedding_function=self.embedding_provider,
                collection_name="haive_tools",
            )

        # Setup component registry if not provided
        if self.component_registry is None:
            self.component_registry = create_component_registry(
                use_embeddings=True, embedding_provider="openai:text-embedding-3-small"
            )

        return self

    def index_tools(self, tools: List[Any]) -> None:
        """Index tools in vector store and component registry."""
        # Also register in component registry
        if self.component_registry:
            for tool in tools:
                self.component_registry.register_component(tool, ComponentType.TOOL)

        # Create documents for vector store
        documents = []
        for tool in tools:
            # Extract tool information
            name = getattr(tool, "name", str(tool))
            description = getattr(tool, "description", "")

            # Create document text
            doc_text = f"Tool: {name}\nDescription: {description}"

            # Add capabilities if available
            if hasattr(tool, "capabilities"):
                doc_text += f"\nCapabilities: {', '.join(tool.capabilities)}"

            # Create document
            doc = Document(
                page_content=doc_text,
                metadata={
                    "tool_name": name,
                    "type": "tool",
                    "capabilities": getattr(tool, "capabilities", []),
                },
            )
            documents.append(doc)

        # Add to vector store
        if documents:
            self.vector_store.add_documents(documents)
            logger.info(f"Indexed {len(documents)} tools in vector store")

    async def select_tools(
        self, query: str, strategy: ToolSelectionStrategy = ToolSelectionStrategy.TOP_K
    ) -> List[ComponentMetadata]:
        """Select tools based on query using specified strategy."""
        if strategy == ToolSelectionStrategy.TOP_K:
            return await self._select_top_k(query)
        elif strategy == ToolSelectionStrategy.THRESHOLD:
            return await self._select_by_threshold(query)
        elif strategy == ToolSelectionStrategy.HYBRID:
            return await self._select_hybrid(query)
        else:
            # Use component registry for advanced strategies
            if self.component_registry:
                results = self.component_registry.search_components(
                    query,
                    component_types=[ComponentType.TOOL],
                    max_results=self.max_tools,
                )
                return results
            else:
                return await self._select_top_k(query)

    async def _select_top_k(self, query: str) -> List[ComponentMetadata]:
        """Select top K most similar tools."""
        # Use component registry if available
        if self.component_registry:
            return self.component_registry.search_components(
                query, component_types=[ComponentType.TOOL], max_results=self.max_tools
            )

        # Fallback to direct vector store search
        results = self.vector_store.similarity_search_with_score(
            query, k=self.max_tools
        )

        selected_tools = []
        for doc, score in results:
            metadata = ComponentMetadata(
                name=doc.metadata.get("tool_name", "Unknown"),
                component_type=ComponentType.TOOL,
                description=doc.page_content,
                capabilities=doc.metadata.get("capabilities", []),
                similarity_score=score,
            )
            selected_tools.append(metadata)

        return selected_tools

    async def _select_by_threshold(self, query: str) -> List[ComponentMetadata]:
        """Select tools above similarity threshold."""
        # Use component registry if available
        if self.component_registry:
            all_results = self.component_registry.search_components(
                query,
                component_types=[ComponentType.TOOL],
                max_results=20,  # Get more results to filter
            )
            # Filter by threshold
            return [
                r
                for r in all_results
                if r.similarity_score >= self.similarity_threshold
            ]

        # Fallback to direct vector store search
        results = self.vector_store.similarity_search_with_score(
            query, k=20  # Get more results to filter
        )

        selected_tools = []
        for doc, score in results:
            if score >= self.similarity_threshold:
                metadata = ComponentMetadata(
                    name=doc.metadata.get("tool_name", "Unknown"),
                    component_type=ComponentType.TOOL,
                    description=doc.page_content,
                    capabilities=doc.metadata.get("capabilities", []),
                    similarity_score=score,
                )
                selected_tools.append(metadata)

        return selected_tools[: self.max_tools]

    async def _select_hybrid(self, query: str) -> List[ComponentMetadata]:
        """Hybrid selection combining similarity and capability matching."""
        # Use component registry for hybrid search
        if self.component_registry:
            # First get similarity-based results
            similar_tools = await self._select_top_k(query)

            # Then get capability-based results
            query_analysis = QueryAnalyzer().analyze_query(query)
            capability_tools = self.component_registry.find_by_capabilities(
                query_analysis.inferred_capabilities,
                component_types=[ComponentType.TOOL],
            )

            # Combine and deduplicate
            all_tools = {t.name: t for t in similar_tools}
            for tool in capability_tools:
                if tool.name not in all_tools:
                    all_tools[tool.name] = tool
                else:
                    # Update scores
                    existing = all_tools[tool.name]
                    existing.capability_match_score = tool.capability_match_score
                    existing.composite_score = (
                        existing.similarity_score * 0.6
                        + existing.capability_match_score * 0.4
                    )

            # Sort by composite score
            sorted_tools = sorted(
                all_tools.values(), key=lambda t: t.composite_score, reverse=True
            )

            return sorted_tools[: self.max_tools]

        # Fallback to simple similarity search
        return await self._select_top_k(query)


class QueryAnalyzer(BaseModel):
    """Analyzes queries to extract relevant information for tool selection."""

    capability_keywords: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "search": ["search", "find", "look", "query", "discover"],
            "analysis": ["analyze", "examine", "inspect", "evaluate", "assess"],
            "generation": ["generate", "create", "make", "produce", "build"],
            "transformation": ["transform", "convert", "change", "modify", "alter"],
            "communication": ["send", "email", "notify", "message", "communicate"],
            "storage": ["save", "store", "persist", "cache", "archive"],
            "retrieval": ["get", "fetch", "retrieve", "load", "read"],
            "processing": ["process", "handle", "execute", "run", "perform"],
        },
        description="Mapping of capabilities to keywords",
    )

    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze query to extract useful information."""
        query_lower = query.lower()

        # Extract keywords
        words = query_lower.split()
        extracted_keywords = [w for w in words if len(w) > 3]

        # Infer capabilities
        inferred_capabilities = []
        for capability, keywords in self.capability_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                inferred_capabilities.append(capability)

        # Extract domain tags
        domain_tags = self._extract_domain_tags(query_lower)

        # Calculate complexity
        complexity_score = self._calculate_complexity(query)

        # Classify intent
        intent = self._classify_intent(query_lower, inferred_capabilities)

        return QueryAnalysis(
            original_query=query,
            extracted_keywords=extracted_keywords,
            inferred_capabilities=inferred_capabilities,
            domain_tags=domain_tags,
            complexity_score=complexity_score,
            intent_classification=intent,
        )

    def _extract_domain_tags(self, query: str) -> List[str]:
        """Extract domain-specific tags from query."""
        domains = {
            "web": ["web", "website", "url", "internet", "online"],
            "file": ["file", "document", "pdf", "csv", "excel"],
            "data": ["data", "dataset", "database", "table", "record"],
            "api": ["api", "endpoint", "service", "rest", "graphql"],
            "email": ["email", "mail", "smtp", "inbox", "message"],
        }

        tags = []
        for domain, keywords in domains.items():
            if any(keyword in query for keyword in keywords):
                tags.append(domain)

        return tags

    def _calculate_complexity(self, query: str) -> float:
        """Calculate query complexity score."""
        # Simple heuristic based on length and structure
        words = query.split()

        # Base complexity from length
        complexity = min(len(words) / 20.0, 1.0)

        # Increase for compound sentences
        if any(conj in query.lower() for conj in ["and", "or", "then", "but"]):
            complexity += 0.2

        # Increase for multiple steps
        if any(step in query.lower() for step in ["first", "then", "finally", "after"]):
            complexity += 0.3

        return min(complexity, 1.0)

    def _classify_intent(self, query: str, capabilities: List[str]) -> str:
        """Classify the primary intent of the query."""
        if not capabilities:
            return "unknown"

        # Priority order for intents
        intent_priority = [
            "generation",
            "analysis",
            "search",
            "transformation",
            "communication",
            "retrieval",
            "processing",
            "storage",
        ]

        for intent in intent_priority:
            if intent in capabilities:
                return intent

        return capabilities[0] if capabilities else "unknown"


class CapabilityMatcher(BaseModel):
    """Matches tools based on required capabilities."""

    capability_matrix: Dict[str, List[str]] = Field(
        default_factory=dict, description="Matrix mapping tools to capabilities"
    )

    component_registry: Optional[EnhancedComponentRegistry] = Field(
        default=None, description="Component registry for capability lookup"
    )

    def build_capability_matrix(self, tools: List[Any]) -> None:
        """Build capability matrix from tools."""
        for tool in tools:
            name = getattr(tool, "name", str(tool))
            capabilities = getattr(tool, "capabilities", [])

            if not capabilities:
                # Infer capabilities from tool description/type
                capabilities = self._infer_capabilities(tool)

            self.capability_matrix[name] = capabilities

    def match_tools(
        self,
        required_capabilities: List[str],
        optional_capabilities: Optional[List[str]] = None,
    ) -> List[Tuple[str, float]]:
        """Match tools based on capabilities."""
        # Use component registry if available
        if self.component_registry:
            results = self.component_registry.find_by_capabilities(
                required_capabilities, component_types=[ComponentType.TOOL]
            )
            return [(r.name, r.capability_match_score) for r in results]

        # Fallback to local capability matrix
        matches = []

        for tool_name, tool_capabilities in self.capability_matrix.items():
            # Check required capabilities
            required_match = all(
                cap in tool_capabilities for cap in required_capabilities
            )

            if not required_match:
                continue

            # Calculate match score
            score = len(set(required_capabilities).intersection(set(tool_capabilities)))

            # Bonus for optional capabilities
            if optional_capabilities:
                optional_match = sum(
                    1 for cap in optional_capabilities if cap in tool_capabilities
                )
                score += optional_match * 0.5

            matches.append((tool_name, score))

        # Sort by score
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _infer_capabilities(self, tool: Any) -> List[str]:
        """Infer capabilities from tool attributes."""
        capabilities = []

        # Check tool name and description
        name = getattr(tool, "name", "").lower()
        description = getattr(tool, "description", "").lower()

        # Common capability patterns
        patterns = {
            "search": ["search", "find", "query", "lookup"],
            "read": ["read", "load", "fetch", "get"],
            "write": ["write", "save", "store", "persist"],
            "process": ["process", "transform", "convert", "analyze"],
            "communicate": ["send", "email", "notify", "message"],
        }

        for capability, keywords in patterns.items():
            if any(kw in name or kw in description for kw in keywords):
                capabilities.append(capability)

        return capabilities if capabilities else ["general"]


class SemanticDiscoveryEngine(BaseModel):
    """Main semantic discovery engine combining all capabilities."""

    vector_selector: VectorBasedToolSelector = Field(
        default_factory=VectorBasedToolSelector,
        description="Vector-based tool selector",
    )
    query_analyzer: QueryAnalyzer = Field(
        default_factory=QueryAnalyzer, description="Query analyzer"
    )
    capability_matcher: CapabilityMatcher = Field(
        default_factory=CapabilityMatcher, description="Capability matcher"
    )
    selection_strategy: BaseSelectionStrategy = Field(
        default_factory=SemanticSelectionStrategy,
        description="Selection strategy to use",
    )

    # Enhanced component registry
    component_registry: Optional[EnhancedComponentRegistry] = Field(
        default=None, description="Shared component registry"
    )

    @model_validator(mode="after")
    def setup_registry(self) -> "SemanticDiscoveryEngine":
        """Setup shared component registry."""
        if self.component_registry is None:
            self.component_registry = create_component_registry(use_embeddings=True)

        # Share registry with sub-components
        self.vector_selector.component_registry = self.component_registry
        self.capability_matcher.component_registry = self.component_registry

        return self

    async def discover_tools(
        self, tools: Optional[List[Any]] = None, haive_root: Optional[str] = None
    ) -> List[ComponentMetadata]:
        """Discover available tools."""
        if tools is None:
            # Use Haive discovery
            if haive_root:
                discovery = UnifiedHaiveDiscovery(haive_root)
                discovered = discovery.discover_all()
                tools = discovered.get("tools", [])
            else:
                # Use basic discovery
                tool_components = discover_tools()
                tools = get_all_tools(tool_components)

        # Register all tools
        tool_metadata = []
        for tool in tools:
            metadata = self.component_registry.register_component(
                tool, ComponentType.TOOL
            )
            tool_metadata.append(metadata)

        # Also index in vector store
        self.vector_selector.index_tools(tools)

        # Build capability matrix
        self.capability_matcher.build_capability_matrix(tools)

        logger.info(f"Discovered and indexed {len(tools)} tools")
        return tool_metadata

    async def semantic_tool_selection(
        self,
        query: str,
        max_tools: int = 5,
        strategy: ToolSelectionStrategy = ToolSelectionStrategy.HYBRID,
        capability_filter: Optional[List[str]] = None,
    ) -> Tuple[List[ComponentMetadata], QueryAnalysis]:
        """Perform semantic tool selection for a query."""
        # Analyze query
        query_analysis = self.query_analyzer.analyze_query(query)

        # Use component registry for advanced search
        if self.component_registry:
            # Perform hybrid search
            selected_tools = self.component_registry.search_components(
                query,
                component_types=[ComponentType.TOOL],
                max_results=max_tools * 2,  # Get more for filtering
            )

            # Apply capability filter if provided
            if capability_filter:
                filtered_tools = []
                for tool in selected_tools:
                    if any(cap in tool.capabilities for cap in capability_filter):
                        filtered_tools.append(tool)
                selected_tools = filtered_tools

            # Apply selection strategy
            if hasattr(self.selection_strategy, "select"):
                context = {
                    "query": query,
                    "query_analysis": query_analysis,
                    "capability_filter": capability_filter,
                }
                selected_tools = self.selection_strategy.select(
                    selected_tools[: max_tools * 2], context, max_tools
                )
            else:
                selected_tools = selected_tools[:max_tools]
        else:
            # Fallback to vector selector
            selected_tools = await self.vector_selector.select_tools(query, strategy)

        # Update query analysis with selected tools
        query_analysis.suggested_tools = [t.name for t in selected_tools]

        return selected_tools, query_analysis

    async def get_tools_for_capabilities(
        self,
        required_capabilities: List[str],
        optional_capabilities: Optional[List[str]] = None,
        max_tools: int = 5,
    ) -> List[ComponentMetadata]:
        """Get tools that match specific capabilities."""
        if self.component_registry:
            # Use registry capability search
            all_capabilities = required_capabilities.copy()
            if optional_capabilities:
                all_capabilities.extend(optional_capabilities)

            results = self.component_registry.find_by_capabilities(
                all_capabilities, component_types=[ComponentType.TOOL]
            )

            # Filter by required capabilities
            filtered = []
            for result in results:
                if all(cap in result.capabilities for cap in required_capabilities):
                    filtered.append(result)

            return filtered[:max_tools]
        else:
            # Use capability matcher
            matches = self.capability_matcher.match_tools(
                required_capabilities, optional_capabilities
            )

            # Convert to ComponentMetadata
            results = []
            for tool_name, score in matches[:max_tools]:
                metadata = ComponentMetadata(
                    name=tool_name,
                    component_type=ComponentType.TOOL,
                    description=f"Tool: {tool_name}",
                    capabilities=self.capability_matcher.capability_matrix.get(
                        tool_name, []
                    ),
                    capability_match_score=score,
                )
                results.append(metadata)

            return results

    def update_selection_strategy(
        self, strategy: Union[BaseSelectionStrategy, str]
    ) -> None:
        """Update the selection strategy."""
        if isinstance(strategy, str):
            # Create strategy from string
            strategy_map = {
                "semantic": SemanticSelectionStrategy,
                "capability": CapabilityBasedStrategy,
                "adaptive": AdaptiveSelectionStrategy,
                "contextual": ContextualSelectionStrategy,
                "ensemble": EnsembleSelectionStrategy,
            }

            strategy_class = strategy_map.get(strategy, SemanticSelectionStrategy)
            self.selection_strategy = strategy_class()
        else:
            self.selection_strategy = strategy
