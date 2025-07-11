# Example usage

from langchain_core.messages import HumanMessage

from haive.agents.document_modifiers.complex_extraction.factory import (
    create_complex_extraction_agent,
)

if __name__ == "__main__":
    from pydantic import BaseModel, Field

    # Define an extraction model
    class PersonInfo(BaseModel):
        name: str = Field(description="The person's full name")
        age: int = Field(description="The person's age in years")
        occupation: str | None = Field(
            default=None, description="The person's job or profession"
        )

    # Create the agent
    agent = create_complex_extraction_agent(
        extraction_model=PersonInfo,
        system_prompt="Extract person information from the provided text.",
        model="gpt-4o",
        max_retries=3,
        parse_pydantic=True,  # Enable Pydantic object parsing
    )

    # Run extraction
    result = agent.run(
        {
            "messages": [
                HumanMessage(
                    content="John Smith is a 42-year-old software developer living in New York."
                )
            ]
        },
        debug=True,
    )

    # Print the extracted data
    extracted_data = result.get("extracted_data", {})
