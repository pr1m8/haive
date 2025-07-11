"""
Basic test structure for the schema compatibility module.

This provides a template for comprehensive testing of all module components.
"""

from typing import List, Optional

import pytest
from pydantic import BaseModel, Field

from haive.core.schema.compatibility import (
    CompatibilityChecker,
    CompatibilityLevel,
    ConverterRegistry,
    FieldMapper,
    SchemaMerger,
    TypeAnalyzer,
    check_compatibility,
    create_mapping,
    generate_report,
)
from haive.core.schema.compatibility.types import ConversionQuality


class TestTypeAnalyzer:
    """Test type analysis functionality."""

    def test_basic_type_analysis(self):
        """Test analysis of basic types."""
        analyzer = TypeAnalyzer()

        # Test simple type
        info = analyzer.get_type_info(str)
        assert info.type_hint == str
        assert not info.is_generic
        assert not info.is_optional

    def test_generic_type_analysis(self):
        """Test analysis of generic types."""
        analyzer = TypeAnalyzer()

        # Test List[str]
        info = analyzer.get_type_info(List[str])
        assert info.is_generic
        assert info.origin == list
        assert str in info.args

    def test_optional_type_detection(self):
        """Test Optional type detection."""
        analyzer = TypeAnalyzer()

        # Test Optional[int]
        info = analyzer.get_type_info(Optional[int])
        assert info.is_optional
        assert info.is_union

    def test_schema_analysis(self):
        """Test Pydantic schema analysis."""

        class TestSchema(BaseModel):
            name: str
            age: int = 0
            tags: List[str] = Field(default_factory=list)

        analyzer = TypeAnalyzer()
        schema_info = analyzer.analyze_schema(TestSchema)

        assert schema_info.name == "TestSchema"
        assert len(schema_info.fields) == 3
        assert "name" in schema_info.fields
        assert schema_info.fields["name"].is_required
        assert not schema_info.fields["age"].is_required


class TestCompatibilityChecker:
    """Test compatibility checking."""

    def test_exact_compatibility(self):
        """Test exact type compatibility."""

        class Schema1(BaseModel):
            field: str

        class Schema2(BaseModel):
            field: str

        result = check_compatibility(Schema1, Schema2)
        assert result.is_compatible
        assert result.level == CompatibilityLevel.EXACT

    def test_missing_required_field(self):
        """Test missing required field detection."""

        class Source(BaseModel):
            field1: str

        class Target(BaseModel):
            field1: str
            field2: str  # Required!

        result = check_compatibility(Source, Target)
        assert not result.is_compatible
        assert "field2" in result.missing_required_fields

    def test_type_mismatch(self):
        """Test type mismatch detection."""

        class Source(BaseModel):
            field: str

        class Target(BaseModel):
            field: int

        result = check_compatibility(Source, Target)
        assert "field" in result.field_results
        assert not result.field_results["field"].is_compatible

    def test_optional_field_compatibility(self):
        """Test optional field handling."""

        class Source(BaseModel):
            field: str

        class Target(BaseModel):
            field: Optional[str] = None

        result = check_compatibility(Source, Target)
        assert result.is_compatible


class TestConverterRegistry:
    """Test type conversion system."""

    def test_builtin_converters(self):
        """Test built-in type converters."""
        registry = ConverterRegistry()

        # Test int to float
        result = registry.convert(42, int, float)
        assert result == 42.0
        assert isinstance(result, float)

    def test_conversion_path_finding(self):
        """Test multi-step conversion paths."""
        registry = ConverterRegistry()

        # Should find: int -> float -> str
        path = registry.find_conversion_path(int, str)
        assert path is not None
        assert path.step_count > 0

    def test_custom_converter_registration(self):
        """Test registering custom converters."""
        from haive.core.schema.compatibility.converters import FunctionConverter

        registry = ConverterRegistry()

        # Register custom converter
        converter = FunctionConverter(
            source_type=dict,
            target_type=str,
            converter_func=lambda d, ctx: str(d),
            quality=ConversionQuality.SAFE,
            name="dict_to_str_custom",
        )

        registry.register(converter)

        # Test conversion
        result = registry.convert({"key": "value"}, dict, str)
        assert isinstance(result, str)


class TestFieldMapper:
    """Test field mapping functionality."""

    def test_simple_mapping(self):
        """Test basic field mapping."""
        mapper = FieldMapper()
        mapper.add_mapping("source", "target")

        result = mapper.map_data({"source": "value"})
        assert result == {"target": "value"}

    def test_nested_path_mapping(self):
        """Test nested path extraction."""
        mapper = FieldMapper()
        mapper.add_mapping("user.name", "username")

        result = mapper.map_data({"user": {"name": "John", "age": 30}})
        assert result == {"username": "John"}

    def test_transformation_mapping(self):
        """Test field transformation."""
        mapper = FieldMapper()
        mapper.add_mapping(
            "price", "formatted_price", transformer=lambda x: f"${x:.2f}"
        )

        result = mapper.map_data({"price": 10.5})
        assert result == {"formatted_price": "$10.50"}

    def test_computed_field(self):
        """Test computed field generation."""
        mapper = FieldMapper()
        mapper.add_computed_field("timestamp", generator=lambda: "2024-01-01")

        result = mapper.map_data({})
        assert result == {"timestamp": "2024-01-01"}

    def test_aggregate_field(self):
        """Test field aggregation."""
        mapper = FieldMapper()
        mapper.add_aggregate_field(
            sources=["first", "last"],
            target="full_name",
            aggregator=lambda vals: " ".join(vals),
        )

        result = mapper.map_data({"first": "John", "last": "Doe"})
        assert result == {"full_name": "John Doe"}


