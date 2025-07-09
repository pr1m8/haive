"""Compatible RAG Workflow Factory

Generic factory for building composable RAG workflows based on I/O schema compatibility.
Uses the enhanced multi-agent base with automatic compatibility checking, agent replacement,
and workflow optimization. Allows replacing agents by compatible I/O schemas.

Key Features:
    - Automatic I/O schema compatibility analysis
    - Agent replacement based on schema compatibility
    - Workflow optimization for better field flow
    - Component-based RAG workflow building
    - Integration with search tools from haive.tools
    - Enhanced system prompts and grading
"""

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ConditionalAgent, ParallelAgent, SequentialAgent
from haive.agents.rag.adaptive.agent import AdaptiveRAGAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.document_graders.comprehensive_grader import (
    COMPREHENSIVE_DOCUMENT_GRADING_PROMPT,
    HALLUCINATION_DETECTION_PROMPT,
    QUALITY_ASSESSMENT_PROMPT,
    ComprehensiveDocumentGrade,
    ComprehensiveGradingResponse,
)
from haive.agents.rag.corrective.agent_v2 import CorrectiveRAGAgentV2
from haive.agents.rag.document_grading.agent import DocumentGradingAgent
from haive.agents.rag.hallucination_grading.agent import (
    AdvancedHallucinationGraderAgent,
    HallucinationGraderAgent,
    RealtimeHallucinationGraderAgent,
    create_hallucination_grader,
)
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.query_decomposition.agent import (
    AdaptiveQueryDecomposerAgent,
    ContextualQueryDecomposerAgent,
    HierarchicalQueryDecomposerAgent,
    QueryDecomposerAgent,
    create_query_decomposer,
)
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)

# ============================================================================
# RAG COMPONENT DEFINITIONS
# ============================================================================


class RAGComponent(str, Enum):
    """Available RAG components for composition."""

    # Core components
    BASE_RETRIEVAL = "base_retrieval"
    SIMPLE_RAG = "simple_rag"

    # Advanced RAG
    CORRECTIVE_RAG = "corrective_rag"
    HYDE_RAG = "hyde_rag"
    MULTI_QUERY_RAG = "multi_query_rag"
    ADAPTIVE_RAG = "adaptive_rag"

    # Processing components
    DOCUMENT_GRADING = "document_grading"
    HALLUCINATION_DETECTION = "hallucination_detection"
    HALLUCINATION_GRADING = "hallucination_grading"
    ADVANCED_HALLUCINATION_GRADING = "advanced_hallucination_grading"
    REALTIME_HALLUCINATION_GRADING = "realtime_hallucination_grading"
    QUALITY_ASSESSMENT = "quality_assessment"
    COMPREHENSIVE_GRADING = "comprehensive_grading"

    # Query components
    QUERY_EXPANSION = "query_expansion"
    QUERY_ANALYSIS = "query_analysis"
    QUERY_DECOMPOSITION = "query_decomposition"
    HIERARCHICAL_DECOMPOSITION = "hierarchical_decomposition"
    CONTEXTUAL_DECOMPOSITION = "contextual_decomposition"
    ADAPTIVE_DECOMPOSITION = "adaptive_decomposition"

    # Search tools
    WEB_SEARCH = "web_search"
    ARXIV_SEARCH = "arxiv_search"

    # Answer generation
    ANSWER_GENERATION = "answer_generation"
    FUSION_GENERATION = "fusion_generation"


class WorkflowPattern(str, Enum):
    """Common workflow patterns from the architecture guide."""

    # Basic patterns
    SIMPLE = "simple"  # Retrieval → Answer
    GRADED = "graded"  # Retrieval → Grading → Answer

    # Advanced patterns
    CORRECTIVE = "corrective"  # CRAG pattern
    ADAPTIVE = "adaptive"  # Dynamic routing

    # Query transformation patterns
    MULTI_QUERY = "multi_query"  # Query expansion
    HYDE = "hyde"  # Hypothetical documents
    FUSION = "fusion"  # Multi-source fusion

    # Tool-enabled patterns
    AGENTIC = "agentic"  # Tool-using agents


# ============================================================================
# ENHANCED COMPATIBLE RAG FACTORY
# ============================================================================


