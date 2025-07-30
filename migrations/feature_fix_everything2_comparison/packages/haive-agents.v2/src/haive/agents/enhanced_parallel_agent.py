"""Enhanced ParallelAgent implementation using Agent[AugLLMConfig].

ParallelAgent = Agent[AugLLMConfig] + parallel execution of agents.
"""

import asyncio
import logging
from typing import Any, Literal

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field, field_validator

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase as Agent

logger = logging.getLogger(__name__)


class ParallelAgent(Agent):  # Will be Agent[AugLLMConfig] when imports fixed
    """Enhanced ParallelAgent that executes agents concurrently.

    ParallelAgent = Agent[AugLLMConfig] + parallel execution + result aggregation.

    All agents receive the same input and execute concurrently. Results can be
    aggregated using various strategies (all, first, best, majority).

    Attributes:
        agents: List of agents to execute in parallel
        aggregation_strategy: How to combine results
        timeout_per_agent: Timeout for each agent
        min_agents_for_consensus: Minimum agents for consensus strategies

    Examples:
        Parallel analysis with multiple experts::

            experts = ParallelAgent(
                name="expert_panel",
                agents=[
                    FinanceExpert(),
                    TechExpert(),
                    MarketExpert()
                ],
                aggregation_strategy="all"
            )

            # All experts analyze simultaneously
            results = experts.run("Analyze startup investment opportunity")

        Consensus-based decision making::

            validators = ParallelAgent(
                name="validation_ensemble",
                agents=[Validator1(), Validator2(), Validator3()],
                aggregation_strategy="majority",
                min_agents_for_consensus=2
            )

            # Returns majority consensus
            decision = validators.run("Is this transaction valid?")
    """

    # Parallel specific fields
    agents: list[Agent] = Field(
        default_factory=list, description="List of agents to execute in parallel"
    )

    aggregation_strategy: Literal["all", "first", "best", "majority", "merge"] = Field(
        default="all", description="Strategy for aggregating results"
    )

    timeout_per_agent: float | None = Field(
        default=30.0, gt=0, description="Timeout for each agent in seconds"
    )

    continue_on_timeout: bool = Field(
        default=True, description="Continue if some agents timeout"
    )

    min_agents_for_consensus: int = Field(
        default=2, ge=1, description="Minimum agents needed for consensus strategies"
    )

    quality_scorer: Any | None = Field(
        default=None, description="Function to score result quality for 'best' strategy"
    )

    merge_with_llm: bool = Field(
        default=True, description="Use LLM to merge results in 'merge' strategy"
    )

    # Convenience fields
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    system_message: str | None = Field(default=None)

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: list[Agent]) -> list[Agent]:
        """Validate agent list."""
        if not v:
            raise ValueError("ParallelAgent requires at least one agent")

        if len(v) == 1:
            logger.warning("ParallelAgent with single agent is inefficient")

        return v

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the parallel group.

        Args:
            agent: Agent to add
        """
        self.agents.append(agent)
        logger.info(f"Added {type(agent).__name__} to parallel group")

    def remove_agent(self, agent: Agent) -> bool:
        """Remove an agent from the parallel group.

        Args:
            agent: Agent to remove

        Returns:
            True if removed, False if not found
        """
        try:
            self.agents.remove(agent)
            return True
        except ValueError:
            return False

    def setup_agent(self) -> None:
        """Setup parallel coordinator."""
        if isinstance(self.engine, AugLLMConfig):
            self.engine.temperature = self.temperature

            if not self.engine.system_message:
                if self.aggregation_strategy == "merge":
                    self.engine.system_message = self._get_merge_prompt()
                else:
                    self.engine.system_message = (
                        "You coordinate parallel agent execution."
                    )

    def _get_merge_prompt(self) -> str:
        """Get prompt for merging results."""
        agent_names = [
            getattr(agent, "name", f"Agent{i}") for i, agent in enumerate(self.agents)
        ]

        return f"""You are aggregating results from multiple parallel agents:

Agents: {', '.join(agent_names)}

Your task:
1. Receive all agent outputs
2. Identify common themes and unique insights
3. Resolve any contradictions intelligently
4. Synthesize a comprehensive response
5. Preserve important details from each agent

