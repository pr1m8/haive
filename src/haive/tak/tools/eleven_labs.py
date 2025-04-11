#from langchain_community.tools import ElevenLabsText2SpeechTool
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
load_dotenv('.env')

eleven_labs_text2speech_tool = load_tools(["eleven_labs_text2speech"])



