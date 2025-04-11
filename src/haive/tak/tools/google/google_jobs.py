import os

from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
load_dotenv('.env')

tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
google_job_search_tool =load_tools(["google-jobs"])
