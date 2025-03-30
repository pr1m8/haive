#https://python.langchain.com/api_reference/_modules/langchain_community/utilities/brave_search.html#BraveSearchWrapper

from langchain_community.utilities.brave_search import BraveSearchWrapper
from langchain_community.agent_toolkits import load_tools


brave_search_tool = load_tools(["brave-search"])