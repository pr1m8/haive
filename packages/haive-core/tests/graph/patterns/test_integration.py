# tests/graph/patterns/test_integration.py

import logging
import uuid
from typing import Any, Dict, Optional

from langgraph.graph import END, START
from pydantic import BaseModel
from rich import print as rprint
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.traceback import install

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import EngineType
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.patterns.base import (
    GraphPattern,
    ParameterDefinition,
    PatternMetadata,
)
from haive.core.graph.patterns.integration import register_integrations
from haive.core.models.llm.base import AzureLLMConfig

# Set up rich traceback handling for better error display
install(show_locals=True)

# Set up rich logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)

logger = logging.getLogger("tests.graph.patterns.test_integration")


# Create a test state schema
# Do this (with underscore):
class _TestState(BaseModel):
    """Test state for pattern integration tests."""

    test: str = ""
    value: Optional[str] = None


# Register integrations before running tests
def setup_module():
    """Set up for all tests in this module."""
    rprint(Panel.fit("Setting up pattern integration tests", style="cyan"))
    register_integrations()


class TestAgentPatternIntegration:
    """Test integration of patterns with agents and graphs."""

    def setup_method(self):
        """Set up for each test."""
        # Create a unique test ID for this run
        self.test_id = uuid.uuid4().hex[:8]
        rprint(Panel.fit(f"Running test with ID: {self.test_id}", style="green"))

    def create_test_llm_engine(self):
        """Create a test LLM engine for pattern testing."""
        logger.info("Creating test LLM engine")
        return AugLLMConfig(
            name="test_llm",
            llm_config=AzureLLMConfig(
                provider="azure",
                model="gpt-4o",
                api_key="dummy_key",
                api_version="2024-08-01-preview",
                api_base="https://awt-gpt.openai.azure.com/",
                api_type="azure",
            ),
            temperature=0.0,
            max_tokens=100,
        )

    def create_test_agent_config(self):
        """Create a test agent config for pattern testing."""
        logger.info("Creating test agent config")
        return AgentConfig(
            name="pattern_agent",
            engine=self.create_test_llm_engine(),
            engine_type=EngineType.AGENT,
            visualize=True,
            output_dir="./test_outputs",
            debug=False,
            save_history=True,
            runnable_config={
                "configurable": {
                    "thread_id": str(uuid.uuid4()),
                    "recursion_limit": 200,
                    "engine_configs": {},
                }
            },
            persistence={
                "type": "postgres",
                "setup_needed": True,
                "db_host": "localhost",
                "db_port": 5432,
                "db_name": "postgres",
                "db_user": "postgres",
                "db_pass": "postgres",
                "ssl_mode": "disable",
            },
        )

    def test_pattern_enhanced_workflow(self):
        """Test applying a pattern to enhance a workflow."""
        logger.info("Testing pattern enhanced workflow")

        # Create a test pattern class
        class TestIntegrationPattern(GraphPattern):
            """Test pattern for integration testing."""

            def __init__(self):
                logger.info("Creating test integration pattern")
                # Use proper ParameterDefinition for parameters
                metadata = PatternMetadata(
                    name="test_integration_pattern",
                    description="Test pattern for integration",
                    pattern_type="test",
                    parameters={
                        "node_name": ParameterDefinition(
                            type="str",
                            default="integration_node",
                            description="Name of the integration node",
                            required=False,
                        )
                    },
                )
                super().__init__(metadata=metadata)

            def apply(self, graph, **kwargs):
                """Apply the test pattern to a graph."""
                logger.info(f"Applying pattern to graph with kwargs: {kwargs}")

                # Extract parameters with defaults
                node_name = kwargs.get("node_name", "integration_node")

                # Add a node to the graph
                def node_fn(state):
                    """Test node function."""
                    logger.info(f"Processing state in test node: {state}")
                    return {
                        "test_applied": True,
                        "pattern_name": "test_integration_pattern",
                    }

                # Add the node to the graph
                try:
                    graph.add_node(node_name, node_fn)
                    logger.info(f"Added node {node_name} to graph")

                    # Add edges
                    graph.add_edge(START, node_name)
                    graph.add_edge(node_name, END)
                    logger.info(f"Added edges: START → {node_name} → END")

                    return True
                except Exception as e:
                    logger.error(f"Error applying pattern: {e}", exc_info=True)
                    return False

        # Create pattern instance
        pattern = TestIntegrationPattern()

        # Create test graph
        graph = DynamicGraph(name="enhanced_workflow_test", state_schema=_TestState)

        # Apply the pattern
        with console.status("[bold green]Applying pattern to graph..."):
            result = pattern.apply(graph)

        # Verify pattern was applied
        assert result is True, "Pattern application should succeed"
        assert "integration_node" in graph.nodes, "Node should be added to graph"

        # Check that nodes have engine/function
        assert (
            graph.nodes["integration_node"] is not None
        ), "Node should have engine/function"

        # Build the graph
        with console.status("[bold green]Building graph..."):
            built_graph = graph.build()
        assert built_graph is not None, "Graph building should succeed"

        # Compile the graph
        with console.status("[bold green]Compiling graph..."):
            compiled_graph = graph.compile()
        assert compiled_graph is not None, "Graph compilation should succeed"

        # Invoke the graph with a test state
        input_data = _TestState(test="test_value")
        with console.status("[bold green]Invoking graph..."):
            result = compiled_graph.invoke(input_data.model_dump())

        # Display the result
        rprint(Panel.fit(f"Graph execution result: {result}", style="blue"))

        # Verify the result
        assert "test_applied" in result, "Expected 'test_applied' in result"
        assert result["test_applied"] is True, "Expected test_applied to be True"
        assert (
            result["pattern_name"] == "test_integration_pattern"
        ), "Pattern name mismatch"

    def test_agent_config_pattern_integration(self):
        """Test integrating patterns with agent configs."""
        logger.info("Testing agent config pattern integration")

        # Create a test pattern class
        class TestIntegrationPattern(GraphPattern):
            """Test pattern for agent config integration."""

            def __init__(self):
                logger.info("Creating test integration pattern")
                # Use proper ParameterDefinition for parameters
                metadata = PatternMetadata(
                    name="test_integration_pattern",
                    description="Test pattern for integration",
                    pattern_type="test",
                    parameters={
                        "node_name": ParameterDefinition(
                            type="str",
                            default="integration_node",
                            description="Name of the integration node",
                            required=False,
                        )
                    },
                )
                super().__init__(metadata=metadata)

            def apply(self, agent_config, **kwargs):
                """Apply the test pattern to an agent config."""
                logger.info(f"Applying pattern to agent config: {agent_config.name}")

                # Modify the agent config
                if agent_config.node_configs is None:
                    agent_config.node_configs = {}

                # Extract parameter with default
                node_name = kwargs.get("node_name", "integration_node")

                # Add a node config
                agent_config.node_configs[node_name] = {
                    "name": node_name,
                    "engine": "test_llm",  # Reference the engine by name
                    "command_goto": "END",
                }

                logger.info(f"Added node config: {node_name}")
                return True

        # Create pattern instance
        pattern = TestIntegrationPattern()

        # Create test agent config
        agent_config = self.create_test_agent_config()

        # Apply the pattern
        with console.status("[bold green]Applying pattern to agent config..."):
            result = pattern.apply(agent_config)

        # Verify pattern was applied
        assert result is True, "Pattern application should succeed"
        assert (
            "integration_node" in agent_config.node_configs
        ), "Node config should be added"

        # Display the updated agent config
        rprint(
            Panel.fit(
                f"Updated node configs: {agent_config.node_configs}", style="blue"
            )
        )

    def test_dynamic_graph_integration_with_agent(self):
        """Test integrating patterns with dynamic graph and agent config."""
        logger.info("Testing dynamic graph integration with agent")

        # Create graph
        graph = DynamicGraph(name="dynamic_graph_test", state_schema=_TestState)
        logger.info(f"Created graph: {graph}")

        # Create test LLM engine
        llm_engine = self.create_test_llm_engine()
        logger.info("Adding engine to graph")

        # Create agent config
        pattern_agent_config = self.create_test_agent_config()

        # Create test pattern
        class TestPattern(GraphPattern):
            """Test pattern for dynamic graph with agent config."""

            def __init__(self):
                # Use proper ParameterDefinition for parameters
                metadata = PatternMetadata(
                    name="test_dynamic_graph_pattern",
                    description="Test pattern for dynamic graph with agent",
                    pattern_type="test",
                    parameters={
                        "node_name": ParameterDefinition(
                            type="str",
                            default="test_node",
                            description="Name of the node to create",
                            required=False,
                        )
                    },
                )
                super().__init__(metadata=metadata)

            def apply(self, graph, agent_config=None, **kwargs):
                """Apply the pattern to a graph and optionally agent config."""
                logger.info(
                    f"Applying pattern to graph with agent config: {agent_config is not None}"
                )

                # Extract parameters with defaults
                node_name = kwargs.get("node_name", "test_node")

                # Add engine to graph components
                graph.add_node(node_name, llm_engine, command_goto=END)
                logger.info(f"Added node {node_name} to graph")

                # Add edges
                graph.add_edge(START, node_name)
                logger.info(f"Added edge: START → {node_name}")

                # Update agent config if provided
                if agent_config:
                    if agent_config.node_configs is None:
                        agent_config.node_configs = {}

                    agent_config.node_configs[node_name] = {
                        "name": node_name,
                        "engine": llm_engine.name,
                        "command_goto": "END",
                    }
                    logger.info(f"Updated agent config with node: {node_name}")

                return True

        # Create pattern instance
        pattern = TestPattern()

        # Apply the pattern
        with console.status(
            "[bold green]Applying pattern to graph and agent config..."
        ):
            result = pattern.apply(graph, agent_config=pattern_agent_config)

        # Verify pattern was applied
        assert result is True, "Pattern application should succeed"
        assert "test_node" in graph.nodes, "Node should be added to graph"
        assert (
            "test_node" in pattern_agent_config.node_configs
        ), "Node config should be added to agent"

        # Build the graph
        with console.status("[bold green]Building graph..."):
            built_graph = graph.build()
        assert built_graph is not None, "Graph building should succeed"

        # Display the updated structures
        rprint(
            Panel.fit(f"Updated graph nodes: {list(graph.nodes.keys())}", style="blue")
        )
        rprint(
            Panel.fit(
                f"Updated agent node configs: {pattern_agent_config.node_configs}",
                style="blue",
            )
        )

    def test_pattern_schema_integration(self):
        """Test integrating patterns with state schema."""
        logger.info("Testing pattern schema integration")

        # Create graph with state schema
        graph = DynamicGraph(name="schema_pattern_test", state_schema=_TestState)
        logger.info(f"Created graph: {graph}")

        # Create test LLM engine
        self.create_test_llm_engine()
        logger.info("Adding engine to graph")

        # Create agent config
        self.create_test_agent_config()

        # Create test pattern with schema enhancement
        class SchemaPattern(GraphPattern):
            """Test pattern that enhances state schema."""

            def __init__(self):
                # Use proper ParameterDefinition for parameters
                metadata = PatternMetadata(
                    name="schema_pattern",
                    description="Pattern that enhances state schema",
                    pattern_type="schema",
                    parameters={
                        "node_name": ParameterDefinition(
                            type="str",
                            default="schema_node",
                            description="Name of the node to create",
                            required=False,
                        )
                    },
                )
                super().__init__(metadata=metadata)

            def apply(self, graph, **kwargs):
                """Apply the schema pattern to enhance a graph's state schema."""
                from haive.core.schema.schema_composer import SchemaComposer

                logger.info("Applying schema pattern to graph")

                # Extract parameters with defaults
                node_name = kwargs.get("node_name", "schema_node")

                # Create enhanced schema
                try:
                    # Get existing schema
                    existing_schema = graph.state_schema
                    logger.info(f"Found existing schema: {existing_schema.__name__}")

                    # Create composer with existing schema
                    composer = SchemaComposer(
                        name=f"Enhanced{existing_schema.__name__}"
                    )

                    # Add fields from existing schema
                    composer.add_fields_from_model(existing_schema)
                    logger.info("Added fields from existing schema")

                    # Add enhanced fields
                    composer.add_field(
                        "enhanced",
                        bool,
                        default=False,
                        description="Flag added by schema pattern",
                    )
                    composer.add_field(
                        "pattern_metadata",
                        Dict[str, Any],
                        default_factory=dict,
                        description="Metadata from pattern",
                    )
                    logger.info("Added enhanced fields")

                    # Build new schema
                    enhanced_schema = composer.build()
                    logger.info(f"Built enhanced schema: {enhanced_schema.__name__}")

                    # Add a node that uses the enhanced schema
                    def schema_node(state):
                        """Node that uses enhanced schema."""
                        logger.info(f"Schema node processing state: {state}")
                        # Update enhanced fields
                        return {
                            "enhanced": True,
                            "pattern_metadata": {
                                "pattern": "schema_pattern",
                                "applied_at": str(uuid.uuid4()),
                            },
                        }

                    # Add node to graph
                    graph.add_node(node_name, schema_node)
                    logger.info(f"Added node {node_name} to graph")

                    # Update graph's schema
                    graph.state_schema = enhanced_schema
                    logger.info(f"Updated graph schema to {enhanced_schema.__name__}")

                    return True
                except Exception as e:
                    logger.error(f"Error in schema pattern: {e}", exc_info=True)
                    return False

        # Create pattern instance
        pattern = SchemaPattern()

        # Apply the pattern
        with console.status("[bold green]Applying schema pattern to graph..."):
            result = pattern.apply(graph)

        # Verify pattern was applied
        assert result is True, "Pattern application should succeed"
        assert "schema_node" in graph.nodes, "Node should be added to graph"
        assert hasattr(
            graph.state_schema, "model_fields"
        ), "Schema should be a Pydantic model"
        assert (
            "enhanced" in graph.state_schema.model_fields
        ), "Enhanced field should be added to schema"

        # Display the enhanced schema
        rprint(
            Panel.fit(
                f"Enhanced schema fields: {list(graph.state_schema.model_fields.keys())}",
                style="blue",
            )
        )

    def test_simple_pattern_direct(self):
        """Test simple pattern application directly."""
        logger.info("Testing pattern integration directly")

        # Create simple graph
        graph = DynamicGraph(name="direct_test_graph", state_schema=_TestState)

        # Create simple test pattern
        class SimpleTestPattern(GraphPattern):
            """Basic test pattern."""

            def __init__(self):
                metadata = PatternMetadata(
                    name="simple_test_pattern",
                    description="Basic test pattern",
                    pattern_type="test",
                    parameters={},  # No parameters needed
                )
                super().__init__(metadata=metadata)

            def apply(self, graph, **kwargs):
                """Apply a simple pattern directly."""
                logger.info("Applying simple pattern to graph")

                # Simple identity function
                def identity_function(state):
                    """Return state unchanged."""
                    logger.info(f"Identity function called with state: {state}")
                    return {"processed": True}

                # Add node to graph
                try:
                    graph.add_node("direct_test_node", identity_function)
                    logger.info("Added direct_test_node to graph")

                    # Add edges
                    graph.add_edge(START, "direct_test_node")
                    graph.add_edge("direct_test_node", END)
                    logger.info("Added edges to graph")

                    return True
                except Exception as e:
                    logger.error(f"Error applying simple pattern: {e}", exc_info=True)
                    return False

        # Create pattern instance
        pattern = SimpleTestPattern()

        # Apply the pattern
        with console.status("[bold green]Applying simple pattern to graph..."):
            result = pattern.apply(graph)

        # Verify pattern was applied
        assert result is True, "Pattern application should succeed"
        assert "direct_test_node" in graph.nodes, "Node should be added to graph"

        # Build and compile the graph
        with console.status("[bold green]Building and compiling graph..."):
            compiled_graph = graph.compile()

        # Invoke the graph
        input_data = _TestState(test="simple_test")
        with console.status("[bold green]Invoking graph..."):
            result = compiled_graph.invoke(input_data.model_dump())

        # Display the result
        rprint(Panel.fit(f"Graph execution result: {result}", style="blue"))

        # Verify the result
        assert "processed" in result, "Expected 'processed' in result"
        assert result["processed"] is True, "Expected processed to be True"

    def teardown_method(self):
        """Clean up after each test."""
        rprint(Panel.fit(f"Test completed: {self.test_id}", style="green"))


if __name__ == "__main__":
    # Run all tests manually
    test_instance = TestAgentPatternIntegration()

    # Set up module
    setup_module()

    # Run test methods with rich output
    test_methods = [
        test_instance.test_pattern_enhanced_workflow,
        test_instance.test_agent_config_pattern_integration,
        test_instance.test_dynamic_graph_integration_with_agent,
        test_instance.test_pattern_schema_integration,
        test_instance.test_simple_pattern_direct,
    ]

    for test_method in test_methods:
        test_instance.setup_method()
        try:
            with console.status(f"[bold green]Running {test_method.__name__}..."):
                test_method()
            console.print(f"[bold green]✓[/] {test_method.__name__} passed")
        except Exception as e:
            console.print(f"[bold red]✗[/] {test_method.__name__} failed: {e}")
            console.print_exception()
        finally:
            test_instance.teardown_method()
