from azure.identity import DefaultAzureCredential
from langchain_community.agent_toolkits import PowerBIToolkit, create_pbi_agent
from langchain_community.utilities.powerbi import PowerBIDataset

credential = DefaultAzureCredential()

pbi_toolkit = PowerBIToolkit(
    dataset_id="1234567890",
    credential=credential,
)
