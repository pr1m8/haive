from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
import requests

BASE_URL = "https://openlibrary.org"

### ---- Tool 1: Search for books ---- ###
class BookSearchInput(BaseModel):
    query: str = Field(..., description="The book title, keywords, or search query")
    page: int = Field(default=1, description="Page number of results")

def search_books(query: str, page: int = 1) -> dict:
    url = f"{BASE_URL}/search.json"
    params = {"q": query, "page": page}
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    return {
        "num_results": data.get("numFound"),
        "books": [
            {
                "title": doc.get("title"),
                "author": ", ".join(doc.get("author_name", [])),
                "first_publish_year": doc.get("first_publish_year"),
                "olid": doc.get("key").split("/")[-1] if doc.get("key") else None,
            }
            for doc in data.get("docs", [])[:5]
        ]
    }

search_books_tool = StructuredTool.from_function(
    func=search_books,
    name="search_books_openlibrary",
    description="Search for books by title, keyword, or subject using OpenLibrary",
    args_schema=BookSearchInput
)


### ---- Tool 2: Search for authors ---- ###
class AuthorSearchInput(BaseModel):
    name: str = Field(..., description="Name of the author to search for")

def search_authors(name: str) -> dict:
    url = f"{BASE_URL}/search/authors.json"
    params = {"q": name}
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    return {
        "authors": [
            {
                "name": doc.get("name"),
                "birth_date": doc.get("birth_date"),
                "top_work": doc.get("top_work"),
                "work_count": doc.get("work_count"),
                "olid": doc.get("key").split("/")[-1] if doc.get("key") else None,
            }
            for doc in data.get("docs", [])[:5]
        ]
    }

search_authors_tool = StructuredTool.from_function(
    func=search_authors,
    name="search_authors_openlibrary",
    description="Search for authors by name using OpenLibrary",
    args_schema=AuthorSearchInput
)


### ---- Tool 3: Get Cover Image URL ---- ###
class CoverInput(BaseModel):
    olid: str = Field(..., description="The OpenLibrary ID for a book or author")
    is_author: bool = Field(default=False, description="Set to true if the OLID is for an author")

def get_cover_image_url(olid: str, is_author: bool = False) -> str:
    prefix = "a" if is_author else "b"
    return f"https://covers.openlibrary.org/{prefix}/olid/{olid}-M.jpg"

get_cover_image_tool = StructuredTool.from_function(
    func=get_cover_image_url,
    name="get_openlibrary_cover_image",
    description="Get the cover image URL from an OpenLibrary ID (for book or author)",
    args_schema=CoverInput
)

open_library_tools = [search_books_tool, search_authors_tool, get_cover_image_tool]