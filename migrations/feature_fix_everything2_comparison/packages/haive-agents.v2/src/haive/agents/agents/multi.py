"""MultiMemoryAgent - Coordinates different memory strategies.

This agent acts as a meta-coordinator that routes queries to different specialized
memory agents based on query type, context, and memory strategy optimization.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import DeepSeekLLMConfig
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.simple.agent import SimpleAgent

from ..base.token_state import MemoryStateWithTokens

# Import memory agents
from .simple import SimpleMemoryAgent, TokenAwareMemoryConfig

# Optional imports with graceful fallback
try:
    from ..coordination.agentic_rag_coordinator import AgenticRAGCoordinator
    from ..retrieval.advanced_rag import AdvancedRAGMemoryAgent
    HAS_RAG_MEMORY = True
except ImportError:
    AdvancedRAGMemoryAgent = None
    AgenticRAGCoordinator = None
    HAS_RAG_MEMORY = False

# Graph memory not yet implemented in reorganized structure
HAS_GRAPH_MEMORY = False
GraphMemoryAgent = None
GraphMemoryConfig = None

logger = logging.getLogger(__name__)


class MemoryStrategy(str, Enum):
    """Types of memory strategies available."""

    SIMPLE = "simple"  # Basic conversation memory
    GRAPH = "graph"  # Knowledge graph memory
    RAG = "rag"  # Retrieval-augmented memory
    HYBRID = "hybrid"  # Combine multiple strategies
    ADAPTIVE = "adaptive"  # Dynamically choose best strategy


class QueryType(str, Enum):
    """Types of queries that determine memory routing."""

    CONVERSATIONAL = "conversational"  # General conversation
    FACTUAL = "factual"  # Fact-based questions
    RELATIONSHIP = "relationship"  # About connections/relationships
    TEMPORAL = "temporal"  # Time-based questions
    PREFERENCE = "preference"  # User preferences
    MEMORY_RETRIEVAL = "memory_retrieval"  # Direct memory access
    MIXED = "mixed"  # Multiple query types


class MemoryPriority(str, Enum):
    """Priority levels for memory processing."""

    IMMEDIATE = "immediate"  # Real-time response needed
    HIGH = "high"  # Important but can wait
    NORMAL = "normal"  # Standard processing
    LOW = "low"  # Background processing
    BATCH = "batch"  # Process with other items


@dataclass
class MemoryRoutingRule:
    """Rule for routing queries to specific memory strategies."""

    query_type: QueryType
    strategy: MemoryStrategy
    confidence_threshold: float = 0.7
    fallback_strategy: MemoryStrategy | None = None
    conditions: dict[str, Any] = field(default_factory=dict)


class MultiMemoryConfig(BaseModel):
    """Configuration for MultiMemoryAgent."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core configuration
    name: str = Field(default="multi_memory_coordinator")
    llm_config: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            llm_config=DeepSeekLLMConfig(model="deepseek-chat", temperature=0.7)
        )
    )

    # Memory agent configurations
    enable_simple_memory: bool = Field(default=True)
    simple_memory_config: TokenAwareMemoryConfig | None = Field(
        default_factory=TokenAwareMemoryConfig
    )

    enable_graph_memory: bool = Field(default=HAS_GRAPH_MEMORY)
    graph_memory_config: dict[str, Any] | None = Field(default_factory=dict)

    enable_rag_memory: bool = Field(default=HAS_RAG_MEMORY)
    rag_memory_config: dict[str, Any] | None = Field(default_factory=dict)

    # Routing configuration
    default_strategy: MemoryStrategy = Field(default=MemoryStrategy.ADAPTIVE)
    routing_rules: list[MemoryRoutingRule] = Field(
        default_factory=lambda: [
            MemoryRoutingRule(QueryType.CONVERSATIONAL, MemoryStrategy.SIMPLE),
            MemoryRoutingRule(
                QueryType.FACTUAL,
                MemoryStrategy.RAG,
                fallback_strategy=MemoryStrategy.SIMPLE,
            ),
            MemoryRoutingRule(
                QueryType.RELATIONSHIP,
                MemoryStrategy.GRAPH,
                fallback_strategy=MemoryStrategy.SIMPLE,
            ),
            MemoryRoutingRule(
                QueryType.TEMPORAL,
                MemoryStrategy.RAG,
                fallback_strategy=MemoryStrategy.SIMPLE,
            ),
            MemoryRoutingRule(QueryType.PREFERENCE, MemoryStrategy.SIMPLE),
            MemoryRoutingRule(QueryType.MEMORY_RETRIEVAL, MemoryStrategy.HYBRID),
            MemoryRoutingRule(QueryType.MIXED, MemoryStrategy.ADAPTIVE),
        ]
    )

    # Performance settings
    query_classification_confidence: float = Field(default=0.8)
    enable_parallel_querying: bool = Field(default=True)
    max_concurrent_queries: int = Field(default=3)
    response_timeout_seconds: int = Field(default=30)

    # Memory coordination settings
    enable_cross_memory_validation: bool = Field(default=True)
    enable_response_synthesis: bool = Field(default=True)
    confidence_weighted_synthesis: bool = Field(default=True)


