# src/haive/agents/react_agent2/examples.py
import logging
import uuid

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.react_class.react_agent2.agent2 import create_react_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Helper function to print the latest message
def print_latest_message(result):
    """Print the latest message from the result."""
    messages = result.get("messages", [])
    if messages:
        final_message = messages[-1]
        if hasattr(final_message, "content"):
            pass
        elif isinstance(final_message, dict) and "content" in final_message:
            final_message["content"]
        else:
            str(final_message)


# =============================================
# Example 1: Basic React Agent with Tools
# =============================================


def example_basic_react_agent():
    """Basic React agent with search and calculator tools."""

    # Define a simple search tool
    @tool
    def search(query: str) -> str:
        """Search for information on the given query."""
        return f"Search results for '{query}':\n- Found that {query} was first discovered in 1905\n- {query} is associated with important historical events\n- Most experts consider {query} to be significant in modern science"

    # Define a calculator tool
    @tool
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Warning: In production, use safer evaluation methods
            return f"Result of '{expression}' = {eval(expression)}"
        except Exception as e:
            return f"Error evaluating expression: {e!s}"

    # Create a React agent with these tools
    agent = create_react_agent(
        tools=[search, calculator],
        name="basic_react_agent",
        model="gpt-4o",
        temperature=0.7,
    )

    # Run the agent with a question
    result = agent.run("Who was Albert Einstein and what is 2023 minus his birth year?")

    # Display the final answer
    print_latest_message(result)

    return agent


# =============================================
# Example 2: React Agent with Structured Output
# =============================================


def example_structured_output_agent():
    """React agent that returns structured output."""

    # Define a structured output model
    class MovieReview(BaseModel):
        """A structured movie review."""

        title: str = Field(description="The title of the movie")
        year: int = Field(description="The year the movie was released")
        rating: float = Field(description="Rating from 0-10")
        summary: str = Field(description="A brief summary of the movie")
        pros: list[str] = Field(description="Positive aspects of the movie")
        cons: list[str] = Field(description="Negative aspects of the movie")

    # Define a search tool
    @tool
    def search_movie(movie_title: str) -> str:
        """Search for information about a movie."""
        if movie_title.lower() == "inception":
            return """
            Inception (2010) - IMDb rating: 8.8/10
            Directed by Christopher Nolan, starring Leonardo DiCaprio, Joseph Gordon-Levitt, and Ellen Page.
            A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.
            Known for its complex plot, stunning visuals, and mind-bending concept.
            Won four Academy Awards for Best Cinematography, Best Sound Editing, Best Sound Mixing, and Best Visual Effects.
            Some viewers found the plot overly complicated and the ending ambiguous.
            """
        return f"Found movie: {movie_title} (fictional search results)"

    # Create a React agent with structured output
    agent = create_react_agent(
        tools=[search_movie],
        name="movie_review_agent",
        model="gpt-4o",
        temperature=0.7,
        response_format=MovieReview,
    )

    # Run the agent with a question
    result = agent.run("Can you provide a review of the movie Inception?")

    # Display the structured output
    structured_output = result.get("structured_output")
    if structured_output:
        movie_review = structured_output
        for _pro in movie_review.pros:
            pass
        for _con in movie_review.cons:
            pass

    return agent


# =============================================
# Example 3: React Agent with Memory
# =============================================


def example_memory_agent():
    """React agent with conversation memory."""

    # Define a simple weather tool
    @tool
    def get_weather(location: str) -> str:
        """Get the current weather for a location."""
        return f"Weather in {location}: Sunny, 75°F (24°C), light breeze from the west."

    # Create a React agent with memory
    agent = create_react_agent(
        tools=[get_weather],
        name="memory_agent",
        model="gpt-4o",
        temperature=0.7,
        use_memory=True,
    )

    # Create a thread ID for this conversation
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # First question
    result1 = agent.run("What's the weather like in San Francisco?", **config)
    print_latest_message(result1)

    # Follow-up question
    result2 = agent.run("Should I bring a jacket?", **config)
    print_latest_message(result2)

    # Another follow-up
    result3 = agent.run("What about in Miami?", **config)
    print_latest_message(result3)

    return agent


# =============================================
# Example 4: Business Intelligence Agent
# =============================================


def example_business_intelligence_agent():
    """React agent specialized in business intelligence tasks."""

    # Define business intelligence tools
    @tool
    def search_db(query: str) -> str:
        """Search an internal database for information."""
        return f"Database results for '{query}':\n1. Internal document #42: {query} overview\n2. Internal document #56: {query} details\n3. Internal document #78: {query} procedures"

    @tool
    def search_web(query: str) -> str:
        """Search the web for public information."""
        return f"Web results for '{query}':\n1. Wikipedia: Information about {query}\n2. News sites: Recent developments in {query}\n3. Blogs: Opinions on {query}"

    @tool
    def analyze_data(data_source: str, analysis_type: str) -> str:
        """Analyze specified data with analysis type (basic, detailed, predictive)."""
        return f"Analysis ({analysis_type}) of {data_source}:\n1. Key Metric 1: 42%\n2. Key Metric 2: $1.2M\n3. Key Metric 3: 15% YoY growth"

    @tool
    def execute_action(action: str, target: str) -> str:
        """Execute a business action on the specified target."""
        return f"Action '{action}' executed on {target}. Status: Success"

    # Create business intelligence agent
    system_prompt = """You are a skilled business intelligence assistant that helps analyze data, find information, and perform business actions.

    You have access to internal databases, web searches, data analysis tools, and can execute business actions when properly authorized.

    When responding to requests:
    1. First understand what information or action is needed
    2. Search for relevant data or context
    3. Analyze the information if necessary
    4. Execute actions only when explicitly requested and authorized
    5. Provide clear, concise, and actionable insights

    Always maintain confidentiality of internal data and verify authorization before executing business actions.
    """

    agent = create_react_agent(
        tools=[search_db, search_web, analyze_data, execute_action],
        name="BusinessIntelligenceAgent",
        model="gpt-4o",
        temperature=0.7,
        system_prompt=system_prompt,
    )

    # Run tests
    result1 = agent.run("Can you analyze our sales data in detail?")
    print_latest_message(result1)

    result2 = agent.run("Can you approve purchase order #45678?")
    print_latest_message(result2)

    result3 = agent.run("What's the current market trend for AI technology companies?")
    print_latest_message(result3)

    return agent


# =============================================
# Interactive Chat with React Agent
# =============================================


def interactive_chat():
    """Start an interactive chat with a React agent."""

    # Define tools
    @tool
    def search(query: str) -> str:
        """Search for information on the given query."""
        return f"Search results for '{query}':\n- Found relevant information about {query}\n- Several sources mention important details\n- Recent articles discuss new developments"

    @tool
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            return f"Result of '{expression}' = {eval(expression)}"
        except Exception as e:
            return f"Error evaluating expression: {e!s}"

    # Create a React agent
    agent = create_react_agent(
        tools=[search, calculator],
        name="chat_agent",
        model="gpt-4o",
        temperature=0.7,
        use_memory=True,
        system_prompt="You are a helpful assistant who can search for information and perform calculations.",
    )

    # Start interactive chat
    agent.chat()

    return agent


# =============================================
# Main Function to Run Examples
# =============================================


def run_examples():
    """Run all React agent examples."""
    # Run basic example
    example_basic_react_agent()

    # Run structured output example
    example_structured_output_agent()

    # Run memory example
    example_memory_agent()

    # Run business intelligence example
    example_business_intelligence_agent()

    # Uncomment to run interactive chat


if __name__ == "__main__":
    run_examples()
