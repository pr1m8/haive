#from langchain.document_transformers.base import BaseDocumentTransformer
from typing import Any, Iterator, List, Sequence, Tuple, Union, cast
#from
from langchain_neo4j import Neo4jGraph
from langchain_core.documents import Document,BaseDocumentTransformer
from pydantic import BaseModel,Field
import os
from src.config.config import Config
class GraphDBConfig(BaseModel):
    graph_db_uri: str = Field(default=Config.NEO4J_URI, description="The URI of the graph database")
    graph_db_user: str = Field(default=Config.NEO4J_USER, description="The username of the graph database")
    graph_db_password: str = Field(default=Config.NEO4J_PASSWORD, description="The password of the graph database")
    graph_db_database: str = Field(default=Config.NEO4J_DATABASE, description="The name of the database to connect to")
    enhanced_schema: bool = Field(default=True, description="Whether to use the enhanced schema")

    def get_graph_db(self):
        """Neo4j database wrapper for various graph operations."""
        return Neo4jGraph(
            url=self.graph_db_uri,  # Now using self instead of cls
            username=self.graph_db_user,
            password=self.graph_db_password,
            database=self.graph_db_database,
            timeout=10,
            sanitize=True,
            refresh_schema=True,
            enhanced_schema=self.enhanced_schema,
        )  

    def get_graph_db_schema(self):
        return self.get_graph_db().get_schema()
    



class GraphTransformer(BaseDocumentTransformer):
    """
    A document transformer that transforms a document into a graph.
    """
    def transform_documents(self, documents: List[Document]) -> List[Document]:

        return documents
    
# Instantiate GraphDBConfig before using the method
a = GraphDBConfig()

# Now call the method
print(a.get_graph_db_schema())
