"""RAG (Retrieval-Augmented Generation) Module.

Comprehensive RAG implementations with multi-agent orchestration, document grading,
hallucination detection, and adaptive retrieval strategies. Built on the Haive
multi-agent framework for flexible composition and routing.

Key Features:
    - Multiple RAG architectures (Simple, Corrective, HyDE, Multi-Query, Adaptive)
    - Advanced document grading and quality assessment
    - Hallucination detection and mitigation
    - Search tool integration (Google, DuckDuckGo, ArXiv)
    - Composable workflows with I/O schema compatibility
    - Conditional routing based on query complexity
    - ReAct pattern integration for tool usage

Available RAG Agents:
    - SimpleRAGAgent: Basic retrieval → answer generation
    - CorrectiveRAGAgent: Self-correcting with document grading
    - HyDERAGAgent: Hypothetical Document Embeddings for better matching
    - MultiQueryRAGAgent: Query expansion for improved recall
    - AdaptiveRAGAgent: Dynamic strategy selection based on complexity
    - DocumentGradingAgent: Standalone document quality assessment
    - RAGFusionAgent: Multi-query with reciprocal rank fusion
    - StepBackRAGAgent: Abstract reasoning with step-back prompting
    - SelfRouteRAGAgent: Dynamic routing with structured analysis
    - SpeculativeRAGAgent: Parallel hypothesis generation and verification
    - MemoryAwareRAGAgent: Persistent context and iterative learning

Example:
    Basic RAG workflow::

        from haive.agents.rag import SimpleRAGAgent
        from haive.agents.rag.factories import CompatibleRAGFactory
        from langchain_core.documents import Document

        # Simple RAG
        docs = [Document(page_content="AI is transformative technology")]
        agent = SimpleRAGAgent.from_documents(docs)
        result = agent.run({"query": "What is AI?"})

        # Composable workflow with grading
        workflow = CompatibleRAGFactory.create_graded_hyde_workflow(
            documents=docs,
            enable_search_tools=True
        )
        result = workflow.run({"query": "Latest AI developments"})

    Advanced adaptive routing::

        from haive.agents.rag import AdaptiveRAGAgent

        # Automatically routes based on query complexity
        adaptive_agent = AdaptiveRAGAgent.from_documents(docs)

        # Simple query → SimpleRAG
        result1 = adaptive_agent.run({"query": "What is machine learning?"})

        # Complex query → HyDE + Multi-Query
        result2 = adaptive_agent.run({"query": "How do transformer attention mechanisms enable emergent capabilities in large language models?"})

    Modular plug-and-play components::

        from haive.agents.rag import (
            create_plug_and_play_component,
            RAGComponent,
            CompatibleRAGFactory
        )
        from haive.agents.multi.base import SequentialAgent

        # Create standalone components
        decomposer = create_plug_and_play_component(
            RAGComponent.ADAPTIVE_DECOMPOSITION, docs
        )
        hallucination_grader = create_plug_and_play_component(
            RAGComponent.ADVANCED_HALLUCINATION_GRADING, docs
        )

        # Combine with any workflow
        workflow = SequentialAgent(
            agents=[decomposer, simple_rag, hallucination_grader],
            schema_separation="smart"  # Uses I/O compatibility checking
        )

        # Or use the factory for common patterns
        full_pipeline = CompatibleRAGFactory.create_full_pipeline_workflow(
            documents=docs,
            enable_search_tools=True
        )

        # Replace components at runtime
        factory = CompatibleRAGFactory(docs)
        success = factory.replace_agent_in_workflow(
            workflow=full_pipeline,
            target_agent_name="Advanced Hallucination Grader",
            replacement_component=RAGComponent.REALTIME_HALLUCINATION_GRADING
        )

See Also:
    :mod:`haive.agents.rag.base`: Core RAG functionality and BaseRAGAgent
    :mod:`haive.agents.rag.simple`: Basic RAG implementation
    :mod:`haive.agents.rag.corrective`: Self-correcting RAG with grading
    :mod:`haive.agents.rag.hyde`: Hypothetical Document Embeddings
    :mod:`haive.agents.rag.multi_query`: Query expansion for better recall
    :mod:`haive.agents.rag.adaptive`: Dynamic strategy selection
    :mod:`haive.agents.rag.common`: Shared components (graders, generators)
    :mod:`haive.agents.rag.factories`: Workflow builders and composers
    :mod:`haive.agents.rag.hallucination_grading`: Modular hallucination detection agents
    :mod:`haive.agents.rag.query_decomposition`: Modular query decomposition agents
    :mod:`haive.agents.rag.fusion`: RAG Fusion with reciprocal rank fusion
    :mod:`haive.agents.rag.step_back`: Step-back prompting for abstract reasoning
    :mod:`haive.agents.rag.self_route`: Self-routing with dynamic strategy selection
    :mod:`haive.agents.rag.speculative`: Speculative RAG with parallel hypothesis processing
    :mod:`haive.agents.rag.memory_aware`: Memory-aware RAG with persistent learning
"""

