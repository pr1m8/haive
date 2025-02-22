import os
import importlib
import inspect
from typing import Any, Dict, List, Optional, Type, Union, Tuple, Callable, get_type_hints
from pydantic import BaseModel, Field, field_validator
from langchain.schema import Document
from langchain.document_transformers import *
class DynamicModuleType(str):
    """Enum for dynamically loaded module types (retrievers, tools, transformers, etc.)."""
    pass  # Populated dynamically


def get_available_classes(module_names: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Get available classes from multiple modules and remove duplicates.

    Args:
        module_names (List[str]): The list of module names to scan.

    Returns:
        Dict[str, Dict[str, Any]]: Mapping of class names to metadata.
    """
    available_classes = {}

    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
            for cls_name in getattr(module, "__all__", []):
                if cls_name in available_classes:
                    continue  # Skip duplicates

                cls = getattr(module, cls_name, None)
                if not inspect.isclass(cls):
                    continue

                # ✅ Extract class metadata
                docstring = cls.__doc__.strip() if cls.__doc__ else "No description available."
                parent_classes = [base.__name__ for base in cls.__bases__ if base.__name__ != "object"]

                # ✅ Extract init args with types (handles string annotations)
                init_args = {}
                try:
                    signature = inspect.signature(cls)
                    type_hints = get_type_hints(cls)  # Resolves forward-referenced types

                    for param_name, param in signature.parameters.items():
                        param_type = (
                            type_hints.get(param_name, "Unknown")  # Use resolved type hints
                            if param_name in type_hints
                            else param.annotation.__name__
                            if hasattr(param.annotation, "__name__")
                            else str(param.annotation)  # Convert to string for unknown types
                        )
                        init_args[param_name] = param_type
                except (ValueError, TypeError):
                    pass  # Some classes have dynamic signatures or unresolvable types

                # ✅ Detect API dependencies (e.g., `api_key`, `api_wrapper`, `resource`)
                missing_dependencies = [
                    arg for arg in init_args.keys()
                    if "api" in arg.lower() or "wrapper" in arg.lower() or "resource" in arg.lower()
                ]

                # ✅ Detect `args_schema` and extract its fields
                args_schema = None
                schema_fields = {}
                if hasattr(cls, "args_schema"):
                    schema_cls = getattr(cls, "args_schema")
                    if inspect.isclass(schema_cls) and issubclass(schema_cls, BaseModel):
                        schema_fields = {
                            field_name: {
                                "description": field_info.description if field_info.description else "No description available.",
                                "type": field_info.annotation.__name__ if hasattr(field_info, "annotation") and field_info.annotation else "Unknown",
                            }
                            for field_name, field_info in schema_cls.model_fields.items()
                        }
                        args_schema = schema_cls.__name__

                available_classes[cls_name] = {
                    "description": docstring,
                    "parent_classes": parent_classes,
                    "init_args": init_args,
                    "missing_dependencies": missing_dependencies,
                    "args_schema_class": args_schema,
                    "args_schema_fields": schema_fields if args_schema else None,
                }

        except ImportError as e:
            print(f"⚠️ Failed to import module {module_name}: {e}")

    return available_classes


class DynamicModuleConfig(BaseModel):
    """
    Configuration for dynamically loading LangChain components (retrievers, tools, transformers, etc.).
    """
    module_names: List[str] = Field(
        description="List of module paths for dynamic loading (e.g., ['langchain_community.document_transformers'])"
    )
    class_type: Optional[str] = Field(None, description="Specific class to load from the modules.")
    init_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Initialization arguments.")

    def get_available_classes(self) -> Dict[str, Any]:
        """Retrieve metadata of all available classes in the specified modules."""
        return get_available_classes(self.module_names)

    def set_class_type(self, class_type: str):
        """
        Set the class_type dynamically.

        Args:
            class_type (str): The class to load.
        """
        available_classes = self.get_available_classes()
        if class_type not in available_classes:
            raise ValueError(f"Invalid class '{class_type}'. Available: {list(available_classes.keys())}")
        self.class_type = class_type

    def load_instance(self) -> Any:
        """
        Dynamically loads and returns an instance of the specified class.
        """
        if not self.class_type:
            raise ValueError("Class type must be set before loading instance.")

        for module_name in self.module_names:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, self.class_type):
                    component_class = getattr(module, self.class_type)

                    if "model_rebuild" in dir(component_class):  # ✅ Handle Pydantic validation issues
                        component_class.model_rebuild()

                    return component_class(**self.init_kwargs)  # ✅ Instantiate dynamically

            except ImportError:
                continue  # Skip to the next module
            except AttributeError:
                continue  # Skip to the next module
            except TypeError as e:
                raise TypeError(
                    f"Error instantiating '{self.class_type}': {e}. "
                    "Check if required init arguments are missing."
                )

        raise ImportError(f"Class '{self.class_type}' not found in any of the modules: {self.module_names}")

    def get_class_metadata(self) -> Dict[str, Any]:
        """Get metadata (docstring, dependencies, args_schema, tools) for the selected class."""
        if not self.class_type:
            raise ValueError("Class type must be set before retrieving metadata.")

        available_classes = self.get_available_classes()
        if self.class_type not in available_classes:
            raise ValueError(f"Class '{self.class_type}' not found in the given modules.")

        return available_classes[self.class_type]


# ✅ **Example Usage**
config = DynamicModuleConfig(module_names=["langchain_community.agent_toolkits"])
# 🎯 Step 1: Retrieve available classes
available_classes = config.get_available_classes()
print(f"📌 Available Classes: {list(available_classes.keys())}")

# 🎯 Step 2: Set class type dynamically
config.set_class_type("BeautifulSoupTransformer")  # Change this to any document transformer

# 🎯 Step 3: Retrieve class metadata
metadata = config.get_class_metadata()
print(f"🔹 Class: {config.class_type}")
print(f"📝 Description: {metadata['description']}")
print(f"👨‍👩‍👧 Parent Classes: {metadata['parent_classes']}")
print(f"⚠️ Missing Dependencies: {metadata['missing_dependencies']}")
print(f"🔧 Required Init Args: {metadata['init_args']}")
print(f"📜 Args Schema Class: {metadata['args_schema_class']}")
print(f"📜 Args Schema Fields: {metadata['args_schema_fields']}")

# 🎯 Step 4: Load instance & correctly handle different types
try:
    instance = config.load_instance()

    # ✅ If it's a document transformer, call `.transform_documents()`
    if "BaseDocumentTransformer" in metadata["parent_classes"]:
        docs = [Document(page_content="Hello, world!", metadata={"source": "test"})]
        transformed_docs = instance.transform_documents(docs)
        print(f"✅ Successfully transformed documents: {transformed_docs}")
    else:
        print(f"✅ Successfully loaded instance: {instance}")

except Exception as e:
    pri
