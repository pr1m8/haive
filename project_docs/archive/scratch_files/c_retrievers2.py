import functools
import importlib
import inspect
import json
import os
from typing import Any, Dict, List, get_type_hints

BASE_CLASS_MAP = {
    "langchain_community.retrievers": "BaseRetriever",
    "langchain_community.tools": "BaseTool",
    "langchain_community.document_loaders": "BaseDocumentLoader",
    "langchain_text_splitters": "BaseSplitter",
}


@functools.lru_cache(maxsize=None)
def get_available_classes(module_name: str) -> dict[str, dict[str, Any]]:
    try:
        module = importlib.import_module(module_name)
        available_classes = {}
        base_class_to_ignore = BASE_CLASS_MAP.get(module_name)

        for cls_name in getattr(module, "__all__", []):
            cls = getattr(module, cls_name, None)
            if not inspect.isclass(cls):
                continue

            docstring = (
                cls.__doc__.strip() if cls.__doc__ else "No description available."
            )
            parent_classes = [
                base.__name__
                for base in cls.__bases__
                if base.__name__ not in {"object", base_class_to_ignore}
            ]
            attributes = _extract_class_attributes(cls)
            methods = _extract_class_methods(cls)
            missing_env_vars = _check_required_env_vars(cls)
            has_validate_environment = hasattr(cls, "validate_environment")

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


def _extract_class_attributes(cls) -> dict[str, Any]:
    attributes = {}
    try:
        type_hints = get_type_hints(cls, globalns=globals(), localns=locals())
    except Exception:
        type_hints = {}

    for name, attr in type_hints.items():
        try:
            attr_name = attr.__name__ if hasattr(attr, "__name__") else str(attr)
        except Exception:
            attr_name = "UnknownType"

        default_value = getattr(cls, name, None)
        attributes[name] = {
            "type": attr_name,
            "default": str(default_value),
        }

    return attributes


def _extract_class_methods(cls) -> dict[str, dict[str, str]]:
    methods = {}
    for name, method in cls.__dict__.items():
        if inspect.isfunction(method) or inspect.ismethod(method):
            sig = inspect.signature(method)
            methods[name] = {
                param: str(sig.parameters[param].annotation) for param in sig.parameters
            }
    return methods


def _check_required_env_vars(cls) -> list[str]:
    missing_env_vars = []
    for base in cls.__bases__:
        if "APIWrapper" in base.__name__:
            try:
                api_wrapper_init = inspect.signature(base.__init__)
                for param in api_wrapper_init.parameters:
                    if param.isupper() and param not in os.environ:
                        missing_env_vars.append(param)
            except Exception:
                pass
    return missing_env_vars


if __name__ == "__main__":
    module_name = "langchain_community.document_loaders"
    metadata = get_available_classes(module_name)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(root_dir, "resources", "inspect")
    os.makedirs(output_dir, exist_ok=True)

    filename = module_name.replace(".", "_") + ".json"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

    for _cls in metadata:
        pass
