# haive/core/engine/loaders/scripts/comprehensive_loader_inspector.py

import ast
import importlib
import inspect
import pkgutil
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type

import langchain_community.document_loaders as loaders_pkg


@dataclass
class LoaderProfile:
    """Comprehensive profile of a document loader."""

    name: str
    module_path: str

    # Basic info
    description: str = ""
    base_classes: list[str] = field(default_factory=list)

    # What it loads
    source_types: list[str] = field(default_factory=list)
    file_extensions: list[str] = field(default_factory=list)
    url_patterns: list[str] = field(default_factory=list)

    # How it loads
    load_methods: dict[str, str] = field(
        default_factory=dict
    )  # method_name -> description
    has_scrape_all: bool = False
    has_lazy_load: bool = False
    has_async_load: bool = False

    # Special behaviors
    extraction_logic: str = ""  # Summary of how it extracts content
    special_features: list[str] = field(default_factory=list)

    # Configuration
    init_params: dict[str, Any] = field(default_factory=dict)
    required_params: list[str] = field(default_factory=list)

    # Dependencies
    env_vars: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    external_packages: list[str] = field(default_factory=list)

    # Code snippets
    example_usage: str = ""
    key_methods_code: dict[str, str] = field(default_factory=dict)


class ComprehensiveLoaderInspector:
    """Deep inspection of document loaders."""

    def __init__(self):
        self.profiles: dict[str, LoaderProfile] = {}

        # Patterns
        self.env_var_pattern = re.compile(r"\b([A-Z][A-Z0-9_]+(?:_[A-Z0-9]+)*)\b")
        self.url_pattern = re.compile(r'(https?://[^\s"\']+)')
        self.file_ext_pattern = re.compile(r'\.([a-zA-Z0-9]+)(?:[\s"\']|$)')

    def inspect_all_loaders(self) -> dict[str, LoaderProfile]:
        """Deep inspection of all loaders."""
        for _, module_name, _ in pkgutil.walk_packages(
            loaders_pkg.__path__, loaders_pkg.__name__ + "."
        ):
            try:
                module = importlib.import_module(module_name)
                self._inspect_module(module, module_name)
            except Exception as e:
                passe}")

        return self.profiles

    def _inspect_module(self, module: Any, module_name: str):
        """Inspect a module for loader classes."""
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if self._is_loader_class(obj, name):
                profile = self._create_profile(obj, name, module_name)
                if profile:
                    self.profiles[name] = profile

    def _is_loader_class(self, obj: type, name: str) -> bool:
        """Check if this is a real loader class."""
        return (
            name.endswith("Loader")
            and hasattr(obj, "load")
            and name not in ["BaseLoader", "Loader"]
            and
            # Check it's defined in the module, not imported
            obj.__module__.startswith("langchain")
        )

    def _create_profile(
        self, cls: type, name: str, module_name: str
    ) -> LoaderProfile | None:
        """Create comprehensive profile of a loader."""
        try:
            profile = LoaderProfile(name=name, module_path=module_name)

            # Get base classes
            profile.base_classes = [base.__name__ for base in cls.__bases__]

            # Extract from docstring
            self._extract_from_docstring(cls, profile)

            # Analyze methods
            self._analyze_methods(cls, profile)

            # Extract from source
            self._extract_from_source(cls, profile)

            # Get init parameters
            self._extract_init_params(cls, profile)

            # Infer characteristics
            self._infer_characteristics(profile)

            return profile

        except Exception as e:
            return None

    def _extract_from_docstring(self, cls: type, profile: LoaderProfile):
        """Extract comprehensive info from docstring."""
        docstring = inspect.getdoc(cls) or ""

        # Get description (first paragraph)
        paragraphs = docstring.split("\n\n")
        if paragraphs:
            profile.description = paragraphs[0].replace("\n", " ").strip()

        # Extract example code
        if "Example:" in docstring or ".. code-block::" in docstring:
            # Look for code blocks
            code_blocks = re.findall(
                r"```(?:python)?\n(.*?)\n```", docstring, re.DOTALL
            )
            if not code_blocks:
                # Try doctest format
                code_blocks = re.findall(
                    r".. code-block:: python\n\n(.*?)(?=\n\n|\Z)", docstring, re.DOTALL
                )

            if code_blocks:
                # Clean up indentation
                profile.example_usage = textwrap.dedent(code_blocks[0]).strip()

        # Extract URLs mentioned
        urls = self.url_pattern.findall(docstring)
        profile.url_patterns.extend(urls)

        # Extract file extensions
        extensions = self.file_ext_pattern.findall(docstring)
        profile.file_extensions.extend([f".{ext}" for ext in extensions])

        # Look for special features mentioned
        feature_keywords = [
            "lazy",
            "async",
            "stream",
            "chunk",
            "progress",
            "continue_on_failure",
            "recursive",
            "sitemap",
            "authentication",
            "headers",
            "metadata",
        ]
        for keyword in feature_keywords:
            if keyword in docstring.lower():
                profile.special_features.append(keyword)

    def _analyze_methods(self, cls: type, profile: LoaderProfile):
        """Analyze loader methods to understand behavior."""
        # Get all methods
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        function_methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        all_methods = dict(methods + function_methods)

        # Check for specific methods
        profile.has_lazy_load = "lazy_load" in all_methods
        profile.has_async_load = any(
            name.startswith("a") and name.endswith("load") for name in all_methods
        )
        profile.has_scrape_all = "scrape_all" in all_methods

        # Document key methods
        key_method_names = [
            "load",
            "lazy_load",
            "aload",
            "scrape",
            "scrape_all",
            "_get_elements",
            "parse",
        ]

        for method_name in key_method_names:
            if method_name in all_methods:
                method = all_methods[method_name]
                # Get method signature
                try:
                    sig = inspect.signature(method)
                    profile.load_methods[method_name] = str(sig)

                    # Try to get source code for important methods
                    if method_name in ["load", "scrape", "_get_elements"]:
                        try:
                            source = inspect.getsource(method)
                            # Keep just the important parts
                            lines = source.split("\n")
                            # Remove docstring
                            clean_lines = []
                            in_docstring = False
                            for line in lines:
                                if '"""' in line:
                                    in_docstring = not in_docstring
                                elif not in_docstring:
                                    clean_lines.append(line)

                            profile.key_methods_code[method_name] = "\n".join(
                                clean_lines[:20]
                            )  # First 20 lines
                        except:
                            pass
                except:
                    pass

    def _extract_from_source(self, cls: type, profile: LoaderProfile):
        """Extract detailed info from source code."""
        try:
            source = inspect.getsource(cls)

            # Look for environment variables
            env_vars = set()

            # Multiple patterns for env vars
            patterns = [
                r'os\.environ\[[\'"](.*?)[\'"]\]',
                r'os\.getenv\([\'"](.*?)[\'"]',
                r'get_from_dict_or_env\([^,]+,\s*[\'"](.*?)[\'"]',
                r'get_from_env\([\'"](.*?)[\'"]',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, source)
                env_vars.update(matches)

            # Also look for obvious env var names
            potential_vars = self.env_var_pattern.findall(source)
            env_vars.update(
                [
                    var
                    for var in potential_vars
                    if len(var) > 3
                    and "_" in var
                    and var not in ["TRUE", "FALSE", "NONE", "JSON", "HTML", "PDF"]
                ]
            )

            profile.env_vars = sorted(env_vars)

            # Extract imports
            tree = ast.parse(source)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)

            profile.imports = imports

            # Identify external packages
            external_indicators = {
                "pandas": "pandas",
                "numpy": "numpy",
                "requests": "requests",
                "beautifulsoup": "beautifulsoup4",
                "bs4": "beautifulsoup4",
                "selenium": "selenium",
                "playwright": "playwright",
                "pypdf": "pypdf",
                "PyPDF": "pypdf",
                "pdfminer": "pdfminer.six",
                "pdfplumber": "pdfplumber",
                "docx": "python-docx",
                "openpyxl": "openpyxl",
                "feedparser": "feedparser",
                "newspaper": "newspaper3k",
                "youtube_transcript": "youtube-transcript-api",
                "arxiv": "arxiv",
                "pymupdf": "pymupdf",
                "fitz": "pymupdf",
                "unstructured": "unstructured",
                "boto3": "boto3",
                "google": "google-api-python-client",
                "slack_sdk": "slack-sdk",
                "notion_client": "notion-client",
            }

            for imp in imports:
                for indicator, package in external_indicators.items():
                    if indicator in imp.lower():
                        if package not in profile.external_packages:
                            profile.external_packages.append(package)

            # Analyze extraction logic
            self._analyze_extraction_logic(source, profile)

        except Exception as e:
            pass

    def _analyze_extraction_logic(self, source: str, profile: LoaderProfile):
        """Analyze how the loader extracts content."""
        extraction_hints = []

        # Look for BeautifulSoup usage
        if "BeautifulSoup" in source or "soup" in source:
            extraction_hints.append("Uses BeautifulSoup for HTML parsing")

            # Look for specific extraction patterns
            if "find_all" in source:
                matches = re.findall(r'find_all\(["\'](\w+)', source)
                if matches:
                    extraction_hints.append(f"Extracts {', '.join(set(matches))} tags")

            if "select" in source:
                extraction_hints.append("Uses CSS selectors")

        # Look for PDF extraction
        if "pypdf" in source.lower() or "pdfminer" in source:
            extraction_hints.append("Extracts text from PDFs")
            if "extract_text" in source:
                extraction_hints.append("Uses extract_text method")

        # Look for structured data extraction
        if "json" in source.lower():
            extraction_hints.append("Handles JSON data")
        if "csv" in source.lower() or "pandas" in source:
            extraction_hints.append("Processes CSV/tabular data")

        # Look for special parsing
        if "partition" in source:
            extraction_hints.append("Uses unstructured partitioning")
        if "markdownify" in source:
            extraction_hints.append("Converts to Markdown")

        # Combine into description
        if extraction_hints:
            profile.extraction_logic = "; ".join(extraction_hints)

    def _extract_init_params(self, cls: type, profile: LoaderProfile):
        """Extract initialization parameters."""
        try:
            sig = inspect.signature(cls.__init__)

            for param_name, param in sig.parameters.items():
                if param_name in ["self", "args", "kwargs"]:
                    continue

                param_info = {
                    "type": (
                        str(param.annotation)
                        if param.annotation != inspect.Parameter.empty
                        else "Any"
                    ),
                    "default": (
                        param.default
                        if param.default != inspect.Parameter.empty
                        else None
                    ),
                    "required": param.default == inspect.Parameter.empty,
                }

                profile.init_params[param_name] = param_info

                if param_info["required"]:
                    profile.required_params.append(param_name)

        except Exception:
            pass

    def _infer_characteristics(self, profile: LoaderProfile):
        """Infer source types and characteristics from all gathered info."""
        # Combine all text for analysis
        text = f"{profile.name} {profile.description} {' '.join(profile.base_classes)}".lower()

        # Source type inference
        source_indicators = {
            "PDF": ["pdf"],
            "CSV": ["csv"],
            "EXCEL": ["excel", "xlsx", "xls"],
            "WORD": ["docx", "word"],
            "HTML": ["html", "web"],
            "MARKDOWN": ["markdown", "md"],
            "JSON": ["json"],
            "XML": ["xml"],
            "ARXIV": ["arxiv"],
            "YOUTUBE": ["youtube"],
            "GITHUB": ["github"],
            "URL": ["url", "web"],
            "RSS": ["rss", "feed"],
            "API": ["api"],
            "DATABASE": ["database", "sql"],
        }

        for source_type, indicators in source_indicators.items():
            if any(ind in text for ind in indicators):
                profile.source_types.append(source_type)

        # Add source type based on base class
        if "WebBaseLoader" in profile.base_classes and "URL" not in profile.source_types:
            profile.source_types.append("URL")


