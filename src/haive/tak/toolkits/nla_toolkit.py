from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict

from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool, BaseToolkit
from langchain_community.agent_toolkits.nla.toolkit import NLAToolkit as RawNLAToolkit
from langchain_community.utilities.requests import Requests

from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig

# -----------------------------
# 📦 Load Environment
# -----------------------------
load_dotenv(".env")


# -----------------------------
# 🔧 Config Schema
# -----------------------------
class NLAToolkitConfig(BaseModel):
    """Config for instantiating NLAToolkit."""
    url: str = Field(..., description="URL of the OpenAPI spec or AI plugin manifest.")
    llm_config: Optional[LLMConfig] = Field(default_factory=AzureLLMConfig, description="LLM configuration.")

    def create_llm(self) -> Optional[BaseLanguageModel]:
        if self.llm_config:
            return self.llm_config.instantiate_llm()
        return None


# -----------------------------
# 🧰 Structured NLA Toolkit
# -----------------------------
class StructuredNLAToolkit(BaseToolkit):
    config: NLAToolkitConfig
    llm: Optional[BaseLanguageModel] = None
    url: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> List[BaseTool]:
        if not self.llm:
            raise ValueError("LLM must be initialized before using the NLA toolkit.")
        raw_toolkit = RawNLAToolkit.from_llm_and_url(llm=self.llm, open_api_url=self.url, requests=Requests())
        return raw_toolkit.get_tools()

    @classmethod
    def from_config(cls, config: NLAToolkitConfig) -> StructuredNLAToolkit:
        return cls(
            config=config,
            llm=config.create_llm(),
            url=config.url,
        )


# -----------------------------
# 🧪 CLI Test
# -----------------------------
if __name__ == "__main__":
    from pprint import pprint

    config = NLAToolkitConfig(
        url=os.getenv("NLA_URL", "https://www.klarna.com/us/shopping/openai/v0/api-docs/"),
        
    )

    toolkit = StructuredNLAToolkit.from_config(config)
    tools = toolkit.get_tools()

    print("✅ Loaded NLA tools:")
    for tool in tools:
        pprint({"name": tool.name, "description": tool.description})