class TestSchemaMerger:
    """Test schema merging functionality."""

    def test_union_merge(self):
        """Test union merge strategy."""

        class Schema1(BaseModel):
            field1: str
            common: int

        class Schema2(BaseModel):
            field2: str
            common: int

        merger = SchemaMerger(strategy="union")
        Merged = merger.merge_schemas([Schema1, Schema2])

        fields = set(Merged.model_fields.keys())
        assert fields == {"field1", "field2", "common"}

    def test_intersection_merge(self):
        """Test intersection merge strategy."""

        class Schema1(BaseModel):
            field1: str
            common: int

        class Schema2(BaseModel):
            field2: str
            common: int

        merger = SchemaMerger(strategy="intersection")
        Merged = merger.merge_schemas([Schema1, Schema2])

        fields = set(Merged.model_fields.keys())
        assert fields == {"common"}

    def test_conflict_resolution(self):
        """Test handling of field conflicts."""

        class Schema1(BaseModel):
            field: str

        class Schema2(BaseModel):
            field: int  # Different type!

        merger = SchemaMerger(strategy="union")
        # Should handle conflict according to strategy
        Merged = merger.merge_schemas([Schema1, Schema2])
        assert "field" in Merged.model_fields


class TestValidators:
    """Test validation framework."""

    def test_field_validator(self):
        """Test field validation."""
        from haive.core.schema.compatibility.validators import (
            FieldValidator,
            ValidationContext,
        )

        validator = FieldValidator("age")
        validator.add_validator(lambda x: x >= 0, "Age must be non-negative")

        context = ValidationContext()

        # Valid case
        result = validator.validate(25, context)
        assert result.is_valid

        # Invalid case
        result = validator.validate(-5, context)
        assert not result.is_valid
        assert len(result.errors) == 1

    def test_model_validator(self):
        """Test model validation."""
        from haive.core.schema.compatibility.validators import (
            FieldValidator,
            ModelValidator,
            ValidationContext,
        )

        validator = ModelValidator()

        # Add field validator
        age_validator = FieldValidator("age")
        age_validator.add_validator(lambda x: x >= 18, "Must be 18+")
        validator.add_field_validator("age", age_validator)

        # Test validation
        context = ValidationContext()
        result = validator.validate({"age": 25}, context)
        assert result.is_valid

        result = validator.validate({"age": 16}, context)
        assert not result.is_valid


class TestCompatibilityReports:
    """Test report generation."""

    def test_report_generation(self):
        """Test basic report generation."""

        class Source(BaseModel):
            field1: str

        class Target(BaseModel):
            field1: str
            field2: int

        report = generate_report(Source, Target)

        assert not report.overall_compatible
        assert len(report.critical_issues) > 0
        assert "field2" in str(report.critical_issues[0])

    def test_report_formats(self):
        """Test different report formats."""

        class Schema(BaseModel):
            field: str

        report = generate_report(Schema, Schema)

        # Test markdown format
        markdown = report.to_markdown()
        assert "# Schema Compatibility Report" in markdown

        # Test JSON format
        json_str = report.to_json()
        assert '"overall_compatible": true' in json_str


class TestLangChainConverters:
    """Test LangChain-specific converters."""

    @pytest.mark.skipif(
        not hasattr(pytest, "langchain_installed"), reason="LangChain not installed"
    )
    def test_message_conversion(self):
        """Test message type conversions."""
        from langchain_core.messages import AIMessage, HumanMessage

        from haive.core.schema.compatibility.langchain_converters import (
            MessageConverter,
        )

        converter = MessageConverter()
        context = ConversionContext(source_type="HumanMessage", target_type="AIMessage")

        human_msg = HumanMessage(content="Hello")
        ai_msg = converter.convert(human_msg, context)

        assert isinstance(ai_msg, AIMessage)
        assert ai_msg.content == "Hello"


class TestUtils:
    """Test utility functions."""

    def test_similarity_calculation(self):
        """Test string similarity calculation."""
        from haive.core.schema.compatibility.utils import calculate_similarity

        score = calculate_similarity("email", "Email")
        assert score == 1.0  # Case insensitive

        score = calculate_similarity("username", "user_name")
        assert score > 0.5  # Similar

    def test_nested_dict_operations(self):
        """Test nested dictionary utilities."""
        from haive.core.schema.compatibility.utils import (
            flatten_nested_dict,
            unflatten_dict,
        )

        nested = {"user": {"name": "John", "age": 30}}
        flat = flatten_nested_dict(nested)
        assert flat == {"user.name": "John", "user.age": 30}

        unflat = unflatten_dict(flat)
        assert unflat == nested


# Integration tests
class TestIntegration:
    """Integration tests combining multiple components."""

    def test_full_compatibility_workflow(self):
        """Test complete compatibility checking workflow."""

        # Define schemas
        class SourceAgent(BaseModel):
            query: str
            context: List[str] = Field(default_factory=list)

        class TargetAgent(BaseModel):
            question: str  # Different name!
            context: List[str] = Field(default_factory=list)
            max_tokens: int = 1000

        # Check compatibility
        result = check_compatibility(SourceAgent, TargetAgent)
        assert not result.is_compatible  # Missing 'question'

        # Create mapping
        mapper = FieldMapper()
        mapper.add_mapping("query", "question")
        mapper.add_mapping("context", "context")
        mapper.add_computed_field("max_tokens", generator=lambda: 1000)

        # Test mapping
        source_data = {"query": "What is AI?", "context": ["doc1", "doc2"]}
        mapped_data = mapper.map_data(source_data)

        # Validate against target
        target_instance = TargetAgent(**mapped_data)
        assert target_instance.question == "What is AI?"
        assert target_instance.max_tokens == 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
