"""Dynamic Routing Engine for Haive Supervisor System.

Handles intelligent routing decisions using DynamicChoiceModel and LLM-based analysis.
Provides context-aware agent selection with validation and fallback mechanisms.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import InvokableEngine
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()


class RoutingDecision(BaseModel):
    """Model for routing decisions."""

    choice: str = Field(..., description="Selected agent name or END")
    confidence: float | None = Field(None, description="Confidence score 0-1")
    reasoning: str | None = Field(None, description="Reasoning for the choice")


class RoutingContext(BaseModel):
    """Context extracted from state for routing decisions."""

    last_message: str = Field(..., description="Last message content")
    message_type: str = Field(..., description="Type of last message")
    task_keywords: list[str] = Field(
        default_factory=list, description="Extracted keywords"
    )
    conversation_length: int = Field(..., description="Number of messages")
    previous_agent: str | None = Field(None, description="Previously active agent")
    task_complexity: str = Field(..., description="Simple/Medium/Complex")


class TaskClassifier:
    """Classifies tasks for better routing decisions."""

    TASK_PATTERNS = {
        "research": ["research", "find", "search", "investigate", "analyze", "study"],
        "math": ["calculate", "compute", "solve", "equation", "number", "math"],
        "writing": ["write", "draft", "compose", "create", "generate", "summarize"],
        "coding": ["code", "program", "implement", "debug", "function", "script"],
        "analysis": ["analyze", "compare", "evaluate", "assess", "review"],
        "planning": ["plan", "strategy", "organize", "schedule", "workflow"],
    }

    @classmethod
    def classify_task(cls, message: str) -> list[str]:
        """Classify task based on message content.

        Args:
            message: Message to classify

        Returns:
            List of detected task types
        """
        message_lower = message.lower()
        detected_types = []

        for task_type, keywords in cls.TASK_PATTERNS.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_types.append(task_type)

        return detected_types or ["general"]

    @classmethod
    def estimate_complexity(cls, message: str, conversation_length: int) -> str:
        """Estimate task complexity.

        Args:
            message: Message content
            conversation_length: Length of conversation

        Returns:
            Complexity level: Simple/Medium/Complex
        """
        complexity_indicators = [
            "multiple",
            "complex",
            "detailed",
            "comprehensive",
            "advanced",
            "sophisticated",
            "integrate",
            "coordinate",
            "multi-step",
        ]

        message_lower = message.lower()
        complexity_score = sum(
            1 for indicator in complexity_indicators if indicator in message_lower
        )

        # Factor in conversation length
        if conversation_length > 10:
            complexity_score += 1
        if conversation_length > 20:
            complexity_score += 1

        if complexity_score >= 3:
            return "Complex"
        if complexity_score >= 1:
            return "Medium"
        return "Simple"


class BaseRoutingStrategy(ABC):
    """Abstract base for routing strategies."""

    @abstractmethod
    async def make_routing_decision(
        self,
        context: RoutingContext,
        available_agents: list[str],
        agent_capabilities: dict[str, str],
        config: RunnableConfig | None = None,
    ) -> RoutingDecision:
        """Make routing decision based on context."""


class LLMRoutingStrategy(BaseRoutingStrategy):
    """LLM-based routing strategy using structured output."""

    def __init__(
        self, routing_engine: InvokableEngine, routing_model: DynamicChoiceModel[str]
    ):
        self.routing_engine = routing_engine
        self.routing_model = routing_model

    async def make_routing_decision(
        self,
        context: RoutingContext,
        available_agents: list[str],
        agent_capabilities: dict[str, str],
        config: RunnableConfig | None = None,
    ) -> RoutingDecision:
        """Make LLM-based routing decision."""
        # Build routing prompt
        prompt = self._build_routing_prompt(
            context, available_agents, agent_capabilities
        )

        # Get choice model for structured output
        choice_model = self.routing_model.current_model

        # Create messages
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Route this request: {context.last_message}"),
        ]

        try:
            # Get LLM decision with structured output
            if hasattr(self.routing_engine, "with_structured_output"):
                structured_engine = self.routing_engine.with_structured_output(
                    choice_model
                )
                result = await structured_engine.ainvoke(messages, config)
                return RoutingDecision(choice=result.choice)
            # Fallback to regular invocation
            result = await self.routing_engine.ainvoke(messages, config)
            choice = self._extract_choice_from_response(result.content)
            return RoutingDecision(choice=choice)

        except Exception as e:
            logger.exception(f"LLM routing failed: {e}")
            return self._fallback_routing(context, available_agents)

    def _build_routing_prompt(
        self,
        context: RoutingContext,
        available_agents: list[str],
        agent_capabilities: dict[str, str],
    ) -> str:
        """Build context-aware routing prompt."""
        # Format agent capabilities
        agent_info = []
        for agent in available_agents:
            if agent == "END":
                agent_info.append("- END: Complete the conversation")
            else:
                capability = agent_capabilities.get(agent, f"Handles {agent} tasks")
                agent_info.append(f"- {agent}: {capability}")

        prompt = f"""You are an intelligent task router for a multi-agent system.

