from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.prebuilt.misc.weather_disaster_management.engines import disaster_engine, severity_engine, response_engine, civil_defense_engine, public_works_engine, social_media_monitoring_engine
from src.haive.core.engine.aug_llm import AugLLMConfig
from typing import Dict, Union
from pydantic import Field
from src.haive.core.graph.branches import Branch
from src.haive.prebuilt.misc.weather_disaster_management.engines import disaster_engine, severity_engine, response_engine, civil_defense_engine, public_works_engine, social_media_monitoring_engine
from src.haive.toolkits.weather import weather_tool
from langchain_core.tools import StructuredTool
from src.haive.prebuilt.misc.weather_disaster_management.branches import route_branch
from src.haive.prebuilt.misc.weather_disaster_management.state import WeatherState, WeatherLocation
from pydantic import BaseModel, ConfigDict

class WeatherDisasterManagerConfig(AgentConfig):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # ✅ Add this

    engines: Dict[str, Union[AugLLMConfig, AgentConfig]] = Field(default={
        "analyze_disaster_type": disaster_engine,
        "severity_engine": severity_engine,
        "response_engine": response_engine,
        "civil_defense_engine": civil_defense_engine,
        "public_works_engine": public_works_engine,
        "social_media_monitoring": social_media_monitoring_engine,
    })

    branches: Dict[str, Branch] = Field(default={
        "route_branch": route_branch,   
    })

    tools: Dict[str, StructuredTool] = Field(default={
        "weather_tool": weather_tool,
    })

    state_schema: BaseModel = WeatherState
    input_schema: BaseModel = WeatherLocation
    