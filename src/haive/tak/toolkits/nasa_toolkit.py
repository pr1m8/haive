
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.nasa.toolkit import NasaToolkit
from langchain_community.utilities.nasa import NasaAPIWrapper


nasa_api_wrapper = NasaAPIWrapper()
nasa_toolkit = NasaToolkit.from_nasa_api_wrapper(nasa_api_wrapper)
