import os
import importlib
import inspect
import functools
from enum import Enum
from typing import Any, Dict, List, Type, Optional, Tuple, Union, get_type_hints
from pydantic import BaseModel, Field, field_validator


BASE_CLASS_MAP = {
    "langchain_community.retrievers": "BaseRetriever",
    "langchain_community.tools": "BaseTool",
    "langchain_community.document_loaders": "BaseDocumentLoader",
}


@functools.lru_cache(maxsize=None)  # ✅ Cache lookups for efficiency
def get_available_classes(module_name: str) -> Dict[str, Dict[str, Any]]:
    """
    Get available classes from a module with metadata:
    - `description`: Class docstring.
    - `parent_classes`: Parent classes (excluding base class).
    - `attributes`: Attributes & defaults.
    - `methods`: Available methods & signatures.
    - `missing_env_vars`: Required environment variables.
    - `has_validate_environment`: If `validate_environment` exists.

    Args:
        module_name (str): The module to scan.

    Returns:
        Dict[str, Dict[str, Any]]: Mapping of class names to metadata.
    """
    try:
        module = importlib.import_module(module_name)
        available_classes = {}
        base_class_to_ignore = BASE_CLASS_MAP.get(module_name, None)

        for cls_name in getattr(module, "__all__", []):
            cls = getattr(module, cls_name, None)
            if not inspect.isclass(cls):
                continue

            # ✅ Extract metadata
            docstring = cls.__doc__.strip() if cls.__doc__ else "No description available."
            parent_classes = [
                base.__name__
                for base in cls.__bases__
                if base.__name__ not in {"object", base_class_to_ignore}
            ]
            attributes = _extract_class_attributes(cls)
            methods = _extract_class_methods(cls)
            missing_env_vars = _check_required_env_vars(cls)
            has_validate_environment = hasattr(cls, "validate_environment")

            # ✅ Store metadata
            available_classes[cls_name] = {
                "description": docstring,
                "parent_classes": parent_classes,
                "attributes": attributes,
                "methods": methods,
                "missing_env_vars": missing_env_vars,
                "has_validate_environment": has_validate_environment,
            }

        return available_classes

    except ImportError as e:
        raise ImportError(f"Failed to import module {module_name}: {e}")


def _extract_class_attributes(cls) -> Dict[str, Any]:
    """
    Extracts class attributes (including default values), safely resolving types.

    Args:
        cls (Type): The class to inspect.

    Returns:
        Dict[str, Any]: A dictionary of attribute names and their default values.
    """
    attributes = {}
    try:
        type_hints = get_type_hints(cls, globalns=globals(), localns=locals())  # ✅ Fixed
    except Exception:
        type_hints = {}  # ✅ If evaluation fails, default to empty hints

    for name, attr in type_hints.items():
        try:
            attr_name = attr.__name__ if hasattr(attr, "__name__") else str(attr)
        except Exception:
            attr_name = "UnknownType"  # ✅ If unknown type, fallback safely

        default_value = getattr(cls, name, None)
        attributes[name] = {
            "type": attr_name,
            "default": default_value,
        }

    return attributes


def _extract_class_methods(cls) -> Dict[str, Dict[str, str]]:
    """
    Extract methods that are **defined or overridden** in the given class (not just inherited).
    """
    methods = {}

    for name, method in cls.__dict__.items():
        if inspect.isfunction(method) or inspect.ismethod(method):
            sig = inspect.signature(method)
            methods[name] = {
                param: str(sig.parameters[param].annotation)
                for param in sig.parameters
            }

    return methods


def _check_required_env_vars(cls) -> List[str]:
    """
    Identify missing environment variables required for class instantiation.

    Args:
        cls (Type): The class to inspect.

    Returns:
        List[str]: List of missing environment variables.
    """
    missing_env_vars = []
    for base in cls.__bases__:
        if "APIWrapper" in base.__name__:
            api_wrapper_init = inspect.signature(base.__init__)
            for param in api_wrapper_init.parameters:
                if param.isupper() and param not in os.environ:
                    missing_env_vars.append(param)
    return missing_env_vars


