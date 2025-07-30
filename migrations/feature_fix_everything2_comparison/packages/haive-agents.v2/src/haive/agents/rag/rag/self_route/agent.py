"""Self-Route RAG Agents.

from typing import Any
Implementation of self-routing RAG with dynamic strategy selection and iterative planning.
Uses structured output models for complex routing decisions and preprocessing.
"""

import logging
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class QueryComplexity(str, Enum):
    """Query complexity levels for routing decisions."""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class RoutingStrategy(str, Enum):
    """Available routing strategies."""

    SIMPLE_RAG = "simple_rag"
    CORRECTIVE_RAG = "corrective_rag"
    HYDE_RAG = "hyde_rag"
    MULTI_QUERY_RAG = "multi_query_rag"
    FUSION_RAG = "fusion_rag"
    STEP_BACK_RAG = "step_back_rag"
    ADAPTIVE_RAG = "adaptive_rag"
    SEARCH_ENHANCED_RAG = "search_enhanced_rag"


class QueryAnalysis(BaseModel):
    """Structured analysis of query for routing decisions."""

    original_query: str = Field(description="Original query text")

    # Complexity Analysis
    complexity_level: QueryComplexity = Field(
        description="Overall complexity assessment"
    )
    complexity_score: float = Field(
        ge=0.0, le=1.0, description="Complexity score (0-1)"
    )

    # Query Characteristics
    requires_factual_accuracy: bool = Field(
        description="Needs highly accurate factual information"
    )
    requires_multiple_perspectives: bool = Field(
        description="Benefits from multiple viewpoints"
    )
    requires_domain_expertise: bool = Field(
        description="Needs specialized domain knowledge"
    )
    requires_recent_information: bool = Field(
        description="Needs up-to-date information"
    )
    requires_reasoning: bool = Field(
        description="Involves logical reasoning or inference"
    )

    # Technical Indicators
    named_entities: list[str] = Field(description="Identified named entities")
    domain_topics: list[str] = Field(description="Domain-specific topics")
    query_intent: str = Field(
        description="Primary intent (factual, analytical, creative, etc.)"
    )

    # Preprocessing Requirements
    needs_decomposition: bool = Field(
        description="Would benefit from query decomposition"
    )
    needs_expansion: bool = Field(description="Needs query expansion/reformulation")
    needs_context_enrichment: bool = Field(description="Requires additional context")

    # Routing Recommendations
    primary_strategy: RoutingStrategy = Field(
        description="Primary recommended strategy"
    )
    fallback_strategies: list[RoutingStrategy] = Field(
        description="Alternative strategies"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in routing decision"
    )

    reasoning: str = Field(description="Detailed reasoning for routing decision")


class IterativePlan(BaseModel):
    """Iterative processing plan with loop structure."""

    total_iterations: int = Field(ge=1, le=5, description="Total planned iterations")
    current_iteration: int = Field(ge=0, description="Current iteration number")

    # Per-iteration planning
    iteration_goals: dict[str, str] = Field(description="Goals for each iteration")
    iteration_strategies: dict[str, RoutingStrategy] = Field(
        description="Strategy for each iteration"
    )

    # Loop control
    convergence_criteria: str = Field(description="When to stop iterating")
    quality_threshold: float = Field(
        ge=0.0, le=1.0, description="Quality threshold for completion"
    )

    # State tracking
    accumulated_context: str = Field(
        description="Context accumulated across iterations"
    )
    iteration_results: dict[str, str] = Field(description="Results from each iteration")
    should_continue: bool = Field(description="Whether to continue iterations")

    completion_reason: str | None = Field(description="Why iteration completed")


class RoutingDecision(BaseModel):
    """Final routing decision with execution plan."""

    selected_strategy: RoutingStrategy = Field(description="Chosen strategy")
    execution_plan: dict[str, Any] = Field(description="Detailed execution parameters")

    # Quality assurance
    expected_quality: float = Field(
        ge=0.0, le=1.0, description="Expected result quality"
    )
    risk_factors: list[str] = Field(description="Potential risks or limitations")
    mitigation_strategies: list[str] = Field(description="Risk mitigation approaches")

    # Performance optimization
    estimated_latency: str = Field(description="Expected response time")
    resource_requirements: str = Field(description="Computational resource needs")

    # Fallback planning
    fallback_enabled: bool = Field(description="Whether fallback is configured")
    fallback_trigger: str | None = Field(
        description="Conditions for fallback activation"
    )


