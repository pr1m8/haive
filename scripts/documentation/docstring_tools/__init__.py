"""Modular docstring and documentation tools for Haive Framework.

This package provides comprehensive docstring analysis, generation, and formatting
using industry-standard tools like pydocstyle, docformatter, interrogate, and vale.

Components:
- coverage: Docstring coverage analysis and reporting
- formatting: Automatic docstring formatting with docformatter
- generation: Google/Sphinx style docstring generation
- validation: PEP 257 compliance checking with pydocstyle
- quality: Vale prose linting for documentation quality
- audit: Comprehensive documentation auditing

Usage:
    from haive.scripts.documentation.docstring_tools import (
        CoverageAnalyzer,
        DocstringFormatter,
        DocstringGenerator,
        ComplianceChecker,
        QualityChecker,
        DocumentationAuditor
    )
"""

from .audit import DocumentationAuditor
from .coverage import CoverageAnalyzer, CoverageReport, DocstringTarget
from .formatting import DocstringFormatter
from .generation import DocstringGenerator
from .quality import QualityChecker
from .validation import ComplianceChecker

__all__ = [
    "CoverageAnalyzer",
    "DocstringTarget",
    "CoverageReport",
    "DocstringFormatter",
    "DocstringGenerator",
    "ComplianceChecker",
    "QualityChecker",
    "DocumentationAuditor",
]
