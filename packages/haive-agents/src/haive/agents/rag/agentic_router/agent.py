"""Agentic RAG Router with ReAct Pattern Agents.

Implementation of autonomous RAG routing using ReAct (Reason + Act) patterns.
Provides intelligent agent selection, strategy planning, and execution coordination.
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
from haive.agents.rag.flare.agent import FLARERAGAgent
from haive.agents.rag.fusion.agent import RAGFusionAgent
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class RAGStrategy(str, Enum):
    """Available RAG strategies for routing."""

    SIMPLE = "simple"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"
    FUSION = "fusion"
    FLARE = "flare"
    ADAPTIVE = "adaptive"
    CORRECTIVE = "corrective"


class ReasoningStep(BaseModel):
    """Individual reasoning step in ReAct pattern."""

    step_number: int = Field(description="Step number in reasoning chain")
    thought: str = Field(description="Reasoning or thought process")
    action: str = Field(description="Action to take based on reasoning")
    observation: str = Field(description="Observation from action result")

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in this reasoning step"
    )
    next_step_needed: bool = Field(
        description="Whether another reasoning step is needed"
    )


class ReActPlan(BaseModel):
    """Complete ReAct planning result."""

    query_analysis: str = Field(description="Analysis of the input query")
    reasoning_chain: list[ReasoningStep] = Field(description="Chain of reasoning steps")

    # Strategy selection
    selected_strategy: RAGStrategy = Field(description="Selected RAG strategy")
    strategy_confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in strategy selection"
    )
    fallback_strategies: list[RAGStrategy] = Field(
        description="Fallback strategies if primary fails"
    )

    # Execution planning
    execution_steps: list[str] = Field(description="Planned execution steps")
    success_criteria: list[str] = Field(description="Criteria for successful execution")
    failure_handling: str = Field(description="How to handle execution failures")

    # Resource estimation
    estimated_complexity: float = Field(
        ge=0.0, le=1.0, description="Estimated query complexity"
    )
    estimated_time: float = Field(description="Estimated processing time")
    resource_requirements: dict[str, Any] = Field(description="Required resources")

    planning_metadata: dict[str, Any] = Field(
        description="Additional planning metadata"
    )


class ExecutionResult(BaseModel):
    """Result from strategy execution."""

    strategy_used: RAGStrategy = Field(description="Strategy that was executed")
    execution_successful: bool = Field(description="Whether execution was successful")

    # Performance metrics
    execution_time: float = Field(description="Actual execution time")
    retrieval_count: int = Field(description="Number of retrieval operations")
    processing_steps: int = Field(description="Number of processing steps")

    # Quality metrics
    result_confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in result quality"
    )
    completeness_score: float = Field(
        ge=0.0, le=1.0, description="Completeness of answer"
    )
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Relevance to original query"
    )

    # Content
    final_response: str = Field(description="Final generated response")
    supporting_evidence: list[str] = Field(description="Key supporting evidence")
    source_documents: list[Document] = Field(description="Source documents used")

    # Error handling
    errors_encountered: list[str] = Field(description="Any errors during execution")
    fallback_used: bool = Field(description="Whether fallback strategy was used")

    execution_metadata: dict[str, Any] = Field(description="Execution statistics")


class AgenticRouterResult(BaseModel):
    """Complete result from agentic RAG routing."""

    original_query: str = Field(description="Original query")
    final_response: str = Field(description="Final generated response")

    # Reasoning analytics
    reasoning_steps: int = Field(description="Number of reasoning steps")
    decision_confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in routing decision"
    )
    autonomous_decisions: int = Field(description="Number of autonomous decisions made")

    # Strategy analytics
    primary_strategy: RAGStrategy = Field(description="Primary strategy selected")
    strategies_considered: list[RAGStrategy] = Field(
        description="All strategies considered"
    )
    strategy_switch_count: int = Field(description="Number of strategy switches")

    # Performance analytics
    total_processing_time: float = Field(description="Total processing time")
    efficiency_score: float = Field(ge=0.0, le=1.0, description="Processing efficiency")
    resource_utilization: dict[str, float] = Field(
        description="Resource utilization metrics"
    )

    # Quality analytics
    answer_quality: float = Field(ge=0.0, le=1.0, description="Overall answer quality")
    reasoning_quality: float = Field(
        ge=0.0, le=1.0, description="Quality of reasoning process"
    )
    evidence_strength: float = Field(
        ge=0.0, le=1.0, description="Strength of supporting evidence"
    )

    processing_metadata: dict[str, Any] = Field(
        description="Complete processing metadata"
    )


# Enhanced prompts for agentic routing with ReAct
REACT_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert agentic RAG router using ReAct (Reason + Act) patterns.

**REACT METHODOLOGY:**
1. **REASON**: Analyze the query, consider options, evaluate trade-offs
2. **ACT**: Select and plan specific actions based on reasoning
3. **OBSERVE**: Evaluate results and plan next steps iteratively

**AVAILABLE RAG STRATEGIES:**
- **Simple**: Direct retrieval and generation, fastest but basic
- **Multi-Query**: Multiple query variations, better coverage
- **HyDE**: Hypothetical document expansion, good for abstract queries
- **Fusion**: Reciprocal rank fusion, high-quality results
- **FLARE**: Forward-looking active retrieval, iterative improvement
- **Adaptive**: Context-aware strategy selection, balanced approach
- **Corrective**: Self-correcting with quality checks, most robust

**REASONING FRAMEWORK:**
1. Query complexity analysis and requirements identification
2. Available resource assessment and constraint evaluation
3. Strategy comparison across multiple dimensions
4. Risk assessment and fallback planning
5. Execution pathway optimization

**DECISION CRITERIA:**
- Query complexity and type
- Required accuracy vs. speed trade-offs
- Available computational resources
- Expected result quality requirements
- Risk tolerance for errors

Use systematic reasoning to select optimal RAG strategies.""",
        ),
        (
            """human""",
            """Plan RAG strategy using ReAct reasoning:

**Query:** {query}

**Context:** {context}

**Available Resources:** {available_resources}

**Requirements:** {requirements}

**Previous Context:** {previous_results}

**REASONING TASK:**
1. Analyze the query characteristics and requirements
2. Reason through available RAG strategy options
3. Consider resource constraints and quality requirements
4. Plan step-by-step execution approach
5. Identify success criteria and failure handling

Use ReAct methodology - provide clear reasoning for each decision point.""",
        ),
    ]
)


