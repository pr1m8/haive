# output_parser_analysis.py

import inspect
import json
import sys
from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass  # This is built-in for Python 3.7+

# Try to import langchain
try:
    import langchain.output_parsers as lc_parsers
    HAS_LANGCHAIN = True
except ImportError:
    lc_parsers = None
    HAS_LANGCHAIN = False
    print("Warning: langchain package not found")


@dataclass
class ParserInfo:
    name: str
    module: str
    docstring: Optional[str]
    base_classes: List[str]
    methods: List[str]
    parse_signature: Optional[str] = None
    parse_docstring: Optional[str] = None


def analyze_parser_class(cls: Type) -> ParserInfo:
    """Extract basic information about a parser class."""
    # Get base classes
    base_classes = [base.__name__ for base in cls.__bases__]
    
    # Get methods
    methods = []
    parse_signature = None
    parse_docstring = None
    
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Skip private methods except __init__
        if name.startswith('_') and name != '__init__':
            continue
            
        methods.append(name)
        
        # Store details about the parse method
        if name == 'parse':
            try:
                parse_signature = str(inspect.signature(method))
                parse_docstring = inspect.getdoc(method)
            except Exception as e:
                print(f"Error getting parse signature for {cls.__name__}: {e}")
    
    return ParserInfo(
        name=cls.__name__,
        module=cls.__module__,
        docstring=inspect.getdoc(cls),
        base_classes=base_classes,
        methods=methods,
        parse_signature=parse_signature,
        parse_docstring=parse_docstring
    )


def analyze_output_parsers():
    """Analyze available output parser classes."""
    parser_infos = {}
    
    # Only process langchain parsers if available
    if HAS_LANGCHAIN:
        print("Analyzing langchain output parsers...")
        for name, obj in inspect.getmembers(lc_parsers):
            if inspect.isclass(obj) and (
                'OutputParser' in name or 
                any('OutputParser' in base.__name__ for base in obj.__mro__)
            ):
                try:
                    parser_infos[name] = analyze_parser_class(obj)
                    print(f"Processed: {name}")
                except Exception as e:
                    print(f"Error processing {name}: {e}")
    
    return parser_infos


def generate_report(parsers: Dict[str, ParserInfo]):
    """Generate a report on the output parsers."""
    print(f"\n==== Output Parser Analysis Report ====")
    print(f"Found {len(parsers)} output parser classes")
    
    # Find common interfaces
    method_counts = {}
    for info in parsers.values():
        for method in info.methods:
            method_counts[method] = method_counts.get(method, 0) + 1
    
    common_methods = {m: c for m, c in method_counts.items() if c > 1}
    sorted_methods = sorted(common_methods.items(), key=lambda x: x[1], reverse=True)
    
    print("\n== Common Methods ==")
    for method, count in sorted_methods[:10]:  # Top 10 methods
        percentage = (count / len(parsers)) * 100
        print(f"{method}: {count} parsers ({percentage:.1f}%)")
    
    # Check for parse method
    parsers_with_parse = [name for name, info in parsers.items() if 'parse' in info.methods]
    print(f"\n{len(parsers_with_parse)} parsers implement 'parse' method ({(len(parsers_with_parse)/len(parsers))*100:.1f}%)")
    
    # Display some key parser details
    print("\n== Key Parser Details ==")
    key_parsers = [
        "BaseOutputParser", "StrOutputParser", "ListOutputParser", 
        "PydanticOutputParser", "JsonOutputParser"
    ]
    
    for name in key_parsers:
        if name in parsers:
            info = parsers[name]
            print(f"\n{name} ({info.module})")
            if info.parse_signature:
                print(f"  parse{info.parse_signature}")
            if info.parse_docstring:
                first_line = info.parse_docstring.split('\n')[0]
                print(f"  Doc: {first_line}")
    
    # Save to JSON file
    with open('parser_analysis.json', 'w') as f:
        json.dump(
            {name: {
                "name": info.name,
                "module": info.module,
                "base_classes": info.base_classes,
                "methods": info.methods,
                "parse_signature": info.parse_signature,
                "docstring": info.docstring
            } for name, info in parsers.items()},
            f, 
            indent=2
        )
    print(f"\nDetailed analysis saved to parser_analysis.json")


if __name__ == "__main__":
    print("Starting output parser analysis...")
    
    if not HAS_LANGCHAIN:
        print("Error: langchain package not found. Please install it.")
        sys.exit(1)
    
    parsers = analyze_output_parsers()
    
    if not parsers:
        print("No parser classes found.")
        sys.exit(1)
    
    generate_report(parsers)