Current Request Analysis:
- Message: "{context.last_message}"
- Task Type: {", ".join(context.task_keywords) if context.task_keywords else "General"}
- Complexity: {context.task_complexity}
- Conversation Length: {context.conversation_length} messages
- Previous Agent: {context.previous_agent or "None"}

Available Agents:
{chr(10).join(agent_info)}

Instructions:
1. Analyze the request to understand what needs to be done
2. Consider the task type and complexity
3. Select the most appropriate agent for this specific request
4. If the conversation should end or task is complete, select END
5. Avoid selecting the same agent repeatedly unless truly necessary

Response Format: Provide only the agent name or END as your choice."""

        return prompt

    def _extract_choice_from_response(self, response: str) -> str:
        """Extract choice from LLM response if structured output fails."""
        response_upper = response.strip().upper()

        # Check for END
        if "END" in response_upper:
            return "END"

        # Look for valid agent names
        available_options = self.routing_model.option_names
        for option in available_options:
            if option.upper() in response_upper:
                return option

        # Default fallback
        return available_options[0] if available_options else "END"

    def _fallback_routing(
        self, context: RoutingContext, available_agents: list[str]
    ) -> RoutingDecision:
        """Fallback routing when LLM fails."""
        logger.warning("Using fallback routing strategy")

        # Simple keyword-based fallback
        task_types = TaskClassifier.classify_task(context.last_message)

        for task_type in task_types:
            for agent in available_agents:
                if task_type in agent.lower():
                    return RoutingDecision(
                        choice=agent, reasoning="Fallback keyword matching"
                    )

        # Ultimate fallback
        if available_agents and available_agents[0] != "END":
            return RoutingDecision(
                choice=available_agents[0], reasoning="Fallback to first agent"
            )

        return RoutingDecision(choice="END", reasoning="Fallback to END")


class RuleBasedRoutingStrategy(BaseRoutingStrategy):
    """Rule-based routing strategy for deterministic routing."""

    def __init__(self, routing_rules: dict[str, str]):
        """Initialize with routing rules.

        Args:
            routing_rules: Dict mapping keywords to agent names
        """
        self.routing_rules = routing_rules

    async def make_routing_decision(
        self,
        context: RoutingContext,
        available_agents: list[str],
        agent_capabilities: dict[str, str],
        config: RunnableConfig | None = None,
    ) -> RoutingDecision:
        """Make rule-based routing decision."""
        message_lower = context.last_message.lower()

        # Check rules
        for keyword, agent_name in self.routing_rules.items():
            if keyword.lower() in message_lower and agent_name in available_agents:
                return RoutingDecision(
                    choice=agent_name, reasoning=f"Rule match: {keyword}"
                )

        # Default to first available agent
        if available_agents and available_agents[0] != "END":
            return RoutingDecision(choice=available_agents[0], reasoning="Default rule")

        return RoutingDecision(choice="END", reasoning="No matching rules")


class DynamicRoutingEngine:
    """Main routing engine that orchestrates routing decisions.

    Handles context extraction, strategy selection, and routing execution
    with comprehensive error handling and fallback mechanisms.
    """

    def __init__(
        self,
        routing_model: DynamicChoiceModel[str],
        routing_engine: InvokableEngine | None = None,
        routing_strategy: BaseRoutingStrategy | None = None,
        enable_context_analysis: bool = True,
    ):
        """Initialize routing engine.

        Args:
            routing_model: DynamicChoiceModel for available choices
            routing_engine: Engine for LLM-based routing (optional)
            routing_strategy: Custom routing strategy (optional)
            enable_context_analysis: Whether to perform context analysis
        """
        self.routing_model = routing_model
        self.routing_engine = routing_engine
        self.enable_context_analysis = enable_context_analysis

        # Set default strategy
        if routing_strategy:
            self.routing_strategy = routing_strategy
        elif routing_engine:
            self.routing_strategy = LLMRoutingStrategy(routing_engine, routing_model)
        else:
            # Fallback to simple rule-based strategy
            self.routing_strategy = RuleBasedRoutingStrategy(
                {
                    "research": "research_agent",
                    "math": "math_agent",
                    "write": "writer_agent",
                    "code": "code_agent",
                }
            )

        logger.info("DynamicRoutingEngine initialized")

    async def route_request(
        self,
        state: Any,
        agent_capabilities: dict[str, str],
        config: RunnableConfig | None = None,
    ) -> Command:
        """Main routing method.

        Args:
            state: Current graph state
            agent_capabilities: Dict of agent capabilities
            config: Runnable configuration

        Returns:
            Command object with routing decision
        """
        try:
            # Extract context
            context = self._extract_context(state)

            # Get available agents
            available_agents = self.routing_model.option_names

            if not available_agents:
                logger.warning("No agents available for routing")
                return Command(
                    goto="__end__", update={"routing_error": "No agents available"}
                )

            # Make routing decision
            decision = await self.routing_strategy.make_routing_decision(
                context, available_agents, agent_capabilities, config
            )

            # Validate decision
            if not self.routing_model.validate_choice(decision.choice):
                logger.error(f"Invalid routing choice: {decision.choice}")
                decision = RoutingDecision(
                    choice="END", reasoning="Invalid choice fallback"
                )

            # Log decision
            logger.info(
                f"Routing decision: {decision.choice} (reasoning: {decision.reasoning})"
            )

            # Create routing command
            return self._create_routing_command(decision, state, context)

        except Exception as e:
            logger.exception(f"Routing failed: {e}")
            return Command(goto="__end__", update={"routing_error": str(e)})

    def _extract_context(self, state: Any) -> RoutingContext:
        """Extract routing context from state."""
        messages = getattr(state, "messages", [])

        if not messages:
            return RoutingContext(
                last_message="",
                message_type="empty",
                conversation_length=0,
                task_complexity="Simple",
            )

        last_message = messages[-1]
        last_content = ""
        message_type = "unknown"

        if isinstance(last_message, BaseMessage):
            last_content = str(last_message.content)
            message_type = type(last_message).__name__
        else:
            last_content = str(last_message)

        # Extract task keywords
        task_keywords = TaskClassifier.classify_task(last_content)

        # Get previous agent if available
        previous_agent = getattr(state, "last_agent", None)

        # Estimate complexity
        complexity = TaskClassifier.estimate_complexity(last_content, len(messages))

        return RoutingContext(
            last_message=last_content,
            message_type=message_type,
            task_keywords=task_keywords,
            conversation_length=len(messages),
            previous_agent=previous_agent,
            task_complexity=complexity,
        )

    def _create_routing_command(
        self, decision: RoutingDecision, state: Any, context: RoutingContext
    ) -> Command:
        """Create routing command based on decision."""
        # Prepare state updates
        updates = {
            "routing_decision": decision.choice,
            "routing_timestamp": time.time(),
            "routing_reasoning": decision.reasoning,
            "routing_confidence": decision.confidence,
            "task_keywords": context.task_keywords,
            "task_complexity": context.task_complexity,
        }

        # Handle END case
        if decision.choice == "END":
            updates["conversation_complete"] = True
            return Command(goto="__end__", update=updates)

        # Route to selected agent
        updates["target_agent"] = decision.choice
        return Command(goto=decision.choice, update=updates)

    def print_routing_stats(self) -> None:
        """Print routing engine statistics."""
        table = Table(title="🧭 Dynamic Routing Engine Stats")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Available Agents", str(len(self.routing_model.option_names)))
        table.add_row("Routing Options", ", ".join(self.routing_model.option_names))
        table.add_row("Strategy Type", type(self.routing_strategy).__name__)
        table.add_row("Context Analysis", str(self.enable_context_analysis))
        table.add_row("Has LLM Engine", str(self.routing_engine is not None))

        console.print(table)
