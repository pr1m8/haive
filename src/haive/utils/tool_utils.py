from langchain_core.tools import BaseTool
from typing import List
def _format_tool_descriptions(tools: List[BaseTool]) -> str:
    tool_descriptions = []
    for tool in tools:
        tool_descriptions.append(f"- {tool.name}: {tool.description} \n Input: {tool.args_schema}")
    print(tool_descriptions)
    return "\n".join(tool_descriptions)