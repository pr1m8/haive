from langchain_community.document_loaders import HuggingFaceModelLoader, HuggingFaceDatasetLoader
from langchain.tools import tool
from typing import Optional, List, Dict

@tool
def load_huggingface_models(
    search: Optional[str] = None,
    author: Optional[str] = None,
    filter: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    limit: Optional[int] = 3,
    full: Optional[bool] = None,
    config: Optional[bool] = None
) -> List[Dict]:
    """
    Load model information from Hugging Face Hub, including README content.

    Args:
        search: Filter based on substrings for repos and their usernames.
        author: Filter models by an author or organization.
        filter: Filter based on tags.
        sort: Property to use when sorting.
        direction: Direction in which to sort.
        limit: Limit the number of models fetched.
        full: Whether to fetch most model data.
        config: Whether to also fetch the repo config.

    Returns:
        A list of dictionaries containing model metadata and README content.
    """
    loader = HuggingFaceModelLoader(
        search=search,
        author=author,
        filter=filter,
        sort=sort,
        direction=direction,
        limit=limit,
        full=full,
        config=config
    )
    documents = list(loader.lazy_load())
    return [{"metadata": doc.metadata, "content": doc.page_content} for doc in documents]

@tool
def load_huggingface_datasets(
    search: Optional[str] = None,
    author: Optional[str] = None,
    filter: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    limit: Optional[int] = 3,
    full: Optional[bool] = None,
    config: Optional[bool] = None
) -> List[Dict]:
    """
    Load dataset information from Hugging Face Hub, including README content.

    Args:
        search: Filter based on substrings for repos and their usernames.
        author: Filter datasets by an author or organization.
        filter: Filter based on tags.
        sort: Property to use when sorting.
        direction: Direction in which to sort.
        limit: Limit the number of datasets fetched.
        full: Whether to fetch most dataset data.
        config: Whether to also fetch the repo config.

    Returns:
        A list of dictionaries containing dataset metadata and README content.
    """
    loader = HuggingFaceDatasetLoader(
        search=search,
        author=author,
        filter=filter,
        sort=sort,
        direction=direction,
        limit=limit,
        full=full,
        config=config
    )
    documents = list(loader.lazy_load())
    return [{"metadata": doc.metadata, "content": doc.page_content} for doc in documents]
