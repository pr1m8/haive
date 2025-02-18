import os
import importlib
import inspect
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel, Field, field_validator


class DynamicModuleType(str):
    """Enum for dynamically loaded module types (retrievers, tools, etc.)."""
    pass  # Populated dynamically


def get_available_classes(module_name: str) -> Dict[str, Dict[str, Any]]:
    """
    Get available classes from a module along with their descriptions, dependencies, args_schema, and tools.

    Args:
        module_name (str): The module to scan.

    Returns:
        Dict[str, Dict[str, Any]]: Mapping of class names to metadata.
    """
    try:
        module = importlib.import_module(module_name)
        available_classes = {}

        for cls_name in getattr(module, "__all__", []):
            cls = getattr(module, cls_name, None)
            if inspect.isclass(cls):
                docstring = cls.__doc__.strip() if cls.__doc__ else "No description available."
                parent_classes = [base.__name__ for base in cls.__bases__ if base.__name__ != "object"]
                init_args = list(inspect.signature(cls).parameters.keys())

                # ✅ Detect required API wrappers or dependencies
                missing_dependencies = []
                for arg in init_args:
                    if "api" in arg.lower() or "wrapper" in arg.lower():
                        missing_dependencies.append(arg)

                # ✅ Detect if class requires `Resource`
                requires_resource = "Resource" in init_args

                # ✅ Detect `args_schema` and extract its fields
                args_schema = None
                schema_fields = {}
                if hasattr(cls, "args_schema"):
                    schema_cls = getattr(cls, "args_schema")

                    # ✅ Ensure it's a Pydantic model
                    if inspect.isclass(schema_cls) and issubclass(schema_cls, BaseModel):
                        schema_fields = {
                            field_name: {
                                "description": field_info.description
                                if field_info.description else "No description available.",
                                "type": field_info.annotation.__name__
                                if hasattr(field_info, "annotation") and field_info.annotation else "Unknown",
                            }
                            for field_name, field_info in schema_cls.model_fields.items()
                        }
                        args_schema = schema_cls.__name__

                available_classes[cls_name] = {
                    "description": docstring,
                    "parent_classes": parent_classes,
                    "init_args": init_args,
                    "missing_dependencies": missing_dependencies,
                    "requires_resource": requires_resource,
                    "args_schema_class": args_schema,
                    "args_schema_fields": schema_fields if args_schema else None,
                }

        return available_classes

    except ImportError as e:
        raise ImportError(f"Failed to import module {module_name}: {e}")


class DynamicModuleConfig(BaseModel):
    """
    Configuration for dynamically loading LangChain components (retrievers, tools, API wrappers, etc.).
    """
    module_name: str = Field(description="Module path for dynamic loading (e.g., 'langchain_community.tools')")
    class_type: str = Field(description="Specific class to load from the module.")
    init_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Initialization arguments.")

    @field_validator("class_type")
    @classmethod
    def validate_class_type(cls, v: str, values) -> str:
        """
        Validate that the class type exists in the specified module.
        """
        module_name = values.data.get("module_name")
        if not module_name:
            raise ValueError("Module name must be provided before validating class_type.")

        available_classes = get_available_classes(module_name)
        if v not in available_classes:
            raise ValueError(
                f"Invalid class '{v}' for module '{module_name}'. Available: {list(available_classes.keys())}"
            )

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
        except TypeError as e:
            raise TypeError(
                f"Error instantiating '{self.class_type}': {e}. "
                "Check if required init arguments are missing."
            )

    def get_class_metadata(self) -> Dict[str, Any]:
        """
        Get metadata (docstring, dependencies, args_schema, tools) for the selected class.
        """
        available_classes = get_available_classes(self.module_name)
        if self.class_type not in available_classes:
            raise ValueError(f"Class '{self.class_type}' not found in module '{self.module_name}'")

        return available_classes[self.class_type]

    def get_tools(self) -> Union[List[Any], str]:
        """
        Call `.get_tools()` if the class supports it and return the available tools.
        """
        try:
            instance = self.load_instance()
            if hasattr(instance, "get_tools") and callable(instance.get_tools):
                return instance.get_tools()
            return "This module does not support `get_tools()`."
        except Exception as e:
            return f"Failed to retrieve tools: {e}"


# ✅ Example Usage - Detect `args_schema` and `get_tools()` in LangChain Toolkits
ToolType = DynamicModuleType

tool_config = DynamicModuleConfig(
    module_name="langchain_community.agent_toolkits",
    class_type="GmailToolkit",
)

metadata = tool_config.get_class_metadata()

try:
    tool_instance = tool_config.load_instance()
except TypeError as e:
    print(f"⚠️ Failed to instantiate '{tool_config.class_type}': {e}")

tools = tool_config.get_tools()

print(f"🔹 Tool: {tool_config.class_type}")
print(f"📝 Description: {metadata['description']}")
print(f"👨‍👩‍👧 Parent Classes: {metadata['parent_classes']}")
print(f"⚠️ Missing Dependencies: {metadata['missing_dependencies']}")
print(f"🔧 Required Init Args: {metadata['init_args']}")
print(f"📜 Args Schema Class: {metadata['args_schema_class']}")
print(f"📜 Args Schema Fields: {metadata['args_schema_fields']}")
print(f"🛠️ Tools Available: {tools}")
