import getpass
from config.config import Config
from langchain_discord_shikenso.toolkits import DiscordToolkit
from dotenv import load_dotenv

load_dotenv('.env.example')

discord_toolkit = DiscordToolkit()

discord_tools = discord_toolkit.get_tools()


