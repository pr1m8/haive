"""Dynamic Activation MCP Server Example.

This example demonstrates the MCP (Model Context Protocol) integration
with the Dynamic Activation Pattern using real components.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- MCP protocol specification
- Real component integration (no mocks)

Usage:
    poetry run python examples/dynamic_activation_mcp_example.py
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any

from haive.core.registry import RegistryItem

from haive.mcp.dynamic_activation_mcp import (
    DynamicActivationMCPServer,
    MCPTool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_1_basic_mcp_server():
    """Example 1: Basic MCP server with dynamic tool activation."""
    logger.info("=== Example 1: Basic MCP Server ===")

    # Create MCP server
    server = DynamicActivationMCPServer(
        name="basic_mcp_server",
        discovery_source="@haive-tools",  # Use Haive tools for discovery
        discovery_config={"auto_discover": True, "max_tools": 20, "cache_ttl": 1800},
    )

    logger.info(f"Created MCP server: {server.name}")

    # Create MCP tools
    async def calculator_handler(input_data: dict[str, Any]) -> float:
        """Calculator tool handler."""
        try:
            expression = input_data.get("expression", "")
            result = eval(expression)
            return float(result)
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return 0.0

    async def text_processor_handler(input_data: dict[str, Any]) -> str:
        """Text processor tool handler."""
        try:
            text = input_data.get("text", "")
            operation = input_data.get("operation", "uppercase")

            if operation == "uppercase":
                return text.upper()
            if operation == "lowercase":
                return text.lower()
            if operation == "reverse":
                return text[::-1]
            return text
        except Exception as e:
            logger.error(f"Text processor error: {e}")
            return str(input_data)

    async def data_formatter_handler(input_data: dict[str, Any]) -> str:
        """Data formatter tool handler."""
        try:
            data = input_data.get("data", {})
            format_type = input_data.get("format", "json")

            if format_type == "json":
                return json.dumps(data, indent=2)
            if format_type == "pretty":
                return "\n".join(f"{k}: {v}" for k, v in data.items())
            return str(data)
        except Exception as e:
            logger.error(f"Data formatter error: {e}")
            return str(input_data)

    # Create MCP tools
    mcp_tools = [
        MCPTool(
            name="calculator",
            description="Perform mathematical calculations",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate",
                    }
                },
                "required": ["expression"],
            },
            handler=calculator_handler,
            metadata={"category": "math", "version": "1.0"},
        ),
        MCPTool(
            name="text_processor",
            description="Process text with various operations",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to process"},
                    "operation": {
                        "type": "string",
                        "enum": ["uppercase", "lowercase", "reverse"],
                        "description": "Operation to perform",
                    },
                },
                "required": ["text"],
            },
            handler=text_processor_handler,
            metadata={"category": "text", "version": "1.0"},
        ),
        MCPTool(
            name="data_formatter",
            description="Format data in various output formats",
            input_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Data to format"},
                    "format": {
                        "type": "string",
                        "enum": ["json", "pretty"],
                        "description": "Output format",
                    },
                },
                "required": ["data"],
            },
            handler=data_formatter_handler,
            metadata={"category": "formatting", "version": "1.0"},
        ),
    ]

    # Register MCP tools
    for i, tool in enumerate(mcp_tools):
        item = RegistryItem(
            id=f"mcp_tool_{i:03d}",
            name=tool.name.title(),
            description=tool.description,
            component=tool,
            metadata=tool.metadata,
        )
        server.tool_registry.register(item)

    logger.info(f"Registered {len(mcp_tools)} MCP tools")

    # Start MCP server
    await server.start()
    logger.info("MCP server started")

    # Get available tools
    available_tools = server.get_available_tools()
    logger.info(f"Available tools: {[tool['name'] for tool in available_tools]}")

    # Simulate client connection
    client_info = {
        "name": "Basic Test Client",
        "version": "1.0",
        "capabilities": ["tools"],
    }

    connection_response = await server.handle_client_connect(
        "basic_client", client_info
    )
    logger.info(f"Client connected: {connection_response['status']}")
    logger.info(f"Session ID: {connection_response['session_id']}")

    # Activate tools
    for i in range(len(mcp_tools)):
        tool = await server.tool_registry.activate_mcp_tool(f"mcp_tool_{i:03d}")
        logger.info(f"Activated tool: {tool.name if tool else 'None'}")

    # Execute tool requests
    test_requests = [
        {
            "tool": "calculator",
            "input": {"expression": "10 + 5 * 2"},
            "client_id": "basic_client",
        },
        {
            "tool": "text_processor",
            "input": {"text": "Hello World", "operation": "uppercase"},
            "client_id": "basic_client",
        },
        {
            "tool": "data_formatter",
            "input": {
                "data": {"name": "John", "age": 30, "city": "New York"},
                "format": "json",
            },
            "client_id": "basic_client",
        },
    ]

    logger.info("Executing tool requests...")
    for request in test_requests:
        response = await server.handle_tool_request(request)
        logger.info(f"Tool '{request['tool']}' result: {response}")

    # Get server statistics
    stats = server.get_server_stats()
    logger.info(f"Server statistics: {stats}")

    # Disconnect client and stop server
    await server.handle_client_disconnect("basic_client")
    await server.stop()
    logger.info("MCP server stopped")

    return server


async def example_2_discovery_based_mcp():
    """Example 2: MCP server with discovery-based tool loading."""
    logger.info("=== Example 2: Discovery-based MCP Server ===")

    # Create comprehensive tool documentation
    import os
    import tempfile

    discovery_doc = """
    # MCP Discovery Tools Documentation
    
    ## Mathematical Tools
    
    ### Advanced Calculator
    - **Name**: advanced_calculator
    - **Description**: Advanced mathematical operations
    - **Input**: Complex expressions, functions, equations
    - **Output**: Precise numerical results
    - **Capabilities**: basic_math, trigonometry, calculus, statistics
    
    ### Statistics Engine
    - **Name**: statistics_engine
    - **Description**: Statistical analysis and computations
    - **Input**: Data arrays, statistical operations
    - **Output**: Statistical results and visualizations
    - **Capabilities**: descriptive, inferential, regression, correlation
    
    ## Text Processing Tools
    
    ### Natural Language Processor
    - **Name**: nlp_processor
    - **Description**: Advanced natural language processing
    - **Input**: Text documents, language processing tasks
    - **Output**: Processed text with annotations
    - **Capabilities**: tokenization, sentiment, entities, summarization
    
    ### Content Analyzer
    - **Name**: content_analyzer
    - **Description**: Content analysis and insights
    - **Input**: Text content, analysis parameters
    - **Output**: Content insights and metrics
    - **Capabilities**: readability, keywords, themes, quality
    
    ## Data Processing Tools
    
    ### Data Transformer
    - **Name**: data_transformer
    - **Description**: Transform data between formats
    - **Input**: Source data, transformation rules
    - **Output**: Transformed data in target format
    - **Capabilities**: csv, json, xml, yaml, sql
    
    ### Schema Validator
    - **Name**: schema_validator
    - **Description**: Validate data against schemas
    - **Input**: Data objects, schema definitions
    - **Output**: Validation results and error reports
    - **Capabilities**: json_schema, xml_schema, custom_rules
    
    ## Workflow Tools
    
    ### Task Orchestrator
    - **Name**: task_orchestrator
    - **Description**: Orchestrate complex task workflows
    - **Input**: Task definitions, dependencies, parameters
    - **Output**: Workflow execution results
    - **Capabilities**: sequential, parallel, conditional, loops
    
    ### Event Processor
    - **Name**: event_processor
    - **Description**: Process and handle events
    - **Input**: Event streams, processing rules
    - **Output**: Processed events and actions
    - **Capabilities**: filtering, routing, transformation, aggregation
    """

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(discovery_doc)
        temp_file = f.name

    try:
        # Create MCP server with discovery
        server = DynamicActivationMCPServer(
            name="discovery_mcp_server",
            discovery_source=temp_file,
            discovery_config={
                "auto_discover": True,
                "max_tools": 50,
                "cache_ttl": 3600,
                "similarity_threshold": 0.7,
            },
        )

        logger.info(f"Created discovery MCP server: {server.name}")

        # Start server (triggers auto-discovery)
        await server.start()
        logger.info("Discovery MCP server started")

        # Connect client
        client_info = {
            "name": "Discovery Test Client",
            "version": "2.0",
            "capabilities": ["tools", "discovery", "streaming"],
        }

        connection_response = await server.handle_client_connect(
            "discovery_client", client_info
        )
        logger.info(f"Client connected: {connection_response}")

        # Test discovery-based tool requests
        discovery_requests = [
            {
                "tool": "advanced_calculator",
                "input": {"expression": "sin(pi/2) + cos(0)"},
                "client_id": "discovery_client",
            },
            {
                "tool": "nlp_processor",
                "input": {"text": "This is a test sentence for NLP processing."},
                "client_id": "discovery_client",
            },
            {
                "tool": "data_transformer",
                "input": {"data": {"name": "test", "value": 42}, "format": "xml"},
                "client_id": "discovery_client",
            },
        ]

        logger.info("Testing discovery-based tool requests...")
        for request in discovery_requests:
            response = await server.handle_tool_request(request)
            logger.info(f"Discovery tool '{request['tool']}' response: {response}")

        # Get comprehensive statistics
        stats = server.get_server_stats()
        logger.info(f"Discovery server statistics: {stats}")

        # Test tool schema retrieval
        tool_schemas = server.tool_registry.get_tool_schemas()
        logger.info(f"Available tool schemas: {list(tool_schemas.keys())}")

        # Disconnect and stop
        await server.handle_client_disconnect("discovery_client")
        await server.stop()

        return server

    finally:
        # Clean up
        os.unlink(temp_file)


async def example_3_multi_client_mcp():
    """Example 3: Multi-client MCP server with concurrent operations."""
    logger.info("=== Example 3: Multi-client MCP Server ===")

    # Create MCP server
    server = DynamicActivationMCPServer(
        name="multi_client_mcp_server",
        discovery_source="@haive-tools",
        discovery_config={
            "auto_discover": False,  # Manual tool registration
            "max_tools": 100,
        },
    )

    # Create concurrent-safe tools
    async def concurrent_calculator(input_data: dict[str, Any]) -> dict[str, Any]:
        """Concurrent-safe calculator."""
        client_id = input_data.get("client_id", "unknown")
        expression = input_data.get("expression", "0")

        try:
            result = eval(expression)
            return {
                "client_id": client_id,
                "expression": expression,
                "result": result,
                "timestamp": str(datetime.now()),
            }
        except Exception as e:
            return {
                "client_id": client_id,
                "expression": expression,
                "error": str(e),
                "timestamp": str(datetime.now()),
            }

    async def concurrent_text_processor(input_data: dict[str, Any]) -> dict[str, Any]:
        """Concurrent-safe text processor."""
        client_id = input_data.get("client_id", "unknown")
        text = input_data.get("text", "")

        try:
            # Simulate processing time
            await asyncio.sleep(0.1)

            return {
                "client_id": client_id,
                "original_text": text,
                "processed_text": text.upper(),
                "length": len(text),
                "timestamp": str(datetime.now()),
            }
        except Exception as e:
            return {
                "client_id": client_id,
                "error": str(e),
                "timestamp": str(datetime.now()),
            }

    async def concurrent_data_validator(input_data: dict[str, Any]) -> dict[str, Any]:
        """Concurrent-safe data validator."""
        client_id = input_data.get("client_id", "unknown")
        data = input_data.get("data", {})

        try:
            # Validate data structure
            validation_results = {
                "has_keys": len(data) > 0,
                "key_count": len(data),
                "has_strings": any(isinstance(v, str) for v in data.values()),
                "has_numbers": any(isinstance(v, (int, float)) for v in data.values()),
            }

            return {
                "client_id": client_id,
                "data": data,
                "validation": validation_results,
                "valid": validation_results["has_keys"],
                "timestamp": str(datetime.now()),
            }
        except Exception as e:
            return {
                "client_id": client_id,
                "error": str(e),
                "timestamp": str(datetime.now()),
            }

    # Create and register concurrent tools
    concurrent_tools = [
        MCPTool(
            name="concurrent_calculator",
            description="Concurrent mathematical calculator",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string"},
                    "client_id": {"type": "string"},
                },
                "required": ["expression"],
            },
            handler=concurrent_calculator,
        ),
        MCPTool(
            name="concurrent_text_processor",
            description="Concurrent text processing",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "client_id": {"type": "string"},
                },
                "required": ["text"],
            },
            handler=concurrent_text_processor,
        ),
        MCPTool(
            name="concurrent_data_validator",
            description="Concurrent data validation",
            input_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "object"},
                    "client_id": {"type": "string"},
                },
                "required": ["data"],
            },
            handler=concurrent_data_validator,
        ),
    ]

    # Register tools
    for i, tool in enumerate(concurrent_tools):
        item = RegistryItem(
            id=f"concurrent_tool_{i:03d}",
            name=tool.name.title(),
            description=tool.description,
            component=tool,
        )
        server.tool_registry.register(item)

    # Start server
    await server.start()
    logger.info("Multi-client MCP server started")

    # Create multiple clients
    clients = [
        {"id": "client_001", "name": "Client 1", "version": "1.0"},
        {"id": "client_002", "name": "Client 2", "version": "1.0"},
        {"id": "client_003", "name": "Client 3", "version": "1.0"},
    ]

    # Connect all clients
    for client in clients:
        response = await server.handle_client_connect(client["id"], client)
        logger.info(f"Connected {client['id']}: {response['status']}")

    # Activate tools
    for i in range(len(concurrent_tools)):
        await server.tool_registry.activate_mcp_tool(f"concurrent_tool_{i:03d}")

    # Create concurrent requests from multiple clients
    concurrent_requests = []

    for i, client in enumerate(clients):
        # Each client sends multiple requests
        client_requests = (
            [
                {
                    "tool": "concurrent_calculator",
                    "input": {
                        "expression": f"{i + 1} * {j + 1}",
                        "client_id": client["id"],
                    },
                    "client_id": client["id"],
                }
                for j in range(3)
            ]
            + [
                {
                    "tool": "concurrent_text_processor",
                    "input": {
                        "text": f"Hello from {client['name']}",
                        "client_id": client["id"],
                    },
                    "client_id": client["id"],
                }
            ]
            + [
                {
                    "tool": "concurrent_data_validator",
                    "input": {
                        "data": {"client": client["name"], "index": i},
                        "client_id": client["id"],
                    },
                    "client_id": client["id"],
                }
            ]
        )

        concurrent_requests.extend(client_requests)

    # Execute all requests concurrently
    logger.info(f"Executing {len(concurrent_requests)} concurrent requests...")

    async def execute_request(request):
        """Execute a single request."""
        return await server.handle_tool_request(request)

    start_time = asyncio.get_event_loop().time()

    # Execute all requests concurrently
    concurrent_responses = await asyncio.gather(
        *[execute_request(req) for req in concurrent_requests]
    )

    end_time = asyncio.get_event_loop().time()

    logger.info(
        f"Concurrent execution completed in {end_time - start_time:.3f} seconds"
    )

    # Analyze results
    successful_requests = sum(1 for resp in concurrent_responses if resp.get("success"))
    failed_requests = len(concurrent_responses) - successful_requests

    logger.info(
        f"Successful requests: {successful_requests}/{len(concurrent_responses)}"
    )
    logger.info(f"Failed requests: {failed_requests}/{len(concurrent_responses)}")

    # Get detailed statistics
    stats = server.get_server_stats()
    logger.info(f"Server statistics after concurrent execution: {stats}")

    # Disconnect all clients
    for client in clients:
        await server.handle_client_disconnect(client["id"])

    # Stop server
    await server.stop()

    return {
        "total_requests": len(concurrent_requests),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "execution_time": end_time - start_time,
        "requests_per_second": len(concurrent_requests) / (end_time - start_time),
    }


async def example_4_mcp_performance_testing():
    """Example 4: MCP server performance testing."""
    logger.info("=== Example 4: MCP Performance Testing ===")

    import time

    # Create high-performance MCP server
    server = DynamicActivationMCPServer(
        name="performance_mcp_server",
        discovery_source="@haive-tools",
        discovery_config={"auto_discover": False, "max_tools": 1000, "cache_ttl": 7200},
    )

    # Create lightweight performance tools
    async def fast_echo(input_data: dict[str, Any]) -> dict[str, Any]:
        """Fast echo tool for performance testing."""
        return {
            "input": input_data,
            "timestamp": str(datetime.now()),
            "tool": "fast_echo",
        }

    async def fast_counter(input_data: dict[str, Any]) -> dict[str, Any]:
        """Fast counter tool."""
        count = input_data.get("count", 1)
        return {
            "count": count,
            "doubled": count * 2,
            "timestamp": str(datetime.now()),
            "tool": "fast_counter",
        }

    # Create many lightweight tools
    performance_tools = []

    for i in range(100):
        tool = MCPTool(
            name=f"perf_tool_{i:03d}",
            description=f"Performance test tool {i}",
            input_schema={
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "operation": {"type": "string"},
                },
                "required": ["value"],
            },
            handler=fast_echo if i % 2 == 0 else fast_counter,
        )
        performance_tools.append(tool)

    # Register all tools
    start_time = time.time()

    for i, tool in enumerate(performance_tools):
        item = RegistryItem(
            id=f"perf_tool_{i:03d}",
            name=tool.name.title(),
            description=tool.description,
            component=tool,
        )
        server.tool_registry.register(item)

    registration_time = time.time() - start_time
    logger.info(f"Tool registration time: {registration_time:.3f} seconds (100 tools)")

    # Start server
    await server.start()

    # Connect performance client
    perf_client_info = {
        "name": "Performance Test Client",
        "version": "1.0",
        "capabilities": ["tools", "high_throughput"],
    }

    await server.handle_client_connect("perf_client", perf_client_info)

    # Activate all tools
    start_time = time.time()

    for i in range(100):
        await server.tool_registry.activate_mcp_tool(f"perf_tool_{i:03d}")

    activation_time = time.time() - start_time
    logger.info(f"Tool activation time: {activation_time:.3f} seconds (100 tools)")

    # Performance test 1: Sequential requests
    logger.info("Performance test 1: Sequential requests")

    sequential_requests = [
        {
            "tool": f"perf_tool_{i:03d}",
            "input": {"value": i, "operation": "test"},
            "client_id": "perf_client",
        }
        for i in range(50)
    ]

    start_time = time.time()

    sequential_responses = []
    for request in sequential_requests:
        response = await server.handle_tool_request(request)
        sequential_responses.append(response)

    sequential_time = time.time() - start_time
    logger.info(
        f"Sequential execution time: {sequential_time:.3f} seconds (50 requests)"
    )
    logger.info(
        f"Sequential requests per second: {len(sequential_requests) / sequential_time:.1f}"
    )

    # Performance test 2: Concurrent requests
    logger.info("Performance test 2: Concurrent requests")

    concurrent_requests = [
        {
            "tool": f"perf_tool_{i:03d}",
            "input": {"value": i, "operation": "concurrent"},
            "client_id": "perf_client",
        }
        for i in range(50)
    ]

    start_time = time.time()

    await asyncio.gather(
        *[server.handle_tool_request(req) for req in concurrent_requests]
    )

    concurrent_time = time.time() - start_time
    logger.info(
        f"Concurrent execution time: {concurrent_time:.3f} seconds (50 requests)"
    )
    logger.info(
        f"Concurrent requests per second: {len(concurrent_requests) / concurrent_time:.1f}"
    )

    # Performance test 3: Tool discovery performance
    logger.info("Performance test 3: Tool discovery performance")

    discovery_requests = [
        {
            "tool": f"nonexistent_tool_{i}",
            "input": {"value": i},
            "client_id": "perf_client",
        }
        for i in range(10)
    ]

    start_time = time.time()

    discovery_responses = []
    for request in discovery_requests:
        response = await server.handle_tool_request(request)
        discovery_responses.append(response)

    discovery_time = time.time() - start_time
    logger.info(f"Discovery time: {discovery_time:.3f} seconds (10 requests)")

    # Get final statistics
    final_stats = server.get_server_stats()

    # Performance summary
    logger.info("=== Performance Summary ===")
    logger.info(f"Tool registration: {registration_time:.3f}s (100 tools)")
    logger.info(f"Tool activation: {activation_time:.3f}s (100 tools)")
    logger.info(f"Sequential RPS: {len(sequential_requests) / sequential_time:.1f}")
    logger.info(f"Concurrent RPS: {len(concurrent_requests) / concurrent_time:.1f}")
    logger.info(f"Discovery overhead: {discovery_time / 10:.3f}s per request")
    logger.info(f"Total tool calls: {final_stats['tool_calls']}")
    logger.info(f"Active tools: {final_stats['active_components']}")

    # Cleanup
    await server.handle_client_disconnect("perf_client")
    await server.stop()

    return {
        "registration_time": registration_time,
        "activation_time": activation_time,
        "sequential_rps": len(sequential_requests) / sequential_time,
        "concurrent_rps": len(concurrent_requests) / concurrent_time,
        "discovery_overhead": discovery_time / 10,
        "total_tool_calls": final_stats["tool_calls"],
    }


async def main():
    """Run all MCP examples."""
    logger.info("Starting Dynamic Activation MCP Examples")

    try:
        # Example 1: Basic MCP server
        basic_server = await example_1_basic_mcp_server()

        # Example 2: Discovery-based MCP
        discovery_server = await example_2_discovery_based_mcp()

        # Example 3: Multi-client MCP
        multi_client_results = await example_3_multi_client_mcp()

        # Example 4: Performance testing
        performance_results = await example_4_mcp_performance_testing()

        logger.info("All MCP examples completed successfully!")

        # MCP Summary
        logger.info("=== MCP Examples Summary ===")
        logger.info(f"Basic server tools: {len(basic_server.tool_registry.items)}")
        logger.info(
            f"Discovery server discovery enabled: {discovery_server._discovery_agent is not None}"
        )
        logger.info(
            f"Multi-client concurrent requests: {multi_client_results['total_requests']}"
        )
        logger.info(
            f"Multi-client RPS: {multi_client_results['requests_per_second']:.1f}"
        )
        logger.info(
            f"Performance concurrent RPS: {performance_results['concurrent_rps']:.1f}"
        )

    except Exception as e:
        logger.error(f"MCP example execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
