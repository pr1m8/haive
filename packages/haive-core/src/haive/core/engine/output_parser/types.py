from enum import Enum


class OutputParserType(str, Enum):
    """Enumeration of supported output parser types."""

    BOOLEAN = "boolean"
    LIST = "list"
    COMMA_SEPARATED_LIST = "comma_separated_list"
    NUMBERED_LIST = "numbered_list"
    MARKDOWN_LIST = "markdown_list"
    DATETIME = "datetime"
    JSON = "json"
    SIMPLE_JSON = "simple_json"
    XML = "xml"
    PYDANTIC = "pydantic"
    COMBINING = "combining"
    STRING = "string"
    REGEX = "regex"
    REGEX_DICT = "regex_dict"
    STRUCTURED = "structured"
    PANDAS_DATAFRAME = "pandas_dataframe"
    YAML = "yaml"
    ENUM = "enum"
    OPENAI_TOOLS = "openai_tools"
    OPENAI_TOOLS_KEY = "openai_tools_key"
    PYDANTIC_TOOLS = "pydantic_tools"
