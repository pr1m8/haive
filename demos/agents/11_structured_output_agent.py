"""Demo 11: StructuredOutputAgent.

Tests: Dedicated structured output extraction agent
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.structured.agent import StructuredOutputAgent


class MovieReview(BaseModel):
    """Structured movie review."""
    title: str = Field(description="Movie title")
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    genre: str = Field(description="Primary genre")
    summary: str = Field(description="One-sentence summary")


async def main():
    print("=" * 60)
    print("Demo 11: StructuredOutputAgent")
    print("=" * 60)

    agent = StructuredOutputAgent(
        name="review_extractor",
        engine=AugLLMConfig(temperature=0.1),
        structured_output_model=MovieReview,
        output_model=MovieReview,
    )
    print(f"[OK] Instantiated: {agent.name}")

    print("\n--- Running arun ---")
    try:
        result = await agent.arun(
            "The Matrix (1999) is a groundbreaking sci-fi film. It's an incredible "
            "action movie with philosophical themes about reality. I'd give it a 9 out of 10."
        )
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        print("\n[OK] StructuredOutputAgent demo complete")
    except Exception as e:
        print(f"[BROKEN] arun failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
