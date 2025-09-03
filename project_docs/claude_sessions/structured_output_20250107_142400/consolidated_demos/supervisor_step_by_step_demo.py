#!/usr/bin/env python3
"""Demo showing supervisor's step-by-step decision process with actual execution."""
from __future__ import annotations

import asyncio
import logging

from haive.agents.experiments.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def create_decision_making_tools(supervisor: DynamicSupervisorAgent):
    """Add tools for autonomous agent creation with decision logging."""

    @tool
    def evaluate_task_requirements(task: str) -> str:
        """Analyze a task to determine what type of agent is needed.

        Args:
            task: The task description to analyze

        Returns:
            Analysis of task requirements
        """
        task_lower = task.lower()

        analysis = "📋 TASK ANALYSIS:\n"
        analysis += f"Task: '{task}'\n\n"

        # Identify task type
        if any(
            word in task_lower
            for word in ["code", "python", "function", "debug", "program"]
        ):
            analysis += "🔍 Task Type: CODING\n"
            analysis += "💡 Requires: Programming expertise\n"
            analysis += "🤖 Suggested Agent: coding_agent\n"
            analysis += "📝 Skills Needed: Python, debugging, algorithms"
        elif any(
            word in task_lower
            for word in ["write", "blog", "article", "content", "story"]
        ):
            analysis += "🔍 Task Type: WRITING\n"
            analysis += "💡 Requires: Creative writing skills\n"
            analysis += "🤖 Suggested Agent: writing_agent\n"
            analysis += "📝 Skills Needed: Content creation, editing"
        elif any(
            word in task_lower
            for word in ["analyze", "data", "statistics", "chart", "graph"]
        ):
            analysis += "🔍 Task Type: DATA ANALYSIS\n"
            analysis += "💡 Requires: Data science expertise\n"
            analysis += "🤖 Suggested Agent: data_agent\n"
            analysis += "📝 Skills Needed: Statistics, visualization"
        elif any(
            word in task_lower for word in ["research", "find", "search", "investigate"]
        ):
            analysis += "🔍 Task Type: RESEARCH\n"
            analysis += "💡 Requires: Research and synthesis skills\n"
            analysis += "🤖 Suggested Agent: research_agent\n"
            analysis += "📝 Skills Needed: Web search, summarization"
        else:
            analysis += "🔍 Task Type: GENERAL\n"
            analysis += "💡 Requires: General assistance\n"
            analysis += "🤖 Suggested Agent: general_agent\n"
            analysis += "📝 Skills Needed: Broad knowledge base"

        return analysis

    @tool
    def check_agent_availability(agent_name: str) -> str:
        """Check if a specific agent exists and is available.

        Args:
            agent_name: Name of the agent to check

        Returns:
            Availability status
        """
        agents = supervisor.agent_registry.list_agents()

        result = f"🔎 CHECKING: {agent_name}\n"

        if agent_name in agents:
            result += f"✅ STATUS: Agent '{agent_name}' EXISTS\n"
            result += f"📋 Description: {agents[agent_name]['description']}\n"
            result += "🚀 Action: Can delegate immediately"
        else:
            result += f"❌ STATUS: Agent '{agent_name}' NOT FOUND\n"
            result += "🔧 Action: Need to create this agent first"

        return result

    @tool
    def create_specialized_agent(
        agent_name: str, agent_purpose: str, agent_expertise: str
    ) -> str:
        """Create a new specialized agent after evaluation.

        Args:
            agent_name: Internal name (e.g., 'coding_agent')
            agent_purpose: What the agent does
            agent_expertise: System prompt/expertise

        Returns:
            Creation status
        """
        result = f"🏗️ CREATING AGENT: {agent_name}\n"

        try:
            # Check if already exists
            if agent_name in supervisor.agent_registry.list_agents():
                return f"⚠️ Agent '{agent_name}' already exists! Skipping creation."

            # Create the agent
            supervisor.add_agent_to_registry(
                name=agent_name,
                description=agent_purpose,
                agent_class=SimpleAgent,
                config={
                    "name": agent_name.replace("_", " ").title(),
                    "system_message": agent_expertise,
                },
            )

            result += "✅ SUCCESS: Agent created\n"n"
            result += f"🔧 New Tool: handoff_to_{agent_name}\n"
            result += (
                f"📊 Total Agents: {len(supervisor.agent_registry.list_agents())}\n"
            )
            result += "🎯 Ready to delegate tasks!"s!"

            return result

        except Exception as e:
            return f"❌ ERROR: Failed to create agent - {e!s}"}"

    @tool
    def decide_next_action(task_analysis: str, availability_check: str) -> str:
        """Decide whether to create an agent or delegate directly.

        Args:
            task_analysis: Result from evaluate_task_requirements
            availability_check: Result from check_agent_availability

        Returns:
            Decision and next steps
        """
        decision = "🤔 DECISION POINT:\n"

        if "EXISTS" in availability_check:
            decision += "✅ Decision: DELEGATE DIRECTLY\n"
            decision += "📌 Reason: Required agent already exists\n"
            decision += "➡️ Next Step: Use handoff tool to delegate task"
        else:
            decision += "🔧 Decision: CREATE AGENT FIRST\n"
            decision += "📌 Reason: Required agent doesn't exist yet\n"
            decision += "➡️ Next Steps:\n"
            decision += "   1. Use create_specialized_agent tool\n"
            decision += "   2. Then use handoff tool to delegate"

        return decision

    # Add all tools
    supervisor.tools.extend(
        [
            evaluate_task_requirements,
            check_agent_availability,
            create_specialized_agent,
            decide_next_action,
        ]
    )

    # Update system message
    supervisor.system_message = """You are an autonomous supervisor that creates agents as needed.

STEP-BY-STEP PROCESS for each task:

1. EVALUATE: Use 'evaluate_task_requirements' to analyze what type of agent is needed
2. CHECK: Use 'check_agent_availability' to see if that agent exists
3. DECIDE: Use 'decide_next_action' to determine whether to create or delegate
4. ACT: Either:
   - CREATE: Use 'create_specialized_agent' if needed, then delegate
   - DELEGATE: Use 'handoff_to_X' if agent already exists

Always show your reasoning at each step."""


