"""Sphinx extension for automatic agent documentation with examples and.

visualization.
"""

from __future__ import annotations

from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)

# Agent metadata registry
AGENT_METADATA = {
    "SimpleAgent": {
        "category":
        "simple",
        "description":
        "Basic conversational agent for straightforward interactions",
        "example_config": {
            "engine": "AugLLMConfig",
            "params": {
                "temperature": 0.7,
                "system_message": "You are a helpful assistant.",
            },
        },
        "example_usage":
        """
# Single turn conversation
response = await agent.arun("What's the capital of France?")

# Multi-turn with state persistence
config = {"configurable": {"thread_id": "conv-123"}}
await agent.arun("My name is Alice", config=config)
response = await agent.arun("What's my name?", config=config)
""",
        "visualization": {
            "supports_graph": True,
            "graph_type": "simple",
            "state_schema": "MessageState",
        },
        "related_examples": ["simple/example.py"],
        "key_features": [
            "Stateful conversations",
            "Streaming support",
            "Token usage tracking",
            "Persistence integration",
        ],
    },
    "ReactAgent": {
        "category":
        "react",
        "description":
        "Reasoning and acting agent with tool use capabilities",
        "example_config": {
            "tools": ["SearchTool()", "CalculatorTool()"],
            "params": {
                "max_iterations": 5,
                "verbose": True
            },
        },
        "example_usage":
        """
# Research with reasoning
result = await agent.arun(
    "Find the population density of Tokyo and compare to NYC"
)

# Access reasoning trace
trace = agent.get_reasoning_trace()
""",
        "visualization": {
            "supports_graph": True,
            "graph_type": "cyclic",
            "includes_tools": True,
            "state_schema": "ReactState",
        },
        "related_examples": ["react/example.py"],
        "key_features": [
            "Tool integration",
            "Reasoning traces",
            "Error recovery",
            "Parallel tool execution",
        ],
    },
    "BaseRAGAgent": {
        "category":
        "rag",
        "description":
        "Base retrieval-augmented generation agent",
        "example_config": {
            "retriever": "VectorRetriever",
            "params": {
                "collection": "docs",
                "top_k": 5,
                "llm_config": {
                    "temperature": 0.3
                },
            },
        },
        "example_usage":
        """
# Query with retrieval
answer = await agent.arun("What are the main features?")

# Get source documents
sources = agent.get_source_documents()
for doc in sources:
    print(f"Source: {doc.metadata['source']}")
""",
        "visualization": {
            "supports_graph": True,
            "graph_type": "dag",
            "components": ["retriever", "reranker", "generator"],
            "state_schema": "RAGState",
        },
        "related_examples": ["rag/base/example.py"],
        "key_features": [
            "Document retrieval",
            "Source tracking",
            "Reranking support",
            "Context window management",
        ],
    },
    "DebateConversation": {
        "category":
        "conversation",
        "description":
        "Structured debate with multiple participants",
        "example_config": {
            "factory_method": "create_simple_debate",
            "params": {
                "topic": "AI Ethics",
                "position_a": ["Alice", "Pro-regulation"],
                "position_b": ["Bob", "Pro-innovation"],
                "enable_judge": True,
                "arguments_per_side": 3,
            },
        },
        "example_usage":
        """
# Run debate
result = await debate.arun()

# Get debate summary
summary = debate.get_debate_summary()
print(f"Winner: {summary['winner']}")
print(f"Key arguments: {summary['key_points']}")
""",
        "visualization": {
            "supports_graph": True,
            "graph_type": "multi_agent",
            "shows_turns": True,
            "state_schema": "DebateState",
        },
        "related_examples": ["conversation/debate/example.py"],
        "key_features": [
            "Turn management",
            "Argument tracking",
            "Judge integration",
            "Position enforcement",
        ],
    },
    "AdaptiveRAGAgent": {
        "category":
        "rag",
        "description":
        "RAG agent that adapts retrieval strategy based on query",
        "example_config": {
            "strategies": ["simple", "multi_query", "hyde", "fusion"],
            "params": {
                "strategy_selector": "auto",
                "fallback_strategy": "simple"
            },
        },
        "example_usage":
        """
# Complex query with adaptive strategy
result = await agent.arun(
    "Compare pricing tiers focusing on enterprise features"
)

# Check which strategy was used
print(f"Strategy: {agent.last_strategy}")
print(f"Confidence: {agent.strategy_confidence}")
""",
        "visualization": {
            "supports_graph": True,
            "graph_type": "conditional",
            "strategy_flow": True,
            "state_schema": "AdaptiveRAGState",
        },
        "related_examples": ["rag/adaptive_rag/example.py"],
        "key_features": [
            "Strategy selection",
            "Query analysis",
            "Fallback handling",
            "Performance tracking",
        ],
    },
}


