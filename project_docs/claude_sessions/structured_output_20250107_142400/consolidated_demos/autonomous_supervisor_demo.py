#!/usr/bin/env python3
"""Demo of a supervisor that can autonomously create agents based on task requirements."""
from __future__ import annotations

import asyncio
import json
import logging

from haive.agents.experiments.dynamic_supervisor_enhanced import SelfModifyingSupervisor
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_autonomous_supervisor():
    """Demonstrate a supervisor that creates its own agents."""

    # Create supervisor with minimal initial agents
    supervisor = SelfModifyingSupervisor(
        name="Autonomous Task Manager", enable_self_modification=True, debug=True
    )

    # Start with just a general assistant
    supervisor.agent_registry.register(
        "general_agent",
        "General purpose assistant for basic tasks",
        SimpleAgent,
        {
            "name": "General Assistant",
            "system_message": "You are a helpful general assistant.",
        },
    )

    # Show self-modification tools
    mgmt_tools = [
        t.name
        for t in supervisor.tools
        if t.name
        in [
            "create_agent",
            "remove_agent",
            "modify_agent",
            "analyze_task_and_suggest_agent",
        ]
    ]

    # Simulate different tasks that require specialized agents
    tasks = [
        {
            "description": "Complex coding task",
            "message": "I need to create a REST API in Python with authentication, database integration, and comprehensive error handling.",
        },
        {
            "description": "Data analysis task",
            "message": "Analyze this sales data, identify trends, and create visualizations showing year-over-year growth.",
        },
        {
            "description": "Content creation task",
            "message": "Write a compelling blog post about the future of AI in healthcare, targeting medical professionals.",
        },
    ]

    for i, task in enumerate(tasks, 1):

        # Prepare the supervisor's input
        {
            "messages": [HumanMessage(content=task["message"])],
            "agent_registry": supervisor.agent_registry._agents,
            "current_iteration": 0,
            "max_iterations": 10,
        }

        # The supervisor should:
        # 1. Use 'list_agents' to see available agents
        # 2. Use 'analyze_task_and_suggest_agent' to determine needs
        # 3. Use 'create_agent' to create specialized agent if needed
        # 4. Use 'handoff_to_X' to delegate the task

        # In a real scenario, you would invoke the supervisor:

        # For demo, just show what would happen
        if "coding" in task["description"].lower():
            pass")
        elif "data" in task["description"].lower():
            pass")
        elif "content" in task["description"].lower():
            pass")


    # Show final state after autonomous operation


    return supervisor


def show_supervisor_thought_process():
    """Show how the supervisor would think through a task."""

    thought_process = """
Task: "Build a machine learning model to predict customer churn"

Supervisor's Internal Process:
1. Check available agents with 'list_agents' tool
   → Result: Only 'general_agent' available

2. Analyze task requirements with 'analyze_task_and_suggest_agent'
   → Identifies keywords: 'machine learning', 'model', 'predict'
   → Suggests creating 'ml_agent' with React type

3. Create specialized agent with 'create_agent' tool
   → create_agent(
       name="ml_agent",
       description="Machine learning model development and analysis",
       agent_type="react",
       system_message="You are an ML engineer expert in predictive modeling.",
       capabilities="sklearn,pandas,model_training,evaluation"
     )

4. Verify agent creation
   → New tool available: 'handoff_to_ml_agent'

5. Delegate task with 'handoff_to_ml_agent'
   → Pass the original task to the specialized agent

6. Monitor and coordinate
   → Forward results back to user
   → Keep ml_agent in registry for future ML tasks
"""




if __name__ == "__main__":
    # Run the demo
    supervisor = asyncio.run(demo_autonomous_supervisor())

    # Show thought process
    show_supervisor_thought_process()
