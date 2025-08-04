#!/usr/bin/env python3
"""Compare current nitpick_ignore with comprehensive list and generate
update."""
from __future__ import annotations

from pathlib import Path

# Current nitpick_ignore from conf.py
CURRENT_NITPICK_IGNORE = [
    # Basic Python types that don't need cross-references
    ("py:class", "str"),
    ("py:class", "int"),
    ("py:class", "bool"),
    ("py:class", "float"),
    ("py:class", "list"),
    ("py:class", "dict"),
    ("py:class", "tuple"),
    ("py:class", "set"),
    ("py:class", "bytes"),
    ("py:class", "None"),
    ("py:class", "type"),
    ("py:class", "object"),
    # Common typing module types
    ("py:class", "Any"),
    ("py:class", "List"),
    ("py:class", "Dict"),
    ("py:class", "Tuple"),
    ("py:class", "Set"),
    ("py:class", "Optional"),
    ("py:class", "Union"),
    ("py:class", "Callable"),
    ("py:class", "Type"),
    ("py:class", "TypeVar"),
    ("py:class", "Generic"),
    ("py:class", "Literal"),
    ("py:class", "Protocol"),
    ("py:class", "TypedDict"),
    # Pydantic types
    ("py:class", "BaseModel"),
    ("py:class", "Field"),
    ("py:class", "SecretStr"),
    ("py:class", "ConfigDict"),
    # datetime types
    ("py:class", "datetime.datetime"),
    ("py:class", "datetime.date"),
    ("py:class", "datetime.time"),
    ("py:class", "datetime.timedelta"),
    # Common missing classes
    ("py:class", "Document"),
    ("py:class", "BaseMessage"),
    ("py:class", "HumanMessage"),
    ("py:class", "AIMessage"),
    ("py:class", "SystemMessage"),
    ("py:class", "ToolMessage"),
    # Ignore some specific references that are causing issues
    ("py:class", "T"),
    ("py:class", "Agent"),
    ("py:class", "TIn"),
    ("py:class", "TOut"),
    ("py:class", "InvokableEngine"),
]


# Read the comprehensive list
def load_comprehensive_list():
    """Load the comprehensive list from the generated file."""
    from expanded_nitpick_ignore import EXPANDED_NITPICK_IGNORE

    return EXPANDED_NITPICK_IGNORE


def compare_lists():
    """Compare current vs comprehensive lists."""

    current_set = set(CURRENT_NITPICK_IGNORE)
    comprehensive_set = set(load_comprehensive_list())

    # Find additions needed
    additions = comprehensive_set - current_set

    # Find redundant entries (unlikely but possible)
    redundant = current_set - comprehensive_set

    print(f"Current list: {len(current_set)} entries")
    print(f"Comprehensive list: {len(comprehensive_set)} entries")
    print(f"New additions needed: {len(additions)}")
    print(f"Potentially redundant: {len(redundant)}")

    return additions, redundant


def categorize_additions(additions):
    """Categorize the additions by type and domain."""

    categories = {
        "Basic Python Types": [],
        "Advanced Typing": [],
        "Collections & Async": [],
        "Pydantic Enhancements": [],
        "LangChain Core": [],
        "LangGraph": [],
        "External Libraries": [],
        "Generic Types": [],
        "Methods & Functions": [],
        "Modules & Exceptions": [],
    }

    for ref_type, target in sorted(additions):
        if ref_type == "py:class":
            if target in [
                "frozenset",
                "bytearray",
                "slice",
                "range",
                "enumerate",
                "zip",
                "filter",
                "map",
            ]:
                categories["Basic Python Types"].append((ref_type, target))
            elif any(
                x in target
                for x in [
                    "typing_extensions",
                    "Iterator",
                    "Iterable",
                    "Generator",
                    "Async",
                    "Awaitable",
                    "Coroutine",
                ]
            ):
                categories["Advanced Typing"].append((ref_type, target))
            elif any(x in target for x in ["collections", "asyncio", "pathlib"]):
                categories["Collections & Async"].append((ref_type, target))
            elif "pydantic" in target or target in [
                "ValidationError",
                "EmailStr",
                "HttpUrl",
                "PositiveInt",
                "StrictStr",
                "constr",
                "UUID1",
            ]:
                categories["Pydantic Enhancements"].append((ref_type, target))
            elif "langchain" in target and "langgraph" not in target:
                categories["LangChain Core"].append((ref_type, target))
            elif "langgraph" in target:
                categories["LangGraph"].append((ref_type, target))
            elif any(
                x in target
                for x in [
                    "numpy",
                    "pandas",
                    "requests",
                    "httpx",
                    "fastapi",
                    "uuid",
                    "decimal",
                    "enum",
                    "logging",
                    "threading",
                ]
            ):
                categories["External Libraries"].append((ref_type, target))
            elif len(target) <= 3 and (
                target.isupper() or target.startswith("~") or target.startswith("_")
            ):
                categories["Generic Types"].append((ref_type, target))
            else:
                categories["External Libraries"].append((ref_type, target))  # Default
        else:
            categories["Methods & Functions"].append((ref_type, target))

    return categories


