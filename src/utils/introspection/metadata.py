import inspect
import os
from typing import Type, Any, Dict, List, get_type_hints
from pydantic import BaseModel, create_model


def get_env_from_docstring(obj: Any) -> List[str]:
    doc = inspect.getdoc(obj) or ""
    return sorted({
        token for line in doc.splitlines() for token in line.split()
        if token.isupper() and "_" in token
    })

def analyze_env_vars(env_vars: List[str], actual_env: Dict[str, str]) -> Dict[str, List[str]]:
    return {
        "env_required": env_vars,
        "env_found": [e for e in env_vars if e in actual_env],
        "env_missing": [e for e in env_vars if e not in actual_env],
    }

def safe_signature(cls: Type) -> inspect.Signature:
    try:
        return inspect.signature(cls.__init__)
    except Exception:
        return inspect.Signature()

def create_arg_schema(cls: Type, force: bool = False) -> BaseModel:
    sig = safe_signature(cls)
    fields = {
        name: (
            param.annotation if param.annotation != inspect._empty else Any,
            param.default if param.default != inspect._empty else ...
        )
        for name, param in sig.parameters.items() if name != "self"
    }
    base = {"__config__": type("Config", (), {"arbitrary_types_allowed": True})} if force else {}
    return create_model(f"{cls.__name__}Args", **base, **fields)

def extract_output_type(cls: Type) -> str:
    for method_name in ["load", "get_relevant_documents", "invoke"]:
        if hasattr(cls, method_name):
            try:
                return_type = get_type_hints(getattr(cls, method_name)).get("return")
                return str(return_type) if return_type else "Unknown"
            except Exception:
                continue
    return "Unknown"

def extract_metadata(cls: Type, module_name: str, actual_env: Dict[str, str], tool_type: str) -> Dict[str, Any]:
    docstring = inspect.getdoc(cls) or ""
    env_vars = get_env_from_docstring(cls)
    env_status = analyze_env_vars(env_vars, actual_env)

    try:
        arg_model = create_arg_schema(cls, force=False)
        arg_schema = arg_model.model_json_schema()
        serializable = True
        forced = False
    except Exception:
        try:
            arg_model = create_arg_schema(cls, force=True)
            arg_schema = arg_model.model_json_schema()
            serializable = True
            forced = True
        except Exception as e:
            arg_schema = {}
            serializable = False
            forced = False
            env_status["schema_error"] = str(e)

    return {
        "tool_type": tool_type,
        "module": module_name,
        "class_name": cls.__name__,
        "description": docstring.split("\n")[0],
        "docstring": docstring,
        "arg_schema": arg_schema,
        "output_schema_hint": extract_output_type(cls),
        "is_serializable": serializable,
        "forced_serializable": forced,
        **env_status
    }
