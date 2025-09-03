"""Example of using lazy_loader for Sphinx-compatible lazy imports.

This shows how to implement lazy loading for haive.core.models
"""
# ===== Option 1: Using lazy_loader (Recommended) =====
# haive/core/models/__init__.py
"""Models module with lazy loading for performance."""

from __future__ import annotations
import importlib


# Define submodules to lazy load

submodules = ['llm', 'embeddings', 'retriever', 'vectorstore']

# Define specific attributes from submodules
submod_attrs = {
    'llm': ['LLMConfig', 'LLMFactory', 'LLMProvider', 'create_llm'],
    'embeddings': ['BaseEmbeddingConfig', 'EmbeddingProvider', 'OpenAIEmbeddingConfig'],
    'retriever': ['RetrieverConfig', 'RetrieverType'],
    'vectorstore': ['VectorStoreConfig', 'VectorStoreProvider'],
}

# Attach lazy loading - this creates __getattr__, __dir__, and __all__
__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=submodules,
    submod_attrs=submod_attrs,
)

# Add any eagerly loaded items

# Update __all__ to include eager imports
__all__ += ['MetadataMixin', 'ModelMetadata']

# ===== Option 1B: With Type Stubs (Better for IDEs) =====

# haive/core/models/__init__.py

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, '__init__.pyi')

# haive/core/models/__init__.pyi (type stub file)
"""Type stubs for models module."""

# Submodules

# Specific imports

__all__ = [
    # Submodules
    'llm',
    'embeddings',
    'retriever',
    'vectorstore',
    # Classes
    'LLMConfig',
    'LLMFactory',
    'LLMProvider',
    'create_llm',
    'BaseEmbeddingConfig',
    'EmbeddingProvider',
    'OpenAIEmbeddingConfig',
    'ModelMetadata',
    'MetadataMixin',
]

# ===== Option 2: PEP 562 Pattern (Built-in, no deps) =====

# haive/core/models/__init__.py
"""Models module with PEP 562 lazy loading."""

# For type checking, import everything
if TYPE_CHECKING:
    from scripts.maintenance import embeddings, llm, retriever, vectorstore
    from scripts.maintenance.embeddings import BaseEmbeddingConfig, EmbeddingProvider
    from scripts.maintenance.llm import LLMConfig, LLMFactory, LLMProvider
    from scripts.maintenance.metadata import ModelMetadata
    from scripts.maintenance.metadata_mixin import MetadataMixin

# Lazy imports mapping
_LAZY_IMPORTS = {
    # Submodules
    'llm': 'haive.core.models.llm',
    'embeddings': 'haive.core.models.embeddings',
    'retriever': 'haive.core.models.retriever',
    'vectorstore': 'haive.core.models.vectorstore',
    # Specific classes (module_path, attribute)
    'LLMConfig': ('haive.core.models.llm', 'LLMConfig'),
    'LLMFactory': ('haive.core.models.llm', 'LLMFactory'),
    'LLMProvider': ('haive.core.models.llm', 'LLMProvider'),
    'create_llm': ('haive.core.models.llm', 'create_llm'),
    'BaseEmbeddingConfig': ('haive.core.models.embeddings', 'BaseEmbeddingConfig'),
    'EmbeddingProvider': ('haive.core.models.embeddings', 'EmbeddingProvider'),
    'OpenAIEmbeddingConfig': ('haive.core.models.embeddings', 'OpenAIEmbeddingConfig'),
    'RetrieverConfig': ('haive.core.models.retriever', 'RetrieverConfig'),
    'RetrieverType': ('haive.core.models.retriever', 'RetrieverType'),
    'VectorStoreConfig': ('haive.core.models.vectorstore', 'VectorStoreConfig'),
    'VectorStoreProvider': ('haive.core.models.vectorstore', 'VectorStoreProvider'),
}

# Eager imports (lightweight)


def __getattr__(name: str):
    """PEP 562 lazy loading."""
    if name in _LAZY_IMPORTS:
        import_info = _LAZY_IMPORTS[name]

        if isinstance(import_info, str):
            # It's a module
            module = importlib.import_module(import_info)
            globals()[name] = module
            return module
        # It's an attribute from a module
        module_name, attr_name = import_info
        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        globals()[name] = attr
        return attr

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__():
    """List available attributes."""
    return list(__all__)


__all__ = [
    # Submodules
    'llm',
    'embeddings',
    'retriever',
    'vectorstore',
    # Classes from submodules (lazy)
    'LLMConfig',
    'LLMFactory',
    'LLMProvider',
    'create_llm',
    'BaseEmbeddingConfig',
    'EmbeddingProvider',
    'OpenAIEmbeddingConfig',
    'RetrieverConfig',
    'RetrieverType',
    'VectorStoreConfig',
    'VectorStoreProvider',
    # Eager imports
    'ModelMetadata',
    'MetadataMixin',
]

# ===== Option 3: Hybrid Approach (Safest for Sphinx) =====

# haive/core/models/__init__.py
"""Models module with conditional lazy loading."""

# Check if we're building docs
BUILDING_DOCS = os.environ.get('READTHEDOCS') == 'True' or 'sphinx' in sys.modules

if BUILDING_DOCS:
    # For documentation, import everything normally
    from scripts.maintenance import embeddings, llm, retriever, vectorstore
    from scripts.maintenance.embeddings import (
        BaseEmbeddingConfig,
        EmbeddingProvider,
        OpenAIEmbeddingConfig,
    )
    from scripts.maintenance.llm import LLMConfig, LLMFactory, LLMProvider, create_llm
    from scripts.maintenance.metadata import ModelMetadata
    from scripts.maintenance.metadata_mixin import MetadataMixin
    from scripts.maintenance.retriever import RetrieverConfig, RetrieverType
    from scripts.maintenance.vectorstore import VectorStoreConfig, VectorStoreProvider
else:
    # For runtime, use lazy loading
    import lazy_loader as lazy

    __getattr__, __dir__, __all__ = lazy.attach(
        __name__,
        submodules=['llm', 'embeddings', 'retriever', 'vectorstore'],
        submod_attrs={
            'llm': ['LLMConfig', 'LLMFactory', 'LLMProvider', 'create_llm'],
            'embeddings': [
                'BaseEmbeddingConfig',
                'EmbeddingProvider',
                'OpenAIEmbeddingConfig',
            ],
            'retriever': ['RetrieverConfig', 'RetrieverType'],
            'vectorstore': ['VectorStoreConfig', 'VectorStoreProvider'],
        },
    )

    # Eager imports
    from scripts.maintenance.metadata import ModelMetadata
    from scripts.maintenance.metadata_mixin import MetadataMixin

    __all__ += ['MetadataMixin', 'ModelMetadata']

# ===== Testing and Development =====

# To disable lazy loading during development:
# export EAGER_IMPORT=1

# To test that lazy loading works:
"""
import haive.core.models
# At this point, submodules are NOT loaded

print('llm' in sys.modules)  # False
models.llm  # Now it loads
print('haive.core.models.llm' in sys.modules)  # True
"""
