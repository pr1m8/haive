"""
Component information data model with serialization support.
"""

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ComponentInfo:
    """Standardized component information with serialization support."""

    name: str
    component_type: str
    module_path: str
    class_name: str
    description: str
    source_code: str
    env_vars: List[str]
    schema: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: str

    # Tool and engine creation results
    tool_instance: Optional[Any] = None
    engine_config: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, handling non-serializable fields."""
        data = {
            "name": self.name,
            "component_type": self.component_type,
            "module_path": self.module_path,
            "class_name": self.class_name,
            "description": self.description,
            "source_code": self.source_code,
            "env_vars": self.env_vars,
            "timestamp": self.timestamp,
        }

        # Handle schema serialization
        try:
            data["schema"] = self._make_json_serializable(self.schema)
        except Exception as e:
            logger.debug(f"Could not serialize schema for {self.name}: {e}")
            data["schema"] = {"error": f"Schema not serializable: {str(e)}"}

        # Handle metadata serialization
        try:
            data["metadata"] = self._make_json_serializable(self.metadata)
        except Exception as e:
            logger.debug(f"Could not serialize metadata for {self.name}: {e}")
            data["metadata"] = {"error": f"Metadata not serializable: {str(e)}"}

        # Add tool info if available
        if self.tool_instance:
            data["has_tool"] = True
            data["tool_name"] = getattr(self.tool_instance, "name", "unknown")
            data["tool_description"] = getattr(self.tool_instance, "description", "")
        else:
            data["has_tool"] = False

        # Add engine config if available
        if self.engine_config:
            try:
                data["engine_config"] = self._make_json_serializable(self.engine_config)
            except Exception as e:
                logger.debug(f"Could not serialize engine config for {self.name}: {e}")
                data["engine_config"] = {
                    "error": f"Engine config not serializable: {str(e)}"
                }

        return data

    def _make_json_serializable(
        self, obj: Any, max_depth: int = 5, current_depth: int = 0
    ) -> Any:
        """Recursively make an object JSON serializable."""
        if current_depth > max_depth:
            return f"<Max depth {max_depth} reached>"

        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj

        if isinstance(obj, (list, tuple)):
            return [
                self._make_json_serializable(item, max_depth, current_depth + 1)
                for item in obj
            ]

        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                try:
                    str_key = str(key)
                    result[str_key] = self._make_json_serializable(
                        value, max_depth, current_depth + 1
                    )
                except Exception as e:
                    result[str_key] = f"<Error serializing value: {str(e)}>"
            return result

        # Handle objects with __dict__
        if hasattr(obj, "__dict__"):
            try:
                return self._make_json_serializable(
                    {k: v for k, v in obj.__dict__.items() if not k.startswith("_")},
                    max_depth,
                    current_depth + 1,
                )
            except Exception:
                pass

        # Handle Pydantic models
        if hasattr(obj, "model_dump"):
            try:
                return obj.model_dump()
            except Exception:
                pass

        if hasattr(obj, "dict"):
            try:
                return obj.dict()
            except Exception:
                pass

        # Last resort - convert to string
        try:
            return str(obj)
        except Exception:
            return f"<{type(obj).__name__} object>"

    def to_document_content(self) -> str:
        """Convert to RAG-friendly document content."""
        content = []
        content.append(f"# {self.name}")
        content.append(f"**Type:** {self.component_type}")
        content.append(f"**Module:** {self.module_path}")
        content.append(f"**Class:** {self.class_name}")
        content.append("")

        if self.description:
            content.append("## Description")
            content.append(self.description)
            content.append("")

        if self.env_vars:
            content.append("## Environment Variables")
            for var in self.env_vars:
                content.append(f"- `{var}`")
            content.append("")

        if self.schema and not (
            isinstance(self.schema, dict) and self.schema.get("error")
        ):
            content.append("## Schema")
            content.append("```json")
            try:
                content.append(json.dumps(self.schema, indent=2))
            except:
                content.append(str(self.schema))
            content.append("```")
            content.append("")

        if self.tool_instance:
            content.append("## Usage as Tool")
            content.append(
                f"**Tool Name:** `{getattr(self.tool_instance, 'name', 'unknown')}`"
            )
            content.append(
                f"**Description:** {getattr(self.tool_instance, 'description', '')}"
            )
            content.append("")

        if self.engine_config:
            content.append("## Engine Configuration")
            content.append("This component can be used as a Haive engine:")
            content.append("```python")
            content.append("# Example engine usage")
            content.append(f"engine = {self.class_name}Engine(name='{self.name}')")
            content.append("```")
            content.append("")

        if self.metadata and not (
            isinstance(self.metadata, dict) and self.metadata.get("error")
        ):
            content.append("## Metadata")
            content.append("```json")
            try:
                content.append(json.dumps(self.metadata, indent=2))
            except:
                content.append(str(self.metadata))
            content.append("```")
            content.append("")

        content.append("## Source Code")
        content.append("```python")
        content.append(self.source_code)
        content.append("```")

        return "\n".join(content)
