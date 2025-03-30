from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict

from langchain_core.tools import BaseTool, BaseToolkit
from langchain_core.language_models import BaseLanguageModel
from langchain_community.tools.amadeus.closest_airport import AmadeusClosestAirport
from langchain_community.tools.amadeus.flight_search import AmadeusFlightSearch
from amadeus import Client

# Load environment variables
load_dotenv(".env.example")

# Import your LLM config wrapper
from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig

# -----------------------------
# 🔧 Amadeus Config (Serializable)
# -----------------------------
class AmadeusToolkitConfig(BaseModel):
    """
    JSON-serializable config for instantiating the Amadeus toolkit and its dependencies.
    """
    client_id: str = Field(default_factory=lambda: os.getenv("AMADEUS_CLIENT_ID", ""), description="Amadeus API client ID.")
    client_secret: str = Field(default_factory=lambda: os.getenv("AMADEUS_CLIENT_SECRET", ""), description="Amadeus API client secret.")
    llm_config: Optional[LLMConfig] = Field(default=AzureLLMConfig(), description="LLM configuration dict, passed to LLMConfig")

    def create_client(self) -> Client:
        return Client(client_id=self.client_id, client_secret=self.client_secret)

    def create_llm(self) -> Optional[BaseLanguageModel]:
        if self.llm_config:
            #print(self.llm_config)
            return self.llm_config.instantiate_llm()  # ✅ Use create_llm
        return None

# -----------------------------
# 🧰 Amadeus Toolkit (LangChain-compatible)
# -----------------------------
class AmadeusToolkit(BaseToolkit):
    """
    LangChain-compatible toolkit for interacting with Amadeus APIs.
    """
    config: AmadeusToolkitConfig
    client: Client
    llm: Optional[BaseLanguageModel] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> List[BaseTool]:
        # Required model rebuilds for Pydantic v2
        AmadeusClosestAirport.model_rebuild()
        AmadeusFlightSearch.model_rebuild()

        return [
            AmadeusClosestAirport(llm=self.llm),
            AmadeusFlightSearch(),
        ]

    @classmethod
    def from_config(cls, config: AmadeusToolkitConfig) -> "AmadeusToolkit":
        return cls(
            config=config,
            client=config.create_client(),
            llm=config.create_llm()
        )

# -----------------------------
# 🧪 Test CLI
# -----------------------------
if __name__ == "__main__":
    from pprint import pprint

    config = AmadeusToolkitConfig(
        client_id=os.getenv("AMADEUS_CLIENT_ID", ""),
        client_secret=os.getenv("AMADEUS_CLIENT_SECRET", ""),
    )

    toolkit = AmadeusToolkit.from_config(config)
    tools = toolkit.get_tools()

    print("✅ Loaded Amadeus tools:")
    for tool in tools:
        pprint({"name": tool.name, "description": tool.description})
