Creating Custom Tools
=====================

While Haive provides many built-in tools, you'll often need to create custom tools specific to your use case.

This guide walks you through creating your own tools and organizing them into toolkits.

Tool Basics

-----------

A Haive tool consists of:

1. **Input Scheme*a**: Defines the parameters the tool accepts*

2.*** *Logi**c*: The code that executes when the tool is called

3.*** *Output Scheme**a*: Defines the structure of the tool's response

Creating a Simple Tool

----------------------

Here's how to create a basic custom tool:

.. code-block:: python

    # Code example here

    from pydantic import BaseModel, Field
    from haive.tools.base import BaseTool

    # Define input schema
    class WeatherInput(BaseModel):
    location: str = Field(..., description="City and country")
    units: str = Field("metric", description="Temperature units (metric/imperial)")

    # Define output schema
    class WeatherOutput(BaseModel):
    temperature: float = Field(..., description="Current temperature")
    conditions: str = Field(..., description="Weather conditions")
    humidity: int = Field(..., description="Humidity percentage")

    # Create the tool
    class WeatherTool(BaseTool):
    name = "weather_lookup"
    description = "Gets current weather for a location"
    input_schema = WeatherInput
    output_schema = WeatherOutput

    def _run(self, location: str, units: str = "metric") -> WeatherOutput:
    # Implementation to fetch weather data
    # This could call an API, use a library, etc.

    # Example implementation (replace with real API call)
    if location.lower() == "london, uk":
    return WeatherOutput(
    temperature=18.5,
    conditions="Partly cloudy",
    humidity=72
    )

    # Handle other locations or errors
    return WeatherOutput(
    temperature=20.0,
    conditions="Unknown",
    humidity=50
    )

    Tool Best Practices


-------------------

    When creating custom tools:

    1.*** *Clear Description**n*: Write clear descriptions for your tool and parameters

    2.*** *Input Validatio**n*: Use Pydantic models to validate inputs

    3.*** *Error Handling**g*: Gracefully handle errors and edge cases
    4.*** *Asynchronous Support**t*: For improved performance, consider implementing ``_arun``
    5.*** *Documentatio**n*: Document your tool's purpose, inputs, outputs, and limitations

    Creating Tool Kits

    ------------------

    Related tools can be organized into toolkits:

.. code-block:: python

    # Code example here

    from haive.tools.base import BaseToolkit

    class WeatherToolkit(BaseToolkit):
    name = "weather_tools"
    description = "Tools for retrieving weather information"

    def get_tools(self):
    return [
    WeatherTool(),
    ForecastTool(),
    HistoricalWeatherTool()
    ]

    Registering Custom Tools


------------------------

    To make your tools available throughout your application:

.. code-block:: python

    # Code example here

    from haive.core.registry import tool_registry

    # Register a single tool
    tool_registry.register(WeatherTool())

    # Register a toolkit
    tool_registry.register(WeatherToolkit())

    Using Environment Variables and Configuration


---------------------------------------------

    For API keys and configuration:

.. code-block:: python

    # Code example here

    import os
    from haive.core.config import settings

    class GoogleSearchTool(BaseTool):
    name = "google_search"

    def __init__(self):
    self.api_key = os.getenv("GOOGLE_API_KEY") or settings.google_api_key

    def _run(self, query: str):
    # Use self.api_key to authenticate API request
    # ...

    Testing Custom Tools


--------------------

    Always write tests for your custom tools:

.. code-block:: python

    # Code example here

    def test_weather_tool():
    tool = WeatherTool()
    result = tool.run(location="London, UK")

    assert isinstance(result, WeatherOutput)
    assert isinstance(result.temperature, float)
    assert isinstance(result.conditions, str)
    assert isinstance(result.humidity, int)

    Next Steps


----------

    Now that you can create custom tools:

    - Learn about :doc:`tool_routing for advanced tool usage patterns`

    - Review the :mod:``haive.tools.base API for more tool customization options``
    - Explore :mod:``haive.core.registry to understand tool registration***``
