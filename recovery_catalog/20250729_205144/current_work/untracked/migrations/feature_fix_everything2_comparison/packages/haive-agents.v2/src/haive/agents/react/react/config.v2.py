"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    ReactAgentConfig: ReactAgentConfig implementation.
"""

from haive.core.graph.branches.branch import Branch
from haive.core.types import Tool_Type
from langgraph.types import RetryPolicy
from pydantic import Field

from haive.agents.simple.config import SimpleAgentConfig


class ReactAgentConfig(SimpleAgentConfig):
    """Configuration for the React Agent."""

    tools: list[Tool_Type] = Field(
        default_factory=list, description="The tools to use for the agent"
    )
    continuation_branch: Branch = Field(description="The branch to continue the agent")
    max_iterations: int = Field(
        default=10, description="The maximum number of iterations for the agent"
    )
    retry_policy: RetryPolicy = Field(description="The retry policy for the agent")
