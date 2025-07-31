"""Enhanced SupervisorAgent implementation using Agent[AugLLMConfig].

SupervisorAgent = Agent[AugLLMConfig] + worker management + delegation.
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from pydantic import Field, field_validator, model_validator

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
# For now, using minimal base
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase as Agent

logger = logging.getLogger(__name__)


class SupervisorAgent(Agent):  # Will be Agent[AugLLMConfig] when imports fixed
    """Enhanced SupervisorAgent that coordinates multiple worker agents.

    SupervisorAgent = Agent[AugLLMConfig] + worker management + delegation.

    The Supervisor pattern allows:
    1. Managing a team of worker agents
    2. Delegating tasks to appropriate workers
    3. Coordinating results from multiple workers
    4. Making decisions based on worker outputs

    Attributes:
        workers: Dictionary of worker agents
        max_delegation_rounds: Maximum rounds of delegation
        delegation_strategy: How to choose workers (first, best, all)
        supervisor_prompt: Custom prompt for supervision

    Examples:
        Basic supervisor with workers::

            from haive.agents.simple import SimpleAgent
            from haive.agents.react import ReactAgent

            # Create workers
            analyst = SimpleAgent(name="analyst", engine=AugLLMConfig())
            researcher = ReactAgent(name="researcher", tools=[web_search])

            # Create supervisor
            supervisor = SupervisorAgent(
                name="project_managef",
                workers={
                    "analyst": analyst,
                    "researcher": researcher
                }
            )

            result = supervisor.run("Analyze market trends for electric vehicles")
            # Supervisor will delegate to researcher for data, then analyst for insights

        Dynamic worker addition::

            supervisor = SupervisorAgent(name="manager")
            supervisor.add_worker("coder", CodingAgent())
            supervisor.add_worker("tester", TestingAgent())

            result = supervisor.run("Implement and test a sorting algorithm")
    """

    # Supervisor specific fields
    workers: dict[str, Agent] = Field(
        default_factory=dict, description="Dictionary of worker agents"
    )

    max_delegation_rounds: int = Field(
        default=3, ge=1, le=10, description="Maximum rounds of delegation to workers"
    )

    delegation_strategy: Literal["first", "best", "all", "round_robin"] = Field(
        default="best", description="Strategy for choosing workers"
    )

    supervisor_prompt: str | None = Field(
        default=None, description="Custom supervisor prompt"
    )

    allow_direct_response: bool = Field(
        default=True, description="Whether supervisor can respond without delegating"
    )

    # Convenience fields
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)  # Lower temp for decisions
    max_tokens: int | None = Field(default=None, ge=1)

    @field_validator("workers")
    @classmethod
    def validate_workers(cls, v: dict[str, Agent]) -> dict[str, Agent]:
        """Validate worker agents."""
        if not isinstance(v, dict):
            raise ValueError("Workers must be a dictionary")

        for name, agent in v.items():
            if not hasattr(agent, "run") and not hasattr(agent, "arun"):
                raise ValueError(f"Worker '{name}' must be a valid agent")

        return v

    @model_validator(mode="before")
    @classmethod
    def ensure_aug_llm_config(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure supervisor has AugLLMConfig engine."""
        if not isinstance(values, dict):
            return values

        # Create engine if not provided
        if "engine" not in values or values["engine"] is None:
            values["engine"] = AugLLMConfig(
                temperature=values.get("temperature", 0.3),
                max_tokens=values.get("max_tokens"),
                system_message=values.get("supervisor_prompt"),
            )

        return values

    def add_worker(self, name: str, agent: Agent) -> None:
        """Add a worker agent.

        Args:
            name: Unique name for the worker
            agent: Worker agent instance

        Raises:
            ValueError: If worker name already exists
        """
        if name in self.workers:
            raise ValueError(f"Worker '{name}' already exists")

        self.workers[name] = agent
        logger.info(f"Added worker '{name}' to supervisor '{self.name}'")

    def remove_worker(self, name: str) -> Agent | None:
        """Remove a worker agent.

        Args:
            name: Name of worker to remove

        Returns:
            Removed agent or None if not found
        """
        return self.workers.pop(name, None)

    def list_workers(self) -> list[str]:
        """List all worker names."""
        return list(self.workers.keys())

    def get_worker(self, name: str) -> Agent | None:
        """Get a specific worker by name."""
        return self.workers.get(name)

    def setup_agent(self) -> None:
        """Setup supervisor with appropriate prompt."""
        if isinstance(self.engine, AugLLMConfig):
            self.engine.temperature = self.temperature
            if self.max_tokens:
                self.engine.max_tokens = self.max_tokens

            # Set supervisor prompt
            if not self.engine.system_message:
                self.engine.system_message = self._get_default_supervisor_prompt()

    def _get_default_supervisor_prompt(self) -> str:
        """Get default supervisor prompt."""
        worker_descriptions = "\n".join(
            [
                f"- {name}: {type(agent).__name__}"
                for name, agent in self.workers.items()
            ]
        )

        return f"""You are a supervisor agent coordinating a team of workers.

Your workers:
{worker_descriptions if worker_descriptions else "No workers assigned yet"}

Your responsibilities:
1. Analyze incoming requests
2. Decide which worker(s) should handle each task
3. Delegate tasks to appropriate workers
4. Synthesize results from workers
5. Provide comprehensive responses

Delegation strategy: {self.delegation_strategy}
Can respond directly: {self.allow_direct_response}

For each request, think about:
- What expertise is needed
- Which worker(s) are best suited
- How to combine multiple worker outputs
- Whether you need to handle it yourself"""

    def build_graph(self) -> BaseGraph:
        """Build supervisor delegation graph."""
        graph = BaseGraph(name=f"{self.name}_supervisor_graph")

        # Supervisor decision node
        supervisor_node = EngineNodeConfig(name="supervisor", engine=self.engine)
        graph.add_node("supervisor", supervisor_node)
        graph.add_edge(START, "supervisor")

        # Add worker nodes
        for worker_name, worker_agent in self.workers.items():
            # Create node for each worker
            worker_node = EngineNodeConfig(
                name=f"worker_{worker_name}",
                engine=(
                    worker_agent.engine
                    if hasattr(worker_agent, "engine")
                    else worker_agent
                ),
            )
            graph.add_node(f"worker_{worker_name}", worker_node)

        # Routing function
        def route_supervisor(state: dict[str, Any]) -> str:
            """Route based on supervisor decision."""
            messages = state.get("messages", [])
            if not messages:
                return "end"

            last_message = messages[-1]

            # Check delegation rounds
            delegations = sum(
                1
                for m in messages
                if isinstance(m, AIMessage)
                and "delegating to" in str(m.content).lower()
            )
            if delegations >= self.max_delegation_rounds:
                return "end"

            # Parse supervisor decision (in real implementation, use structured output)
            if isinstance(last_message, AIMessage):
                content = str(last_message.content).lower()

                # Check for delegation indicators
                for worker_name in self.workers:
                    if (
                        f"delegate to {worker_name}" in content
                        or f"asking {worker_name}" in content
                    ):
                        return f"worker_{worker_name}"

                # Check if supervisor is providing final answer
                if any(
                    phrase in content
                    for phrase in ["final answer", "in conclusion", "to summarize"]
                ):
                    return "end"

            # Default to end if no clear delegation
            return "end" if self.allow_direct_response else "supervisof"

        # Add conditional routing
        routes = {f"worker_{name}": f"worker_{name}" for name in self.workers}
        routes["end"] = END
        if not self.allow_direct_response and self.workers:
            routes["supervisor"] = "supervisor"  # Loop back if must delegate

        graph.add_conditional_edges("supervisor", route_supervisor, routes)

        # Workers report back to supervisor
        for worker_name in self.workers:
            graph.add_edge(f"worker_{worker_name}", "supervisor")

        return graph

    def __repr__(self) -> str:
        """String representation with worker info."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        worker_names = list(self.workers.keys())
        return f"SupervisorAgent[{engine_type}](name='{self.name}', workers={worker_names})"


# Example usage
if __name__ == "__main__":
    # Mock worker agents for demo
    class MockWorker:
        def __init__(self, name: str, specialty: str):
            self.name = name
            self.specialty = specialty
            self.engine = AugLLMConfig()

        async def arun(self, input_data: str) -> str:
            return f"{self.name} ({self.specialty}): Processed '{input_data}'"

    # Create supervisor with workers
    supervisor = SupervisorAgent(
        name="project_manager",
        temperature=0.3,  # Low temperature for decisions
        delegation_strategy="best",
        workers={
            "analyst": MockWorker("Alice", "Data Analysis"),
            "developer": MockWorker("Bob", "Software Development"),
            "designer": MockWorker("Carol", "UI/UX Design"),
        },
    )

    print(f"Created: {supervisor}")
    print(f"Workers: {supervisor.list_workers()}")
    print(f"Delegation strategy: {supervisor.delegation_strategy}")

    # Add another worker dynamically
    supervisor.add_worker("tester", MockWorker("Dave", "Quality Assurance"))
    print(f"Updated workers: {supervisor.list_workers()}")

    # Example delegation scenarios
    print("\nExample delegation scenarios:")
    print("1. 'Analyze user engagement metrics' -> delegate to analyst")
    print("2. 'Build a REST API' -> delegate to developer")
    print("3. 'Create mockups for mobile app' -> delegate to designer")
    print("4. 'Test the new features' -> delegate to tester")
    print("5. 'Plan the project timeline' -> supervisor handles directly")
