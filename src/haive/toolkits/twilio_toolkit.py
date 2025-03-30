#from langchain_community.agent_toolkits
from langchain_community.utilities.twilio import TwilioAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from src.config.config import Config
if not Config.TWILIO_ACCOUNT_SID:
    raise ValueError("TWILIO_ACCOUNT_SID is not set")
if not Config.TWILIO_AUTH_TOKEN:
    raise ValueError("TWILIO_AUTH_TOKEN is not set")


twilio_tool=TwilioAPIWrapper()
twilio_toolkit = load_tools(["twilio"])
tool_choice = twilio_toolkit.get_tools()[0]
tool_choice.invoke(input={'query':f'send a text message to +12484345508 with the message "Hello, world!"'})