#!/usr/bin/env python
"""Advanced test case with prebuilt agents - some active, some inactive.

This test demonstrates:
1. A pool of prebuilt agents with different capabilities
2. Dynamic activation/deactivation based on needs
3. Performance tracking and agent selection
4. Real-world agent coordination scenarios
"""

import asyncio
import logging
import random
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    """Agent status in the pool."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AgentMetrics(BaseModel):
    """Performance metrics for an agent."""

    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    average_response_time: float = 0.0
    last_used: datetime | None = None
    error_rate: float = 0.0
    specialization_score: dict[str, float] = Field(default_factory=dict)


class PrebuiltAgent:
    """A sophisticated prebuilt agent with capabilities and metrics."""

    def __init__(
        self,
        name: str,
        capabilities: list[str],
        specialization: str,
        initial_status: AgentStatus = AgentStatus.INACTIVE,
        resource_cost: int = 1,
        max_concurrent: int = 1,
    ):
        self.name = name
        self.capabilities = capabilities
        self.specialization = specialization
        self.status = initial_status
        self.resource_cost = resource_cost
        self.max_concurrent = max_concurrent
        self.current_tasks = 0
        self.metrics = AgentMetrics()

        # Simulate different response times for different agents
        self.base_response_time = random.uniform(0.1, 0.5)

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process request with simulated work."""
        start_time = datetime.now()

        if self.status != AgentStatus.ACTIVE:
            raise RuntimeError(
                f"Agent {self.name} is not active (status: {self.status})"
            )

        if self.current_tasks >= self.max_concurrent:
            raise RuntimeError(f"Agent {self.name} at max capacity")

        self.current_tasks += 1
        self.metrics.total_calls += 1

        try:
            # Simulate processing time
            await asyncio.sleep(self.base_response_time)

            messages = state.get("messages", [])
            last_message = messages[-1] if messages else None

            # Generate specialized response based on capabilities
            response_content = self._generate_response(last_message)

            # Simulate occasional errors for realism
            if random.random() < 0.05:  # 5% error rate
                raise Exception("Simulated processing error")

            response = AIMessage(
                content=response_content,
                additional_kwargs={
                    "agent": self.name,
                    "specialization": self.specialization,
                    "capabilities_used": self._determine_used_capabilities(
                        last_message
                    ),
                },
            )

            self.metrics.successful_calls += 1

            # Update metrics
            elapsed = (datetime.now() - start_time).total_seconds()
            self._update_metrics(elapsed, success=True)

            return {"messages": [*messages, response]}

        except Exception:
            self.metrics.failed_calls += 1
            self._update_metrics(0, success=False)
            raise
        finally:
            self.current_tasks -= 1

    def _generate_response(self, message) -> str:
        """Generate a response based on agent specialization."""
        content = getattr(message, "content", "") if message else ""

        responses = {
            "research": f"📚 Research Agent ({self.name}): Found {random.randint(5, 20)} relevant sources. Key findings: {content[:50]}...",
            "analysis": f"📊 Analysis Agent ({self.name}): Processed data with {random.choice(['statistical', 'ML', 'heuristic'])} methods. Confidence: {random.randint(75, 95)}%",
            "writing": f"✍️ Writing Agent ({self.name}): Composed {random.choice(['technical', 'creative', 'formal'])} content. Style: {random.choice(['professional', 'casual', 'academic'])}",
            "coding": f"💻 Coding Agent ({self.name}): Generated {random.randint(10, 100)} lines of {random.choice(['Python', 'JavaScript', 'SQL'])} code",
            "planning": f"📋 Planning Agent ({self.name}): Created {random.randint(3, 7)}-step plan with {random.choice(['sequential', 'parallel', 'hybrid'])} execution",
            "qa": f"✅ QA Agent ({self.name}): Validated with {random.randint(5, 15)} test cases. Coverage: {random.randint(80, 99)}%",
            "translation": f"🌐 Translation Agent ({self.name}): Translated to {random.choice(['Spanish', 'French', 'German', 'Chinese'])} with {random.randint(90, 99)}% accuracy",
            "summarization": f"📝 Summarization Agent ({self.name}): Condensed {random.randint(500, 2000)} words to {random.randint(50, 200)} words",
        }

        return responses.get(
            self.specialization,
            f"🤖 {self.name}: Processed request using {self.specialization}",
        )

    def _determine_used_capabilities(self, message) -> list[str]:
        """Determine which capabilities were used."""
        if not message:
            return []

        content = getattr(message, "content", "").lower()
        used = []

        for capability in self.capabilities:
            if any(keyword in content for keyword in capability.lower().split()):
                used.append(capability)

        return used[:3]  # Return top 3 used

    def _update_metrics(self, elapsed_time: float, success: bool):
        """Update agent metrics."""
        self.metrics.last_used = datetime.now()

        if success and elapsed_time > 0:
            # Update average response time
            total_time = self.metrics.average_response_time * (
                self.metrics.successful_calls - 1
            )
            self.metrics.average_response_time = (
                total_time + elapsed_time
            ) / self.metrics.successful_calls

        # Update error rate
        if self.metrics.total_calls > 0:
            self.metrics.error_rate = (
                self.metrics.failed_calls / self.metrics.total_calls
            )

    def can_handle(self, request_type: str) -> float:
        """Return confidence score (0-1) for handling request type."""
        request_lower = request_type.lower()

        # Check direct capability match
        for capability in self.capabilities:
            if (
                capability.lower() in request_lower
                or request_lower in capability.lower()
            ):
                return 0.9

        # Check specialization match
        if self.specialization.lower() in request_lower:
            return 0.8

        # Partial matches
        capability_keywords = [
            word for cap in self.capabilities for word in cap.lower().split()
        ]
        matches = sum(1 for keyword in capability_keywords if keyword in request_lower)

        return min(0.7, matches * 0.2)


