from pydantic import BaseModel
from typing import Any
from typing import List
from src.haive.agents.self_discover.models import ReasoningModule
from langchain_core.tools import BaseTool
def _format_tool_descriptions(tools: List[BaseTool]) -> str:
    tool_descriptions = []
    for tool in tools:
        tool_descriptions.append(f"- {tool.name}: {tool.description}")
    return "\n".join(tool_descriptions)
def parse_list_to_string(list_to_parse: List[str]) -> str:
    """
    Parse the reasoning modules list into a formatted string.

    Args:
        reasoning_modules (List[str]): The list of reasoning modules.

    Returns:
        str: The reasoning modules formatted as a string.
    """
    return "\n".join(list_to_parse)
def parse_reasoning_modules_to_string(modules: List[ReasoningModule]) -> str:
    """
    Convert a list of ReasoningModule instances into a formatted string.

    Args:
        modules (List[ReasoningModule]): List of reasoning modules.

    Returns:
        str: Reasoning modules formatted as a string.
    """
    return "\n".join([f"- {module.name}: {module.description}" for module in modules])
