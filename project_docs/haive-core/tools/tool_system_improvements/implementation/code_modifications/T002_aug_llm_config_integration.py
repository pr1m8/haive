"""T002 - AugLLMConfig Integration with Enhanced ToolRouteMixin
Updates to make AugLLMConfig use the enhanced tool management
Location: /haive-core/src/haive/core/engine/aug_llm/config.py.

Key changes:
1. Use enhanced ToolRouteMixin methods
2. Smart routing for structured output models
3. Better tool validation and conversion
"""
# The AugLLMConfig already inherits from ToolRouteMixin
# We need to override/enhance certain methods to use the new functionality
# Add this import
# Override the comprehensive_validation_and_setup method to use enhanced tool handling
from __future__ import annotations


def comprehensive_validation_and_setup(self):
    """Enhanced validation that uses improved tool management."""
    # ... existing validation code ...

    # After tools validation section, add:

    # Use enhanced tool analysis for all tools
    for tool in self.tools:
        # Add tool with enhanced metadata
        self.add_tool(tool)

    # Handle structured output model as a special tool
    if self.structured_output_model and self.structured_output_version == "v2":
        # Add structured output model as a tool with special routing
        self.add_tool(
            self.structured_output_model,
            route="structured_output_tool",
            metadata={
                "purpose": "structured_output",
                "version": self.structured_output_version,
                "force_use": True,
            },
        )

        # Set force tool choice to the model name
        self.force_tool_choice = self.structured_output_model.__name__
        self.force_tool_use = True

    # ... rest of validation ...


# Add method to get tools for LLM binding
def get_tools_for_binding(
        self) -> List[Union[BaseTool, Type[BaseModel], Callable]]:
    """Get tools in the format needed for LLM tool binding.

    Returns:
        List of tools ready for bind_tools()
    """
    binding_tools = []

    # Get all tools based on their routes
    for tool_name, route in self.tool_routes.items():
        tool = self.get_tool(tool_name)
        if not tool:
            continue

        # Include based on route and LLM compatibility
        if route in [
                "langchain_tool",
                "function",
                "pydantic_tool",
                "structured_output_tool",
        ]:
            binding_tools.append(tool)
        elif route == "pydantic_model":
            # Only include Pydantic models that are meant for tool use
            metadata = self.tool_metadata.get(tool_name, {})
            if metadata.get("is_executable") or metadata.get(
                    "purpose") == "structured_output":
                binding_tools.append(tool)

    return binding_tools


# Override create_runnable to use enhanced tool management
def create_runnable(self,
                    runnable_config: Optional[RunnableConfig] = None) -> Any:
    """Create a runnable with enhanced tool handling."""
    # ... existing code ...

    # When creating the chain with tools
    if self.tools or self.structured_output_model:
        # Get properly filtered tools for binding
        binding_tools = self.get_tools_for_binding()

        if binding_tools:
            # Bind tools with enhanced metadata
            llm.bind_tools(tools=binding_tools, **self.bind_tools_kwargs)

    # ... rest of chain creation ...


# Add method to handle Pydantic model routing based on context
def route_pydantic_model_for_llm(self, model: Type[BaseModel]) -> str:
    """Determine how to route a Pydantic model in LLM context.

    Args:
        model: Pydantic model to route

    Returns:
        Route string based on usage context
    """
    # Check if it's the structured output model
    if self.structured_output_model and model == self.structured_output_model:
        if self.structured_output_version == "v2":
            return "structured_output_tool"
        return "parser"

    # Check if model has __call__ (executable tool)
    if callable(model) and callable(model.__call__):
        return "pydantic_tool"

    # Check if it's in our tools list
    model_name = model.__name__
    if model_name in self.tool_instances:
        # Use the route we assigned when adding
        return self.tool_routes.get(model_name, "pydantic_model")

    # Default to parser for output parsing
    return "parser"


# Override _analyze_tool to use context-aware routing
def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Analyze tool with LLM-specific context awareness."""
    # Special handling for Pydantic models
    if isinstance(tool, type) and issubclass(tool, BaseModel):
        route = self.route_pydantic_model_for_llm(tool)
        metadata = {
            "class_name": tool.__name__,
            "module": getattr(tool, "__module__", "unknown"),
            "llm_route": route,
        }

        # Add structured output context if applicable
        if self.structured_output_model and tool == self.structured_output_model:
            metadata["is_structured_output"] = True
            metadata[
                "structured_output_version"] = self.structured_output_version

        return route, metadata

    # Use parent implementation for other tools
    return super()._analyze_tool(tool)


# Add helper to convert tools for different LLM providers
def prepare_tools_for_provider(self, provider: str = "openai") -> List[Any]:
    """Prepare tools in the format expected by specific LLM providers.

    Args:
        provider: LLM provider name (openai, anthropic, etc)

    Returns:
        List of tools formatted for the provider
    """
    prepared_tools = []

    for tool in self.get_tools_for_binding():
        if provider == "openai":
            # OpenAI expects tools in specific format
            if isinstance(tool, BaseTool | Tool | StructuredTool):
                # LangChain tools work directly
                prepared_tools.append(tool)
            elif isinstance(tool, type) and issubclass(tool, BaseModel):
                # Pydantic models need to be in tools format
                prepared_tools.append(tool)
            elif callable(tool):
                # Functions might need conversion
                # This would need actual conversion logic
                logger.debug(
                    f"Function {
                        getattr(
                            tool,
                            '__name__',
                            'unknown')} may need conversion",
                )

        # Add other provider-specific handling as needed

    return prepared_tools
