import requests
from langchain.tools import StructuredTool, BaseToolkit
from pydantic import BaseModel, Field
from typing import List


class BinLookupInput(BaseModel):
    bin_number: str = Field(..., description="The first 6 to 8 digits of a card number")


def lookup_bin(input: BinLookupInput) -> dict:
    headers = {"Accept-Version": "3"}
    response = requests.get(f"https://lookup.binlist.net/{input.bin_number}", headers=headers)
    if response.status_code == 404:
        return {"error": "No matching card found"}
    response.raise_for_status()
    return response.json()


bin_lookup_tool = StructuredTool.from_function(
    name="lookup_card_bin_info",
    description="Look up card information based on the first 6 to 8 digits (BIN/IIN) using Binlist.net API",
    func=lookup_bin
)
