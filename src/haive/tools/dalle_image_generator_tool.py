from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
load_dotenv('.env.example')

tools = load_tools(["dalle-image-generator"])
print(tools)



