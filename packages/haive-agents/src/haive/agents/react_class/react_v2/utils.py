"""Utility functions for creating and customizing ReactAgents."""

from collections.abc import Callable

from langchain_core.tools import BaseTool, StructuredTool, Tool
from pydantic import BaseModel
from src.haive.core.engine.aug_llm import AugLLMConfig

from src.haive.agents.v2.agent import ReactAgent
from src.haive.agents.v2.config import ReactAgentConfig, ToolsInput
from src.haive.agents.v2.state import create_structured_state


def create_react_agent(
    tools: ToolsInput,
    model: str = "gpt-4o",
    system_prompt: str | None = None,
    name: str | None = None,
    max_iterations: int = 10,
    temperature: float = 0.7,
    parallel_tool_execution: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.5,
    **kwargs,
) -> ReactAgent:
    """Create a ReactAgent with the specified tools and configuration.

    Args:
        tools: Tools available to the agent (list or node mapping)
        model: The model name to use
        system_prompt: Optional system prompt
        name: Optional agent name
        max_iterations: Maximum number of iterations
        temperature: Temperature for LLM generation
        parallel_tool_execution: Whether to execute tools in parallel
        max_retries: Maximum number of retries for tool failures
        retry_delay: Delay between retry attempts in seconds
        **kwargs: Additional configuration options

    Returns:
        Configured ReactAgent instance
    """
    # Create config
    config = ReactAgentConfig.from_tools(
        tools=tools,
        model=model,
        system_prompt=system_prompt,
        name=name,
        temperature=temperature,
        max_iterations=max_iterations,
        parallel_tool_execution=parallel_tool_execution,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )

    # Create and return agent
    return ReactAgent(config)


def create_structured_react_agent(
    output_model: type[BaseModel],
    tools: ToolsInput,
    model: str = "gpt-4o",
    system_prompt: str | None = None,
    name: str | None = None,
    max_iterations: int = 10,
    temperature: float = 0.7,
    parallel_tool_execution: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.5,
    **kwargs,
) -> ReactAgent:
    """Create a ReactAgent that produces structured output according to the specified model.

    Args:
        output_model: Pydantic model for structured output
        tools: Tools available to the agent (list or node mapping)
        model: The model name to use
        system_prompt: Optional system prompt
        name: Optional agent name
        max_iterations: Maximum number of iterations
        temperature: Temperature for LLM generation
        parallel_tool_execution: Whether to execute tools in parallel
        max_retries: Maximum number of retries for tool failures
        retry_delay: Delay between retry attempts in seconds
        **kwargs: Additional configuration options

    Returns:
        Configured ReactAgent instance with structured output support
    """
    # Create structured state class
    state_class = create_structured_state(output_model)

    # Create config
    config = ReactAgentConfig.with_structured_output(
        model_class=output_model,
        tools=tools,
        system_prompt=system_prompt,
        name=name,
        max_iterations=max_iterations,
        temperature=temperature,
        state_schema=state_class,
        parallel_tool_execution=parallel_tool_execution,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )

    # Create and return agent
    return ReactAgent(config)


def organize_tools_by_category(
    tools: list[BaseTool | StructuredTool | Tool | Callable],
    categories: dict[str, list[str]] | None = None,
) -> dict[str, list[BaseTool | StructuredTool | Tool | Callable]]:
    """Organize tools into categories for parallel processing.

    Args:
        tools: List of tools to organize
        categories: Optional mapping of category names to tool names

    Returns:
        Dictionary mapping category names to tool lists
    """
    if not categories:
        # Default to one tool per category
        return {f"tool_{i}": [tool] for i, tool in enumerate(tools)}

    # Create a mapping of tool names to tools
    tool_map = {}
    for tool in tools:
        if hasattr(tool, "name"):
            tool_map[tool.name] = tool
        elif hasattr(tool, "__name__"):
            tool_map[tool.__name__] = tool

    # Organize by categories
    result = {}
    for category, tool_names in categories.items():
        result[category] = [tool_map[name] for name in tool_names if name in tool_map]

    # Add any remaining tools to "other" category
    used_tools = set()
    for tools_list in result.values():
        for tool in tools_list:
            if hasattr(tool, "name"):
                used_tools.add(tool.name)
            elif hasattr(tool, "__name__"):
                used_tools.add(tool.__name__)

    remaining_tools = []
    for tool in tools:
        tool_name = getattr(tool, "name", getattr(tool, "__name__", None))
        if tool_name and tool_name not in used_tools:
            remaining_tools.append(tool)

    if remaining_tools:
        result["other"] = remaining_tools

    return result


def create_agent_with_custom_engine(
    engine: AugLLMConfig,
    tools: ToolsInput,
    name: str | None = None,
    max_iterations: int = 10,
    parallel_tool_execution: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.5,
    **kwargs,
) -> ReactAgent:
    """Create a ReactAgent with a custom engine configuration.

    Args:
        engine: Custom AugLLMConfig
        tools: Tools available to the agent (list or node mapping)
        name: Optional agent name
        max_iterations: Maximum number of iterations
        parallel_tool_execution: Whether to execute tools in parallel
        max_retries: Maximum number of retries for tool failures
        retry_delay: Delay between retry attempts in seconds
        **kwargs: Additional configuration options

    Returns:
        Configured ReactAgent instance
    """
    # Add tools to the engine if they're not already there
    if hasattr(engine, "tools") and not engine.tools:
        if isinstance(tools, dict):
            # Flatten tools from dict
            all_tools = []
            for tool_set in tools.values():
                if isinstance(tool_set, list):
                    all_tools.extend(tool_set)
                else:
                    all_tools.append(tool_set)
            engine.tools = all_tools
        else:
            engine.tools = tools

    # Create config
    config = ReactAgentConfig(
        name=name or f"custom_react_{engine.name}",
        engine=engine,
        tools=tools,
        max_iterations=max_iterations,
        parallel_tool_execution=parallel_tool_execution,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )

    # Create and return agent
    return ReactAgent(config)