class AgentPool:
    """Manages a pool of prebuilt agents."""

    def __init__(self, resource_limit: int = 10):
        self.agents: dict[str, PrebuiltAgent] = {}
        self.resource_limit = resource_limit
        self.current_resource_usage = 0

    def add_agent(self, agent: PrebuiltAgent):
        """Add agent to pool."""
        self.agents[agent.name] = agent
        logger.info(f"Added {agent.name} to pool (status: {agent.status})")

    def activate_agent(self, agent_name: str) -> bool:
        """Activate an agent if resources allow."""
        agent = self.agents.get(agent_name)
        if not agent:
            return False

        if agent.status == AgentStatus.ACTIVE:
            return True

        if self.current_resource_usage + agent.resource_cost > self.resource_limit:
            logger.warning(f"Cannot activate {agent_name}: insufficient resources")
            return False

        agent.status = AgentStatus.ACTIVE
        self.current_resource_usage += agent.resource_cost
        logger.info(
            f"Activated {agent_name} (resources: {self.current_resource_usage}/{self.resource_limit})"
        )
        return True

    def deactivate_agent(self, agent_name: str) -> bool:
        """Deactivate an agent."""
        agent = self.agents.get(agent_name)
        if not agent or agent.status != AgentStatus.ACTIVE:
            return False

        agent.status = AgentStatus.INACTIVE
        self.current_resource_usage -= agent.resource_cost
        logger.info(
            f"Deactivated {agent_name} (resources: {self.current_resource_usage}/{self.resource_limit})"
        )
        return True

    def get_active_agents(self) -> list[PrebuiltAgent]:
        """Get all active agents."""
        return [
            agent
            for agent in self.agents.values()
            if agent.status == AgentStatus.ACTIVE
        ]

    def get_best_agent_for_task(self, task_description: str) -> PrebuiltAgent | None:
        """Find best active agent for a task."""
        active_agents = self.get_active_agents()
        if not active_agents:
            return None

        # Score each agent
        agent_scores = []
        for agent in active_agents:
            if agent.current_tasks >= agent.max_concurrent:
                continue

            score = agent.can_handle(task_description)

            # Adjust score based on performance
            if agent.metrics.total_calls > 0:
                performance_multiplier = (1 - agent.metrics.error_rate) * 0.5 + 0.5
                score *= performance_multiplier

            agent_scores.append((agent, score))

        if not agent_scores:
            return None

        # Return highest scoring agent
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        return agent_scores[0][0] if agent_scores[0][1] > 0.3 else None