STRATEGY_EXECUTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at executing RAG strategies based on agentic routing decisions.

**EXECUTION PRINCIPLES:**
1. **Fidelity**: Execute exactly as planned, maintaining strategy intent
2. **Monitoring**: Track execution progress and quality continuously
3. **Adaptation**: Adapt to unexpected conditions while preserving goals
4. **Efficiency**: Optimize execution for speed and resource usage
5. **Quality**: Maintain high standards throughout execution

**EXECUTION MONITORING:**
- Track retrieval effectiveness and document quality
- Monitor generation coherence and factual accuracy
- Assess resource utilization and performance metrics
- Evaluate adherence to success criteria
- Detect and handle execution anomalies

**QUALITY CONTROL:**
- Validate retrieval relevance at each step
- Check generation consistency with evidence
- Verify completeness against query requirements
- Assess confidence levels throughout process
- Implement quality gates and checkpoints

Execute the planned strategy with precision and continuous quality monitoring.""",
        ),
        (
            """human""",
            """Execute RAG strategy based on agentic routing plan:

**Original Query:** {query}

**Selected Strategy:** {selected_strategy}

**Execution Plan:** {execution_plan}

**Available Documents:** {documents_summary}

**Success Criteria:** {success_criteria}

**Resource Constraints:** {resource_constraints}

**EXECUTION TASK:**
1. Execute the planned RAG strategy step-by-step
2. Monitor quality and performance at each stage
3. Apply quality controls and validation checks
4. Generate comprehensive final response
5. Evaluate execution success against criteria

