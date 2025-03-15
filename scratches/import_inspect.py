import importlib
import inspect
from typing import Dict, Type, Any, List, Optional

def get_retrievers(module_name: str, serialize: bool = True) -> Dict[str, Any]:
    """
    Dynamically loads retrievers, handles dynamic imports, and extracts metadata.

    Args:
        module_name (str): The module to inspect (e.g., "langchain.retrievers").
        serialize (bool): If True, converts non-serializable objects to strings.

    Returns:
        Dict[str, Any]: A structured dictionary containing retriever details.
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise ValueError(f"Module '{module_name}' not found.")

    retriever_names = getattr(module, "__all__", [])
    module_lookup = getattr(module, "_module_lookup", {})

    retrievers = {}
    base_retriever_name = "BaseRetriever"  # Store this once instead of repeating it

    for name in retriever_names:
        retriever_module_name = module_lookup.get(name, module_name)

        try:
            retriever_module = importlib.import_module(retriever_module_name)
            retriever_class = getattr(retriever_module, name, None)

            if retriever_class is None and hasattr(module, "__getattr__"):
                retriever_class = module.__getattr__(name)

            if retriever_class:
                # Extract core details
                class_docstring = inspect.getdoc(retriever_class) or "No class docstring available."
                init_args, init_docstring = extract_init_info(retriever_class)
                properties = extract_class_properties(retriever_class)
                methods = extract_methods(retriever_class)

                # Extract base classes but remove `BaseRetriever`
                base_classes = [
                    base.__name__ for base in retriever_class.__bases__ if base.__name__ != base_retriever_name
                ]
                additional_wrappers = [
                    base.__name__ for base in retriever_class.__bases__ if base.__name__ not in [base_retriever_name]
                ]

                # Detect API key requirement
                requires_api_key = detect_api_key_requirement(retriever_class)

                # Extract wrapper class details
                wrapper_details = extract_wrapper_details(retriever_class)

                # Check for validate_environment and ImportError
                validate_environment, import_error = extract_validate_environment(retriever_class)

                retrievers[name] = {
                    "class": retriever_class.__name__ if serialize else retriever_class,
                    "import_path": f"{retriever_module_name}.{name}",
                    "class_docstring": class_docstring,
                    "init_args": {k: str(v) for k, v in init_args.items()} if serialize else init_args,
                    "init_docstring": init_docstring,
                    "properties": {
                        k: {"type": str(v["type"]), "default": str(v["default"])}
                        for k, v in properties.items()
                    } if serialize else properties,
                    "methods": {
                        method: {
                            "parameters": {k: str(v) for k, v in meta["parameters"].items()},
                            "return_type": str(meta["return_type"])
                        }
                        for method, meta in methods.items()
                    } if serialize else methods,
                    "base_classes": base_classes,  # ✅ No `BaseRetriever`
                    "additional_wrappers": additional_wrappers,
                    "requires_api_key": requires_api_key,
                    "wrapper_details": wrapper_details if not serialize else {
                        wrapper: {
                            "docstring": meta["docstring"],
                            "init_args": {k: str(v) for k, v in meta["init_args"].items()},
                            "properties": {
                                k: {"type": str(v["type"]), "default": str(v["default"])}
                                for k, v in meta["properties"].items()
                            },
                            "methods": {
                                method: {
                                    "parameters": {k: str(v) for k, v in meta["methods"][method]["parameters"].items()},
                                    "return_type": str(meta["methods"][method]["return_type"])
                                }
                                for method in meta["methods"]
                            }
                        }
                        for wrapper, meta in wrapper_details.items()
                    },
                    "validate_environment": validate_environment,
                    "import_error": import_error
                }
        except ImportError as e:
            print(f"⚠ {name} requires missing dependencies. Error: {e}")
        except AttributeError as e:
            print(f"⚠ {name} not found in {retriever_module_name}. Error: {e}")

    return {
        "module": module_name,
        "base_class": base_retriever_name,  # ✅ Stored at the top level only once
        "retrievers": retrievers
    }

def extract_methods(cls: Type) -> Dict[str, Dict[str, Any]]:
    """
    Extracts all methods of a class, including method signatures and return types.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary where:
            - Keys are method names.
            - Values contain:
                - "parameters": Dict of parameter names and their types.
                - "return_type": The return type of the method.
                - "method_type": One of ["instance", "class", "static"].
    """
    methods = {}

    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith("__"):
            continue  # Skip dunder methods

        signature = inspect.signature(method)

        # Extract parameter types
        parameters = {
            param.name: str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
            for param in signature.parameters.values()
            if param.name != "self" and param.name != "cls"
        }

        # Extract return type
        return_type = (
            str(signature.return_annotation) if signature.return_annotation != inspect.Signature.empty else "Unknown"
        )

        # Determine if method is instance, class, or static
        if isinstance(method, classmethod):
            method_type = "class"
        elif isinstance(method, staticmethod):
            method_type = "static"
        else:
            method_type = "instance"

        methods[name] = {
            "parameters": parameters,
            "return_type": return_type,
            "method_type": method_type
        }

    return methods


def extract_init_info(cls: Type) -> (Dict[str, Any], Optional[str]):
    """Extracts __init__ method parameters and docstring, including inherited ones."""
    init_args = {}
    init_docstring = None
    found_init = False

    for base in inspect.getmro(cls):
        try:
            if base is object:
                break

            init_method = base.__init__
            init_signature = inspect.signature(init_method)

            for param in init_signature.parameters.values():
                if param.name != "self" and param.name not in init_args:
                    init_args[param.name] = (
                        param.default if param.default is not inspect.Parameter.empty else "REQUIRED"
                    )

            if not found_init and inspect.getdoc(init_method):
                init_docstring = inspect.getdoc(init_method)
                found_init = True

        except AttributeError:
            continue

    return init_args, init_docstring or "No __init__ docstring available."


def extract_class_properties(cls: Type) -> Dict[str, Any]:
    """Extracts explicitly defined class attributes."""
    properties = {}

    for name, value in cls.__annotations__.items():
        properties[name] = {"type": value, "default": None}

    for name, value in cls.__dict__.items():
        if not name.startswith("__") and name in properties:
            properties[name]["default"] = value

    return properties


def detect_api_key_requirement(cls: Type) -> bool:
    """Detects if a retriever requires an API key based on its base class docstrings."""
    for base in inspect.getmro(cls):
        if base is object:
            break

        docstring = inspect.getdoc(base)
        if docstring and any(
            keyword in docstring.lower()
            for keyword in ["api", "authentication", "external service", "key"]
        ):
            return True

    return False


def extract_wrapper_details(cls: Type) -> Dict[str, Any]:
    """Extracts __init__ arguments, properties, and docstrings from wrapper classes."""
    wrapper_details = {}

    for base in cls.__bases__:
        if base.__name__ == "BaseRetriever":
            continue

        wrapper_details[base.__name__] = {
            "docstring": inspect.getdoc(base) or "No wrapper docstring available.",
            "init_args": extract_init_info(base)[0],
            "properties": extract_class_properties(base)
        }

    return wrapper_details




def extract_validate_environment(cls: Type) -> (bool, Optional[str]):
    """Checks if a class or any of its wrapper classes have `validate_environment` and detects ImportError."""
    for base in inspect.getmro(cls):
        if base is object:
            break

        if hasattr(base, "validate_environment") and inspect.isfunction(base.validate_environment):
            source = inspect.getsource(base.validate_environment)
            if "ImportError" in source:
                return True, source
            return True, None

    return False, None


# Example usage
retrievers = get_retrievers("langchain_community.agent_toolkits")

# Print dynamically found retrievers with inheritance details
for name, meta in retrievers.items():
    print(f"\n🔹 {name}")
    print(f"📄 Class Docstring:\n{meta['class_docstring'][:300]}...")
    print(f"🔧 Init Arguments: {meta['init_args']}")
    print(f"📄 Init Docstring:\n{meta['init_docstring'][:300]}...")
    print(f"🏷️ Properties: {meta['properties']}")
    print(f"🔗 Base Classes: {meta['base_classes']}")
    print(f"🧩 Additional Wrappers: {meta['additional_wrappers']}")
    print(f"🔍 Wrapper Details: {meta['wrapper_details']}")
    print(f"🔑 Requires API Key: {meta['requires_api_key']}")
    print(f"🛠️ Has `validate_environment`: {meta['validate_environment']}")
    print(f"⚠ ImportError in `validate_environment`: {meta['import_error']}")
