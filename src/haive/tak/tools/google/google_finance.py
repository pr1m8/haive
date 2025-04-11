from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
load_dotenv('.env')

google_finance_tool=load_tools(["google-finance"])
#print(google_finance_tool)
#print(google_places_tool)