Focus on high-quality execution with continuous monitoring and validation.""",
        ),
    ]
)


AGENTIC_SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at synthesizing results from agentic RAG routing processes.

**SYNTHESIS PRINCIPLES:**
1. **Integration**: Combine reasoning, execution, and results coherently
2. **Evaluation**: Assess quality of the complete agentic process
3. **Transparency**: Provide clear insight into decision-making process
4. **Optimization**: Identify improvements for future routing decisions
5. **Completeness**: Ensure comprehensive coverage of original query

**QUALITY ASSESSMENT:**
- Evaluate reasoning quality and decision appropriateness
- Assess strategy execution effectiveness and efficiency
- Measure result quality against original query requirements
- Analyze resource utilization and process optimization
- Identify lessons learned for future improvements

**RESULT INTEGRATION:**
- Synthesize final response from all processing stages
- Integrate supporting evidence and reasoning traces
- Maintain transparency about decision processes
- Provide confidence assessments and quality metrics
- Include actionable insights for process improvement

Create comprehensive, high-quality final results with full process transparency.""",
        ),
        (
            """human""",
            """Synthesize agentic RAG routing results:

**Original Query:** {query}

**ReAct Planning:** {react_plan}

**Execution Results:** {execution_results}

**Strategy Performance:** {strategy_performance}

**Quality Metrics:** {quality_metrics}

**Resource Usage:** {resource_usage}

**SYNTHESIS TASK:**
1. Integrate all results into coherent final response
2. Evaluate overall process quality and effectiveness
3. Assess reasoning and execution quality
4. Provide transparency about decision-making process
5. Generate comprehensive result with metadata

Focus on creating the highest quality integrated result with full process insight.""",
        ),
    ]
)


