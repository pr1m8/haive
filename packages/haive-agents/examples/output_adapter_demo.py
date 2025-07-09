"""Demo of OutputAdapter and transformation functionality."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from haive.agents.base.mixins.output_mixin import OutputAdapter, OutputMixin


# Define structured output models
class ProductAnalysis(BaseModel):
    """Structured output for product analysis."""

    product_name: str = Field(description="Name of the product")
    pros: List[str] = Field(description="List of advantages")
    cons: List[str] = Field(description="List of disadvantages")
    overall_rating: float = Field(description="Overall rating out of 10")
    recommendation: str = Field(description="Buy, Consider, or Avoid")


class EmailSummary(BaseModel):
    """Structured output for email summarization."""

    subject: str = Field(description="Email subject")
    sender: str = Field(description="Who sent the email")
    urgency: str = Field(description="High, Medium, or Low")
    action_items: List[str] = Field(description="Action items from email")
    deadline: Optional[str] = Field(default=None, description="Deadline if any")


class APIResponse(BaseModel):
    """Generic API response format."""

    status: str
    data: Dict[str, Any]
    error: Optional[str] = None


def demo_basic_transformation():
    """Demo: Basic output transformation."""
    print("=== Basic Transformation Demo ===")

    # Create adapter for product analysis
    adapter = OutputAdapter(target_schema=ProductAnalysis)

    # Simulate raw output from an agent
    raw_output = {
        "product_name": "TechPro X500 Headphones",
        "pros": [
            "Excellent sound quality",
            "30+ hour battery life",
            "Comfortable design",
        ],
        "cons": ["Expensive at $350", "Bulky carrying case"],
        "overall_rating": 8.5,
        "recommendation": "Consider",
    }

    print("Raw Output (dict):")
    print(f"  Type: {type(raw_output)}")
    print(f"  Keys: {list(raw_output.keys())}")

    # Transform to structured output
    structured = adapter.transform(raw_output)

    print("\nStructured Output:")
    print(f"  Type: {type(structured)}")
    print(f"  Product: {structured.product_name}")
    print(f"  Rating: {structured.overall_rating}/10")
    print(f"  Recommendation: {structured.recommendation}")
    print(f"  Pros: {len(structured.pros)} items")
    print(f"  Cons: {len(structured.cons)} items")


def demo_field_mapping():
    """Demo: Field mapping during transformation."""
    print("\n\n=== Field Mapping Demo ===")

    # Create adapter with field mapping
    adapter = OutputAdapter(
        target_schema=EmailSummary,
        field_mapping={
            "email_subject": "subject",
            "from": "sender",
            "priority": "urgency",
            "todos": "action_items",
            "due_date": "deadline",
        },
    )

    # Raw output with different field names
    raw_output = {
        "email_subject": "Q4 Budget Review",
        "from": "john@company.com",
        "priority": "High",
        "todos": [
            "Review financial reports",
            "Prepare questions for meeting",
            "Confirm attendance",
        ],
        "due_date": "2024-01-10",
        "other_field": "ignored",  # This will be ignored
    }

    print("Raw Output Fields:")
    for key, value in raw_output.items():
        print(f"  {key}: {value}")

    # Transform with field mapping
    structured = adapter.transform(raw_output)

    print("\nMapped Output:")
    print(f"  Subject: {structured.subject}")
    print(f"  Sender: {structured.sender}")
    print(f"  Urgency: {structured.urgency}")
    print(f"  Action Items: {structured.action_items}")
    print(f"  Deadline: {structured.deadline}")


def demo_field_extraction():
    """Demo: Extracting nested fields."""
    print("\n\n=== Field Extraction Demo ===")

    # Create adapter that extracts from nested field
    adapter = OutputAdapter(
        target_schema=ProductAnalysis, extract_field="analysis_result"
    )

    # Nested output structure
    raw_output = {
        "status": "success",
        "timestamp": "2024-01-07T10:30:00Z",
        "analysis_result": {
            "product_name": "SmartWatch Pro",
            "pros": ["Health tracking", "Long battery", "Water resistant"],
            "cons": ["Limited app selection", "Small screen"],
            "overall_rating": 7.5,
            "recommendation": "Buy",
        },
        "metadata": {"analyzer_version": "1.0", "confidence": 0.9},
    }

    print("Nested Output Structure:")
    print(f"  Top-level keys: {list(raw_output.keys())}")
    print(f"  Extraction target: 'analysis_result'")

    # Extract and transform
    structured = adapter.transform(raw_output)

    print("\nExtracted and Structured:")
    print(f"  Product: {structured.product_name}")
    print(f"  Rating: {structured.overall_rating}")
    print(f"  Pros: {', '.join(structured.pros[:2])}...")


def demo_missing_fields():
    """Demo: Handling missing fields with defaults."""
    print("\n\n=== Missing Fields Demo ===")

    adapter = OutputAdapter(target_schema=EmailSummary)

    # Partial data - missing optional fields
    partial_output = {
        "subject": "Team Meeting",
        "sender": "manager@company.com",
        "urgency": "Medium",
        "action_items": ["Attend meeting", "Bring reports"],
        # deadline is missing but it's optional
    }

    print("Partial Output:")
    print(f"  Provided fields: {list(partial_output.keys())}")
    print(f"  Missing: deadline (optional)")

    structured = adapter.transform(partial_output)

    print("\nStructured with Defaults:")
    print(f"  Subject: {structured.subject}")
    print(f"  Deadline: {structured.deadline} (None is the default)")


def demo_validation_errors():
    """Demo: How validation errors are handled."""
    print("\n\n=== Validation Error Handling Demo ===")

    adapter = OutputAdapter(target_schema=ProductAnalysis)

    # Invalid data - missing required fields
    invalid_output = {
        "product_name": "Incomplete Product",
        "overall_rating": "not a number",  # Wrong type
        # Missing: pros, cons, recommendation
    }

    print("Invalid Output:")
    print(f"  Fields: {list(invalid_output.keys())}")
    print(f"  Issues: wrong type for rating, missing required fields")

    try:
        structured = adapter.transform(invalid_output)
        print("\nTransformation succeeded with defaults:")
        print(f"  Product: {structured.product_name}")
        print(f"  Rating: {structured.overall_rating}")
        print(f"  Pros: {structured.pros} (auto-filled)")
        print(f"  Cons: {structured.cons} (auto-filled)")
        print(f"  Recommendation: {structured.recommendation} (auto-filled)")
    except Exception as e:
        print(f"\nTransformation failed: {type(e).__name__}")
        print(f"  Error: {str(e)}")


def demo_complex_transformation():
    """Demo: Complex transformation with multiple steps."""
    print("\n\n=== Complex Transformation Demo ===")

    # API response to structured format
    class UserActivity(BaseModel):
        user_id: str
        total_actions: int
        last_action: str
        is_active: bool
        activity_score: float

    # Complex adapter with extraction and mapping
    adapter = OutputAdapter(
        target_schema=UserActivity,
        extract_field="data",
        field_mapping={
            "id": "user_id",
            "action_count": "total_actions",
            "latest_activity": "last_action",
            "active_status": "is_active",
            "engagement_score": "activity_score",
        },
    )

    # Complex nested response
    api_response = {
        "success": True,
        "data": {
            "id": "user_123",
            "action_count": 42,
            "latest_activity": "Posted comment",
            "active_status": True,
            "engagement_score": 0.85,
            "profile": {"name": "John Doe", "joined": "2023-01-01"},
        },
        "meta": {"request_id": "req_456", "duration_ms": 125},
    }

    print("Complex API Response:")
    print(f"  Structure: Nested with data, meta sections")
    print(f"  Data fields need mapping to match schema")

    structured = adapter.transform(api_response)

    print("\nTransformed Result:")
    print(f"  User ID: {structured.user_id}")
    print(f"  Total Actions: {structured.total_actions}")
    print(f"  Last Action: {structured.last_action}")
    print(f"  Active: {structured.is_active}")
    print(f"  Activity Score: {structured.activity_score}")


def demo_output_mixin():
    """Demo: Using OutputMixin in a custom class."""
    print("\n\n=== OutputMixin Usage Demo ===")

    class DataProcessor(OutputMixin):
        """Example processor using OutputMixin."""

        def __init__(self):
            super().__init__(
                structured_output_model=ProductAnalysis, output_field_name="analysis"
            )

        def process(self, data: Dict[str, Any]) -> ProductAnalysis:
            """Process data and return structured output."""
            # Use the mixin's transform_output method
            return self.transform_output(data)

    processor = DataProcessor()

    # Input data
    data = {
        "product_name": "EcoBottle 2.0",
        "pros": ["Sustainable", "Durable", "BPA-free"],
        "cons": ["Higher price point"],
        "overall_rating": 9.0,
        "recommendation": "Buy",
    }

    print("Using OutputMixin in custom class:")
    print(f"  Class: {processor.__class__.__name__}")
    print(f"  Output Model: {processor.structured_output_model.__name__}")
    print(f"  Field Name: {processor._get_output_field_name()}")

    result = processor.process(data)

    print("\nProcessed Output:")
    print(f"  Type: {type(result).__name__}")
    print(f"  Product: {result.product_name}")
    print(f"  Rating: {result.overall_rating}/10")


def main():
    """Run all demos."""
    print("=== OutputAdapter and Transformation Demos ===\n")

    demo_basic_transformation()
    demo_field_mapping()
    demo_field_extraction()
    demo_missing_fields()
    demo_validation_errors()
    demo_complex_transformation()
    demo_output_mixin()

    print("\n\n=== Summary ===")
    print("OutputAdapter provides:")
    print("• Type-safe transformation from dict to Pydantic models")
    print("• Field mapping for different naming conventions")
    print("• Nested field extraction")
    print("• Automatic handling of missing optional fields")
    print("• Validation with helpful defaults")
    print("• Integration with agent classes via OutputMixin")


if __name__ == "__main__":
    main()
