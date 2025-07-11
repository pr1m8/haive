# src/haive/agents/person_research/config.py

from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AnthropicLLMConfig
from pydantic import Field


class PersonResearchAgentConfig(AgentConfig):
    """Configuration for the Person Research Agent."""

    name: str = Field(default="person_research_agent", description="Name of the agent")

    # Use Claude model by default
    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="research_engine",
            llm_config=AnthropicLLMConfig(
                model="claude-3-5-sonnet-latest",
                parameters={"temperature": 0.0, "max_tokens": 4000},
            ),
        )
    )

    # Add additional engines for specific tasks
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            "query_generator": AugLLMConfig(
                name="query_generator",
                llm_config=AnthropicLLMConfig(
                    model="claude-3-5-sonnet-latest", parameters={"temperature": 0.0}
                ),
            ),
            "researcher": AugLLMConfig(
                name="researcher",
                llm_config=AnthropicLLMConfig(
                    model="claude-3-5-sonnet-latest", parameters={"temperature": 0.0}
                ),
            ),
            "extractor": AugLLMConfig(
                name="extractor",
                llm_config=AnthropicLLMConfig(
                    model="claude-3-5-sonnet-latest", parameters={"temperature": 0.0}
                ),
            ),
            "reflection": AugLLMConfig(
                name="reflection",
                llm_config=AnthropicLLMConfig(
                    model="claude-3-5-sonnet-latest", parameters={"temperature": 0.0}
                ),
            ),
        }
    )

    # Agent-specific settings
    agent_settings: dict[str, Any] = Field(
        default_factory=lambda: {
            "max_search_queries": 3,  # Max search queries per person
            "max_search_results": 3,  # Max search results per query
            "max_reflection_steps": 0,  # Max reflection steps
            "tavily_api_key": None,  # Will be loaded from environment
        }
    )
