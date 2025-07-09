# src/haive/agents/person_research/utils.py

from typing import Any


def deduplicate_and_format_sources(
    search_response: Any, max_tokens_per_source: int, include_raw_content: bool = True
) -> str:
    """Takes either a single search response or list of responses from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.

    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results
        max_tokens_per_source: Maximum number of tokens per source
        include_raw_content: Whether to include the raw_content from Tavily

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
    unique_sources = {}
    for source in sources_list:
        if source["url"] not in unique_sources:
            unique_sources[source["url"]] = source

    # Format output
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
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
    """Format a list of notes into a string.

    Args:
        completed_notes: List of notes to format

    Returns:
        str: Formatted notes
    """
    formatted_str = ""
    for idx, people_notes in enumerate(completed_notes, 1):
        formatted_str += f"""
{'='*60}
People {idx}:
{'='*60}
Notes from research:
{people_notes}"""

    return formatted_str


def get_config_from_runnable_config(config: dict[str, Any]) -> dict[str, Any]:
    """Extract configuration values from a runnable config.

    Args:
        config: Runnable configuration

    Returns:
        dict: Configuration values
    """
    if not config or "configurable" not in config:
        return {}

    configurable = config["configurable"]
    return {
        "max_search_queries": configurable.get("max_search_queries", 3),
        "max_search_results": configurable.get("max_search_results", 3),
        "max_reflection_steps": configurable.get("max_reflection_steps", 0),
    }