# Enhanced prompts with structured output
QUERY_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query analyzer for RAG routing decisions.

Analyze the query across multiple dimensions to determine the optimal routing strategy:

**COMPLEXITY ASSESSMENT:**
- Simple: Straightforward factual questions, single concept
- Moderate: Multi-faceted questions, some reasoning required
- Complex: Multi-step reasoning, domain expertise needed
- Expert: Research-level, requiring deep analysis

**ROUTING STRATEGIES:**
- simple_rag: Basic retrieval for straightforward questions
- corrective_rag: Self-correcting with quality assessment
- hyde_rag: Hypothetical documents for better matching
- multi_query_rag: Query expansion for comprehensive coverage
- fusion_rag: Multiple perspectives with rank fusion
- step_back_rag: Abstract reasoning for complex topics
- adaptive_rag: Dynamic strategy selection
- search_enhanced_rag: External search integration

**ANALYSIS FRAMEWORK:**
1. Parse query structure and intent
2. Assess complexity and domain requirements
3. Identify technical characteristics
4. Determine preprocessing needs
5. Recommend optimal routing strategy

Provide detailed, structured analysis for routing optimization.""",
        ),
        (
            "human",
            """Analyze this query for optimal RAG routing:

**Query:** {query}

**Available Context:** {context}

**Domain Information:** {domain_info}

Provide comprehensive analysis including:
1. Complexity assessment with detailed reasoning
2. Query characteristics and requirements
3. Technical indicators and preprocessing needs
4. Primary routing strategy with confidence
5. Fallback strategies and risk assessment

Focus on actionable routing decisions with clear justification.""",
        ),
    ]
)


ITERATIVE_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at iterative planning for complex RAG workflows.

Design multi-iteration plans that progressively refine results:

**ITERATION PRINCIPLES:**
1. **Progressive Refinement**: Each iteration builds on previous results
2. **Convergence Criteria**: Clear conditions for stopping
3. **Quality Monitoring**: Track improvement across iterations
4. **Adaptive Strategy**: Adjust approach based on intermediate results

**LOOP STRUCTURE:**
- Iteration 1: Initial exploration and baseline
- Iteration 2+: Refinement based on gaps/issues
- Final: Quality validation and synthesis

**CONVERGENCE DETECTION:**
- Quality threshold achieved
- Diminishing returns observed
- Maximum iterations reached
- Satisfactory coverage obtained

Design efficient iterative plans that balance thoroughness with performance.""",
        ),
        (
            "human",
            """Create an iterative plan for this query processing:

**Query:** {query}
**Query Analysis:** {query_analysis}
**Available Strategies:** {available_strategies}

**Current Context:** {current_context}
**Quality Requirements:** {quality_requirements}

Design a plan with:
1. Optimal number of iterations (1-5)
2. Clear goals for each iteration
3. Strategy progression and refinement
4. Convergence criteria and quality thresholds
5. State management across iterations

Focus on efficient convergence with high-quality results.""",
        ),
    ]
)


ROUTING_DECISION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert routing engine for RAG systems.

Make final routing decisions based on query analysis and iterative planning:

**DECISION FRAMEWORK:**
1. **Strategy Selection**: Choose optimal routing strategy
2. **Parameter Optimization**: Configure strategy parameters
3. **Risk Assessment**: Identify potential issues
4. **Fallback Planning**: Prepare contingency strategies
5. **Performance Estimation**: Predict latency and quality

**OPTIMIZATION GOALS:**
- Maximize answer quality and relevance
- Minimize latency and resource usage
- Ensure robustness and reliability
- Provide clear execution guidance

Make data-driven routing decisions with clear justification.""",
        ),
        (
            "human",
            """Make routing decision for this query:

**Query:** {query}
**Query Analysis:** {query_analysis}
**Iterative Plan:** {iterative_plan}

**Available Resources:** {available_resources}
**Performance Requirements:** {performance_requirements}

Provide final routing decision with:
1. Selected strategy with detailed parameters
2. Execution plan and configuration
3. Quality expectations and risk factors
4. Performance estimates and optimization
5. Fallback strategy and trigger conditions

Focus on actionable, optimized routing decisions.""",
        ),
    ]
)


class QueryAnalyzerAgent(Agent):
    """Agent that performs structured query analysis for routing."""

    name: str = "Query Analyzer"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        analysis_depth: str = "comprehensive",
        **kwargs,
    ):
        """Initialize query analyzer.

        Args:
            llm_config: LLM configuration
            analysis_depth: Depth of analysis ("basic", "comprehensive", "expert")
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.analysis_depth = analysis_depth
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build query analysis graph."""
        graph = BaseGraph(name="QueryAnalyzer")

        # Create analysis engine with structured output
        analysis_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=QUERY_ANALYSIS_PROMPT,
            structured_output_model=QueryAnalysis,
            output_key="query_analysis",
        )

        def analyze_query(state: dict[str, Any]) -> dict[str, Any]:
            """Perform comprehensive query analysis."""
            query = getattr(state, "query", "")
            context = getattr(state, "context", "") or getattr(
                state, "retrieved_documents", ""
            )

            # Format context for analysis
            if isinstance(context, list):
                context_str = (
                    "\n".join(
                        [
                            f"Doc {i+1}: {doc.page_content[:150]}..."
                            for i, doc in enumerate(context[:3])
                        ]
                    )
                    if context
                    else "No context available"
                )
            else:
                context_str = (
                    str(context)[:500] + "..."
                    if len(str(context)) > 500
                    else str(context)
                )

            # Extract domain information from query
            domain_info = self._extract_domain_info(query)

            # Perform structured analysis
            analysis_result = analysis_engine.invoke(
                {"query": query, "context": context_str, "domain_info": domain_info}
            )

            return {
                "query_analysis": analysis_result,
                "complexity_level": analysis_result.complexity_level,
                "complexity_score": analysis_result.complexity_score,
                "primary_strategy": analysis_result.primary_strategy,
                "fallback_strategies": analysis_result.fallback_strategies,
                "routing_confidence": analysis_result.confidence,
                "analysis_reasoning": analysis_result.reasoning,
                "preprocessing_requirements": {
                    "needs_decomposition": analysis_result.needs_decomposition,
                    "needs_expansion": analysis_result.needs_expansion,
                    "needs_context_enrichment": analysis_result.needs_context_enrichment,
                },
            }

        graph.add_node("analyze_query", analyze_query)
        graph.add_edge(START, "analyze_query")
        graph.add_edge("analyze_query", END)

        return graph

    def _extract_domain_info(self, query: str) -> str:
        """Extract domain information from query."""
        # Simple domain key detection
        domain_keywords = {
            "ai": [
                "artificial intelligence",
                "machine learning",
                "neural network",
                "deep learning",
            ],
            "medicine": ["medical", "disease", "treatment", "diagnosis", "health"],
            "finance": ["financial", "market", "investment", "trading", "economy"],
            "technology": ["software", "programming", "computer", "algorithm", "data"],
            "science": ["research", "experiment", "theory", "hypothesis", "analysis"],
        }

        query_lower = query.lower()
        detected_domains = []

        for domain, keywords in domain_keywords.items():
            if any(key in query_lower for key in keywords):
                detected_domains.append(domain)

        return (
            f"Detected domains: {', '.join(detected_domains)}"
            if detected_domains
            else "General domain"
        )


class IterativePlannerAgent(Agent):
    """Agent that creates iterative processing plans."""

    name: str = "Iterative Planner"

    def __init__(
        self, llm_config: LLMConfig | None = None, max_iterations: int = 3, **kwargs
    ):
        """Initialize iterative planner.

        Args:
            llm_config: LLM configuration
            max_iterations: Maximum number of iterations
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.max_iterations = max_iterations
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build iterative planning graph."""
        graph = BaseGraph(name="IterativePlanner")

        # Create planning engine with structured output
        planning_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=ITERATIVE_PLANNING_PROMPT,
            structured_output_model=IterativePlan,
            output_key="iterative_plan",
        )

        def create_iterative_plan(state: dict[str, Any]) -> dict[str, Any]:
            """Create structured iterative plan."""
            query = getattr(state, "query", "")
            query_analysis = getattr(state, "query_analysis", None)
            current_context = getattr(state, "context", "") or getattr(
                state, "retrieved_documents", ""
            )

            # Available strategies based on analysis
            available_strategies = [strategy.value for strategy in RoutingStrategy]
            if query_analysis:
                # Prioritize recommended strategies
                available_strategies = (
                    [query_analysis.primary_strategy.value]
                    + [s.value for s in query_analysis.fallback_strategies]
                    + available_strategies
                )
                # Remove duplicates while preserving order
                available_strategies = list(dict.fromkeys(available_strategies))

            # Quality requirements based on complexity
            quality_requirements = (
                "high"
                if hasattr(query_analysis, "complexity_level")
                and query_analysis.complexity_level
                in [QueryComplexity.COMPLEX, QueryComplexity.EXPERT]
                else "moderate"
            )

            # Create iterative plan
            plan_result = planning_engine.invoke(
                {
                    "query": query,
                    "query_analysis": (
                        str(query_analysis)
                        if query_analysis
                        else "No analysis available"
                    ),
                    "available_strategies": ", ".join(available_strategies),
                    "current_context": (
                        str(current_context)[:300] + "..."
                        if len(str(current_context)) > 300
                        else str(current_context)
                    ),
                    "quality_requirements": quality_requirements,
                }
            )

            # Ensure plan doesn't exceed max iterations
            plan_result.total_iterations = min(
                plan_result.total_iterations, self.max_iterations
            )

            return {
                "iterative_plan": plan_result,
                "total_iterations": plan_result.total_iterations,
                "iteration_goals": plan_result.iteration_goals,
                "iteration_strategies": plan_result.iteration_strategies,
                "convergence_criteria": plan_result.convergence_criteria,
                "quality_threshold": plan_result.quality_threshold,
            }

        graph.add_node("create_plan", create_iterative_plan)
        graph.add_edge(START, "create_plan")
        graph.add_edge("create_plan", END)

        return graph


class RoutingDecisionAgent(Agent):
    """Agent that makes final routing decisions."""

    name: str = "Routing Decision Engine"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        enable_fallback: bool = True,
        **kwargs,
    ):
        """Initialize routing decision agent.

        Args:
            llm_config: LLM configuration
            enable_fallback: Whether to enable fallback strategies
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.enable_fallback = enable_fallback
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build routing decision graph."""
        graph = BaseGraph(name="RoutingDecision")

        # Create decision engine with structured output
        decision_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=ROUTING_DECISION_PROMPT,
            structured_output_model=RoutingDecision,
            output_key="routing_decision",
        )

        def make_routing_decision(state: dict[str, Any]) -> dict[str, Any]:
            """Make final routing decision."""
            query = getattr(state, "query", "")
            query_analysis = getattr(state, "query_analysis", None)
            iterative_plan = getattr(state, "iterative_plan", None)

            # Available resources and performance requirements
            available_resources = (
                "standard"  # Could be configured based on system state
            )
            performance_requirements = (
                "balanced"  # Could be derived from query analysis
            )

            # Make routing decision
            decision_result = decision_engine.invoke(
                {
                    "query": query,
                    "query_analysis": (
                        str(query_analysis)
                        if query_analysis
                        else "No analysis available"
                    ),
                    "iterative_plan": (
                        str(iterative_plan) if iterative_plan else "No iterative plan"
                    ),
                    "available_resources": available_resources,
                    "performance_requirements": performance_requirements,
                }
            )

            # Configure fallback if enabled
            if self.enable_fallback and not decision_result.fallback_enabled:
                decision_result.fallback_enabled = True
                decision_result.fallback_trigger = "quality_threshold_not_met"

            return {
                "routing_decision": decision_result,
                "selected_strategy": decision_result.selected_strategy,
                "execution_plan": decision_result.execution_plan,
                "expected_quality": decision_result.expected_quality,
                "risk_factors": decision_result.risk_factors,
                "fallback_enabled": decision_result.fallback_enabled,
                "routing_complete": True,
            }

        graph.add_node("make_decision", make_routing_decision)
        graph.add_edge(START, "make_decision")
        graph.add_edge("make_decision", END)

        return graph


class SelfRouteRAGAgent(SequentialAgent):
    """Complete Self-Route RAG agent with structured analysis and iterative planning."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        analysis_depth: str = "comprehensive",
        max_iterations: int = 3,
        enable_fallback: bool = True,
        **kwargs,
    ):
        """Create Self-Route RAG agent from documents.

        Args:
            documents: Documents to index
            llm_config: LLM configuration
            analysis_depth: Depth of query analysis
            max_iterations: Maximum iterations for planning
            enable_fallback: Whether to enable fallback routing
            **kwargs: Additional arguments

        Returns:
            SelfRouteRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: Query analysis with structured output
        query_analyzer = QueryAnalyzerAgent(
            llm_config=llm_config, analysis_depth=analysis_depth, name="Query Analyzer"
        )

        # Step 2: Iterative planning with loop structure
        iterative_planner = IterativePlannerAgent(
            llm_config=llm_config,
            max_iterations=max_iterations,
            name="Iterative Planner",
        )

        # Step 3: Final routing decision
        routing_decision = RoutingDecisionAgent(
            llm_config=llm_config,
            enable_fallback=enable_fallback,
            name="Routing Decision Engine",
        )

        # Step 4: Strategy executor (would execute the chosen strategy)
        strategy_executor = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are a strategy execution coordinator. Execute the routing decision.",
                        ),
                        (
                            "human",
                            "Execute routing strategy: {selected_strategy}\nExecution plan: {execution_plan}\nQuery: {query}",
                        ),
                    ]
                ),
            ),
            name="Strategy Executor",
        )

        return cls(
            agents=[
                query_analyzer,
                iterative_planner,
                routing_decision,
                strategy_executor,
            ],
            name=kwargs.get("name", "Self-Route RAG Agent"),
            **kwargs,
        )


# Factory function
def create_self_route_rag_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    routing_mode: str = "adaptive",
    **kwargs,
) -> SelfRouteRAGAgent:
    """Create a Self-Route RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        routing_mode: Routing mode ("conservative", "adaptive", "aggressive")
        **kwargs: Additional arguments

    Returns:
        Configured Self-Route RAG agent
    """
    # Adjust parameters based on routing mode
    if routing_mode == "conservative":
        kwargs.setdefault("analysis_depth", "basic")
        kwargs.setdefault("max_iterations", 2)
        kwargs.setdefault("enable_fallback", True)
    elif routing_mode == "aggressive":
        kwargs.setdefault("analysis_depth", "expert")
        kwargs.setdefault("max_iterations", 5)
        kwargs.setdefault("enable_fallback", False)
    else:  # adaptive
        kwargs.setdefault("analysis_depth", "comprehensive")
        kwargs.setdefault("max_iterations", 3)
        kwargs.setdefault("enable_fallback", True)

    return SelfRouteRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_self_route_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Self-Route RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "query_analysis",
            "complexity_level",
            "complexity_score",
            "primary_strategy",
            "fallback_strategies",
            "routing_confidence",
            "analysis_reasoning",
            "preprocessing_requirements",
            "iterative_plan",
            "total_iterations",
            "iteration_goals",
            "iteration_strategies",
            "convergence_criteria",
            "quality_threshold",
            "routing_decision",
            "selected_strategy",
            "execution_plan",
            "expected_quality",
            "risk_factors",
            "fallback_enabled",
            "routing_complete",
            "response",
            "messages",
        ],
    }