from .adaptive.agent import AdaptiveRAGAgent

# Base components
from .base.agent import BaseRAGAgent
from .corrective.agent_v2 import CorrectiveRAGAgentV2

# Factories for composable workflows
from .factories.compatible_rag_factory_simple import (
    CompatibleRAGFactory,
    RAGComponent,
    WorkflowPattern,
    create_plug_and_play_component,
    get_component_compatibility_info,
)

# Advanced RAG architectures
# from .fusion.agent import RAGFusionAgent, ReciprocalRankFusionAgent  # Temporarily disabled - missing rag_state
from .hallucination_grading.agent import (
    AdvancedHallucinationGraderAgent,
    HallucinationGraderAgent,
    RealtimeHallucinationGraderAgent,
    create_hallucination_grader,
)
from .hyde.agent_v2 import HyDERAGAgentV2
from .memory_aware.agent import MemoryAwareRAGAgent, MemoryRetrievalAgent
from .multi_query.agent import MultiQueryRAGAgent
from .query_decomposition.agent import (
    AdaptiveQueryDecomposerAgent,
    ContextualQueryDecomposerAgent,
    HierarchicalQueryDecomposerAgent,
    QueryDecomposerAgent,
    create_query_decomposer,
)
from .self_route.agent import QueryAnalyzerAgent, SelfRouteRAGAgent

# Core RAG agents
from .simple.agent import SimpleRAGAgent
from .speculative.agent import HypothesisGeneratorAgent, SpeculativeRAGAgent
from .step_back.agent import StepBackQueryGeneratorAgent, StepBackRAGAgent

# Temporarily disabled due to import issues

__all__ = [
    "AdaptiveQueryDecomposerAgent",
    "AdaptiveRAGAgent",
    "AdvancedHallucinationGraderAgent",
    # Base components
    "BaseRAGAgent",
    # Workflow factories and components
    "CompatibleRAGFactory",
    "ContextualQueryDecomposerAgent",
    "CorrectiveRAGAgentV2",
    # "DocumentGradingAgent",  # Temporarily disabled - missing callable_node
    # Modular Hallucination Graders
    "HallucinationGraderAgent",
    "HierarchicalQueryDecomposerAgent",
    "HyDERAGAgentV2",
    "HypothesisGeneratorAgent",
    "MemoryAwareRAGAgent",
    "MemoryRetrievalAgent",
    "MultiQueryRAGAgent",
    "QueryAnalyzerAgent",
    # Modular Query Decomposers
    "QueryDecomposerAgent",
    # "RAGWorkflowFactory",  # Temporarily disabled
    "RAGComponent",
    "RealtimeHallucinationGraderAgent",
    "SelfRouteRAGAgent",
    # Core RAG Agents
    "SimpleRAGAgent",
    "SpeculativeRAGAgent",
    "StepBackQueryGeneratorAgent",
    # Advanced RAG Architectures
    # "RAGFusionAgent",  # Temporarily disabled - missing rag_state
    # "ReciprocalRankFusionAgent",  # Temporarily disabled - missing rag_state
    "StepBackRAGAgent",
    "WorkflowPattern",
    "create_hallucination_grader",
    "create_plug_and_play_component",
    "create_query_decomposer",
    "get_component_compatibility_info",
]
