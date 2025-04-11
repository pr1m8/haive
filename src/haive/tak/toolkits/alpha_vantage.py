from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from dotenv import load_dotenv
import os
load_dotenv('.env')

class AlphaVantageConfig(BaseModel):
    """Configuration for AlphaVantage Toolkit."""
    api_key: Optional[str] = Field(default=os.getenv("ALPHAVANTAGE_API_KEY"), description="Alpha Vantage API key")

    def get_client(self) -> AlphaVantageAPIWrapper:
        return AlphaVantageAPIWrapper()


def get_alpha_vantage_tools(config: AlphaVantageConfig) -> List[Tool]:
    """Returns a list of structured Alpha Vantage tools."""
    client = config.get_client()

    return [
        Tool.from_function(
            func=client.run,
            name="alpha_vantage_exchange_rate",
            description="Get real-time currency exchange rate from one currency to another. Input is a string: 'USD,JPY'.",
        ),
        Tool.from_function(
            func=client._get_time_series_daily,
            name="alpha_vantage_daily_stock_data",
            description="Get daily stock time series data for a given symbol. Input is a string symbol (e.g., 'IBM').",
        ),
        Tool.from_function(
            func=client._get_time_series_weekly,
            name="alpha_vantage_weekly_stock_data",
            description="Get weekly stock time series data for a given symbol. Input is a string symbol (e.g., 'IBM').",
        ),
        Tool.from_function(
            func=client._get_quote_endpoint,
            name="alpha_vantage_quote",
            description="Get real-time quote data (price, volume) for a given symbol. Input is a string symbol (e.g., 'IBM').",
        ),
        Tool.from_function(
            func=client.search_symbols,
            name="alpha_vantage_search_symbol",
            description="Search for matching company symbols by input string (e.g., 'Tesla', 'IBM').",
        ),
        Tool.from_function(
            func=client._get_market_news_sentiment,
            name="alpha_vantage_market_sentiment",
            description="Get market news sentiment for a given symbol.",
        ),
        Tool.from_function(
            func=client._get_top_gainers_losers,
            name="alpha_vantage_market_movers",
            description="Get top 20 gainers, losers, and most active stocks in the US market.",
        ),
    ]
alpha_vantage_toolkit = get_alpha_vantage_tools(AlphaVantageConfig())