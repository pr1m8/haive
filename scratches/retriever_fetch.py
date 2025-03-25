#!/usr/bin/env python3
"""
Document Loader Inspector Script

This script analyses all document loaders in LangChain and extracts detailed information
about their signatures, parameters, default values, required parameters, docstrings,
and inheritance hierarchy. The data is saved in both JSON and Markdown formats.
"""

import os
import sys
import json
import inspect
import importlib
import pkgutil
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set, get_type_hints
from dataclasses import dataclass, asdict
from datetime import datetime
import re

# Make sure LangChain is installed
try:
    import langchain_community
except ImportError:
    print("LangChain Community package not found. Please install it with:")
    print("pip install langchain-community")
    sys.exit(1)

@dataclass
class ParameterInfo:
    """Information about a constructor parameter."""
    name: str
    type_hint: str
    default_value: str
    is_required: bool
    doc_description: str = ""
    
@dataclass
class LoaderInfo:
    """Detailed information about a document loader."""
    name: str
    module: str
    full_path: str
    docstring: str
    base_classes: List[str]
    parameters: List[ParameterInfo]
    source_type: str = ""  # Will be filled later: LOCAL, REMOTE, DATABASE, API, etc.
    category: str = ""  # Will be filled later: file_loaders, web_loaders, etc.
    formats: List[str] = None  # Will be filled later
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = []

