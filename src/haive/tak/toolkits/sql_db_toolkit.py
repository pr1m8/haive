from langchain import hub

from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Add wrapper from our sql rag. 
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# Pull prompt (or define your own)
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")