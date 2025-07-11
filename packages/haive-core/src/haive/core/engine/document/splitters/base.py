from typing import List

from langchain.document_loaders.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from haive.core.engine.base.base import InvokableEngine

"""Kept for backwards compatibility."""

from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
    TextSplitter,
    Tokenizer,
    TokenTextSplitter,
)
from langchain_text_splitters.base import split_text_on_tokens
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_text_splitters.html import ElementType, HTMLHeaderTextSplitter
from langchain_text_splitters.json import RecursiveJsonSplitter
from langchain_text_splitters.konlpy import KonlpyTextSplitter
from langchain_text_splitters.latex import LatexTextSplitter
from langchain_text_splitters.markdown import (
    HeaderType,
    LineType,
    MarkdownHeaderTextSplitter,
    MarkdownTextSplitter,
)
from langchain_text_splitters.nltk import NLTKTextSplitter
from langchain_text_splitters.python import PythonCodeTextSplitter
from langchain_text_splitters.sentence_transformers import (
    SentenceTransformersTokenTextSplitter,
)
from langchain_text_splitters.spacy import SpacyTextSplitter

__all__ = [
    "TokenTextSplitter",
    "TextSplitter",
    "Tokenizer",
    "Language",
    "RecursiveCharacterTextSplitter",
    "RecursiveJsonSplitter",
    "LatexTextSplitter",
    "PythonCodeTextSplitter",
    "KonlpyTextSplitter",
    "SpacyTextSplitter",
    "NLTKTextSplitter",
    "split_text_on_tokens",
    "SentenceTransformersTokenTextSplitter",
    "ElementType",
    "HeaderType",
    "LineType",
    "HTMLHeaderTextSplitter",
    "MarkdownHeaderTextSplitter",
    "MarkdownTextSplitter",
    "CharacterTextSplitter",
]


class BaseTextSplitter(InvokableEngine[List[Document], List[Document]]):
    """
    A base class for text splitters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
