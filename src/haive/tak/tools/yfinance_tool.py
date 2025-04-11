"""
YFinance News Tool
========================
This tool is used to get the latest news from Yahoo Finance.
It is a wrapper around the YahooFinanceNewsTool and yfinance.
"""
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

yfinance_news_tool = YahooFinanceNewsTool()

#print([yfinance_news_tool.name, yfinance_news_tool.description])