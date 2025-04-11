from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
import requests

BASE_URL = "https://thereportoftheweek-api.herokuapp.com"

# --- Tool: Get All Reports ---
class GetAllReportsInput(BaseModel):
    pass

def get_all_reports(_: GetAllReportsInput) -> list:
    response = requests.get(f"{BASE_URL}/reports")
    response.raise_for_status()
    return response.json()

get_all_reports_tool = StructuredTool.from_function(
    name="get_all_report_of_the_week_reviews",
    description="Retrieve all food and drink reviews from The Report Of The Week.",
    func=get_all_reports,
    args_schema=GetAllReportsInput,
)

# --- Tool: Filter by Category ---
class GetReportsByCategoryInput(BaseModel):
    category: str = Field(..., description="The category to filter by, such as 'Energy Crisis' or 'Running On Empty'.")

def get_reports_by_category(input: GetReportsByCategoryInput) -> list:
    response = requests.get(f"{BASE_URL}/reports", params={"category": input.category})
    response.raise_for_status()
    return response.json()

get_reports_by_category_tool = StructuredTool.from_function(
    name="get_report_of_the_week_by_category",
    description="Get reviews by category, such as 'Energy Crisis' for energy drinks or 'Running On Empty' for food.",
    func=get_reports_by_category,
    args_schema=GetReportsByCategoryInput,
)

# --- Tool: Filter by Date Range ---
class GetReportsByDateRangeInput(BaseModel):
    start_date: str = Field(..., description="Start date in YYYY-M-D format.")
    end_date: str = Field(..., description="End date in YYYY-M-D format.")

def get_reports_by_date_range(input: GetReportsByDateRangeInput) -> list:
    query = f"{input.start_date}|{input.end_date}"
    response = requests.get(f"{BASE_URL}/reports", params={"between": query})
    response.raise_for_status()
    return response.json()

get_reports_by_date_range_tool = StructuredTool.from_function(
    name="get_report_of_the_week_by_date_range",
    description="Get reviews posted between two dates (format: YYYY-M-D).",
    func=get_reports_by_date_range,
    args_schema=GetReportsByDateRangeInput,
)