async def create_prebuilt_agent_pool() -> AgentPool:
    """Create a pool of diverse prebuilt agents."""
    pool = AgentPool(resource_limit=10)

    # Research agents
    pool.add_agent(
        PrebuiltAgent(
            "research_alpha",
            ["web search", "academic papers", "fact checking"],
            "research",
            initial_status=AgentStatus.ACTIVE,
            resource_cost=2,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "research_beta",
            ["market research", "competitor analysis", "trend analysis"],
            "research",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=2,
        )
    )

    # Analysis agents
    pool.add_agent(
        PrebuiltAgent(
            "analyst_prime",
            ["data analysis", "statistical modeling", "visualization"],
            "analysis",
            initial_status=AgentStatus.ACTIVE,
            resource_cost=3,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "analyst_secondary",
            ["sentiment analysis", "pattern recognition", "anomaly detection"],
            "analysis",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=2,
        )
    )

    # Writing agents
    pool.add_agent(
        PrebuiltAgent(
            "writer_creative",
            ["creative writing", "storytelling", "content generation"],
            "writing",
            initial_status=AgentStatus.ACTIVE,
            resource_cost=1,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "writer_technical",
            ["technical documentation", "API docs", "user guides"],
            "writing",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=1,
        )
    )

    # Coding agents
    pool.add_agent(
        PrebuiltAgent(
            "coder_senior",
            ["Python", "JavaScript", "system design", "code review"],
            "coding",
            initial_status=AgentStatus.ACTIVE,
            resource_cost=3,
            max_concurrent=2,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "coder_junior",
            ["Python", "bug fixing", "unit tests"],
            "coding",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=1,
        )
    )

    # Specialized agents
    pool.add_agent(
        PrebuiltAgent(
            "planner_strategic",
            ["project planning", "resource allocation", "timeline estimation"],
            "planning",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=2,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "qa_specialist",
            ["testing", "quality assurance", "test automation"],
            "qa",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=2,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "translator_multi",
            ["language translation", "localization", "cultural adaptation"],
            "translation",
            initial_status=AgentStatus.INACTIVE,
            resource_cost=1,
        )
    )

    pool.add_agent(
        PrebuiltAgent(
            "summarizer_expert",
            ["text summarization", "key point extraction", "abstract generation"],
            "summarization",
            initial_status=AgentStatus.ACTIVE,
            resource_cost=1,
        )
    )

    return pool


