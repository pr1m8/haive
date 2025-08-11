#!/usr/bin/env python3
"""Custom Tools Example - Creating and using custom tools with agents.

This example demonstrates how to create custom tools and integrate
them with Haive agents for specialized functionality.
"""

import asyncio
import contextlib
from datetime import datetime
from typing import Any

from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# === CUSTOM TOOL EXAMPLES ===


@tool
def get_current_time() -> str:
    """Get the current date and time.

    Returns:
        Current timestamp in readable format
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def temperature_converter(
    temperature: float, from_unit: str = "celsius", to_unit: str = "fahrenheit"
) -> str:
    """Convert temperature between different units.

    Args:
        temperature: Temperature value to convert
        from_unit: Source unit (celsius, fahrenheit, kelvin)
        to_unit: Target unit (celsius, fahrenheit, kelvin)

    Returns:
        Converted temperature with unit
    """
    # Convert to Celsius first
    if from_unit.lower() == "fahrenheit":
        celsius = (temperature - 32) * 5 / 9
    elif from_unit.lower() == "kelvin":
        celsius = temperature - 273.15
    else:  # celsius
        celsius = temperature

    # Convert from Celsius to target
    if to_unit.lower() == "fahrenheit":
        result = (celsius * 9 / 5) + 32
        unit = "°F"
    elif to_unit.lower() == "kelvin":
        result = celsius + 273.15
        unit = "K"
    else:  # celsius
        result = celsius
        unit = "°C"

    return f"{result:.2f}{unit}"


class TaskInput(BaseModel):
    """Input schema for task management tool."""

    task: str = Field(..., description="Task description")
    priority: str = Field("medium", description="Priority level (low/medium/high)")
    due_date: str = Field(None, description="Due date (YYYY-MM-DD)")


# Global task storage for this example
TASK_LIST: list[dict[str, Any]] = []


@tool(args_schema=TaskInput)
def add_task(task: str, priority: str = "medium", due_date: str | None = None) -> str:
    """Add a new task to the task list.

    Args:
        task: Description of the task
        priority: Priority level (low, medium, high)
        due_date: Optional due date in YYYY-MM-DD format

    Returns:
        Confirmation message with task ID
    """
    task_id = len(TASK_LIST) + 1
    new_task = {
        "id": task_id,
        "task": task,
        "priority": priority,
        "due_date": due_date,
        "created": datetime.now().isoformat(),
        "completed": False,
    }
    TASK_LIST.append(new_task)
    return f"✅ Task #{task_id} added: '{task}' (Priority: {priority})"


@tool
def list_tasks() -> str:
    """List all current tasks.

    Returns:
        Formatted list of all tasks
    """
    if not TASK_LIST:
        return "📝 No tasks found."

    result = "📋 Current Tasks:\n"
    for task in TASK_LIST:
        status = "✅" if task["completed"] else "⏳"
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        emoji = priority_emoji.get(task["priority"], "⚪")

        result += f"{status} #{task['id']}: {task['task']} {emoji}\n"
        if task["due_date"]:
            result += f"   📅 Due: {task['due_date']}\n"

    return result.strip()


@tool
def text_analyzer(text: str) -> str:
    """Analyze text for various metrics and characteristics.

    Args:
        text: Text to analyze

    Returns:
        Comprehensive text analysis
    """
    words = text.split()
    sentences = text.split(".")

    # Count various elements
    word_count = len(words)
    char_count = len(text)
    sentence_count = len([s for s in sentences if s.strip()])
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

    # Analyze word lengths
    word_lengths = [len(word.strip('.,!?;:"()[]{}')) for word in words]
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    # Find longest and shortest words
    longest_word = max(words, key=len) if words else ""
    shortest_word = min(words, key=len) if words else ""

    analysis = f"""📊 Text Analysis Results:
📝 Basic Metrics:
   • Words: {word_count}
   • Characters: {char_count}
   • Sentences: {sentence_count}
   • Paragraphs: {paragraph_count}

📏 Word Analysis:
   • Average word length: {avg_word_length:.1f} characters
   • Longest word: "{longest_word}" ({len(longest_word)} chars)
   • Shortest word: "{shortest_word}" ({len(shortest_word)} chars)

📈 Readability:
   • Words per sentence: {word_count / sentence_count:.1f}
   • Characters per word: {char_count / word_count:.1f}"""

    return analysis


async def main():
    """Run the custom tools example."""
    # Create agent configuration
    config = AugLLMConfig(
        model="gpt-4",
        temperature=0.4,
        system_message=(
            "You are a helpful assistant with access to custom tools. "
            "Use the tools to help users with various tasks including "
            "time queries, temperature conversion, task management, and text analysis."
        ),
    )

    # Create custom tools list
    custom_tools = [
        get_current_time,
        temperature_converter,
        add_task,
        list_tasks,
        text_analyzer,
    ]

    # Create ReactAgent with custom tools
    agent = ReactAgent(name="custom_tools_agent", engine=config, tools=custom_tools)

    for _custom_tool in custom_tools:
        pass

    # Example tasks using custom tools
    tasks = [
        "What's the current time?",
        "Convert 25 degrees Celsius to Fahrenheit",
        "Add a high priority task to 'Finish documentation examples' due 2024-01-20",
        "Add a medium priority task to 'Review agent performance'",
        "Show me all my current tasks",
        "Analyze this text: 'The Haive framework enables developers to build sophisticated AI agents with ease. It provides a comprehensive toolkit for creating conversational agents, game-playing AI, and complex multi-agent systems.'",
        "Convert 100 Fahrenheit to Kelvin",
    ]

    for _i, task in enumerate(tasks, 1):
        with contextlib.suppress(Exception):
            await agent.arun(task)

        # Small delay between tasks
        await asyncio.sleep(1.5)

    # Show final task list
    list_tasks()


if __name__ == "__main__":
    asyncio.run(main())
