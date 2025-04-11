
import os

from src.config.config import Config    
if not Config.DATAFORSEO_LOGIN or not    Config.DATAFORSEO_PASSWORD:
    raise ValueError("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set")

from langchain_community.utilities.dataforseo_api_search import DataForSeoAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools


dataforseo = DataForSeoAPIWrapper()
result = dataforseo.run("https://python.langchain.com/docs/integrations/tools/dataforseo/")
print(result)

dataforseo_tools = load_tools(["dataforseo-api"])
print(dataforseo_tools)