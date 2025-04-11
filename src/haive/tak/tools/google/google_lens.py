import os

from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities.google_lens import GoogleLensAPIWrapper
load_dotenv('.env')

tool = GoogleLensAPIWrapper()
google_lens_tool =load_tools(["google-lens"])
