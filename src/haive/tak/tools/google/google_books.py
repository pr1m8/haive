
from langchain_community.tools.google_books import GoogleBooksQueryRun
from langchain_community.utilities.google_books import GoogleBooksAPIWrapper
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
import os
load_dotenv('.env')

google_books_tool=load_tools(["google-books"])
#print(google_books_tool)