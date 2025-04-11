import requests
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


BASE_URL = "https://bible-api.com"
DATA_URL = "https://bible-api.com/data"


### TOOL 1: Query by natural language reference

class BibleQueryInput(BaseModel):
    reference: str = Field(..., description="A natural language reference like 'John 3:16', 'Matt 5:1-10', or 'Jude 1'")

def query_bible_by_reference(reference: str) -> str:
    response = requests.get(f"{BASE_URL}/{reference}")
    if not response.ok:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    return "\n".join([f"{v['book_name']} {v['chapter']}:{v['verse']}: {v['text'].strip()}" for v in data.get("verses", [])])

query_tool = StructuredTool.from_function(
    func=query_bible_by_reference,
    name="query_bible_by_reference",
    description="Look up one or more Bible verses using a human-readable reference",
    args_schema=BibleQueryInput
)


### TOOL 2: Random verse

class RandomVerseInput(BaseModel):
    book_ids: Optional[List[str]] = Field(default=None, description="List of book IDs like ['GEN', 'JHN'], or 'OT'/'NT'")

def get_random_verse(book_ids: Optional[List[str]] = None) -> str:
    book_path = ",".join(book_ids) if book_ids else ""
    url = f"{DATA_URL}/web/random/{book_path}" if book_path else f"{DATA_URL}/web/random"
    response = requests.get(url)
    if not response.ok:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    return f"{data['book_name']} {data['chapter']}:{data['verse']}: {data['text'].strip()}"

random_tool = StructuredTool.from_function(
    func=get_random_verse,
    name="get_random_bible_verse",
    description="Fetch a random verse, optionally from specific books or testaments",
    args_schema=RandomVerseInput
)


### TOOL 3: Get all translations

def list_translations() -> str:
    response = requests.get(f"{DATA_URL}")
    if not response.ok:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    return "\n".join([f"{t['id']}: {t['name']}" for t in data])

translations_tool = StructuredTool.from_function(
    func=list_translations,
    name="list_bible_translations",
    description="Get all available Bible translations"
)


### TOOL 4: Get books by translation

class TranslationBooksInput(BaseModel):
    translation_id: str = Field(..., description="Translation ID such as 'web', 'kjv', etc.")

def list_books(translation_id: str) -> str:
    response = requests.get(f"{DATA_URL}/{translation_id}")
    if not response.ok:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    return "\n".join([f"{b['id']}: {b['name']}" for b in data])

books_tool = StructuredTool.from_function(
    func=list_books,
    name="list_books_in_translation",
    description="List books in a specified translation",
    args_schema=TranslationBooksInput
)


### TOOL 5: Get verses in a chapter

class ChapterVersesInput(BaseModel):
    translation_id: str = Field(..., description="Translation ID (e.g., 'web')")
    book_id: str = Field(..., description="Book ID (e.g., 'JHN')")
    chapter: int = Field(..., description="Chapter number")

def get_chapter_verses(translation_id: str, book_id: str, chapter: int) -> str:
    url = f"{DATA_URL}/{translation_id}/{book_id}/{chapter}"
    response = requests.get(url)
    if not response.ok:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    return "\n".join([f"{v['verse']}: {v['text'].strip()}" for v in data.get("verses", [])])

chapter_tool = StructuredTool.from_function(
    func=get_chapter_verses,
    name="get_verses_in_chapter",
    description="Fetch all verses in a specific book chapter",
    args_schema=ChapterVersesInput
)


### Toolkit

vbible_toolkit = [
    query_tool,
    random_tool,
    translations_tool,
    books_tool,
    chapter_tool
]
# tests/test_vbible_toolkit.py
import pytest
from src.haive.toolkits.vbible_toolkit import (
    query_bible_by_reference,
    get_random_verse,
    list_translations,
    list_books,
    get_chapter_verses,
)

def test_query_single_verse():
    output = query_bible_by_reference("John 3:16")
    assert "John 3:16" in output

def test_query_multi_verse():
    output = query_bible_by_reference("Matt 5:1-3")
    assert "Matthew 5:1" in output
    assert "Matthew 5:3" in output

def test_get_random_verse():
    output = get_random_verse()
    assert isinstance(output, str)
    assert any(c.isdigit() for c in output)  # should contain chapter/verse

def test_list_translations():
    output = list_translations()
    assert "kjv" in output.lower()
    assert "web" in output.lower()

def test_list_books_for_translation():
    output = list_books("web")
    assert "GEN: Genesis" in output or "Genesis" in output

def test_get_verses_in_chapter():
    output = get_chapter_verses("web", "JHN", 3)
    assert "16: " in output  # John 3 has a verse 16
