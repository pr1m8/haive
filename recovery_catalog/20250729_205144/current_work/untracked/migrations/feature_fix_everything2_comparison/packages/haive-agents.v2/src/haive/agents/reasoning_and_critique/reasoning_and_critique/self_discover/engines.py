"""Engines engine module.

This module provides engines functionality for the Haive framework.

Functions:
    create_select_engine: Create Select Engine functionality.
    create_adapt_engine: Create Adapt Engine functionality.
    create_structure_engine: Create Structure Engine functionality.
"""

# src/haive/agents/selfdiscover/engines.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from haive.agents.reasoning_and_critique.self_discover.models import (
    ModuleAdaptationResult,
    ModuleSelectionResult,
    ReasoningOutput,
    ReasoningStructure,
)


def create_select_engine(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    custom_prompt: str | ChatPromptTemplate | None = None,
    **kwargs
) -> AugLLMConfig:
    """Create the engine for selecting reasoning modules with structured output.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        custom_prompt: Optional custom prompt
        **kwargs: Additional parameters for AugLLMConfig

    Returns:
        AugLLMConfig for selection stage
    """
    # Default prompt for selecting modules
    default_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert problem solver with strong analytical skills.

        Your task is to select the most appropriate reasoning modules for solving a specific problem.

        For each selected module, provide:
        1. The module ID (number)
        2. A brief description of the module
        3. A clear explanation of why this module is particularly relevant for the given task""",
            ),
            (
                "human",
                """
        Select 3-5 reasoning modules that are crucial to utilize in order to solve the given task:

        Available reasoning modules:
        {reasoning_modules}

        Task to solve:
        {task_description}

        Return your answer as a structured selection of modules, explaining why each one is suitable for this task.
        """,
            ),
        ]
    )

    # Use custom prompt if provided
    prompt = custom_prompt if custom_prompt else default_prompt

    # Create LLM config
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Create and return the AugLLMConfig with structured output
    return AugLLMConfig(
        name="select_modules_engine",
        llm_config=llm_config,
        prompt_template=(
            prompt if isinstance(prompt, ChatPromptTemplate | PromptTemplate) else None
        ),
        structured_output_model=ModuleSelectionResult,
        **kwargs
    )


def create_adapt_engine(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    custom_prompt: str | ChatPromptTemplate | None = None,
    **kwargs
) -> AugLLMConfig:
    """Create the engine for adapting selected reasoning modules with structured output.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        custom_prompt: Optional custom prompt
        **kwargs: Additional parameters for AugLLMConfig

    Returns:
        AugLLMConfig for adaptation stage
    """
    # Default prompt for adapting modules
    default_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at customizing reasoning approaches for specific problems.

        Your task is to adapt general reasoning modules to address the specific challenges of the given task.

        For each module, provide:
        1. A reference to the original module ID
        2. A customized description focused on this specific task
        3. A concrete strategy for applying this module to the task""",
            ),
            (
                "human",
                """
        Rephrase and specify each selected reasoning module so that it better helps solving the specific task:

        SELECTED module descriptions:
        {selected_modules}

        Task to solve:
        {task_description}

        Return your answer as a structured list of adapted modules with specific application strategies.
        """,
            ),
        ]
    )

    # Use custom prompt if provided
    prompt = custom_prompt if custom_prompt else default_prompt

    # Create LLM config
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Create and return the AugLLMConfig with structured output
    return AugLLMConfig(
        name="adapt_modules_engine",
        llm_config=llm_config,
        prompt_template=(
            prompt if isinstance(prompt, ChatPromptTemplate | PromptTemplate) else None
        ),
        structured_output_model=ModuleAdaptationResult,
        **kwargs
    )


