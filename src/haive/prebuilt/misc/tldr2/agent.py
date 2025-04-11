from src.haive.agents.base import AgentConfig
from pydantic import Field
from typing import List         
from src.haive.agents.tldr2.models import NewsApiParams
from src.haive.agents.tldr2.state import GraphState

class TLDRAgentConfig(AgentConfig):
    news_query: str = Field(description="Input query to extract news search parameters from.")
    num_searches_remaining: int = Field(description="Number of articles to search for.")
    newsapi_params: dict = Field(description="Structured argument for the News API.")
    past_searches: List[dict] = Field(description="List of search params already used.")
    
