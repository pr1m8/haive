
from datetime import datetime

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.clickup.toolkit import ClickupToolkit
from langchain_community.utilities.clickup import ClickupAPIWrapper

from src.config.config import Config


def get_clickup_toolkit():
    clickup_api_wrapper = ClickupAPIWrapper(
        api_key=Config.CLICKUP_API_KEY,
        redirect_uri=Config.CLICKUP_REDIRECT_URI,
        client_id=Config.CLICKUP_CLIENT_ID,
        client_secret=Config.CLICKUP_CLIENT_SECRET
    )

    return ClickupToolkit(api_wrapper=clickup_api_wrapper)
