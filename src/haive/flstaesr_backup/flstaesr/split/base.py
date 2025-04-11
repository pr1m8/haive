from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

from langchain_text_splitters import (
    Language,
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    PythonCodeTextSplitter,
    MarkdownTextSplitter,
    MarkdownHeaderTextSplitter,
    ExperimentalMarkdownSyntaxTextSplitter,
    LatexTextSplitter,
    RecursiveJsonSplitter,
    HTMLHeaderTextSplitter,
    HTMLSectionSplitter,
    HTMLSemanticPreservingSplitter,
    JSFrameworkTextSplitter,
    NLTKTextSplitter,
    SpacyTextSplitter,
    KonlpyTextSplitter,
    SentenceTransformersTokenTextSplitter,
    TokenTextSplitter,
)

class TextSplitterType(str, Enum):
    RECURSIVE_CHARACTER = "recursive_character"
    CHARACTER = "character"
    PYTHON_CODE = "python_code"
    MARKDOWN = "markdown"
    MARKDOWN_HEADER = "markdown_header"
    MARKDOWN_SYNTAX = "markdown_syntax"
    LATEX = "latex"
    JSON = "json"
    HTML_HEADER = "html_header"
    HTML_SECTION = "html_section"
    HTML_SEMANTIC = "html_semantic"
    JS_FRAMEWORK = "js_framework"
    NLTK = "nltk"
    SPACY = "spacy"
    KONLPY = "konlpy"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    TOKEN = "token"

class TextSplitterConfig(BaseModel):
    splitter_type: TextSplitterType = Field(default=TextSplitterType.RECURSIVE_CHARACTER)
    chunk_size: int = Field(default=512)
    chunk_overlap: int = Field(default=50)
    language: Optional[str] = None
    file_type: Optional[str] = None

    def resolve_language(self) -> Optional[Language]:
        if self.language:
            return Language(self.language)
        if self.file_type:
            ext_map = {
                "py": "python", "js": "js", "ts": "ts", "java": "java", "kt": "kotlin",
                "cpp": "cpp", "c": "c", "cs": "csharp", "rb": "ruby", "rs": "rust",
                "go": "go", "md": "markdown", "html": "html", "xml": "html", "sol": "sol",
                "tex": "latex", "php": "php", "proto": "proto", "lua": "lua",
                "pl": "perl", "hs": "haskell", "rst": "rst", "cbl": "cobol", "ps1": "powershell"
            }
            lang_str = ext_map.get(self.file_type.strip(".").lower())
            if lang_str:
                return Language(lang_str)
        return None

    def create_splitter(self):
        kwargs = {"chunk_size": self.chunk_size, "chunk_overlap": self.chunk_overlap}
        lang = self.resolve_language()

        if self.splitter_type == TextSplitterType.RECURSIVE_CHARACTER:
            return RecursiveCharacterTextSplitter.from_language(language=lang, **kwargs) if lang else RecursiveCharacterTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.CHARACTER:
            return CharacterTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.PYTHON_CODE:
            return PythonCodeTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.MARKDOWN:
            return MarkdownTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.MARKDOWN_HEADER:
            return MarkdownHeaderTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.MARKDOWN_SYNTAX:
            return ExperimentalMarkdownSyntaxTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.LATEX:
            return LatexTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.JSON:
            return RecursiveJsonSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.HTML_HEADER:
            return HTMLHeaderTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.HTML_SECTION:
            return HTMLSectionSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.HTML_SEMANTIC:
            return HTMLSemanticPreservingSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.JS_FRAMEWORK:
            return JSFrameworkTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.NLTK:
            return NLTKTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.SPACY:
            return SpacyTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.KONLPY:
            return KonlpyTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.SENTENCE_TRANSFORMERS:
            return SentenceTransformersTokenTextSplitter(**kwargs)
        elif self.splitter_type == TextSplitterType.TOKEN:
            return TokenTextSplitter(**kwargs)

        raise ValueError(f"Unsupported splitter type: {self.splitter_type}")
