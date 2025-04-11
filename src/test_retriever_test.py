import os
import pkgutil
import importlib
import inspect
import json
from typing import List, Type, Dict, Any
from pydantic import BaseModel, create_model
from langchain_core.tools import StructuredTool
import langchain_community.retrievers as base_retriever_pkg
from dotenv import dotenv_values


def load_env_files(example_path=".env", actual_path=".env") -> dict:
    return {
        "example_vars": dotenv_values(example_path),
        "actual_vars": dotenv_values(actual_path),
    }


def analyze_env_vars(required_vars: List[str], env_info: dict) -> dict:
    return {
        "env_required": required_vars,
        "env_found": [var for var in required_vars if var in env_info["actual_vars"]],
        "env_missing": [var for var in required_vars if var not in env_info["actual_vars"]],
    }


def safe_signature(cls: Type) -> inspect.Signature:
    try:
        return inspect.signature(cls.__init__)
    except Exception:
        return inspect.Signature()


def create_arg_schema(cls: Type, force_serializable: bool = False) -> Type[BaseModel]:
    sig = safe_signature(cls)
    fields = {
        name: (
            param.annotation if param.annotation != inspect._empty else Any,
            param.default if param.default != inspect._empty else ...
        )
        for name, param in sig.parameters.items() if name != "self"
    }

    base = {"__config__": type("Config", (), {"arbitrary_types_allowed": True})} if force_serializable else {}
    return create_model(f"{cls.__name__}Args", **base, **fields)


def get_required_env_vars(cls: Type) -> List[str]:
    doc = inspect.getdoc(cls) or ""
    return sorted({
        token for line in doc.splitlines() for token in line.split()
        if token.isupper() and "_" in token and token not in os.environ
    })


def create_retriever_tool(cls: Type, module_name: str, env_info: dict) -> StructuredTool:
    arg_model = create_arg_schema(cls)
    env_vars = get_required_env_vars(cls)
    env_status = analyze_env_vars(env_vars, env_info)
    description = inspect.getdoc(cls) or "LangChain Retriever"

    def retriever_func(**kwargs):
        instance = cls(**kwargs)
        return str(instance)

    try:
        schema = arg_model.model_json_schema()
        serializable = True
        forced = False
    except Exception:
        try:
            arg_model = create_arg_schema(cls, force_serializable=True)
            schema = arg_model.model_json_schema()
            serializable = True
            forced = True
        except Exception as e:
            schema = {}
            serializable = False
            forced = False
            env_status["schema_error"] = str(e)

    return StructuredTool.from_function(
        func=retriever_func,
        name=cls.__name__,
        description=description,
        args_schema=arg_model,
        metadata={
            "retriever_class": cls.__name__,
            "retriever_module": module_name,
            "arg_schema": schema,
            "is_serializable": serializable,
            "forced_serializable": forced,
            **env_status
        }
    )


def find_all_retriever_classes(base_pkg) -> List[tuple[Type, str]]:
    retrievers = []
    for _, module_name, _ in pkgutil.walk_packages(base_pkg.__path__, base_pkg.__name__ + "."):
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"❌ Failed to import {module_name}: {e}")
            continue

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if "Retriever" in name and callable(getattr(cls, "__init__", None)):
                retrievers.append((cls, module_name))
    return retrievers


def print_summary(tool: StructuredTool):
    meta = tool.metadata
    print(f"\n🧰 {tool.name}")
    print(f"📄 {tool.description[:80]}...")
    print(f"📦 Module: {meta.get('retriever_module')}")
    print(f"🧠 Serializable: {meta.get('is_serializable')}")
    if meta.get("forced_serializable"):
        print("⚠️  Forced serialization used")
    if meta.get("env_required"):
        print(f"🔐 Requires ENV: {meta['env_required']}")
        print(f"✅ Found: {meta['env_found']}")
        print(f"❌ Missing: {meta['env_missing']}")
    if meta.get("arg_schema"):
        print("🧾 Args Schema:")
        print(json.dumps(meta["arg_schema"], indent=2))


def main():
    print("🔍 Searching for LangChain retrievers...\n")
    env_info = load_env_files()
    retriever_classes = find_all_retriever_classes(base_retriever_pkg)

    structured = []
    failed = []
    forced = []

    for cls, module_name in retriever_classes:
        try:
            tool = create_retriever_tool(cls, module_name, env_info)
            structured.append(tool)
            if tool.metadata.get("forced_serializable"):
                forced.append(tool.name)
            print_summary(tool)
        except Exception as e:
            failed.append((cls.__name__, str(e)))

    print("\n🔢 Stats:")
    print(f"✅ Wrapped: {len(structured)}")
    print(f"⚠️  Forced serializable: {len(forced)}")
    print(f"❌ Failed: {len(failed)}")

    missing_env = sorted(set(var for t in structured for var in t.metadata.get("env_missing", [])))
    if missing_env:
        print("\n🔐 Missing ENV Vars:")
        for var in missing_env:
            print(f"  - {var}")
    else:
        print("\n✅ All required environment variables appear to be set.")


if __name__ == "__main__":
    main()
