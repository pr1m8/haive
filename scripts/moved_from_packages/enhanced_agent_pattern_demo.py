#!/usr/bin/env python3
"""Enhanced Agent Pattern Demo - Shows the engine-focused generic pattern.

This example demonstrates:
1. The enhanced agent pattern: Agent[EngineT]
2. How SimpleAgent is just Agent[AugLLMConfig]
3. How different engine types create different agent types
4. The clean type safety this provides
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

# ========================================================================
# MOCK ENGINE TYPES (in real code, import from haive.core.engine)
# ========================================================================


class Engine:
    """Base engine type."""


class AugLLMConfig(Engine):
    """Standard LLM engine with augmentations."""

    def __init__(self, temperature: float = 0.7):
        self.temperature = temperature


class RetrieverEngine(Engine):
    """Engine that includes retrieval capabilities."""

    def __init__(self, index_name: str):
        self.index_name = index_name


class ReasoningEngine(Engine):
    """Engine with enhanced reasoning capabilities."""

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations


class MultiModalEngine(Engine):
    """Engine that handles text, images, audio."""

    def __init__(self, modalities: list[str]):
        self.modalities = modalities


# ========================================================================
# ENHANCED AGENT PATTERN
# ========================================================================

# Engine-focused generic type
EngineT = TypeVar("EngineT", bound=Engine)


class Workflow(ABC):
    """Pure workflow orchestration without engine dependencies.

    Workflow handles pure orchestration - routing, transformation,
    coordination - without requiring engines.
    """

    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the workflow logic."""


class Agent(Workflow, Generic[EngineT]):
    """Enhanced Agent with engine-focused generics.

    Agent = Workflow + Engine. The engine type is the primary generic parameter,
    enabling type-safe engine-specific functionality.

    Key Benefits:
    - Engine-specific type safety: Agent[AugLLMConfig] vs Agent[RetrieverEngine]
    - Engine determines capabilities
    - Clean separation of concerns
    """

    def __init__(self, name: str, engine: EngineT):
        self.name = name
        self.engine = engine
        self.history: list[dict[str, Any]] = []

    async def execute(self, input_data: Any) -> Any:
        """Execute using the engine."""
        # Log the execution
        self.history.append(
            {"input": input_data, "engine_type": type(self.engine).__name__}
        )

        # In real implementation, this would use the engine
        result = (
            f"{self.name} processed '{input_data}' using {type(self.engine).__name__}"
        )

        self.history[-1]["output"] = result
        return result

    def get_engine(self) -> EngineT:
        """Get the engine with proper typing."""
        return self.engine

    def __repr__(self) -> str:
        engine_type = type(self.engine).__name__
        return f"{self.__class__.__name__}[{engine_type}](name='{self.name}')"


# ========================================================================
# AGENT IMPLEMENTATIONS - Just Agent[SpecificEngine]!
# ========================================================================


class SimpleAgent(Agent[AugLLMConfig]):
    """SimpleAgent is just Agent[AugLLMConfig].

    That's it! SimpleAgent is nothing more than an Agent with its engine
    type locked to AugLLMConfig. All behavior comes from the base Agent
    and the engine type.
    """


class RAGAgent(Agent[RetrieverEngine]):
    """RAGAgent is just Agent[RetrieverEngine].

    The RetrieverEngine type provides retrieval capabilities.
    """

    async def retrieve(self, query: str) -> list[str]:
        """Retrieve relevant documents - available because engine is RetrieverEngine."""
        # Type-safe access to retriever-specific features
        return [f"Retrieved from {self.engine.index_name}: Doc about {query}"]


class ReasoningAgent(Agent[ReasoningEngine]):
    """ReasoningAgent is just Agent[ReasoningEngine].

    The ReasoningEngine provides iterative reasoning capabilities.
    """

    async def reason(self, problem: str) -> str:
        """Multi-step reasoning - available because engine is ReasoningEngine."""
        steps = []
        for i in range(self.engine.max_iterations):
            steps.append(f"Step {i + 1}: Analyzing {problem}")
        return " -> ".join(steps)


class MultiModalAgent(Agent[MultiModalEngine]):
    """MultiModalAgent is just Agent[MultiModalEngine].

    Handles multiple modalities based on engine capabilities.
    """

    def supported_modalities(self) -> list[str]:
        """Get supported modalities from engine."""
        return self.engine.modalities


# ========================================================================
# MULTI-AGENT PATTERN (Agent that contains other agents)
# ========================================================================


@dataclass
class AgentRef:
    """Reference to an agent with its type."""

    name: str
    agent_type: str


class MultiAgent(Agent[AugLLMConfig]):
    """MultiAgent coordinates multiple agents.

    Note: MultiAgent itself is Agent[AugLLMConfig] because it uses
    an LLM to coordinate. The agents it coordinates can be any type.
    """

    def __init__(self, name: str, engine: AugLLMConfig, agents: dict[str, Agent[Any]]):
        super().__init__(name, engine)
        self.agents = agents

    async def execute(self, input_data: Any) -> Any:
        """Coordinate multiple agents."""
        # Use LLM to decide which agent to use
        decision = f"Routing '{input_data}' to appropriate agent..."

        # For demo, just use all agents
        results = {}
        for agent_name, agent in self.agents.items():
            results[agent_name] = await agent.execute(input_data)

        return {"coordinator": self.name, "decision": decision, "results": results}

    def list_agents(self) -> list[AgentRef]:
        """List all coordinated agents with their types."""
        return [
            AgentRef(name=name, agent_type=repr(agent))
            for name, agent in self.agents.items()
        ]


# ========================================================================
# DEMONSTRATION
# ========================================================================


async def main():
    """Demonstrate the enhanced agent pattern."""
    # 1. SimpleAgent = Agent[AugLLMConfig]
    simple = SimpleAgent(name="assistant", engine=AugLLMConfig(temperature=0.7))
    result = await simple.execute("Hello world")

    # 2. RAGAgent = Agent[RetrieverEngine]
    rag = RAGAgent(
        name="researcher", engine=RetrieverEngine(index_name="knowledge_base")
    )
    await rag.retrieve("Python programming")
    result = await rag.execute("Find information about Python")

    # 3. ReasoningAgent = Agent[ReasoningEngine]
    reasoner = ReasoningAgent(name="thinker", engine=ReasoningEngine(max_iterations=3))
    await reasoner.reason("How to solve world hunger")

    # 4. MultiModalAgent = Agent[MultiModalEngine]
    MultiModalAgent(
        name="vision", engine=MultiModalEngine(modalities=["text", "image", "audio"])
    )

    # 5. MultiAgent coordinating others
    coordinator = MultiAgent(
        name="coordinator",
        engine=AugLLMConfig(temperature=0.3),  # Low temp for coordination
        agents={"simple": simple, "rag": rag, "reasoner": reasoner},
    )
    for _agent_ref in coordinator.list_agents():
        pass

    result = await coordinator.execute("Explain quantum computing")
    for _agent_name, _agent_result in result["results"].items():
        pass

    # 6. Type safety demonstration


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