def generate_incremental_update(additions):
    """Generate an incremental update to add to existing conf.py."""

    categories = categorize_additions(additions)

    lines = ["# INCREMENTAL ADDITIONS TO NITPICK_IGNORE"]
    lines.append("# Add these entries to your existing nitpick_ignore list in conf.py")
    lines.append("")

    for category, items in categories.items():
        if not items:
            continue

        lines.append(f"    # === {category.upper()} ===")
        for ref_type, target in sorted(items):
            lines.append(f'    ("{ref_type}", "{target}"),')
        lines.append("")

    return "\n".join(lines)


def generate_prioritized_update():
    """Generate a prioritized list of most important additions."""

    additions, _ = compare_lists()

    # High priority additions (most common causes of warnings)
    high_priority = []
    medium_priority = []
    low_priority = []

    for ref_type, target in additions:
        # High priority: Common LangChain/Pydantic types
        if any(
            x in target.lower()
            for x in [
                "langchain",
                "pydantic",
                "typing_extensions",
                "basemodel",
                "document",
                "message",
            ]
        ):
            high_priority.append((ref_type, target))
        # Medium priority: Python standard library
        elif any(
            x in target.lower()
            for x in ["collections", "asyncio", "datetime", "pathlib", "enum"]
        ):
            medium_priority.append((ref_type, target))
        else:
            low_priority.append((ref_type, target))

    output = []

    if high_priority:
        output.append("# HIGH PRIORITY - Most likely to reduce warnings")
        for ref_type, target in sorted(high_priority)[:20]:  # Top 20
            output.append(f'    ("{ref_type}", "{target}"),')
        output.append("")

    if medium_priority:
        output.append("# MEDIUM PRIORITY - Standard library types")
        for ref_type, target in sorted(medium_priority)[:15]:  # Top 15
            output.append(f'    ("{ref_type}", "{target}"),')
        output.append("")

    if low_priority and len(low_priority) <= 10:
        output.append("# LOW PRIORITY - Less common types")
        for ref_type, target in sorted(low_priority):
            output.append(f'    ("{ref_type}", "{target}"),')

    return "\n".join(output)


def main():
    """Main function."""

    print("=== Nitpick Ignore Analysis ===\n")

    additions, redundant = compare_lists()

    if redundant:
        print("⚠️  Potentially redundant entries in current config:")
        for ref_type, target in sorted(redundant):
            print(f"  {ref_type}: {target}")
        print()

    if not additions:
        print("✅ Your current nitpick_ignore list is comprehensive!")
        return

    # Generate categorized analysis
    categories = categorize_additions(additions)

    print("📊 Analysis of missing entries by category:")
    for category, items in categories.items():
        if items:
            print(f"  {category}: {len(items)} items")
    print()

    # Save different output formats
    incremental_update = generate_incremental_update(additions)
    Path("nitpick_ignore_incremental_additions.txt").write_text(incremental_update)

    prioritized_update = generate_prioritized_update()
    Path("nitpick_ignore_priority_additions.txt").write_text(prioritized_update)

    print("📁 Files generated:")
    print("  - nitpick_ignore_incremental_additions.txt (full categorized list)")
    print("  - nitpick_ignore_priority_additions.txt (prioritized essentials)")
    print()

    print("🚀 Quick start recommendation:")
    print("  1. Add the HIGH PRIORITY items first")
    print("  2. Test your documentation build")
    print("  3. Add MEDIUM PRIORITY items if needed")
    print("  4. Add remaining items as warnings appear")
    print()

    # Show sample of high priority items
    print("📝 Top 10 high priority additions:")
    lines = prioritized_update.split("\n")
    for line in lines[1:11]:  # Skip header, show first 10
        if line.strip() and not line.startswith("#"):
            print(f"  {line}")


if __name__ == "__main__":
    main()
