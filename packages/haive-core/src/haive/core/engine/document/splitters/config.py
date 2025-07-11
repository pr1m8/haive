from enum import Enum

__all__ = [
    "CharacterTextSplitter",
    "DocSplitterType",
    "ElementType",
    "HTMLHeaderTextSplitter",
    "HeaderType",
    "KonlpyTextSplitter",
    "Language",
    "LatexTextSplitter",
    "LineType",
    "MarkdownHeaderTextSplitter",
    "MarkdownTextSplitter",
    "NLTKTextSplitter",
    "PythonCodeTextSplitter",
    "RecursiveCharacterTextSplitter",
    "RecursiveJsonSplitter",
    "SentenceTransformersTokenTextSplitter",
    "SpacyTextSplitter",
    "TextSplitter",
    "TokenTextSplitter",
    "Tokenizer",
    "split_text_on_tokens",
]


class DocSplitterType(str, Enum):
    """Document splitter types available in the system."""

    NLTK = "nltk"
    CHARACTER = "character"
    RECURSIVE_CHARACTER = "recursive_character"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    LATEX = "latex"
    PYTHON = "python"
    KONLPY = "konlpy"
    SPACY = "spacy"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    TOKEN = "token"
    TEXT = "text"
