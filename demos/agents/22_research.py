"""Demo 22: Research Agents.

Tests: OpenPerplexity, Person, STORM pipeline
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 22: Research Agents")
    print("=" * 60)

    research_modules = [
        ("open_perplexity", "haive.agents.research.open_perplexity.agent"),
        ("person", "haive.agents.research.person.agent"),
        ("storm/wiki_writer", "haive.agents.research.storm.wiki_writer.agent"),
        ("storm/perspectives", "haive.agents.research.storm.generate_perspectives.agent"),
        ("storm/outline_gen", "haive.agents.research.storm.outline_generator.agent"),
        ("storm/outline_ref", "haive.agents.research.storm.outline_refiner.agent"),
        ("storm/topics", "haive.agents.research.storm.related_topics_generator.agent"),
        ("storm/section", "haive.agents.research.storm.section_writer.agent"),
    ]

    ok = broken = 0
    for name, module_path in research_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c or "Writer" in c or "Generator" in c]
            print(f"  [OK] {name:<25} {[c for c in classes if not c.startswith('_')][:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<25} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  Research agents: {ok}/{ok+broken} OK")
    print("\n[OK] Research agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
