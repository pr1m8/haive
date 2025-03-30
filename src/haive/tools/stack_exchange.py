from langchain_community.utilities import StackExchangeAPIWrapper
from src.config.config import Config
from langchain_community.tools.stackexchange.tool import StackExchangeTool

stackexchange_tool=[StackExchangeTool(api_wrapper=StackExchangeAPIWrapper())]

