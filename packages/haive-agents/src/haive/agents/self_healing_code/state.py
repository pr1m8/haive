from collections.abc import Callable

from pydantic import BaseModel, Field


class SelfHealingCodeState(BaseModel):
    function: Callable = Field(description="The function to be called")
    function_string: str = Field(
        description="The string representation of the function"
    )
    arguments: list = Field(description="The arguments to be passed to the function")
    error: bool = Field(description="Whether the function has an error")
    error_description: str = Field(description="The description of the error")
    new_function_string: str = Field(
        description="The new string representation of the function"
    )
    bug_report: str = Field(description="The bug report")
    memory_search_results: list = Field(
        description="The search results from the memory"
    )
    memory_ids_to_update: list = Field(
        description="The ids of the memories to be updated"
    )
