"""
Specialized Workflows V2 - Using Enhanced State Schemas

Updated versions of FLARE, Dynamic RAG, Debate RAG, etc. using
state schemas with built-in configuration support.
"""

from typing import Any, Dict, List, Optional

from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.rag.multi_agent_rag.enhanced_state_schemas import (
    AdaptiveThresholdRAGState,
    DebateRAGState,
    DynamicRAGState,
    FLAREState,
    StateConfigMixin,
)
from haive.agents.simple import SimpleAgent


class FLAREAgentV2(MultiAgent, StateConfigMixin):
    """
    FLARE V2 - Configuration stored in FLAREState
    """

    def __init__(
        self,
        uncertainty_threshold: float = 0.3,
        max_retrieval_rounds: int = 3,
        **kwargs,
    ):
        generation_monitor = SimpleAgent(
            name="generation_monitor",
            instructions="""
            Monitor text generation for uncertainty indicators.
            Use state.uncertainty_threshold to determine when to trigger retrieval.
            Track retrieval rounds against state.max_retrieval_rounds.
            """,
            output_schema={
                "current_segment": "str",
                "uncertainty_detected": "bool",
                "uncertainty_score": "float",
                "retrieval_needed": "bool",
            },
        )

        active_retrieval = SimpleAgent(
            name="active_retrieval",
            instructions="""
            Perform targeted retrieval when uncertainty exceeds threshold.
            Check state.retrieval_rounds < state.max_retrieval_rounds.
            """,
            output_schema={
                "retrieved_documents": "List[str]",
                "retrieval_query": "str",
            },
        )

        informed_generator = SimpleAgent(
            name="informed_generator",
            instructions="""
            Continue generation using retrieved information.
            Update state.generation_segments and confidence_scores.
            """,
            output_schema={
                "generated_segment": "str",
                "confidence_score": "float",
                "generation_complete": "bool",
            },
        )

        synthesis_agent = SimpleAgent(
            name="synthesis_agent",
            instructions="""
            Synthesize all segments into final response.
            Use state.generation_segments and confidence_scores.
            """,
            output_schema={"final_response": "str", "overall_confidence": "float"},
        )

        agents = [
            generation_monitor,
            active_retrieval,
            informed_generator,
            synthesis_agent,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=FLAREState,
            **kwargs,
        )

        self._initial_config = {
            "uncertainty_threshold": uncertainty_threshold,
            "max_retrieval_rounds": max_retrieval_rounds,
            "workflow_type": "flare",
        }

    async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Inject configuration into state"""
        for key, value in self._initial_config.items():
            if key not in inputs:
                inputs[key] = value
        return await super().ainvoke(inputs)

    def build_custom_graph(self):
        """Build the custom graph for this workflow"""
        return None  # Use default graph structure


class DynamicRAGAgentV2(MultiAgent, StateConfigMixin):
    """
    Dynamic RAG V2 - Configuration in DynamicRAGState
    """

    def __init__(
        self,
        min_retrievers: int = 1,
        max_retrievers: int = 5,
        performance_threshold: float = 0.6,
        **kwargs,
    ):
        retriever_manager = SimpleAgent(
            name="retriever_manager",
            instructions="""
            Manage retriever pool based on state configuration.
            Ensure state.min_retrievers <= active <= state.max_retrievers.
            Remove retrievers below state.performance_threshold.
            """,
            output_schema={
                "retrievers_to_add": "List[Dict[str, Any]]",
                "retrievers_to_remove": "List[str]",
                "active_retriever_count": "int",
            },
        )

        retriever_coordinator = SimpleAgent(
            name="retriever_coordinator",
            instructions="""
            Coordinate retrieval across state.active_retrievers.
            Track performance in state.retriever_performance.
            """,
            output_schema={
                "retrieval_results": "Dict[str, List[str]]",
                "performance_updates": "Dict[str, float]",
            },
        )

        performance_analyzer = SimpleAgent(
            name="performance_analyzer",
            instructions="""
            Analyze retriever performance against state.performance_threshold.
            Update state.retriever_performance and make recommendations.
            """,
            output_schema={
                "performance_report": "Dict[str, float]",
                "recommendations": "List[str]",
            },
        )

        dynamic_synthesis = SimpleAgent(
            name="dynamic_synthesis",
            instructions="""
            Synthesize using retrievers above performance threshold.
            Weight by performance scores from state.
            """,
            output_schema={
                "answer": "str",
                "retriever_contributions": "Dict[str, float]",
            },
        )

        agents = [
            retriever_manager,
            retriever_coordinator,
            performance_analyzer,
            dynamic_synthesis,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=DynamicRAGState,
            **kwargs,
        )

        self._initial_config = {
            "min_retrievers": min_retrievers,
            "max_retrievers": max_retrievers,
            "performance_threshold": performance_threshold,
            "workflow_type": "dynamic_rag",
        }

    async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Inject configuration"""
        for key, value in self._initial_config.items():
            if key not in inputs:
                inputs[key] = value
        return await super().ainvoke(inputs)

    def build_custom_graph(self):
        """Build the custom graph for this workflow"""
        return None  # Use default graph structure


