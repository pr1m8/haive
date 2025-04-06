import logging
from typing import List, Dict, Any
from langchain_core.tools import Tool

from src.haive.agents.rec_plan.agent import create_recursive_tree_planner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define some example tools
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # This is a mock implementation
    return f"Information about '{query}' from Wikipedia: This is a placeholder for real search results."

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

def fetch_weather(location: str) -> str:
    """Fetch weather information for a location."""
    # This is a mock implementation
    return f"Weather for {location}: Sunny, 75°F"

def summarize(text: str) -> str:
    """Summarize a piece of text."""
    # This is a mock implementation
    words = text.split()
    if len(words) <= 10:
        return text
    return " ".join(words[:10]) + "..."

# Create tools
search_tool = Tool(
    name="search",
    func=search_wikipedia,
    description="Search Wikipedia for information about a topic. Input should be a search query."
)

math_tool = Tool(
    name="calculate",
    func=calculate,
    description="Calculate a mathematical expression. Input should be a valid mathematical expression (e.g., '2 + 2')."
)

weather_tool = Tool(
    name="weather",
    func=fetch_weather,
    description="Get weather information for a location. Input should be a location name."
)

summarize_tool = Tool(
    name="summarize",
    func=summarize,
    description="Summarize a piece of text. Input should be the text to summarize."
)

# List of tools to provide to the agent
tools = [search_tool, math_tool, weather_tool, summarize_tool]

def run_example():
    """Run an example with the recursive tree planner agent."""
    # Create the agent
    agent = create_recursive_tree_planner(
        name="example_agent",
        tools=tools,
        max_iterations=2,
        max_parallel_steps=3
    )
    
    # Define a task
    task = """
    Calculate the sum of:
    1. The square of 25
    2. The current temperature in San Francisco (in Fahrenheit)
    3. The year that Albert Einstein published the theory of relativity
    
    Then, find information about the scientist who was born closest to that sum.
    """
    
    # Run the agent
    logger.info(f"Running agent with task: {task}")
    result = agent.run(task, debug=False)
    
    # Print the final answer
    logger.info("Agent execution completed")
    logger.info(f"Final answer: {result.get('final_answer', 'No answer generated')}")
    
    # Return the full result for analysis
    return result

def run_multistep_example():
    """Run a multi-step example that demonstrates parallel execution."""
    # Create the agent
    agent = create_recursive_tree_planner(
        name="multistep_agent",
        tools=tools,
        max_iterations=2,
        max_parallel_steps=3
    )
    
    # Define a more complex task that benefits from parallelization
    task = """
    I need a comparative analysis of three topics:
    
    1. The population growth of New York City over the last century
    2. The mathematical concept of exponential growth
    3. The weather patterns in major coastal cities
    
    For each topic, find key information, then create a summary that explains how these three topics might relate to each other.
    """
    
    # Run the agent
    logger.info(f"Running agent with multi-step task: {task}")
    result = agent.run(task, debug=False)
    
    # Print the final answer
    logger.info("Agent execution completed")
    logger.info(f"Final answer: {result.get('final_answer', 'No answer generated')}")
    
    # Return the full result for analysis
    return result

if __name__ == "__main__":
    # Run the example
    result = run_example()
    
    # Print messages for analysis
    print("\nMessage history:")
    for i, message in enumerate(result.get("messages", [])):
        print(f"[{i}] {message.type}: {message.content[:100]}...")
    
    # Run the multi-step example
    #multistep_result = run_multistep_example()