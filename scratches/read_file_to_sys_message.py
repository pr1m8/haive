import yaml
from langchain.schema import SystemMessage
from pathlib import Path
from typing import Union

def read_file_content(file_path: Union[str, Path]) -> str:
    """
    Reads a file (.md, .txt, .yml) and returns its content as a string.
    
    :param file_path: Path to the file.
    :return: Content of the file as a string.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix in {'.txt', '.md'}:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.suffix == '.yml':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)
            if isinstance(content, dict):
                return content.get('message', '')  # Expecting a 'message' key in YAML
            if not isinstance(content, str):
                raise ValueError("Invalid YAML format: Expected a string under 'message' key.")
    else:
        raise ValueError("Unsupported file format. Use .md, .txt, or .yml")

def read_system_message(file_path: Union[str, Path]) -> SystemMessage:
    """
    Reads a file and converts its content into a LangChain SystemMessage.
    
    :param file_path: Path to the file.
    :return: SystemMessage containing the file content.
    """
    content = read_file_content(file_path)
    return SystemMessage(content=content)

# Example usage:
# message = read_system_message("system_prompt.md")
# print(message.content)
