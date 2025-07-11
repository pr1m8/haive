from langchain_community.retrievers import AskNewsRetriever

retriever = AskNewsRetriever(
    client_id="your_client_id",
    client_secret="your_client_secret",
)
