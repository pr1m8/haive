#!/usr/bin/env python3
"""Test enhanced ToolRouteMixin functionality.

Following [MEM-008] Testing Philosophy - Real components only, no mocks.
Memory Reference: [MEM-004-CORE-G-002] Enhanced Tool Management Session.
"""

from typing import Any, Dict, List

import pytest
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin


class SamplePydanticModel(BaseModel):
    """Regular Pydantic model for testing."""

    data: str = Field(description="Test data")


class SampleExecutableModel(BaseModel):
    """Pydantic model with explicit __call__ method."""

    query: str = Field(description="Query to process")

    def __call__(self) -> str:
        """Explicit __call__ makes this executable."""
        return f"Processed: {self.query}"


def sample_calculator(expression: str) -> str:
    """Sample function tool."""
    return f"Calculated: {expression}"


class SampleBaseTool(BaseTool):
    """Sample BaseTool for testing."""

    name: str = "sample_base_tool"
    description: str = "A sample base tool for testing"

    def _run(self, query: str) -> str:
        """Execute the tool."""
        return f"BaseTool processed: {query}"


def create_structured_tool() -> StructuredTool:
    """Create a sample StructuredTool for testing."""

    def _run_tool(query: str) -> str:
        """Execute the tool."""
        return f"StructuredTool processed: {query}"

    return StructuredTool.from_function(
        func=_run_tool,
        name="sample_structured_tool",
        description="A sample structured tool for testing",
    )


class SampleConfig(ToolRouteMixin, BaseModel):
    """Test configuration using enhanced ToolRouteMixin."""

    name: str


class TestEnhancedToolRouting:
    """Test suite for enhanced ToolRouteMixin functionality."""

    def test_tool_storage_and_routing(self):
        """Test that enhanced ToolRouteMixin stores tools and creates correct routes."""
        # Arrange
        tools = [SamplePydanticModel, SampleExecutableModel, sample_calculator]
        config = SampleConfig(name="test_routing", tools=tools)

        # Act - Process tools through enhanced routing
        for tool in tools:
            config.add_tool(tool)

        # Assert - Verify storage
        assert len(config.tools) == 3
        assert len(config.tool_instances) == 3
        assert len(config.tool_routes) == 3

        # Assert - Verify correct routing
        routes = config.tool_routes
        assert (
            routes.get("SamplePydanticModel") == "pydantic_model"
        )  # No explicit __call__
        assert (
            routes.get("SampleExecutableModel") == "pydantic_tool"
        )  # Has explicit __call__
        assert routes.get("sample_calculator") == "function"  # Function tool

    def test_tool_management_operations(self):
        """Test enhanced tool management methods."""
        # Arrange
        config = SampleConfig(name="test_management", tools=[])

        # Act & Assert - Add tool
        config.add_tool(sample_calculator)
        assert len(config.tools) == 1
        assert "sample_calculator" in config.tool_routes

        # Act & Assert - Get tool
        retrieved = config.get_tool("sample_calculator")
        assert retrieved == sample_calculator

        # Act & Assert - Get tools by route
        function_tools = config.get_tools_by_route("function")
        assert len(function_tools) == 1
        assert function_tools[0] == sample_calculator

        # Act & Assert - Clear tools
        config.clear_tools()
        assert len(config.tools) == 0
        assert len(config.tool_routes) == 0

    def test_explicit_call_detection(self):
        """Test that only explicit __call__ methods trigger pydantic_tool routing."""
        # Arrange
        config = SampleConfig(name="test_call_detection", tools=[])

        # Act - Analyze regular model (no explicit __call__)
        regular_route, regular_metadata = config._analyze_tool(SamplePydanticModel)

        # Act - Analyze executable model (explicit __call__)
        executable_route, executable_metadata = config._analyze_tool(
            SampleExecutableModel
        )

        # Assert - Verify routing differences
        assert regular_route == "pydantic_model"
        assert regular_metadata["is_executable"] == False

        assert executable_route == "pydantic_tool"
        assert executable_metadata["is_executable"] == True

    def test_enhanced_metadata_generation(self):
        """Test that enhanced metadata is generated for tools."""
        # Arrange
        config = SampleConfig(name="test_metadata", tools=[])
        config.add_tool(sample_calculator)

        # Act
        metadata = config.tool_metadata.get("sample_calculator")

        # Assert - Verify enhanced metadata exists
        assert metadata is not None
        assert "is_async" in metadata
        assert "parameter_count" in metadata
        assert "callable_kind" in metadata
        assert metadata["callable_kind"] == "function"

    def test_langchain_tool_routing(self):
        """Test that BaseTool and StructuredTool are routed correctly."""
        # Arrange
        config = SampleConfig(name="test_langchain", tools=[])
        base_tool = SampleBaseTool()
        structured_tool = create_structured_tool()

        # Act - Add tools
        config.add_tool(base_tool)
        config.add_tool(structured_tool)

        # Assert - Verify routing
        assert len(config.tools) == 2
        assert config.tool_routes.get("sample_base_tool") == "langchain_tool"
        assert config.tool_routes.get("sample_structured_tool") == "langchain_tool"

        # Assert - Verify tool instances
        assert config.get_tool("sample_base_tool") == base_tool
        assert config.get_tool("sample_structured_tool") == structured_tool

        # Assert - Verify tools by route
        langchain_tools = config.get_tools_by_route("langchain_tool")
        assert len(langchain_tools) == 2
        assert base_tool in langchain_tools
        assert structured_tool in langchain_tools
