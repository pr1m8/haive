import os

from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities.google_scholar import GoogleScholarAPIWrapper
load_dotenv('.env')

tool = GoogleScholarAPIWrapper()
google_scholar_tool =load_tools(["google-scholar"])
#print(google_scholar_tool)#