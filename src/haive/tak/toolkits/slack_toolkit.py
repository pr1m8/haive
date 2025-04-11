
import getpass
import os
from src.config.config import Config

if not Config.SLACK_USER_TOKEN:
    os.environ["SLACK_USER_TOKEN"] = getpass.getpass("Enter your Slack user token: ")

from langchain_community.agent_toolkits import SlackToolkit
slack_toolkit=SlackToolkit().get_tools()





