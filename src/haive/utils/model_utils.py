from pydantic import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser




def get_format_instructions(pydantic_object: BaseModel) -> str:
    """Get the format instructions for a pydantic object."""
    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    return parser.get_format_instructions()
