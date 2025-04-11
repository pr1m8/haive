from langchain_community.utilities import StackExchangeAPIWrapper
from langchain.agents import load_tools

stackexchange_tools = load_tools(["stackexchange"])