Create a unified response that leverages all agent contributions."""

    def build_graph(self) -> BaseGraph:
        """Build parallel execution graph."""
        graph = BaseGraph(name=f"{self.name}_parallel_graph")

        # Add parallel split node
        split_node = EngineNodeConfig(name="split", engine=self.engine)
        graph.add_node("split", split_node)
        graph.add_edge(START, "split")

        # Add each agent as parallel branch
        agent_nodes = []
        for i, agent in enumerate(self.agents):
            node_name = f"agent_{i}_{getattr(agent, 'name', f'parallel_{i}')}"

            agent_node = EngineNodeConfig(
                name=node_name,
                engine=agent.engine if hasattr(agent, "engine") else agent,
            )
            graph.add_node(node_name, agent_node)
            graph.add_edge("split", node_name)
            agent_nodes.append(node_name)

        # Add aggregation node
        if self.aggregation_strategy in ["merge", "best", "majority"]:
            agg_node = EngineNodeConfig(name="aggregate", engine=self.engine)
            graph.add_node("aggregate", agg_node)

            # Connect all agents to aggregator
            for node_name in agent_nodes:
                graph.add_edge(node_name, "aggregate")

            graph.add_edge("aggregate", END)
        else:
            # Direct to end for simple strategies
            for node_name in agent_nodes:
                graph.add_edge(node_name, END)

        return graph

    async def execute_parallel(self, input_data: Any) -> list[Any] | Any:
        """Execute all agents in parallel.

        Args:
            input_data: Input for all agents

        Returns:
            Aggregated results based on strategy
        """
        # Create tasks for all agents
        tasks = []
        for i, agent in enumerate(self.agents):
            if hasattr(agent, "arun"):
                task = agent.arun(input_data)
            else:
                # Wrap sync in async
                task = asyncio.create_task(asyncio.to_thread(agent.run, input_data))

            # Wrap with timeout if specified
            if self.timeout_per_agent:
                task = asyncio.wait_for(task, timeout=self.timeout_per_agent)

            tasks.append(task)

        # Execute all tasks
        if self.continue_on_timeout:
            # Gather with return_exceptions
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out exceptions
            valid_results = []
            errors = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    errors.append((i, str(result)))
                    logger.warning(f"Agent {i} failed: {result}")
                else:
                    valid_results.append((i, result))

            if not valid_results:
                raise RuntimeError(f"All agents failed: {errors}")

            results = valid_results
        else:
            # Fail fast on any error
            results = list(enumerate(await asyncio.gather(*tasks)))

        # Aggregate results based on strategy
        return await self._aggregate_results(results, input_data)

    async def _aggregate_results(
        self, results: list[tuple[int, Any]], original_input: Any
    ) -> list[Any] | Any:
        """Aggregate results based on strategy.

        Args:
            results: List of (agent_index, result) tuples
            original_input: Original input for context

        Returns:
            Aggregated result
        """
        if self.aggregation_strategy == "all":
            # Return all results with agent info
            return [
                {
                    "agent": getattr(self.agents[i], "name", f"agent_{i}"),
                    "result": result,
                }
                for i, result in results
            ]

        if self.aggregation_strategy == "first":
            # Return first successful result
            return results[0][1] if results else None

        if self.aggregation_strategy == "best":
            # Score and return best result
            if self.quality_scorer:
                scored = [
                    (i, result, self.quality_scorer(result)) for i, result in results
                ]
                best = max(scored, key=lambda x: x[2])
                return best[1]
            # Default to longest response
            best = max(results, key=lambda x: len(str(x[1])))
            return best[1]

        if self.aggregation_strategy == "majority":
            # Find consensus (simplified - real impl would be smarter)
            if len(results) < self.min_agents_for_consensus:
                raise ValueError(
                    f"Need at least {self.min_agents_for_consensus} agents for consensus"
                )

            # Group similar results (simplified)
            from collections import Counter

            result_strs = [str(r[1]).lower().strip() for r in results]
            consensus = Counter(result_strs).most_common(1)[0]

            # Return the original result that matches consensus
            for _i, result in results:
                if str(result).lower().strip() == consensus[0]:
                    return result

        elif self.aggregation_strategy == "merge":
            # Use LLM to merge all results
            if self.merge_with_llm and hasattr(self, "arun"):
                merge_input = {
                    "original_query": original_input,
                    "agent_results": [
                        {
                            "agent": getattr(self.agents[i], "name", f"agent_{i}"),
                            "result": result,
                        }
                        for i, result in results
                    ],
                    "instruction": "Merge these agent results into a comprehensive response",
                }
                return await self.arun(merge_input)
            # Simple concatenation
            return "\n\n".join(
                [
                    f"{getattr(self.agents[i], 'name', f'Agent {i}')}: {result}"
                    for i, result in results
                ]
            )

        return results

    def __repr__(self) -> str:
        """String representation with parallel info."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        [getattr(agent, "name", f"agent_{i}") for i, agent in enumerate(self.agents)]
        return (
            f"ParallelAgent[{engine_type}]("
            f"name='{self.name}', "
            f"agents={len(self.agents)}, "
            f"strategy='{self.aggregation_strategy}')"
        )


# Example usage
if __name__ == "__main__":
    # Mock agents for demo
    class MockExpert:
        def __init__(self, name: str, specialty: str):
            self.name = name
            self.specialty = specialty
            self.engine = AugLLMConfig()

        async def arun(self, input_data: str) -> str:
            # Simulate different processing times
            import random

            await asyncio.sleep(random.uniform(0.1, 0.5))
            return f"{self.name} ({self.specialty}): Analysis of '{input_data}' from {self.specialty} perspective"

    # Create parallel agent ensemble
    ensemble = ParallelAgent(
        name="expert_ensemble",
        agents=[
            MockExpert("Alice", "Finance"),
            MockExpert("Bob", "Technology"),
            MockExpert("Carol", "Marketing"),
            MockExpert("Dave", "Operations"),
        ],
        aggregation_strategy="all",
        timeout_per_agent=2.0,
    )

    print(f"Created: {ensemble}")
    print(f"Experts: {[agent.name for agent in ensemble.agents]}")
    print(f"Strategy: {ensemble.aggregation_strategy}")

    # Different aggregation strategies
    strategies = {
        "all": "Returns all expert opinions",
        "first": "Returns fastest expert's response",
        "best": "Returns highest quality response",
        "majority": "Returns consensus opinion",
        "merge": "LLM merges all responses",
    }

    print("\nAggregation strategies:")
    for strategy, description in strategies.items():
        print(f"  {strategy}: {description}")

    # Example execution
    print("\nExample parallel execution:")
    print("Input: 'Should we expand to European markets?'")
    print("\nAll experts analyze simultaneously...")
    print("- Alice (Finance): Financial feasibility analysis")
    print("- Bob (Technology): Technical infrastructure needs")
    print("- Carol (Marketing): Market opportunity assessment")
    print("- Dave (Operations): Operational requirements")
    print("\nResults aggregated based on strategy")