async def test_advanced_dynamic_supervisor():
    """Test advanced scenarios with prebuilt agent pool."""

    # Import the fixed supervisor
    try:
        from dynamic_supervisor_fixed import DynamicSupervisorFixed
    except ImportError:
        return False

    # Create agent pool
    pool = await create_prebuilt_agent_pool()


    active_names = [agent.name for agent in pool.get_active_agents()]

    # Create supervisor
    supervisor = DynamicSupervisorFixed(
        name="advanced_supervisor", auto_rebuild_graph=True
    )

    # Register only active agents initially
    for agent in pool.get_active_agents():
        supervisor.register_agent(
            agent, f"{agent.specialization}: {', '.join(agent.capabilities)}"
        )


    # Test 1: Basic routing to specialized agents

    test_requests = [
        "Research the latest AI developments",
        "Analyze this data for patterns",
        "Write a creative story about robots",
        "Create a Python function for sorting",
        "Summarize this long document",
    ]

    for request in test_requests:

        # Find best agent
        best_agent = pool.get_best_agent_for_task(request)
        if best_agent:
            pass

        try:
            result = await supervisor.ainvoke(
                {"messages": [HumanMessage(content=request)]}
            )
            response = (
                result.get("messages", [])[-1] if result.get("messages") else None
            )

            if response:
                if hasattr(response, "additional_kwargs"):
                    agent_used = response.additional_kwargs.get("agent", "unknown")
        except Exception as e:
            pass")

    # Test 2: Dynamic activation based on demand

    # Request requiring technical writing (not currently active)

    # Activate technical writer
    if pool.activate_agent("writer_technical"):
        technical_writer = pool.agents["writer_technical"]
        supervisor.register_agent(technical_writer, "Technical writing specialist")

    # Now test the request
    result = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(content="Write technical documentation for our API")
            ]
        }
    )

    # Test 3: Resource management and agent swapping


    # Try to activate a high-cost agent (should fail due to resources)
    if not pool.activate_agent("planner_strategic"):

        # Deactivate a lower-priority agent
        pool.deactivate_agent("summarizer_expert")
        supervisor.unregister_agent("summarizer_expert")

        # Try again
        if pool.activate_agent("planner_strategic"):
            planner = pool.agents["planner_strategic"]
            supervisor.register_agent(planner, "Strategic planning")

    # Test planning request
    result = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Create a project plan for launching a new product"
                )
            ]
        }
    )

    # Test 4: Performance-based agent selection

    # Simulate multiple requests to build performance metrics

    requests = [
        "Analyze sales data from Q4",
        "Research competitor strategies",
        "Write a blog post about AI",
        "Debug this Python code",
        "Analyze customer feedback",
    ] * 3  # Repeat to build metrics

    for i, request in enumerate(requests):
        try:
            await supervisor.ainvoke({"messages": [HumanMessage(content=request)]})
            if i % 5 == 0:
                pass
        except:
            pass  # Some may fail randomly

    # Display performance metrics
    for agent in pool.get_active_agents():
        if agent.metrics.total_calls > 0:

    # Test 5: Complex multi-agent workflow

    # Activate QA specialist for comprehensive workflow
    if pool.current_resource_usage + 2 <= pool.resource_limit:
        pool.activate_agent("qa_specialist")
        qa_agent = pool.agents["qa_specialist"]
        supervisor.register_agent(qa_agent, "Quality assurance")

    complex_request = """
    I need a comprehensive solution:
    1. Research best practices for Python web APIs
    2. Write code for a REST endpoint
    3. Create technical documentation
    4. Develop test cases
    """


    # This would ideally trigger multiple agents in sequence
    result = await supervisor.ainvoke(
        {"messages": [HumanMessage(content=complex_request)]}
    )

    # Show final agent pool status

    for agent_name, agent in pool.agents.items():
        status_icon = "🟢" if agent.status == AgentStatus.ACTIVE else "⚫"
        calls = agent.metrics.total_calls

    return True


async def test_edge_cases_advanced():
    """Test edge cases with advanced scenarios."""

    from dynamic_supervisor_fixed import DynamicSupervisorFixed

    pool = await create_prebuilt_agent_pool()
    supervisor = DynamicSupervisorFixed(name="edge_supervisor")

    # Edge case 1: Agent at max capacity

    busy_agent = pool.agents["coder_senior"]
    busy_agent.status = AgentStatus.ACTIVE
    busy_agent.current_tasks = busy_agent.max_concurrent

    supervisor.register_agent(busy_agent)

    try:
        await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write some code")]}
        )
    except Exception as e:
        pass")

    # Edge case 2: All agents inactive

    # Start with active agents
    for agent in pool.get_active_agents()[:2]:
        supervisor.register_agent(agent)

    # Deactivate all after registration
    for agent_name in list(supervisor.get_registered_agents()):
        if agent_name in pool.agents:
            pool.agents[agent_name].status = AgentStatus.MAINTENANCE

    try:
        await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Do something")]}
        )
    except Exception as e:
        pass



if __name__ == "__main__":

    # Run main advanced test
    asyncio.run(test_advanced_dynamic_supervisor())

    # Run edge cases
    asyncio.run(test_edge_cases_advanced())

