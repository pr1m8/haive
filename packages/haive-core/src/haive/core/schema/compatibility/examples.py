"""
Examples demonstrating the schema compatibility module.

This file shows various use cases and patterns for using the
schema compatibility system in the Haive framework.
"""

from typing import Any, Dict, List, Optional, Tuple

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field

# Import compatibility module components
from haive.core.schema.compatibility import (
    CompatibilityChecker,
    CompatibilityLevel,
    ConverterRegistry,
    FieldMapper,
    MessageConverter,
    SchemaMerger,
    TypeAnalyzer,
    check_compatibility,
    create_mapping,
    generate_report,
    merge_schemas,
    register_converter,
)


# Example 1: Basic Schema Compatibility Check
def example_basic_compatibility():
    """Check basic compatibility between two schemas."""
    print("=== Example 1: Basic Compatibility Check ===\n")

    # Define source schema
    class UserInput(BaseModel):
        name: str
        email: str
        age: int
        preferences: List[str] = Field(default_factory=list)

    # Define target schema
    class UserProfile(BaseModel):
        name: str
        email: str
        age: Optional[int] = None
        bio: str = ""
        preferences: List[str] = Field(default_factory=list)

    # Check compatibility
    result = check_compatibility(UserInput, UserProfile)

    print(f"Compatible: {result.is_compatible}")
    print(f"Level: {result.level}")
    print(f"Missing required fields: {result.missing_required_fields}")
    print(f"Extra fields: {result.extra_fields}")
    print()


# Example 2: Type Conversion with LangChain Types
def example_langchain_conversion():
    """Convert between LangChain types."""
    print("=== Example 2: LangChain Type Conversion ===\n")

    # Create converter registry
    registry = ConverterRegistry()

    # Register LangChain converters
    registry.register(MessageConverter())

    # Convert HumanMessage to AIMessage
    human_msg = HumanMessage(content="Hello, how are you?")

    ai_msg = registry.convert(
        human_msg,
        source_type=HumanMessage,
        target_type=AIMessage,
    )

    print(f"Original: {human_msg}")
    print(f"Converted: {ai_msg}")
    print()

    # Convert Document to HumanMessage
    doc = Document(
        page_content="This is important information.",
        metadata={"source": "manual.pdf", "page": 5},
    )

    # This would need DocumentConverter registered
    # msg = registry.convert(doc, Document, HumanMessage)


