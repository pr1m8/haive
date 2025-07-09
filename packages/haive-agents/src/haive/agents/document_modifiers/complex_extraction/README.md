# Complex Extraction

Advanced structured data extraction with validation and retry mechanisms.

## Overview

The Complex Extraction module provides a robust agent for extracting structured data from unstructured text using schema validation and intelligent retry strategies. It's designed to handle complex extraction scenarios where initial attempts may fail, using JSONPatch-based error correction to iteratively improve extraction results.

Key features:

- **Schema-based extraction**: Define target data structure using Pydantic models
- **Validation with retries**: Automatic retry with error feedback
- **JSONPatch correction**: Fine-grained fixes for validation errors
- **Flexible retry strategies**: Configurable retry policies
- **Type safety**: Full type validation for extracted data

This module is ideal for:

- Extracting structured business data from documents
- Parsing complex forms and reports
- Converting unstructured text to database records
- Building reliable data pipelines with validation
- Handling extraction tasks that require multiple attempts

## Architecture

The module uses a multi-layered approach:

1. **Initial Extraction**: Attempt to extract data according to schema
2. **Validation**: Check extracted data against Pydantic model
3. **Error Analysis**: If validation fails, analyze specific errors
4. **JSONPatch Generation**: Create targeted fixes for validation errors
5. **Retry with Corrections**: Apply patches and retry extraction
6. **Success or Exhaustion**: Return valid data or best attempt

## Key Components

### ComplexExtractionAgent

The main agent class that orchestrates the extraction process with intelligent retry logic.

### Configuration

- **ComplexExtractionAgentConfig**: Comprehensive configuration options
- **RetryStrategy**: Defines how retries are handled
- **ExtractionModel**: Your Pydantic model defining the target schema

### Models

- **ExtractionResult**: Wraps extracted data with metadata
- **ValidationError**: Detailed error information for failed extractions
- **JSONPatch**: Correction operations for fixing extraction errors

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Structured Extraction

```python
from haive.agents.document_modifiers.complex_extraction import ComplexExtractionAgent
from haive.agents.document_modifiers.complex_extraction.config import ComplexExtractionAgentConfig
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Define your target schema
class CompanyInfo(BaseModel):
    name: str = Field(..., description="Company legal name")
    founded_year: int = Field(..., ge=1800, le=2024)
    headquarters: str = Field(..., description="City and country")
    employees: int = Field(..., gt=0)
    revenue: Optional[float] = Field(None, description="Annual revenue in millions USD")
    products: List[str] = Field(..., min_items=1)
    public: bool = Field(..., description="Whether publicly traded")

# Configure the agent
config = ComplexExtractionAgentConfig(
    extraction_model=CompanyInfo,
    max_retries=3,
    use_jsonpatch=True,
    name="company_extractor"
)

# Create agent
agent = ComplexExtractionAgent(config)

# Extract from text
text = """
Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
The company is headquartered in Cupertino, USA and employs approximately 164,000
people worldwide. With annual revenue exceeding $380 billion, Apple is publicly
traded and known for products including the iPhone, iPad, Mac computers,
Apple Watch, and various software services.
"""

result = agent.run(text)
company = result["extracted_data"]

print(f"Company: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Employees: {company.employees:,}")
print(f"Products: {', '.join(company.products)}")
```

### Complex Nested Extraction

