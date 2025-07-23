"""
Core Agent Registry Pattern
===========================

This example demonstrates the haive.core.engine.agent pattern, which uses
a registry-based approach for agent configuration and instantiation.
"""

# %%
# Import Required Components
# --------------------------
# Import the core agent system components.

import os
from typing import Any, Dict

from haive.agents.base.agent import Agent, AgentConfig, register_agent
from haive.core.schema.message import BaseMessage
from pydantic import Field

# Disable checkpointer for this example
os.environ["HAIVE_DISABLE_CHECKPOINTER"] = "true"

# %%
# Define a Custom Agent Configuration
# -----------------------------------
# First, we'll create a custom configuration class that extends AgentConfig.


class AnalyzerConfig(AgentConfig):
    """Configuration for our custom analyzer agent."""

    analysis_depth: str = Field(
        default="detailed",
        description="Level of analysis: 'basic', 'detailed', or 'comprehensive'",
    )

    focus_areas: list[str] = Field(
        default_factory=lambda: ["summary", "insights"],
        description="Areas to focus analysis on",
    )

    def model_post_init(self, __context: Any) -> None:
        """Set defaults after initialization."""
        super().model_post_init(__context)
        self.agent_class = "AnalyzerAgent"  # Link to agent class


# %%
# Define the Agent Implementation
# -------------------------------
# Now we'll create the actual agent class and register it.


@register_agent(AnalyzerConfig)
class AnalyzerAgent(Agent[AnalyzerConfig]):
    """A custom analyzer agent using the core pattern."""

    def build_graph(self, schema_map: dict[str, Any]) -> Any:
        """Build the agent's processing graph."""
        # In a real implementation, this would build a StateGraph
        # For this example, we'll create a simple mock structure
        return {"nodes": ["analyze", "summarize"], "edges": [("analyze", "summarize")]}

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Async processing of messages."""
        # Mock implementation
        return {
            "analysis": "Detailed analysis of input",
            "depth": self.config.analysis_depth,
        }

    def invoke(
        self,
        messages: list[BaseMessage],
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Synchronous processing of messages."""
        # Mock implementation
        return {
            "analysis": "Detailed analysis of input",
            "depth": self.config.analysis_depth,
        }


# %%
# Instantiate Agent Using Configuration
# -------------------------------------
# Create an agent instance using the configuration.

# Create configuration
config = AnalyzerConfig(
    name="market_analyzer",
    analysis_depth="comprehensive",
    focus_areas=["trends", "risks", "opportunities"],
)

print(f"Configuration created: {config.name}")
print(f"Analysis depth: {config.analysis_depth}")
print(f"Focus areas: {config.focus_areas}")

# %%
# Agent Creation from Configuration
# ---------------------------------
# In the core pattern, agents are typically created from configurations.

# Create agent instance
agent = config.build()  # This uses the registry to instantiate the correct agent

print(f"\nAgent created: {type(agent).__name__}")
print(f"Agent configuration: {agent.config.name}")

# %%
# Registry Pattern Benefits
# -------------------------
# The registry pattern provides several advantages:

print("\n=== Core Agent Registry Pattern Benefits ===")
print("✓ Type-safe configuration with Pydantic models")
print("✓ Automatic agent discovery via @register_agent decorator")
print("✓ Clear separation between configuration and implementation")
print("✓ Easy serialization/deserialization of agent configs")
print("✓ Support for complex agent hierarchies")

# %%
# Show Registry Contents
# ----------------------
# Display what's in the agent registry.

from haive.core.engine.agent import AGENT_REGISTRY

print("\n=== Registered Agent Types ===")
for config_class, agent_class in AGENT_REGISTRY.items():
    print(f"Config: {config_class.__name__} → Agent: {agent_class.__name__}")

# %%
# Configuration Serialization
# ---------------------------
# Configurations can be easily serialized for storage or transmission.

# Serialize to dict
config_dict = config.model_dump()
print("\n=== Serialized Configuration ===")
print(config_dict)

# Recreate from dict
restored_config = AnalyzerConfig(**config_dict)
print(f"\nRestored config: {restored_config.name}")

print("\nExample completed!")
