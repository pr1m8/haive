from enum import Enum


class LoadMethod(str, Enum):
    """Methods for loading documents."""

    LOAD = "load"  # Basic document loading
    LOAD_AND_SPLIT = "load_and_split"  # Load and split documents
    FETCH_ALL = "fetch_all"  # Fetch all available sources and load documents