```python
from typing import List, Dict, Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

class ContactInfo(BaseModel):
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{10,14}$')
    website: Optional[str] = None

class Person(BaseModel):
    first_name: str
    last_name: str
    title: Optional[str] = None
    department: Optional[str] = None

class Meeting(BaseModel):
    title: str
    date: datetime
    duration_minutes: int = Field(..., ge=15, le=480)
    location: Address
    organizer: Person
    attendees: List[Person]
    contact: ContactInfo
    agenda_items: List[str]
    notes: Optional[str] = None

# Configure with custom retry strategy
config = ComplexExtractionAgentConfig(
    extraction_model=Meeting,
    max_retries=5,  # More retries for complex schema
    use_jsonpatch=True,
    retry_strategy="exponential_backoff",
    temperature=0.1  # Lower temperature for consistency
)

agent = ComplexExtractionAgent(config)

meeting_text = """
Meeting: Q4 Planning Session
Date: December 15, 2024 at 2:00 PM
Duration: 90 minutes

Location:
Tech Corp Headquarters
123 Innovation Drive
San Francisco, CA 94105

Organizer: Sarah Johnson (VP of Product, Product Development)
Contact: sarah.johnson@techcorp.com, +1-415-555-0123
Website: www.techcorp.com/meetings

Attendees:
- Michael Chen (Director, Engineering)
- Emily Rodriguez (Senior Manager, Marketing)
- David Kim (Lead Designer, Design)

Agenda:
1. Review Q3 performance metrics
2. Set Q4 OKRs and targets
3. Discuss resource allocation
4. Address technical debt priorities
5. Marketing campaign planning

Notes: Please review the Q3 report before attending.
"""

result = agent.run(meeting_text)
meeting = result["extracted_data"]
```

### Error Handling and Validation

```python
class ProductReview(BaseModel):
    product_name: str
    rating: float = Field(..., ge=1.0, le=5.0)
    review_date: date
    verified_purchase: bool
    pros: List[str] = Field(..., min_items=1)
    cons: List[str] = Field(default_factory=list)
    recommendation: Literal["yes", "no", "maybe"]

# Configure with validation focus
config = ComplexExtractionAgentConfig(
    extraction_model=ProductReview,
    max_retries=4,
    use_jsonpatch=True,
    strict_validation=True,  # Enforce all constraints
    log_errors=True  # Log validation errors for debugging
)

agent = ComplexExtractionAgent(config)

# Handle extraction with error recovery
try:
    result = agent.run(review_text)
    review = result["extracted_data"]

    # Check extraction confidence
    if result.get("confidence", 0) < 0.8:
        print("Warning: Low confidence extraction")

except ExtractionError as e:
    print(f"Extraction failed: {e}")
    # Access partial results if available
    if e.partial_result:
        print(f"Partial data: {e.partial_result}")
```

### JSONPatch Error Correction

```python
# The agent uses JSONPatch to fix specific validation errors
# This happens automatically when use_jsonpatch=True

# Example of what happens internally:
# 1. Initial extraction attempt
initial_data = {
    "name": "Apple",  # Missing "Inc."
    "founded_year": "1976",  # Should be int
    "employees": -1,  # Invalid negative number
    "products": []  # Empty list not allowed
}

# 2. Validation errors detected
# 3. JSONPatch operations generated:
patches = [
    {"op": "replace", "path": "/name", "value": "Apple Inc."},
    {"op": "replace", "path": "/founded_year", "value": 1976},
    {"op": "replace", "path": "/employees", "value": 164000},
    {"op": "add", "path": "/products/0", "value": "iPhone"}
]

# 4. Patches applied and re-validated
# 5. Process repeats until valid or max retries
```

### Batch Processing

```python
from haive.agents.document_modifiers.complex_extraction.utils import batch_extract

class Invoice(BaseModel):
    invoice_number: str
    date: date
    total_amount: float
    items: List[Dict[str, Any]]
    paid: bool

# Process multiple documents
documents = load_invoice_documents()  # Your document loader

config = ComplexExtractionAgentConfig(
    extraction_model=Invoice,
    max_retries=3,
    use_jsonpatch=True,
    parallel_processing=True  # Enable parallel extraction
)

agent = ComplexExtractionAgent(config)

# Batch extraction with progress tracking
results = []
for i, doc in enumerate(documents):
    try:
        result = agent.run(doc)
        results.append(result["extracted_data"])
        print(f"Processed {i+1}/{len(documents)}")
    except Exception as e:
        print(f"Failed on document {i}: {e}")
        results.append(None)

# Filter successful extractions
valid_invoices = [r for r in results if r is not None]
```

## Configuration Options

