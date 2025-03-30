from langchain_community.agent_toolkits import AzureAiServicesToolkit
from src.config.config import Config


azure_toolkit = AzureAiServicesToolkit().get_tools()

