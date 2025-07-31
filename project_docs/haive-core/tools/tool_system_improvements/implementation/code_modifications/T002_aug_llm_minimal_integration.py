"""T002 - Minimal AugLLMConfig Integration with ToolRouteMixin
A practical approach that works with existing AugLLMConfig structure
Location: /haive-core/src/haive/core/engine/aug_llm/config.py.

This approach:
1. Keeps existing AugLLMConfig tool handling
2. Adds routing sync to leverage ToolRouteMixin
3. Minimal breaking changes
"""

# Add this method to AugLLMConfig class:


def _sync_tools_with_routes(self):
    """Sync processed tools with ToolRouteMixin routing system.

    This runs after _process_tools() to add routing metadata.
    """
    debug_print("🔄 [blue]Syncing tools with routing system...[/blue]")

    # Clear existing routes to avoid stale data
    self.tool_routes.clear()
    self.tool_metadata.clear()

    # Process each tool through the routing system
    for tool in self.tools:
        # Get tool name (use existing logic)
        tool_name = None
        if hasattr(tool, "name"):
            tool_name = tool.name
        elif hasattr(tool, "__name__"):
            tool_name = tool.__name__
        else:
            tool_name = str(tool)

        # Analyze tool for routing
        route, metadata = self._analyze_tool(tool)

        # Add AugLLM-specific metadata
        metadata = metadata or {}
        metadata["source"] = "aug_llm_config"

        # Check if it's the structured output model
        if self.structured_output_model and tool == self.structured_output_model:
            route = (
                "structured_output_tool"
                if self.structured_output_version == "v2"
                else "parser"
            )
            metadata["is_structured_output"] = True
            metadata["structured_output_version"] = self.structured_output_version

        # Set the route
        self.tool_routes[tool_name] = route
        self.tool_metadata[tool_name] = metadata

    debug_print(f"✅ [green]Synced {len(self.tool_routes)} tools with routes[/green]")


# Override _analyze_tool to handle AugLLM-specific cases:


def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Analyze tool with AugLLM-specific logic.

    Extends ToolRouteMixin's analysis with structured output awareness.
    """
    # Check if this is structured output model first
    if self.structured_output_model and tool == self.structured_output_model:
        # Route based on version
        route = (
            "structured_output_tool"
            if self.structured_output_version == "v2"
            else "parser"
        )

        metadata = {
            "class_name": tool.__name__ if hasattr(tool, "__name__") else str(tool),
            "purpose": "structured_output",
            "version": self.structured_output_version,
        }
        return route, metadata

    # For Pydantic models, check if they're in pydantic_tools
    if isinstance(tool, type) and issubclass(tool, BaseModel):
        # Check if it's being used as a tool or parser
        if tool in self.pydantic_tools:
            route = "pydantic_tool"
            metadata = {
                "class_name": tool.__name__,
                "in_pydantic_tools": True,
                "likely_use": "tool",
            }
        else:
            route = "pydantic_model"
            metadata = {
                "class_name": tool.__name__,
                "in_pydantic_tools": False,
                "likely_use": "parser",
            }
        return route, metadata

    # Fall back to parent implementation
    return super()._analyze_tool(tool)


# Update comprehensive_validation_and_setup to call sync:


def comprehensive_validation_and_setup(self):
    """Enhanced validation that syncs with routing system."""
    # ... existing validation code ...

    # After _process_tools() is called:
    self._process_tools()

    # NEW: Sync with routing system
    self._sync_tools_with_routes()

    # ... rest of validation ...


# Add helper method to get tools by their route:


def get_tools_for_binding(self) -> List[Any]:
    """Get tools filtered by route for LLM binding.

    Uses routing information to select appropriate tools.
    """
    binding_tools = []

    for tool in self.tools:
        tool_name = getattr(tool, "name", getattr(tool, "__name__", str(tool)))
        route = self.tool_routes.get(tool_name)

        # Include tools based on their route
        if route in [
            "langchain_tool",
            "function",
            "pydantic_tool",
            "structured_output_tool",
        ]:
            binding_tools.append(tool)
        elif route == "pydantic_model":
            # Only include if it's meant for tool use
            metadata = self.tool_metadata.get(tool_name, {})
            if metadata.get("in_pydantic_tools") or metadata.get(
                "is_structured_output"
            ):
                binding_tools.append(tool)

    return binding_tools


# Add method to check tool capabilities:


def has_tool_capability(self, capability: str) -> bool:
    """Check if any tools have a specific capability.

    Args:
        capability: Capability to check (e.g., "is_async", "is_structured_output")

    Returns:
        True if any tool has this capability
    """
    return any(metadata.get(capability) for metadata in self.tool_metadata.values())


# Update create_runnable to use routing:


def create_runnable(self, runnable_config: Optional[RunnableConfig] = None) -> Any:
    """Create runnable with route-aware tool binding."""
    # ... existing code ...

    # When binding tools, use filtered list
    if self.tools:
        # Get tools appropriate for binding
        binding_tools = self.get_tools_for_binding()

        if binding_tools:
            # Log what we're binding
            debug_print(
                f"🔗 [cyan]Binding {len(binding_tools)} tools (filtered from {len(self.tools)})[/cyan]"
            )

            # Check tool routes for insights
            tool_routes = [
                self.tool_routes.get(getattr(t, "name", str(t)), "unknown")
                for t in binding_tools
            ]
            debug_print(f"📊 [dim]Tool routes: {Counter(tool_routes)}[/dim]")

            llm.bind_tools(tools=binding_tools, **self.bind_tools_kwargs)

    # ... rest of chain creation ...
