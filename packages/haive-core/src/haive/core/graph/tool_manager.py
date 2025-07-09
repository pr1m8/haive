"""Tool manager wrapper for dynamic tool management."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field

from haive.core.graph.ToolManager import ToolManager as CoreToolManager


class ToolManager(BaseModel):
    """Wrapper for the core ToolManager with simplified interface.

    This class provides a simplified interface for managing tools
    while maintaining compatibility with the existing ToolManager infrastructure.
    """

    name: str = Field(default="tool_manager", description="Name of the tool manager")
    tools: Dict[str, Any] = Field(default_factory=dict, description="Managed tools")

    def __init__(self, name: str = "tool_manager", **kwargs):
        """Initialize a new tool manager."""
        super().__init__(name=name, **kwargs)
        self._core_manager = CoreToolManager()

    def add_tool(self, tool_name: str, tool: Any) -> "ToolManager":
        """Add a tool to the manager."""
        self.tools[tool_name] = tool
        return self

    def get_tool(self, tool_name: str) -> Any:
        """Get a tool by name."""
        return self.tools.get(tool_name)

    def list_tools(self) -> List[str]:
        """List all available tools."""
        return list(self.tools.keys())
