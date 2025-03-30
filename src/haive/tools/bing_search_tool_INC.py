#https://python.langchain.com/docs/integrations/tools/bing_search/


from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from src.config.config import Config
if not Config.BING_SUBSCRIPTION_KEY:
    raise ValueError("BING_SUBSCRIPTION_KEY is not set")
elif not Config.BING_SEARCH_URL:
    bing_search_url="https://api.bing.microsoft.com/v7.0/search"
    raise ValueError("BING_SEARCH_URL is not set")



bing_search_tool=BingSearchAPIWrapper(bing_subscription_key=Config.BING_SUBSCRIPTION_KEY, bing_search_url=Config.BING_SEARCH_URL)


search_result=bing_search_tool.run("python")

print(search_result)