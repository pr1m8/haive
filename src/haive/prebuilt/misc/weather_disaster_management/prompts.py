from langchain_core.prompts import ChatPromptTemplate
# --- 3. Prompt Template ---
severity_prompt = ChatPromptTemplate.from_template(
    """You are a weather risk analyst.

Given the current weather conditions and the identified disaster type '{disaster_type}', assess the severity level.

Conditions:
- Description: {weather}
- Wind Speed: {wind_speed} m/s
- Temperature: {temperature}°C

Respond with only one of: "Critical", "High", "Medium", or "Low"
"""
)
# --- 3. Prompt Template ---
disaster_prompt = ChatPromptTemplate.from_template(
    """You are an expert in weather risk analysis.

Based on the following weather conditions, identify if there's a potential weather disaster.

Weather conditions:
- Description: {weather}
- Wind Speed: {wind_speed} m/s
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Pressure: {pressure} hPa

Respond ONLY with one of the following:
"Hurricane", "Flood", "Heatwave", "Severe Storm", "Winter Storm", or "No Immediate Threat"
"""
)


response_prompt = ChatPromptTemplate.from_template(
        "Create an emergency response plan for a {disaster_type} situation "
        "with {severity} severity level in {city}. Include immediate actions needed."
    )
civil_defense_prompt = ChatPromptTemplate.from_template(
        "Create a civil defense response plan for a {disaster_type} situation "
        "with {severity} severity level in {city}. Focus on public safety measures."
    )

public_works_prompt = ChatPromptTemplate.from_template(
        "Create a public works response plan for a {disaster_type} situation "
        "with {severity} severity level in {city}. Focus on infrastructure protection."
    )

social_media_monitoring_prompt = ChatPromptTemplate.from_template(
    "Monitor social media for {disaster_type} situation "
    "with {severity} severity level in {city}. Focus on public safety measures."
    "Provide a report on the situation and the public safety measures taken."
)