# Example 3: Field Mapping
def example_field_mapping():
    """Map fields between incompatible schemas."""
    print("=== Example 3: Field Mapping ===\n")

    # Source data structure
    source_data = {
        "user": {
            "firstName": "John",
            "lastName": "Doe",
            "contactInfo": {"email": "john@example.com", "phone": "555-1234"},
        },
        "items": [
            {"name": "Item 1", "price": 10.99},
            {"name": "Item 2", "price": 25.50},
        ],
    }

    # Create field mapper
    mapper = FieldMapper()

    # Add mappings with transformations
    mapper.add_mapping(
        source="user.firstName", target="first_name", transformer=str.lower
    )

    mapper.add_mapping(
        source="user.lastName", target="last_name", transformer=str.lower
    )

    mapper.add_mapping(source="user.contactInfo.email", target="email")

    # Aggregate mapping - combine first and last name
    mapper.add_aggregate_field(
        sources=["user.firstName", "user.lastName"],
        target="full_name",
        aggregator=lambda names: " ".join(names),
    )

    # Computed field
    mapper.add_computed_field(
        target="total_price",
        generator=lambda: sum(item["price"] for item in source_data.get("items", [])),
    )

    # Apply mappings
    result = mapper.map_data(source_data)

    print("Mapped result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print()


# Example 4: Schema Merging
def example_schema_merging():
    """Merge multiple schemas with different strategies."""
    print("=== Example 4: Schema Merging ===\n")

    # Define schemas to merge
    class BasicInfo(BaseModel):
        id: str
        name: str
        created_at: str

    class ContactInfo(BaseModel):
        name: str  # Overlapping field
        email: str
        phone: Optional[str] = None

    class Preferences(BaseModel):
        theme: str = "light"
        notifications: bool = True
        language: str = "en"

    # Merge with union strategy (all fields)
    UnionUser = merge_schemas(
        [BasicInfo, ContactInfo, Preferences], strategy="union", name="UnionUser"
    )

    print("Union merge - all fields:")
    for field_name, field_info in UnionUser.model_fields.items():
        print(f"  {field_name}: {field_info.annotation}")
    print()

    # Merge with intersection strategy (common fields only)
    CommonUser = merge_schemas(
        [BasicInfo, ContactInfo], strategy="intersection", name="CommonUser"
    )

    print("Intersection merge - common fields only:")
    for field_name, field_info in CommonUser.model_fields.items():
        print(f"  {field_name}: {field_info.annotation}")
    print()


# Example 5: Custom Type Converter
def example_custom_converter():
    """Create and register a custom type converter."""
    print("=== Example 5: Custom Type Converter ===\n")

    from haive.core.schema.compatibility.converters import TypeConverter
    from haive.core.schema.compatibility.types import (
        ConversionContext,
        ConversionQuality,
    )

    # Define custom types
    class Temperature(BaseModel):
        value: float
        unit: str  # "C" or "F"

    class Celsius(BaseModel):
        degrees: float

    # Create custom converter
    class TemperatureConverter(TypeConverter):
        @property
        def name(self) -> str:
            return "temperature_converter"

        def can_convert(self, source_type: type, target_type: type) -> bool:
            return (source_type == Temperature and target_type == Celsius) or (
                source_type == Celsius and target_type == Temperature
            )

        def get_quality(
            self, source_type: type, target_type: type
        ) -> ConversionQuality:
            return ConversionQuality.LOSSLESS

        def convert(self, value: Any, context: ConversionContext) -> Any:
            if isinstance(value, Temperature):
                # Convert to Celsius
                if value.unit == "C":
                    return Celsius(degrees=value.value)
                else:  # Fahrenheit
                    celsius = (value.value - 32) * 5 / 9
                    return Celsius(degrees=celsius)
            elif isinstance(value, Celsius):
                # Convert to Temperature (default to Celsius)
                return Temperature(value=value.degrees, unit="C")

    # Register converter
    register_converter(TemperatureConverter())

    # Use converter
    temp_f = Temperature(value=98.6, unit="F")
    temp_c = ConverterRegistry().convert(
        temp_f, source_type=Temperature, target_type=Celsius
    )

    print(f"Original: {temp_f}")
    print(f"Converted: {temp_c}")
    print()


# Example 6: Compatibility Report Generation
def example_compatibility_report():
    """Generate detailed compatibility report."""
    print("=== Example 6: Compatibility Report ===\n")

    # Define schemas with various compatibility issues
    class SourceAgent(BaseModel):
        messages: List[BaseMessage]
        context: str
        temperature: float = 0.7
        max_tokens: int = 1000

    class TargetAgent(BaseModel):
        messages: List[BaseMessage]
        context: List[str]  # Different type!
        model_name: str  # Required field missing in source
        temperature: float = 0.5
        stream: bool = False

    # Generate report
    report = generate_report(SourceAgent, TargetAgent)

    # Print markdown report
    print(report.to_markdown())
    print()


# Example 7: Haive StateSchema Integration
def example_state_schema_compatibility():
    """Check compatibility with Haive StateSchema features."""
    print("=== Example 7: StateSchema Compatibility ===\n")

    from haive.core.schema.compatibility.analyzer import TypeAnalyzer

    # Simulate StateSchema with special attributes
    class ChatState(BaseModel):
        messages: List[BaseMessage] = Field(default_factory=list)
        query: str = ""
        response: str = ""

        # Haive-specific metadata (would normally be class attributes)
        class Config:
            extra = "allow"

    # Add Haive metadata
    ChatState.__shared_fields__ = ["messages"]
    ChatState.__reducer_fields__ = {"messages": "add_messages"}
    ChatState.__engine_io_mappings__ = {
        "llm": {"inputs": ["messages", "query"], "outputs": ["response"]}
    }

    # Analyze schema
    analyzer = TypeAnalyzer()
    schema_info = analyzer.analyze_schema(ChatState)

    print(f"Schema: {schema_info.name}")
    print(f"Shared fields: {schema_info.shared_fields}")
    print(f"Reducer fields: {schema_info.reducer_fields}")
    print(f"Engine I/O mappings: {schema_info.engine_io_mappings}")
    print()


# Example 8: Complex Field Validation
def example_field_validation():
    """Create complex field validators."""
    print("=== Example 8: Field Validation ===\n")

    from haive.core.schema.compatibility.validators import (
        FieldValidator,
        ModelValidator,
        ValidatorBuilder,
        create_validator,
    )

    # Define schema with validation needs
    class UserRegistration(BaseModel):
        username: str
        email: str
        age: int
        password: str
        confirm_password: str
        interests: List[str] = Field(default_factory=list)

    # Create model validator
    validator = ModelValidator()

    # Add field validators
    validator.add_field_validator(
        "username", ValidatorBuilder.for_pattern(r"^[a-zA-Z0-9_]{3,20}$", "username")
    )

    validator.add_field_validator(
        "email", ValidatorBuilder.for_pattern(r"^[\w\.-]+@[\w\.-]+\.\w+$", "email")
    )

    validator.add_field_validator(
        "age", ValidatorBuilder.for_range(min_value=13, max_value=120, field_name="age")
    )

    # Add cross-field validator
    def passwords_match(data: dict) -> tuple[bool, str]:
        if data.get("password") != data.get("confirm_password"):
            return False, "Passwords do not match"
        return True, ""

    validator.add_cross_field_validator(passwords_match)

    # Validate data
    test_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 25,
        "password": "secure123",
        "confirm_password": "secure123",
        "interests": ["coding", "reading"],
    }

    result = validator.validate(test_data, None)
    print(f"Valid: {result.is_valid}")
    print(f"Errors: {[e.message for e in result.errors]}")
    print()


