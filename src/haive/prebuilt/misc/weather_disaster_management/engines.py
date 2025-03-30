from src.haive.prebuilt.misc.weather_disaster_management.prompts import (
    disaster_prompt,
    severity_prompt,
    response_prompt,
    civil_defense_prompt,
    public_works_prompt,
    social_media_monitoring_prompt
)
from src.haive.prebuilt.misc.weather_disaster_management.models import DisasterOutput, SeverityAssessment
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.agents.react_agent2.config2 import ReactAgentConfig
from src.haive.tools.search_tools import tavily_search_tool

disaster_engine = AugLLMConfig(
    prompt_template=disaster_prompt,
    structured_output_model=DisasterOutput,
)

severity_engine = AugLLMConfig(
    prompt_template=severity_prompt,
    structured_output_model=SeverityAssessment,
)

response_engine = AugLLMConfig(
    prompt_template=response_prompt,
    #structured_output=ResponseOutput,
)

civil_defense_engine = AugLLMConfig(
    prompt_template=civil_defense_prompt,
    #structured_output=CivilDefenseOutput,
)

public_works_engine = AugLLMConfig(
    prompt_template=public_works_prompt,
    #structured_output=PublicWorksOutput,
)

social_media_monitoring_engine = ReactAgentConfig(
    prompt_template=social_media_monitoring_prompt,
    tools=[tavily_search_tool],
    #structured_output=SocialMediaMonitoringOutput,
)
