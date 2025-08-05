"""Agent Cache Loader - Load cached agent execution data for documentation demos.

This module loads pre-generated agent execution data and formats it for
use in Jinja2 templates and documentation generation.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AgentCacheLoader:
    """Loads and processes cached agent execution data."""

    def __init__(self, cache_dir: Path | None = None):
        """Initialize with cache directory."""
        if cache_dir is None:
            cache_dir = Path(__file__).parent
        self.cache_dir = Path(cache_dir)
        self._cache = {}

    def load_agent_cache(self, agent_type: str) -> dict[str, Any]:
        """Load cached execution data for an agent type.

        Args:
            agent_type: Agent type (e.g., 'simple', 'react', 'rag')

        Returns:
            Dictionary containing cached execution data
        """
        cache_key = f"agent_cache_{agent_type}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            logger.warning(f"Cache file not found: {cache_file}")
            return self._get_fallback_data(agent_type)

        try:
            with open(cache_file) as f:
                cache_data = json.load(f)

            # Process and clean the data
            processed_data = self._process_cache_data(cache_data)

            # Store in memory cache
            self._cache[cache_key] = processed_data

            logger.info(
                f"✅ Loaded cache for {agent_type} with {len(processed_data['executions'])} executions"
            )
            return processed_data

        except Exception as e:
            logger.exception(f"Error loading cache for {agent_type}: {e}")
            return self._get_fallback_data(agent_type)

    def _process_cache_data(self, cache_data: dict[str, Any]) -> dict[str, Any]:
        """Process and clean cached data for template use."""
        processed = cache_data.copy()

        # Process each execution
        for execution in processed.get("executions", []):
            # Extract clean response text from agent output
            agent_output = execution.get("agent_output", "")

            # Try to extract the actual AI response text
            if "AIMessage(content=" in agent_output:
                # Extract the response from the message format
                try:
                    # Find the last AIMessage content
                    import re

                    ai_messages = re.findall(
                        r"AIMessage\(content='([^']*)'", agent_output
                    )
                    if ai_messages:
                        execution["clean_response"] = ai_messages[-1]
                    else:
                        # Try with double quotes
                        ai_messages = re.findall(
                            r'AIMessage\(content="([^"]*)"', agent_output
                        )
                        if ai_messages:
                            execution["clean_response"] = ai_messages[-1]
                        else:
                            execution["clean_response"] = (
                                "AI response extraction failed"
                            )
                except Exception as e:
                    logger.warning(f"Could not extract clean response: {e}")
                    execution["clean_response"] = "Response text unavailable"
            else:
                execution["clean_response"] = str(agent_output)

            # Extract token usage if available
            if "token_usage" in agent_output:
                try:
                    import re

                    token_match = re.search(r"'total_tokens': (\d+)", agent_output)
                    if token_match:
                        execution["token_usage"] = int(token_match.group(1))
                    else:
                        execution["token_usage"] = 0
                except Exception:
                    execution["token_usage"] = 0
            else:
                execution["token_usage"] = 0

            # Format execution summary
            summary = execution.get("execution_summary", {})
            if summary.get("duration_seconds"):
                execution["duration_formatted"] = f"{summary['duration_seconds']:.2f}s"
            else:
                execution["duration_formatted"] = "N/A"

        return processed

    def _get_fallback_data(self, agent_type: str) -> dict[str, Any]:
        """Get fallback data when cache is not available."""
        return {
            "agent_type": agent_type,
            "agent_name": f"{agent_type.title()}Agent",
            "agent_class": f"haive.agents.{agent_type}.{agent_type.title()}Agent",
            "generated_at": "N/A",
            "executions": [
                {
                    "execution_id": f"{agent_type}_demo_fallback",
                    "input_text": "Hello! Can you demonstrate your capabilities?",
                    "clean_response": f"I'm a {agent_type} agent designed to help with various tasks. This is fallback demo data.",
                    "token_usage": 0,
                    "duration_formatted": "N/A",
                    "execution_summary": {
                        "duration_seconds": 0,
                        "total_events": 0,
                        "total_steps": 0,
                        "state_updates": 0,
                    },
                    "execution_trace": [],
                    "state_history": [],
                    "graph_data": {},
                    "visualization_data": {},
                    "streaming_events": [],
                }
            ],
        }

    def get_agent_demo_data(self, agent_type: str) -> dict[str, Any]:
        """Get formatted demo data for agent documentation.

        Args:
            agent_type: Agent type (e.g., 'simple', 'react', 'rag')

        Returns:
            Dictionary formatted for Jinja2 templates
        """
        cache_data = self.load_agent_cache(agent_type)

        # Get the first execution as primary demo
        execution = cache_data["executions"][0] if cache_data["executions"] else {}

        # Format for template use
        demo_data = {
            # Agent metadata
            "agent_name": cache_data.get("agent_name", f"{agent_type.title()}Agent"),
            "agent_description": self._get_agent_description(agent_type),
            "agent_icon": self._get_agent_icon(agent_type),
            "agent_type": agent_type,
            "agent_class": cache_data.get("agent_class", f"haive.agents.{agent_type}"),
            "agent_module_import": f"haive.agents.{agent_type}",
            # Features and capabilities
            "agent_features": self._get_agent_features(agent_type),
            "agent_config": self._get_agent_config(agent_type),
            "agent_architecture_details": self._get_agent_architecture(agent_type),
            # Execution data from cache
            "example_input": execution.get("input_text", "Hello! Can you help me?"),
            "example_output": execution.get("clean_response", "I am ready to help!"),
            "execution_duration": execution.get("duration_formatted", "N/A"),
            "token_usage": execution.get("token_usage", 0),
            # Visualization data
            "graph_data": execution.get("graph_data", {}),
            "state_history": execution.get("state_history", []),
            "execution_trace": execution.get("execution_trace", []),
            # JSON serialization for JavaScript
            "graph_data_json": json.dumps(execution.get("graph_data", {})),
            "state_history_json": json.dumps(execution.get("state_history", [])),
            "execution_trace_json": json.dumps(execution.get("execution_trace", [])),
            # Cache metadata
            "cache_generated_at": cache_data.get("generated_at", "N/A"),
            "cache_available": len(cache_data["executions"]) > 0,
        }

        return demo_data

    def _get_agent_description(self, agent_type: str) -> str:
        """Get agent description."""
        descriptions = {
            "simple": "A straightforward conversational agent for general-purpose tasks",
            "react": "A reasoning and acting agent with tool use capabilities",
            "rag": "A retrieval-augmented generation agent with knowledge base integration",
        }
        return descriptions.get(
            agent_type, f"A {agent_type} agent for specialized tasks"
        )

    def _get_agent_icon(self, agent_type: str) -> str:
        """Get agent icon emoji."""
        icons = {"simple": "🤖", "react": "⚡", "rag": "📚"}
        return icons.get(agent_type, "🔧")

    def _get_agent_features(self, agent_type: str) -> list[str]:
        """Get agent features list."""
        features = {
            "simple": [
                "Conversational AI",
                "General-purpose assistance",
                "Message-based interaction",
                "Persistent state management",
            ],
            "react": [
                "Reasoning and planning",
                "Tool use and integration",
                "Multi-step workflows",
                "Adaptive problem solving",
            ],
            "rag": [
                "Knowledge retrieval",
                "Document understanding",
                "Context-aware responses",
                "Source attribution",
            ],
        }
        return features.get(agent_type, [f"{agent_type} capabilities"])

    def _get_agent_config(self, agent_type: str) -> str:
        """Get agent configuration example."""
        configs = {
            "simple": "AugLLMConfig(temperature=0.7)",
            "react": "AugLLMConfig(temperature=0.3, tools=[...])",
            "rag": "AugLLMConfig(temperature=0.5, retriever=...)",
        }
        return configs.get(agent_type, "AugLLMConfig()")

    def _get_agent_architecture(self, agent_type: str) -> str:
        """Get agent architecture description."""
        architectures = {
            "simple": "Single-node graph with LLM engine and state management",
            "react": "Multi-node graph with reasoning, tool use, and decision loops",
            "rag": "Graph with retrieval, context injection, and generation nodes",
        }
        return architectures.get(agent_type, f"{agent_type} architecture")


# Global cache loader instance
_cache_loader = AgentCacheLoader()


def get_agent_demo_context(agent_type: str) -> dict[str, Any]:
    """Get agent demo context for Jinja2 templates.

    Args:
        agent_type: Agent type (e.g., 'simple', 'react', 'rag')

    Returns:
        Dictionary containing demo data for templates
    """
    return _cache_loader.get_agent_demo_data(agent_type)


def get_available_agent_types() -> list[str]:
    """Get list of available agent types with cached data."""
    cache_dir = Path(__file__).parent
    cache_files = list(cache_dir.glob("agent_cache_*.json"))

    agent_types = []
    for cache_file in cache_files:
        # Extract agent type from filename
        agent_type = cache_file.stem.replace("agent_cache_", "")
        agent_types.append(agent_type)

    return sorted(agent_types)
