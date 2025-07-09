from haive.core.tools.search_tools import tavily_search
from langchain_core.tools import tool


@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]
