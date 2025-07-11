"""Analyzer for Haive engine components."""

import inspect
import logging
from datetime import datetime
from typing import Any

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo

logger = logging.getLogger(__name__)


class EngineAnalyzer(ComponentAnalyzer):
    """Analyzer for Haive engines."""

    def can_analyze(self, obj: Any) -> bool:
        return (
            inspect.isclass(obj)
            and hasattr(obj, "engine_type")
            and hasattr(obj, "create_runnable")
        )

    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        metadata = {}
        if hasattr(obj, "engine_type"):
            metadata["engine_type"] = str(obj.engine_type)

        info = ComponentInfo(
            name=self.safe_get_name(obj, "Engine"),
            component_type="engine",
            module_path=module_path,
            class_name=self.safe_get_class_name(obj),
            description=inspect.getdoc(obj) or "",
            source_code=self.get_source_code(obj),
            env_vars=self.detect_env_vars(self.get_source_code(obj)),
            schema=self.extract_schema(obj),
            metadata=metadata,
            timestamp=datetime.now().isoformat(),
            engine_config={
                "class": self.safe_get_class_name(obj),
                "module": module_path,
            },
        )

        return info