class MultiMemoryState(MemoryStateWithTokens):
    """Extended state for MultiMemoryAgent with routing information."""

    # Query classification
    detected_query_type: QueryType = Field(default=QueryType.CONVERSATIONAL)
    query_confidence: float = Field(default=0.0)
    classification_reasoning: str = Field(default="")

    # Memory routing
    selected_strategy: MemoryStrategy = Field(default=MemoryStrategy.SIMPLE)
    routing_decision: dict[str, Any] = Field(default_factory=dict)
    fallback_used: bool = Field(default=False)

    # Multi-memory responses
    memory_responses: dict[str, Any] = Field(default_factory=dict)
    response_synthesis: dict[str, Any] = Field(default_factory=dict)

    # Performance tracking
    query_processing_time: float = Field(default=0.0)
    memory_latencies: dict[str, float] = Field(default_factory=dict)
    total_coordination_time: float = Field(default=0.0)


class MultiMemoryAgent(SimpleAgent):
    """Agent that coordinates multiple memory strategies.

    This agent acts as a smart router and coordinator for different memory approaches,
    automatically selecting the best strategy based on query analysis and combining
    responses when appropriate.
    """

    def __init__(self, config: MultiMemoryConfig):
        self.multi_config = config

        # Initialize base agent with extended state
        super().__init__(
            name=config.name,
            engine=config.llm_config,
            state_schema=MultiMemoryState,
            use_prebuilt_base=True,
        )

        # Initialize specialized memory agents
        self._init_memory_agents()

        # Query classification system
        self._init_query_classifier()

        # Response synthesis system
        self._init_response_synthesizer()

        # Performance tracking
        self._query_stats = {
            "total_queries": 0,
            "strategy_usage": {},
            "average_latency": 0.0,
            "error_count": 0,
        }

    def _init_memory_agents(self):
        """Initialize the specialized memory agents."""
        self.memory_agents = {}

        # Simple Memory Agent (always available)
        if self.multi_config.enable_simple_memory:
            try:
                self.memory_agents["simple"] = SimpleMemoryAgent(
                    name=f"{self.multi_config.name}_simple",
                    engine=self.multi_config.llm_config,
                    memory_config=self.multi_config.simple_memory_config,
                )
                logger.info("Initialized SimpleMemoryAgent")
            except Exception as e:
                logger.exception(f"Failed to initialize SimpleMemoryAgent: {e}")

        # Graph Memory Agent (if available)
        if self.multi_config.enable_graph_memory and HAS_GRAPH_MEMORY:
            try:
                graph_config = GraphMemoryConfig(
                    llm_config=self.multi_config.llm_config,
                    **self.multi_config.graph_memory_config,
                )
                self.memory_agents["graph"] = GraphMemoryAgent(graph_config)
                logger.info("Initialized GraphMemoryAgent")
            except Exception as e:
                logger.warning(f"Failed to initialize GraphMemoryAgent: {e}")

        # RAG Memory Agent (if available)
        if self.multi_config.enable_rag_memory and HAS_RAG_MEMORY:
            try:
                # RAG Memory initialization would go here
                # For now, we'll skip since it has complex dependencies
                logger.info(
                    "RAG Memory Agent initialization skipped (complex dependencies)"
                )
            except Exception as e:
                logger.warning(f"Failed to initialize RAG Memory Agent: {e}")

        logger.info(
            f"Initialized {
                len(
                    self.memory_agents)} memory agents: {
                list(
                    self.memory_agents.keys())}"
        )

    def _init_query_classifier(self):
        """Initialize the query classification system."""
        self.query_classifier = QueryClassifier(self.multi_config.llm_config)

    def _init_response_synthesizer(self):
        """Initialize the response synthesis system."""
        self.response_synthesizer = ResponseSynthesizer(self.multi_config.llm_config)

    async def classify_query(self, query: str) -> dict[str, Any]:
        """Classify the query to determine appropriate memory strategy."""
        return await self.query_classifier.classify(query)

    def route_query(
        self,
        query_type: QueryType,
        confidence: float,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Route query to appropriate memory strategy based on classification."""
        # Find matching routing rule
        selected_rule = None
        for rule in self.multi_config.routing_rules:
            if (
                rule.query_type == query_type
                and confidence >= rule.confidence_threshold
            ):
                # Check additional conditions if any
                if self._check_rule_conditions(rule, context):
                    selected_rule = rule
                    break

        # Fall back to default strategy if no rule matched
        if selected_rule is None:
            strategy = self.multi_config.default_strategy
            fallback_strategy = MemoryStrategy.SIMPLE
            rule_matched = False
        else:
            strategy = selected_rule.strategy
            fallback_strategy = selected_rule.fallback_strategy
            rule_matched = True

        # Check if selected strategy is available
        available_strategies = []
        if "simple" in self.memory_agents:
            available_strategies.append(MemoryStrategy.SIMPLE)
        if "graph" in self.memory_agents:
            available_strategies.append(MemoryStrategy.GRAPH)
        if "rag" in self.memory_agents:
            available_strategies.append(MemoryStrategy.RAG)

        # Adjust strategy based on availability
        final_strategy = strategy
        fallback_used = False

        if strategy not in [s.value for s in available_strategies] + [
            "hybrid",
            "adaptive",
        ]:
            if fallback_strategy and fallback_strategy.value in [
                s.value for s in available_strategies
            ]:
                final_strategy = fallback_strategy
                fallback_used = True
            else:
                final_strategy = MemoryStrategy.SIMPLE  # Always fall back to simple
                fallback_used = True

        return {
            "strategy": final_strategy,
            "fallback_used": fallback_used,
            "rule_matched": rule_matched,
            "available_strategies": [s.value for s in available_strategies],
            "reasoning": f"Query type {query_type} routed to {final_strategy} (confidence: {
                confidence:.2f})",
        }

    def _check_rule_conditions(
        self, rule: MemoryRoutingRule, context: dict[str, Any] | None
    ) -> bool:
        """Check if additional rule conditions are met."""
        if not rule.conditions or not context:
            return True

        for condition, expected_value in rule.conditions.items():
            if context.get(condition) != expected_value:
                return False

        return True

    async def query_memory_agent(
        self, agent_key: str, query: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Query a specific memory agent."""
        start_time = datetime.now()

        if agent_key not in self.memory_agents:
            return {
                "error": f"Memory agent '{agent_key}' not available",
                "agent": agent_key,
                "latency": 0.0,
            }

        try:
            agent = self.memory_agents[agent_key]

            # Use async if available, otherwise sync
            if hasattr(agent, "arun"):
                result = await agent.arun(query)
            else:
                result = agent.run(query)

            latency = (datetime.now() - start_time).total_seconds()

            return {
                "result": result,
                "agent": agent_key,
                "latency": latency,
                "success": True,
            }

        except Exception as e:
            latency = (datetime.now() - start_time).total_seconds()
            logger.exception(f"Error querying {agent_key} memory agent: {e}")

            return {
                "error": str(e),
                "agent": agent_key,
                "latency": latency,
                "success": False,
            }

    async def execute_strategy(
        self,
        strategy: MemoryStrategy,
        query: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute the selected memory strategy."""
        if strategy == MemoryStrategy.SIMPLE:
            return await self.query_memory_agent("simple", query, context)

        if strategy == MemoryStrategy.GRAPH:
            return await self.query_memory_agent("graph", query, context)

        if strategy == MemoryStrategy.RAG:
            return await self.query_memory_agent("rag", query, context)

        if strategy == MemoryStrategy.HYBRID:
            # Query multiple agents in parallel
            tasks = []
            available_agents = list(self.memory_agents.keys())[
                : self.multi_config.max_concurrent_queries
            ]

            for agent_key in available_agents:
                task = self.query_memory_agent(agent_key, query, context)
                tasks.append(task)

            if self.multi_config.enable_parallel_querying:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            else:
                results = []
                for task in tasks:
                    try:
                        result = await task
                        results.append(result)
                    except Exception as e:
                        results.append({"error": str(e), "success": False})

            return {
                "strategy": "hybrid",
                "results": results,
                "agents_queried": available_agents,
                "success": any(
                    r.get("success", False) for r in results if isinstance(r, dict)
                ),
            }

        if strategy == MemoryStrategy.ADAPTIVE:
            # Use AI to decide the best approach
            adaptive_result = await self._adaptive_strategy_selection(query, context)
            return await self.execute_strategy(
                adaptive_result["selected_strategy"], query, context
            )

        return {"error": f"Unknown strategy: {strategy}", "success": False}

    async def _adaptive_strategy_selection(
        self, query: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Use AI to adaptively select the best memory strategy."""
        available_strategies = list(self.memory_agents.keys())
        strategy_descriptions = {
            "simple": "Basic conversational memory with token-aware management",
            "graph": "Knowledge graph memory for relationships and structured data",
            "rag": "Retrieval-augmented memory for factual information",
        }

        # Create prompt for strategy selection
        strategy_prompt = f"""
        You are a memory strategy coordinator. Given the query and available memory strategies,
        select the most appropriate approach.

        Query: "{query}"

        Available strategies:
        {chr(10).join([f"- {k}: {strategy_descriptions.get(k, 'Unknown')}" for k in available_strategies])}

        Context: {context if context else "None"}

        Select the best strategy and explain your reasoning. Respond with just the strategy name.
        """

        try:
            # Use the LLM to select strategy
            llm_response = await self.engine.ainvoke(strategy_prompt)
            selected_strategy = llm_response.strip().lower()

            # Map response to actual strategy
            strategy_mapping = {
                "simple": MemoryStrategy.SIMPLE,
                "graph": MemoryStrategy.GRAPH,
                "rag": MemoryStrategy.RAG,
            }

            final_strategy = strategy_mapping.get(
                selected_strategy, MemoryStrategy.SIMPLE
            )

            return {
                "selected_strategy": final_strategy,
                "reasoning": f"AI selected {selected_strategy} based on query analysis",
                "llm_response": llm_response,
            }

        except Exception as e:
            logger.exception(f"Adaptive strategy selection failed: {e}")
            return {
                "selected_strategy": MemoryStrategy.SIMPLE,
                "reasoning": f"Fallback to simple due to error: {e}",
                "error": str(e),
            }

    async def synthesize_responses(
        self, responses: list[dict[str, Any]], query: str
    ) -> dict[str, Any]:
        """Synthesize multiple memory responses into a coherent answer."""
        if not self.multi_config.enable_response_synthesis:
            # Just return the first successful response
            for response in responses:
                if response.get("success", False):
                    return response
            return {"error": "No successful responses to synthesize"}

        # Use the response synthesizer
        return await self.response_synthesizer.synthesize(responses, query)

    async def _prepare_input(self, input_data: Any) -> dict[str, Any]:
        """Prepare input with multi-memory coordination."""
        start_time = datetime.now()

        # Get base input preparation
        base_input = super()._prepare_input(input_data)

        # Extract query
        if isinstance(input_data, str):
            query = input_data
        elif isinstance(input_data, dict) and "messages" in input_data:
            messages = input_data["messages"]
            if messages and hasattr(messages[-1], "content"):
                query = messages[-1].content
            else:
                query = str(messages[-1]) if messages else ""
        else:
            query = str(input_data)

        # Classify query
        classification_result = await self.classify_query(query)

        # Route query
        routing_result = self.route_query(
            classification_result["query_type"],
            classification_result["confidence"],
            classification_result.get("context"),
        )

        # Execute selected strategy
        execution_result = await self.execute_strategy(
            routing_result["strategy"], query, classification_result.get("context")
        )

        # Update statistics
        self._update_query_stats(routing_result["strategy"], start_time)

        # Enhance input with coordination results
        enhanced_input = base_input.copy()
        enhanced_input.update(
            {
                "detected_query_type": classification_result["query_type"],
                "query_confidence": classification_result["confidence"],
                "classification_reasoning": classification_result.get("reasoning", ""),
                "selected_strategy": routing_result["strategy"],
                "routing_decision": routing_result,
                "fallback_used": routing_result["fallback_used"],
                "memory_responses": {"primary": execution_result},
                "total_coordination_time": (
                    datetime.now() - start_time
                ).total_seconds(),
            }
        )

        return enhanced_input

    def _update_query_stats(self, strategy: MemoryStrategy, start_time: datetime):
        """Update query processing statistics."""
        latency = (datetime.now() - start_time).total_seconds()

        self._query_stats["total_queries"] += 1

        if strategy.value not in self._query_stats["strategy_usage"]:
            self._query_stats["strategy_usage"][strategy.value] = 0
        self._query_stats["strategy_usage"][strategy.value] += 1

        # Update rolling average latency
        prev_avg = self._query_stats["average_latency"]
        total_queries = self._query_stats["total_queries"]
        new_avg = (prev_avg * (total_queries - 1) + latency) / total_queries
        self._query_stats["average_latency"] = new_avg

    def get_coordination_stats(self) -> dict[str, Any]:
        """Get statistics about query coordination and routing."""
        return {
            **self._query_stats,
            "available_agents": list(self.memory_agents.keys()),
            "strategy_distribution": (
                {
                    strategy: (count / self._query_stats["total_queries"]) * 100
                    for strategy, count in self._query_stats["strategy_usage"].items()
                }
                if self._query_stats["total_queries"] > 0
                else {}
            ),
            "timestamp": datetime.now().isoformat(),
        }

    def get_comprehensive_status(self) -> dict[str, Any]:
        """Get comprehensive status of the MultiMemoryAgent."""
        base_status = super().get_comprehensive_status()

        agent_statuses = {}
        for agent_key, agent in self.memory_agents.items():
            try:
                if hasattr(agent, "get_comprehensive_status"):
                    agent_statuses[agent_key] = agent.get_comprehensive_status()
                else:
                    agent_statuses[agent_key] = {
                        "status": "available",
                        "type": type(agent).__name__,
                    }
            except Exception as e:
                agent_statuses[agent_key] = {"errof": str(e)}

        return {
            **base_status,
            "agent_type": "MultiMemoryAgent",
            "coordination_config": {
                "default_strategy": self.multi_config.default_strategy.value,
                "parallel_querying": self.multi_config.enable_parallel_querying,
                "max_concurrent": self.multi_config.max_concurrent_queries,
            },
            "memory_agents": agent_statuses,
            "coordination_stats": self.get_coordination_stats(),
        }


class QueryClassifier:
    """Classifies queries to determine appropriate memory strategy."""

    def __init__(self, llm_config: AugLLMConfig):
        self.llm_config = llm_config
        self.engine = llm_config.instantiate()

    async def classify(self, query: str) -> dict[str, Any]:
        """Classify a query to determine its type and characteristics."""
        classification_prompt = f"""
        Classify the following query to determine the best memory strategy approach.

        Query: "{query}"

        Analyze the query for:
        1. Primary intent (conversational, factual, relationship-based, temporal, preference, memory retrieval)
        2. Information type needed (recent conversation, stored facts, relationships, timeline, user preferences)
        3. Complexity level (simple, moderate, complex)

        Respond in this format:
        Type: [conversational/factual/relationship/temporal/preference/memory_retrieval/mixed]
        Confidence: [0.0-1.0]
        Reasoning: [brief explanation]
        """

        try:
            response = await self.engine.ainvoke(classification_prompt)

            # Parse the response (simplified parsing)
            lines = response.strip().split("\n")
            result = {
                "query_type": QueryType.CONVERSATIONAL,
                "confidence": 0.5,
                "reasoning": "Default classification",
            }

            for line in lines:
                if line.startswith("Type:"):
                    type_str = line.split(":", 1)[1].strip().lower()
                    type_mapping = {
                        "conversational": QueryType.CONVERSATIONAL,
                        "factual": QueryType.FACTUAL,
                        "relationship": QueryType.RELATIONSHIP,
                        "temporal": QueryType.TEMPORAL,
                        "preference": QueryType.PREFERENCE,
                        "memory_retrieval": QueryType.MEMORY_RETRIEVAL,
                        "mixed": QueryType.MIXED,
                    }
                    result["query_type"] = type_mapping.get(
                        type_str, QueryType.CONVERSATIONAL
                    )

                elif line.startswith("Confidence:"):
                    try:
                        confidence = float(line.split(":", 1)[1].strip())
                        result["confidence"] = max(0.0, min(1.0, confidence))
                    except ValueError:
                        pass

                elif line.startswith("Reasoning:"):
                    result["reasoning"] = line.split(":", 1)[1].strip()

            return result

        except Exception as e:
            logger.exception(f"Query classification failed: {e}")
            return {
                "query_type": QueryType.CONVERSATIONAL,
                "confidence": 0.5,
                "reasoning": f"Classification failed: {e}",
                "error": str(e),
            }


class ResponseSynthesizer:
    """Synthesizes responses from multiple memory agents."""

    def __init__(self, llm_config: AugLLMConfig):
        self.llm_config = llm_config
        self.engine = llm_config.instantiate()

    async def synthesize(
        self, responses: list[dict[str, Any]], original_query: str
    ) -> dict[str, Any]:
        """Synthesize multiple memory responses into a coherent answer."""
        # Filter successful responses
        successful_responses = [r for r in responses if r.get("success", False)]

        if not successful_responses:
            return {
                "error": "No successful responses to synthesize",
                "original_responses": responses,
            }

        if len(successful_responses) == 1:
            return successful_responses[0]

        # Create synthesis prompt
        response_summaries = []
        for i, response in enumerate(successful_responses):
            agent_name = response.get("agent", f"agent_{i}")
            result_content = str(response.get("result", ""))[
                :500
            ]  # Truncate for prompt
            response_summaries.append(f"{agent_name}: {result_content}")

        synthesis_prompt = f"""
        Synthesize the following responses from different memory agents into a single, coherent answer.

        Original Query: "{original_query}"

        Agent Responses:
        {chr(10).join(response_summaries)}

        Provide a synthesized response that:
        1. Combines relevant information from all agents
        2. Resolves any contradictions by noting different perspectives
        3. Maintains coherence and relevance to the original query
        4. Indicates confidence level in the synthesized answer
        """

        try:
            synthesized_response = await self.engine.ainvoke(synthesis_prompt)

            return {
                "synthesized_response": synthesized_response,
                "source_agents": [r.get("agent") for r in successful_responses],
                "synthesis_success": True,
                "original_responses": successful_responses,
            }

        except Exception as e:
            logger.exception(f"Response synthesis failed: {e}")
            return {
                "error": f"Synthesis failed: {e}",
                "fallback_response": successful_responses[0]["result"],
                "synthesis_success": False,
                "original_responses": successful_responses,
            }


# Example usage and factory functions
def create_multi_memory_agent(
    name: str = "multi_memory_coordinator",
    enable_graph: bool = HAS_GRAPH_MEMORY,
    enable_rag: bool = HAS_RAG_MEMORY,
    **kwargs,
) -> MultiMemoryAgent:
    """Factory function to create a MultiMemoryAgent with sensible defaults."""
    config = MultiMemoryConfig(
        name=name,
        enable_graph_memory=enable_graph,
        enable_rag_memory=enable_rag,
        **kwargs,
    )

    return MultiMemoryAgent(config)
