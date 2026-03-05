"""Demo 03: ReactAgent with Tools.

Tests: ReactAgent with tool calling and reasoning loop
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.react.agent import ReactAgent


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression. Use Python syntax (e.g., 2+2, 15*23, 100/7)."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city (mock data for demo)."""
    weather_data = {
        "london": "Cloudy, 12C",
        "tokyo": "Sunny, 22C",
        "new york": "Partly cloudy, 18C",
        "paris": "Rainy, 14C",
    }
    return weather_data.get(city.lower(), f"No weather data for {city}")


async def main():
    print("=" * 60)
    print("Demo 03: ReactAgent with Tools")
    print("=" * 60)

    config = AugLLMConfig(
        temperature=0.3,
        system_message="You are a helpful assistant with access to a calculator and weather tool. Use tools when needed.",
    )

    agent = ReactAgent(
        name="react_demo",
        engine=config,
        tools=[calculator, get_weather],
    )
    print(f"[OK] Instantiated: {agent.name}")
    print(f"[OK] Tools: {[t.name for t in agent.tools]}")

    print("\n--- Running arun ---")
    result = await agent.arun("What is 15 * 23? Also, what's the weather in Tokyo?")
    print(f"Result type: {type(result)}")

    if hasattr(result, "messages"):
        content = result.messages[-1].content if result.messages else str(result)
    elif isinstance(result, dict) and "messages" in result:
        content = result["messages"][-1].content if result["messages"] else str(result)
    elif isinstance(result, str):
        content = result
    else:
        content = str(result)

    print(f"Response: {content[:300]}")
    print("\n[OK] ReactAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
