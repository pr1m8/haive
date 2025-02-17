import yaml

def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Utility function to read a markdown file and integrate it as a system message
def read_file_content(file_path):
    """
    Reads a file and returns the content.
    Args:
        file_path (str): Path to the .md file.

    Returns:
        ChatPromptTemplate: Chat prompt template with the file content as the system message.
    """
    try:
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            return read_yaml_file(file_path)
        # Read the content of the .md file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    return file_content

