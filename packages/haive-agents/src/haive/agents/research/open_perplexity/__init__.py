"""Open Perplexity - A deep research agent with dynamic document loader selection.

This module provides a comprehensive research agent capable of performing in-depth
research on any topic, dynamically selecting document loaders based on the research
needs, and producing detailed reports with confidence assessments.

Modules:
- agent: Implements the ResearchAgent class that conducts the research process
- config: Defines the configuration for the research agent
- state: Contains state schemas for tracking research progress
- models: Defines data models for research findings and sources
- prompts: Contains prompt templates for different research tasks
- structured_tools: Implements document loader tools and utilities
- engines: Factory functions for creating specialized LLM engines
- react_agent_config: Configuration for React-based sub-agents
- cli: Command-line interface for running research

Classes:
    ResearchAgent: Main agent class that performs research
    ResearchAgentConfig: Configuration for the research agent
    ResearchState: State schema for the research process
    ResearchInputState: Input state schema
    ResearchOutputState: Output state schema
    ResearchSummary: Model for summarizing research findings
    ResearchFinding: Model for individual research findings
    ResearchSource: Model for tracking and evaluating sources
    DataSourceType: Enumeration of data source types
    ContentReliability: Enumeration of content reliability levels
    ContentFreshness: Enumeration of content freshness levels
"""

from haive.agents.research.open_perplexity.agent import ResearchAgent
from haive.agents.research.open_perplexity.config import ResearchAgentConfig
from haive.agents.research.open_perplexity.models import (
    ContentFreshness,
    ContentReliability,
    DataSourceType,
    ResearchDepth,
    ResearchFinding,
    ResearchSource,
    ResearchSummary,
)
from haive.agents.research.open_perplexity.state import (
    ResearchInputState,
    ResearchOutputState,
    ResearchState,
)

__all__ = [
    "ContentFreshness",
    "ContentReliability",
    "DataSourceType",
    "ResearchAgent",
    "ResearchAgentConfig",
    "ResearchDepth",
    "ResearchFinding",
    "ResearchInputState",
    "ResearchOutputState",
    "ResearchSource",
    "ResearchState",
    "ResearchSummary",
]
