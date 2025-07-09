"""
Analyzers for retriever and vector store components.
"""

import importlib
import inspect
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo

logger = logging.getLogger(__name__)

# Check for LangChain availability
try:
    from langchain_core.tools import StructuredTool
    from pydantic import BaseModel, Field

    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available. Tool features will be limited.")
    LANGCHAIN_AVAILABLE = False


class RetrieverAnalyzer(ComponentAnalyzer):
    """Analyzer for retrievers."""

    def can_analyze(self, obj: Any) -> bool:
        # More robust check
        try:
            if not inspect.isclass(obj):
                return False

            # Check for Retriever in name
            if hasattr(obj, "__name__") and "Retriever" in obj.__name__:
                return True

            # Check for retriever-like methods
            if hasattr(obj, "get_relevant_documents") or hasattr(obj, "retrieve"):
                return True

            return False
        except Exception as e:
            logger.debug(f"Error checking if can analyze: {e}")
            return False

    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        info = ComponentInfo(
            name=self.safe_get_name(obj, "Retriever"),
            component_type="retriever",
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

        info.engine_config = self.create_engine_config(info)
        return info

    def create_tool(self, component_info: ComponentInfo) -> Optional[Any]:
        """Convert retriever to a StructuredTool."""
        if not LANGCHAIN_AVAILABLE:
            return None

        try:
            # Import the class
            module = importlib.import_module(component_info.module_path)
            retriever_class = getattr(module, component_info.class_name)

            # Create args model
            args_model = self.create_pydantic_model(
                retriever_class, force_serializable=True
            )

            # Add query fields
            class RetrieverArgs(args_model):
                query: str = Field(description="Query to search for")
                k: Optional[int] = Field(
                    default=4, description="Number of documents to retrieve"
                )

            def retriever_function(**kwargs):
                """Retrieve documents."""
                try:
                    query = kwargs.pop("query")
                    k = kwargs.pop("k", 4)

                    # Filter kwargs
                    filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
                    instance = retriever_class(**filtered_kwargs)

                    # Retrieve documents
                    if hasattr(instance, "get_relevant_documents"):
                        documents = instance.get_relevant_documents(query)
                    elif hasattr(instance, "retrieve"):
                        documents = instance.retrieve(query)
                    else:
                        return {
                            "error": "Retriever doesn't have expected methods",
                            "success": False,
                        }

                    documents = documents[:k]

                    return {
                        "num_documents": len(documents),
                        "query": query,
                        "documents": [
                            {
                                "content": doc.page_content,
                                "metadata": doc.metadata,
                                "score": getattr(doc, "score", None),
                            }
                            for doc in documents
                        ],
                    }
                except Exception as e:
                    return {"error": str(e), "success": False}

            # Create safe tool name
            tool_name = f"retrieve_{component_info.name.lower().replace(' ', '_').replace('-', '_')}"
            tool_name = "".join(
                c if c.isalnum() or c == "_" else "_" for c in tool_name
            )

            return StructuredTool.from_function(
                func=retriever_function,
                name=tool_name,
                description=f"Retrieve documents using {component_info.class_name}",
                args_schema=RetrieverArgs,
            )

        except Exception as e:
            logger.warning(f"Error creating tool: {e}")
            return None

    def create_engine_config(
        self, component_info: ComponentInfo
    ) -> Optional[Dict[str, Any]]:
        """Create a Haive RetrieverEngine config."""
        try:
            return {
                "engine_type": "retriever",
                "retriever_class": component_info.class_name,
                "module_path": component_info.module_path,
                "description": component_info.description,
                "env_vars": component_info.env_vars,
                "schema": component_info.schema,
            }
        except Exception as e:
            logger.warning(f"Error creating engine config: {e}")
            return None


class VectorStoreAnalyzer(ComponentAnalyzer):
    """Analyzer for vector stores."""

    def can_analyze(self, obj: Any) -> bool:
        try:
            if not inspect.isclass(obj):
                return False

            # Check name
            if hasattr(obj, "__name__") and "VectorStore" in obj.__name__:
                return True

            # Check methods
            if hasattr(obj, "similarity_search") or hasattr(obj, "add_documents"):
                return True

            return False
        except Exception as e:
            logger.debug(f"Error checking if can analyze: {e}")
            return False

    def analyze(self, obj: Any, module_path: str) -> ComponentInfo:
        info = ComponentInfo(
            name=self.safe_get_name(obj, "VectorStore"),
            component_type="vector_store",
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

        info.engine_config = self.create_engine_config(info)
        return info

    def create_tool(self, component_info: ComponentInfo) -> Optional[Any]:
        """Convert vector store to a StructuredTool."""
        if not LANGCHAIN_AVAILABLE:
            return None

        try:

            class VectorStoreArgs(BaseModel):
                query: str = Field(description="Query to search for")
                k: Optional[int] = Field(
                    default=4, description="Number of documents to retrieve"
                )
                filter: Optional[Dict[str, Any]] = Field(
                    default=None, description="Metadata filter"
                )

            def vectorstore_search(**kwargs):
                """Search vector store placeholder."""
                return {
                    "message": f"Vector store {component_info.class_name} search placeholder",
                    "query": kwargs.get("query"),
                    "k": kwargs.get("k", 4),
                    "note": "This is a placeholder. Actual implementation requires instantiated vector store.",
                }

            # Create safe tool name
            tool_name = f"search_{component_info.name.lower().replace(' ', '_').replace('-', '_')}"
            tool_name = "".join(
                c if c.isalnum() or c == "_" else "_" for c in tool_name
            )

            return StructuredTool.from_function(
                func=vectorstore_search,
                name=tool_name,
                description=f"Search documents using {component_info.class_name}",
                args_schema=VectorStoreArgs,
            )

        except Exception as e:
            logger.warning(f"Error creating tool: {e}")
            return None

    def create_engine_config(
        self, component_info: ComponentInfo
    ) -> Optional[Dict[str, Any]]:
        """Create a Haive VectorStoreEngine config."""
        try:
            return {
                "engine_type": "vector_store",
                "vector_store_class": component_info.class_name,
                "module_path": component_info.module_path,
                "description": component_info.description,
                "env_vars": component_info.env_vars,
                "schema": component_info.schema,
            }
        except Exception as e:
            logger.warning(f"Error creating engine config: {e}")
            return None
