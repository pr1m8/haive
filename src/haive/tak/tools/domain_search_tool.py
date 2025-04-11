import requests
from typing import Optional
from pydantic import BaseModel, Field,AnyUrl
from langchain_core.tools import StructuredTool


class DomainSearchInput(BaseModel):
    domain: AnyUrl= Field(description="A keyword to search for, e.g., 'facebook', 'ai', 'nasa', etc.")

def search_registered_domains(domain: str) -> str:
    """Search for registered domain names using a keyword"""
    url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"
    response = requests.get(url)
    if not response.ok:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()
    domains = data.get("domains", [])
    if not domains:
        return f"No results found for '{domain}'"

    return "\n".join([d["domain"] for d in domains[:10]])

domain_search_tool = StructuredTool.from_function(
    func=search_registered_domains,
    name="search_registered_domains",
    description="Search for registered domain names using a keyword",
    args_schema=DomainSearchInput
)
