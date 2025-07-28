"""Basic Dynamic Activation Pattern Example.

This example demonstrates the basic usage of the Dynamic Activation Pattern
with real components following Pydantic best practices.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
- No mocks, real Azure OpenAI integration

Usage:
    poetry run python examples/dynamic_activation_basic_example.py
"""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.registry import RegistryItem
from langchain_core.tools import tool

from haive.agents.react.dynamic_react_agent import DynamicReactAgent
from haive.agents.supervisor.dynamic_activation_supervisor import (
    DynamicActivationSupervisor,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Example 1: Basic Dynamic Tool Loading
@tool
def calculator(expression: str) -> float:
    """Calculate mathematical expression.

    Args:
        expression: Mathematical expression as string

    Returns:
        Calculated result

    Examples:
        calculator("2 + 2") -> 4.0
        calculator("10 * 5") -> 50.0
    """
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        logger.exception(f"Calculator error: {e}")
        return 0.0


@tool
def text_processor(text: str) -> str:
    """Process text input with various transformations.

    Args:
        text: Input text to process

    Returns:
        Processed text

    Examples:
        text_processor("hello world") -> "HELLO WORLD (processed)"
    """
    try:
        # Example processing: uppercase and add annotation
        processed = text.upper() + " (processed)"
        return processed
    except Exception as e:
        logger.exception(f"Text processor error: {e}")
        return text


@tool
def word_counter(text: str) -> int:
    """Count words in text.

    Args:
        text: Input text

    Returns:
        Number of words

    Examples:
        word_counter("hello world") -> 2
        word_counter("one two three four") -> 4
    """
    try:
        words = text.split()
        return len(words)
    except Exception as e:
        logger.exception(f"Word counter error: {e}")
        return 0


async def example_1_basic_dynamic_react_agent():
    """Example 1: Basic DynamicReactAgent with tool loading."""
    logger.info("=== Example 1: Basic DynamicReactAgent ===")

    # Create AugLLMConfig (real Azure OpenAI)
    config = AugLLMConfig(
        name="basic_example_llm", temperature=0.3, max_tokens=200, model="gpt-4o-mini"
    )

    # Create tools list for agent
    tools = [
        {
            "id": "calc_001",
            "name": "Calculator",
            "description": "Mathematical calculations",
            "component": calculator,
            "category": "math",
        },
        {
            "id": "text_001",
            "name": "Text Processor",
            "description": "Text processing and transformation",
            "component": text_processor,
            "category": "text",
        },
        {
            "id": "word_001",
            "name": "Word Counter",
            "description": "Count words in text",
            "component": word_counter,
            "category": "text",
        },
    ]

    # Create DynamicReactAgent with tools
    agent = DynamicReactAgent.create_with_tools(
        name="basic_dynamic_agent", tools=tools, engine=config
    )

    logger.info(f"Created agent: {agent.name}")
    logger.info(f"Registry has {len(agent.state.registry.items)} tools")

    # Activate specific tools
    await agent.activate_tool_by_name("Calculator")
    await agent.activate_tool_by_name("Text Processor")

    active_tools = agent.get_active_tool_names()
    logger.info(f"Active tools: {active_tools}")

    # Execute agent with a task
    try:
        result = await agent.arun(
            "Calculate 15 + 25 and then process the text 'hello world'"
        )
        logger.info(f"Agent result: {result}")
    except Exception as e:
        logger.exception(f"Agent execution error: {e}")

    # Get tool usage statistics
    stats = agent.get_tool_usage_stats()
    logger.info(f"Tool usage stats: {stats}")

    # Get registry statistics
    registry_stats = agent.get_registry_stats()
    logger.info(f"Registry stats: {registry_stats}")

    return agent


async def example_2_dynamic_activation_supervisor():
    """Example 2: DynamicActivationSupervisor with component management."""
    logger.info("=== Example 2: DynamicActivationSupervisor ===")

    # Create AugLLMConfig
    config = AugLLMConfig(
        name="supervisor_example_llm",
        temperature=0.5,
        max_tokens=300,
        model="gpt-4o-mini",
    )

    # Create components for supervisor
    components = [
        {
            "id": "math_processor",
            "name": "Math Processor",
            "description": "Mathematical processing component",
            "component": {
                "type": "processor",
                "category": "math",
                "capabilities": [
                    "addition",
                    "subtraction",
                    "multiplication",
                    "division",
                ],
            },
        },
        {
            "id": "text_analyzer",
            "name": "Text Analyzer",
            "description": "Text analysis component",
            "component": {
                "type": "analyzer",
                "category": "text",
                "capabilities": [
                    "sentiment",
                    "language_detection",
                    "keyword_extraction",
                ],
            },
        },
        {
            "id": "data_validator",
            "name": "Data Validator",
            "description": "Data validation component",
            "component": {
                "type": "validator",
                "category": "data",
                "capabilities": [
                    "format_validation",
                    "schema_validation",
                    "content_validation",
                ],
            },
        },
    ]

    # Create DynamicActivationSupervisor
    supervisor = DynamicActivationSupervisor.create_with_components(
        name="example_supervisor", components=components, engine=config
    )

    logger.info(f"Created supervisor: {supervisor.name}")
    logger.info(f"Registry has {len(supervisor.state.registry.items)} components")

    # Activate components
    supervisor.state.activate_component("math_processor")
    supervisor.state.activate_component("text_analyzer")

    logger.info(
        f"Activated components: {list(supervisor.state.active_components.keys())}"
    )

    # Execute supervisor
    try:
        result = await supervisor.arun(
            "I need help with mathematical calculations and text analysis"
        )
        logger.info(f"Supervisor result: {result}")
    except Exception as e:
        logger.exception(f"Supervisor execution error: {e}")

    # Get activation statistics
    activation_stats = supervisor.state.get_activation_stats()
    logger.info(f"Activation stats: {activation_stats}")

    # Deactivate a component
    supervisor.state.deactivate_component("text_analyzer")

    # Get updated stats
    updated_stats = supervisor.state.get_activation_stats()
    logger.info(f"Updated stats after deactivation: {updated_stats}")

    return supervisor


async def example_3_discovery_based_activation():
    """Example 3: Discovery-based dynamic activation."""
    logger.info("=== Example 3: Discovery-based Dynamic Activation ===")

    # Create temporary documentation for discovery
    import os
    import tempfile

    tools_doc = """
    # Example Tools Documentation

    ## Mathematical Tools

    ### Advanced Calculator
    - **Name**: advanced_calculator
    - **Description**: Advanced mathematical calculations with scientific functions
    - **Input**: Complex mathematical expressions
    - **Output**: Precise numerical results
    - **Category**: math
    - **Capabilities**: basic_math, trigonometry, logarithms, statistics

    ### Statistics Analyzer
    - **Name**: statistics_analyzer
    - **Description**: Statistical analysis and data processing
    - **Input**: Data arrays and statistical operations
    - **Output**: Statistical results and insights
    - **Category**: math
    - **Capabilities**: mean, median, mode, standard_deviation, correlation

    ## Text Processing Tools

    ### Natural Language Processor
    - **Name**: nlp_processor
    - **Description**: Advanced natural language processing
    - **Input**: Text documents and processing instructions
    - **Output**: Processed text with annotations
    - **Category**: text
    - **Capabilities**: tokenization, pos_tagging, named_entity_recognition

    ### Document Summarizer
    - **Name**: document_summarizer
    - **Description**: Automatic document summarization
    - **Input**: Long text documents
    - **Output**: Concise summaries
    - **Category**: text
    - **Capabilities**: extractive_summary, abstractive_summary

    ## Data Processing Tools

    ### Data Cleaner
    - **Name**: data_cleaner
    - **Description**: Clean and preprocess data
    - **Input**: Raw data in various formats
    - **Output**: Cleaned and structured data
    - **Category**: data
    - **Capabilities**: null_handling, duplicate_removal, format_conversion

    ### Schema Validator
    - **Name**: schema_validator
    - **Description**: Validate data against schemas
    - **Input**: Data and schema definitions
    - **Output**: Validation results and error reports
    - **Category**: data
    - **Capabilities**: json_schema, xml_schema, custom_validation
    """

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(tools_doc)
        temp_file = f.name

    try:
        # Create AugLLMConfig
        config = AugLLMConfig(
            name="discovery_example_llm",
            temperature=0.4,
            max_tokens=250,
            model="gpt-4o-mini",
        )

        # Create DynamicReactAgent with discovery
        agent = DynamicReactAgent.create_with_discovery(
            name="discovery_agent", document_path=temp_file, engine=config
        )

        logger.info(f"Created discovery agent: {agent.name}")
        logger.info(f"Discovery agent configured: {agent._discovery_agent is not None}")

        # Discover tools for specific tasks
        try:
            math_tools = await agent.discover_and_load_tools(
                "mathematical calculations and statistics"
            )
            logger.info(f"Discovered {len(math_tools)} math tools")

            text_tools = await agent.discover_and_load_tools(
                "text processing and summarization"
            )
            logger.info(f"Discovered {len(text_tools)} text tools")

            # Check discovery queries
            logger.info(f"Discovery queries: {agent.state.discovery_queries}")

        except Exception as e:
            logger.exception(f"Discovery error: {e}")

        # Execute agent with discovered tools
        try:
            result = await agent.arun(
                "I need help with statistical analysis of text data"
            )
            logger.info(f"Discovery agent result: {result}")
        except Exception as e:
            logger.exception(f"Discovery agent execution error: {e}")

        # Get tool categorization
        categories = agent.state.tool_categories
        logger.info(f"Tool categories: {categories}")

        # Get tools by category
        for category in categories:
            tools_in_category = agent.get_tools_by_category(category)
            logger.info(f"Tools in {category}: {tools_in_category}")

        return agent

    finally:
        # Clean up temporary file
        os.unlink(temp_file)


async def example_4_registry_management():
    """Example 4: Direct registry management and component lifecycle."""
    logger.info("=== Example 4: Registry Management ===")

    from haive.core.registry import DynamicRegistry
    from haive.core.schema.prebuilt.dynamic_activation_state import (
        DynamicActivationState,
    )

    # Create registry for custom components
    registry = DynamicRegistry[dict[str, Any]]()

    # Create custom components
    components = [
        {
            "name": "data_processor",
            "type": "processor",
            "version": "1.0",
            "capabilities": ["csv", "json", "xml"],
            "status": "ready",
        },
        {
            "name": "file_manager",
            "type": "manager",
            "version": "2.0",
            "capabilities": ["read", "write", "delete"],
            "status": "ready",
        },
        {
            "name": "network_client",
            "type": "client",
            "version": "1.5",
            "capabilities": ["http", "https", "websocket"],
            "status": "ready",
        },
    ]

    # Register components
    for i, component in enumerate(components):
        item = RegistryItem(
            id=f"comp_{i:03d}",
            name=component["name"].title(),
            description=f"{component['type'].title()} component",
            component=component,
            metadata={
                "version": component["version"],
                "capabilities": component["capabilities"],
            },
        )
        registry.register(item)

    logger.info(f"Registered {len(registry.items)} components")

    # Test activation patterns
    logger.info("Testing activation patterns...")

    # Activate all components
    for item_id in registry.list_components():
        success = registry.activate(item_id)
        logger.info(f"Activated {item_id}: {success}")

    # Get active components
    active_items = registry.get_active_items()
    logger.info(f"Active components: {[item.name for item in active_items]}")

    # Test deactivation
    registry.deactivate("comp_001")
    logger.info("Deactivated comp_001")

    # Get registry statistics
    stats = registry.get_stats()
    logger.info(f"Registry stats: {stats}")

    # Create DynamicActivationState with registry
    state = DynamicActivationState()

    # Transfer components to state registry
    for item_id in registry.list_components():
        item = registry.get_item(item_id)
        if item:
            state.registry.register(item)

    # Test component activation with MetaStateSchema
    logger.info("Testing component activation with MetaStateSchema...")

    for item_id in state.registry.list_components():
        meta_state = state.activate_component(item_id)
        if meta_state:
            logger.info(
                f"Activated {item_id} with MetaStateSchema: {meta_state.execution_status}"
            )

    # Get activation statistics
    activation_stats = state.get_activation_stats()
    logger.info(f"Activation stats: {activation_stats}")

    return state


async def example_5_performance_testing():
    """Example 5: Performance testing with many components."""
    logger.info("=== Example 5: Performance Testing ===")

    import time

    from haive.core.registry import DynamicRegistry

    # Create large registry
    large_registry = DynamicRegistry[dict[str, Any]]()

    # Create many components
    num_components = 1000
    logger.info(f"Creating {num_components} components...")

    start_time = time.time()

    components = []
    for i in range(num_components):
        component = {
            "name": f"component_{i}",
            "type": "test",
            "version": "1.0",
            "index": i,
            "data": f"test_data_{i}",
        }
        components.append(component)

    creation_time = time.time() - start_time
    logger.info(f"Created {num_components} components in {creation_time:.3f} seconds")

    # Register all components
    start_time = time.time()

    for i, component in enumerate(components):
        item = RegistryItem(
            id=f"perf_{i:04d}",
            name=f"Component {i}",
            description=f"Performance test component {i}",
            component=component,
        )
        large_registry.register(item)

    registration_time = time.time() - start_time
    logger.info(
        f"Registered {num_components} components in {registration_time:.3f} seconds"
    )

    # Test activation performance
    start_time = time.time()

    # Activate first 100 components
    activated_count = 0
    for i in range(100):
        success = large_registry.activate(f"perf_{i:04d}")
        if success:
            activated_count += 1

    activation_time = time.time() - start_time
    logger.info(
        f"Activated {activated_count} components in {activation_time:.3f} seconds"
    )

    # Test stats performance
    start_time = time.time()
    stats = large_registry.get_stats()
    stats_time = time.time() - start_time
    logger.info(f"Generated stats in {stats_time:.3f} seconds")
    logger.info(f"Performance stats: {stats}")

    # Test deactivation performance
    start_time = time.time()

    deactivated_count = 0
    for i in range(0, 100, 2):  # Deactivate every other component
        success = large_registry.deactivate(f"perf_{i:04d}")
        if success:
            deactivated_count += 1

    deactivation_time = time.time() - start_time
    logger.info(
        f"Deactivated {deactivated_count} components in {deactivation_time:.3f} seconds"
    )

    # Final stats
    final_stats = large_registry.get_stats()
    logger.info(f"Final stats: {final_stats}")

    return large_registry


async def main():
    """Run all examples."""
    logger.info("Starting Dynamic Activation Pattern Examples")

    try:
        # Example 1: Basic dynamic React agent
        agent = await example_1_basic_dynamic_react_agent()

        # Example 2: Dynamic activation supervisor
        supervisor = await example_2_dynamic_activation_supervisor()

        # Example 3: Discovery-based activation
        discovery_agent = await example_3_discovery_based_activation()

        # Example 4: Registry management
        state = await example_4_registry_management()

        # Example 5: Performance testing
        perf_registry = await example_5_performance_testing()

        logger.info("All examples completed successfully!")

        # Summary
        logger.info("=== Summary ===")
        logger.info(f"Basic agent active tools: {len(agent.get_active_tool_names())}")
        logger.info(
            f"Supervisor active components: {len(supervisor.state.active_components)}"
        )
        logger.info(
            f"Discovery agent queries: {len(discovery_agent.state.discovery_queries)}"
        )
        logger.info(f"State registry components: {len(state.registry.items)}")
        logger.info(f"Performance registry components: {len(perf_registry.items)}")

    except Exception as e:
        logger.exception(f"Example execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
