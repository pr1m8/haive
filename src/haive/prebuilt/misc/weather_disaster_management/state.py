from typing import TypedDict, List, Union, Dict
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
#https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/Weather_Disaster_Management_AI_AGENT.ipynb
    
class WeatherLocation(BaseModel):
    """The location to get weather data for"""
    city:str = Field(..., description="The city to get weather data for")
    country:str = Field(..., description="The country to get weather data for")
    def __str__(self):
        return f"{self.city}, {self.country}"
    
class WeatherState(WeatherLocation,BaseModel):
    weather_data: Dict = Field(description="The weather data for the city")
    disaster_type: str = Field(description="The type of disaster to manage")
    severity: str = Field(description="The severity of the disaster")
    response: str = Field(description="The response to the disaster")
    messages: List[Union[SystemMessage, HumanMessage, AIMessage]] = Field(description="The messages to send to the user")
    alerts: List[str] = Field(description="The alerts to send to the user")
    human_approved: bool = Field(description="Whether the user has approved the response")
