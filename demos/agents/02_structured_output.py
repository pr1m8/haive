"""Demo 02: SimpleAgent with Structured Output.

Tests: structured output via Pydantic model
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent


class CityInfo(BaseModel):
    """Structured output for city information."""
    name: str = Field(description="City name")
    country: str = Field(description="Country the city is in")
    population_estimate: str = Field(description="Approximate population")
    famous_for: list[str] = Field(description="What the city is famous for (2-3 items)")


async def main():
    print("=" * 60)
    print("Demo 02: SimpleAgent + Structured Output")
    print("=" * 60)

    config = AugLLMConfig(
        temperature=0.3,
        system_message="You extract city information into structured format.",
        structured_output_model=CityInfo,
    )

    agent = SimpleAgent(name="structured_demo", engine=config)
    print(f"[OK] Instantiated: {agent.name}")
    print(f"[OK] Structured output model: {config.structured_output_model}")

    print("\n--- Running arun ---")
    result = await agent.arun("Tell me about Tokyo, Japan.")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    print("\n[OK] Structured output demo complete")


if __name__ == "__main__":
    asyncio.run(main())
