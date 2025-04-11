"""
LangChain-compatible weather tool using city and country input.
Supports structured output and Celsius/Fahrenheit conversion.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
from langchain_community.agent_toolkits.load_tools import load_tools
from src.config.config import Config
import os
import getpass
import re


# --- Input Schema ---
class CityCountryWeatherInput(BaseModel):
    city: str = Field(..., description="City name, e.g. 'Tokyo'")
    country: str = Field(..., description="2-letter country code in lowercase, e.g. 'jp'")
    parse: bool = Field(default=True, description="Whether to parse structured weather data")
    temperature_unit: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", description="Return temperatures in Celsius or Fahrenheit"
    )


# --- Output Model ---
class WeatherData(BaseModel):
    location: Optional[str]
    status: Optional[str]
    wind_speed_mps: Optional[float]
    wind_direction_deg: Optional[int]
    humidity_percent: Optional[int]
    temp_current_c: Optional[float]
    temp_high_c: Optional[float]
    temp_low_c: Optional[float]
    temp_feels_like_c: Optional[float]
    rain_mm_last_hour: Optional[float]
    cloud_cover_percent: Optional[int]

    def convert_to_fahrenheit(self) -> "WeatherData":
        def c_to_f(c: Optional[float]) -> Optional[float]:
            return round(c * 9 / 5 + 32, 2) if c is not None else None

        return WeatherData(
            **self.dict(exclude={
                "temp_current_c", "temp_high_c", "temp_low_c", "temp_feels_like_c"
            }),
            temp_current_c=c_to_f(self.temp_current_c),
            temp_high_c=c_to_f(self.temp_high_c),
            temp_low_c=c_to_f(self.temp_low_c),
            temp_feels_like_c=c_to_f(self.temp_feels_like_c),
        )

    @classmethod
    def from_openweather_response(cls, response: str) -> "WeatherData":
        data = {}

        if match := re.search(r"In (.+?), the current weather is as follows:", response):
            data["location"] = match.group(1).strip()

        if match := re.search(r"Detailed status: (.+)", response):
            data["status"] = match.group(1).strip()

        if match := re.search(r"Wind speed: ([\d.]+) m/s, direction: (\d+)°", response):
            data["wind_speed_mps"] = float(match.group(1))
            data["wind_direction_deg"] = int(match.group(2))

        if match := re.search(r"Humidity: (\d+)%", response):
            data["humidity_percent"] = int(match.group(1))

        if match := re.search(
            r"Temperature:\s+- Current: ([\d.]+)°C\s+- High: ([\d.]+)°C\s+- Low: ([\d.]+)°C\s+- Feels like: ([\d.]+)°C",
            response,
            re.DOTALL
        ):
            data["temp_current_c"] = float(match.group(1))
            data["temp_high_c"] = float(match.group(2))
            data["temp_low_c"] = float(match.group(3))
            data["temp_feels_like_c"] = float(match.group(4))

        if match := re.search(r"Rain: \{[^}]*'1h': ([\d.]+)[^}]*\}", response):
            data["rain_mm_last_hour"] = float(match.group(1))

        if match := re.search(r"Cloud cover: (\d+)%", response):
            data["cloud_cover_percent"] = int(match.group(1))

        return cls(**data)


# --- Tool Function ---
def get_weather_by_city_country(
    city: str,
    country: str,
    parse: bool = True,
    temperature_unit: Literal["celsius", "fahrenheit"] = "celsius"
):
    """Fetch weather using city and country components as input."""

    if not Config.OPENWEATHERMAP_API_KEY:
        os.environ["OPENWEATHERMAP_API_KEY"] = getpass.getpass("Enter your OpenWeatherMap API Key: ")

    location = f"{city},{country}"
    tool = load_tools(["openweathermap-api"])[0]
    result = tool.run(location)

    if parse:
        data = WeatherData.from_openweather_response(result)
        if temperature_unit == "fahrenheit":
            data = data.convert_to_fahrenheit()
        return data.model_dump()

    return result


# --- Exported Tool ---
weather_tool = StructuredTool.from_function(
    func=get_weather_by_city_country,
    name="get_weather_by_city_country",
    description="Fetch current weather using city and 2-letter country code with optional structured output",
    args_schema=CityCountryWeatherInput,
    return_direct=True
)
