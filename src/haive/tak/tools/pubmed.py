from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.agent_toolkits.load_tools import load_tools


pubmed_tools= load_tools(["pubmed"])
