import json
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from langchain_core.documents import Document


def save_docs_to_jsonl(docs: Iterable[Document], file_path: str) -> None:
    """Save a list of LangChain Document objects to a JSONL file.

    Each document is serialized using its `.json()` method.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.json() + "\n")


def clean_text(text: str) -> str:
    """Remove newlines and tabs from a string."""
    return text.replace("\n", " ").replace("\t", " ")


def clean_page_content(doc: Document) -> str:
    """Clean the `page_content` of a Document by removing newlines and tabs."""
    return clean_text(doc.page_content)


def combine_docs(docs: Iterable[Document]) -> Document:
    """Combine a list of Documents into a single Document."""
    combined_content = "\n\n".join(doc.page_content for doc in docs)
    return Document(page_content=combined_content)


def format_doc(doc: Document, max_length: int = 1000) -> str:
    """Format a single document into a Markdown-style summary.

    Includes the title, summary, and related categories.
    Truncates output to `max_length` characters.
    """
    title = doc.metadata.get("title", "Untitled")
    summary = clean_text(doc.page_content)
    related = doc.metadata.get("categories", [])
    related_str = "- " + "\n- ".join(related) if related else "None"

    formatted = f"### {title}\n\nSummary: {summary}\n\nRelated\n{related_str}"
    return formatted[:max_length]


def format_docs(docs: Iterable[Document], max_length: int | None = 1000) -> str:
    """Format multiple documents using `format_doc` and join with spacing."""
    return "\n\n".join(format_doc(doc, max_length=max_length) for doc in docs)