async def demo_step_by_step():
    """Run demo showing step-by-step decision making."""

    # Create supervisor
    supervisor = DynamicSupervisorAgent(name="Step-by-Step Supervisor", debug=True)

    # Add decision-making tools
    create_decision_making_tools(supervisor)

    # Start with one general agent
    supervisor.agent_registry.register(
        "general_agent",
        "General purpose assistant",
        SimpleAgent,
        {"name": "General Assistant", "system_message": "You are a helpful assistant."},
    )


    # Test tasks
    test_tasks = [
        "Write a Python function to calculate fibonacci numbers",
        "Research the history of artificial intelligence",
        "Write another Python script for sorting algorithms",  # Should reuse coding_agent
    ]


    for i, task in enumerate(test_tasks, 1):

        # Prepare input
        {
            "messages": [HumanMessage(content=task)],
            "agent_registry": supervisor.agent_registry._agents,
            "current_iteration": 0,
            "max_iterations": 10,
        }

        # Show expected decision process

        # In real execution, supervisor would run:

        # For demo, show what would happen
        if i == 1:
        elif i == 2:
        else:

        await asyncio.sleep(0.1)  # Small delay for readability


    return supervisor


def save_execution_trace():
    """Save a detailed execution trace for review."""
    trace = {
        "execution_steps": [
            {
                "step": 1,
                "tool": "evaluate_task_requirements",
                "input": "Write a Python function to calculate fibonacci numbers",
                "output": "Task Type: CODING, Suggested Agent: coding_agent",
            },
            {
                "step": 2,
                "tool": "check_agent_availability",
                "input": "coding_agent",
                "output": "STATUS: Agent 'coding_agent' NOT FOUND",
            },
            {
                "step": 3,
                "tool": "decide_next_action",
                "input": "Previous results",
                "output": "Decision: CREATE AGENT FIRST",
            },
            {
                "step": 4,
                "tool": "create_specialized_agent",
                "input": {
                    "name": "coding_agent",
                    "purpose": "writes Python code",
                    "expertise": "You are an expert Python developer",
                },
                "output": "SUCCESS: Agent created, New Tool: handoff_to_coding_agent",
            },
            {
                "step": 5,
                "tool": "handoff_to_coding_agent",
                "input": "Write a Python function to calculate fibonacci numbers",
                "output": "Task delegated to coding_agent",
            },
        ]
    }

    import json

    with open("/tmp/supervisor_execution_trace.json", "w") as f:
        json.dump(trace, f, indent=2)



if __name__ == "__main__":
    # Run the demo
    supervisor = asyncio.run(demo_step_by_step())

    # Save execution trace
    save_execution_trace()
