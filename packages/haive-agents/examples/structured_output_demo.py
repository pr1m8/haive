"""Real-world demo of structured output functionality without mocks."""

import asyncio
from typing import Any, Dict, List, Optional

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
    target_audience: list[str] = Field(description="Who this product is for")


class EmailSummary(BaseModel):
    """Structured output for email summarization."""

    subject: str = Field(description="Email subject or main topic")
    sender_intent: str = Field(description="What the sender wants")
    key_points: list[str] = Field(description="Main points from the email")
    action_required: bool = Field(description="Whether action is needed")
    urgency: str = Field(description="High, Medium, or Low")
    suggested_response: str | None = Field(
        default=None, description="Suggested reply if needed"
    )


class TechnicalDocAnalysis(BaseModel):
    """Structured output for technical documentation analysis."""

    title: str = Field(description="Document title")
    purpose: str = Field(description="Main purpose of the document")
    key_concepts: list[str] = Field(description="Important technical concepts")
    code_examples: list[str] = Field(description="Code snippets or examples found")
    prerequisites: list[str] = Field(description="Required knowledge or tools")
    difficulty_level: str = Field(description="Beginner, Intermediate, or Advanced")


async def demo_product_analysis():
    """Demo: Analyze a product review and extract structured insights."""

    # Create a simple agent with a mock engine for demo
    # In production, you'd use a real LLM engine
    analysis_agent = SimpleAgent(
        name="product_analyzer",
        engine=AugLLMConfig(
            name="mock_engine",
            model="gpt-4",  # This would be a real model in production
            temperature=0.3,
        ),
        system_message="You are a product analysis expert. Analyze products objectively and provide structured insights.",
    )

    # Wrap with structured output
    StructuredOutputAgent.wrap(
        agent=analysis_agent,
        structured_output_model=ProductAnalysis,
        transformation_prompt="""Analyze the product review and extract:
- Product name
- List of pros (advantages)
- List of cons (disadvantages)
- Overall rating (0-10)
- Recommendation (Buy/Consider/Avoid)
- Target audience

Be objective and thorough in your analysis.""",
    )

    # Sample product review
    review = """
    I recently purchased the TechPro X500 Wireless Headphones and have been using them for 2 weeks.

    The sound quality is exceptional - crisp highs and deep bass. The noise cancellation is
    incredibly effective, blocking out most ambient noise. Battery life is impressive at 30+ hours.
    The headphones are comfortable for long listening sessions.

    However, they are quite expensive at $350. The carrying case is bulky and doesn't fit well
    in backpacks. The touch controls can be overly sensitive and trigger accidentally.

    Overall, these are premium headphones for audiophiles and frequent travelers who value
    sound quality and noise cancellation over portability and price.
    """


    # Run analysis (in real usage, this would call the LLM)
    # For demo, we'll create a mock result
    mock_result = ProductAnalysis(
        product_name="TechPro X500 Wireless Headphones",
        pros=[
            "Exceptional sound quality with crisp highs and deep bass",
            "Highly effective noise cancellation",
            "Impressive 30+ hour battery life",
            "Comfortable for extended use",
        ],
        cons=[
            "High price point at $350",
            "Bulky carrying case",
            "Overly sensitive touch controls",
        ],
        overall_rating=8.5,
        recommendation="Consider",
        target_audience=[
            "Audiophiles",
            "Frequent travelers",
            "Remote workers",
            "Music professionals",
        ],
    )

    for pro in mock_result.pros:
        pass
    for con in mock_result.cons:
        pass


async def demo_email_summary():
    """Demo: Summarize emails with structured output."""

    # Create email summarizer
    email_agent = SimpleAgent(
        name="email_summarizer",
        engine=AugLLMConfig(
            name="mock_email_engine", model="gpt-3.5-turbo", temperature=0.2
        ),
        system_message="You are an email analysis assistant. Extract key information from emails.",
    )

    StructuredOutputAgent.wrap(
        agent=email_agent, structured_output_model=EmailSummary
    )

    # Sample email
    email = """
    Subject: Urgent: Q4 Budget Review Meeting Rescheduled

    Hi Team,

    Due to the CEO's schedule conflict, we need to reschedule tomorrow's Q4 budget review meeting.

    New time: Thursday, 2:00 PM - 4:00 PM (Conference Room A)

    Please review the attached financial reports before the meeting. Pay special attention to:
    - Marketing spend variance (15% over budget)
    - R&D allocation for Project Phoenix
    - Proposed headcount changes for 2024

    I need everyone to confirm attendance by EOD today. If you can't make the new time,
    please propose alternatives.

    Also, Sarah from Finance will present the revised forecasts, so please prepare any
    questions you have about the numbers.

    Thanks,
    Mark
    """


    # Mock structured output
    mock_summary = EmailSummary(
        subject="Q4 Budget Review Meeting Rescheduled",
        sender_intent="Reschedule meeting and ensure preparation",
        key_points=[
            "Meeting moved to Thursday 2-4 PM in Conference Room A",
            "Review financial reports beforehand",
            "Marketing 15% over budget needs attention",
            "R&D allocation for Project Phoenix to be discussed",
            "2024 headcount changes on agenda",
            "Sarah from Finance will present revised forecasts",
        ],
        action_required=True,
        urgency="High",
        suggested_response="Hi Mark, I can confirm attendance for Thursday 2-4 PM. I've reviewed the reports and have questions about the marketing variance. See you Thursday.",
    )

    for point in mock_summary.key_points:
        pass")


