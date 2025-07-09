"""MCP (Model Context Protocol) mixin for adding MCP support to configurations.

This module provides a mixin that enhances configuration classes with MCP integration
capabilities. It enables automatic discovery and wrapping of MCP tools, resource
management, and prompt template integration while maintaining compatibility with
existing Haive patterns.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins import MCPMixin
    from haive.mcp.config import MCPConfig, MCPServerConfig

    class MyConfig(MCPMixin, BaseModel):
        name: str

    # Create config with MCP support
    config = MyConfig(
        name="agent",
        mcp_config=MCPConfig(
            enabled=True,
            servers={
                "filesystem": MCPServerConfig(
                    transport="stdio",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem"]
                )
            }
        )
    )

    # Initialize MCP (discovers tools, resources, prompts)
    await config.setup_mcp()

    # Access MCP tools (automatically wrapped)
    tools = config.get_mcp_tools()

    # Access MCP resources
    resources = config.get_mcp_resources()

    # Use MCP-enhanced system prompt
    enhanced_prompt = config.enhance_system_prompt_with_mcp("Base prompt")
    ```
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr

# Type checking imports
if TYPE_CHECKING:
    from haive.mcp.config import MCPConfig
    from haive.mcp.manager import MCPManager

logger = logging.getLogger(__name__)


class MCPResource(BaseModel):
    """Model representing an MCP resource."""

    uri: str = Field(..., description="Resource URI")
    name: str = Field(..., description="Resource name")
    description: str = Field(default="", description="Resource description")
    mime_type: str = Field(default="application/json", description="MIME type")
    content: Optional[Any] = Field(None, description="Cached content")


class MCPPromptTemplate(BaseModel):
    """Model representing an MCP prompt template."""

    name: str = Field(..., description="Prompt name")
    description: str = Field(..., description="Prompt description")
    arguments: List[Dict[str, Any]] = Field(
        default_factory=list, description="Prompt arguments"
    )
    template: str = Field(default="", description="Prompt template string")


class MCPToolWrapper(BaseTool):
    """Wrapper to convert MCP tools to Haive-compatible tools.

    This wrapper allows MCP tools to be used seamlessly within the Haive
    framework by adapting their interface to match BaseTool expectations.
    """

    name: str
    description: str
    mcp_tool: Dict[str, Any]
    mcp_client: Any  # MCPClient instance

    def _run(self, **kwargs: Any) -> Any:
        """Synchronous execution (not implemented for MCP)."""
        raise NotImplementedError("MCP tools only support async execution")

    async def _arun(self, **kwargs: Any) -> Any:
        """Execute the MCP tool asynchronously.

        Args:
            **kwargs: Tool arguments

        Returns:
            Tool execution result
        """
        try:
            result = await self.mcp_client.call_tool(self.name, arguments=kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing MCP tool {self.name}: {e}")
            raise


class MCPMixin(BaseModel):
    """Mixin for adding MCP (Model Context Protocol) support to configurations.

    This mixin provides seamless integration with MCP servers, enabling:
    - Automatic discovery and wrapping of MCP tools
    - Resource loading and caching from MCP servers
    - Prompt template management
    - Enhanced system prompts with MCP information

    The mixin is designed to work with ToolRouteMixin for proper tool routing
    and can be combined with other mixins in the configuration hierarchy.

    Attributes:
        mcp_config: Optional MCP configuration for server connections
        mcp_resources: List of discovered MCP resources
        mcp_prompts: Dictionary of MCP prompt templates
        auto_discover_mcp_tools: Whether to automatically discover MCP tools
        inject_mcp_resources: Whether to inject resources into context
        use_mcp_prompts: Whether to use MCP prompts for enhancement
    """

    # MCP configuration
    mcp_config: Optional["MCPConfig"] = Field(
        None, description="MCP configuration for server connections"
    )

    # MCP resources and prompts
    mcp_resources: List[MCPResource] = Field(
        default_factory=list, description="MCP resources available to the configuration"
    )

    mcp_prompts: Dict[str, MCPPromptTemplate] = Field(
        default_factory=dict, description="MCP prompt templates"
    )

    # Control flags
    auto_discover_mcp_tools: bool = Field(
        default=True, description="Automatically discover and add MCP tools"
    )

    inject_mcp_resources: bool = Field(
        default=True, description="Inject MCP resources into context"
    )

    use_mcp_prompts: bool = Field(
        default=True, description="Use MCP prompts to enhance system prompts"
    )

    # Private attributes
    _mcp_manager: Optional["MCPManager"] = PrivateAttr(default=None)
    _mcp_tools: List[MCPToolWrapper] = PrivateAttr(default_factory=list)

    async def setup_mcp(self) -> None:
        """Initialize MCP integration.

        Sets up the MCP manager, discovers tools, loads resources, and
        configures prompts based on the MCP configuration.

        This method should be called after creating the configuration but
        before using any MCP features.
        """
        if not self.mcp_config or not getattr(self.mcp_config, "enabled", False):
            logger.info("MCP not enabled or configured")
            return

        try:
            # Lazy import to avoid circular dependencies
            from haive.mcp.manager import MCPManager

            # Create MCP manager
            self._mcp_manager = MCPManager(self.mcp_config)
            await self._mcp_manager.initialize()

            # Discover and wrap tools
            if self.auto_discover_mcp_tools:
                await self._discover_mcp_tools()

            # Load resources
            if self.inject_mcp_resources:
                await self._load_mcp_resources()

            # Load prompts
            if self.use_mcp_prompts:
                await self._load_mcp_prompts()

            logger.info("MCP integration setup complete")

        except Exception as e:
            logger.error(f"Error setting up MCP integration: {e}")
            raise

    async def _discover_mcp_tools(self) -> None:
        """Discover and wrap MCP tools as Haive tools."""
        if not self._mcp_manager:
            return

        self._mcp_tools.clear()

        for server_name, client in self._mcp_manager.clients.items():
            try:
                # Get tools from server
                tools = await client.list_tools()

                for tool in tools:
                    # Create wrapper
                    wrapper = MCPToolWrapper(
                        name=f"{server_name}_{tool['name']}",
                        description=tool.get("description", ""),
                        mcp_tool=tool,
                        mcp_client=client,
                    )
                    self._mcp_tools.append(wrapper)

                    # If this mixin is used with ToolRouteMixin, add the tool
                    if hasattr(self, "add_tool"):
                        self.add_tool(
                            wrapper,
                            route="mcp_tool",
                            metadata={
                                "mcp_server": server_name,
                                "original_name": tool["name"],
                            },
                        )

                logger.info(f"Discovered {len(tools)} tools from {server_name}")

            except Exception as e:
                logger.error(f"Error discovering tools from {server_name}: {e}")

    async def _load_mcp_resources(self) -> None:
        """Load MCP resources from connected servers."""
        if not self._mcp_manager:
            return

        self.mcp_resources.clear()

        for server_name, client in self._mcp_manager.clients.items():
            try:
                # List resources
                resources = await client.list_resources()

                for resource in resources:
                    mcp_resource = MCPResource(
                        uri=resource["uri"],
                        name=resource.get("name", resource["uri"]),
                        description=resource.get("description", ""),
                        mime_type=resource.get("mimeType", "application/json"),
                    )
                    self.mcp_resources.append(mcp_resource)

                logger.info(f"Loaded {len(resources)} resources from {server_name}")

            except Exception as e:
                logger.error(f"Error loading resources from {server_name}: {e}")

    async def _load_mcp_prompts(self) -> None:
        """Load MCP prompts from connected servers."""
        if not self._mcp_manager:
            return

        self.mcp_prompts.clear()

        for server_name, client in self._mcp_manager.clients.items():
            try:
                # List prompts
                prompts = await client.list_prompts()

                for prompt in prompts:
                    template = MCPPromptTemplate(
                        name=prompt["name"],
                        description=prompt.get("description", ""),
                        arguments=prompt.get("arguments", []),
                        template="",  # Would need to fetch actual template
                    )
                    self.mcp_prompts[f"{server_name}_{prompt['name']}"] = template

                logger.info(f"Loaded {len(prompts)} prompts from {server_name}")

            except Exception as e:
                logger.error(f"Error loading prompts from {server_name}: {e}")

    def get_mcp_tools(self) -> List[MCPToolWrapper]:
        """Get all discovered MCP tools.

        Returns:
            List of MCP tool wrappers
        """
        return self._mcp_tools.copy()

    def get_mcp_resources(self) -> List[MCPResource]:
        """Get all loaded MCP resources.

        Returns:
            List of MCP resources
        """
        return self.mcp_resources.copy()

    def get_mcp_prompts(self) -> Dict[str, MCPPromptTemplate]:
        """Get all loaded MCP prompt templates.

        Returns:
            Dictionary of prompt templates by name
        """
        return self.mcp_prompts.copy()

    def enhance_system_prompt_with_mcp(self, base_prompt: str = "") -> str:
        """Enhance a system prompt with MCP information.

        Adds information about available MCP resources and operations to
        help the LLM understand what capabilities are available.

        Args:
            base_prompt: Base system prompt to enhance

        Returns:
            Enhanced system prompt including MCP resources and capabilities
        """
        if not self.mcp_config or not getattr(self.mcp_config, "enabled", False):
            return base_prompt

        enhancements = []

        # Add resource information
        if self.mcp_resources:
            resource_section = "\n## Available MCP Resources:\n"
            for resource in self.mcp_resources:
                resource_section += (
                    f"- {resource.name}: {resource.description} ({resource.uri})\n"
                )
            enhancements.append(resource_section)

        # Add MCP prompt information
        if self.mcp_prompts:
            prompt_section = "\n## Available MCP Operations:\n"
            for name, prompt in self.mcp_prompts.items():
                prompt_section += f"- {name}: {prompt.description}\n"
            enhancements.append(prompt_section)

        # Add MCP tool information
        if self._mcp_tools:
            tool_section = "\n## MCP Tools:\n"
            for tool in self._mcp_tools:
                tool_section += f"- {tool.name}: {tool.description}\n"
            enhancements.append(tool_section)

        if enhancements:
            return base_prompt + "\n" + "\n".join(enhancements)

        return base_prompt

    async def get_mcp_resource_content(self, uri: str) -> Any:
        """Fetch content for an MCP resource.

        Args:
            uri: Resource URI

        Returns:
            Resource content

        Raises:
            ValueError: If MCP manager not initialized or resource not found
        """
        if not self._mcp_manager:
            raise ValueError("MCP manager not initialized")

        # Find which server handles this resource
        for server_name, client in self._mcp_manager.clients.items():
            try:
                content = await client.read_resource(uri)

                # Update cached content
                for resource in self.mcp_resources:
                    if resource.uri == uri:
                        resource.content = content
                        break

                return content

            except Exception as e:
                logger.debug(f"Server {server_name} cannot handle resource {uri}: {e}")
                continue

        raise ValueError(f"No MCP server can handle resource: {uri}")

    async def call_mcp_prompt(
        self, prompt_name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Call an MCP prompt to get formatted messages.

        Args:
            prompt_name: Name of the prompt (can include server prefix)
            arguments: Arguments to pass to the prompt

        Returns:
            List of message dictionaries with role and content

        Raises:
            ValueError: If prompt not found or MCP not initialized
        """
        if not self._mcp_manager:
            raise ValueError("MCP manager not initialized")

        # Find the prompt
        if prompt_name not in self.mcp_prompts:
            # Try to find by suffix match
            matching = [k for k in self.mcp_prompts.keys() if k.endswith(prompt_name)]
            if not matching:
                raise ValueError(f"Prompt '{prompt_name}' not found")
            prompt_name = matching[0]

        # Extract server name from prompt name
        parts = prompt_name.split("_", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid prompt name format: {prompt_name}")

        server_name, actual_prompt_name = parts

        # Get the client
        if server_name not in self._mcp_manager.clients:
            raise ValueError(f"Server '{server_name}' not found")

        client = self._mcp_manager.clients[server_name]

        try:
            # Call the prompt
            result = await client.get_prompt(actual_prompt_name, arguments or {})

            # Convert to message format
            messages = []
            for msg in result.messages:
                messages.append({"role": msg.role, "content": msg.content})

            return messages

        except Exception as e:
            logger.error(f"Error calling prompt {prompt_name}: {e}")
            raise

    def cleanup_mcp(self) -> None:
        """Clean up MCP resources.

        This should be called when the configuration is no longer needed
        to properly close MCP connections.
        """
        if self._mcp_manager:
            try:
                # Synchronous cleanup if available
                if hasattr(self._mcp_manager, "cleanup"):
                    self._mcp_manager.cleanup()
                logger.info("MCP cleanup complete")
            except Exception as e:
                logger.error(f"Error during MCP cleanup: {e}")

        # Clear resources
        self._mcp_tools.clear()
        self.mcp_resources.clear()
        self.mcp_prompts.clear()
        self._mcp_manager = None
