import os
from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()
# Update
load_dotenv(dotenv_path='.env')
class Config:
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "my_database")

    NEO4J_URI = os.getenv("NEO4J_URI", "localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
    OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")


    # Tools
    # Polygon
    # ========================
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
    # Wolfram Alpha
    WOLFRAM_ALPHA_APPID = os.getenv("WOLFRAM_ALPHA_APPID")
    # Amadeus
    AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
    AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
    # OpenWeatherMap
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    # TAVILY_API_KEY
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    # Merriam Webster
    MERRIAM_WEBSTER_API_KEY = os.getenv("MERRIAM_WEBSTER_API_KEY")
    # Bing
    BING_SUBSCRIPTION_KEY = os.getenv("BING_SUBSCRIPTION_KEY")
    BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")
    # Reddit
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    # Google Trends
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    # Steam
    STEAM_KEY = os.getenv("STEAM_KEY")
    STEAM_ID = os.getenv("STEAM_ID")
    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    # Slack
    SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")


    # Azure API Configuration
    # ========================
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_OBJECT_ID = os.getenv("AZURE_OBJECT_ID")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_SECRET_ID = os.getenv("AZURE_SECRET_ID")
    #AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

    # Document Loaders
    # ========================
    # Dropbox
    DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
    DROPBOX_FOLDER_PATH = os.getenv("DROPBOX_FOLDER_PATH")
    DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
    DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

    # DataForSEO
    # ========================
    DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
    DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")

    # ClickUp
    # ========================
    CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
    CLICKUP_REDIRECT_URI = os.getenv("CLICKUP_REDIRECT_URI")
    CLICKUP_CLIENT_ID = os.getenv("CLICKUP_CLIENT_ID")
    CLICKUP_CLIENT_SECRET = os.getenv("CLICKUP_CLIENT_SECRET")

    # GitHub
    # ========================
    GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
    GITHUB_APP_PRIVATE_KEY = os.getenv("GITHUB_APP_PRIVATE_KEY")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")
    GITHUB_BASE_BRANCH = os.getenv("GITHUB_BASE_BRANCH")


    # Discord
    # ========================
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    DISCORD_WEBHOOK_USERNAME = os.getenv("DISCORD_WEBHOOK_USERNAME")

    @staticmethod
    def database_url():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

if __name__ == "__main__":
    print("🛠 Config Loaded:", Config.database_url())
