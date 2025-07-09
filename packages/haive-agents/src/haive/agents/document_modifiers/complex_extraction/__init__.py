"""Advanced structured data extraction with validation and retry mechanisms.

This module provides a sophisticated agent for extracting structured data from
unstructured text using Pydantic schema validation and intelligent retry strategies.
It features JSONPatch-based error correction to handle complex extraction scenarios
where initial attempts may fail due to validation errors.

The module implements a multi-layered approach:
    1. Initial extraction based on schema definition
    2. Validation against Pydantic models
    3. Error analysis and JSONPatch generation for corrections
    4. Iterative retry with targeted fixes
    5. Return of validated data or best effort

Key Features:
    - Schema-based extraction using Pydantic models
    - Automatic retry with validation error feedback
    - JSONPatch corrections for fine-grained error fixes
    - Configurable retry strategies (immediate, exponential backoff)
    - Full type safety and validation
    - Support for nested and complex data structures

Classes:
    - :class:`~haive.agents.document_modifiers.complex_extraction.agent.ComplexExtractionAgent`: Main extraction agent
    - :class:`~haive.agents.document_modifiers.complex_extraction.config.ComplexExtractionAgentConfig`: Configuration
    - :class:`~haive.agents.document_modifiers.complex_extraction.models.RetryStrategy`: Retry behavior customization

Example:
    Basic extraction with validation::

        from haive.agents.document_modifiers.complex_extraction import ComplexExtractionAgent
        from haive.agents.document_modifiers.complex_extraction.config import ComplexExtractionAgentConfig
        from pydantic import BaseModel, Field
        from typing import List

        class PersonInfo(BaseModel):
            name: str = Field(..., description="Full name")
            age: int = Field(..., ge=0, le=150)
            skills: List[str] = Field(..., min_items=1)

        config = ComplexExtractionAgentConfig(
            extraction_model=PersonInfo,
            max_retries=3,
            use_jsonpatch=True
        )

        agent = ComplexExtractionAgent(config)

        text = "John Doe is a 35-year-old developer skilled in Python, JavaScript, and SQL."
        result = agent.run(text)
        person = result["extracted_data"]

        print(f"{person.name} knows {len(person.skills)} languages")

    Complex nested extraction::

        from datetime import date

        class Address(BaseModel):
            street: str
            city: str
            zip_code: str

        class Company(BaseModel):
            name: str
            founded: date
            headquarters: Address
            employee_count: int = Field(..., gt=0)

        config = ComplexExtractionAgentConfig(
            extraction_model=Company,
            max_retries=5,  # More retries for complex schema
            temperature=0.1  # Lower temperature for consistency
        )

        agent = ComplexExtractionAgent(config)
        company_data = agent.run(company_description)

See Also:
    - :mod:`haive.agents.document_modifiers.base`: Base document processing
    - :mod:`pydantic`: Schema validation library
    - `JSONPatch RFC 6902 <https://tools.ietf.org/html/rfc6902>`_: JSONPatch specification

Note:
    This module is particularly useful for extracting structured business data,
    parsing forms and reports, and building reliable data pipelines that require
    validation and type safety.
"""
