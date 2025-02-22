from langchain_community.document_loaders import TelegramChatFileLoader,TelegramChatApiLoader,TelegramChatLoader

from typing import Optional
from pydantic import Field
from telethon.hints import EntityLike
from pydantic import BaseModel
class TelegramChatApiLoaderConfig(BaseModel):
    """
    Config for the TelegramChatApiLoader
    """
    chat_entity: Optional[EntityLike] = Field(default=None,description="The chat entity to fetch data from")
    api_id: Optional[int] = Field(default=None,description="The API ID")
    api_hash: Optional[str] = Field(default=None,description="The API hash")
    username: Optional[str] = Field(default=None,description="The username")
    file_path: str = Field(default="telegram_data.json",description="The file path to save the data to")
class TelegramChatFileLoaderConfig(BaseModel):
    """
    Config for the TelegramChatFileLoader
    """
    path: str = Field(default="telegram_data.json",description="The file path to save the data to")
    
def TelegramChatApiLoader