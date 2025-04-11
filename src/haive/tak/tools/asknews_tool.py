from langchain_community.tools.asknews import AskNewsSearch
from src.config.config import Config
import os
import getpass
from dotenv import load_dotenv
load_dotenv('.env')
asknews_search_tool=[AskNewsSearch()]








