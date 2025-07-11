from langchain_core.tools import tool

from haive.core.tools.search_tools import tavily_search


@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]
