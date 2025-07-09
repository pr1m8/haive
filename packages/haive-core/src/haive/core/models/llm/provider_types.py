"""
LLM Provider Types Module.

This module defines the supported LLM providers as an enumeration,
ensuring consistent identification and type safety when configuring LLM models.

These provider types are used throughout the Haive LLM framework to identify
the source of language models and apply appropriate configuration patterns.

Typical usage example:
    ```python
    from haive.core.models.llm.provider_types import LLMProvider

    # Check if a provider is supported
    if provider == LLMProvider.OPENAI:
        # Use OpenAI-specific configuration
        pass
    ```
"""

from enum import Enum


class LLMProvider(str, Enum):
    """
    Enumeration of supported LLM providers.

    This enum inherits from str to allow string comparison and serialization
    while maintaining type safety and providing autocompletion support.

    Attributes:
        OPENAI: OpenAI language models (GPT-4, etc.)
        ANTHROPIC: Anthropic language models (Claude, etc.)
        HUGGINGFACE: HuggingFace model hub language models
        AZURE: Microsoft Azure OpenAI language models
        DEEPSEEK: DeepSeek language models
        GEMINI: Google Gemini language models
        COHERE: Cohere language models
        AI21: AI21 Labs language models (Jurassic, etc.)
        ALEPH_ALPHA: Aleph Alpha language models (Luminous, etc.)
        GOOSEAI: GooseAI language models
        MOSAICML: MosaicML language models
        NLP_CLOUD: NLP Cloud language models
        OPENLM: OpenLM language models
        PETALS: Petals distributed language models
        REPLICATE: Replicate-hosted language models
        TOGETHER_AI: Together.ai language models
        FIREWORKS_AI: Fireworks.ai language models
        PERPLEXITY: Perplexity language models
        MISTRALAI: Mistral AI language models
        GROQ: Groq language models
        VERTEX_AI: Google Vertex AI language models
        BEDROCK: AWS Bedrock language models
        NVIDIA: NVIDIA AI Endpoints language models
        OLLAMA: Ollama local language models
        LLAMACPP: Llama.cpp local language models
        UPSTAGE: Upstage language models
        DATABRICKS: Databricks language models
        WATSONX: IBM Watson.x language models
        XAI: xAI language models
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    AZURE = "azure"
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
    FIREWORKS_AI = "fireworks_ai"
    PERPLEXITY = "perplexity"
    MISTRALAI = "mistralai"
    GROQ = "groq"
    VERTEX_AI = "vertex_ai"
    BEDROCK = "bedrock"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"
    UPSTAGE = "upstage"
    DATABRICKS = "databricks"
    WATSONX = "watsonx"
    XAI = "xai"