class AgentDocDirective(SphinxDirective):
    """Directive to automatically generate agent documentation."""

    has_content = True
    required_arguments = 1  # Agent class name
    optional_arguments = 0
    option_spec = {
        "show-example": lambda x: x.lower() == "true",
        "show-visualization": lambda x: x.lower() == "true",
        "show-config": lambda x: x.lower() == "true",
        "example-style": str,  # 'basic' or 'advanced'
    }

    def run(self):
        agent_name = self.arguments[0].split(".")[-1]  # Get class name

        # Get metadata
        metadata = AGENT_METADATA.get(agent_name, {})
        if not metadata:
            logger.warning(f"No metadata found for agent: {agent_name}")
            metadata = self._get_default_metadata(agent_name)

        # Create content
        content = []

        # Add description
        if metadata.get("description"):
            para = nodes.paragraph()
            para += nodes.Text(metadata["description"])
            content.append(para)

        # Add key features
        if metadata.get("key_features"):
            features_section = nodes.section()
            features_section += nodes.title(text="Key Features")

            feature_list = nodes.bullet_list()
            for feature in metadata["key_features"]:
                item = nodes.list_item()
                item += nodes.paragraph(text=feature)
                feature_list += item

            features_section += feature_list
            content.append(features_section)

        # Add example if requested
        if self.options.get("show-example", True):
            example_section = self._create_example_section(
                agent_name, metadata)
            if example_section:
                content.append(example_section)

        # Add visualization info
        if self.options.get("show-visualization", True):
            viz_section = self._create_visualization_section(
                agent_name, metadata)
            if viz_section:
                content.append(viz_section)

        # Add configuration details
        if self.options.get("show-config", True):
            config_section = self._create_config_section(agent_name, metadata)
            if config_section:
                content.append(config_section)

        return content

    def _get_default_metadata(self, agent_name: str) -> dict[str, Any]:
        """Generate default metadata for agents without explicit entries."""
        category = "unknown"
        if "RAG" in agent_name:
            category = "rag"
        elif "React" in agent_name:
            category = "react"
        elif "Conversation" in agent_name or "Debate" in agent_name:
            category = "conversation"
        elif "Simple" in agent_name:
            category = "simple"

        return {
            "category": category,
            "description": f"{agent_name} - AI agent implementation",
            "visualization": {
                "supports_graph": True,
                "graph_type": "simple"
            },
        }

    def _create_example_section(
        self,
        agent_name: str,
        metadata: dict[str, Any],
    ) -> nodes.section | None:
        """Create example usage section."""
        section = nodes.section()
        section += nodes.title(text="Example Usage")

        # Configuration example
        if metadata.get("example_config"):
            config_title = nodes.paragraph()
            config_title += nodes.strong(text="Configuration:")
            section += config_title

            config_code = self._format_config_example(
                agent_name,
                metadata["example_config"],
            )
            literal = nodes.literal_block(config_code, config_code)
            literal["language"] = "python"
            section += literal

        # Usage example
        if metadata.get("example_usage"):
            usage_title = nodes.paragraph()
            usage_title += nodes.strong(text="Usage:")
            section += usage_title

            literal = nodes.literal_block(
                metadata["example_usage"],
                metadata["example_usage"],
            )
            literal["language"] = "python"
            section += literal

        return section if len(section) > 1 else None

    def _create_visualization_section(
        self,
        agent_name: str,
        metadata: dict[str, Any],
    ) -> nodes.section | None:
        """Create visualization section."""
        viz_info = metadata.get("visualization", {})
        if not viz_info.get("supports_graph"):
            return None

        section = nodes.section()
        section += nodes.title(text="Visualization")

        # Graph type info
        para = nodes.paragraph()
        para += nodes.Text(
            f"This agent supports graph visualization (type: {
                viz_info.get(
                    'graph_type', 'simple')})", )
        section += para

        # Visualization code
        viz_code = f"""
# Visualize the agent's execution graph
agent.visualize_graph("{agent_name.lower()}_graph.png")

# Interactive HTML visualization
agent.visualize_graph("{agent_name.lower()}_graph.html", format="html")
"""
        literal = nodes.literal_block(viz_code, viz_code)
        literal["language"] = "python"
        section += literal

        return section

    def _create_config_section(
        self,
        agent_name: str,
        metadata: dict[str, Any],
    ) -> nodes.section | None:
        """Create configuration details section."""
        section = nodes.section()
        section += nodes.title(text="Configuration Details")

        # Add any specific configuration notes
        if metadata.get("state_schema"):
            para = nodes.paragraph()
            para += nodes.Text("State Schema: ")
            para += nodes.literal(text=metadata["state_schema"])
            section += para

        return section if len(section) > 1 else None

    def _format_config_example(self, agent_name: str,
                               config: dict[str, Any]) -> str:
        """Format configuration example."""
        lines = [f"from haive.agents import {agent_name}"]

        if config.get("factory_method"):
            lines.append(f"\nagent = {agent_name}.{config['factory_method']}(")
        else:
            lines.append(f"\nagent = {agent_name}(")

        # Add parameters
        params = config.get("params", {})
        for key, value in params.items():
            if isinstance(value, str):
                lines.append(f'    {key}="{value}",')
            else:
                lines.append(f"    {key}={value},")

        # Add tools if specified
        if config.get("tools"):
            lines.append(f"    tools=[{', '.join(config['tools'])}],")

        lines.append(")")

        return "\n".join(lines)


