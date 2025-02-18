

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Type
from enum import Enum
from src.config.config import *
# Enum for supported LLM providers
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGING_FACE = "huggingface"
    AZURE = "azure"
    #DEEPSPEED = "deepspeed"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    COHERE = "cohere"
    AI21 = "ai21"
    ALEPH_ALPHA = "aleph_alpha"
    GOOSEAI = "gooseai"
    MOSAICML = "mosaicml"
    NLP_CLOUD = "nlp_cloud"
    OPENLM = "openlm"
    PETALS = "petals"
    REPLICATE = "replicate"
    TOGETHER_AI = "together_ai"


# Base LLM configuration
class LLMConfig(BaseModel):
    provider: LLMProvider = Field(description="The provider of the LLM.",default=LLMProvider.AZURE)
    model: str = Field(description="The model to be used, e.g., gpt-4.",default="gpt-4o")
    api_key: str = Field(description="The API key for the LLM provider.")
    cache_enabled: bool = Field(default=False, description="Enable or disable response caching.")
    cache_ttl: Optional[int] = Field(default=300, description="Time-to-live for cache (in seconds).")
    extra_params: Optional[Dict[str, Any]] = Field(default=None, description="Optional extra parameters for LLM configuration.")

    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def instantiate_llm(self, **kwargs) -> Any:
        """Factory method to create an LLM instance dynamically based on the provider."""
        raise NotImplementedError("This method should be overridden in subclasses.")
    def create_graph_transformer(self) -> Any:
        """Creates an LLMGraphTransformer instance using the Azure LLM."""
        from langchain_experimental.graph_transformers import LLMGraphTransformer
        llm = self.instantiate_llm()
        return LLMGraphTransformer(llm=llm)
    
    
    
# Azure-specific LLM configuration
class AzureLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.AZURE
    api_key: str = Field(default=os.getenv("AZURE_OPENAI_API_KEY"), description="Azure API key.")
    api_version: str = Field(default=os.getenv("AZURE_OPENAI_API_VERSION"), description="Azure API version.")
    api_base: str = Field(default=os.getenv("AZURE_OPENAI_API_BASE"), description="Azure API base URL.")
    api_type: str = Field(default=os.getenv("AZURE_OPENAI_API_TYPE"), description="API type for Azure OpenAI services.")
    api_endpoint: str = Field(default=os.getenv("AZURE_OPENAI_API_ENDPOINT"), description="Custom endpoint if needed (optional).")

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an Azure LLM instance using the provided config."""
        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            deployment_name=self.model,
            openai_api_key=self.api_key,
            openai_api_version=self.api_version,
            openai_api_base=self.api_base,
            openai_api_type=self.api_type,
            **(self.extra_params or {}),
            **kwargs
        )

    

# OpenAI-specific LLM configuration
class OpenAILLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.OPENAI

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an OpenAI LLM instance using the provided config."""
        from langchain_openai import OpenAIChat
        return OpenAIChat(
            model_name=self.model,
            openai_api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )

# Anthropic-specific LLM configuration
class AnthropicLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.ANTHROPIC

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an Anthropic LLM instance using the provided config."""
        from langchain_anthropic import AnthropicChat
        return AnthropicChat(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )

# Hugging Face-specific LLM configuration
class HuggingFaceLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.HUGGING_FACE
    endpoint: Optional[str] = Field(description="The Hugging Face endpoint for inference.")

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Hugging Face model instance using the provided config."""
        from huggingface_hub import InferenceAPI
        return InferenceAPI(
            repo_id=self.model,
            token=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class CohereLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.COHERE
    model: str = Field(default="command", description="Cohere model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Cohere LLM instance."""
        from langchain_cohere import ChatCohere
        return ChatCohere(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class AI21LLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.AI21
    model: str = Field(default="j2-ultra", description="AI21 model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an AI21 LLM instance."""
        from langchain_ai21 import ChatAI21
        return ChatAI21(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class AlephAlphaLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.ALEPH_ALPHA
    model: str = Field(default="luminous-base", description="Aleph Alpha model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an Aleph Alpha LLM instance."""
        from langchain_community.llms import ChatAlephAlpha
        return ChatAlephAlpha(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class GooseAILLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.GOOSEAI
    model: str = Field(default="gpt-neo-2.7B", description="GooseAI model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a GooseAI LLM instance."""
        from langchain_community.llms import ChatGooseAI
        return ChatGooseAI(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class MosaicMLLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.MOSAICML
    model: str = Field(default="mpt-7b", description="MosaicML model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a MosaicML LLM instance."""
        from langchain_community.llms import ChatMosaicML
        return ChatMosaicML(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class NLPCLOUDLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.NLP_CLOUD
    model: str = Field(default="finetuned-gpt-neo", description="NLP Cloud model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an NLP Cloud LLM instance."""
        from langchain_nlpcloud import ChatNLPCloud
        return ChatNLPCloud(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class OpenLMLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.OPENLM
    model: str = Field(default="gpt3-compatible", description="OpenLM model name.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates an OpenLM LLM instance."""
        from langchain_openlm import ChatOpenLM
        return ChatOpenLM(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class PetalsLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.PETALS
    model: str = Field(default="petals-bloom", description="Petals distributed model.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Petals LLM instance."""
        from langchain_community.llms import ChatPetals
        return ChatPetals(
            model=self.model,
            **(self.extra_params or {}),
            **kwargs
        )
class ReplicateLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.REPLICATE
    model: str = Field(default="meta/llama-2-7b", description="Replicate model identifier.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Replicate LLM instance."""
        from langchain_community.llms import ChatReplicate
        return ChatReplicate(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class TogetherAILLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.TOGETHER_AI
    model: str = Field(default="together-ai/gpt-j-6B", description="Together AI model.")
    
    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Together AI LLM instance."""
        from langchain_together import ChatTogether
        return ChatTogether(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class GeminiLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.GEMINI
    model: str = Field(default="gemini", description="The Gemini model to be used.")
    api_key: str = Field(description="The API key for the Gemini API.")

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a Gemini model instance using the provided config."""
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )
class DeepSeekLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.DEEPSEEK
    model: str = Field(default="deepseek-chat", description="The DeepSeek model to be used.")
    api_key: str = Field(description="The API key for the DeepSeek API.")

    def instantiate_llm(self, **kwargs) -> Any:
        """Creates a DeepSeek model instance using the provided config."""
        from langchain_deepseek import ChatDeepSeek

        return ChatDeepSeek(
            model=self.model,
            api_key=self.api_key,
            **(self.extra_params or {}),
            **kwargs
        )

"""
import os
from langchain.cache import SQLiteCache
from langchain.llms import OpenAI

def setup_llm_cache(db_name):
    cache_dir = "cache_LangChain"
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{db_name}.db")
    cache = SQLiteCache(cache_path)
    OpenAI.cache = cache

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Set up LLM cache with SQL cache.")
    parser.add_argument("db_name", help="Name of the database for the cache.")
    
    args = parser.parse_args()
    setup_llm_cache(args.db_name)
"""