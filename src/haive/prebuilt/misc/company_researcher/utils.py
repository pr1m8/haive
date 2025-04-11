

def deduplicate_sources(search_response: dict | list[dict]) -> list[dict]:
    """
    Takes either a single search response or list of responses from Tavily API and de-duplicates them based on the URL.

    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results

    Returns:
        str: Formatted string with deduplicated sources
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response["results"]
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and "results" in response:
                sources_list.extend(response["results"])
            else:
                sources_list.extend(response)
    else:
        raise ValueError(
            "Input must be either a dict with 'results' or a list of search results"
        )

    # Deduplicate by URL
    unique_urls = set()
    unique_sources_list = []
    for source in sources_list:
        if source["url"] not in unique_urls:
            unique_urls.add(source["url"])
            unique_sources_list.append(source)

    return unique_sources_list


def format_sources(
    sources_list: list[dict],
    include_raw_content: bool = True,
    max_tokens_per_source: int = 1000,
) -> str:
    """
    Takes a list of unique results from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    include_raw_content specifies whether to include the raw_content from Tavily in the formatted string.

    Args:
        sources_list: list of unique results from Tavily API
        max_tokens_per_source: int, maximum number of tokens per each search result to include in the formatted string
        include_raw_content: bool, whether to include the raw_content from Tavily in the formatted string

    Returns:
        str: Formatted string with deduplicated sources
    """
    # Format output
    formatted_text = "Sources:\n\n"
    for source in sources_list:
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += (
            f"Most relevant content from source: {source['content']}\n===\n"
        )
        if include_raw_content:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4
            # Handle None raw_content
            raw_content = source.get("raw_content", "")
            if raw_content is None:
                raw_content = ""
                print(f"Warning: No raw_content found for source {source['url']}")
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"

    return formatted_text.strip()


def format_all_notes(completed_notes: list[str]) -> str:
    """Format a list of notes into a string"""
    formatted_str = ""
    for idx, company_notes in enumerate(completed_notes, 1):
        formatted_str += f"""
{'='*60}
Note: {idx}:
{'='*60}
Notes from research:
{company_notes}"""
    return formatted_str