class DebateRAGAgentV2(MultiAgent, StateConfigMixin):
    """
    Debate RAG V2 - Configuration in DebateRAGState
    """

    def __init__(
        self,
        position_names: Optional[List[str]] = None,
        max_debate_rounds: int = 3,
        require_consensus: bool = False,
        enable_judge: bool = True,
        **kwargs,
    ):
        if position_names is None:
            position_names = ["Affirmative", "Negative", "Neutral"]

        # Create position agents
        position_agents = []
        for position in position_names:
            agent = SimpleAgent(
                name=f"{position.lower()}_position",
                instructions=f"""
                Argue from the {position} perspective.
                Check state.debate_rounds < state.max_debate_rounds.
                Update state.arguments_by_position['{position}'].
                """,
                output_schema={
                    "argument": "str",
                    "evidence": "List[str]",
                    "confidence": "float",
                },
            )
            position_agents.append(agent)

        # Moderator
        moderator = SimpleAgent(
            name="debate_moderator",
            instructions="""
            Moderate debate using state.position_names.
            Check if state.require_consensus for ending criteria.
            Track state.debate_rounds.
            """,
            output_schema={
                "summary": "str",
                "consensus_check": "bool",
                "continue_debate": "bool",
            },
        )

        # Optional judge
        if enable_judge:
            judge = SimpleAgent(
                name="debate_judge",
                instructions="""
                Judge the debate based on arguments and evidence.
                Set state.debate_winner if clear winner emerges.
                """,
                output_schema={
                    "judgment": "str",
                    "winner": "Optional[str]",
                    "scores": "Dict[str, float]",
                },
            )
            agents = position_agents + [moderator, judge]
        else:
            agents = position_agents + [moderator]

        # Synthesis
        synthesis_judge = SimpleAgent(
            name="synthesis_judge",
            instructions="""
            Synthesize all positions into final answer.
            Consider state.consensus_reached and debate_winner.
            """,
            output_schema={"final_answer": "str", "synthesis_method": "str"},
        )

        agents.append(synthesis_judge)

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=DebateRAGState,
            **kwargs,
        )

        self._initial_config = {
            "position_names": position_names,
            "max_debate_rounds": max_debate_rounds,
            "require_consensus": require_consensus,
            "enable_judge": enable_judge,
            "workflow_type": "debate_rag",
        }

    async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Inject configuration and initialize debate positions"""
        for key, value in self._initial_config.items():
            if key not in inputs:
                inputs[key] = value

        # Initialize debate positions if not set
        if "debate_positions" not in inputs:
            inputs["debate_positions"] = {
                name: f"{name} position on the topic"
                for name in self._initial_config["position_names"]
            }

        return await super().ainvoke(inputs)

    def build_custom_graph(self):
        """Build the custom graph for this workflow"""
        return None  # Use default graph structure


class AdaptiveThresholdRAGAgentV2(MultiAgent, StateConfigMixin):
    """
    Adaptive Threshold RAG V2 - Configuration in AdaptiveThresholdRAGState
    """

    def __init__(
        self,
        initial_threshold: float = 0.7,
        threshold_step: float = 0.1,
        min_threshold: float = 0.3,
        max_threshold: float = 0.95,
        **kwargs,
    ):
        query_analyzer = SimpleAgent(
            name="query_analyzer",
            instructions="""
            Analyze query complexity and set initial threshold.
            Use state.initial_threshold as starting point.
            Store complexity in state.query_complexity_score.
            """,
            output_schema={"complexity_score": "float", "suggested_threshold": "float"},
        )

        adaptive_retriever = SimpleAgent(
            name="adaptive_retriever",
            instructions="""
            Retrieve with current state.adaptive_threshold.
            Adjust by state.threshold_step if needed.
            Respect state.min_threshold and max_threshold bounds.
            """,
            output_schema={
                "documents": "List[str]",
                "threshold_used": "float",
                "adjustment_made": "float",
            },
        )

        confidence_assessor = SimpleAgent(
            name="confidence_assessor",
            instructions="""
            Assess if current threshold is appropriate.
            Suggest adjustments based on document quality.
            Update state.threshold_adjustments history.
            """,
            output_schema={
                "confidence": "float",
                "suggest_adjustment": "bool",
                "adjustment_direction": "str",
            },
        )

        threshold_aware_generator = SimpleAgent(
            name="threshold_aware_generator",
            instructions="""
            Generate answer aware of threshold adjustments.
            Note if threshold affected answer quality.
            """,
            output_schema={"answer": "str", "threshold_impact": "str"},
        )

        agents = [
            query_analyzer,
            adaptive_retriever,
            confidence_assessor,
            threshold_aware_generator,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=AdaptiveThresholdRAGState,
            **kwargs,
        )

        self._initial_config = {
            "initial_threshold": initial_threshold,
            "threshold_step": threshold_step,
            "min_threshold": min_threshold,
            "max_threshold": max_threshold,
            "adaptive_threshold": initial_threshold,  # Set initial value
            "workflow_type": "adaptive_threshold_rag",
        }

    async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Inject configuration"""
        for key, value in self._initial_config.items():
            if key not in inputs:
                inputs[key] = value
        return await super().ainvoke(inputs)

    def build_custom_graph(self):
        """Build the custom graph for this workflow"""
        return None  # Use default graph structure