def generate_smart_registry(profiles: dict[str, LoaderProfile]) -> str:
    """Generate enhanced registry with detailed loader profiles."""
    lines = [
        "# Auto-generated comprehensive loader registry",
        "# Generated by ComprehensiveLoaderInspector",
        "",
        "from typing import Dict, List, Any, Optional",
        "from pydantic import BaseModel, Field",
        "",
        "",
        "class LoaderProfile(BaseModel):",
        '    """Comprehensive profile of a document loader."""',
        "    name: str",
        "    module_path: str",
        "    description: str = ''",
        "    base_classes: List[str] = Field(default_factory=list)",
        "    source_types: List[str] = Field(default_factory=list)",
        "    file_extensions: List[str] = Field(default_factory=list)",
        "    extraction_logic: str = ''",
        "    special_features: List[str] = Field(default_factory=list)",
        "    required_params: List[str] = Field(default_factory=list)",
        "    env_vars: List[str] = Field(default_factory=list)",
        "    external_packages: List[str] = Field(default_factory=list)",
        "    has_lazy_load: bool = False",
        "    has_async_load: bool = False",
        "    has_scrape_all: bool = False",
        "",
        "",
        "LOADER_PROFILES: Dict[str, LoaderProfile] = {",
    ]

    for name, profile in sorted(profiles.items()):
        lines.append(f'    "{name}": LoaderProfile(')
        lines.append(f'        name="{profile.name}",')
        lines.append(f'        module_path="{profile.module_path}",')
        lines.append(f"        description={profile.description[:200]!r},")

        if profile.base_classes:
            lines.append(f"        base_classes={profile.base_classes},")
        if profile.source_types:
            lines.append(f"        source_types={profile.source_types},")
        if profile.file_extensions:
            lines.append(f"        file_extensions={profile.file_extensions},")
        if profile.extraction_logic:
            lines.append(f"        extraction_logic={profile.extraction_logic!r},")
        if profile.special_features:
            lines.append(f"        special_features={profile.special_features},")
        if profile.required_params:
            lines.append(f"        required_params={profile.required_params},")
        if profile.env_vars:
            lines.append(f"        env_vars={profile.env_vars},")
        if profile.external_packages:
            lines.append(f"        external_packages={profile.external_packages},")
        if profile.has_lazy_load:
            lines.append("        has_lazy_load=True,")
        if profile.has_async_load:
            lines.append("        has_async_load=True,")
        if profile.has_scrape_all:
            lines.append("        has_scrape_all=True,")

        lines.append("    ),")

    lines.append("}")

    return "\n".join(lines)


def main():
    """Run comprehensive inspection."""

    inspector = ComprehensiveLoaderInspector()
    profiles = inspector.inspect_all_loaders()


    # Generate enhanced registry
    registry_code = generate_smart_registry(profiles)

    output_path = Path("./scratches/loader_profiles.py")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(registry_code)


    # Show some interesting stats

    # Loaders with scrape_all
    scrape_all_loaders = [name for name, p in profiles.items() if p.has_scrape_all]
    if scrape_all_loaders:
        pass}")

    # Async loaders
    async_loaders = [name for name, p in profiles.items() if p.has_async_load]
    if async_loaders:
        pass")

    # Loaders with special extraction
    special_extraction = [
        (name, p.extraction_logic)
        for name, p in profiles.items()
        if p.extraction_logic and len(p.extraction_logic) > 50
    ]
    if special_extraction:
        for name, logic in special_extraction[:5]:
            pass


if __name__ == "__main__":
    main()
