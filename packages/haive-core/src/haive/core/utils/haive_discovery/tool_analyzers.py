"""
Analyzers for tool-related components.
"""

import importlib
import inspect
import logging
from datetime import datetime
from typing import Any, Optional

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo

logger = logging.getLogger(__name__)

# Check for LangChain availability
try:
    from langchain_core.tools import BaseTool, StructuredTool
    from pydantic import BaseModel, Field, create_model

    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available. Tool features will be limited.")
    LANGCHAIN_AVAILABLE = False


class ToolAnalyzer(ComponentAnalyzer):
    """Analyzer for LangChain tools."""

    def can_analyze(self, obj: Any) -> bool:
        if not LANGCHAIN_AVAILABLE:
            return False
        try:
            return isinstance(obj, BaseTool)
        except:
            return False

    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        return ComponentInfo(
            name=self.safe_get_name(obj, "Tool"),
            component_type="tool",
            module_path=module_path,
            class_name=self.safe_get_class_name(obj),
            description=getattr(obj, "description", "") or "",
            source_code=self.get_source_code(obj),
            env_vars=self.detect_env_vars(self.get_source_code(obj)),
            schema=self.extract_schema(obj),
            metadata=getattr(obj, "metadata", {}) or {},
            timestamp=datetime.now().isoformat(),
            tool_instance=obj,
        )


class DocumentLoaderAnalyzer(ComponentAnalyzer):
    """Analyzer for document loaders."""

    def can_analyze(self, obj: Any) -> bool:
        return (
            inspect.isclass(obj)
            and hasattr(obj, "load")
            and callable(getattr(obj, "load", None))
        )

    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        info = ComponentInfo(
            name=self.safe_get_name(obj, "DocumentLoader"),
            component_type="document_loader",
            module_path=module_path,
            class_name=self.safe_get_class_name(obj),
            description=inspect.getdoc(obj) or "",
            source_code=self.get_source_code(obj),
            env_vars=self.detect_env_vars(self.get_source_code(obj)),
            schema=self.extract_schema(obj),
            metadata={},
            timestamp=datetime.now().isoformat(),
        )

        if LANGCHAIN_AVAILABLE:
            info.tool_instance = self.create_tool(info)

        return info

    def create_tool(self, component_info: ComponentInfo) -> Optional[Any]:
        """Convert document loader to a StructuredTool."""
        if not LANGCHAIN_AVAILABLE:
            return None

        try:
            # Import the loader class
            try:
                module = importlib.import_module(component_info.module_path)
                loader_class = getattr(module, component_info.class_name)
            except (ImportError, AttributeError, SystemExit) as e:
                logger.debug(f"Could not import {component_info.class_name}: {e}")
                return None

            # Create args model
            try:
                args_model = self.create_pydantic_model(
                    loader_class, force_serializable=True
                )
            except Exception as e:
                logger.debug(f"Could not create args model: {e}")
                args_model = create_model(f"{component_info.class_name}Args")

            def loader_function(**kwargs):
                """Load documents using the loader."""
                try:
                    # Filter kwargs for valid parameters
                    filtered_kwargs = {}
                    if hasattr(loader_class, "__init__"):
                        try:
                            sig = inspect.signature(loader_class.__init__)
                            valid_params = set(sig.parameters.keys()) - {"self"}

                            for k, v in kwargs.items():
                                if k in valid_params and v is not None:
                                    filtered_kwargs[k] = v
                        except:
                            pass

                    # Create instance
                    try:
                        instance = loader_class(**filtered_kwargs)
                    except Exception as e:
                        try:
                            instance = loader_class()
                        except Exception as e2:
                            return {
                                "error": f"Could not create instance: {e}",
                                "fallback_error": str(e2),
                                "success": False,
                            }

                    # Load documents
                    try:
                        documents = instance.load()

                        return {
                            "success": True,
                            "num_documents": len(documents),
                            "total_chars": sum(
                                len(doc.page_content) for doc in documents
                            ),
                            "sample_content": (
                                documents[0].page_content[:200] + "..."
                                if documents
                                else ""
                            ),
                            "documents": [
                                {
                                    "content": doc.page_content[:500],
                                    "metadata": doc.metadata,
                                }
                                for doc in documents[:3]
                            ],
                        }
                    except Exception as e:
                        return {
                            "error": f"Could not load documents: {e}",
                            "success": False,
                        }

                except Exception as e:
                    return {"error": f"Unexpected error: {e}", "success": False}

            # Create safe tool name
            tool_name = f"load_documents_{component_info.name.lower().replace(' ', '_').replace('-', '_')}"
            tool_name = "".join(
                c if c.isalnum() or c == "_" else "_" for c in tool_name
            )

            # Create the tool
            return StructuredTool.from_function(
                func=loader_function,
                name=tool_name,
                description=f"Load documents using {component_info.class_name}: {component_info.description[:100]}",
                args_schema=args_model,
            )

        except Exception as e:
            logger.debug(f"Error creating tool for {component_info.name}: {e}")
            return None