class CompatibleRAGFactory:
    """Factory for building RAG workflows with I/O schema compatibility.

    Uses the enhanced multi-agent base with automatic compatibility checking,
    agent replacement, and workflow optimization.
    """

    def __init__(
        self,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        enable_search_tools: bool = False,
        default_embedding_model: Optional[str] = None,
    ):
        """Initialize factory with common dependencies.

        Args:
            documents: Document collection for retrieval
            llm_config: LLM configuration for all components
            enable_search_tools: Whether to integrate external search tools
            default_embedding_model: Default embedding model for vector stores
        """
        self.documents = documents
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.enable_search_tools = enable_search_tools
        self.default_embedding_model = default_embedding_model

        # Component registry
        self._component_builders = {
            RAGComponent.BASE_RETRIEVAL: self._build_base_retrieval,
            RAGComponent.SIMPLE_RAG: self._build_simple_rag,
            RAGComponent.CORRECTIVE_RAG: self._build_corrective_rag,
            RAGComponent.HYDE_RAG: self._build_hyde_rag,
            RAGComponent.MULTI_QUERY_RAG: self._build_multi_query_rag,
            RAGComponent.ADAPTIVE_RAG: self._build_adaptive_rag,
            RAGComponent.DOCUMENT_GRADING: self._build_document_grading,
            RAGComponent.COMPREHENSIVE_GRADING: self._build_comprehensive_grading,
            RAGComponent.HALLUCINATION_DETECTION: self._build_hallucination_detection,
            RAGComponent.HALLUCINATION_GRADING: self._build_hallucination_grading,
            RAGComponent.ADVANCED_HALLUCINATION_GRADING: self._build_advanced_hallucination_grading,
            RAGComponent.REALTIME_HALLUCINATION_GRADING: self._build_realtime_hallucination_grading,
            RAGComponent.QUALITY_ASSESSMENT: self._build_quality_assessment,
            RAGComponent.QUERY_EXPANSION: self._build_query_expansion,
            RAGComponent.QUERY_ANALYSIS: self._build_query_analysis,
            RAGComponent.QUERY_DECOMPOSITION: self._build_query_decomposition,
            RAGComponent.HIERARCHICAL_DECOMPOSITION: self._build_hierarchical_decomposition,
            RAGComponent.CONTEXTUAL_DECOMPOSITION: self._build_contextual_decomposition,
            RAGComponent.ADAPTIVE_DECOMPOSITION: self._build_adaptive_decomposition,
            RAGComponent.WEB_SEARCH: self._build_web_search,
            RAGComponent.ARXIV_SEARCH: self._build_arxiv_search,
            RAGComponent.ANSWER_GENERATION: self._build_answer_generation,
            RAGComponent.FUSION_GENERATION: self._build_fusion_generation,
        }

        # Workflow patterns
        self._pattern_builders = {
            WorkflowPattern.SIMPLE: self._build_simple_pattern,
            WorkflowPattern.GRADED: self._build_graded_pattern,
            WorkflowPattern.CORRECTIVE: self._build_corrective_pattern,
            WorkflowPattern.ADAPTIVE: self._build_adaptive_pattern,
            WorkflowPattern.MULTI_QUERY: self._build_multi_query_pattern,
            WorkflowPattern.HYDE: self._build_hyde_pattern,
            WorkflowPattern.FUSION: self._build_fusion_pattern,
            WorkflowPattern.AGENTIC: self._build_agentic_pattern,
        }

    def create_workflow(
        self,
        pattern: WorkflowPattern,
        components: Optional[List[RAGComponent]] = None,
        routing_conditions: Optional[Dict[str, Callable]] = None,
        **kwargs,
    ) -> Union[SequentialAgent, ConditionalAgent, ParallelAgent]:
        """Create a workflow based on pattern and components.

        Args:
            pattern: Workflow pattern to use
            components: Optional component overrides
            routing_conditions: Conditional routing logic
            **kwargs: Additional configuration

        Returns:
            Configured multi-agent workflow
        """
        if pattern in self._pattern_builders:
            return self._pattern_builders[pattern](
                components=components, routing_conditions=routing_conditions, **kwargs
            )
        else:
            return self._build_custom_workflow(
                components=components or [],
                routing_conditions=routing_conditions,
                **kwargs,
            )

    def create_from_schema_compatibility(
        self,
        component_sequence: List[RAGComponent],
        auto_optimize: bool = True,
        **kwargs,
    ) -> SequentialAgent:
        """Create workflow by chaining components with compatible I/O schemas.

        This is the core generic functionality - it analyzes I/O schemas
        and builds a compatible chain using the enhanced multi-agent base.

        Args:
            component_sequence: Ordered list of components to chain
            auto_optimize: Whether to auto-optimize agent order
            **kwargs: Additional configuration

        Returns:
            SequentialAgent with compatible component chain
        """
        agents = []

        for component in component_sequence:
            if component in self._component_builders:
                agent = self._component_builders[component](**kwargs)
                agents.append(agent)

        # Use enhanced AgentSchemaComposer with compatibility checking
        return SequentialAgent(
            agents=agents,
            name=kwargs.get("name", "Schema-Compatible RAG Workflow"),
            schema_separation="smart",
        )

    def replace_agent_in_workflow(
        self,
        workflow: Union[SequentialAgent, ConditionalAgent],
        target_agent_name: str,
        replacement_component: RAGComponent,
        **kwargs,
    ) -> bool:
        """Replace an agent in existing workflow based on I/O compatibility.

        Uses the enhanced multi-agent base compatibility checking.

        Args:
            workflow: Existing workflow to modify
            target_agent_name: Name of agent to replace
            replacement_component: New component to use
            **kwargs: Configuration for new component

        Returns:
            True if replacement successful
        """
        if replacement_component not in self._component_builders:
            logger.error(f"Unknown component: {replacement_component}")
            return False

        # Build replacement agent
        replacement_agent = self._component_builders[replacement_component](**kwargs)

        # Use multi-agent base replacement method with compatibility checking
        return workflow.replace_agent_by_compatibility(
            target_agent_name=target_agent_name,
            replacement_agent=replacement_agent,
            check_compatibility=True,
        )

    def analyze_workflow_compatibility(
        self, workflow: Union[SequentialAgent, ConditionalAgent]
    ) -> Dict[str, Any]:
        """Analyze I/O compatibility of existing workflow.

        Args:
            workflow: Workflow to analyze

        Returns:
            Compatibility analysis report
        """
        return workflow.analyze_io_compatibility()

    def suggest_workflow_optimizations(
        self, workflow: Union[SequentialAgent, ConditionalAgent]
    ) -> Dict[str, Any]:
        """Suggest optimizations for workflow based on I/O compatibility.

        Args:
            workflow: Workflow to optimize

        Returns:
            Optimization suggestions
        """
        compatibility = workflow.analyze_io_compatibility()
        optimized_order = workflow.optimize_agent_order()

        current_order = [agent.name for agent in workflow.agents]
        suggested_order = [agent.name for agent in optimized_order]

        suggestions = {
            "current_compatibility_score": (
                compatibility.get("compatibility_matrix", [[]])[0][1]
                if len(compatibility.get("compatibility_matrix", [])) > 1
                else 1.0
            ),
            "suggested_agent_order": suggested_order,
            "order_changed": current_order != suggested_order,
            "routing_suggestions": compatibility.get("routing_suggestions", []),
            "potential_replacements": self._suggest_component_replacements(workflow),
        }

        return suggestions

    def _suggest_component_replacements(
        self, workflow: Union[SequentialAgent, ConditionalAgent]
    ) -> List[Dict[str, Any]]:
        """Suggest component replacements for better compatibility."""
        suggestions = []

        # Analyze each agent and suggest alternatives
        for agent in workflow.agents:
            agent_outputs = workflow._get_agent_output_fields(agent)
            agent_inputs = workflow._get_agent_input_fields(agent)

            # Find components that could replace this agent
            for component, builder in self._component_builders.items():
                try:
                    candidate = builder(name=f"Test_{component}")
                    candidate_outputs = workflow._get_agent_output_fields(candidate)
                    candidate_inputs = workflow._get_agent_input_fields(candidate)

                    # Check if candidate has better I/O overlap
                    output_overlap = len(agent_outputs.intersection(candidate_outputs))
                    input_overlap = len(agent_inputs.intersection(candidate_inputs))

                    if output_overlap > 0 or input_overlap > 0:
                        suggestions.append(
                            {
                                "current_agent": agent.name,
                                "suggested_component": component.value,
                                "output_field_overlap": output_overlap,
                                "input_field_overlap": input_overlap,
                                "compatibility_score": (output_overlap + input_overlap)
                                / max(len(agent_outputs) + len(agent_inputs), 1),
                            }
                        )
                except Exception:
                    # Skip if component can't be built
                    continue

        # Sort by compatibility score
        suggestions.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return suggestions[:5]  # Top 5 suggestions

    # Pattern builders
    def _build_simple_pattern(self, **kwargs) -> SequentialAgent:
        """Simple: Retrieval → Answer Generation"""
        return self.create_from_schema_compatibility(
            [RAGComponent.BASE_RETRIEVAL, RAGComponent.ANSWER_GENERATION], **kwargs
        )

    def _build_graded_pattern(self, **kwargs) -> SequentialAgent:
        """Graded: Retrieval → Document Grading → Answer Generation"""
        return self.create_from_schema_compatibility(
            [
                RAGComponent.BASE_RETRIEVAL,
                RAGComponent.COMPREHENSIVE_GRADING,
                RAGComponent.ANSWER_GENERATION,
            ],
            **kwargs,
        )

    def _build_corrective_pattern(self, **kwargs) -> ConditionalAgent:
        """CRAG: Retrieval → Grade → Route (Refine/Web/Continue)"""
        return self._build_corrective_rag(**kwargs)

    def _build_hyde_pattern(self, **kwargs) -> SequentialAgent:
        """HyDE: Query → Hypothetical Doc → Retrieval → Answer"""
        return self.create_from_schema_compatibility([RAGComponent.HYDE_RAG], **kwargs)

    def _build_multi_query_pattern(self, **kwargs) -> SequentialAgent:
        """Multi-Query: Query Expansion → Parallel Retrieval → Answer"""
        return self.create_from_schema_compatibility(
            [RAGComponent.MULTI_QUERY_RAG], **kwargs
        )

    def _build_adaptive_pattern(self, **kwargs) -> ConditionalAgent:
        """Adaptive: Query Analysis → Route to Best Strategy"""
        return self._build_adaptive_rag(**kwargs)

    def _build_fusion_pattern(self, **kwargs) -> SequentialAgent:
        """Fusion: Multi-Source → Rank Fusion → Generate"""
        components = [RAGComponent.MULTI_QUERY_RAG]

        if self.enable_search_tools:
            components.extend([RAGComponent.WEB_SEARCH, RAGComponent.ARXIV_SEARCH])

        components.append(RAGComponent.FUSION_GENERATION)

        return self.create_from_schema_compatibility(components, **kwargs)

    def _build_agentic_pattern(self, **kwargs) -> ConditionalAgent:
        """Agentic: Tool Selection → Execute → Aggregate"""
        query_analyzer = self._build_query_analysis(**kwargs)

        # Tool agents
        retrieval = self._build_base_retrieval(**kwargs)

        agents = [query_analyzer, retrieval]

        if self.enable_search_tools:
            web_search = self._build_web_search(**kwargs)
            arxiv = self._build_arxiv_search(**kwargs)
            agents.extend([web_search, arxiv])

        answer_gen = self._build_fusion_generation(**kwargs)
        agents.append(answer_gen)

        # Route based on query analysis
        def route_by_intent(state: Dict[str, Any]) -> str:
            analysis = state.get("query_analysis", {})

            if isinstance(analysis, dict):
                if analysis.get("domain_specific") and self.enable_search_tools:
                    return "arxiv_search"
                elif analysis.get("temporal_sensitivity") and self.enable_search_tools:
                    return "web_search"
                else:
                    return "base_retrieval"

            return "base_retrieval"

        routing = {"query_analyzer": {"condition": route_by_intent}}

        return ConditionalAgent(
            agents=agents,
            branches=routing,
            name=kwargs.get("name", "Agentic RAG Workflow"),
        )

    def _build_custom_workflow(
        self,
        components: List[RAGComponent],
        routing_conditions: Optional[Dict[str, Callable]] = None,
        **kwargs,
    ) -> Union[SequentialAgent, ConditionalAgent]:
        """Build custom workflow from component list."""
        if routing_conditions:
            agents = [
                self._component_builders[comp](**kwargs)
                for comp in components
                if comp in self._component_builders
            ]
            return ConditionalAgent(
                agents=agents,
                branches=routing_conditions,
                name=kwargs.get("name", "Custom RAG Workflow"),
            )
        else:
            return self.create_from_schema_compatibility(components, **kwargs)

    # Component builders - enhanced with better compatibility
    def _build_base_retrieval(self, **kwargs) -> BaseRAGAgent:
        """Build basic retrieval agent."""
        return BaseRAGAgent.from_documents(
            documents=self.documents,
            embedding_model=kwargs.get("embedding_model", self.default_embedding_model),
            name=kwargs.get("name", "Base Retriever"),
        )

    def _build_simple_rag(self, **kwargs) -> SimpleRAGAgent:
        """Build simple RAG agent."""
        return SimpleRAGAgent.from_documents(
            documents=self.documents, llm_config=self.llm_config, **kwargs
        )

    def _build_corrective_rag(self, **kwargs) -> CorrectiveRAGAgentV2:
        """Build corrective RAG agent."""
        return CorrectiveRAGAgentV2.from_documents(
            documents=self.documents, llm_config=self.llm_config, **kwargs
        )

    def _build_hyde_rag(self, **kwargs) -> HyDERAGAgentV2:
        """Build HyDE RAG agent."""
        return HyDERAGAgentV2.from_documents(
            documents=self.documents,
            llm_config=self.llm_config,
            embedding_model=kwargs.get("embedding_model", self.default_embedding_model),
            **kwargs,
        )

    def _build_multi_query_rag(self, **kwargs) -> MultiQueryRAGAgent:
        """Build multi-query RAG agent."""
        return MultiQueryRAGAgent.from_documents(
            documents=self.documents,
            llm_config=self.llm_config,
            embedding_model=kwargs.get("embedding_model", self.default_embedding_model),
            **kwargs,
        )

    def _build_adaptive_rag(self, **kwargs) -> AdaptiveRAGAgent:
        """Build adaptive RAG agent."""
        return AdaptiveRAGAgent.from_documents(
            documents=self.documents,
            llm_config=self.llm_config,
            embedding_model=kwargs.get("embedding_model", self.default_embedding_model),
            **kwargs,
        )

    def _build_document_grading(self, **kwargs) -> DocumentGradingAgent:
        """Build document grading agent."""
        return DocumentGradingAgent(llm_config=self.llm_config, **kwargs)

    def _build_comprehensive_grading(self, **kwargs) -> SimpleAgent:
        """Build comprehensive document grading agent."""
        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=COMPREHENSIVE_DOCUMENT_GRADING_PROMPT,
                structured_output_model=ComprehensiveGradingResponse,
                output_key="grading_results",
            ),
            name=kwargs.get("name", "Comprehensive Grader"),
        )

    def _build_hallucination_detection(self, **kwargs) -> SimpleAgent:
        """Build basic hallucination detection agent."""
        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=HALLUCINATION_DETECTION_PROMPT,
                output_key="hallucination_analysis",
            ),
            name=kwargs.get("name", "Hallucination Detector"),
        )

    def _build_hallucination_grading(self, **kwargs) -> HallucinationGraderAgent:
        """Build standalone hallucination grading agent."""
        return HallucinationGraderAgent(llm_config=self.llm_config, **kwargs)

    def _build_advanced_hallucination_grading(
        self, **kwargs
    ) -> AdvancedHallucinationGraderAgent:
        """Build advanced hallucination grading agent."""
        return AdvancedHallucinationGraderAgent(
            llm_config=self.llm_config,
            enable_context_expansion=self.enable_search_tools,
            **kwargs,
        )

    def _build_realtime_hallucination_grading(
        self, **kwargs
    ) -> RealtimeHallucinationGraderAgent:
        """Build realtime hallucination grading agent."""
        return RealtimeHallucinationGraderAgent(llm_config=self.llm_config, **kwargs)

    def _build_quality_assessment(self, **kwargs) -> SimpleAgent:
        """Build quality assessment agent."""
        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=QUALITY_ASSESSMENT_PROMPT,
                output_key="quality_analysis",
            ),
            name=kwargs.get("name", "Quality Assessor"),
        )

    def _build_query_expansion(self, **kwargs) -> SimpleAgent:
        """Build query expansion agent."""
        from haive.agents.rag.multi_query.agent import (
            QUERY_EXPANSION_PROMPT,
            QueryVariations,
        )

        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=QUERY_EXPANSION_PROMPT,
                structured_output_model=QueryVariations,
                output_key="query_variations",
            ),
            name=kwargs.get("name", "Query Expander"),
        )

    def _build_query_analysis(self, **kwargs) -> SimpleAgent:
        """Build query analysis agent."""
        from haive.agents.rag.adaptive.agent import QUERY_ANALYZER_PROMPT, QueryAnalysis

        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=QUERY_ANALYZER_PROMPT,
                structured_output_model=QueryAnalysis,
                output_key="query_analysis",
            ),
            name=kwargs.get("name", "Query Analyzer"),
        )

    def _build_query_decomposition(self, **kwargs) -> QueryDecomposerAgent:
        """Build basic query decomposition agent."""
        return QueryDecomposerAgent(llm_config=self.llm_config, **kwargs)

    def _build_hierarchical_decomposition(
        self, **kwargs
    ) -> HierarchicalQueryDecomposerAgent:
        """Build hierarchical query decomposition agent."""
        return HierarchicalQueryDecomposerAgent(llm_config=self.llm_config, **kwargs)

    def _build_contextual_decomposition(
        self, **kwargs
    ) -> ContextualQueryDecomposerAgent:
        """Build contextual query decomposition agent."""
        return ContextualQueryDecomposerAgent(llm_config=self.llm_config, **kwargs)

    def _build_adaptive_decomposition(self, **kwargs) -> AdaptiveQueryDecomposerAgent:
        """Build adaptive query decomposition agent."""
        return AdaptiveQueryDecomposerAgent(llm_config=self.llm_config, **kwargs)

    def _build_web_search(self, **kwargs) -> SimpleAgent:
        """Build web search agent with tool integration."""
        if not self.enable_search_tools:
            raise ValueError("Search tools not enabled")

        # This would integrate with haive.tools
        try:
            from haive.tools import DuckDuckGoSearchTool, GoogleSearchTool

            # Create tool-enabled agent
            search_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Use web search to find current information about the query.",
                    ),
                    ("human", "Search for: {query}"),
                ]
            )

            return SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=self.llm_config,
                    prompt_template=search_prompt,
                    # Would add tools here in full implementation
                    output_key="web_search_results",
                ),
                name=kwargs.get("name", "Web Searcher"),
            )
        except ImportError:
            # Fallback without tools
            return SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=self.llm_config,
                    prompt_template=ChatPromptTemplate.from_messages(
                        [
                            ("system", "Generate web search results (simulated)."),
                            ("human", "Query: {query}"),
                        ]
                    ),
                    output_key="web_search_results",
                ),
                name=kwargs.get("name", "Web Searcher (Simulated)"),
            )

    def _build_arxiv_search(self, **kwargs) -> SimpleAgent:
        """Build ArXiv search agent."""
        if not self.enable_search_tools:
            raise ValueError("Search tools not enabled")

        try:
            from haive.tools import ArxivTool

            arxiv_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Search ArXiv for academic papers related to the query.",
                    ),
                    ("human", "Search ArXiv for: {query}"),
                ]
            )

            return SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=self.llm_config,
                    prompt_template=arxiv_prompt,
                    output_key="arxiv_results",
                ),
                name=kwargs.get("name", "ArXiv Searcher"),
            )
        except ImportError:
            # Fallback
            return SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=self.llm_config,
                    prompt_template=ChatPromptTemplate.from_messages(
                        [
                            ("system", "Generate ArXiv search results (simulated)."),
                            ("human", "Query: {query}"),
                        ]
                    ),
                    output_key="arxiv_results",
                ),
                name=kwargs.get("name", "ArXiv Searcher (Simulated)"),
            )

    def _build_answer_generation(self, **kwargs) -> SimpleAgent:
        """Build answer generation agent."""
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name=kwargs.get("name", "Answer Generator"),
        )

    def _build_fusion_generation(self, **kwargs) -> SimpleAgent:
        """Build fusion answer generation for multi-source results."""
        fusion_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert at synthesizing information from multiple sources.
            