# Example 9: Schema Evolution
def example_schema_evolution():
    """Handle schema version migration."""
    print("=== Example 9: Schema Evolution ===\n")

    # V1 Schema
    class UserV1(BaseModel):
        name: str
        email: str
        role: str  # "admin" or "user"

    # V2 Schema - role becomes enum, add created_at
    from datetime import datetime
    from enum import Enum

    class Role(str, Enum):
        ADMIN = "admin"
        USER = "user"
        MODERATOR = "moderator"

    class UserV2(BaseModel):
        name: str
        email: str
        role: Role
        created_at: datetime = Field(default_factory=datetime.now)
        active: bool = True

    # Create migration function
    def migrate_v1_to_v2(v1_data: dict) -> dict:
        """Migrate UserV1 data to UserV2 format."""
        v2_data = v1_data.copy()

        # Convert role string to enum
        role_str = v2_data.get("role", "user")
        try:
            v2_data["role"] = Role(role_str)
        except ValueError:
            v2_data["role"] = Role.USER

        # Add new fields
        if "created_at" not in v2_data:
            v2_data["created_at"] = datetime.now()
        if "active" not in v2_data:
            v2_data["active"] = True

        return v2_data

    # Test migration
    v1_user = {"name": "Alice", "email": "alice@example.com", "role": "admin"}
    v2_user = migrate_v1_to_v2(v1_user)

    # Validate against V2 schema
    user_v2_instance = UserV2(**v2_user)
    print(f"Migrated user: {user_v2_instance}")
    print()


# Example 10: Performance Optimization
def example_performance_optimization():
    """Demonstrate performance features."""
    print("=== Example 10: Performance Optimization ===\n")

    import time

    # Create analyzer with cache
    analyzer = TypeAnalyzer(cache_size=1000)

    # Define complex schema
    class ComplexSchema(BaseModel):
        field1: str
        field2: int
        field3: List[str]
        field4: Dict[str, Any]
        field5: Optional[bool]
        # ... many more fields

    # First analysis (not cached)
    start = time.time()
    info1 = analyzer.analyze_schema(ComplexSchema)
    time1 = time.time() - start

    # Second analysis (cached)
    start = time.time()
    info2 = analyzer.analyze_schema(ComplexSchema)
    time2 = time.time() - start

    print(f"First analysis: {time1*1000:.2f}ms")
    print(f"Cached analysis: {time2*1000:.2f}ms")
    print(f"Speedup: {time1/time2:.1f}x")
    print()


# Run all examples
if __name__ == "__main__":
    examples = [
        example_basic_compatibility,
        example_langchain_conversion,
        example_field_mapping,
        example_schema_merging,
        example_custom_converter,
        example_compatibility_report,
        example_state_schema_compatibility,
        example_field_validation,
        example_schema_evolution,
        example_performance_optimization,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print()
