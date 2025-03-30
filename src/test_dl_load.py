import os
import pkgutil
import importlib
import inspect
import json
from typing import List, Type, Dict, Any
from pydantic import BaseModel, create_model
from langchain_core.tools import StructuredTool
import langchain_community.document_loaders as base_loader_pkg

from dotenv import dotenv_values

def load_env_files(example_path=".env.example", actual_path=".env") -> dict:
    example_vars = dotenv_values(example_path)
    actual_vars = dotenv_values(actual_path)
    return {
        "example_vars": example_vars,
        "actual_vars": actual_vars,
    }

def analyze_loader_env(loader_env_vars: List[str], env_info: dict) -> dict:
    found = []
    missing = []

    for var in loader_env_vars:
        if var in env_info["actual_vars"]:
            found.append(var)
        else:
            missing.append(var)

    return {
        "env_required": loader_env_vars,
        "env_found": found,
        "env_missing": missing,
    }

def safe_signature(cls: Type) -> inspect.Signature:
    try:
        return inspect.signature(cls.__init__)
    except Exception:
        return inspect.Signature()  # Empty signature fallback


def create_arg_schema(cls: Type, force_serializable: bool = False) -> Type[BaseModel]:
    sig = safe_signature(cls)
    fields = {}

    for name, param in sig.parameters.items():
        if name == "self":
            continue
        ann = param.annotation if param.annotation != inspect._empty else Any
        default = param.default if param.default != inspect._empty else ...
        fields[name] = (ann, default)

    if force_serializable:
        return create_model(
            f"{cls.__name__}Args",
            __config__=type("Config", (), {"arbitrary_types_allowed": True}),
            **fields,
        )
    else:
        return create_model(f"{cls.__name__}Args", **fields)


def get_required_env_vars(cls: Type) -> List[str]:
    """
    Naively scan __init__ signature or docstring for environment variable names.
    """
    env_vars = []

    doc = inspect.getdoc(cls) or ""
    for line in doc.splitlines():
        for token in line.split():
            if token.isupper() and "_" in token:
                if token in os.environ:
                    continue
                env_vars.append(token)

    return sorted(set(env_vars))


def extract_metadata(cls: Type, arg_model: Type[BaseModel], module_name: str) -> Dict[str, Any]:
    env_vars = get_required_env_vars(cls)

    try:
        json_schema = arg_model.model_json_schema()
        return {
            "loader_class": cls.__name__,
            "loader_module": module_name,
            "arg_schema": json_schema,
            "is_serializable": True,
            "forced_serializable": False,
            "env_required": env_vars,
        }
    except Exception:
        try:
            # Retry with forced model
            arg_model = create_arg_schema(cls, force_serializable=True)
            return {
                "loader_class": cls.__name__,
                "loader_module": module_name,
                "arg_schema": arg_model.model_json_schema(),
                "is_serializable": True,
                "forced_serializable": True,
                "env_required": env_vars,
            }
        except Exception as e:
            return {
                "loader_class": cls.__name__,
                "loader_module": module_name,
                "arg_schema": {},
                "is_serializable": False,
                "forced_serializable": False,
                "env_required": env_vars,
                "schema_error": str(e),
            }
def create_loader_tool(cls: Type, module_name: str, env_info: dict) -> StructuredTool:
    arg_model = create_arg_schema(cls, force_serializable=False)
    description = inspect.getdoc(cls) or "LangChain Document Loader"

    def loader_function(**kwargs):
        instance = cls(**kwargs)
        return instance.load()

    # extract env
    required_env = get_required_env_vars(cls)
    env_status = analyze_loader_env(required_env, env_info)

    # build metadata
    try:
        json_schema = arg_model.model_json_schema()
        metadata = {
            "loader_class": cls.__name__,
            "loader_module": module_name,
            "arg_schema": json_schema,
            "is_serializable": True,
            "forced_serializable": False,
            **env_status,
        }
    except Exception:
        try:
            arg_model = create_arg_schema(cls, force_serializable=True)
            metadata = {
                "loader_class": cls.__name__,
                "loader_module": module_name,
                "arg_schema": arg_model.model_json_schema(),
                "is_serializable": True,
                "forced_serializable": True,
                **env_status,
            }
        except Exception as e:
            metadata = {
                "loader_class": cls.__name__,
                "loader_module": module_name,
                "arg_schema": {},
                "is_serializable": False,
                "forced_serializable": False,
                "schema_error": str(e),
                **env_status,
            }

    return StructuredTool.from_function(
        func=loader_function,
        name=cls.__name__,
        description=description,
        args_schema=arg_model,
        metadata=metadata
    )


