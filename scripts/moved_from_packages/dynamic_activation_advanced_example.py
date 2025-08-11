"""Advanced Dynamic Activation Pattern Example.

This example demonstrates advanced usage of the Dynamic Activation Pattern
including MCP integration, multi-agent coordination, and complex workflows.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
- Real Azure OpenAI and MCP integration

Usage:
    poetry run python examples/dynamic_activation_advanced_example.py
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any

from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent
from haive.agents.react.dynamic_react_agent import DynamicReactAgent
from haive.agents.supervisor.dynamic_activation_supervisor import (
    DynamicActivationSupervisor,
)
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.registry import RegistryItem
from haive.mcp.dynamic_activation_mcp import DynamicActivationMCPServer, MCPTool
from langchain_core.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Advanced Tool Examples
@tool
def data_analyzer(data: str, analysis_type: str = "basic") -> dict[str, Any]:
    """Advanced data analysis tool.

    Args:
        data: JSON string or CSV data
        analysis_type: Type of analysis (basic, statistical, advanced)

    Returns:
        Analysis results dictionary
    """
    try:
        # Try parsing as JSON first
        try:
            parsed_data = json.loads(data)
            data_points = (
                parsed_data if isinstance(parsed_data, list) else [parsed_data]
            )
        except json.JSONDecodeError:
            # Fall back to CSV parsing
            lines = data.strip().split("\n")
            data_points = [line.split(",") for line in lines]

        # Perform analysis based on type
        if analysis_type == "basic":
            return {
                "type": "basic_analysis",
                "data_points": len(data_points),
                "sample": data_points[:3] if data_points else [],
                "timestamp": str(datetime.now()),
            }
        if analysis_type == "statistical":
            # Basic statistical analysis
            if isinstance(data_points[0], int | float):
                numbers = [
                    float(x) for x in data_points if isinstance(x, int | float | str)
                ]
                return {
                    "type": "statistical_analysis",
                    "count": len(numbers),
                    "mean": sum(numbers) / len(numbers) if numbers else 0,
                    "min": min(numbers) if numbers else 0,
                    "max": max(numbers) if numbers else 0,
                    "timestamp": str(datetime.now()),
                }
            return {
                "type": "statistical_analysis",
                "count": len(data_points),
                "data_type": "non_numeric",
                "timestamp": str(datetime.now()),
            }
        # advanced
        return {
            "type": "advanced_analysis",
            "data_points": len(data_points),
            "structure": type(data_points[0]).__name__ if data_points else "empty",
            "complexity": (
                "high"
                if len(data_points) > 100
                else "medium" if len(data_points) > 10 else "low"
            ),
            "timestamp": str(datetime.now()),
        }

    except Exception as e:
        logger.exception(f"Data analyzer error: {e}")
        return {"error": str(e), "timestamp": str(datetime.now())}


@tool
def workflow_coordinator(task: str, components: list[str]) -> dict[str, Any]:
    """Coordinate workflow across multiple components.

    Args:
        task: Task description
        components: List of component names to coordinate

    Returns:
        Coordination results
    """
    try:
        # Simulate workflow coordination
        workflow_id = f"workflow_{hash(task) % 10000}"

        return {
            "workflow_id": workflow_id,
            "task": task,
            "components": components,
            "status": "initiated",
            "estimated_duration": f"{len(components) * 2} minutes",
            "steps": [f"Initialize {component}" for component in components]
            + [f"Execute task with {component}" for component in components]
            + ["Consolidate results", "Generate report"],
            "timestamp": str(datetime.now()),
        }

    except Exception as e:
        logger.exception(f"Workflow coordinator error: {e}")
        return {"error": str(e), "timestamp": str(datetime.now())}


@tool
def report_generator(data: dict[str, Any], format_type: str = "json") -> str:
    """Generate formatted reports from data.

    Args:
        data: Data to include in report
        format_type: Report format (json, markdown, text)

    Returns:
        Formatted report string
    """
    try:
        if format_type == "json":
            return json.dumps(data, indent=2)
        if format_type == "markdown":
            report = "# Analysis Report\n\n"
            report += (
                f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            for key, value in data.items():
                report += f"## {key.title()}\n\n"
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        report += f"- **{subkey}**: {subvalue}\n"
                elif isinstance(value, list):
                    for item in value:
                        report += f"- {item}\n"
                else:
                    report += f"{value}\n"
                report += "\n"

            return report
        # text
        report = f"Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 50 + "\n\n"

        for key, value in data.items():
            report += f"{key.upper()}:\n"
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    report += f"  {subkey}: {subvalue}\n"
            elif isinstance(value, list):
                for item in value:
                    report += f"  - {item}\n"
            else:
                report += f"  {value}\n"
            report += "\n"

        return report

    except Exception as e:
        logger.exception(f"Report generator error: {e}")
        return f"Error generating report: {e}"


async def example_1_multi_agent_coordination():
    """Example 1: Multi-agent coordination with dynamic activation."""
    logger.info("=== Example 1: Multi-Agent Coordination ===")

    # Create shared AugLLMConfig
    config = AugLLMConfig(
        name="coordination_llm", temperature=0.3, max_tokens=400, model="gpt-4o-mini"
    )

    # Create specialized agents
    tools_data_agent = [
        {
            "id": "data_analyzer",
            "name": "Data Analyzer",
            "description": "Advanced data analysis",
            "component": data_analyzer,
            "category": "data",
        }
    ]

    tools_workflow_agent = [
        {
            "id": "workflow_coordinator",
            "name": "Workflow Coordinator",
            "description": "Coordinate complex workflows",
            "component": workflow_coordinator,
            "category": "workflow",
        }
    ]

    tools_report_agent = [
        {
            "id": "report_generator",
            "name": "Report Generator",
            "description": "Generate formatted reports",
            "component": report_generator,
            "category": "reporting",
        }
    ]

    # Create specialized agents
    data_agent = DynamicReactAgent.create_with_tools(
        name="data_specialist", tools=tools_data_agent, engine=config
    )

    workflow_agent = DynamicReactAgent.create_with_tools(
        name="workflow_specialist", tools=tools_workflow_agent, engine=config
    )

    report_agent = DynamicReactAgent.create_with_tools(
        name="report_specialist", tools=tools_report_agent, engine=config
    )

    # Create supervisor to coordinate agents
    supervisor_components = [
        {
            "id": "data_agent",
            "name": "Data Agent",
            "description": "Specialized data analysis agent",
            "component": data_agent,
        },
        {
            "id": "workflow_agent",
            "name": "Workflow Agent",
            "description": "Workflow coordination agent",
            "component": workflow_agent,
        },
        {
            "id": "report_agent",
            "name": "Report Agent",
            "description": "Report generation agent",
            "component": report_agent,
        },
    ]

    supervisor = DynamicActivationSupervisor.create_with_components(
        name="multi_agent_supervisor", components=supervisor_components, engine=config
    )

    logger.info("Created multi-agent system with supervisor")

    # Activate all agent components
    for comp_id in ["data_agent", "workflow_agent", "report_agent"]:
        meta_state = supervisor.state.activate_component(comp_id)
        logger.info(f"Activated {comp_id}: {meta_state is not None}")

    # Execute coordinated workflow
    try:
        # Step 1: Data analysis
        sample_data = '[{"value": 10, "category": "A"}, {"value": 20, "category": "B"}, {"value": 15, "category": "C"}]'

        # Activate tools for each agent
        await data_agent.activate_tool_by_name("Data Analyzer")
        await workflow_agent.activate_tool_by_name("Workflow Coordinator")
        await report_agent.activate_tool_by_name("Report Generator")

        # Execute data analysis
        logger.info("Executing data analysis...")
        data_result = await data_agent.arun(f"Analyze this data: {sample_data}")
        logger.info(f"Data analysis result: {data_result}")

        # Execute workflow coordination
        logger.info("Executing workflow coordination...")
        workflow_result = await workflow_agent.arun(
            "Coordinate a data processing workflow with components: data_analyzer, validator, reporter"
        )
        logger.info(f"Workflow coordination result: {workflow_result}")

        # Execute report generation
        logger.info("Executing report generation...")
        report_result = await report_agent.arun(
            "Generate a markdown report for the data analysis results"
        )
        logger.info(f"Report generation result: {report_result}")

        # Supervisor coordination
        logger.info("Supervisor coordinating overall task...")
        supervisor_result = await supervisor.arun(
            "Coordinate a complete data analysis workflow from raw data to final report"
        )
        logger.info(f"Supervisor coordination result: {supervisor_result}")

    except Exception as e:
        logger.exception(f"Multi-agent coordination error: {e}")

    # Get system statistics
    logger.info("=== System Statistics ===")

    for agent_name, agent in [
        ("Data", data_agent),
        ("Workflow", workflow_agent),
        ("Report", report_agent),
    ]:
        stats = agent.get_registry_stats()
        logger.info(f"{agent_name} Agent Stats: {stats}")

    supervisor_stats = supervisor.state.get_activation_stats()
    logger.info(f"Supervisor Stats: {supervisor_stats}")

    return supervisor


async def example_2_mcp_integration():
    """Example 2: MCP (Model Context Protocol) integration."""
    logger.info("=== Example 2: MCP Integration ===")

    # Create comprehensive tools documentation
    import os
    import tempfile

    mcp_tools_doc = """
    # MCP Dynamic Activation Tools

    ## Core Processing Tools

    ### Data Processor
    - **Name**: data_processor
    - **Description**: Process and transform data
    - **Input**: Data objects and processing instructions
    - **Output**: Processed data
    - **Category**: processing

    ### Validator
    - **Name**: validator
    - **Description**: Validate data and configurations
    - **Input**: Data and validation rules
    - **Output**: Validation results
    - **Category**: validation

    ### Formatter
    - **Name**: formatter
    - **Description**: Format data for output
    - **Input**: Data and format specifications
    - **Output**: Formatted data
    - **Category**: formatting

    ## Analysis Tools

    ### Statistical Analyzer
    - **Name**: statistical_analyzer
    - **Description**: Perform statistical analysis
    - **Input**: Numerical data and analysis parameters
    - **Output**: Statistical results
    - **Category**: analysis

    ### Trend Detector
    - **Name**: trend_detector
    - **Description**: Detect trends in time series data
    - **Input**: Time series data
    - **Output**: Trend analysis results
    - **Category**: analysis

    ## Utility Tools

    ### Logger
    - **Name**: logger
    - **Description**: Log system events and data
    - **Input**: Log messages and metadata
    - **Output**: Log confirmations
    - **Category**: utility

    ### Notifier
    - **Name**: notifier
    - **Description**: Send notifications
    - **Input**: Notification messages and channels
    - **Output**: Notification status
    - **Category**: utility
    """

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(mcp_tools_doc)
        temp_file = f.name

    try:
        # Create MCP server with dynamic activation
        mcp_server = DynamicActivationMCPServer(
            name="advanced_mcp_server",
            discovery_source=temp_file,
            discovery_config={
                "auto_discover": True,
                "max_tools": 50,
                "cache_ttl": 3600,
            },
        )

        logger.info(f"Created MCP server: {mcp_server.name}")

        # Create and register MCP tools
        def create_mcp_tool_handler(tool_name: str):
            """Create a handler for MCP tools."""

            async def handler(input_data: dict[str, Any]) -> dict[str, Any]:
                return {
                    "tool": tool_name,
                    "input": input_data,
                    "result": f"Processed by {tool_name}",
                    "timestamp": str(datetime.now()),
                }

            return handler

        mcp_tools = [
            MCPTool(
                name="data_processor",
                description="Process and transform data",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string"},
                        "operation": {
                            "type": "string",
                            "enum": ["clean", "transform", "aggregate"],
                        },
                    },
                    "required": ["data", "operation"],
                },
                handler=create_mcp_tool_handler("data_processor"),
            ),
            MCPTool(
                name="validator",
                description="Validate data and configurations",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string"},
                        "rules": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["data", "rules"],
                },
                handler=create_mcp_tool_handler("validator"),
            ),
            MCPTool(
                name="formatter",
                description="Format data for output",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string"},
                        "format": {"type": "string", "enum": ["json", "xml", "csv"]},
                    },
                    "required": ["data", "format"],
                },
                handler=create_mcp_tool_handler("formatter"),
            ),
        ]

        # Register MCP tools
        for i, tool in enumerate(mcp_tools):
            item = RegistryItem(
                id=f"mcp_tool_{i:03d}",
                name=tool.name.title(),
                description=tool.description,
                component=tool,
            )
            mcp_server.tool_registry.register(item)

        logger.info(f"Registered {len(mcp_tools)} MCP tools")

        # Start MCP server
        await mcp_server.start()
        logger.info("MCP server started")

        # Simulate client connection
        client_info = {
            "name": "Advanced Test Client",
            "version": "2.0",
            "capabilities": ["tools", "discovery", "streaming"],
        }

        connection_response = await mcp_server.handle_client_connect(
            "advanced_client", client_info
        )
        logger.info(f"Client connection: {connection_response}")

        # Activate MCP tools
        for i in range(len(mcp_tools)):
            tool = await mcp_server.tool_registry.activate_mcp_tool(
                f"mcp_tool_{i:03d}", mcp_server
            )
            logger.info(f"Activated MCP tool: {tool.name if tool else 'None'}")

        # Execute MCP tool requests
        requests = [
            {
                "tool": "data_processor",
                "input": {"data": "sample_data", "operation": "clean"},
                "client_id": "advanced_client",
            },
            {
                "tool": "validator",
                "input": {
                    "data": "validation_data",
                    "rules": ["not_empty", "valid_format"],
                },
                "client_id": "advanced_client",
            },
            {
                "tool": "formatter",
                "input": {"data": "format_data", "format": "json"},
                "client_id": "advanced_client",
            },
        ]

        logger.info("Executing MCP tool requests...")
        for request in requests:
            response = await mcp_server.handle_tool_request(request)
            logger.info(f"Tool {request['tool']} response: {response}")

        # Get available tools
        available_tools = mcp_server.get_available_tools()
        logger.info(f"Available tools: {[tool['name'] for tool in available_tools]}")

        # Get server statistics
        server_stats = mcp_server.get_server_stats()
        logger.info(f"Server statistics: {server_stats}")

        # Disconnect client
        await mcp_server.handle_client_disconnect("advanced_client")

        # Stop server
        await mcp_server.stop()
        logger.info("MCP server stopped")

        return mcp_server

    finally:
        # Clean up
        os.unlink(temp_file)


async def example_3_complex_discovery_workflow():
    """Example 3: Complex discovery workflow with multiple sources."""
    logger.info("=== Example 3: Complex Discovery Workflow ===")

    # Create multiple documentation sources
    import os
    import tempfile

    # Source 1: Core tools
    core_tools_doc = """
    # Core Tools Documentation

    ## System Tools

    ### File Manager
    - **Name**: file_manager
    - **Description**: Manage file operations
    - **Capabilities**: read, write, delete, copy, move
    - **Category**: system

    ### Process Monitor
    - **Name**: process_monitor
    - **Description**: Monitor system processes
    - **Capabilities**: list, kill, status, metrics
    - **Category**: system

    ### Network Client
    - **Name**: network_client
    - **Description**: Network communication client
    - **Capabilities**: http, https, websocket, tcp
    - **Category**: network
    """

    # Source 2: AI tools
    ai_tools_doc = """
    # AI Tools Documentation

    ## Machine Learning Tools

    ### Model Trainer
    - **Name**: model_trainer
    - **Description**: Train machine learning models
    - **Capabilities**: supervised, unsupervised, reinforcement
    - **Category**: ml

    ### Inference Engine
    - **Name**: inference_engine
    - **Description**: Run model inference
    - **Capabilities**: batch, streaming, real_time
    - **Category**: ml

    ### Data Preprocessor
    - **Name**: data_preprocessor
    - **Description**: Preprocess data for ML
    - **Capabilities**: cleaning, normalization, feature_engineering
    - **Category**: ml
    """

    # Source 3: Business tools
    business_tools_doc = """
    # Business Tools Documentation

    ## Analytics Tools

    ### KPI Calculator
    - **Name**: kpi_calculator
    - **Description**: Calculate key performance indicators
    - **Capabilities**: financial, operational, customer
    - **Category**: analytics

    ### Forecaster
    - **Name**: forecaster
    - **Description**: Business forecasting tool
    - **Capabilities**: sales, revenue, demand
    - **Category**: analytics

    ### Dashboard Generator
    - **Name**: dashboard_generator
    - **Description**: Generate business dashboards
    - **Capabilities**: charts, tables, metrics
    - **Category**: visualization
    """

    # Create temporary files
    temp_files = []
    for _doc_name, doc_content in [
        ("core_tools.md", core_tools_doc),
        ("ai_tools.md", ai_tools_doc),
        ("business_tools.md", business_tools_doc),
    ]:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(doc_content)
            temp_files.append(f.name)

    try:
        # Create discovery agents for each source
        discovery_agents = []
        for i, temp_file in enumerate(temp_files):
            agent = ComponentDiscoveryAgent(
                document_path=temp_file,
                discovery_config={"max_results": 20, "similarity_threshold": 0.7},
            )
            discovery_agents.append(agent)

        logger.info(f"Created {len(discovery_agents)} discovery agents")

        # Create AugLLMConfig for main agent
        config = AugLLMConfig(
            name="discovery_workflow_llm",
            temperature=0.4,
            max_tokens=500,
            model="gpt-4o-mini",
        )

        # Create main agent with discovery from first source
        DynamicReactAgent.create_with_discovery(
            name="complex_discovery_agent", document_path=temp_files[0], engine=config
        )

        logger.info("Created main agent with discovery capabilities")

        # Perform discovery from multiple sources
        all_discovered_components = []

        discovery_queries = [
            "system administration tools",
            "machine learning and AI tools",
            "business analytics and forecasting tools",
            "data processing and visualization tools",
        ]

        for i, (agent, query) in enumerate(
            zip(discovery_agents, discovery_queries, strict=False)
        ):
            try:
                components = await agent.discover_components(query)
                all_discovered_components.extend(components)
                logger.info(
                    f"Discovery agent {i + 1} found {len(components)} components for '{query}'"
                )
            except Exception as e:
                logger.exception(f"Discovery agent {i + 1} error: {e}")

        logger.info(f"Total discovered components: {len(all_discovered_components)}")

        # Create supervisor with all discovered components
        supervisor_components = []
        for i, component in enumerate(all_discovered_components):
            supervisor_components.append(
                {
                    "id": f"discovered_{i:03d}",
                    "name": component.get("name", f"Component {i}"),
                    "description": component.get("description", "Discovered component"),
                    "component": component,
                }
            )

        # Limit to first 10 components for demo
        supervisor_components = supervisor_components[:10]

        supervisor = DynamicActivationSupervisor.create_with_components(
            name="discovery_supervisor", components=supervisor_components, engine=config
        )

        logger.info(
            f"Created supervisor with {len(supervisor_components)} discovered components"
        )

        # Activate components by category
        categories = {}
        for comp in supervisor_components:
            category = comp["component"].get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(comp["id"])

        logger.info(f"Components by category: {categories}")

        # Activate components from each category
        activated_components = []
        for category, comp_ids in categories.items():
            # Activate first component from each category
            if comp_ids:
                meta_state = supervisor.state.activate_component(comp_ids[0])
                if meta_state:
                    activated_components.append(comp_ids[0])
                    logger.info(f"Activated component from {category}: {comp_ids[0]}")

        # Execute complex workflow
        try:
            workflow_result = await supervisor.arun(
                "Coordinate a complex workflow involving system tools, AI capabilities, and business analytics"
            )
            logger.info(f"Complex workflow result: {workflow_result}")
        except Exception as e:
            logger.exception(f"Complex workflow error: {e}")

        # Get comprehensive statistics
        logger.info("=== Comprehensive Statistics ===")

        # Discovery statistics
        for i, agent in enumerate(discovery_agents):
            if hasattr(agent, "_discovery_agent") and agent._discovery_agent:
                logger.info(f"Discovery agent {i + 1}: Active and configured")

        # Supervisor statistics
        supervisor_stats = supervisor.state.get_activation_stats()
        logger.info(f"Supervisor activation stats: {supervisor_stats}")

        # Component statistics by category
        for category, comp_ids in categories.items():
            active_in_category = [
                comp_id for comp_id in comp_ids if comp_id in activated_components
            ]
            logger.info(
                f"Category {category}: {len(active_in_category)}/{len(comp_ids)} active"
            )

        return supervisor

    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            os.unlink(temp_file)


async def example_4_performance_optimization():
    """Example 4: Performance optimization and monitoring."""
    logger.info("=== Example 4: Performance Optimization ===")

    import time

    # Create performance monitoring tools
    @tool
    def performance_monitor(operation: str, duration: float) -> dict[str, Any]:
        """Monitor performance metrics."""
        return {
            "operation": operation,
            "duration": duration,
            "timestamp": str(datetime.now()),
            "status": (
                "slow" if duration > 1.0 else "normal" if duration > 0.1 else "fast"
            ),
        }

    @tool
    def resource_tracker(resource_type: str, usage: float) -> dict[str, Any]:
        """Track resource usage."""
        return {
            "resource": resource_type,
            "usage": usage,
            "timestamp": str(datetime.now()),
            "status": "high" if usage > 80 else "medium" if usage > 50 else "low",
        }

    # Create optimized configuration
    config = AugLLMConfig(
        name="performance_optimized_llm",
        temperature=0.1,  # Lower temperature for consistency
        max_tokens=200,  # Smaller tokens for faster response
        model="gpt-4o-mini",  # Faster model
    )

    # Performance testing tools
    perf_tools = [
        {
            "id": "perf_monitor",
            "name": "Performance Monitor",
            "description": "Monitor operation performance",
            "component": performance_monitor,
            "category": "monitoring",
        },
        {
            "id": "resource_tracker",
            "name": "Resource Tracker",
            "description": "Track resource usage",
            "component": resource_tracker,
            "category": "monitoring",
        },
    ]

    # Create performance-optimized agent
    perf_agent = DynamicReactAgent.create_with_tools(
        name="performance_agent", tools=perf_tools, engine=config
    )

    logger.info("Created performance-optimized agent")

    # Performance test 1: Rapid tool activation
    logger.info("Testing rapid tool activation...")
    start_time = time.time()

    for tool_name in ["Performance Monitor", "Resource Tracker"]:
        await perf_agent.activate_tool_by_name(tool_name)

    activation_time = time.time() - start_time
    logger.info(f"Tool activation time: {activation_time:.3f} seconds")

    # Performance test 2: Concurrent operations
    logger.info("Testing concurrent operations...")

    async def run_operation(operation_id: int):
        """Run a single operation."""
        start = time.time()
        result = await perf_agent.arun(
            f"Monitor performance for operation {operation_id}"
        )
        duration = time.time() - start
        return {"operation_id": operation_id, "duration": duration, "result": result}

    start_time = time.time()

    # Run multiple operations concurrently
    tasks = [run_operation(i) for i in range(5)]
    await asyncio.gather(*tasks)

    concurrent_time = time.time() - start_time
    logger.info(f"Concurrent operations time: {concurrent_time:.3f} seconds")

    # Performance test 3: Large-scale component management
    logger.info("Testing large-scale component management...")

    from haive.core.registry import DynamicRegistry

    # Create large registry
    large_registry = DynamicRegistry[dict[str, Any]]()

    # Create many components
    start_time = time.time()

    for i in range(500):
        component = {
            "id": f"comp_{i:04d}",
            "name": f"Component {i}",
            "type": "performance_test",
            "metrics": {
                "response_time": 0.1 + (i % 10) * 0.01,
                "cpu_usage": 10 + (i % 80),
                "memory_usage": 50 + (i % 40),
            },
        }

        item = RegistryItem(
            id=f"perf_comp_{i:04d}",
            name=component["name"],
            description=f"Performance test component {i}",
            component=component,
        )

        large_registry.register(item)

    registration_time = time.time() - start_time
    logger.info(f"Large registry registration time: {registration_time:.3f} seconds")

    # Test batch activation
    start_time = time.time()

    # Activate first 100 components
    activation_results = []
    for i in range(100):
        success = large_registry.activate(f"perf_comp_{i:04d}")
        activation_results.append(success)

    batch_activation_time = time.time() - start_time
    successful_activations = sum(activation_results)
    logger.info(f"Batch activation time: {batch_activation_time:.3f} seconds")
    logger.info(f"Successful activations: {successful_activations}/100")

    # Performance test 4: Memory efficiency
    logger.info("Testing memory efficiency...")

    import gc

    import psutil

    # Get initial memory usage
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Create many agents
    agents = []
    for i in range(10):
        agent = DynamicReactAgent.create_with_tools(
            name=f"memory_test_agent_{i}", tools=perf_tools, engine=config
        )
        agents.append(agent)

    # Get memory after agent creation
    after_agents_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Clean up
    agents.clear()
    gc.collect()

    # Get memory after cleanup
    after_cleanup_memory = process.memory_info().rss / 1024 / 1024  # MB

    logger.info(f"Memory usage - Initial: {initial_memory:.1f} MB")
    logger.info(f"Memory usage - After agents: {after_agents_memory:.1f} MB")
    logger.info(f"Memory usage - After cleanup: {after_cleanup_memory:.1f} MB")
    logger.info(
        f"Memory per agent: {(after_agents_memory - initial_memory) / 10:.1f} MB"
    )

    # Performance summary
    logger.info("=== Performance Summary ===")
    logger.info(f"Tool activation: {activation_time:.3f}s")
    logger.info(
        f"Concurrent operations: {concurrent_time:.3f}s ({len(tasks)} operations)"
    )
    logger.info(f"Large registry: {registration_time:.3f}s (500 components)")
    logger.info(f"Batch activation: {batch_activation_time:.3f}s (100 components)")
    logger.info(
        f"Memory efficiency: {(after_agents_memory - initial_memory) / 10:.1f} MB/agent"
    )

    return {
        "activation_time": activation_time,
        "concurrent_time": concurrent_time,
        "registration_time": registration_time,
        "batch_activation_time": batch_activation_time,
        "memory_per_agent": (after_agents_memory - initial_memory) / 10,
        "large_registry": large_registry,
    }


async def main():
    """Run all advanced examples."""
    logger.info("Starting Advanced Dynamic Activation Pattern Examples")

    try:
        # Example 1: Multi-agent coordination
        supervisor = await example_1_multi_agent_coordination()

        # Example 2: MCP integration
        mcp_server = await example_2_mcp_integration()

        # Example 3: Complex discovery workflow
        discovery_supervisor = await example_3_complex_discovery_workflow()

        # Example 4: Performance optimization
        performance_results = await example_4_performance_optimization()

        logger.info("All advanced examples completed successfully!")

        # Advanced summary
        logger.info("=== Advanced Summary ===")
        logger.info(
            f"Multi-agent supervisor active components: {len(supervisor.state.active_components)}"
        )
        logger.info(f"MCP server tools: {len(mcp_server.tool_registry.items)}")
        logger.info(
            f"Discovery supervisor components: {len(discovery_supervisor.state.registry.items)}"
        )
        logger.info(f"Performance test results: {performance_results}")

    except Exception as e:
        logger.exception(f"Advanced example execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
