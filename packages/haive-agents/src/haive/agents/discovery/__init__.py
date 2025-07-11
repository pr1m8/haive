"""Enhanced Discovery System for Dynamic Agent and Tool Management.

This module provides advanced discovery capabilities for Haive agents, including:
- Semantic discovery using vector embeddings
- Dynamic tool selection based on query content
- Component capability matching and analysis
- Memory-aware discovery for persistent systems
- LangGraph-style tool management patterns

The system builds on the existing haive.core.utils.discovery infrastructure
while adding intelligent, context-aware discovery capabilities.
"""

# Re-export component registry items from core
from haive.core.registry import (
    CapabilityCategory,
    CapabilityIndex,
    ComponentAnalyzer,
    ComponentMetadata,
    ComponentType,
    EnhancedComponentRegistry,
    RegistrySearcher,
    create_component_registry,
    register_component_batch,
)

from haive.agents.discovery.dynamic_tool_selector import (
    ContextAwareSelector,
    DynamicToolSelector,
    LangGraphStyleSelector,
    SelectionMode,
    ToolBindingStrategy,
    ToolSelectionResult,
    ToolUsageTracker,
)
from haive.agents.discovery.selection_strategies import (
    AdaptiveSelectionStrategy,
    BaseSelectionStrategy,
    CapabilityBasedStrategy,
    ContextualSelectionStrategy,
    EnsembleSelectionStrategy,
    SemanticSelectionStrategy,
)
from haive.agents.discovery.semantic_discovery import (
    CapabilityMatcher,
    DiscoveryMode,
    QueryAnalysis,
    QueryAnalyzer,
    SemanticDiscoveryEngine,
    ToolSelectionStrategy,
    VectorBasedToolSelector,
)

__all__ = [
    "AdaptiveSelectionStrategy",
    # Selection Strategies
    "BaseSelectionStrategy",
    "CapabilityBasedStrategy",
    "CapabilityCategory",
    "CapabilityIndex",
    "CapabilityMatcher",
    "ComponentAnalyzer",
    "ComponentMetadata",
    # Component Registry (re-exported from core)
    "ComponentType",
    "ContextAwareSelector",
    "ContextualSelectionStrategy",
    "DiscoveryMode",
    # Dynamic Tool Selection
    "DynamicToolSelector",
    "EnhancedComponentRegistry",
    "EnsembleSelectionStrategy",
    "LangGraphStyleSelector",
    "QueryAnalysis",
    "QueryAnalyzer",
    "RegistrySearcher",
    "SelectionMode",
    # Semantic Discovery
    "SemanticDiscoveryEngine",
    "SemanticSelectionStrategy",
    "ToolBindingStrategy",
    "ToolSelectionResult",
    "ToolSelectionStrategy",
    "ToolUsageTracker",
    "VectorBasedToolSelector",
    "create_component_registry",
    "register_component_batch",
]
