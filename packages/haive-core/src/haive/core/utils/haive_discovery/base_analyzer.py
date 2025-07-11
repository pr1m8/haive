"""Base analyzer class and common functionality for component analysis."""

import inspect
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, ConfigDict, create_model

from haive.core.utils.haive_discovery.component_info import ComponentInfo

logger = logging.getLogger(__name__)


class ComponentAnalyzer(ABC):
    """Abstract base class for component analyzers."""

    @abstractmethod
    def can_analyze(self, obj: Any) -> bool:
        """Check if this analyzer can handle the given object."""

    @abstractmethod
    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        """Analyze the object and return component info."""

    def create_tool(self, component_info: ComponentInfo) -> Any | None:
        """Convert component to a StructuredTool if possible."""
        return None

    def create_engine_config(self, component_info: ComponentInfo) -> Any | None:
        """Create a Haive engine config if possible."""
        return None

    def safe_get_name(self, obj: Any, default_prefix: str = "Component") -> str:
        """Safely get the name of an object."""
        try:
            if hasattr(obj, "__name__"):
                return obj.__name__
            if hasattr(obj, "name"):
                return obj.name
            return f"{default_prefix}_{id(obj)}"
        except Exception:
            return f"{default_prefix}_{id(obj)}"

    def safe_get_class_name(self, obj: Any) -> str:
        """Safely get the class name of an object."""
        try:
            if hasattr(obj, "__name__"):
                return obj.__name__
            return type(obj).__name__
        except Exception:
            return "UnknownClass"

    def detect_env_vars(self, source_code: str) -> list[str]:
        """Detect environment variables in source code."""
        if not source_code:
            return []

        patterns = [
            r'os\.environ\.get\(["\']([A-Za-z0-9_]+)["\']',
            r'os\.getenv\(["\']([A-Za-z0-9_]+)["\']',
            r'os\.environ\[["\']([A-Za-z0-9_]+)["\']',
            r'getenv\(["\']([A-Za-z0-9_]+)["\']',
            r'["\']([A-Z][A-Z0-9_]+_(?:KEY|TOKEN|SECRET|PASSWORD|ID|URL|URI|ENDPOINT|CREDENTIALS))["\']',
        ]

        env_vars = set()
        for pattern in patterns:
            matches = re.findall(pattern, source_code)
            env_vars.update(matches)

        return sorted(env_vars)

    def get_source_code(self, obj: Any) -> str:
        """Extract source code from object."""
        try:
            return inspect.getsource(obj)
        except (TypeError, OSError):
            if hasattr(obj, "__wrapped__"):
                try:
                    return inspect.getsource(obj.__wrapped__)
                except (TypeError, OSError):
                    pass
            return ""

    def extract_schema(self, obj: Any) -> dict[str, Any]:
        """Extract schema information from object."""
        try:
            if hasattr(obj, "args_schema") and obj.args_schema:
                # LangChain tool schema
                if hasattr(obj.args_schema, "model_json_schema"):
                    return obj.args_schema.model_json_schema()
                if hasattr(obj.args_schema, "schema"):
                    return obj.args_schema.schema()

            # Try to create schema from __init__ signature
            if hasattr(obj, "__init__"):
                sig = inspect.signature(obj.__init__)
                fields = {}
                for name, param in sig.parameters.items():
                    if name == "self":
                        continue
                    param_type = (
                        param.annotation
                        if param.annotation != inspect._empty
                        else "Any"
                    )
                    default = param.default if param.default != inspect._empty else None
                    fields[name] = {
                        "type": str(param_type),
                        "default": str(default) if default is not None else None,
                    }
                return {"properties": fields}
        except Exception as e:
            logger.warning(f"Error extracting schema: {e}")

        return {}

    def create_pydantic_model(
        self, cls: type, force_serializable: bool = False
    ) -> type[BaseModel]:
        """Create a Pydantic model from a class signature."""
        try:
            sig = inspect.signature(cls.__init__)
            fields = {}

            for name, param in sig.parameters.items():
                if name == "self":
                    continue

                param_type = (
                    param.annotation if param.annotation != inspect._empty else Any
                )
                default = param.default if param.default != inspect._empty else ...

                # Handle complex types that might cause issues
                try:
                    if hasattr(param_type, "__origin__"):
                        # For generic types like Dict[str, Tuple[Type, Any]], simplify to basic types
                        type_str = str(param_type)
                        if "Dict" in type_str:
                            param_type = dict
                        elif "List" in type_str:
                            param_type = list
                        elif "Optional" in type_str:
                            param_type = Any
                except Exception:
                    # If type inspection fails, use Any as fallback
                    param_type = Any

                fields[name] = (param_type, default)

            config = (
                ConfigDict(arbitrary_types_allowed=True) if force_serializable else None
            )

            return create_model(
                f"{cls.__name__}Args",
                __config__=config,
                **fields,
            )
        except Exception as e:
            logger.warning(f"Error creating Pydantic model for {cls.__name__}: {e}")
            # Return a minimal model with just basic fields as fallback
            try:
                return create_model(
                    f"{cls.__name__}Args",
                    __config__=ConfigDict(arbitrary_types_allowed=True),
                    args=(Any, None),
                    kwds=(Any, None),
                )
            except Exception as fallback_error:
                logger.warning(f"Fallback model creation also failed: {fallback_error}")
                return create_model(f"{cls.__name__}Args")
