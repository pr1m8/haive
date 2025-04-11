from typing import Optional, Literal, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import os
import dotenv

dotenv.load_dotenv('.env')

# DeepL-supported languages
DEEPL_TARGET_LANGUAGES = Literal[
    "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI",
    "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL",
    "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
]

DEEPL_SOURCE_LANGUAGES = Literal[
    "BG", "CS", "DA", "DE", "EL", "EN", "ES", "ET", "FI",
    "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL",
    "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
]

# Input Schema for Translation
class DeepLInput(BaseModel):
    text: str = Field(..., description="Text to translate")

# DeepL Translation Tool
class DeepLTranslateTool(BaseTool):
    """
    LangChain-compatible structured tool for translating text using the DeepL API.

    ✅ Supports both free and pro DeepL modes.
    ✅ Accepts structured input with source/target language codes.
    ✅ Validates language codes via Pydantic Literal types.
    """

    name: str = "deepl_translate"
    description: str = (
        "Translate text using DeepL API. "
        "Supports structured input and 'free' or 'pro' modes. "
        "Target language must be one of DeepL's supported codes."
    )

    target_lang: DEEPL_TARGET_LANGUAGES = Field(..., description="Target language (e.g., 'EN-US')")
    source_lang: Optional[DEEPL_SOURCE_LANGUAGES] = Field(default=None, description="Optional source language (e.g., 'FR')")
    mode: Literal["free", "pro"] = Field(default="free", description="DeepL API mode: 'free' or 'pro'")
    api_key: str = Field(default_factory=lambda: os.getenv("DEEPL_API_KEY", ""), description="Your DeepL API key")

    args_schema: Type[BaseModel] = DeepLInput

    def _run(self, text: str) -> str:
        try:
            import deepl

            server_url = "https://api-free.deepl.com" if self.mode == "free" else "https://api.deepl.com"
            translator = deepl.Translator(auth_key=self.api_key, server_url=server_url)

            result = translator.translate_text(
                text=text,
                target_lang=self.target_lang,
                source_lang=self.source_lang,
            )
            return result.text
        except Exception as e:
            return f"❌ DeepL error: {e}"

    def _arun(self, text: str) -> str:
        raise NotImplementedError("Async not supported for DeepLTranslateTool")


deepl_translate_tool=[DeepLTranslateTool]