# examples/react_agent_example.py

import datetime
import logging
import os
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(f"sys.path: {sys.path}")
from haive_agents_dep.react_agent2.agent2 import create_react_agent

# Import agent
from langchain_core.tools import tool

from haive.core.models.llm.base import AzureLLMConfig


# Simple tools for testing
@tool
def search_web(query: str) -> str:
    """Search the web for the given query and return relevant information."""
    # Simulate web search
    if "weather" in query.lower():
        return "The current weather is sunny with a high of 75°F and a low of 60°F."
    if "news" in query.lower():
        return "Recent headlines: New AI breakthrough announced. Global climate summit scheduled for next month."
    if "stock" in query.lower() or "market" in query.lower():
        return "The stock market is currently up 0.5% for the day. Major tech stocks are showing strong performance."
    return f"Search results for '{query}': Found several relevant pages discussing this topic."


@tool
def get_current_date() -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression."""
    try:
        # WARNING: eval is unsafe for production use
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {e!s}"


@tool
def translate_text(text: str, target_language: str) -> str:
    """Translate text to the target language."""
    # Simplified translation simulation
    languages = {
        "spanish": {
            "hello": "hola",
            "goodbye": "adiós",
            "thank you": "gracias",
            "how are you": "cómo estás",
        },
        "french": {
            "hello": "bonjour",
            "goodbye": "au revoir",
            "thank you": "merci",
            "how are you": "comment ça va",
        },
        "german": {
            "hello": "hallo",
            "goodbye": "auf wiedersehen",
            "thank you": "danke",
            "how are you": "wie geht es dir",
        },
    }

    target_language = target_language.lower()
    if target_language not in languages:
        return f"Translation to {target_language} is not supported."

    # Check for exact matches
    text_lower = text.lower()
    if text_lower in languages[target_language]:
        return f"Translation: {languages[target_language][text_lower]}"

    # Simulate translation of other text
    return f"Translation of '{text}' to {target_language}: [Simulated translation]"


# Define test cases
TEST_CASES = [
    "What's the weather like today?",
    "Calculate the square root of 144 plus 36",
    "What's the current date and translate 'hello' to Spanish",
    "Can you find the latest news and summarize it for me?",
]


def run_test_cases():
    """Run the agent on test cases."""
    print("\n=== Creating React Agent ===")

    # Create LLM config (using Azure OpenAI)
    llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})

    # Create tools list
    tools = [search_web, get_current_date, calculate, translate_text]

    # Create agent
    agent = create_react_agent(
        tools=tools,
        llm_config=llm_config,
        name="test_react_agent",
        system_prompt=(
            "You are a helpful assistant that can use tools to answer questions. "
            "You have access to search, date lookup, calculation, and translation tools. "
            "Think step by step and use the appropriate tools to answer the user's question."
        ),
    )

    print(f"Agent created: {agent.config.name}")

    # Run test cases
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n\n=== Test Case {i}: '{test_case}' ===\n")

        # Run agent
        result = agent.run(test_case)

        # Extract messages for display
        messages = result.get("messages", [])

        # Print messages in a readable format
        for msg in messages:
            if hasattr(msg, "content") and hasattr(msg, "type"):
                print(f"{msg.type.upper()}: {msg.content}")
            elif hasattr(msg, "content"):
                print(f"{type(msg).__name__.upper()}: {msg.content}")
            else:
                print(f"MESSAGE: {msg}")

            # Print tool calls if present
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print("\nTOOL CALLS:")
                for call in msg.tool_calls:
                    print(
                        f"  - {call.get('name', 'Unknown tool')}: {call.get('args', {})}"
                    )

        # Print final stats
        print(f"\nSteps taken: {result.get('current_step', 0)}")
        print(f"Observations: {len(result.get('observations', []))}")
        print(f"Tool calls: {len(result.get('action_history', []))}")

        # Print any errors
        if result.get("error"):
            print(f"ERROR: {result['error']}")


if __name__ == "__main__":
    run_test_cases()
