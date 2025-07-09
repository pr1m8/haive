# Example usage of ReactAgent with Human Interaction

import uuid

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from haive.agents.react_class.react_v2.config import ReactAgentConfig


# 1. Define our tools
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"The weather in {location} is sunny and 72 degrees."


def search_database(query: str) -> str:
    """Search the database for information."""
    return f"Found results for '{query}': 3 matching entries."


def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {e!s}"


# Create structured tools
weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="Get the current weather for a location",
)

search_tool = StructuredTool.from_function(
    func=search_database,
    name="search_database",
    description="Search the database for information",
)

calculator_tool = StructuredTool.from_function(
    func=calculate, name="calculate", description="Calculate a mathematical expression"
)


# 2. Define structured output schema
class TripPlan(BaseModel):
    """A structured trip plan."""

    destination: str = Field(description="The destination city")
    activities: list[str] = Field(description="List of planned activities")
    duration_days: int = Field(description="Duration of the trip in days")
    budget_estimate: float = Field(description="Estimated budget for the trip")
    weather_summary: str | None = Field(None, description="Summary of expected weather")


# 3. Configure the React agent
system_prompt = """You are a helpful travel assistant that helps users plan trips. 
You have access to tools that can help you gather information.
Always use tools when appropriate and think step by step.

When you don't have enough information, use the request_human_assistance tool 
to ask the user for more details.
"""

react_config = ReactAgentConfig(
    name="travel_planner",
    engine=AugLLMConfig(
        name="travel_llm",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
    ),
    tools=[weather_tool, search_tool, calculator_tool],
    system_prompt=system_prompt,
    structured_output_schema=TripPlan,
    max_iterations=5,
    parallel_tools=True,
)
print(react_config)
# 4. Build the agent
travel_agent = react_config.build_agent()

# 5. Run the agent with simulated human interaction
user_input = "I want to plan a trip but I'm not sure where to go. Can you help?"


# This simulates an interaction with human intervention
def simulate_react_agent_with_human():
    print("Initial query:", user_input)
    print("\n--- Starting Agent ---\n")

    # Start a thread for persistence
    thread_id = uuid.uuid4()

    # First run - this will likely request human input
    for i, state in enumerate(travel_agent.stream(user_input, thread_id=thread_id)):
        # Print step details
        print(f"\nStep {i+1}:")

        # Check if human input is needed
        if state.get("requires_human_input", False):
            print(
                f"\n🔄 HUMAN INPUT REQUESTED: {state.get('human_request', 'Please provide more information.')}"
            )

            # Simulate human response
            human_response = "I'd like to go somewhere warm, maybe Miami or Hawaii, for about 5 days. My budget is around $2000."
            print(f"\n👤 Human responds: {human_response}")

            # Provide human input to continue the conversation
            state = travel_agent.run(
                {"messages": [HumanMessage(content=human_response)]},
                thread_id=thread_id,
            )
            break

    # Continue agent execution after human input
    print("\n--- Continuing After Human Input ---\n")

    # Run a simple follow-up to see the final plan
    follow_up = "That sounds great. What activities would you recommend?"

    result = travel_agent.run(follow_up, thread_id=thread_id)

    # Print the final structured output
    print("\n=== Final Trip Plan ===")
    if "structured_output" in result:
        plan = result["structured_output"]
        print(f"Destination: {plan.get('destination')}")
        print(f"Duration: {plan.get('duration_days')} days")
        print(f"Budget: ${plan.get('budget_estimate')}")
        print("Activities:")
        for activity in plan.get("activities", []):
            print(f" - {activity}")
        print(f"Weather: {plan.get('weather_summary')}")
    else:
        print("No structured output available yet.")

    return result


# Run the simulation
final_result = simulate_react_agent_with_human()