class DynamicModuleConfig(BaseModel):
    """
    Configuration for dynamically loading LangChain components (retrievers, tools, API wrappers, etc.).
    """
    module_name: str = Field(description="Module path for dynamic loading (e.g., 'langchain_community.retrievers')")
    class_type: Optional[str] = Field(default=None, description="Specific class to load from the module.")
    init_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Initialization arguments.")

    @field_validator("module_name")
    @classmethod
    def validate_module_name(cls, v: str) -> str:
        """
        Validate that the class type exists in the specified module.
        """

        module_name = v
        if not module_name:
            raise ValueError("Module name must be provided ")
        return module_name

    @field_validator("class_type")
    @classmethod
    def validate_class_type(cls, v: Union[str, None], values) -> str:
        """
        Validate that the class type exists in the specified module.
        """
        module_name = values.data.get("module_name")
        if v is not None:
            available_classes = get_available_classes(module_name)
            if v not in available_classes:
                raise ValueError(
                    f"Invalid class '{v}' for module '{module_name}'. Available: {list(available_classes.keys())}"
                )
        else:
            return v

    def load_instance(self) -> Any:
        """
        Dynamically loads and returns an instance of the specified class.
        """
        try:
            module = importlib.import_module(self.module_name)
            component_class = getattr(module, self.class_type)

            return component_class(**self.init_kwargs)  # ✅ Instantiate dynamically

        except ImportError as e:
            raise ImportError(f"Failed to import module {self.module_name}: {e}")
        except AttributeError as e:
            raise AttributeError(f"Class '{self.class_type}' not found in '{self.module_name}': {e}")

    def get_class_metadata(self) -> Dict[str, Any]:
        """
        Get metadata (docstring, parent classes, attributes, methods, missing environment variables).

        Returns:
            Dict[str, Any]: Class metadata.
        """
        available_classes = get_available_classes(self.module_name)
        if self.class_type not in available_classes:
            raise ValueError(f"Class '{self.class_type}' not found in module '{self.module_name}'")

        return available_classes[self.class_type]

"""
# ✅ Example Usage - Load a Retriever
RetrieverType = Enum("RetrieverType", {cls: cls for cls in get_available_classes("langchain_community.retrievers")}, type=str)

retriever_config = DynamicModuleConfig(
    module_name="langchain_community.retrievers",
    class_type="TavilySearchAPIRetriever",
    init_kwargs={"k": 5}
)

retriever = retriever_config.load_instance()
metadata = retriever_config.get_class_metadata()

# ✅ Pretty Print the Extracted Info
print(f"🔹 Retriever: {retriever}")
print(f"📝 Description: {metadata['description']}")
print(f"👨‍👩‍👧 Parent Classes: {metadata['parent_classes']}")
print(f"📌 Attributes: {metadata['attributes']}")
print(f"🛠️ Methods: {metadata['methods']}")
print(f"🔑 Missing Env Vars: {metadata['missing_env_vars']}")
print(f"✅ Has `validate_environment` Method: {metadata['has_validate_environment']}")
"""


# ✅ Updated Example Usage - Load a Document Loader
DocumentLoaderType = Enum(
    "RetrieverType",
    {cls: cls for cls in get_available_classes("langchain_community.document_loaders")},
    type=str
)
from langchain_community.document_loaders import AZLyricsLoader

loader_config = DynamicModuleConfig(
    module_name="langchain_community.document_loaders",
    #class_type="TextLoader",  # Replace with a valid loader class you want to use
    #init_kwargs={"file_path": "example.txt"}  # Customize based on your loader’s __init__ params
)

loader = loader_config.load_instance()
metadata = loader_config.get_class_metadata()

# ✅ Pretty Print the Extracted Info
print(f"📄 Document Loader: {loader}")
print(f"📝 Description: {metadata['description']}")
print(f"👨‍👩‍👧 Parent Classes: {metadata['parent_classes']}")
print(f"📌 Attributes: {metadata['attributes']}")
print(f"🛠️ Methods: {metadata['methods']}")
print(f"🔑 Missing Env Vars: {metadata['missing_env_vars']}")
print(f"✅ Has `validate_environment` Method: {metadata['has_validate_environment']}")
import json


if __name__ == "__main__":
    module_name = "langchain_community.document_loaders.parsers"
    metadata = get_available_classes(module_name)

    with open("all_document_loaders_parsers_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

    print("✅ Saved metadata to all_document_loaders_parsers_metadata.json with full structure.")
import json

with open("all_document_loaders_parsers_metadata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level keys (class names):")
for key in data:
    print("-", key)
