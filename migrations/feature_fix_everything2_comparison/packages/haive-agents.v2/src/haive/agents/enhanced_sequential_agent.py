"""Enhanced SequentialAgent implementation using Agent[AugLLMConfig].

SequentialAgent = Agent[AugLLMConfig] + sequential execution of agents.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field, field_validator

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase as Agent

logger = logging.getLogger(__name__)


class SequentialAgent(Agent):  # Will be Agent[AugLLMConfig] when imports fixed
    """Enhanced SequentialAgent that executes agents in sequence.

    SequentialAgent = Agent[AugLLMConfig] + sequential pipeline execution.

    Each agent's output becomes the next agent's input, creating a pipeline.
    The coordinator (this agent) can optionally process results between steps.

    Attributes:
        agents: List of agents to execute in order
        process_between_steps: Whether to process between agent calls
        continue_on_error: Whether to continue if an agent fails
        return_all_outputs: Return all intermediate outputs vs just final

    Examples:
        Simple pipeline::

            # Create pipeline: Researcher -> Analyst -> Writer
            pipeline = SequentialAgent(
                name="report_pipeline",
                agents=[
                    ResearchAgent(name="researcher"),
                    AnalystAgent(name="analyst"),
                    WriterAgent(name="writer")
                ]
            )

            result = pipeline.run("Create report on AI trends")
            # Researcher finds data -> Analyst processes -> Writer creates report

        With intermediate processing::

            pipeline = SequentialAgent(
                name="enhanced_pipeline",
                agents=[research_agent, analysis_agent],
                process_between_steps=True,
                system_message="Enhance and clarify outputs between steps"
            )

            # Coordinator enhances outputs between each step
    """

    # Sequential specific fields
    agents: list[Agent] = Field(
        default_factory=list, description="Ordered list of agents to execute"
    )

    process_between_steps: bool = Field(
        default=False, description="Whether coordinator processes between steps"
    )

    continue_on_error: bool = Field(
        default=False, description="Continue pipeline if an agent fails"
    )

    return_all_outputs: bool = Field(
        default=False, description="Return all intermediate outputs"
    )

    max_retries_per_step: int = Field(
        default=1, ge=1, le=3, description="Max retries for each step"
    )

    step_timeout: float | None = Field(
        default=None, gt=0, description="Timeout for each step in seconds"
    )

    # Convenience fields
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    system_message: str | None = Field(default=None)

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: list[Agent]) -> list[Agent]:
        """Validate agent list."""
        if not v:
            raise ValueError("SequentialAgent requires at least one agent")

        for i, agent in enumerate(v):
            if not hasattr(agent, "run") and not hasattr(agent, "arun"):
                raise ValueError(f"Agent at index {i} must be a valid agent")

        return v

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the end of the sequence.

        Args:
            agent: Agent to add to pipeline
        """
        self.agents.append(agent)
        logger.info(f"Added {type(agent).__name__} to sequence")

    def insert_agent(self, index: int, agent: Agent) -> None:
        """Insert an agent at specific position.

        Args:
            index: Position to insert at
            agent: Agent to insert
        """
        self.agents.insert(index, agent)
        logger.info(f"Inserted {type(agent).__name__} at position {index}")

    def remove_agent(self, index: int) -> Agent | None:
        """Remove agent at index.

        Args:
            index: Position to remove from

        Returns:
            Removed agent or None
        """
        if 0 <= index < len(self.agents):
            return self.agents.pop(index)
        return None

    def get_pipeline_description(self) -> str:
        """Get human-readable pipeline description."""
        steps = []
        for i, agent in enumerate(self.agents):
            agent_name = getattr(agent, "name", type(agent).__name__)
            steps.append(f"{i+1}. {agent_name}")

        return " → ".join(steps)

    def setup_agent(self) -> None:
        """Setup sequential coordinator."""
        if isinstance(self.engine, AugLLMConfig):
            self.engine.temperature = self.temperature

            if not self.engine.system_message:
                if self.process_between_steps:
                    self.engine.system_message = self._get_coordinator_prompt()
                else:
                    self.engine.system_message = (
                        "You coordinate a sequential pipeline of agents."
                    )

    def _get_coordinator_prompt(self) -> str:
        """Get coordinator prompt for processing between steps."""
        pipeline_desc = self.get_pipeline_description()

        return f"""You are coordinating a sequential pipeline of agents:

Pipeline: {pipeline_desc}

Your role when processing between steps:
1. Receive output from the previous agent
2. Enhance, clarify, or format the output as needed
3. Prepare optimal input for the next agent
4. Ensure smooth data flow through the pipeline
5. Handle any format conversions needed

Always preserve key information while improving clarity and structure."""

    def build_graph(self) -> BaseGraph:
        """Build sequential execution graph."""
        graph = BaseGraph(name=f"{self.name}_sequential_graph")

        prev_node = START

        # Add coordinator node if processing between steps
        if self.process_between_steps:
            coordinator_node = EngineNodeConfig(name="coordinator", engine=self.engine)
            graph.add_node("coordinator", coordinator_node)

        # Add each agent as a node
        for i, agent in enumerate(self.agents):
            node_name = f"step_{i}_{getattr(agent, 'name', f'agent_{i}')}"

            # Create node for agent
            agent_node = EngineNodeConfig(
                name=node_name,
                engine=agent.engine if hasattr(agent, "engine") else agent,
            )
            graph.add_node(node_name, agent_node)

            # Connect nodes
            if self.process_between_steps and i > 0:
                # Previous -> Coordinator -> Current
                graph.add_edge(prev_node, "coordinator")
                graph.add_edge("coordinator", node_name)
            else:
                # Direct connection
                graph.add_edge(prev_node, node_name)

            prev_node = node_name

        # Connect last node to end
        graph.add_edge(prev_node, END)

        return graph

    async def execute_sequence(self, input_data: Any) -> Any | list[Any]:
        """Execute agents in sequence.

        Args:
            input_data: Initial input for the pipeline

        Returns:
            Final output or list of all outputs
        """
        current_input = input_data
        outputs = []

        for i, agent in enumerate(self.agents):
            try:
                # Execute agent
                logger.debug(
                    f"Executing step {i+1}: {getattr(agent, 'name', f'agent_{i}')}"
                )

                if hasattr(agent, "arun"):
                    output = await agent.arun(current_input)
                else:
                    # Fallback to sync
                    output = agent.run(current_input)

                outputs.append(output)

                # Process between steps if enabled
                if self.process_between_steps and i < len(self.agents) - 1:
                    if hasattr(self, "arun"):
                        output = await self.arun(
                            {
                                "previous_output": output,
                                "next_agent": getattr(
                                    self.agents[i + 1], "name", f"agent_{i+1}"
                                ),
                                "instruction": "Process this output for the next agent",
                            }
                        )

                current_input = output

            except Exception as e:
                logger.error(f"Error in step {i+1}: {e}")
                if not self.continue_on_error:
                    raise
                outputs.append({"error": str(e)})
                # Use original input for next step if continuing

        return outputs if self.return_all_outputs else current_input

    def __repr__(self) -> str:
        """String representation with pipeline info."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        pipeline = " → ".join(
            [getattr(agent, "name", type(agent).__name__) for agent in self.agents]
        )
        return (
            f"SequentialAgent[{engine_type}](name='{self.name}', pipeline=[{pipeline}])"
        )


# Example usage
if __name__ == "__main__":
    # Mock agents for demo
    class MockAgent:
        def __init__(self, name: str, transform: str):
            self.name = name
            self.transform = transform
            self.engine = AugLLMConfig()

        async def arun(self, input_data: str) -> str:
            return f"{self.name}: {self.transform}({input_data})"

    # Create sequential pipeline
    pipeline = SequentialAgent(
        name="text_processing_pipeline",
        agents=[
            MockAgent("cleaner", "CLEAN"),
            MockAgent("analyzer", "ANALYZE"),
            MockAgent("summarizer", "SUMMARIZE"),
        ],
        process_between_steps=False,
        return_all_outputs=True,
    )

    print(f"Created: {pipeline}")
    print(f"Pipeline: {pipeline.get_pipeline_description()}")

    # Add another step
    pipeline.add_agent(MockAgent("formatter", "FORMAT"))
    print(f"Updated pipeline: {pipeline.get_pipeline_description()}")

    # Example execution flow
    print("\nExample execution:")
    print("Input: 'Raw text data'")
    print("Step 1: cleaner: CLEAN(Raw text data)")
    print("Step 2: analyzer: ANALYZE(cleaner: CLEAN(Raw text data))")
    print("Step 3: summarizer: SUMMARIZE(analyzer: ANALYZE(...))")
    print("Step 4: formatter: FORMAT(summarizer: SUMMARIZE(...))")

    # With intermediate processing
    pipeline_enhanced = SequentialAgent(
        name="enhanced_pipeline",
        agents=[MockAgent("researcher", "RESEARCH"), MockAgent("writer", "WRITE")],
        process_between_steps=True,
        system_message="Enhance outputs between steps",
    )

    print(f"\nEnhanced pipeline: {pipeline_enhanced}")
    print("Coordinator processes and enhances data between each step")