Combine information from retrieved documents, web search results, and academic papers 
to provide a comprehensive answer. Cite sources and note any conflicting information.""",
                ),
                (
                    "human",
                    """Answer this query using all available sources:

Query: {query}

Retrieved Documents: {retrieved_documents}
Web Search Results: {web_search_results}
ArXiv Results: {arxiv_results}
Grading Results: {grading_results}

Provide a well-sourced, comprehensive answer.""",
                ),
            ]
        )

        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config, prompt_template=fusion_prompt
            ),
            name=kwargs.get("name", "Fusion Generator"),
        )

    # Convenience methods for common patterns
    @classmethod
    def create_graded_hyde_workflow(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        enable_search_tools: bool = False,
        **kwargs,
    ) -> SequentialAgent:
        """Create HyDE → Comprehensive Grading → Answer workflow."""
        factory = cls(
            documents=documents,
            llm_config=llm_config,
            enable_search_tools=enable_search_tools,
        )

        return factory.create_from_schema_compatibility(
            [
                RAGComponent.HYDE_RAG,
                RAGComponent.COMPREHENSIVE_GRADING,
                RAGComponent.ANSWER_GENERATION,
            ],
            **kwargs,
        )

    @classmethod
    def create_decomposed_graded_workflow(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        enable_hallucination_grading: bool = True,
        **kwargs,
    ) -> SequentialAgent:
        """Create Query Decomposition → Retrieval → Grading → Hallucination Check → Answer workflow."""
        factory = cls(
            documents=documents, llm_config=llm_config, enable_search_tools=False
        )

        components = [
            RAGComponent.ADAPTIVE_DECOMPOSITION,
            RAGComponent.BASE_RETRIEVAL,
            RAGComponent.COMPREHENSIVE_GRADING,
        ]

        if enable_hallucination_grading:
            components.append(RAGComponent.ADVANCED_HALLUCINATION_GRADING)

        components.append(RAGComponent.ANSWER_GENERATION)

        return factory.create_from_schema_compatibility(components, **kwargs)

    @classmethod
    def create_modular_rag_workflow(
        cls,
        documents: List[Document],
        components: List[RAGComponent],
        llm_config: Optional[LLMConfig] = None,
        **kwargs,
    ) -> SequentialAgent:
        """Create custom workflow from list of components.

        This is the most generic method - just pass the components you want!
        """
        factory = cls(
            documents=documents, llm_config=llm_config, enable_search_tools=True
        )

        return factory.create_from_schema_compatibility(components, **kwargs)

    @classmethod
    def create_agentic_search_workflow(
        cls, documents: List[Document], llm_config: Optional[LLMConfig] = None, **kwargs
    ) -> ConditionalAgent:
        """Create agentic workflow with search tool integration."""
        factory = cls(
            documents=documents, llm_config=llm_config, enable_search_tools=True
        )

        return factory.create_workflow(pattern=WorkflowPattern.AGENTIC, **kwargs)

    @classmethod
    def create_full_pipeline_workflow(
        cls, documents: List[Document], llm_config: Optional[LLMConfig] = None, **kwargs
    ) -> SequentialAgent:
        """Create comprehensive pipeline with all major components.

        Pipeline: Decomposition → HyDE → Retrieval → Grading → Hallucination Check → Answer
        """
        factory = cls(
            documents=documents, llm_config=llm_config, enable_search_tools=True
        )

        return factory.create_from_schema_compatibility(
            [
                RAGComponent.ADAPTIVE_DECOMPOSITION,
                RAGComponent.HYDE_RAG,
                RAGComponent.COMPREHENSIVE_GRADING,
                RAGComponent.ADVANCED_HALLUCINATION_GRADING,
                RAGComponent.FUSION_GENERATION,
            ],
            **kwargs,
        )

    def build_graph(self) -> BaseGraph:
        """Build graph with compatibility-aware callable sequence."""
        graph = BaseGraph(name=self.name.replace(" ", ""))

        # Add input mapping node if needed
        if self.input_mappings:
            input_mapper = CallableNodeConfig(
                name="input_mapper",
                callable_func=self._create_input_mapper(),
                pass_state=True,
            )
            graph.add_node("input_mapper", input_mapper)
            prev_node = "input_mapper"
            graph.add_edge(START, "input_mapper")
        else:
            prev_node = START

        # Add callable nodes
        for i, callable_func in enumerate(self.callables):
            node_name = f"step_{i}"

            callable_node = CallableNodeConfig(
                name=node_name, callable_func=callable_func, pass_state=True
            )

            graph.add_node(node_name, callable_node)
            graph.add_edge(prev_node, node_name)
            prev_node = node_name

        # Add output mapping node if needed
        if self.output_mappings:
            output_mapper = CallableNodeConfig(
                name="output_mapper",
                callable_func=self._create_output_mapper(),
                pass_state=True,
            )
            graph.add_node("output_mapper", output_mapper)
            graph.add_edge(prev_node, "output_mapper")
            graph.add_edge("output_mapper", END)
        else:
            graph.add_edge(prev_node, END)

        return graph

    def _create_input_mapper(self) -> Callable:
        """Create input mapping function."""

        def input_mapper(input_data: dict) -> dict:
            state = input_data["state"]
            state_dict = (
                state.model_dump() if hasattr(state, "model_dump") else dict(state)
            )

            # Apply input mappings
            mapped_data = {}
            for mapping in self.input_mappings:
                success, value = mapping.apply(state_dict)
                if success:
                    mapped_data[mapping.target_field] = value

            return mapped_data

        return input_mapper

    def _create_output_mapper(self) -> Callable:
        """Create output mapping function."""

        def output_mapper(input_data: dict) -> dict:
            state = input_data["state"]
            state_dict = (
                state.model_dump() if hasattr(state, "model_dump") else dict(state)
            )

            # Apply output mappings
            mapped_data = {}
            for mapping in self.output_mappings:
                success, value = mapping.apply(state_dict)
                if success:
                    mapped_data[mapping.target_field] = value

            return mapped_data

        return output_mapper


# ============================================================================
# PLUG-AND-PLAY COMPONENT CREATION
# ============================================================================


def create_plug_and_play_component(
    component_type: RAGComponent,
    documents: List[Document],
    llm_config: Optional[LLMConfig] = None,
    **kwargs,
) -> Agent:
    """Create any RAG component as a standalone agent.

    This function allows creating any component independently for plug-and-play usage.

    Args:
        component_type: Type of component to create
        documents: Documents for components that need them
        llm_config: LLM configuration
        **kwargs: Component-specific arguments

    Returns:
        Standalone agent that can be plugged into any workflow

    Example:
        # Create standalone components
        decomposer = create_plug_and_play_component(
            RAGComponent.ADAPTIVE_DECOMPOSITION, docs
        )
        hallucination_grader = create_plug_and_play_component(
            RAGComponent.ADVANCED_HALLUCINATION_GRADING, docs
        )

        # Use with any workflow
        workflow = SequentialAgent(agents=[decomposer, retriever, hallucination_grader])
    """
    factory = CompatibleRAGFactory(
        documents=documents,
        llm_config=llm_config,
        enable_search_tools=kwargs.get("enable_search_tools", False),
    )

    if component_type not in factory._component_builders:
        raise ValueError(f"Unknown component type: {component_type}")

    return factory._component_builders[component_type](**kwargs)


def get_component_compatibility_info(
    component_type: RAGComponent,
) -> Dict[str, List[str]]:
    """Get I/O schema information for a component type.

    Args:
        component_type: Component to get info for

    Returns:
        Dict with 'inputs' and 'outputs' lists
    """
    # Import schema functions
    from haive.agents.rag.hallucination_grading.agent import (
        get_hallucination_grader_io_schema,
    )
    from haive.agents.rag.query_decomposition.agent import (
        get_query_decomposer_io_schema,
    )

    # Component schema mappings
    schema_map = {
        # Query components
        RAGComponent.QUERY_DECOMPOSITION: get_query_decomposer_io_schema(),
        RAGComponent.HIERARCHICAL_DECOMPOSITION: get_query_decomposer_io_schema(),
        RAGComponent.CONTEXTUAL_DECOMPOSITION: get_query_decomposer_io_schema(),
        RAGComponent.ADAPTIVE_DECOMPOSITION: get_query_decomposer_io_schema(),
        # Hallucination components
        RAGComponent.HALLUCINATION_GRADING: get_hallucination_grader_io_schema(),
        RAGComponent.ADVANCED_HALLUCINATION_GRADING: get_hallucination_grader_io_schema(),
        RAGComponent.REALTIME_HALLUCINATION_GRADING: get_hallucination_grader_io_schema(),
        # Base components
        RAGComponent.BASE_RETRIEVAL: {
            "inputs": ["query"],
            "outputs": ["retrieved_documents", "messages"],
        },
        RAGComponent.ANSWER_GENERATION: {
            "inputs": ["query", "retrieved_documents", "messages"],
            "outputs": ["response", "generated_response", "messages"],
        },
    }

    return schema_map.get(
        component_type,
        {"inputs": ["query", "messages"], "outputs": ["response", "messages"]},
    )

    # ============================================================================
    # RAG-SPECIFIC FIELD MAPPINGS (LEGACY)
    # ============================================================================

    # Temporarily disabled due to missing FieldMapping import
    # def create_rag_field_mappings() -> List[FieldMapping]:
    """Create common field mappings for RAG workflows."""
    return [
        # Query mappings
        FieldMapping(
            source_path="query",
            target_field="current_query",
            transformer=lambda x: x.strip() if x else "",
        ),
        FieldMapping(
            source_path="query",
            target_field="original_query",
            condition=lambda data: not data.get("original_query"),
            transformer=lambda x: x.strip() if x else "",
        ),
        # Document mappings
        FieldMapping(
            source_path="retrieved_documents",
            target_field="documents",
            transformer=lambda x: x if isinstance(x, list) else [],
        ),
        FieldMapping(
            source_path="documents",
            target_field="retrieved_documents",
            transformer=lambda x: x if isinstance(x, list) else [],
        ),
        # Computed relevant documents from grades
        FieldMapping(
            source_path="graded_documents|retrieved_documents",
            target_field="relevant_documents",
            is_aggregate=True,
            aggregator=lambda values: _extract_relevant_docs(values),
        ),
        # Context preparation
        FieldMapping(
            source_path="relevant_documents|retrieved_documents",
            target_field="context_documents",
            is_aggregate=True,
            aggregator=lambda values: values[0] if values else [],
        ),
        # Quality indicators
        FieldMapping(
            source_path="graded_documents",
            target_field="avg_relevance",
            transformer=_calculate_avg_relevance,
            default_value=0.0,
        ),
        # Workflow state
        FieldMapping(
            source_path="retrieval_count",
            target_field="retrieval_attempts",
            default_value=0,
        ),
    ]


def _extract_relevant_docs(values: List[Any]) -> List[Document]:
    """Extract relevant documents from graded documents and retrieved documents."""
    if not values:
        return []

    graded_docs = values[0] if values and isinstance(values[0], list) else []
    retrieved_docs = (
        values[1] if len(values) > 1 and isinstance(values[1], list) else []
    )

    if not graded_docs:
        return retrieved_docs

    # Get IDs of relevant documents
    relevant_ids = {
        grade.document_id
        for grade in graded_docs
        if getattr(grade, "is_relevant", False)
    }

    # Filter retrieved documents
    relevant_docs = []
    for i, doc in enumerate(retrieved_docs):
        doc_id = f"doc_{i}"
        if hasattr(doc, "metadata") and "id" in doc.metadata:
            doc_id = doc.metadata["id"]

        if doc_id in relevant_ids:
            relevant_docs.append(doc)

    return relevant_docs


def _calculate_avg_relevance(graded_docs: List[Any]) -> float:
    """Calculate average relevance score from graded documents."""
    if not graded_docs:
        return 0.0

    scores = [
        getattr(grade, "relevance_score", 0.0)
        for grade in graded_docs
        if hasattr(grade, "relevance_score")
    ]

    return sum(scores) / len(scores) if scores else 0.0


# ============================================================================
# COMPATIBLE RAG WORKFLOW FACTORIES
# ============================================================================


# ============================================================================
# LEGACY FUNCTIONS (PRESERVED FOR BACKWARDS COMPATIBILITY)
# ============================================================================


def create_compatible_corrective_rag(
    documents: Optional[List[Document]] = None, name: str = "Compatible Corrective RAG"
) -> Agent:
    """Create CRAG agent with compatibility features."""

    # Create retrieval agent
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="Compatible CRAG Retrieval"
    )

    # Create CRAG logic agent with field mappings
    crag_callables = [
        advanced_document_grader,
        relevance_threshold_check,
        requery_decision_maker,
        web_search_simulator,
        response_generator,
        hallucination_detector,
    ]

    # Create field mappings for CRAG
    crag_mappings = create_rag_field_mappings() + [
        # CRAG-specific mappings
        FieldMapping(
            source_path="quality",
            target_field="document_quality",
            default_value="unknown",
        ),
        FieldMapping(
            source_path="needs_web_search",
            target_field="should_use_web_search",
            default_value=False,
        ),
        FieldMapping(
            source_path="web_search_results",
            target_field="external_documents",
            transformer=lambda x: x if isinstance(x, list) else [],
            default_factory=list,
        ),
    ]

    crag_agent = CompatibleRAGAgent(
        name="CRAG Logic Agent",
        callables=crag_callables,
        input_mappings=crag_mappings,
        output_mappings=crag_mappings,
        state_schema=MultiAgentRAGState,
    )

    # Create multi-agent system
    multi_agent = SequentialAgent(
        name=name, agents=[retrieval_agent, crag_agent], state_schema=MultiAgentRAGState
    )

    # Check compatibility
    compatibility_report = crag_agent.check_compatibility_with(retrieval_agent)
    print(f"CRAG Compatibility: {compatibility_report}")

    return multi_agent


def create_compatible_self_rag(
    documents: Optional[List[Document]] = None, name: str = "Compatible Self-RAG"
) -> Agent:
    """Create Self-RAG agent with compatibility features."""

    # Self-RAG specific callables
    def self_rag_retrieval_decision(input_data: dict) -> dict:
        state = input_data["state"]
        query = getattr(state, "query", "").lower()

        needs_external = any(
            term in query
            for term in ["current", "latest", "recent", "today", "price", "cost"]
        )

        return {
            "needs_retrieval": needs_external,
            "retrieval_token": "[Retrieval]" if needs_external else "[No Retrieval]",
            "decision_confidence": 0.8 if needs_external else 0.9,
        }

    self_rag_callables = [
        self_rag_retrieval_decision,
        advanced_document_grader,
        response_generator,
        hallucination_detector,
    ]

    # Self-RAG field mappings
    self_rag_mappings = create_rag_field_mappings() + [
        FieldMapping(
            source_path="retrieval_token",
            target_field="self_rag_decision",
            default_value="[No Retrieval]",
        ),
        FieldMapping(
            source_path="has_hallucination",
            target_field="needs_regeneration",
            default_value=False,
        ),
        FieldMapping(
            source_path="decision_confidence",
            target_field="retrieval_confidence",
            default_value=0.5,
        ),
    ]

    # Create retrieval agent
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="Self-RAG Retrieval"
    )

    # Create Self-RAG logic agent
    self_rag_agent = CompatibleRAGAgent(
        name="Self-RAG Logic Agent",
        callables=self_rag_callables,
        input_mappings=self_rag_mappings,
        output_mappings=self_rag_mappings,
        state_schema=MultiAgentRAGState,
    )

    return SequentialAgent(
        name=name,
        agents=[self_rag_agent, retrieval_agent, self_rag_agent],
        state_schema=MultiAgentRAGState,
    )


def create_compatible_adaptive_rag(
    documents: Optional[List[Document]] = None, name: str = "Compatible Adaptive RAG"
) -> Agent:
    """Create adaptive RAG with compatibility-aware routing."""

    # Create different strategy agents
    simple_rag = SimpleRAGAgent.from_documents(documents or [], name="Simple Strategy")

    # Multi-query strategy
    multi_query_callables = [query_rewriter, response_generator]
    multi_query_mappings = create_rag_field_mappings() + [
        FieldMapping(
            source_path="query_variations",
            target_field="alternative_queries",
            default_factory=list,
        )
    ]

    multi_query_agent = CompatibleRAGAgent(
        name="Multi-Query Strategy",
        callables=multi_query_callables,
        input_mappings=multi_query_mappings,
        state_schema=MultiAgentRAGState,
    )

    # Complex strategy (CRAG)
    complex_agent = create_compatible_corrective_rag(documents, "Complex Strategy")

    # Query analyzer
    analyzer_callables = [query_complexity_analyzer]
    analyzer_mappings = create_rag_field_mappings() + [
        FieldMapping(
            source_path="complexity",
            target_field="query_complexity_level",
            default_value=QueryComplexity.UNKNOWN,
        ),
        FieldMapping(
            source_path="requires_multi_hop",
            target_field="needs_multi_step",
            default_value=False,
        ),
    ]

    analyzer_agent = CompatibleRAGAgent(
        name="Query Analyzer",
        callables=analyzer_callables,
        input_mappings=analyzer_mappings,
        state_schema=MultiAgentRAGState,
    )

    # Create adaptive routing agent
    class CompatibleAdaptiveRAG(ConditionalAgent):
        def __init__(self):
            super().__init__(
                name=name,
                agents=[analyzer_agent, simple_rag, multi_query_agent, complex_agent],
                state_schema=MultiAgentRAGState,
            )

            # Check compatibility between agents
            for agent in self.agents[1:]:  # Skip analyzer
                if hasattr(agent, "check_compatibility_with"):
                    report = agent.check_compatibility_with(analyzer_agent)
                    print(f"Compatibility with {agent.name}: {report}")

            self._setup_adaptive_routing()

        def _setup_adaptive_routing(self):
            def adaptive_router(state) -> str:
                complexity = getattr(state, "complexity", QueryComplexity.UNKNOWN)

                if complexity == QueryComplexity.SIMPLE:
                    return self._get_agent_node_name(self.agents[1])  # simple_rag
                elif complexity == QueryComplexity.MEDIUM:
                    return self._get_agent_node_name(self.agents[2])  # multi_query
                else:
                    return self._get_agent_node_name(self.agents[3])  # complex

            self.add_conditional_edge(
                source_agent=analyzer_agent,
                condition=adaptive_router,
                destinations={
                    self._get_agent_node_name(agent): agent for agent in self.agents[1:]
                },
                default=self.agents[1],  # simple_rag as default
            )

    return CompatibleAdaptiveRAG()


def create_compatible_hyde_rag(
    documents: Optional[List[Document]] = None, name: str = "Compatible HYDE RAG"
) -> Agent:
    """Create HYDE RAG with compatibility features."""

    # HYDE callables

    # HYDE field mappings
    hyde_mappings = create_rag_field_mappings() + [
        FieldMapping(
            source_path="hypothesis",
            target_field="generated_hypothesis",
            default_value="",
        ),
        FieldMapping(
            source_path="hypothesis_confidence",
            target_field="hypothesis_quality",
            default_value=0.0,
        ),
    ]

    # Create agents
    hypothesis_agent = CompatibleRAGAgent(
        name="HYDE Hypothesis Generator",
        callables=[hyde_hypothesis_generator],
        input_mappings=hyde_mappings,
        state_schema=MultiAgentRAGState,
    )

    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="HYDE Retrieval"
    )

    answer_agent = CompatibleRAGAgent(
        name="HYDE Answer Generator",
        callables=[response_generator],
        output_mappings=hyde_mappings,
        state_schema=MultiAgentRAGState,
    )

    return SequentialAgent(
        name=name,
        agents=[hypothesis_agent, retrieval_agent, answer_agent],
        state_schema=MultiAgentRAGState,
    )


# ============================================================================
# MAIN COMPATIBLE FACTORY
# ============================================================================


# ============================================================================
# EXAMPLES AND USAGE PATTERNS
# ============================================================================


def example_modular_rag_usage():
    """Example showing how to use modular RAG components.

    This demonstrates the plug-and-play nature of the system.
    """
    from langchain_core.documents import Document

    # Sample documents
    docs = [Document(page_content="AI is transformative technology")]

    # Method 1: Use pre-built workflows
    workflow1 = CompatibleRAGFactory.create_decomposed_graded_workflow(
        documents=docs, enable_hallucination_grading=True
    )

    # Method 2: Create custom workflow from components
    workflow2 = CompatibleRAGFactory.create_modular_rag_workflow(
        documents=docs,
        components=[
            RAGComponent.QUERY_DECOMPOSITION,
            RAGComponent.HYDE_RAG,
            RAGComponent.ADVANCED_HALLUCINATION_GRADING,
            RAGComponent.FUSION_GENERATION,
        ],
    )

    # Method 3: Create standalone components and combine manually
    decomposer = create_plug_and_play_component(
        RAGComponent.ADAPTIVE_DECOMPOSITION, docs
    )
    hallucination_grader = create_plug_and_play_component(
        RAGComponent.REALTIME_HALLUCINATION_GRADING, docs
    )

    # Combine with any other agents
    from haive.agents.multi.base import SequentialAgent

    workflow3 = SequentialAgent(
        agents=[decomposer, workflow1.agents[1], hallucination_grader],
        schema_separation="smart",  # Uses enhanced compatibility checking
    )

    # Method 4: Runtime agent replacement
    factory = CompatibleRAGFactory(docs)

    # Replace component in existing workflow
    success = factory.replace_agent_in_workflow(
        workflow=workflow1,
        target_agent_name="Comprehensive Grader",
        replacement_component=RAGComponent.REALTIME_HALLUCINATION_GRADING,
    )

    # Method 5: Analyze and optimize workflows
    compatibility = factory.analyze_workflow_compatibility(workflow1)
    suggestions = factory.suggest_workflow_optimizations(workflow1)

    print(f"Compatibility score: {compatibility['compatibility_score']}")
    print(f"Optimization suggestions: {suggestions['routing_suggestions']}")

    return {
        "pre_built": workflow1,
        "modular": workflow2,
        "manual": workflow3,
        "optimized": workflow1,
        "compatibility_report": compatibility,
    }


# Legacy function for backwards compatibility
def create_compatible_rag_workflow(
    workflow_type: str,
    documents: Optional[List[Document]] = None,
    **kwargs,
) -> Agent:
    """Legacy function - use CompatibleRAGFactory.create_workflow() instead."""
    factory = CompatibleRAGFactory(
        documents=documents or [],
        enable_search_tools=kwargs.get("enable_search_tools", False),
    )

    pattern_map = {
        "simple": WorkflowPattern.SIMPLE,
        "graded": WorkflowPattern.GRADED,
        "corrective": WorkflowPattern.CORRECTIVE,
        "adaptive": WorkflowPattern.ADAPTIVE,
        "hyde": WorkflowPattern.HYDE,
        "fusion": WorkflowPattern.FUSION,
        "agentic": WorkflowPattern.AGENTIC,
    }

    if workflow_type not in pattern_map:
        raise ValueError(
            f"Unknown workflow type: {workflow_type}. Available: {list(pattern_map.keys())}"
        )

    return factory.create_workflow(pattern_map[workflow_type], **kwargs)


__all__ = [
    # Main factory class
    "CompatibleRAGFactory",
    # Component and pattern enums
    "RAGComponent",
    "WorkflowPattern",
    # Plug-and-play functions
    "create_plug_and_play_component",
    "get_component_compatibility_info",
    # Pre-built workflow creators
    "CompatibleRAGFactory.create_graded_hyde_workflow",
    "CompatibleRAGFactory.create_decomposed_graded_workflow",
    "CompatibleRAGFactory.create_modular_rag_workflow",
    "CompatibleRAGFactory.create_agentic_search_workflow",
    "CompatibleRAGFactory.create_full_pipeline_workflow",
]
