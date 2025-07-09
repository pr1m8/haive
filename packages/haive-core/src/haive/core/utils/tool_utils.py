from langchain_core.tools import BaseTool


def _format_tool_descriptions(tools: list[BaseTool]) -> str:
    tool_descriptions = []
    for tool in tools:
        tool_descriptions.append(f"- {tool.name}: {tool.description}")
    return "\n".join(tool_descriptions)
