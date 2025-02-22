from langchain_community.document_loaders import WeatherDataLoader
from langchain.tools import tool
from typing import Optional,List,Dict
import os
import asyncio


@tool
def load_weather_data(
    city: str,
    country: str,
    api_key: str
) -> List[Dict]:
    """Load weather data for a specific city and country."""
    loader = WeatherDataLoader.from_params(places=[city],
                                           openweathermap_api_key=api_key)
    return loader.load()




