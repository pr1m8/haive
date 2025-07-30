"""Enhanced_Multi_Agent_Standalone core module.

This module provides enhanced multi agent standalone functionality for the Haive framework.

Classes:
    MinimalEngine: MinimalEngine implementation.
    Agent: Agent implementation.
    SimpleAgent: SimpleAgent implementation.

Functions:
    arun: Arun functionality.
    run: Run functionality.
    arun: Arun functionality.
"""

#!/usr/bin/env python3
"""Standalone Enhanced MultiAgent Implementation - Fully Working.

This is a complete, working implementation of the enhanced multi-agent pattern
that avoids import issues and demonstrates all the core concepts:

- MultiAgent[AgentsT] - Generic on the agents it contains
- Sequential, Parallel, Branching, Conditional, Adaptive patterns
- Real async execution with debug output
- Type safety through generics
- No problematic imports

Key Insight: MultiAgent is generic on its agents, not just engine!
MultiAgent[AgentsT] = Agent[AugLLMConfig] + agents: AgentsT
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

# Generic type for agents contained in MultiAgent
AgentsT = TypeVar("AgentsT", bound=dict[str, "Agent"] | list["Agent"])


# Minimal base classes to avoid import issues
class MinimalEngine(BaseModel):
    """Minimal engine for demonstration."""

    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_message: str | None = Field(default=None)


class Agent(BaseModel, ABC):
    """Enhanced Agent base class - Agent[EngineT] pattern."""

    name: str = Field(...)
    engine: Any = Field(default_factory=MinimalEngine)

    @abstractmethod
    async def arun(self, input_data: str, debug: bool = False) -> str:
        """Async execution method."""

    def run(self, input_data: str, debug: bool = False) -> str:
        """Sync execution method."""
        return asyncio.run(self.arun(input_data, debug))


class SimpleAgent(Agent):
    """SimpleAgent = Agent[AugLLMConfig] - minimal working implementation."""

    async def arun(self, input_data: str, debug: bool = False) -> str:
        """Async run with realistic simulation."""
        if debug:
            pass

        # Simulate different agent behaviors based on name
        await asyncio.sleep(0.1)  # Simulate processing time

        if "planner" in self.name.lower():
            result = f"PLAN: {input_data} -> 1. Analyze requirements, 2. Design solution, 3. Create timeline"
        elif "executor" in self.name.lower():
            result = f"EXECUTED: {input_data} -> Implementation completed successfully"
        elif "reviewer" in self.name.lower():
            result = (
                f"REVIEW: {input_data} -> Quality check passed, ready for deployment"
            )
        elif "technical" in self.name.lower():
            result = f"TECHNICAL: {input_data} -> Technical analysis complete with recommendations"
        elif "business" in self.name.lower():
            result = f"BUSINESS: {input_data} -> Business impact assessment completed"
        elif "fast" in self.name.lower():
            result = f"FAST: {input_data} -> Quick analysis completed"
        elif "accurate" in self.name.lower():
            await asyncio.sleep(0.2)  # Slower but more accurate
            result = f"ACCURATE: {input_data} -> Detailed analysis with high confidence"
        elif "validator" in self.name.lower():
            if "invalid" in input_data.lower():
                result = f"VALIDATOR: Error - {input_data} contains invalid elements"
            else:
                result = f"VALIDATOR: {input_data} -> Validation passed"
        elif "processor" in self.name.lower():
            result = f"PROCESSOR: {input_data} -> Processing completed successfully"
        elif "error_handler" in self.name.lower():
            result = f"ERROR_HANDLER: {input_data} -> Error handled and resolved"
        else:
            result = f"{self.name.upper()}: {input_data} -> Processing completed"

        if debug:
            pass

        return result


class MultiAgent(Agent, Generic[AgentsT]):
    """Enhanced MultiAgent generic on the agents it contains.

    MultiAgent[AgentsT] = Agent[AugLLMConfig] + agents: AgentsT

    This properly represents that MultiAgent is:
    1. An agent itself (uses engine for coordination)
    2. Generic on the agents it contains

    Examples:
        Sequential pipeline::

            agents = [planner, executor, reviewer]
            multi: MultiAgent[List[SimpleAgent]] = MultiAgent(
                name="pipeline",
                agents=agents,
                mode="sequential"
            )

        Branching router::

            agents = {"technical": tech_agent, "business": biz_agent}
            multi: MultiAgent[Dict[str, SimpleAgent]] = MultiAgent(
                name="router",
                agents=agents,
                mode="branch"
            )
    """

    # The agents this MultiAgent coordinates (generic)
    agents: AgentsT = Field(..., description="Agents to coordinate - generic type")

    # Execution mode
    mode: Literal["sequential", "parallel", "conditional", "branch"] = Field(
        default="sequential", description="Execution mode for agents"
    )

    # Coordination configuration
    max_iterations: int = Field(default=10)
    branch_map: dict[str, str] | None = Field(default=None)

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: AgentsT) -> AgentsT:
        """Validate agents based on type."""
        if isinstance(v, dict):
            if not v:
                raise ValueError("Agent dict cannot be empty")
        elif isinstance(v, list):
            if not v:
                raise ValueError("Agent list cannot be empty")
        else:
            raise ValueError("Agents must be dict or list")
        return v

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        if isinstance(self.agents, dict):
            return list(self.agents.keys())
        return [f"agent_{i}" for i in range(len(self.agents))]

    def get_agent(self, name: str) -> Agent | None:
        """Get agent by name."""
        if isinstance(self.agents, dict):
            return self.agents.get(name)
        # Handle list case
        if name.startswith("agent_"):
            try:
                idx = int(name.split("_")[1])
                return self.agents[idx] if idx < len(self.agents) else None
            except (IndexError, ValueError):
                return None
        return None

    async def arun(self, input_data: str, debug: bool = False) -> str:
        """Execute based on mode."""
        if self.mode == "sequential":
            return await self._execute_sequential(input_data, debug)
        if self.mode == "parallel":
            return await self._execute_parallel(input_data, debug)
        if self.mode == "branch":
            return await self._execute_branching(input_data, debug)
        if self.mode == "conditional":
            return await self._execute_conditional(input_data, debug)
        raise ValueError(f"Unsupported mode: {self.mode}")

    async def _execute_sequential(self, input_data: str, debug: bool = False) -> str:
        """Execute agents in sequence."""
        if debug:
            pass

        current_input = input_data
        results = []

        agents = (
            list(self.agents)
            if isinstance(self.agents, list)
            else list(self.agents.values())
        )

        for _i, agent in enumerate(agents):
            if debug:
                pass

            result = await agent.arun(current_input, debug=False)
            results.append(result)
            current_input = result  # Chain outputs

            if debug:
                pass

        final_result = f"Sequential execution complete. Final: {results[-1]}"

        if debug:
            pass

        return final_result

    async def _execute_parallel(self, input_data: str, debug: bool = False) -> str:
        """Execute all agents in parallel."""
        if debug:
            pass

        agents = (
            list(self.agents)
            if isinstance(self.agents, list)
            else list(self.agents.values())
        )

        # Create tasks for parallel execution
        tasks = [agent.arun(input_data, debug=False) for agent in agents]

        # Execute in parallel
        results = await asyncio.gather(*tasks)

        if debug:
            for _agent, _result in zip(agents, results, strict=False):
                pass

        return f"Parallel execution complete. {len(results)} agents executed."

    async def _execute_branching(self, input_data: str, debug: bool = False) -> str:
        """Execute with intelligent routing."""
        if debug:
            pass

        # Route based on content
        route = self._route_request(input_data)

        if debug:
            pass

        # Execute selected agent
        selected_agent = self.get_agent(route)
        if not selected_agent:
            return f"Error: Agent '{route}' not found"

        result = await selected_agent.arun(input_data, debug=False)

        final_result = f"[Routed to {route}] {result}"

        if debug:
            pass

        return final_result

    def _route_request(self, input_data: str) -> str:
        """Route request to appropriate agent based on content."""
        content = input_data.lower()

        if not isinstance(self.agents, dict):
            return "agent_0"  # Default for list

        # Simple keyword-based routing
        if any(
            keyword in content
            for keyword in ["technical", "code", "system", "api", "debug"]
        ):
            return (
                "technical"
                if "technical" in self.agents
                else next(iter(self.agents.keys()))
            )
        if any(
            keyword in content
            for keyword in ["business", "profit", "market", "revenue"]
        ):
            return (
                "business"
                if "business" in self.agents
                else next(iter(self.agents.keys()))
            )
        if any(keyword in content for keyword in ["validate", "check", "verify"]):
            return (
                "validator"
                if "validator" in self.agents
                else next(iter(self.agents.keys()))
            )
        return "general" if "general" in self.agents else next(iter(self.agents.keys()))

    async def _execute_conditional(self, input_data: str, debug: bool = False) -> str:
        """Execute with conditional flow."""
        if debug:
            pass

        # Simple conditional logic: validator -> processor/error_handler
        current_input = input_data
        execution_path = []

        # Start with validator if available
        current_agent_name = "validator"
        if isinstance(self.agents, dict) and "validator" in self.agents:
            current_agent = self.agents["validator"]
        else:
            # Use first agent
            agents_list = (
                list(self.agents)
                if isinstance(self.agents, list)
                else list(self.agents.values())
            )
            current_agent = agents_list[0]
            current_agent_name = current_agent.name

        max_iterations = 3
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            if debug:
                pass

            result = await current_agent.arun(current_input, debug=False)
            execution_path.append(current_agent_name)

            if debug:
                pass

            # Determine next agent based on result
            if "error" in result.lower() or "invalid" in result.lower():
                next_agent_name = "error_handler"
            elif current_agent_name == "validator":
                next_agent_name = "processor"
            else:
                next_agent_name = "end"

            if debug:
                pass

            if next_agent_name == "end":
                break

            # Get next agent
            if isinstance(self.agents, dict) and next_agent_name in self.agents:
                current_agent = self.agents[next_agent_name]
                current_agent_name = next_agent_name
                current_input = result
            else:
                break

        final_result = (
            f"Conditional execution path: {' → '.join(execution_path)}. Final: {result}"
        )

        if debug:
            pass

        return final_result

    def __repr__(self) -> str:
        """String representation."""
        agent_count = len(self.agents)
        agents_type = type(self.agents).__name__

        return (
            f"MultiAgent[{agents_type}]("
            f"name='{self.name}', "
            f"agents={agent_count}, "
            f"mode='{self.mode}')"
        )


# Specialized MultiAgent variants


class BranchingMultiAgent(MultiAgent[dict[str, Agent]]):
    """MultiAgent specialized for branching execution."""

    mode: Literal["branch"] = Field(default="branch")

    def __init__(self, name: str, agents: dict[str, Agent], **kwargs):
        super().__init__(name=name, agents=agents, mode="branch", **kwargs)


class AdaptiveBranchingMultiAgent(BranchingMultiAgent):
    """Branching MultiAgent that adapts routing based on performance."""

    # Performance tracking
    agent_performance: dict[str, dict[str, float]] = Field(default_factory=dict)
    adaptation_rate: float = Field(default=0.1, ge=0.0, le=1.0)

    def __init__(self, name: str, agents: dict[str, Agent], **kwargs):
        super().__init__(name=name, agents=agents, **kwargs)

        # Initialize performance tracking
        for agent_name in agents:
            self.agent_performance[agent_name] = {
                "success_rate": 0.5,
                "avg_duration": 1.0,
                "task_count": 0,
            }

    def update_performance(
        self, agent_name: str, success: bool, duration: float
    ) -> None:
        """Update agent performance metrics."""
        if agent_name not in self.agent_performance:
            return

        metrics = self.agent_performance[agent_name]
        metrics["task_count"] += 1

        # Update success rate with exponential moving average
        current_rate = metrics["success_rate"]
        new_rate = (
            current_rate * (1 - self.adaptation_rate)
            + (1.0 if success else 0.0) * self.adaptation_rate
        )
        metrics["success_rate"] = new_rate

        # Update average duration
        metrics["avg_duration"] = (
            metrics["avg_duration"] * (metrics["task_count"] - 1) + duration
        ) / metrics["task_count"]

    def get_best_agent_for_task(self, task_type: str = "general") -> str:
        """Get best performing agent."""
        best_agent = None
        best_score = 0.0

        for agent_name, metrics in self.agent_performance.items():
            # Score = success_rate / avg_duration (higher is better)
            score = metrics["success_rate"] / max(metrics["avg_duration"], 0.1)
            if score > best_score:
                best_score = score
                best_agent = agent_name

        return best_agent or next(iter(self.agents.keys()))

    async def _execute_branching(self, input_data: str, debug: bool = False) -> str:
        """Execute with adaptive agent selection."""
        if debug:
            pass

        # Select best agent based on performance
        selected_agent_name = self.get_best_agent_for_task()
        selected_agent = self.agents[selected_agent_name]

        if debug:
            self.agent_performance[selected_agent_name]

        # Execute with timing
        start_time = time.time()
        try:
            result = await selected_agent.arun(input_data, debug=False)
            success = True
        except Exception:
            result = f"Error in {selected_agent_name}"
            success = False

        duration = time.time() - start_time

        # Update performance
        self.update_performance(selected_agent_name, success, duration)

        final_result = f"[Adaptive: {selected_agent_name}] {result}"

        if debug:
            pass

        return final_result


# Demonstration and testing
async def demo_enhanced_multi_agent():
    """Demonstrate all enhanced multi-agent patterns."""
    # 1. Sequential Pattern

    planner = SimpleAgent(name="planner", engine=MinimalEngine(temperature=0.3))
    executor = SimpleAgent(name="executor", engine=MinimalEngine(temperature=0.5))
    reviewer = SimpleAgent(name="reviewer", engine=MinimalEngine(temperature=0.1))

    sequential: MultiAgent[list[SimpleAgent]] = MultiAgent(
        name="project_pipeline", agents=[planner, executor, reviewer], mode="sequential"
    )

    await sequential.arun("Build a user authentication system", debug=True)

    # 2. Parallel Pattern

    tech_expert = SimpleAgent(
        name="technical_expert", engine=MinimalEngine(temperature=0.1)
    )
    biz_expert = SimpleAgent(
        name="business_expert", engine=MinimalEngine(temperature=0.7)
    )
    user_expert = SimpleAgent(name="user_expert", engine=MinimalEngine(temperature=0.5))

    parallel: MultiAgent[list[SimpleAgent]] = MultiAgent(
        name="expert_panel",
        agents=[tech_expert, biz_expert, user_expert],
        mode="parallel",
    )

    await parallel.arun("Evaluate the new AI feature proposal", debug=True)

    # 3. Branching Pattern

    tech_agent = SimpleAgent(
        name="technical_specialist", engine=MinimalEngine(temperature=0.1)
    )
    biz_agent = SimpleAgent(
        name="business_analyst", engine=MinimalEngine(temperature=0.5)
    )
    general_agent = SimpleAgent(
        name="general_assistant", engine=MinimalEngine(temperature=0.7)
    )

    branching: BranchingMultiAgent = BranchingMultiAgent(
        name="smart_router",
        agents={
            "technical": tech_agent,
            "business": biz_agent,
            "general": general_agent,
        },
    )

    # Test different routing scenarios
    test_queries = [
        "Help me debug this API integration issue",
        "Analyze the market potential for this product",
        "What's the weather like today?",
    ]

    for query in test_queries:
        await branching.arun(query, debug=True)

    # 4. Adaptive Pattern

    fast_agent = SimpleAgent(
        name="fast_responder", engine=MinimalEngine(temperature=0.1)
    )
    accurate_agent = SimpleAgent(
        name="accurate_analyzer", engine=MinimalEngine(temperature=0.9)
    )
    balanced_agent = SimpleAgent(
        name="balanced_processor", engine=MinimalEngine(temperature=0.5)
    )

    adaptive: AdaptiveBranchingMultiAgent = AdaptiveBranchingMultiAgent(
        name="adaptive_system",
        agents={
            "fast": fast_agent,
            "accurate": accurate_agent,
            "balanced": balanced_agent,
        },
        adaptation_rate=0.2,
    )

    # Simulate multiple requests to see adaptation
    tasks = [
        "Process urgent request 1",
        "Analyze complex data set",
        "Handle routine task",
        "Process urgent request 2",
    ]

    for _i, task in enumerate(tasks):
        await adaptive.arun(task, debug=True)

        # Show performance evolution
        for _agent_name, _metrics in adaptive.agent_performance.items():
            pass

    # 5. Conditional Pattern

    validator = SimpleAgent(name="validator", engine=MinimalEngine(temperature=0.1))
    processor = SimpleAgent(name="processor", engine=MinimalEngine(temperature=0.5))
    error_handler = SimpleAgent(
        name="error_handler", engine=MinimalEngine(temperature=0.7)
    )

    conditional: MultiAgent[dict[str, SimpleAgent]] = MultiAgent(
        name="workflow_engine",
        agents={
            "validator": validator,
            "processor": processor,
            "error_handler": error_handler,
        },
        mode="conditional",
    )

    # Test success and error paths
    test_cases = ["Valid data to process", "Invalid data input"]

    for test_case in test_cases:
        await conditional.arun(test_case, debug=True)


if __name__ == "__main__":
    # Run the complete demonstration
    asyncio.run(demo_enhanced_multi_agent())
