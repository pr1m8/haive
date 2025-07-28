"""Demo of OutputAdapter and transformation functionality."""

import contextlib
from typing import Any

from pydantic import BaseModel, Field

from haive.agents.base.mixins.output_mixin import OutputAdapter, OutputMixin


# Define structured output models
class ProductAnalysis(BaseModel):
    """Structured output for product analysis."""

    product_name: str = Field(description="Name of the product")
    pros: list[str] = Field(description="List of advantages")
    cons: list[str] = Field(description="List of disadvantages")
    overall_rating: float = Field(description="Overall rating out of 10")
    recommendation: str = Field(description="Buy, Consider, or Avoid")


class EmailSummary(BaseModel):
    """Structured output for email summarization."""

    subject: str = Field(description="Email subject")
    sender: str = Field(description="Who sent the email")
    urgency: str = Field(description="High, Medium, or Low")
    action_items: list[str] = Field(description="Action items from email")
    deadline: str | None = Field(default=None, description="Deadline if any")


class APIResponse(BaseModel):
    """Generic API response format."""

    status: str
    data: dict[str, Any]
    error: str | None = None


def demo_basic_transformation():
    """Demo: Basic output transformation."""
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

    # Transform to structured output
    adapter.transform(raw_output)


def demo_field_mapping():
    """Demo: Field mapping during transformation."""
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

    for _key, _value in raw_output.items():
        pass

    # Transform with field mapping
    adapter.transform(raw_output)


def demo_field_extraction():
    """Demo: Extracting nested fields."""
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

    # Extract and transform
    adapter.transform(raw_output)


def demo_missing_fields():
    """Demo: Handling missing fields with defaults."""
    adapter = OutputAdapter(target_schema=EmailSummary)

    # Partial data - missing optional fields
    partial_output = {
        "subject": "Team Meeting",
        "sender": "manager@company.com",
        "urgency": "Medium",
        "action_items": ["Attend meeting", "Bring reports"],
        # deadline is missing but it's optional
    }

    adapter.transform(partial_output)


def demo_validation_errors():
    """Demo: How validation errors are handled."""
    adapter = OutputAdapter(target_schema=ProductAnalysis)

    # Invalid data - missing required fields
    invalid_output = {
        "product_name": "Incomplete Product",
        "overall_rating": "not a number",  # Wrong type
        # Missing: pros, cons, recommendation
    }

    with contextlib.suppress(Exception):
        adapter.transform(invalid_output)


def demo_complex_transformation():
    """Demo: Complex transformation with multiple steps."""

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

    adapter.transform(api_response)


def demo_output_mixin():
    """Demo: Using OutputMixin in a custom class."""

    class DataProcessor(OutputMixin):
        """Example processor using OutputMixin."""

        def __init__(self):
            super().__init__(
                structured_output_model=ProductAnalysis, output_field_name="analysis"
            )

        def process(self, data: dict[str, Any]) -> ProductAnalysis:
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

    processor.process(data)


def main():
    """Run all demos."""
    demo_basic_transformation()
    demo_field_mapping()
    demo_field_extraction()
    demo_missing_fields()
    demo_validation_errors()
    demo_complex_transformation()
    demo_output_mixin()


if __name__ == "__main__":
    main()