def print_loader_summary(tool: StructuredTool):
    meta = tool.metadata
    print(f"\n🧰 {tool.name}")
    print(f"📄 {tool.description[:80]}...")
    print(f"📦 Module: {meta.get('loader_module')}")
    print(f"🧠 Serializable: {meta.get('is_serializable')}")
    if meta.get("forced_serializable"):
        print(f"⚠️  Forced serialization used")

    # Show ENV status
    if meta.get("env_required"):
        print(f"🔐 Requires ENV: {meta['env_required']}")
        print(f"✅ Found: {meta['env_found']}")
        print(f"❌ Missing: {meta['env_missing']}")

    if meta.get("arg_schema"):
        print("🧾 Args Schema:")
        print(json.dumps(meta["arg_schema"], indent=2))


def find_all_loader_classes(base_pkg) -> List[tuple[Type, str]]:
    loader_classes = []
    for _, module_name, _ in pkgutil.walk_packages(base_pkg.__path__, base_pkg.__name__ + "."):
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"❌ Failed import: {module_name}: {e}")
            continue

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if hasattr(cls, "load") and callable(getattr(cls, "load")):
                loader_classes.append((cls, module_name))
    return loader_classes

def print_loader_summary(tool: StructuredTool):
    meta = tool.metadata
    print(f"\n🧰 {tool.name}")
    print(f"📄 {tool.description[:80]}...")
    print(f"📦 Module: {meta.get('loader_module')}")
    print(f"🧠 Serializable: {meta.get('is_serializable')}")
    if meta.get("forced_serializable"):
        print(f"⚠️  Forced serialization used")

    # Show ENV status
    if meta.get("env_required"):
        print(f"🔐 Requires ENV: {meta['env_required']}")
        print(f"✅ Found: {meta['env_found']}")
        print(f"❌ Missing: {meta['env_missing']}")

    if meta.get("arg_schema"):
        print("🧾 Args Schema:")
        print(json.dumps(meta["arg_schema"], indent=2))

def main():
    print("🔍 Searching for LangChain loaders...\n")
    env_info = load_env_files()  # ✅ load this first
    loader_classes = find_all_loader_classes(base_loader_pkg)

    structured = []
    failed = []
    forced = []
    non_serializable = []

    for cls, module_name in loader_classes:
        try:
            tool = create_loader_tool(cls, module_name, env_info)  # ✅ pass env_info here
            structured.append(tool)

            if not tool.metadata.get("is_serializable"):
                non_serializable.append(tool.name)
            elif tool.metadata.get("forced_serializable"):
                forced.append(tool.name)

            print_loader_summary(tool)

        except Exception as e:
            failed.append((cls.__name__, str(e)))

    print("\n🔢 Stats:")
    print(f"✅ Wrapped successfully: {len(structured)}")
    print(f"⚠️  Forced serializable: {len(forced)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"🔒 Non-serializable: {len(non_serializable)}")
    # Unique env vars needed but missing
    missing_env = set()
    for tool in structured:
        missing_env.update(tool.metadata.get("env_missing", []))

    if missing_env:
        print("\n🔐 Missing ENV variables across loaders:")
        for var in sorted(missing_env):
            print(f"  - {var}")
    else:
        print("\n✅ All required environment variables appear to be set.")
main()