from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from dotenv import load_dotenv

load_dotenv('.env')




google_trends_tool = [GoogleTrendsQueryRun(api_wrapper=GoogleTrendsAPIWrapper())]
print(google_trends_tool)
#tool.run(tool_input={'query':'what is the latest news on covid-19'})