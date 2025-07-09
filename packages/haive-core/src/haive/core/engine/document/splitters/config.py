from enum import Enum

__all__ = [
    "DocSplitterType",
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


class DocSplitterType(str, Enum):
    """Document splitter types available in the system."""
    
    NLTK = 'nltk'
    CHARACTER = 'character'
    RECURSIVE_CHARACTER = 'recursive_character'
    HTML = 'html'
    MARKDOWN = 'markdown'
    JSON = 'json'
    LATEX = 'latex'
    PYTHON = 'python'
    KONLPY = 'konlpy'
    SPACY = 'spacy'
    SENTENCE_TRANSFORMERS = 'sentence_transformers'
    TOKEN = 'token'
    TEXT = 'text'