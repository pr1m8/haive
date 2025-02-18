from langchain_community.document_loaders import DataFrameLoader
from langchain_community.document_loaders.base import BaseLoader
from pydantic import Field
from pydantic import BaseModel
from typing_extensions import Literal,Any

class DataFrameLoaderConfig(BaseModel):
    """
    Config for the DataFrameLoader
    """
    path: str = Field(default="dataframe.csv",description="The file path to save the data to")
    page_content_column: str = Field(default="text",description="The column name to use for the page content")
    data_frame: Any = Field(default=None,description="The data frame to load")  

def load_dataframe(config: DataFrameLoaderConfig):
    return DataFrameLoader(config.data_frame,config.page_content_column)
    



