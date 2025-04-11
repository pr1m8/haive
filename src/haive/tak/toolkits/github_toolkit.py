from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from src.config.config import Config
import os
import getpass 
if not Config.GITHUB_APP_ID or not Config.GITHUB_APP_PRIVATE_KEY:   
    Config.GITHUB_APP_ID = getpass.getpass("Enter your GitHub App ID: ")
    Config.GITHUB_APP_PRIVATE_KEY = getpass.getpass("Enter your GitHub App Private Key: ")
    
github = GitHubAPIWrapper(
    app_id=Config.GITHUB_APP_ID,
    private_key=Config.GITHUB_APP_PRIVATE_KEY
)
github_toolkit = GitHubToolkit.from_github_api_wrapper(github)