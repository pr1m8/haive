# output_parser_analysis.py

from dataclasses import dataclass  # This is built-in for Python 3.7+
import inspect
import json
import sys
from typing import Any, Dict, List, Optional, Type


# Try to import langchain
try:
    import langchain.output_parsers as lc_parsers

    HAS_LANGCHAIN = True
except ImportError:
    lc_parsers = None
    HAS_LANGCHAIN = False


@dataclass
class ParserInfo:
    name: str
    module: str
    docstring: str | None
    base_classes: list[str]
    methods: list[str]
    parse_signature: str | None = None
    parse_docstring: str | None = None


def analyze_parser_class(cls: type) -> ParserInfo:
    """Extract basic information about a parser class."""
    # Get base classes
    base_classes = [base.__name__ for base in cls.__bases__]

    # Get methods
    methods = []
    parse_signature = None
    parse_docstring = None

    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Skip private methods except __init__
        if name.startswith("_") and name != "__init__":
            continue

        methods.append(name)

        # Store details about the parse method
        if name == "parse":
            try:
                parse_signature = str(inspect.signature(method))
                parse_docstring = inspect.getdoc(method)
            except Exception:
                pass

    return ParserInfo(
        name=cls.__name__,
        module=cls.__module__,
        docstring=inspect.getdoc(cls),
        base_classes=base_classes,
        methods=methods,
        parse_signature=parse_signature,
        parse_docstring=parse_docstring,
    )


def analyze_output_parsers():
    """Analyze available output parser classes."""
    parser_infos = {}

    # Only process langchain parsers if available
    if HAS_LANGCHAIN:
        for name, obj in inspect.getmembers(lc_parsers):
            if inspect.isclass(obj) and (
                "OutputParser" in name
                or any("OutputParser" in base.__name__ for base in obj.__mro__)
            ):
                try:
                    parser_infos[name] = analyze_parser_class(obj)
                except Exception:
                    pass

    return parser_infos


def generate_report(parsers: dict[str, ParserInfo]):
    """Generate a report on the output parsers."""
    # Find common interfaces
    method_counts = {}
    for info in parsers.values():
        for method in info.methods:
            method_counts[method] = method_counts.get(method, 0) + 1

    common_methods = {m: c for m, c in method_counts.items() if c > 1}
    sorted_methods = sorted(common_methods.items(), key=lambda x: x[1], reverse=True)

    for method, count in sorted_methods[:10]:  # Top 10 methods
        (count / len(parsers)) * 100

    # Check for parse method
    [name for name, info in parsers.items() if "parse" in info.methods]

    # Display some key parser details
    key_parsers = [
        "BaseOutputParser",
        "StrOutputParser",
        "ListOutputParser",
        "PydanticOutputParser",
        "JsonOutputParser",
    ]

    for name in key_parsers:
        if name in parsers:
            info = parsers[name]
            if info.parse_signature:
                pass
            if info.parse_docstring:
                info.parse_docstring.split("\n")[0]

    # Save to JSON file
    with open("parser_analysis.json", "w") as f:
        json.dump(
            {
                name: {
                    "name": info.name,
                    "module": info.module,
                    "base_classes": info.base_classes,
                    "methods": info.methods,
                    "parse_signature": info.parse_signature,
                    "docstring": info.docstring,
                }
                for name, info in parsers.items()
            },
            f,
            indent=2,
        )


if __name__ == "__main__":

    if not HAS_LANGCHAIN:
        sys.exit(1)

    parsers = analyze_output_parsers()

    if not parsers:
        sys.exit(1)

    generate_report(parsers)
