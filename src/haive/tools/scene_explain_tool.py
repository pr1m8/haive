from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
load_dotenv('.env.example')

scene_explain_tool = load_tools(["sceneXplain"])