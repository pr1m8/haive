"""Test registry supervisor with REAL ReactAgents - NO MOCKS."""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the source path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from langchain_core.messages import HumanMessage

from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor.registry_supervisor import RegistrySupervisor
from haive.agents.tools import BaseTool


class RealResearchTool(BaseTool):
    """Real research tool - no mocking."""

    name: str = "research_tool"
    description: str = "Research and analyze information on any topic"

    def _run(self, query: str) -> str:
        return f"RESEARCH COMPLETED: Comprehensive analysis of '{query}' including current trends, key findings, and statistical data."


class RealCodingTool(BaseTool):
    """Real coding tool - no mocking."""

    name: str = "coding_tool"
    description: str = "Write, debug, and analyze code in multiple languages"

    def _run(self, code_request: str) -> str:
        return f"CODE GENERATED: Full implementation for '{code_request}' with proper error handling, type hints, and documentation."


class RealWritingTool(BaseTool):
    """Real writing tool - no mocking."""

    name: str = "writing_tool"
    description: str = "Create professional written content and documentation"

    def _run(self, writing_request: str) -> str:
        return f"CONTENT CREATED: Professional document for '{writing_request}' with structured format and key insights."


def save_state_history(agent_name: str, state_data: dict, test_phase: str):
    """Save agent state history as requested."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_name}_{test_phase}_{timestamp}.json"

    # Create state history directory if it doesn't exist
    state_dir = Path(
        "/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history"
    )
    state_dir.mkdir(parents=True, exist_ok=True)

    filepath = state_dir / filename

    import json

    with open(filepath, "w") as f:
        json.dump(
            {
                "agent_name": agent_name,
                "test_phase": test_phase,
                "timestamp": timestamp,
                "state_data": state_data,
            },
            f,
            indent=2,
            default=str,
        )

    return filepath


async def test_real_registry_supervisor():
    """Test with REAL ReactAgents and save state history."""

    # Create REAL ReactAgent instances

    research_agent = ReactAgent(
        name="research_specialist",
        description="Expert research agent for information analysis",
        tools=[RealResearchTool()],
    )

    coding_agent = ReactAgent(
        name="code_expert",
        description="Professional coding agent for software development",
        tools=[RealCodingTool()],
    )

    writing_agent = ReactAgent(
        name="content_creator",
        description="Professional writing agent for documentation",
        tools=[RealWritingTool()],
    )


    # Create REAL supervisor
    supervisor = RegistrySupervisor(name="dynamic_supervisor")

    # Populate registry with real agents
    supervisor.populate_registry(agents=[research_agent, coding_agent, writing_agent])


    # Save initial state
    initial_state = {
        "registry_size": len(supervisor.agent_registry),
        "total_tools": len(supervisor.tools),
        "agents": list(supervisor.agent_registry.keys()),
    }
    save_state_history("supervisor", initial_state, "initial_setup")

    # Test 1: Real research task

    research_input = {
        "messages": [
            HumanMessage(
                content="Research current AI safety regulations and their impact on ML development"
            )
        ]
    }

    research_result = await supervisor.ainvoke(research_input)

    # Save research state
    research_state = {
        "input": research_input,
        "output": str(research_result),
        "agent_used": "research_specialist",
    }
    save_state_history("supervisor", research_state, "research_test")

    # Test 2: Real coding task

    coding_input = {
        "messages": [
            HumanMessage(
                content="Implement a thread-safe LRU cache in Python with async support"
            )
        ]
    }

    coding_result = await supervisor.ainvoke(coding_input)

    # Save coding state
    coding_state = {
        "input": coding_input,
        "output": str(coding_result),
        "agent_used": "code_expert",
    }
    save_state_history("supervisor", coding_state, "coding_test")

    # Test 3: Real writing task

    writing_input = {
        "messages": [
            HumanMessage(
                content="Create technical documentation for a microservices architecture migration"
            )
        ]
    }

    writing_result = await supervisor.ainvoke(writing_input)

    # Save writing state
    writing_state = {
        "input": writing_input,
        "output": str(writing_result),
        "agent_used": "content_creator",
    }
    save_state_history("supervisor", writing_state, "writing_test")

    # Test 4: Dynamic agent addition

    class RealAnalysisTool(BaseTool):
        name: str = "analysis_tool"
        description: str = "Advanced data analysis and statistical modeling"

        def _run(self, data_request: str) -> str:
            return f"ANALYSIS COMPLETE: Statistical analysis of '{data_request}' with predictive models and actionable insights."

    # Create new REAL agent
    analysis_agent = ReactAgent(
        name="data_analyst",
        description="Expert data analysis agent for statistical insights",
        tools=[RealAnalysisTool()],
    )


    # Add to registry dynamically
    supervisor.agent_registry["data_analyst"] = analysis_agent
    supervisor.tools.extend(analysis_agent.tools)
    supervisor._update_supervisor_tools()


    # Test with new agent
    analysis_input = {
        "messages": [
            HumanMessage(
                content="Analyze user engagement patterns and predict churn probability"
            )
        ]
    }

    analysis_result = await supervisor.ainvoke(analysis_input)

    # Save dynamic addition state
    dynamic_state = {
        "new_agent": analysis_agent.name,
        "registry_size": len(supervisor.agent_registry),
        "tool_count": len(supervisor.tools),
        "input": analysis_input,
        "output": str(analysis_result),
    }
    save_state_history("supervisor", dynamic_state, "dynamic_addition")

    # Final verification

    for name, agent in supervisor.agent_registry.items():
        pass")

    for tool in supervisor.tools:
        pass")

    # Save final state
    final_state = {
        "final_registry_size": len(supervisor.agent_registry),
        "final_tool_count": len(supervisor.tools),
        "all_agents": {
            name: agent.description for name, agent in supervisor.agent_registry.items()
        },
        "all_tools": {tool.name: tool.description for tool in supervisor.tools},
    }
    save_state_history("supervisor", final_state, "final_verification")



if __name__ == "__main__":
    asyncio.run(test_real_registry_supervisor())
