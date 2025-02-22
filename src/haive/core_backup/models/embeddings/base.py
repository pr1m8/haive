from pydantic import BaseModel, Field
from langchain_openai import AzureOpenAIEmbeddings
from src.config.config import *
import os
class EmbeddingsConfig(BaseModel):
    provider: str = Field(default="Azure",description="The provider of the embeddings")
    model: str=Field(default='text-embedding-3-small',description="The model of the embeddings")
    api_key: str=Field(default=os.getenv('AZURE_OPENAI_API_KEY'),description="The API key of the embeddings")
    api_version: str=Field(default='2024-05-13',description="The API version of the embeddings")
    api_base: str=Field(default='https://api.openai.com/v1',description="The API base of the embeddings")
    api_type: str=Field(default='azure',description="The API type of the embeddings")
    api_endpoint: str=Field(default='https://api.openai.com/v1',description="The API endpoint of the embeddings")  


def create_embeddings(embeddings_config: EmbeddingsConfig):
    if embeddings_config.provider == "Azure":
        return AzureOpenAIEmbeddings(
            model=embeddings_config.model,
            #api_key=embeddings_config.api_key,
            #api_version=embeddings_config.api_version,
            #api_base=embeddings_config.api_base,
            #api_type=embeddings_config.api_type,
            #api_endpoint=embeddings_config.api_endpoint
        )
    else:
        raise ValueError(f"Unsupported embeddings provider: {embeddings_config.provider}")
    

#config = EmbeddingsConfig()
#embeddings = create_embeddings(config)
##print(embeddings)

