"""Dynamic Activation MCP Server Implementation.

This module provides MCP (Model Context Protocol) integration for the Dynamic
Activation Pattern, allowing MCP servers to dynamically discover and activate
tools based on client requests.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- MCP protocol specification
- Existing haive-mcp infrastructure
"""

import uuid
from datetime import datetime
from typing import Any

from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent
from haive.core.registry import DynamicRegistry, RegistryItem
from haive.core.schema.prebuilt.dynamic_activation_state import DynamicActivationState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from pydantic import BaseModel, ConfigDict, Field, model_validator


class MCPTool(BaseModel):
    """MCP tool representation for dynamic activation.

    Represents a tool that can be activated and used via MCP protocol.

    Args:
        name: Tool name
        description: Tool description
        input_schema: JSON schema for tool input
        handler: Function to handle tool execution
        metadata: Additional metadata

    Examples:
        Create MCP tool::

            tool = MCPTool(
                name="calculator",
                description="Mathematical calculations",
                input_schema={"type": "object", "properties": {"expression": {"type": "string"}}},
                handler=calculator_handler
            )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    input_schema: dict[str, Any] = Field(..., description="JSON schema for tool input")
    handler: Any = Field(..., description="Function to handle tool execution")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class DynamicMCPRegistry(DynamicRegistry[MCPTool]):
    """MCP-specific registry for dynamic tool activation.

    Extends DynamicRegistry with MCP-specific functionality for tool
    registration and activation with MCP servers.

    Examples:
        Create MCP registry::

            registry = DynamicMCPRegistry()

            # Register MCP tool
            tool = MCPTool(
                name="search",
                description="Web search",
                input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
                handler=search_handler
            )
            item = RegistryItem(
                id="search_001",
                name="Web Search",
                description="Search the web",
                component=tool
            )
            registry.register(item)
    """

    async def activate_mcp_tool(
        self, tool_id: str, mcp_server: Any | None = None
    ) -> MCPTool | None:
        """Activate an MCP tool and register with server.

        Args:
            tool_id: ID of tool to activate
            mcp_server: MCP server to register with (optional)

        Returns:
            Activated MCPTool or None if activation failed

        Examples:
            Activate MCP tool::

                tool = await registry.activate_mcp_tool("search_001", server)
                if tool:
                    print(f"Activated: {tool.name}")
        """
        if self.activate(tool_id):
            item = self.items[tool_id]
            tool = item.component

            # Register with MCP server if provided
            if mcp_server and hasattr(mcp_server, "register_tool"):
                await mcp_server.register_tool(tool)

            return tool

        return None

    def get_tool_schemas(self) -> dict[str, dict[str, Any]]:
        """Get input schemas for all registered tools.

        Returns:
            Dictionary of tool name to input schema

        Examples:
            Get schemas for MCP registration::

                schemas = registry.get_tool_schemas()
                for tool_name, schema in schemas.items():
                    print(f"{tool_name}: {schema}")
        """
        schemas = {}

        for item in self.items.values():
            if isinstance(item.component, MCPTool):
                schemas[item.component.name] = item.component.input_schema

        return schemas


class DynamicMCPState(DynamicActivationState):
    """MCP-specific state for dynamic activation.

    Extends DynamicActivationState with MCP protocol specific fields
    and functionality for handling MCP client requests.

    Args:
        mcp_client_id: ID of connected MCP client
        mcp_session_id: Current MCP session ID
        mcp_protocol_version: MCP protocol version
        tool_call_history: History of MCP tool calls

    Examples:
        Create MCP state::

            state = DynamicMCPState(
                mcp_client_id="client_123",
                mcp_session_id="session_456",
                mcp_protocol_version="1.0"
            )

            # Track tool calls
            state.tool_call_history.append({
                "tool": "calculator",
                "input": {"expression": "2 + 2"},
                "timestamp": "2025-01-15T10:30:00"
            })
    """

    # MCP-specific fields
    mcp_client_id: str | None = Field(
        default=None, description="ID of connected MCP client"
    )

    mcp_session_id: str | None = Field(
        default=None, description="Current MCP session ID"
    )

    mcp_protocol_version: str = Field(default="1.0", description="MCP protocol version")

    tool_call_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of MCP tool calls"
    )

    def track_tool_call(
        self, tool_name: str, input_data: dict[str, Any], result: Any
    ) -> None:
        """Track an MCP tool call.

        Args:
            tool_name: Name of tool called
            input_data: Input data for tool
            result: Result from tool execution

        Examples:
            Track tool call::

                state.track_tool_call(
                    tool_name="calculator",
                    input_data={"expression": "2 + 2"},
                    result=4
                )
        """
        self.tool_call_history.append(
            {
                "tool": tool_name,
                "input": input_data,
                "result": str(result),
                "timestamp": str(datetime.now()),
                "client_id": self.mcp_client_id,
                "session_id": self.mcp_session_id,
            }
        )


class DynamicActivationMCPServer(BaseModel):
    """MCP server with dynamic tool activation capabilities.

    This server implements the MCP protocol with dynamic tool discovery
    and activation. It can discover tools from documentation and activate
    them based on client requests.

    Key Features:
        - Dynamic tool discovery from documentation
        - Tool activation on demand
        - MCP protocol compliance
        - MetaStateSchema integration for tracking
        - Session management

    Args:
        name: Server name
        discovery_source: Source for tool discovery
        tool_registry: Registry for managing tools
        discovery_config: Configuration for discovery
        meta_state: MetaStateSchema for tracking
        state: DynamicMCPState for session management

    Examples:
        Create MCP server::

            server = DynamicActivationMCPServer(
                name="dynamic_mcp_server",
                discovery_source="@haive-tools"
            )

            # Start server
            await server.start()

            # Handle client requests
            result = await server.handle_tool_request({
                "tool": "calculator",
                "input": {"expression": "2 + 2"}
            })

        With custom discovery::

            server = DynamicActivationMCPServer(
                name="custom_mcp_server",
                discovery_source="/path/to/tools",
                discovery_config={
                    "auto_discover": True,
                    "max_tools": 50,
                    "cache_ttl": 3600
                }
            )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    # Core configuration
    name: str = Field(..., description="Server name")
    discovery_source: str = Field(..., description="Source for tool discovery")

    # Components
    tool_registry: DynamicMCPRegistry = Field(
        default_factory=DynamicMCPRegistry, description="Registry for managing tools"
    )

    discovery_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for discovery"
    )

    meta_state: MetaStateSchema | None = Field(
        default=None, description="MetaStateSchema for tracking"
    )

    state: DynamicMCPState = Field(
        default_factory=DynamicMCPState, description="MCP state for session management"
    )

    # Private attributes
    _discovery_agent: ComponentDiscoveryAgent | None = None
    _is_running: bool = False
    _clients: dict[str, Any] = {}

    @model_validator(mode="after")
    @classmethod
    def setup_mcp_server(cls) -> "DynamicActivationMCPServer":
        """Initialize MCP server components.

        This validator:
        1. Sets up discovery configuration
        2. Initializes discovery agent
        3. Wraps in MetaStateSchema
        4. Configures MCP protocol settings
        """
        # Set up discovery configuration
        if not self.discovery_config:
            self.discovery_config = {
                "source": self.discovery_source,
                "auto_discover": True,
                "max_tools": 100,
                "cache_ttl": 3600,
            }

        # Initialize discovery agent
        try:
            self._discovery_agent = ComponentDiscoveryAgent(
                document_path=self.discovery_source
            )
        except Exception:
            # Fallback: no discovery agent
            self._discovery_agent = None

        # Wrap in MetaStateSchema for tracking
        self.meta_state = MetaStateSchema(
            agent=self,  # MCP server as "agent"
            agent_state={
                "mcp_mode": True,
                "protocol_version": self.state.mcp_protocol_version,
            },
            graph_context={
                "protocol": "mcp",
                "server_name": self.name,
                "discovery_enabled": self._discovery_agent is not None,
            },
        )

        return self

    async def start(self) -> None:
        """Start the MCP server.

        Examples:
            Start server::

                await server.start()
                print("MCP server started")
        """
        if self._is_running:
            return

        # Pre-discover tools if auto-discovery is enabled
        if self.discovery_config.get("auto_discover", False) and self._discovery_agent:
            await self._prediscover_tools()

        self._is_running = True

        # Track server start
        if self.meta_state:
            self.meta_state.execution_status = "running"

    async def stop(self) -> None:
        """Stop the MCP server.

        Examples:
            Stop server::

                await server.stop()
                print("MCP server stopped")
        """
        self._is_running = False
        self._clients.clear()

        # Track server stop
        if self.meta_state:
            self.meta_state.execution_status = "stopped"

    async def handle_tool_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle dynamic tool requests from MCP clients.

        Args:
            request: MCP tool request

        Returns:
            Tool execution result

        Examples:
            Handle tool request::

                request = {
                    "tool": "calculator",
                    "input": {"expression": "2 + 2"},
                    "client_id": "client_123"
                }

                result = await server.handle_tool_request(request)
                print(f"Result: {result}")
        """
        tool_name = request.get("tool")
        input_data = request.get("input", {})
        client_id = request.get("client_id")

        if not tool_name:
            return {"error": "Tool name is required"}

        # Update client info
        if client_id:
            self._clients[client_id] = request
            self.state.mcp_client_id = client_id

        try:
            # Check if tool is active
            tool = self._get_active_tool(tool_name)

            if not tool:
                # Try to discover and activate tool
                discovered = await self._discover_and_activate_tool(tool_name)
                if discovered:
                    tool = discovered
                else:
                    return {
                        "error": f"Tool '{tool_name}' not found and could not be discovered"
                    }

            # Execute tool through meta state for tracking
            result = await self.meta_state.execute_agent(
                input_data={
                    "tool_name": tool_name,
                    "tool_input": input_data,
                    "mcp_request": request,
                },
                update_state=True,
            )

            # Track tool call
            self.state.track_tool_call(tool_name, input_data, result)

            return {"result": result.get("output", ""), "success": True}

        except Exception as e:
            error_msg = f"Tool execution failed: {e!s}"

            # Track failed tool call
            self.state.track_tool_call(tool_name, input_data, {"error": error_msg})

            return {"error": error_msg, "success": False}

    async def _prediscover_tools(self) -> None:
        """Pre-discover tools during server startup.

        This method runs tool discovery during server initialization
        to populate the tool registry with available tools.
        """
        if not self._discovery_agent:
            return

        try:
            # Discover general tools
            tools = await self._discovery_agent.discover_components("available tools")

            # Register discovered tools
            for tool_data in tools:
                await self._register_tool_from_data(tool_data)

        except Exception:
            # Continue without pre-discovery
            pass

    async def _discover_and_activate_tool(self, tool_name: str) -> MCPTool | None:
        """Discover and activate a tool by name.

        Args:
            tool_name: Name of tool to discover and activate

        Returns:
            Activated MCPTool or None if not found
        """
        if not self._discovery_agent:
            return None

        try:
            # Search for specific tool
            query = f"tool named {tool_name}"
            tools = await self._discovery_agent.discover_components(query)

            # Find matching tool
            for tool_data in tools:
                if tool_data.get("name", "").lower() == tool_name.lower():
                    return await self._register_and_activate_tool(tool_data)

            return None

        except Exception:
            return None

    async def _register_and_activate_tool(
        self, tool_data: dict[str, Any]
    ) -> MCPTool | None:
        """Register and activate a tool from discovery data.

        Args:
            tool_data: Tool data from discovery

        Returns:
            Activated MCPTool or None if registration failed
        """
        try:
            # Create MCP tool from data
            mcp_tool = MCPTool(
                name=tool_data.get("name", "unknown"),
                description=tool_data.get("description", ""),
                input_schema=tool_data.get("input_schema", {"type": "object"}),
                handler=self._create_tool_handler(tool_data),
                metadata=tool_data.get("metadata", {}),
            )

            # Register in registry
            item = RegistryItem(
                id=tool_data.get("id", tool_data.get("name", "unknown")),
                name=tool_data.get("name", "Unknown Tool"),
                description=tool_data.get("description", ""),
                component=mcp_tool,
            )

            self.tool_registry.register(item)

            # Activate tool
            return await self.tool_registry.activate_mcp_tool(item.id, self)

        except Exception:
            return None

    async def _register_tool_from_data(self, tool_data: dict[str, Any]) -> None:
        """Register a tool from discovery data without activation.

        Args:
            tool_data: Tool data from discovery
        """
        try:
            await self._register_and_activate_tool(tool_data)
        except Exception:
            # Continue with other tools
            pass

    def _create_tool_handler(self, tool_data: dict[str, Any]) -> Any:
        """Create a tool handler function from tool data.

        Args:
            tool_data: Tool data from discovery

        Returns:
            Tool handler function
        """

        async def tool_handler(input_data: dict[str, Any]) -> Any:
            """Handle tool execution."""
            # This is a placeholder - in a real implementation,
            # this would load and execute the actual tool
            return (
                f"Executed {tool_data.get('name', 'unknown')} with input: {input_data}"
            )

        return tool_handler

    def _get_active_tool(self, tool_name: str) -> MCPTool | None:
        """Get an active tool by name.

        Args:
            tool_name: Name of tool to get

        Returns:
            Active MCPTool or None if not found
        """
        active_items = self.tool_registry.get_active_items()

        for item in active_items:
            if isinstance(item.component, MCPTool) and item.component.name == tool_name:
                return item.component

        return None

    def get_available_tools(self) -> list[dict[str, Any]]:
        """Get list of available tools for MCP clients.

        Returns:
            List of tool descriptions for MCP protocol

        Examples:
            Get tools for MCP registration::

                tools = server.get_available_tools()
                for tool in tools:
                    print(f"{tool['name']}: {tool['description']}")
        """
        tools = []

        for item in self.tool_registry.items.values():
            if isinstance(item.component, MCPTool):
                tools.append(
                    {
                        "name": item.component.name,
                        "description": item.component.description,
                        "input_schema": item.component.input_schema,
                        "active": item.is_active,
                    }
                )

        return tools

    def get_server_stats(self) -> dict[str, Any]:
        """Get server statistics.

        Returns:
            Dictionary with server statistics

        Examples:
            Get server status::

                stats = server.get_server_stats()
                print(f"Tools: {stats['total_tools']}")
                print(f"Active: {stats['active_tools']}")
                print(f"Clients: {stats['connected_clients']}")
        """
        registry_stats = self.tool_registry.get_stats()

        return {
            **registry_stats,
            "server_name": self.name,
            "is_running": self._is_running,
            "connected_clients": len(self._clients),
            "protocol_version": self.state.mcp_protocol_version,
            "tool_calls": len(self.state.tool_call_history),
            "discovery_enabled": self._discovery_agent is not None,
        }

    async def handle_client_connect(
        self, client_id: str, client_info: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle MCP client connection.

        Args:
            client_id: ID of connecting client
            client_info: Client information

        Returns:
            Connection response

        Examples:
            Handle client connection::

                response = await server.handle_client_connect("client_123", {
                    "name": "My Client",
                    "version": "1.0"
                })
        """
        # Store client info
        self._clients[client_id] = client_info

        # Update state
        self.state.mcp_client_id = client_id

        # Generate session ID

        session_id = str(uuid.uuid4())
        self.state.mcp_session_id = session_id

        return {
            "status": "connected",
            "session_id": session_id,
            "server_name": self.name,
            "protocol_version": self.state.mcp_protocol_version,
            "available_tools": self.get_available_tools(),
        }

    async def handle_client_disconnect(self, client_id: str) -> None:
        """Handle MCP client disconnection.

        Args:
            client_id: ID of disconnecting client

        Examples:
            Handle client disconnect::

                await server.handle_client_disconnect("client_123")
        """
        if client_id in self._clients:
            del self._clients[client_id]

        # Clear state if this was the current client
        if self.state.mcp_client_id == client_id:
            self.state.mcp_client_id = None
            self.state.mcp_session_id = None
