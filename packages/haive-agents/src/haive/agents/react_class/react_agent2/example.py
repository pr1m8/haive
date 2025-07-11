# examples/react_agent_custom_routing_example.py

import logging
from datetime import datetime
from typing import Any

from agents.react_agent2.agent import create_react_agent
from haive.core.graph.tool_config import ToolConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# Define Tools with Different Behaviors
# =============================================


@tool
def search_db(query: str) -> str:
    """Search an internal database for information."""
    return f"Database results for '{query}':\n1. Internal document #42: {query} overview\n2. Internal document #56: {query} details\n3. Internal document #78: {query} procedures"


@tool
def search_web(query: str) -> str:
    """Search the web for public information."""
    return f"Web results for '{query}':\n1. Wikipedia: Information about {query}\n2. News sites: Recent developments in {query}\n3. Blogs: Opinions on {query}"


@tool
def analyze_data(data_id: str, analysis_type: str = "basic") -> str:
    """Analyze specified data with analysis type (basic, detailed, predictive)."""
    analysis_results = {
        "sales": {
            "basic": "Basic analysis of sales data: Growth of 5.2% year-over-year",
            "detailed": "Detailed analysis of sales data: Growth in Q1: 3.1%, Q2: 5.8%, Q3: 6.2%, Q4: 5.7%",
            "predictive": "Predictive analysis of sales data: Expected 6.5% growth next quarter based on current trends",
        },
        "customers": {
            "basic": "Basic analysis of customer data: 15% increase in new customers",
            "detailed": "Detailed analysis of customer data: 22% increase in urban areas, 8% in suburban, 5% in rural",
            "predictive": "Predictive analysis of customer data: Expected 12% growth in customer base next year",
        },
        "inventory": {
            "basic": "Basic analysis of inventory data: Current stock levels at 78% capacity",
            "detailed": "Detailed analysis of inventory data: Electronics: 92%, Clothing: 76%, Home goods: 65%",
            "predictive": "Predictive analysis of inventory data: Electronics stock expected to reach capacity in 45 days",
        },
    }

    # Default response if data_id not found
    if data_id not in analysis_results:
        return f"Analysis of {data_id} data ({analysis_type}): No significant patterns detected"

    # Default to basic analysis if type not found
    if analysis_type not in analysis_results[data_id]:
        analysis_type = "basic"

    return analysis_results[data_id][analysis_type]


@tool
def execute_action(action_type: str, target_id: str) -> str:
    """Execute a business action on the specified target."""
    # This would normally trigger some business process
    action_results = {
        "approve": f"Approved {target_id} - Confirmation code: AP-{hash(target_id) % 1000:04d}",
        "reject": f"Rejected {target_id} - Reason code: RE-{hash(target_id) % 1000:04d}",
        "escalate": f"Escalated {target_id} to senior management - Tracking number: ES-{hash(target_id) % 1000:04d}",
        "defer": f"Deferred decision on {target_id} until next review cycle - Reminder set",
    }

    # Default response if action_type not recognized
    if action_type not in action_results:
        return f"Unknown action '{action_type}' requested for {target_id} - No action taken"

    return action_results[action_type]


# =============================================
# Custom Tool Processors
# =============================================


def data_analyzer_processor(state: dict[str, Any]) -> dict[str, Any]:
    """Custom processor for data analysis requests."""
    # This would contain specialized logic for handling data analysis
    # For example, adding metadata, logging, or special formatting

    # For demo, we'll just add a note to the state
    updated_state = dict(state)
    if "notes" not in updated_state:
        updated_state["notes"] = []

    updated_state["notes"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "event": "Data analysis request processed through specialized pathway",
        }
    )

    return updated_state


def action_executor_processor(state: dict[str, Any]) -> dict[str, Any]:
    """Custom processor for action execution requests."""
    # This would contain specialized logic for handling business actions
    # For example, authorization checks, audit logging, or notifications

    # For demo, we'll just add a note to the state
    updated_state = dict(state)
    if "notes" not in updated_state:
        updated_state["notes"] = []

    updated_state["notes"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "event": "Business action request processed through specialized pathway",
        }
    )

    return updated_state


# =============================================
# Example: React Agent with Custom Tool Routing
# =============================================


def run_custom_tool_routing_example():
    """Example of React agent with custom tool routing."""

    # Define tools with configurations
    tools = [
        ToolConfig(
            tool=search_db,
            name="search_db",
            description="Search the internal database for information.",
        ),
        ToolConfig(
            tool=search_web,
            name="search_web",
            description="Search the web for public information.",
        ),
        ToolConfig(
            tool=analyze_data,
            name="analyze_data",
            description="Analyze specified data with analysis type.",
        ),
        ToolConfig(
            tool=execute_action,
            name="execute_action",
            description="Execute a business action on the specified target.",
        ),
    ]

    # Define custom tool routing
    tool_routing = {
        # Route specific tools to specialized processors
        "analyze_data": "data_analyzer",
        "execute_action": "action_executor",
    }

    # Create system prompt explaining the different tools
    system_prompt = """You are a Business Intelligence Assistant with access to both internal and external data sources.

You have the following tools available:
1. search_db - Search internal databases for company information
2. search_web - Search the web for public information
3. analyze_data - Perform data analysis on company datasets
4. execute_action - Execute business actions like approvals or escalations

Use internal tools (search_db, analyze_data, execute_action) for company-specific questions.
Use external tools (search_web) for general information or market research.
Always explain your reasoning before using a tool.
"""

    # Create a React agent with custom tool routing
    agent = create_react_agent(
        tools=[t.tool for t in tools],  # Extract tools from src.configs
        model="gpt-4o",
        temperature=0.7,
        system_prompt=system_prompt,
        name="BusinessIntelligenceAgent",
        max_iterations=5,
        visualize=True,  # Generate visualization
        tool_routing=tool_routing,  # Custom tool routing
        debug=True,
    )

    # Add custom processors to the agent after creation
    if hasattr(agent, "app") and agent.app:
        # If the app is already compiled, we need to rebuild it
        # In practice you might want to customize the agent before compilation
        pass

    # Test with questions that would trigger different tool routes
    questions = [
        "Can you analyze our sales data in detail?",
        "Can you approve purchase order #45678?",
        "What's the current market trend for AI technology companies?",
    ]

    for i, question in enumerate(questions):

        # Create input with human message
        input_data = {"messages": [HumanMessage(content=question)]}

        # Run the agent
        result = agent.run(input_data)

        # Print out the messages
        for msg in result.get("messages", []):
            if hasattr(msg, "type") and hasattr(msg, "content"):
                msg_type = msg.type.upper()
                if hasattr(msg, "name") and msg.name:
                    msg_type = f"{msg_type} ({msg.name})"

                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        pass
                else:
            elif isinstance(msg, tuple) and len(msg) == 2:

    # Visualization should have been saved to the output directory
    visualization_dir = agent.config.output_dir or "outputs"


# =============================================
# Run the example
# =============================================

if __name__ == "__main__":
    run_custom_tool_routing_example()
