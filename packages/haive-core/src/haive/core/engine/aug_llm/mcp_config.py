"""MCP-enhanced AugLLMConfig with full type checking.

This module provides MCPAugLLMConfig, which extends AugLLMConfig with Model Context
Protocol (MCP) support through proper mixin composition. It includes full type
checking and seamless integration with the existing Haive configuration system.

The configuration automatically discovers MCP tools, manages resources, and enhances
prompts while maintaining compatibility with all existing AugLLMConfig features.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import Field, model_validator

from haive.core.common.mixins import MCPMixin, ToolRouteMixin
from haive.core.engine.aug_llm.config import AugLLMConfig

if TYPE_CHECKING:
    from haive.mcp.config import MCPConfig

import logging

logger = logging.getLogger(__name__)


class MCPAugLLMConfig(MCPMixin, AugLLMConfig):
    """AugLLMConfig enhanced with MCP (Model Context Protocol) support.

    This configuration class extends AugLLMConfig with MCP capabilities through
    the MCPMixin, providing:
    - Automatic MCP tool discovery and integration
    - Resource management from MCP servers
    - Prompt template enhancement
    - Full type safety with MCP configurations

    The class properly integrates with ToolRouteMixin (inherited from AugLLMConfig)
    to ensure MCP tools are correctly routed and managed alongside regular tools.

    Attributes:
        All attributes from AugLLMConfig plus:
        - mcp_config: Optional MCP configuration
        - mcp_resources: List of discovered MCP resources
        - mcp_prompts: Dictionary of MCP prompt templates
        - auto_discover_mcp_tools: Whether to auto-discover tools
        - inject_mcp_resources: Whether to inject resources
        - use_mcp_prompts: Whether to use MCP prompts

    Example:
        Basic usage with MCP server::

            from haive.mcp.config import MCPConfig, MCPServerConfig

            config = MCPAugLLMConfig(
                name="mcp_agent",
                llm_config=LLMConfig(provider="openai", model="gpt-4"),
                mcp_config=MCPConfig(
                    enabled=True,
                    servers={
                        "filesystem": MCPServerConfig(
                            transport="stdio",
                            command="npx",
                            args=["-y", "@modelcontextprotocol/server-filesystem"]
                        )
                    }
                ),
                system_message="AI assistant with filesystem access"
            )

            # Initialize MCP
            await config.setup()

            # MCP tools are now available alongside regular tools
            print(f"Total tools: {len(config.tools)}")
            print(f"MCP tools: {len(config.get_mcp_tools())}")

        Multiple MCP servers::

            config = MCPAugLLMConfig(
                name="multi_mcp_agent",
                llm_config={"provider": "openai", "model": "gpt-4"},
                mcp_config=MCPConfig(
                    enabled=True,
                    servers={
                        "filesystem": MCPServerConfig(...),
                        "github": MCPServerConfig(...),
                        "postgres": MCPServerConfig(...)
                    }
                ),
                tools=["calculator"],  # Regular tools work too
                auto_discover_mcp_tools=True
            )
    """

    # Override mcp_config to ensure proper typing
    mcp_config: Optional["MCPConfig"] = Field(
        None, description="MCP configuration for server connections"
    )

    @model_validator(mode="after")
    def _validate_mcp_integration(self) -> "MCPAugLLMConfig":
        """Validate MCP integration with AugLLMConfig.

        Ensures that MCP configuration is compatible with the base
        AugLLMConfig settings and tool management.
        """
        # If MCP is enabled and we have tool conflicts, log warning
        if self.mcp_config and self.mcp_config.enabled:
            if self.force_tool_use and not self.tools:
                logger.warning(
                    "force_tool_use is True but no tools specified. "
                    "MCP tools will be discovered during setup."
                )

        return self

    async def setup(self) -> None:
        """Initialize both AugLLMConfig and MCP integration.

        This method:
        1. Sets up MCP servers and discovers tools/resources/prompts
        2. Enhances the system message with MCP information
        3. Integrates MCP tools with the existing tool routing system

        Should be called after creating the configuration but before
        using it with an agent.
        """
        # Initialize MCP first
        await self.setup_mcp()

        # Enhance system message if MCP is enabled
        if self.mcp_config and self.mcp_config.enabled and self.system_message:
            enhanced_message = self.enhance_system_prompt_with_mcp(self.system_message)
            self.system_message = enhanced_message
            logger.debug("Enhanced system message with MCP information")

        # Update tool lists with MCP tools
        self._integrate_mcp_tools()

        logger.info(
            f"MCPAugLLMConfig setup complete: "
            f"{len(self.get_mcp_tools())} MCP tools, "
            f"{len(self.mcp_resources)} resources, "
            f"{len(self.mcp_prompts)} prompts"
        )

    def _integrate_mcp_tools(self) -> None:
        """Integrate discovered MCP tools with AugLLMConfig tool system.

        This ensures MCP tools are properly registered in:
        - The tools list (for compatibility)
        - The tool_routes mapping (via ToolRouteMixin)
        - The tool_instances mapping (for quick lookup)
        """
        mcp_tools = self.get_mcp_tools()
        if not mcp_tools:
            return

        # Add MCP tool names to the tools list
        mcp_tool_names = [tool.name for tool in mcp_tools]

        # Ensure tools list exists
        if not self.tools:
            self.tools = []

        # Add MCP tools that aren't already in the list
        for name in mcp_tool_names:
            if name not in self.tools:
                self.tools.append(name)

        logger.debug(f"Integrated {len(mcp_tool_names)} MCP tools into configuration")

    def get_all_tools(self) -> list[str]:
        """Get all available tool names including MCP tools.

        Returns:
            Combined list of regular tools and MCP tool names
        """
        all_tools = list(self.tools) if self.tools else []

        # Add MCP tools
        for tool in self.get_mcp_tools():
            if tool.name not in all_tools:
                all_tools.append(tool.name)

        return all_tools

    def get_tool_by_name(self, name: str) -> Any | None:
        """Get a tool instance by name, checking both regular and MCP tools.

        Args:
            name: Tool name to retrieve

        Returns:
            Tool instance or None if not found
        """
        # First check ToolRouteMixin's tool instances
        tool = self.get_tool(name)
        if tool:
            return tool

        # Then check MCP tools
        for mcp_tool in self.get_mcp_tools():
            if mcp_tool.name == name:
                return mcp_tool

        return None

    def debug_mcp_state(self) -> None:
        """Print debug information about MCP integration state.

        Useful for troubleshooting MCP configuration and tool discovery.
        """
        from rich.console import Console
        from rich.table import Table

        console = Console()

        # MCP Configuration Status
        if self.mcp_config:
            status_table = Table(title="MCP Configuration Status")
            status_table.add_column("Setting", style="cyan")
            status_table.add_column("Value", style="green")

            status_table.add_row("Enabled", str(self.mcp_config.enabled))
            status_table.add_row("Auto Discover", str(self.mcp_config.auto_discover))
            status_table.add_row("Servers", str(len(self.mcp_config.servers)))
            status_table.add_row("Tools Discovered", str(len(self.get_mcp_tools())))
            status_table.add_row("Resources Loaded", str(len(self.mcp_resources)))
            status_table.add_row("Prompts Available", str(len(self.mcp_prompts)))

            console.print(status_table)

        # MCP Servers
        if self.mcp_config and self.mcp_config.servers:
            server_table = Table(title="MCP Servers")
            server_table.add_column("Server", style="cyan")
            server_table.add_column("Transport", style="yellow")
            server_table.add_column("Status", style="green")

            for name, server in self.mcp_config.servers.items():
                status = "Enabled" if server.enabled else "Disabled"
                server_table.add_row(name, server.transport.value, status)

            console.print(server_table)

        # MCP Tools
        mcp_tools = self.get_mcp_tools()
        if mcp_tools:
            tool_table = Table(title="MCP Tools")
            tool_table.add_column("Tool Name", style="cyan")
            tool_table.add_column("Server", style="yellow")
            tool_table.add_column("Route", style="green")

            for tool in mcp_tools:
                # Extract server name from tool name
                server = tool.name.split("_")[0] if "_" in tool.name else "unknown"
                route = self.get_tool_route(tool.name) or "mcp_tool"
                tool_table.add_row(tool.name, server, route)

            console.print(tool_table)

        # Call parent debug method for tool routes
        if hasattr(super(), "debug_tool_routes"):
            super().debug_tool_routes()

    def cleanup(self) -> None:
        """Clean up resources including MCP connections.

        Should be called when the configuration is no longer needed.
        """
        self.cleanup_mcp()
        logger.info("MCPAugLLMConfig cleanup complete")


# Factory function for convenience
async def create_mcp_aug_llm_config(
    name: str,
    model: str = "gpt-4",
    mcp_servers: dict[str, Any] | None = None,
    **kwargs,
) -> MCPAugLLMConfig:
    """Factory function to create and initialize MCPAugLLMConfig.

    Args:
        name: Configuration name
        model: LLM model to use
        mcp_servers: Dictionary of MCP server configurations
        **kwargs: Additional arguments for MCPAugLLMConfig

    Returns:
        Initialized MCPAugLLMConfig instance

    Example:
        Creating a configuration with factory::

            config = await create_mcp_aug_llm_config(
                name="assistant",
                model="gpt-4",
                mcp_servers={
                    "filesystem": {
                        "transport": "stdio",
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"]
                    }
                },
                system_message="Helpful AI assistant",
                temperature=0.7
            )
    """
    # Lazy import to avoid circular dependencies
    from haive.mcp.config import MCPConfig, MCPServerConfig

    # Create MCP config if servers provided
    mcp_config = None
    if mcp_servers:
        servers = {}
        for server_name, server_config in mcp_servers.items():
            if isinstance(server_config, dict):
                servers[server_name] = MCPServerConfig(
                    name=server_name, **server_config
                )
            else:
                servers[server_name] = server_config

        mcp_config = MCPConfig(enabled=True, servers=servers)

    # Create config
    config = MCPAugLLMConfig(
        name=name,
        llm_config={"provider": "openai", "model": model},
        mcp_config=mcp_config,
        **kwargs,
    )

    # Initialize
    await config.setup()

    return config
