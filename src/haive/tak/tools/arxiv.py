from langchain_community.agent_toolkits.load_tools import load_tools
arxiv_query_tool = load_tools(
["arxiv"],
)



