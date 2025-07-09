# src/haive/agents/plan_and_execute/aug_llms.py
"""
AugLLM configurations for Plan and Execute Agent System.

This module defines the AugLLM configurations for planning, execution,
and replanning agents.
"""

from typing import List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.tools import BaseTool

from haive.agents.planning.p_and_e.models import Act, Plan
from haive.agents.planning.p_and_e.prompts import (
    executor_prompt,
    planner_prompt,
    planner_prompt_simple,
    replan_prompt,
)

# ============================================================================
# PLANNER AGENT CONFIGURATION
# ============================================================================


def create_planner_aug_llm_config(
    model_name: str = "gpt-4o", temperature: float = 0.1, use_context: bool = True
) -> AugLLMConfig:
    """
    Create AugLLM configuration for the planning agent.

    Args:
        model_name: The LLM model to use
        temperature: Temperature for generation (lower = more focused)
        use_context: Whether to use the context-aware prompt template

    Returns:
        Configured AugLLMConfig for planning
    """
    return AugLLMConfig(
        name="planner_llm",
        llm_config=AzureLLMConfig(
            model=model_name,
            # temperature=temperature,
            # max_tokens=2000  # Plans can be detailed
        ),
        prompt_template=planner_prompt if use_context else planner_prompt_simple,
        structured_output_model=Plan,
        structured_output_version="v2",
        # Messages field will be auto-detected from prompt
        uses_messages_field=True,
        # Partial variables can be provided at runtime
        partial_variables=(
            {"context": "No additional context provided."}  # Default
            if use_context
            else {}
        ),
    )


# ============================================================================
# EXECUTOR AGENT CONFIGURATION
# ============================================================================


def create_executor_aug_llm_config(
    model_name: str = "gpt-4o",
    # temperature: float = 0.3,
    tools: Optional[List[BaseTool]] = None,
    force_tool_use: bool = False,
) -> AugLLMConfig:
    """
    Create AugLLM configuration for the execution agent.

    Args:
        model_name: The LLM model to use
        temperature: Temperature for generation
        tools: List of tools available to the executor
        force_tool_use: Whether to force tool usage

    Returns:
        Configured AugLLMConfig for execution
    """
    return AugLLMConfig(
        name="executor_llm",
        llm_config=AzureLLMConfig(
            model=model_name,
            # temperature=temperature,
            # max_tokens=1500
        ),
        prompt_template=executor_prompt,
        tools=tools or [],
        force_tool_use=force_tool_use,
        uses_messages_field=True,
        # These will be provided as partial variables at runtime
        partial_variables={
            "plan_status": "",
            "current_step": "",
            "previous_results": "",
        },
    )


# ============================================================================
# REPLAN AGENT CONFIGURATION
# ============================================================================


def create_replan_aug_llm_config(
    model_name: str = "gpt-4o", temperature: float = 0.2, max_replan_attempts: int = 3
) -> AugLLMConfig:
    """
    Create AugLLM configuration for the replanning agent.

    Args:
        model_name: The LLM model to use
        temperature: Temperature for generation
        max_replan_attempts: Maximum number of replanning attempts

    Returns:
        Configured AugLLMConfig for replanning
    """
    return AugLLMConfig(
        name="replan_llm",
        llm_config=AzureLLMConfig(
            model=model_name,
            # temperature=temperature,
            # max_tokens=2000  # Need room for new plans or detailed answers
        ),
        prompt_template=replan_prompt,
        structured_output_model=Act,  # Uses Response | Plan union
        structured_output_version="v2",
        uses_messages_field=True,
        # Runtime partial variables
        partial_variables={
            "objective": "",
            "plan_progress": "",
            "execution_results": "",
        },
        # Store max attempts in runtime_options for agent to use
        runtime_options={"max_replan_attempts": max_replan_attempts},
    )


# ============================================================================
# DEFAULT CONFIGURATIONS
# ============================================================================

# Default instances that can be used directly
planner_aug_llm_config = create_planner_aug_llm_config()
executor_aug_llm_config = create_executor_aug_llm_config()
replan_aug_llm_config = create_replan_aug_llm_config()