### ComplexExtractionAgentConfig

- `extraction_model`: Pydantic model class defining target schema
- `max_retries`: Maximum extraction attempts (default: 3)
- `use_jsonpatch`: Enable JSONPatch error correction (default: True)
- `retry_strategy`: Strategy for retries ("immediate", "exponential_backoff")
- `temperature`: LLM temperature for extraction (default: 0.3)
- `strict_validation`: Enforce all schema constraints (default: True)
- `log_errors`: Log validation errors for debugging (default: False)
- `timeout`: Timeout per extraction attempt in seconds (default: 30)

### Retry Strategies

1. **Immediate**: Retry immediately after failure
2. **Exponential Backoff**: Increasing delays between retries
3. **Custom**: Define your own retry logic

## Best Practices

1. **Schema Design**
   - Start simple and add complexity gradually
   - Use clear field descriptions for better extraction
   - Set reasonable constraints (min/max values, regex patterns)
   - Make fields Optional when data might be missing

2. **Error Handling**
   - Always wrap extractions in try-except blocks
   - Check confidence scores when available
   - Log failed extractions for analysis
   - Consider partial results for non-critical fields

3. **Performance Optimization**
   - Use lower temperatures (0.1-0.3) for consistency
   - Batch similar documents together
   - Cache extraction results when possible
   - Consider parallel processing for large batches

4. **Validation Strategy**
   - Use JSONPatch for complex schemas
   - Set appropriate max_retries based on complexity
   - Validate business logic separately from schema
   - Test with edge cases and malformed inputs

## Troubleshooting

### Common Issues

1. **Consistent Validation Failures**

   ```python
   # Solution: Relax constraints or improve descriptions
   class FlexibleSchema(BaseModel):
       amount: float = Field(..., description="Amount in any currency")
       # Instead of strict USD validation
   ```

2. **Timeout Errors**

   ```python
   # Solution: Increase timeout or simplify schema
   config.timeout = 60  # 60 seconds
   ```

3. **Poor Extraction Quality**

   ```python
   # Solution: Provide examples in field descriptions
   class BetterSchema(BaseModel):
       category: str = Field(
           ...,
           description="Product category (e.g., 'Electronics', 'Clothing', 'Food')"
       )
   ```

4. **JSONPatch Not Helping**
   ```python
   # Solution: Check if errors are structural vs. content
   config.use_jsonpatch = False  # Disable for simple schemas
   config.max_retries = 5  # Increase direct retries instead
   ```

## Advanced Usage

### Custom Validation

```python
class CustomProduct(BaseModel):
    name: str
    price: float

    @validator('price')
    def price_must_be_reasonable(cls, v):
        if v < 0.01 or v > 1000000:
            raise ValueError('Price must be between $0.01 and $1,000,000')
        return v

    @root_validator
    def check_name_price_consistency(cls, values):
        name = values.get('name', '').lower()
        price = values.get('price', 0)

        if 'luxury' in name and price < 100:
            raise ValueError('Luxury items should be priced above $100')

        return values
```

### Custom Retry Logic

```python
from haive.agents.document_modifiers.complex_extraction.models import RetryStrategy

class CustomRetryStrategy(RetryStrategy):
    def should_retry(self, attempt: int, error: Exception) -> bool:
        # Custom logic for when to retry
        if isinstance(error, ValidationError):
            # Always retry validation errors up to max
            return attempt < self.max_retries
        return False

    def get_delay(self, attempt: int) -> float:
        # Custom delay calculation
        return min(2 ** attempt, 30)  # Exponential with cap

config.retry_strategy = CustomRetryStrategy(max_retries=5)
```

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/document_modifiers/complex_extraction/index.rst).

## See Also

- [`haive.agents.document_modifiers`](../): Parent module
- [`haive.agents.document_modifiers.base`](../base/): Base document processing
- [`pydantic`](https://docs.pydantic.dev/): Schema validation library
- [`jsonpatch`](http://jsonpatch.com/): JSONPatch specification