async def demo_technical_doc_analysis():
    """Demo: Analyze technical documentation."""

    # Create doc analyzer with structured output enhancer
    doc_agent = SimpleAgent(
        name="doc_analyzer",
        engine=AugLLMConfig(name="mock_doc_engine", model="gpt-4", temperature=0.1),
    )

    # Use the enhancer pattern
    StructuredOutputEnhancer.append_structured_output(
        agent=doc_agent,
        structured_output_model=TechnicalDocAnalysis,
        extraction_prompt="Extract technical details including concepts, code examples, and prerequisites.",
    )

    # Sample technical content
    tech_doc = """
    # Building RESTful APIs with FastAPI

    This guide covers creating production-ready REST APIs using FastAPI, a modern Python web framework.

    ## Prerequisites
    - Python 3.8+
    - Basic understanding of REST principles
    - Familiarity with async/await in Python

    ## Quick Start

    ```python
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class Item(BaseModel):
        name: str
        price: float
        is_offer: bool = False

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/items/")
    async def create_item(item: Item):
        return item
    ```

    Key concepts covered:
    - Automatic API documentation with Swagger/OpenAPI
    - Request/response validation using Pydantic
    - Async request handling for high performance
    - Dependency injection system
    - Built-in security and authentication
    """


    # Mock analysis result
    mock_analysis = TechnicalDocAnalysis(
        title="Building RESTful APIs with FastAPI",
        purpose="Guide for creating production-ready REST APIs using FastAPI framework",
        key_concepts=[
            "RESTful API design",
            "FastAPI framework",
            "Pydantic models for validation",
            "Async request handling",
            "Automatic API documentation",
            "Dependency injection",
            "Security and authentication",
        ],
        code_examples=[
            "Basic FastAPI app setup with app = FastAPI()",
            "Pydantic model definition for Item class",
            "GET endpoint example at root path",
            "POST endpoint with async handler and validation",
        ],
        prerequisites=[
            "Python 3.8 or higher",
            "Understanding of REST principles",
            "Knowledge of async/await in Python",
        ],
        difficulty_level="Intermediate",
    )

    for concept in mock_analysis.key_concepts:
        pass}")
    for i, example in enumerate(mock_analysis.code_examples, 1):
        pass
    for prereq in mock_analysis.prerequisites:
        pass")


async def demo_output_adapter():
    """Demo: Direct use of OutputAdapter for transformations."""


    # Example: Transform raw API response to structured format
    class APIResponse(BaseModel):
        status: str
        data: dict
        timestamp: str

    class ProcessedData(BaseModel):
        success: bool
        user_count: int
        message: str

    # Create adapter with field mapping
    adapter = OutputAdapter(
        target_schema=ProcessedData,
        field_mapping={
            "status": "success",
            "total_users": "user_count",
            "response_message": "message",
        },
    )

    # Raw API response
    raw_response = {
        "status": "ok",
        "data": {"users": ["alice", "bob", "charlie"], "total_users": 3},
        "response_message": "Query completed successfully",
        "timestamp": "2024-01-07T10:30:00Z",
    }


    # Transform using adapter
    # Note: We need to flatten the data for this example
    flattened = {
        "status": raw_response["status"] == "ok",
        "total_users": raw_response["data"]["total_users"],
        "response_message": raw_response["response_message"],
    }

    processed = adapter.transform(flattened)



async def main():
    """Run all demos."""

    await demo_product_analysis()
    await demo_email_summary()
    await demo_technical_doc_analysis()
    await demo_output_adapter()



if __name__ == "__main__":
    asyncio.run(main())
