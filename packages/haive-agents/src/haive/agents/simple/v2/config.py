"""Simple agent implementation with comprehensive schema handling.

This module defines a basic single-node agent that uses AugLLMConfig for reasoning,
with support for structured outputs, schema composition, and explicit input/output schemas.
"""

import logging

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.node.config import NodeConfig
from langgraph.graph import END

from haive.agents.simple.config import SimpleAgentConfig

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(SimpleAgentConfig)
class SimpleAgent(Agent[SimpleAgentConfig]):
    """A simple agent with a single node workflow and comprehensive schema handling.

    Features:
    - Single processing node using AugLLMConfig
    - Support for explicit input/output schemas
    - Automatic schema derivation from engine
    - Intelligent input/output mapping
    - Structured output support
    """

    def __init__(self, config: SimpleAgentConfig):
        """Initialize the SimpleAgent with configuration.

        Args:
            config: SimpleAgentConfig instance
        """
        super().__init__(config)

    def setup_workflow(self) -> None:
        """Set up a single-node workflow with the configured schemas and mappings.

        This creates a simple graph with one processing node that handles:
        - Receiving input according to input schema
        - Processing with the AugLLM engine
        - Outputting results according to output schema
        """
        logger.info(f"Setting up workflow for {self.config.name}")

        # Create NodeConfig with command_goto=END
        node_config = NodeConfig(
            name=self.config.node_name,
            engine=self.config.engine,
            command_goto=END,  # Add this to tell the node where to go after processing
            # input_mapping=self.config.input_mapping,
            # output_mapping=self.config.output_mapping
        )

        # Create DynamicGraph with state schema
        gb = DynamicGraph(
            name=self.config.name,
            components=[self.config.engine],
            state_schema=self.config.state_schema,
            visualize=self.config.visualize,
        )

        # Get mappings from config (handles auto-derivation)
        # input_mapping = self.config.derive_input_mapping()
        # output_mapping = self.config.derive_output_mapping()

        # logger.debug(f"Using input mapping: {input_mapping}")
        # logger.debug(f"Using output mapping: {output_mapping}")

        # Add the processing node
        gb.add_node(
            name=self.config.node_name,
            config=node_config,
            # command_goto=END,
            # input_mapping=input_mapping,
            # output_mapping=output_mapping
        )

        # Set entry point
        gb.set_entry_point(self.config.node_name)
        gb.add_edge(self.config.node_name, END)
        # Get the built graph
        self.graph = gb.build()

        logger.info(f"Workflow setup complete for {self.config.name}")

    def has_messages_input(self) -> bool:
        """Check if this agent accepts a 'messages' input.

        Returns:
            True if agent has a messages field in input schema
        """
        # Check input schema if available
        if self.config.input_schema:
            return "messages" in self.config.input_schema.model_fields

        # Check input mapping if available
        if self.config.input_mapping:
            return "messages" in self.config.input_mapping

        # Default assumption
        return True