class AgenticRAGRouterAgent(Agent):
    """Complete Agentic RAG Router with ReAct patterns and autonomous decision-making.

    This agent uses conditional edges to route between different RAG strategies based on
    query analysis and planning.
    """

    name: str = "Agentic RAG Router"
    documents: list[Document] = Field(description="Documents for RAG strategies")
    llm_config: LLMConfig = Field(description="LLM configuration")
    autonomy_level: str = Field(default="high", description="Autonomy level")

    # Engines for different stages (initialized in setup_agent)
    planning_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for ReAct planning"
    )
    synthesis_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for result synthesis"
    )
    strategy_agents: dict[RAGStrategy, Agent] | None = Field(
        default=None, description="RAG strategy agents"
    )

    def setup_agent(self) -> None:
        """Initialize engines and strategy agents."""
        # Create planning engine
        self.planning_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=REACT_PLANNING_PROMPT,
            structured_output_model=ReActPlan,
            output_key="react_plan",
        )

        # Create synthesis engine
        self.synthesis_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=AGENTIC_SYNTHESIS_PROMPT,
            structured_output_model=AgenticRouterResult,
            output_key="agentic_result",
        )

        # Create strategy agents
        self.strategy_agents = {
            RAGStrategy.SIMPLE: SimpleRAGAgent.from_documents(
                documents=self.documents, llm_config=self.llm_config
            ),
            RAGStrategy.MULTI_QUERY: MultiQueryRAGAgent.from_documents(
                documents=self.documents, llm_config=self.llm_config
            ),
            RAGStrategy.HYDE: HyDERAGAgentV2.from_documents(
                documents=self.documents, llm_config=self.llm_config
            ),
            RAGStrategy.FUSION: RAGFusionAgent.from_documents(
                documents=self.documents, llm_config=self.llm_config
            ),
            RAGStrategy.FLARE: FLARERAGAgent.from_documents(
                documents=self.documents, llm_config=self.llm_config
            ),
        }

        # Add engines to registry
        self.engines["planning"] = self.planning_engine
        self.engines["synthesis"] = self.synthesis_engine

    def plan_react_strategy(self, state: RAGState) -> dict[str, Any]:
        """Plan RAG strategy using ReAct reasoning."""
        query = state.query
        context = getattr(state, "context", "")

        # Analyze available resources
        available_resources = f"{len(self.documents)} documents available"
        requirements = f"Autonomy level: {self.autonomy_level}"
        previous_results = getattr(state, "previous_results", "No previous context")

        # Create ReAct plan
        react_plan = self.planning_engine.invoke(
            {
                "query": query,
                "context": context,
                "available_resources": available_resources,
                "requirements": requirements,
                "previous_results": previous_results,
            }
        )

        logger.info(
            f"ReAct planning: Strategy={react_plan.selected_strategy}, Confidence={react_plan.strategy_confidence}"
        )

        return {
            "react_plan": react_plan,
            "selected_strategy": react_plan.selected_strategy,
            "strategy_confidence": react_plan.strategy_confidence,
            "fallback_strategies": react_plan.fallback_strategies,
            "execution_steps": react_plan.execution_steps,
            "success_criteria": react_plan.success_criteria,
            "estimated_complexity": react_plan.estimated_complexity,
            "reasoning_steps": len(react_plan.reasoning_chain),
        }

    def execute_simple_strategy(self, state: RAGState) -> dict[str, Any]:
        """Execute simple RAG strategy."""
        logger.info("Executing simple RAG strategy")
        result = self.strategy_agents[RAGStrategy.SIMPLE].run({"query": state.query})
        return self._process_strategy_result(state, result, RAGStrategy.SIMPLE)

    def execute_multi_query_strategy(self, state: RAGState) -> dict[str, Any]:
        """Execute multi-query RAG strategy."""
        logger.info("Executing multi-query RAG strategy")
        result = self.strategy_agents[RAGStrategy.MULTI_QUERY].run(
            {"query": state.query}
        )
        return self._process_strategy_result(state, result, RAGStrategy.MULTI_QUERY)

    def execute_hyde_strategy(self, state: RAGState) -> dict[str, Any]:
        """Execute HyDE RAG strategy."""
        logger.info("Executing HyDE RAG strategy")
        result = self.strategy_agents[RAGStrategy.HYDE].run({"query": state.query})
        return self._process_strategy_result(state, result, RAGStrategy.HYDE)

    def execute_fusion_strategy(self, state: RAGState) -> dict[str, Any]:
        """Execute fusion RAG strategy."""
        logger.info("Executing fusion RAG strategy")
        result = self.strategy_agents[RAGStrategy.FUSION].run({"query": state.query})
        return self._process_strategy_result(state, result, RAGStrategy.FUSION)

    def execute_flare_strategy(self, state: RAGState) -> dict[str, Any]:
        """Execute FLARE RAG strategy."""
        logger.info("Executing FLARE RAG strategy")
        result = self.strategy_agents[RAGStrategy.FLARE].run({"query": state.query})
        return self._process_strategy_result(state, result, RAGStrategy.FLARE)

    def _process_strategy_result(
        self, state: RAGState, result: dict[str, Any], strategy: RAGStrategy
    ) -> dict[str, Any]:
        """Process the result from a strategy execution."""
        return {
            "execution_result": result,
            "execution_successful": True,
            "final_response": result.get("response", ""),
            "strategy_used": strategy,
            "messages": state.messages,
        }

    def synthesize_agentic_result(self, state: RAGState) -> dict[str, Any]:
        """Synthesize final agentic routing result."""
        query = state.query
        react_plan = getattr(state, "react_plan", None)
        execution_result = getattr(state, "execution_result", None)
        final_response = getattr(state, "final_response", "")
        execution_successful = getattr(state, "execution_successful", False)
        strategy_used = getattr(state, "strategy_used", None)

        # Prepare synthesis inputs
        react_plan_summary = "No ReAct plan available"
        if react_plan:
            react_plan_summary = f"Strategy: {react_plan.selected_strategy}, Steps: {len(react_plan.reasoning_chain)}"

        execution_summary = f"Success: {execution_successful}"
        if execution_result:
            execution_summary += f", Response length: {len(final_response)}"

        strategy_performance = (
            f"Strategy used: {strategy_used if strategy_used else 'Unknown'}"
        )
        quality_metrics = f"Execution success: {execution_successful}"
        resource_usage = f"Documents: {len(self.documents)}"

        # Synthesize final result
        agentic_result = self.synthesis_engine.invoke(
            {
                "query": query,
                "react_plan": react_plan_summary,
                "execution_results": execution_summary,
                "strategy_performance": strategy_performance,
                "quality_metrics": quality_metrics,
                "resource_usage": resource_usage,
            }
        )

        logger.info(
            f"Agentic synthesis completed: Quality={agentic_result.answer_quality}"
        )

        return {
            "response": agentic_result.final_response,
            "agentic_result": agentic_result,
            "decision_confidence": agentic_result.decision_confidence,
            "primary_strategy": agentic_result.primary_strategy,
            "reasoning_steps": agentic_result.reasoning_steps,
            "answer_quality": agentic_result.answer_quality,
            "efficiency_score": agentic_result.efficiency_score,
            "autonomous_decisions": agentic_result.autonomous_decisions,
            "messages": state.messages,
        }

    def strategy_router(self, state: RAGState) -> str:
        """Route to the appropriate strategy execution node based on the selected strategy."""
        selected_strategy = getattr(state, "selected_strategy", RAGStrategy.SIMPLE)

        if selected_strategy == RAGStrategy.SIMPLE:
            return "execute_simple"
        if selected_strategy == RAGStrategy.MULTI_QUERY:
            return "execute_multi_query"
        if selected_strategy == RAGStrategy.HYDE:
            return "execute_hyde"
        if selected_strategy == RAGStrategy.FUSION:
            return "execute_fusion"
        if selected_strategy == RAGStrategy.FLARE:
            return "execute_flare"
        return "execute_simple"  # Default fallback

    def build_graph(self) -> BaseGraph:
        """Build the agentic RAG router graph with conditional edges."""
        graph = BaseGraph(name="AgenticRAGRouter")

        # Add nodes
        graph.add_node("plan_react", self.plan_react_strategy)
        graph.add_node("execute_simple", self.execute_simple_strategy)
        graph.add_node("execute_multi_query", self.execute_multi_query_strategy)
        graph.add_node("execute_hyde", self.execute_hyde_strategy)
        graph.add_node("execute_fusion", self.execute_fusion_strategy)
        graph.add_node("execute_flare", self.execute_flare_strategy)
        graph.add_node("synthesize", self.synthesize_agentic_result)

        # Connect the flow
        graph.add_edge(START, "plan_react")

        # Add conditional routing from planning to execution
        graph.add_conditional_edges(
            "plan_react",
            self.strategy_router,
            {
                "execute_simple": "execute_simple",
                "execute_multi_query": "execute_multi_query",
                "execute_hyde": "execute_hyde",
                "execute_fusion": "execute_fusion",
                "execute_flare": "execute_flare",
            },
        )

        # All execution nodes lead to synthesis
        graph.add_edge("execute_simple", "synthesize")
        graph.add_edge("execute_multi_query", "synthesize")
        graph.add_edge("execute_hyde", "synthesize")
        graph.add_edge("execute_fusion", "synthesize")
        graph.add_edge("execute_flare", "synthesize")

        # Synthesis leads to end
        graph.add_edge("synthesize", END)

        return graph

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        autonomy_level: str = "high",
        **kwargs,
    ):
        """Create Agentic RAG Router from documents.

        Args:
            documents: Documents to index for RAG strategies
            llm_config: LLM configuration
            autonomy_level: Autonomy level ("low", "medium", "high")
            **kwargs: Additional arguments

        Returns:
            AgenticRAGRouterAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        return cls(
            documents=documents,
            llm_config=llm_config,
            autonomy_level=autonomy_level,
            **kwargs,
        )


# Factory function
def create_agentic_rag_router_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    routing_mode: str = "autonomous",
    **kwargs,
) -> AgenticRAGRouterAgent:
    """Create an Agentic RAG Router agent.

    Args:
        documents: Documents for RAG strategies
        llm_config: LLM configuration
        routing_mode: Routing mode ("conservative", "balanced", "autonomous")
        **kwargs: Additional arguments

    Returns:
        Configured Agentic RAG Router agent
    """
    # Configure based on routing mode
    autonomy_level = "high"  # default
    if routing_mode == "conservative":
        autonomy_level = "low"
    elif routing_mode == "balanced":
        autonomy_level = "medium"

    return AgenticRAGRouterAgent.from_documents(
        documents=documents,
        llm_config=llm_config,
        autonomy_level=autonomy_level,
        **kwargs,
    )


# I/O schema for compatibility
def get_agentic_rag_router_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Agentic RAG Router agents."""
    return {
        "inputs": ["query", "context", "previous_results", "messages"],
        "outputs": [
            "react_plan",
            "selected_strategy",
            "strategy_confidence",
            "fallback_strategies",
            "execution_steps",
            "success_criteria",
            "estimated_complexity",
            "reasoning_steps",
            "execution_result",
            "execution_successful",
            "result_confidence",
            "strategy_used",
            "supporting_evidence",
            "source_documents",
            "agentic_result",
            "final_response",
            "decision_confidence",
            "primary_strategy",
            "answer_quality",
            "efficiency_score",
            "autonomous_decisions",
            "response",
            "messages",
        ],
    }
