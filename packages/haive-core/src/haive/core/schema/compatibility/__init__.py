"""
Haive Schema Compatibility Module

A comprehensive type checking, compatibility analysis, and schema transformation system.
"""

from haive.core.schema.compatibility.analyzer import (
    TypeAnalyzer,
    analyze_type,
    get_type_info,
)
from haive.core.schema.compatibility.compatibility import (
    CompatibilityChecker,
    CompatibilityLevel,
    check_compatibility,
)
from haive.core.schema.compatibility.converters import (
    ConversionContext,
    ConversionQuality,
    ConverterRegistry,
    TypeConverter,
    register_converter,
)
from haive.core.schema.compatibility.field_mapping import (
    FieldMapper,
    FieldMapping,
    create_mapping,
)
from haive.core.schema.compatibility.langchain_converters import (
    DocumentConverter,
    MessageConverter,
    PromptConverter,
    register_langchain_converters,
)
from haive.core.schema.compatibility.mergers import (
    MergeStrategy,
    SchemaMerger,
    merge_schemas,
)
from haive.core.schema.compatibility.reports import (
    CompatibilityReport,
    generate_report,
)
from haive.core.schema.compatibility.types import (
    ConversionPath,
    FieldInfo,
    SchemaInfo,
    TypeInfo,
)
from haive.core.schema.compatibility.validators import (
    FieldValidator,
    ModelValidator,
    ValidationContext,
    create_validator,
)

# Initialize default converters on import
register_langchain_converters()

__all__ = [
    # Core types
    "CompatibilityLevel",
    "ConversionQuality",
    "MergeStrategy",
    "TypeInfo",
    "FieldInfo",
    "SchemaInfo",
    "ConversionPath",
    # Main classes
    "TypeAnalyzer",
    "CompatibilityChecker",
    "ConverterRegistry",
    "TypeConverter",
    "FieldMapper",
    "FieldMapping",
    "SchemaMerger",
    "CompatibilityReport",
    "FieldValidator",
    "ModelValidator",
    "ValidationContext",
    "ConversionContext",
    # Converter classes
    "MessageConverter",
    "DocumentConverter",
    "PromptConverter",
    # Convenience functions
    "analyze_type",
    "get_type_info",
    "check_compatibility",
    "register_converter",
    "create_mapping",
    "merge_schemas",
    "generate_report",
    "create_validator",
    "register_langchain_converters",
]

# Module version
__version__ = "0.1.0"