class AgentGalleryDirective(SphinxDirective):
    """Directive to generate agent gallery."""

    has_content = False
    optional_arguments = 1  # Category filter

    def run(self):
        category_filter = self.arguments[0] if self.arguments else None

        # Group agents by category
        categories = {}
        for agent_name, metadata in AGENT_METADATA.items():
            category = metadata.get("category", "other")
            if category_filter and category != category_filter:
                continue

            if category not in categories:
                categories[category] = []
            categories[category].append((agent_name, metadata))

        # Create gallery
        content = []
        for category, agents in sorted(categories.items()):
            section = nodes.section()
            section += nodes.title(text=category.replace("_", " ").title())

            # Create grid for agents
            for agent_name, metadata in agents:
                card = self._create_agent_card(agent_name, metadata)
                section += card

            content.append(section)

        return content

    def _create_agent_card(
        self,
        agent_name: str,
        metadata: dict[str, Any],
    ) -> nodes.container:
        """Create a card for an agent."""
        card = nodes.container()
        card["classes"] = ["agent-card"]

        # Title
        title = nodes.paragraph()
        title += nodes.strong(text=agent_name)
        card += title

        # Description
        desc = nodes.paragraph()
        desc += nodes.Text(metadata.get("description", ""))
        card += desc

        # Features
        if metadata.get("key_features"):
            features = nodes.bullet_list()
            features["classes"] = ["compact"]
            for feature in metadata["key_features"][:3]:  # Show first 3
                item = nodes.list_item()
                item += nodes.paragraph(text=feature)
                features += item
            card += features

        return card


def setup(app: Sphinx):
    """Setup the extension."""
    app.add_directive("agent-doc", AgentDocDirective)
    app.add_directive("agent-gallery", AgentGalleryDirective)

    # Add CSS for agent cards
    app.add_css_file("agent_docs.css")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
