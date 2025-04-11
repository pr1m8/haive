from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
load_dotenv('.env')

scene_explain_tool = load_tools(["sceneXplain"])