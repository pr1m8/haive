from collections.abc import Iterable

from langchain_core.documents import Document


def save_docs_to_jsonl(array: Iterable[Document], file_path: str) -> None:
    with open(file_path, "w") as jsonl_file:
        for doc in array:
            jsonl_file.write(doc.json() + "\n")


# Post-processing
def format_docs(docs: Iterable[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def clean_page_content(doc: Document) -> str:
    """Clean the page content by removing new lines and tabs"""
    page_content = doc.page_content.replace("\n", " ")
    page_content = page_content.replace("\t", " ")
    return page_content


def combine_docs(docs: Iterable[Document]) -> Document:
    """Combine a list of documents into a single document"""
    return Document(page_content="\n\n".join(doc.page_content for doc in docs))


def clean_and_format_text(text: str) -> str:
    """Clean raw text input (as string) by removing newlines and tabs."""
    return text.replace("\n", " ").replace("\t", " ")
