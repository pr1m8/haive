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

from __future__ import annotations

from scripts.documentation.docstring_tools.audit import DocumentationAuditor
from scripts.documentation.docstring_tools.coverage import CoverageAnalyzer
from scripts.documentation.docstring_tools.coverage import CoverageReport
from scripts.documentation.docstring_tools.coverage import DocstringTarget
from scripts.documentation.docstring_tools.formatting import DocstringFormatter
from scripts.documentation.docstring_tools.generation import DocstringGenerator
from scripts.documentation.docstring_tools.quality import QualityChecker
from scripts.documentation.docstring_tools.validation import ComplianceChecker

__all__ = [
    "ComplianceChecker",
    "CoverageAnalyzer",
    "CoverageReport",
    "DocstringFormatter",
    "DocstringGenerator",
    "DocstringTarget",
    "DocumentationAuditor",
    "QualityChecker",
]
