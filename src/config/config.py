import os
from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()
# Update
load_dotenv(dotenv_path='/home/will/Projects/haive/haive-bk/config/env/.env')
class Config:
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "my_database")


    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
    OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
    @staticmethod
    def database_url():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

if __name__ == "__main__":
    print("🛠 Config Loaded:", Config.database_url())
