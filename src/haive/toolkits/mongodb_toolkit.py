from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from langchain_openai import ChatOpenAI

db = MongoDBDatabase.from_connection_string("mongodb://localhost:27017/chinook")
llm = ChatOpenAI(temperature=0)

toolkit = MongoDBDatabaseToolkit(db=db, llm=llm)