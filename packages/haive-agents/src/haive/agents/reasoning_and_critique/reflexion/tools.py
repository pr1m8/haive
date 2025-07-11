from langchain_community.tools import TavilySearchResults

# from haive_agents.reflexion.models import ReviseAnswer,
tavily_tool = TavilySearchResults(max_results=5)


def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries.

    Args:
        search_queries: A list of search queries to run.

    Returns:
        A list of search results.
    """
    return tavily_tool.batch([{"query": query} for query in search_queries])
