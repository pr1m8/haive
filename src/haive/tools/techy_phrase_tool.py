from langchain.tools import Tool
import requests

def get_techy_phrase_text() -> str:
    return requests.get("https://techy-api.vercel.app/api/text").text.strip()

def get_techy_phrase_json() -> dict:
    return requests.get("https://techy-api.vercel.app/api/json").json()

techy_text_tool = Tool(
    name="techy_phrase_text",
    description="Get a random tech phrase in plain text",
    func=lambda x: get_techy_phrase_text()
)

techy_json_tool = Tool(
    name="techy_phrase_json",
    description="Get a random tech phrase in structured JSON format",
    func=lambda x: get_techy_phrase_json()
)
