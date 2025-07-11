"""Agent base class with integrated token usage tracking.

This module provides an enhanced Agent base class that automatically tracks
token usage for all LLM interactions, providing cost analysis and capacity
monitoring capabilities.
"""

import logging
from typing import Any, Literal

from haive.core.schema import MessagesStateWithTokenUsage, SchemaComposer
from pydantic import Field

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class TokenTrackingAgent(Agent):
    """Agent base class with automatic token usage tracking.

    This enhanced agent automatically tracks token usage for all LLM interactions,
    providing detailed metrics on token consumption, costs, and capacity usage.
    It uses MessagesStateWithTokenUsage as the default state schema.

    Additional features:
    - Automatic token extraction from LLM responses
    - Cost calculation based on provider pricing
    - Capacity percentage monitoring
    - Token usage history tracking
    - Conversation cost analysis

    Example:
        ```python
        class MyAgent(TokenTrackingAgent):
            def build_graph(self):
                # Your graph logic
                pass

        agent = MyAgent(
            name="cost_aware_agent",
            engine=llm_engine,
            track_costs=True,
            input_cost_per_1k=0.003,
            output_cost_per_1k=0.015
        )

        # After running
        result = agent.invoke({"query": "Hello"})
        usage = agent.get_token_usage_summary()
        print(f"Total tokens: {usage['total_tokens']}")
        print(f"Total cost: ${usage['total_cost']:.4f}")
        ```
    """

    # Token tracking configuration
    track_costs: bool = Field(
        default=True, description="Whether to calculate token costs"
    )

    input_cost_per_1k: float = Field(
        default=0.0, description="Cost per 1000 input tokens"
    )

    output_cost_per_1k: float = Field(
        default=0.0, description="Cost per 1000 output tokens"
    )

    cached_input_cost_per_1k: float | None = Field(
        default=None, description="Cost per 1000 cached input tokens (if applicable)"
    )

    def _setup_schemas(self) -> None:
        """Generate schemas with token tracking support."""
        # Only generate if not already provided
        if self.state_schema:
            logger.debug(f"State schema already provided for {self.name}")
            self._auto_derive_io_schemas()
            return

        # Check if we should use token tracking
        use_token_tracking = True  # Default for TokenTrackingAgent

        # Collect engines
        engine_list = []
        if self.engine:
            engine_list.append(self.engine)

        for _name, component in self.engines.items():
            if isinstance(component, str):
                continue
            if not isinstance(component, Agent):
                engine_list.append(component)

        if engine_list:
            # Create composer
            composer = SchemaComposer(name=f"{self.__class__.__name__}State")

            # Check if base would be MessagesState
            for engine in engine_list:
                composer.add_engine(engine)
                composer.add_fields_from_engine(engine)

            # Build initial schema to check base class
            temp_schema = composer.build()

            # If it's messages-based and we want token tracking
            if use_token_tracking and hasattr(temp_schema, "messages"):
                # Use MessagesStateWithTokenUsage directly
                self.state_schema = type(
                    f"{self.__class__.__name__}StateWithTokens",
                    (MessagesStateWithTokenUsage,),
                    {},
                )
                logger.debug("Using MessagesStateWithTokenUsage for token tracking")
            else:
                # Use the regular schema
                self.state_schema = temp_schema
        else:
            # No engines - use token tracking messages state
            self.state_schema = MessagesStateWithTokenUsage
            logger.debug("Using MessagesStateWithTokenUsage as default")

        # Derive I/O schemas
        self._auto_derive_io_schemas()

    def get_token_usage_summary(self) -> dict[str, Any]:
        """Get token usage summary from the current state.

        Returns:
            Dictionary with token usage statistics
        """
        if hasattr(self, "_state") and hasattr(self._state, "get_token_usage_summary"):
            return self._state.get_token_usage_summary()
        return {"total_tokens": 0, "total_cost": 0.0, "message_count": 0, "rounds": 0}

    def calculate_conversation_costs(self) -> None:
        """Calculate costs for the current conversation."""
        if hasattr(self, "_state") and hasattr(self._state, "calculate_costs"):
            self._state.calculate_costs(
                input_cost_per_1k=self.input_cost_per_1k,
                output_cost_per_1k=self.output_cost_per_1k,
                cached_input_cost_per_1k=self.cached_input_cost_per_1k,
            )
