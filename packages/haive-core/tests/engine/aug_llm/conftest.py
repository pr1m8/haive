# tests/core/engine/aug_llm/conftest.py

import os

import pytest
from langchain_core.messages import SystemMessage  # , MessagesPlaceholder
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.core.models.llm.base import AzureLLMConfig, OpenAILLMConfig


# Skip tests if API keys aren't available
def check_api_keys():
    """Check if necessary API keys are available in environment."""
    api_keys = {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    }

    return any(api_keys.values())


# Test skipping decorator
skip_if_no_api_keys = pytest.mark.skipif(
    not check_api_keys(), reason="No API keys available for LLM testing"
)


# Define structured output models for testing
class Person(BaseModel):
    """Model representing a person."""

    name: str = Field(description="The person's full name")
    age: int | None = Field(None, description="The person's age in years")
    occupation: str | None = Field(None, description="The person's job or profession")
    location: str | None = Field(None, description="Where the person lives")


class ExtractedEvent(BaseModel):
    """Model representing an event with date, time, location."""

    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Date of the event (YYYY-MM-DD)")
    time: str | None = Field(None, description="Time of the event (HH:MM)")
    location: str | None = Field(None, description="Location of the event")
    attendees: list[str] | None = Field(None, description="List of people attending")


class WeatherQuery(BaseModel):
    """Model for weather query."""

    location: str = Field(description="The location to get weather for")
    date: str | None = Field(
        None, description="The date to get weather for (defaults to current)"
    )


# Test fixtures
@pytest.fixture
def azure_llm_config():
    """Create Azure LLM config for testing."""
    return AzureLLMConfig(
        model="gpt-4o", temperature=0.0, max_tokens=1000  # Deterministic for testing
    )


@pytest.fixture
def openai_llm_config():
    """Create OpenAI LLM config for testing."""
    return OpenAILLMConfig(
        model="gpt-4o", temperature=0.0, max_tokens=1000  # Deterministic for testing
    )


@pytest.fixture
def simple_chat_prompt():
    """Create a simple chat prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful AI assistant."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


@pytest.fixture
def structured_chat_prompt():
    """Create a structured chat prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a data extraction assistant. Extract the requested information from the user's query.
        Return only the structured data with no explanations.
        """
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


@pytest.fixture
def weather_tool():
    """Create a weather lookup tool."""

    @tool
    def get_weather(location: str) -> str:
        """Look up the current weather for a location."""
        # Simulate weather data
        weather_data = {
            "New York": "Sunny, 75°F",
            "London": "Rainy, 60°F",
            "Tokyo": "Cloudy, 70°F",
            "Sydney": "Clear, 80°F",
        }
        return weather_data.get(location, f"Weather data for {location} not available")

    return get_weather


@pytest.fixture
def calculator_tool():
    """Create a calculator tool."""

    @tool
    def calculator(expression: str) -> str:
        """Calculate the result of a mathematical expression."""
        try:
            # This is for testing only - would use a safer approach in production
            return str(eval(expression))
        except Exception as e:
            return f"Error: {e!s}"

    return calculator