def create_structure_engine(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    custom_prompt: str | ChatPromptTemplate | None = None,
    **kwargs
) -> AugLLMConfig:
    """Create the engine for creating structured reasoning plans with structured output.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        custom_prompt: Optional custom prompt
        **kwargs: Additional parameters for AugLLMConfig

    Returns:
        AugLLMConfig for structuring stage
    """
    # Default prompt for structuring reasoning
    default_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at creating structured reasoning plans.

        Your task is to create a step-by-step reasoning plan for solving a specific problem.

        For each step in your plan, provide:
        1. A step ID (e.g., "step1", "step2")
        2. A clear description of what needs to be determined in this step
        3. References to which modules this step relates to (optional)""",
            ),
            (
                "human",
                """
        Operationalize the reasoning modules into a step-by-step reasoning plan:

        Adapted module descriptions:
        {adapted_modules}

        Task to solve:
        {task_description}

        Create a detailed reasoning structure that outlines the exact steps needed to solve this problem.
        Each step should have a unique ID and a clear description of what needs to be determined.

        Do NOT solve the problem yet - only create the plan framework.
        """,
            ),
        ]
    )

    # Use custom prompt if provided
    prompt = custom_prompt if custom_prompt else default_prompt

    # Create LLM config
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Create and return the AugLLMConfig with structured output
    return AugLLMConfig(
        name="structure_reasoning_engine",
        llm_config=llm_config,
        prompt_template=(
            prompt if isinstance(prompt, ChatPromptTemplate | PromptTemplate) else None
        ),
        structured_output_model=ReasoningStructure,
        **kwargs
    )


def create_reasoning_engine(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    custom_prompt: str | ChatPromptTemplate | None = None,
    **kwargs
) -> AugLLMConfig:
    """Create the engine for executing reasoning plans with structured output.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        custom_prompt: Optional custom prompt
        **kwargs: Additional parameters for AugLLMConfig

    Returns:
        AugLLMConfig for reasoning stage
    """
    # Default prompt for executing reasoning
    default_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert problem solver who follows structured reasoning plans precisely.

        Your task is to solve a problem by following a given reasoning structure.

        For each step in the structure:
        1. Provide detailed reasoning for that specific step
        2. Include any relevant calculations or logical deductions
        3. Note any interim results

        After completing all steps, provide a clear final answer to the task.""",
            ),
            (
                "human",
                """
        Follow the step-by-step reasoning plan to correctly solve the task.
        Fill in each step with your actual reasoning for this specific problem.

        Reasoning structure:
        {reasoning_structure}

        Task to solve:
        {task_description}

        For each step in the structure, provide your detailed reasoning.
        After working through all steps, provide your final answer with high confidence.
        """,
            ),
        ]
    )

    # Use custom prompt if provided
    prompt = custom_prompt if custom_prompt else default_prompt

    # Create LLM config
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Create and return the AugLLMConfig with structured output
    return AugLLMConfig(
        name="execute_reasoning_engine",
        llm_config=llm_config,
        prompt_template=(
            prompt if isinstance(prompt, ChatPromptTemplate | PromptTemplate) else None
        ),
        structured_output_model=ReasoningOutput,
        **kwargs
    )


def create_selfdiscover_engines(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    select_prompt: str | ChatPromptTemplate | None = None,
    adapt_prompt: str | ChatPromptTemplate | None = None,
    structure_prompt: str | ChatPromptTemplate | None = None,
    reasoning_prompt: str | ChatPromptTemplate | None = None,
    **kwargs
) -> dict[str, AugLLMConfig]:
    """Create all engines for the SelfDiscover agent with structured output models.

    Args:
        model: Model name to use for all engines
        temperature: Temperature for all engines
        select_prompt: Custom prompt for selection stage
        adapt_prompt: Custom prompt for adaptation stage
        structure_prompt: Custom prompt for structuring stage
        reasoning_prompt: Custom prompt for reasoning stage
        **kwargs: Additional parameters for AugLLMConfigs

    Returns:
        Dictionary of AugLLMConfigs for each stage
    """
    return {
        "select": create_select_engine(model, temperature, select_prompt, **kwargs),
        "adapt": create_adapt_engine(model, temperature, adapt_prompt, **kwargs),
        "structure": create_structure_engine(
            model, temperature, structure_prompt, **kwargs
        ),
        "reasoning": create_reasoning_engine(
            model, temperature, reasoning_prompt, **kwargs
        ),
    }