def get_parameter_doc_description(docstring: str, param_name: str) -> str:
    """Extract parameter description from docstring."""
    if not docstring:
        return ""
    
    # Look for parameter in docstring using common patterns
    patterns = [
        # Sphinx format
        fr':param {param_name}: (.*?)(?:$|\n|\:param)',
        # Google style
        fr'{param_name} \((.*?)\): (.*?)(?=\n\s*\w+:|\n\s*$|\n\s*\n)',
        fr'{param_name}: (.*?)(?=\n\s*\w+:|\n\s*$|\n\s*\n)',
        # Simple format
        fr'{param_name}[^\n]* - (.*?)(?=\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, docstring, re.DOTALL)
        if match:
            desc = match.group(1).strip()
            # Clean up description
            desc = re.sub(r'\s+', ' ', desc)
            return desc
    
    return ""

def get_init_parameters(cls) -> List[ParameterInfo]:
    """Get detailed information about __init__ parameters."""
    try:
        # Get init signature
        signature = inspect.signature(cls.__init__)
        
        # Get type hints if available
        try:
            type_hints = get_type_hints(cls.__init__)
        except (TypeError, ValueError):
            type_hints = {}
        
        # Get docstring
        docstring = inspect.getdoc(cls.__init__) or ""
        
        parameters = []
        
        # Skip 'self' parameter
        for name, param in list(signature.parameters.items())[1:]:
            # Determine type hint
            type_hint = "Any"
            if name in type_hints:
                type_hint = str(type_hints[name]).replace("<class '", "").replace("'>", "")
            elif param.annotation != inspect.Parameter.empty:
                type_hint = str(param.annotation)
            
            # Determine default value
            default_value = "None"
            is_required = True
            if param.default != inspect.Parameter.empty:
                default_value = repr(param.default)
                is_required = False
            
            # Get parameter description from docstring
            doc_description = get_parameter_doc_description(docstring, name)
            
            parameters.append(ParameterInfo(
                name=name,
                type_hint=type_hint,
                default_value=default_value,
                is_required=is_required,
                doc_description=doc_description
            ))
            
        return parameters
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error getting parameters for {cls.__name__}: {str(e)}")
        return []

def get_all_loaders(package_path, module_path="langchain_community.document_loaders") -> List[LoaderInfo]:
    """
    Recursively scan the package for document loaders and extract information.
    
    Args:
        package_path: Path to the langchain_community/document_loaders directory
        module_path: Current module path for imports
        
    Returns:
        List of LoaderInfo objects with details about each document loader
    """
    loaders_info = []
    
    for _, name, ispkg in pkgutil.iter_modules([package_path]):
        full_module_path = f"{module_path}.{name}"
        full_package_path = os.path.join(package_path, name)
        
        # If it's a package, scan it recursively
        if ispkg:
            loaders_info.extend(get_all_loaders(full_package_path, full_module_path))
            continue
        
        # Skip if not a Python file
        if not os.path.isfile(os.path.join(package_path, name + ".py")):
            continue
        
        try:
            # Import the module
            module = importlib.import_module(full_module_path)
            
            # Find all classes that might be document loaders
            for attr_name in dir(module):
                if attr_name.startswith('_'):
                    continue
                
                attr = getattr(module, attr_name)
                
                # Check if it's a class and its name suggests it's a loader
                if (inspect.isclass(attr) and 
                    ("Loader" in attr_name or 
                     attr_name.endswith("Parser") or
                     any(base.__name__.endswith("Loader") 
                         for base in attr.__mro__ if base is not object))):
                    
                    # Get base classes
                    base_classes = [base.__name__ for base in attr.__mro__[1:] 
                                  if base is not object and base.__module__.startswith('langchain')]
                    
                    # Get docstring
                    docstring = inspect.getdoc(attr) or ""
                    
                    # Get parameters
                    parameters = get_init_parameters(attr)
                    
                    # Create loader info
                    loader_info = LoaderInfo(
                        name=attr_name,
                        module=full_module_path,
                        full_path=f"{full_module_path}.{attr_name}",
                        docstring=docstring,
                        base_classes=base_classes,
                        parameters=parameters
                    )
                    
                    loaders_info.append(loader_info)
        
        except (ImportError, AttributeError) as e:
            print(f"Error importing {full_module_path}: {str(e)}")
    
    return loaders_info

def infer_source_type(loader_info: LoaderInfo) -> str:
    """Infer the source type based on the loader name, module, and parameters."""
    name = loader_info.name.lower()
    module = loader_info.module.lower()
    param_names = [p.name.lower() for p in loader_info.parameters]
    
    # Check for local file loaders
    if any(term in name for term in ['file', 'directory', 'csv', 'pdf', 'txt', 'text', 'docx', 'excel']):
        return "LOCAL"
    
    # Check for remote loaders
    if any(term in name for term in ['url', 'web', 'http', 'cloud', 's3', 'azure', 'gcs', 
                                     'cos', 'obs', 'online', 'remote']):
        return "REMOTE"
    
    # Check for database loaders
    if any(term in name for term in ['db', 'database', 'sql', 'mongo', 'cassandra', 
                                     'couchbase', 'rockset', 'snowflake', 'tidb', 'kinetica']):
        return "DATABASE"
    
    # Check for API loaders
    if any(term in name for term in ['api', 'hubspot', 'salesforce', 'stripe', 'figma', 
                                     'zendesk', 'trello', 'weather', 'apikey', 'token']):
        return "API"
    
    # Check parameters for hints
    if any(param in param_names for param in ['url', 'urls', 'web_path', 'endpoint']):
        return "REMOTE"
    
    if any(param in param_names for param in ['file_path', 'path']):
        return "LOCAL"
    
    if any(param in param_names for param in ['query', 'connection', 'connection_string']):
        return "DATABASE"
    
    if any(param in param_names for param in ['api_key', 'token', 'auth']):
        return "API"
    
    # Fallback to custom
    return "CUSTOM"

def infer_loader_category(loader_info: LoaderInfo) -> str:
    """Infer the category based on the loader name and module."""
    name = loader_info.name.lower()
    module = loader_info.module.lower()
    
    # File type categories
    if any(term in name for term in ['pdf']):
        return "pdf_loaders"
    
    if any(term in name for term in ['word', 'docx']):
        return "word_loaders"
    
    if any(term in name for term in ['csv', 'excel', 'dataframe']):
        return "tabular_loaders"
    
    if any(term in name for term in ['html', 'web', 'url']):
        return "web_loaders"
    
    if any(term in name for term in ['json']):
        return "json_loaders"
    
    if any(term in name for term in ['directory']):
        return "directory_loaders"
    
    if any(term in name for term in ['text', 'txt']):
        return "text_loaders"
    
    if any(term in name for term in ['markdown', 'md']):
        return "markdown_loaders"
    
    if any(term in name for term in ['image']):
        return "image_loaders"
    
    if any(term in name for term in ['audio', 'youtube']):
        return "audio_loaders"
    
    if any(term in name for term in ['chat', 'message']):
        return "chat_loaders"
    
    if any(term in name for term in ['email']):
        return "email_loaders"
    
    if any(term in name for term in ['code', 'python']):
        return "code_loaders"
    
    # Source categories
    if any(term in name for term in ['database', 'sql', 'mongo', 'cassandra']):
        return "database_loaders"
    
    if any(term in name for term in ['api', 'salesforce', 'hubspot', 'stripe']):
        return "api_loaders"
    
    if any(term in name for term in ['cloud', 's3', 'azure', 'gcs']):
        return "cloud_storage_loaders"
    
    # Default to generic loader category
    return "other_loaders"

def infer_formats(loader_info: LoaderInfo) -> List[str]:
    """Infer the document formats supported by the loader."""
    name = loader_info.name.lower()
    module = loader_info.module.lower()
    docstring = loader_info.docstring.lower()
    
    formats = []
    
    # Check for specific formats in name or module
    format_keywords = {
        "pdf": "PDF",
        "docx": "DOCX",
        "doc": "DOCX",
        "word": "DOCX",
        "csv": "CSV",
        "excel": "EXCEL",
        "xls": "EXCEL",
        "xlsx": "EXCEL",
        "json": "JSON",
        "html": "HTML",
        "htm": "HTML",
        "markdown": "MARKDOWN",
        "md": "MARKDOWN",
        "txt": "TEXT",
        "text": "TEXT",
        "xml": "XML",
        "yaml": "YAML",
        "yml": "YAML",
        "email": "EMAIL",
        "eml": "EMAIL",
        "image": "IMAGE",
        "img": "IMAGE",
        "png": "IMAGE",
        "jpg": "IMAGE",
        "jpeg": "IMAGE",
        "audio": "AUDIO",
        "mp3": "AUDIO",
        "wav": "AUDIO",
        "code": "CODE",
        "py": "CODE",
        "js": "CODE",
        "java": "CODE",
    }
    
    for keyword, format_name in format_keywords.items():
        if keyword in name or keyword in module:
            formats.append(format_name)
    
    # Special cases
    if "youtube" in name or "youtube" in module:
        formats.append("VIDEO")
    
    if "unstructured" in name or "unstructured" in module:
        # Unstructured typically handles multiple formats
        if not formats:
            formats = ["TEXT", "PDF", "DOCX", "HTML"]
    
    # API and Database loaders typically return structured data
    if infer_source_type(loader_info) in ["API", "DATABASE"]:
        formats.append("JSON")
    
    # Default to TEXT if no formats identified
    if not formats:
        formats.append("TEXT")
    
    # Remove duplicates and return
    return list(set(formats))

def categorize_loaders(loaders_info: List[LoaderInfo]) -> List[LoaderInfo]:
    """Add source type, category, and formats to each loader."""
    categorized_loaders = []
    
    for loader in loaders_info:
        # Infer source type
        loader.source_type = infer_source_type(loader)
        
        # Infer category
        loader.category = infer_loader_category(loader)
        
        # Infer formats
        loader.formats = infer_formats(loader)
        
        categorized_loaders.append(loader)
    
    return categorized_loaders

def generate_markdown(loaders_info: List[LoaderInfo], output_file: str):
    """Generate detailed Markdown documentation for all loaders."""
    with open(output_file, 'w') as f:
        f.write("# LangChain Document Loaders Analysis\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary statistics
        f.write("## Summary\n\n")
        f.write(f"Total loaders: {len(loaders_info)}\n\n")
        
        # Source type breakdown
        source_types = {}
        for loader in loaders_info:
            source_types[loader.source_type] = source_types.get(loader.source_type, 0) + 1
        
        f.write("### Source Types\n\n")
        for source_type, count in sorted(source_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {source_type}: {count} loaders\n")
        f.write("\n")
        
        # Category breakdown
        categories = {}
        for loader in loaders_info:
            categories[loader.category] = categories.get(loader.category, 0) + 1
        
        f.write("### Categories\n\n")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {category}: {count} loaders\n")
        f.write("\n")
        
        # Format breakdown
        formats = {}
        for loader in loaders_info:
            for format_name in loader.formats:
                formats[format_name] = formats.get(format_name, 0) + 1
        
        f.write("### Supported Formats\n\n")
        for format_name, count in sorted(formats.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {format_name}: {count} loaders\n")
        f.write("\n")
        
        # Group loaders by source type
        f.write("## Loaders by Source Type\n\n")
        
        for source_type in sorted(source_types.keys()):
            f.write(f"### {source_type}\n\n")
            
            # Group by category within source type
            source_categories = {}
            for loader in loaders_info:
                if loader.source_type == source_type:
                    if loader.category not in source_categories:
                        source_categories[loader.category] = []
                    source_categories[loader.category].append(loader)
            
            for category, loaders in sorted(source_categories.items()):
                f.write(f"#### {category}\n\n")
                
                for loader in sorted(loaders, key=lambda x: x.name):
                    f.write(f"##### {loader.name}\n\n")
                    f.write(f"**Module**: `{loader.module}`\n\n")
                    f.write(f"**Formats**: {', '.join(loader.formats)}\n\n")
                    
                    # Base classes
                    if loader.base_classes:
                        f.write(f"**Inherits from**: {', '.join(loader.base_classes)}\n\n")
                    
                    # Docstring
                    if loader.docstring:
                        f.write(f"**Description**:\n{loader.docstring}\n\n")
                    
                    # Parameters
                    if loader.parameters:
                        f.write("**Parameters**:\n\n")
                        for param in loader.parameters:
                            required = "(Required)" if param.is_required else f"(Default: {param.default_value})"
                            f.write(f"- `{param.name}`: {param.type_hint} {required}")
                            if param.doc_description:
                                f.write(f" - {param.doc_description}")
                            f.write("\n")
                        f.write("\n")
                    
                    f.write("\n")
        
        # Generate pydantic model examples
        f.write("## Serializable Configuration Examples\n\n")
        
        # Choose representative loaders from each source type
        example_loaders = {}
        for source_type in source_types.keys():
            for loader in loaders_info:
                if loader.source_type == source_type and loader.parameters:
                    if source_type not in example_loaders:
                        example_loaders[source_type] = loader
        
        for source_type, loader in sorted(example_loaders.items()):
            f.write(f"### {source_type} Configuration Example: {loader.name}\n\n")
            
            # Generate pydantic model example
            f.write("```python\n")
            f.write(f"class {loader.name}Config(BaseConfig):\n")
            f.write(f'    """Configuration for {loader.name}."""\n')
            
            for param in loader.parameters:
                param_type = param.type_hint
                if "Optional" in param_type:
                    param_type = param_type.replace("Optional[", "").replace("]", "")
                    
                # Format default value for Field
                default_param = f"default={param.default_value}"
                if param.is_required:
                    default_param = "..."
                    
                desc = param.doc_description or f"{param.name} parameter"
                f.write(f'    {param.name}: {param_type} = Field({default_param}, description="{desc}")\n')
            
            f.write("```\n\n")

def main():
    parser = argparse.ArgumentParser(description="Extract information about LangChain document loaders")
    parser.add_argument("--output-dir", default="loader_analysis", help="Directory to save output files")
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Find path to langchain_community/document_loaders
    try:
        langchain_path = os.path.dirname(langchain_community.__file__)
        loaders_path = os.path.join(langchain_path, "document_loaders")
        
        if not os.path.isdir(loaders_path):
            print(f"Cannot find document_loaders directory at {loaders_path}")
            sys.exit(1)
            
        print(f"Found document_loaders directory at {loaders_path}")
    except Exception as e:
        print(f"Error finding document_loaders directory: {str(e)}")
        sys.exit(1)
    
    # Extract loader information
    print("Extracting information about document loaders...")
    loaders_info = get_all_loaders(loaders_path)
    print(f"Found {len(loaders_info)} document loaders")
    
    # Categorize loaders
    print("Categorizing loaders...")
    categorized_loaders = categorize_loaders(loaders_info)
    
    # Save to JSON
    json_output = os.path.join(args.output_dir, "document_loaders_info.json")
    with open(json_output, 'w') as f:
        json.dump([asdict(loader) for loader in categorized_loaders], f, indent=2)
    print(f"Saved JSON data to {json_output}")
    
    # Generate Markdown documentation
    markdown_output = os.path.join(args.output_dir, "document_loaders_analysis.md")
    generate_markdown(categorized_loaders, markdown_output)
    print(f"Generated Markdown documentation: {markdown_output}")
    
    # Provide stats
    sources = {}
    for loader in categorized_loaders:
        sources[loader.source_type] = sources.get(loader.source_type, 0) + 1
    
    print("\nDocument Loader Statistics:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} loaders")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()