#!/usr/bin/env python3
"""Refined Documentation Analyzer - Advanced issue detection and categorization.

This script provides sophisticated analysis of documentation issues with
detailed categorization, quality scoring, and intelligent prioritization.
"""

import ast
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path
import re
from typing import Any

import click


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IssueSeverity(Enum):
    """Issue severity levels."""

    CRITICAL = "critical"  # Blocks functionality/builds
    HIGH = "high"  # Major impact on usability
    MEDIUM = "medium"  # Moderate improvement
    LOW = "low"  # Nice to have
    INFO = "info"  # Informational only


class IssueCategory(Enum):
    """Refined issue categories."""

    # Docstring issues
    DOCSTRING_MISSING = "docstring_missing"
    DOCSTRING_EMPTY = "docstring_empty"
    DOCSTRING_POOR_QUALITY = "docstring_poor_quality"
    DOCSTRING_WRONG_STYLE = "docstring_wrong_style"
    DOCSTRING_INCOMPLETE = "docstring_incomplete"

    # Type hint issues
    TYPE_MISSING_RETURN = "type_missing_return"
    TYPE_MISSING_PARAMS = "type_missing_params"
    TYPE_USING_ANY = "type_using_any"
    TYPE_INCONSISTENT = "type_inconsistent"
    TYPE_OUTDATED_SYNTAX = "type_outdated_syntax"

    # Code quality
    CODE_COMPLEXITY_HIGH = "code_complexity_high"
    CODE_LINE_TOO_LONG = "code_line_too_long"
    CODE_NAMING_POOR = "code_naming_poor"
    CODE_STRUCTURE_POOR = "code_structure_poor"

    # Import issues
    IMPORT_UNUSED = "import_unused"
    IMPORT_STAR = "import_star"
    IMPORT_CIRCULAR = "import_circular"
    IMPORT_RELATIVE_EXTERNAL = "import_relative_external"

    # Documentation structure
    DOC_MISSING_EXAMPLES = "doc_missing_examples"
    DOC_MISSING_RAISES = "doc_missing_raises"
    DOC_MISSING_RETURNS = "doc_missing_returns"
    DOC_MISSING_ARGS = "doc_missing_args"

    # API design
    API_INCONSISTENT_NAMING = "api_inconsistent_naming"
    API_MISSING_ERROR_HANDLING = "api_missing_error_handling"
    API_POOR_INTERFACE = "api_poor_interface"


@dataclass
class RefinedIssue:
    """Represents a refined documentation/code quality issue."""

    id: str
    file_path: str
    line_number: int
    category: IssueCategory
    severity: IssueSeverity
    title: str
    description: str
    context: str  # Code snippet showing the issue

    # Quality metrics
    complexity_score: float = 0.0  # 0-10 scale
    maintainability_impact: float = 0.0  # 0-10 scale
    user_impact: float = 0.0  # 0-10 scale

    # Fix information
    auto_fixable: bool = False
    fix_confidence: float = 0.0  # 0-1 scale
    fix_tools: list[str] = field(default_factory=list)
    fix_effort_minutes: int = 0
    fix_suggestion: str = ""

    # Dependencies and relationships
    related_issues: list[str] = field(default_factory=list)
    blocks_issues: list[str] = field(default_factory=list)

    # Metadata
    detected_by: str = ""
    created_at: str = ""
    priority_score: float = 0.0  # Calculated composite score


class RefinedDocumentationAnalyzer:
    """Advanced documentation and code quality analyzer."""

    def __init__(self, root_path: str = "packages/"):
        self.root_path = Path(root_path)
        self.issues: list[RefinedIssue] = []
        self.file_metrics: dict[str, dict[str, Any]] = {}

        # Patterns for different issues
        self.google_docstring_sections = {
            "Args:",
            "Arguments:",
            "Parameters:",
            "Returns:",
            "Return:",
            "Yields:",
            "Yield:",
            "Raises:",
            "Except:",
            "Exceptions:",
            "Example:",
            "Examples:",
            "Note:",
            "Notes:",
            "See Also:",
            "References:",
            "Todo:",
        }

        # Common poor naming patterns
        self.poor_naming_patterns = [
            r"^[a-z]$",  # Single letter variables (except in loops)
            r"^temp\d*$",  # temp, temp1, temp2, etc.
            r"^data\d*$",  # data, data1, data2, etc.
            r"^var\d*$",  # var, var1, var2, etc.
            r"^[a-z]+\d+$",  # variable1, item2, etc.
            r"^(foo|bar|baz|qux)$",  # Placeholder names
        ]

        # Type hint patterns
        self.outdated_type_patterns = [
            r"typing\.List\[",
            r"typing\.Dict\[",
            r"typing\.Tuple\[",
            r"typing\.Set\[",
            r"typing\.Optional\[",
            r"typing\.Union\[",
        ]

    def analyze_file(self, file_path: Path) -> list[RefinedIssue]:
        """Analyze a single Python file comprehensively."""
        if self._should_skip_file(file_path):
            return []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            tree = ast.parse(content)

        except Exception as e:
            logger.warning(f"Could not parse {file_path}: {e}")
            return []

        file_issues = []

        # Calculate file-level metrics
        self.file_metrics[str(file_path)] = self._calculate_file_metrics(content, tree)

        # Analyze different aspects
        file_issues.extend(self._analyze_docstrings(file_path, content, lines, tree))
        file_issues.extend(self._analyze_type_hints(file_path, content, lines, tree))
        file_issues.extend(self._analyze_code_quality(file_path, content, lines, tree))
        file_issues.extend(self._analyze_imports(file_path, content, lines, tree))
        file_issues.extend(self._analyze_api_design(file_path, content, lines, tree))

        # Calculate priority scores
        for issue in file_issues:
            issue.priority_score = self._calculate_priority_score(issue)

        return file_issues

    def _calculate_file_metrics(self, content: str, tree: ast.AST) -> dict[str, Any]:
        """Calculate comprehensive file metrics."""
        lines = content.splitlines()

        metrics = {
            "lines_of_code": len(
                [l for l in lines if l.strip() and not l.strip().startswith("#")]
            ),
            "total_lines": len(lines),
            "comment_lines": len([l for l in lines if l.strip().startswith("#")]),
            "docstring_lines": 0,
            "complexity_score": 0,
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "has_module_docstring": bool(ast.get_docstring(tree)),
        }

        # Count AST elements
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["function_count"] += 1
                metrics["complexity_score"] += self._calculate_complexity(node)
            elif isinstance(node, ast.ClassDef):
                metrics["class_count"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics["import_count"] += 1
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                # Potential docstring
                if len(node.value.splitlines()) > 1:
                    metrics["docstring_lines"] += len(node.value.splitlines())

        # Calculate quality scores
        metrics["documentation_ratio"] = metrics["docstring_lines"] / max(
            metrics["lines_of_code"], 1
        )
        metrics["complexity_per_function"] = metrics["complexity_score"] / max(
            metrics["function_count"], 1
        )

        return metrics

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if (
                isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor))
                or isinstance(child, ast.ExceptHandler)
                or isinstance(child, (ast.And, ast.Or))
            ):
                complexity += 1

        return complexity

    def _analyze_docstrings(
        self, file_path: Path, content: str, lines: list[str], tree: ast.AST
    ) -> list[RefinedIssue]:
        """Analyze docstring quality comprehensively."""
        issues = []

        # Module docstring
        module_docstring = ast.get_docstring(tree)
        if not module_docstring:
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_module_docstring",
                    file_path=str(file_path),
                    line_number=1,
                    category=IssueCategory.DOCSTRING_MISSING,
                    severity=(
                        IssueSeverity.HIGH
                        if self._is_public_module(file_path)
                        else IssueSeverity.MEDIUM
                    ),
                    title="Missing module docstring",
                    description=f"Module {file_path.name} lacks a descriptive docstring",
                    context=f"# File: {file_path.name}\n# No module docstring found",
                    auto_fixable=True,
                    fix_confidence=0.7,
                    fix_tools=["pydocstring", "ai_tools"],
                    fix_effort_minutes=10,
                    fix_suggestion="Add comprehensive module docstring with purpose, usage, and examples",
                    user_impact=7.0,
                    maintainability_impact=8.0,
                    detected_by="docstring_analyzer",
                )
            )
        elif len(module_docstring.strip()) < 50:
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_module_docstring_short",
                    file_path=str(file_path),
                    line_number=1,
                    category=IssueCategory.DOCSTRING_POOR_QUALITY,
                    severity=IssueSeverity.MEDIUM,
                    title="Module docstring too brief",
                    description=f"Module docstring is only {len(module_docstring)} characters",
                    context=f'"""{module_docstring}"""',
                    auto_fixable=True,
                    fix_confidence=0.6,
                    fix_tools=["ai_tools"],
                    fix_effort_minutes=15,
                    fix_suggestion="Expand docstring with detailed description, examples, and usage patterns",
                    user_impact=5.0,
                    maintainability_impact=6.0,
                    detected_by="docstring_analyzer",
                )
            )

        # Function and class docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                issues.extend(self._analyze_function_docstring(file_path, node, lines))
            elif isinstance(node, ast.ClassDef):
                issues.extend(self._analyze_class_docstring(file_path, node, lines))

        return issues

    def _analyze_function_docstring(
        self, file_path: Path, node: ast.FunctionDef, lines: list[str]
    ) -> list[RefinedIssue]:
        """Analyze function docstring quality."""
        issues = []

        is_public = not node.name.startswith("_")
        is_complex = self._calculate_complexity(node) > 5
        has_params = bool(node.args.args)
        has_return = bool(node.returns) or any(
            isinstance(n, ast.Return) and n.value for n in ast.walk(node)
        )

        docstring = ast.get_docstring(node)

        if not docstring:
            severity = IssueSeverity.HIGH if is_public else IssueSeverity.MEDIUM
            if is_complex:
                severity = IssueSeverity.CRITICAL

            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{node.name}_missing_docstring",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    category=IssueCategory.DOCSTRING_MISSING,
                    severity=severity,
                    title=f"Function '{node.name}' missing docstring",
                    description=f"{'Public' if is_public else 'Private'} function with complexity {self._calculate_complexity(node)}",
                    context=self._get_function_signature(node, lines),
                    auto_fixable=True,
                    fix_confidence=0.8,
                    fix_tools=["pydocstring", "ai_tools"],
                    fix_effort_minutes=5 if not is_complex else 15,
                    fix_suggestion="Add Google-style docstring with Args, Returns, and Examples sections",
                    complexity_score=self._calculate_complexity(node),
                    user_impact=8.0 if is_public else 4.0,
                    maintainability_impact=9.0,
                    detected_by="docstring_analyzer",
                )
            )
        else:
            # Analyze docstring quality
            quality_issues = self._analyze_docstring_quality(
                file_path,
                node.name,
                node.lineno,
                docstring,
                has_params,
                has_return,
                is_public,
            )
            issues.extend(quality_issues)

        return issues

    def _analyze_class_docstring(
        self, file_path: Path, node: ast.ClassDef, lines: list[str]
    ) -> list[RefinedIssue]:
        """Analyze class docstring quality."""
        issues = []

        is_public = not node.name.startswith("_")
        method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])

        docstring = ast.get_docstring(node)

        if not docstring:
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{node.name}_missing_docstring",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    category=IssueCategory.DOCSTRING_MISSING,
                    severity=IssueSeverity.HIGH if is_public else IssueSeverity.MEDIUM,
                    title=f"Class '{node.name}' missing docstring",
                    description=f"{'Public' if is_public else 'Private'} class with {method_count} methods",
                    context=f"class {node.name}({', '.join(base.id for base in node.bases if isinstance(base, ast.Name))}):",
                    auto_fixable=True,
                    fix_confidence=0.7,
                    fix_tools=["pydocstring", "ai_tools"],
                    fix_effort_minutes=10,
                    fix_suggestion="Add class docstring with purpose, attributes, and usage examples",
                    user_impact=8.0 if is_public else 3.0,
                    maintainability_impact=8.0,
                    detected_by="docstring_analyzer",
                )
            )
        else:
            # Analyze class docstring quality
            quality_issues = self._analyze_docstring_quality(
                file_path,
                node.name,
                node.lineno,
                docstring,
                method_count > 0,
                True,
                is_public,
                is_class=True,
            )
            issues.extend(quality_issues)

        return issues

    def _analyze_docstring_quality(
        self,
        file_path: Path,
        name: str,
        line_no: int,
        docstring: str,
        has_params: bool,
        has_return: bool,
        is_public: bool,
        is_class: bool = False,
    ) -> list[RefinedIssue]:
        """Analyze the quality of an existing docstring."""
        issues = []

        # Check for Google style
        has_google_sections = any(
            section in docstring for section in self.google_docstring_sections
        )

        if not has_google_sections and (has_params or has_return):
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{name}_wrong_style",
                    file_path=str(file_path),
                    line_number=line_no,
                    category=IssueCategory.DOCSTRING_WRONG_STYLE,
                    severity=IssueSeverity.MEDIUM,
                    title="Docstring not in Google style",
                    description="Missing structured sections (Args:, Returns:, etc.)",
                    context=(
                        docstring[:200] + "..." if len(docstring) > 200 else docstring
                    ),
                    auto_fixable=True,
                    fix_confidence=0.6,
                    fix_tools=["docformatter", "ai_tools"],
                    fix_effort_minutes=8,
                    fix_suggestion="Convert to Google-style with proper sections",
                    user_impact=4.0,
                    maintainability_impact=6.0,
                    detected_by="docstring_analyzer",
                )
            )

        # Check for missing sections
        if has_params and not any(
            section in docstring for section in ["Args:", "Arguments:", "Parameters:"]
        ):
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{name}_missing_args",
                    file_path=str(file_path),
                    line_number=line_no,
                    category=IssueCategory.DOC_MISSING_ARGS,
                    severity=IssueSeverity.MEDIUM,
                    title="Missing Args section",
                    description="Function has parameters but no Args documentation",
                    context=docstring[:100],
                    auto_fixable=True,
                    fix_confidence=0.7,
                    fix_tools=["ai_tools"],
                    fix_effort_minutes=10,
                    fix_suggestion="Add Args: section documenting all parameters",
                    user_impact=6.0,
                    maintainability_impact=7.0,
                    detected_by="docstring_analyzer",
                )
            )

        if has_return and not any(
            section in docstring
            for section in ["Returns:", "Return:", "Yields:", "Yield:"]
        ):
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{name}_missing_returns",
                    file_path=str(file_path),
                    line_number=line_no,
                    category=IssueCategory.DOC_MISSING_RETURNS,
                    severity=IssueSeverity.MEDIUM,
                    title="Missing Returns section",
                    description="Function returns value but no Returns documentation",
                    context=docstring[:100],
                    auto_fixable=True,
                    fix_confidence=0.7,
                    fix_tools=["ai_tools"],
                    fix_effort_minutes=5,
                    fix_suggestion="Add Returns: section describing return value",
                    user_impact=6.0,
                    maintainability_impact=7.0,
                    detected_by="docstring_analyzer",
                )
            )

        # Check for examples in public APIs
        if is_public and not any(
            section in docstring for section in ["Example:", "Examples:"]
        ):
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{name}_missing_examples",
                    file_path=str(file_path),
                    line_number=line_no,
                    category=IssueCategory.DOC_MISSING_EXAMPLES,
                    severity=IssueSeverity.MEDIUM if is_class else IssueSeverity.LOW,
                    title="Missing usage examples",
                    description="Public API lacks usage examples",
                    context=docstring[:100],
                    auto_fixable=True,
                    fix_confidence=0.5,
                    fix_tools=["ai_tools"],
                    fix_effort_minutes=15,
                    fix_suggestion="Add Examples: section with practical usage",
                    user_impact=8.0,
                    maintainability_impact=5.0,
                    detected_by="docstring_analyzer",
                )
            )

        return issues

    def _analyze_type_hints(
        self, file_path: Path, content: str, lines: list[str], tree: ast.AST
    ) -> list[RefinedIssue]:
        """Analyze type hint quality and coverage."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                issues.extend(
                    self._analyze_function_type_hints(file_path, node, content)
                )

        # Check for outdated typing syntax
        for pattern in self.outdated_type_patterns:
            for match in re.finditer(pattern, content):
                line_no = content[: match.start()].count("\n") + 1
                issues.append(
                    RefinedIssue(
                        id=f"{file_path.stem}_outdated_typing_{line_no}",
                        file_path=str(file_path),
                        line_number=line_no,
                        category=IssueCategory.TYPE_OUTDATED_SYNTAX,
                        severity=IssueSeverity.LOW,
                        title="Outdated typing syntax",
                        description=f"Using old typing.{match.group()} instead of modern syntax",
                        context=lines[line_no - 1] if line_no <= len(lines) else "",
                        auto_fixable=True,
                        fix_confidence=0.9,
                        fix_tools=["pyupgrade"],
                        fix_effort_minutes=1,
                        fix_suggestion="Use modern built-in types (list, dict, etc.) instead of typing module",
                        user_impact=2.0,
                        maintainability_impact=3.0,
                        detected_by="type_analyzer",
                    )
                )

        return issues

    def _analyze_function_type_hints(
        self, file_path: Path, node: ast.FunctionDef, content: str
    ) -> list[RefinedIssue]:
        """Analyze type hints for a specific function."""
        issues = []

        is_public = not node.name.startswith("_")
        is_special = node.name.startswith("__") and node.name.endswith("__")

        # Skip special methods like __init__, __str__, etc. for some checks
        if is_special:
            return issues

        # Check return type annotation
        if not node.returns and not node.name.startswith("_"):
            # Check if function actually returns something
            has_return = any(
                isinstance(n, ast.Return) and n.value for n in ast.walk(node)
            )
            if has_return:
                issues.append(
                    RefinedIssue(
                        id=f"{file_path.stem}_{node.name}_missing_return_type",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        category=IssueCategory.TYPE_MISSING_RETURN,
                        severity=(
                            IssueSeverity.MEDIUM if is_public else IssueSeverity.LOW
                        ),
                        title="Missing return type annotation",
                        description=f"Function '{node.name}' returns value but lacks type annotation",
                        context=self._get_function_signature(
                            node, content.splitlines()
                        ),
                        auto_fixable=True,
                        fix_confidence=0.6,
                        fix_tools=["monkeytype", "mypy", "ai_tools"],
                        fix_effort_minutes=3,
                        fix_suggestion="Add return type annotation based on actual return value",
                        user_impact=5.0 if is_public else 2.0,
                        maintainability_impact=6.0,
                        detected_by="type_analyzer",
                    )
                )

        # Check parameter type annotations
        untyped_params = []
        for arg in node.args.args:
            if not arg.annotation and arg.arg != "self" and arg.arg != "cls":
                untyped_params.append(arg.arg)

        if untyped_params:
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_{node.name}_missing_param_types",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    category=IssueCategory.TYPE_MISSING_PARAMS,
                    severity=IssueSeverity.MEDIUM if is_public else IssueSeverity.LOW,
                    title="Missing parameter type annotations",
                    description=f"Parameters {untyped_params} lack type annotations",
                    context=self._get_function_signature(node, content.splitlines()),
                    auto_fixable=True,
                    fix_confidence=0.7,
                    fix_tools=["monkeytype", "ai_tools"],
                    fix_effort_minutes=len(untyped_params) * 2,
                    fix_suggestion="Add type annotations for all parameters",
                    user_impact=5.0 if is_public else 2.0,
                    maintainability_impact=7.0,
                    detected_by="type_analyzer",
                )
            )

        return issues

    def _analyze_code_quality(
        self, file_path: Path, content: str, lines: list[str], tree: ast.AST
    ) -> list[RefinedIssue]:
        """Analyze general code quality issues."""
        issues = []

        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line) > 88:  # PEP 8 recommendation
                issues.append(
                    RefinedIssue(
                        id=f"{file_path.stem}_long_line_{i}",
                        file_path=str(file_path),
                        line_number=i,
                        category=IssueCategory.CODE_LINE_TOO_LONG,
                        severity=IssueSeverity.LOW,
                        title=f"Line too long ({len(line)} chars)",
                        description="Line exceeds 88 character limit",
                        context=line[:100] + "..." if len(line) > 100 else line,
                        auto_fixable=True,
                        fix_confidence=0.8,
                        fix_tools=["black", "autopep8"],
                        fix_effort_minutes=1,
                        fix_suggestion="Break line into multiple lines or use line continuation",
                        user_impact=1.0,
                        maintainability_impact=2.0,
                        detected_by="code_analyzer",
                    )
                )

        # Check function complexity
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > 10:  # High complexity threshold
                    issues.append(
                        RefinedIssue(
                            id=f"{file_path.stem}_{node.name}_high_complexity",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            category=IssueCategory.CODE_COMPLEXITY_HIGH,
                            severity=(
                                IssueSeverity.MEDIUM
                                if complexity > 15
                                else IssueSeverity.LOW
                            ),
                            title=f"High cyclomatic complexity ({complexity})",
                            description=f"Function '{node.name}' has complexity score of {complexity}",
                            context=self._get_function_signature(node, lines),
                            auto_fixable=False,
                            fix_confidence=0.0,
                            fix_tools=[],
                            fix_effort_minutes=complexity * 5,
                            fix_suggestion="Refactor into smaller functions or reduce branching logic",
                            complexity_score=complexity,
                            user_impact=3.0,
                            maintainability_impact=8.0,
                            detected_by="code_analyzer",
                        )
                    )

        # Check naming conventions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if any(
                    re.match(pattern, node.name)
                    for pattern in self.poor_naming_patterns
                ):
                    issues.append(
                        RefinedIssue(
                            id=f"{file_path.stem}_{node.name}_poor_naming",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            category=IssueCategory.CODE_NAMING_POOR,
                            severity=IssueSeverity.LOW,
                            title=f"Poor function name: '{node.name}'",
                            description="Function name is not descriptive",
                            context=f"def {node.name}(...)",
                            auto_fixable=False,
                            fix_confidence=0.0,
                            fix_tools=[],
                            fix_effort_minutes=10,
                            fix_suggestion="Use descriptive name that explains what the function does",
                            user_impact=4.0,
                            maintainability_impact=6.0,
                            detected_by="code_analyzer",
                        )
                    )

        return issues

    def _analyze_imports(
        self, file_path: Path, content: str, lines: list[str], tree: ast.AST
    ) -> list[RefinedIssue]:
        """Analyze import-related issues."""
        issues = []

        imports_used = set()
        imports_defined = {}

        # Collect all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports_defined[name] = (node.lineno, alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.names[0].name == "*":
                    issues.append(
                        RefinedIssue(
                            id=f"{file_path.stem}_star_import_{node.lineno}",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            category=IssueCategory.IMPORT_STAR,
                            severity=IssueSeverity.MEDIUM,
                            title="Star import found",
                            description=f"Star import from {node.module}",
                            context=(
                                lines[node.lineno - 1]
                                if node.lineno <= len(lines)
                                else ""
                            ),
                            auto_fixable=True,
                            fix_confidence=0.7,
                            fix_tools=["autoflake", "isort"],
                            fix_effort_minutes=5,
                            fix_suggestion="Replace star import with explicit imports",
                            user_impact=3.0,
                            maintainability_impact=7.0,
                            detected_by="import_analyzer",
                        )
                    )
                else:
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name
                        imports_defined[name] = (
                            node.lineno,
                            f"{node.module}.{alias.name}",
                        )

        # Check for usage of imports (simplified)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id in imports_defined:
                    imports_used.add(node.id)
            elif isinstance(node, ast.Attribute):
                if hasattr(node.value, "id") and node.value.id in imports_defined:
                    imports_used.add(node.value.id)

        # Find unused imports
        unused_imports = set(imports_defined.keys()) - imports_used
        for unused in unused_imports:
            line_no, full_name = imports_defined[unused]
            issues.append(
                RefinedIssue(
                    id=f"{file_path.stem}_unused_import_{line_no}",
                    file_path=str(file_path),
                    line_number=line_no,
                    category=IssueCategory.IMPORT_UNUSED,
                    severity=IssueSeverity.LOW,
                    title=f"Unused import: {unused}",
                    description=f"Import '{full_name}' is not used",
                    context=lines[line_no - 1] if line_no <= len(lines) else "",
                    auto_fixable=True,
                    fix_confidence=0.9,
                    fix_tools=["autoflake"],
                    fix_effort_minutes=1,
                    fix_suggestion="Remove unused import",
                    user_impact=1.0,
                    maintainability_impact=2.0,
                    detected_by="import_analyzer",
                )
            )

        return issues

    def _analyze_api_design(
        self, file_path: Path, content: str, lines: list[str], tree: ast.AST
    ) -> list[RefinedIssue]:
        """Analyze API design quality."""
        issues = []

        # Find public functions that don't handle errors
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                has_try_except = any(isinstance(n, ast.Try) for n in ast.walk(node))
                has_raises_doc = False

                docstring = ast.get_docstring(node)
                if docstring and any(
                    section in docstring
                    for section in ["Raises:", "Except:", "Exceptions:"]
                ):
                    has_raises_doc = True

                if not has_try_except and not has_raises_doc:
                    complexity = self._calculate_complexity(node)
                    if complexity > 3:  # Only flag complex functions
                        issues.append(
                            RefinedIssue(
                                id=f"{file_path.stem}_{node.name}_missing_error_handling",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                category=IssueCategory.API_MISSING_ERROR_HANDLING,
                                severity=IssueSeverity.MEDIUM,
                                title="Missing error handling",
                                description=f"Public function '{node.name}' lacks error handling documentation",
                                context=self._get_function_signature(node, lines),
                                auto_fixable=False,
                                fix_confidence=0.0,
                                fix_tools=[],
                                fix_effort_minutes=20,
                                fix_suggestion="Add try/except blocks or document potential exceptions in Raises section",
                                complexity_score=complexity,
                                user_impact=6.0,
                                maintainability_impact=7.0,
                                detected_by="api_analyzer",
                            )
                        )

        return issues

    def _calculate_priority_score(self, issue: RefinedIssue) -> float:
        """Calculate composite priority score for an issue."""
        severity_weights = {
            IssueSeverity.CRITICAL: 10.0,
            IssueSeverity.HIGH: 7.0,
            IssueSeverity.MEDIUM: 5.0,
            IssueSeverity.LOW: 2.0,
            IssueSeverity.INFO: 1.0,
        }

        # Base score from severity
        score = severity_weights[issue.severity]

        # Adjust based on impact metrics
        impact_factor = (issue.user_impact + issue.maintainability_impact) / 20.0
        score *= 1.0 + impact_factor

        # Bonus for auto-fixable issues
        if issue.auto_fixable:
            score *= 1.0 + issue.fix_confidence * 0.5

        # Penalty for high effort
        if issue.fix_effort_minutes > 30:
            score *= 0.8

        return round(score, 2)

    def _is_public_module(self, file_path: Path) -> bool:
        """Determine if a module is part of the public API."""
        return (
            not file_path.name.startswith("_")
            and "test" not in str(file_path).lower()
            and "example" not in str(file_path).lower()
            and "debug" not in str(file_path).lower()
        )

    def _get_function_signature(self, node: ast.FunctionDef, lines: list[str]) -> str:
        """Extract function signature from source."""
        try:
            start_line = node.lineno - 1
            # Find the end of the function definition
            end_line = start_line
            paren_count = 0
            in_function_def = False

            for i in range(start_line, min(len(lines), start_line + 10)):
                line = lines[i]
                if "def " in line:
                    in_function_def = True
                if in_function_def:
                    paren_count += line.count("(") - line.count(")")
                    end_line = i
                    if paren_count == 0 and ":" in line:
                        break

            return "\n".join(lines[start_line : end_line + 1])
        except:
            return f"def {node.name}(...):"

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if file should be skipped."""
        skip_patterns = [
            "__pycache__",
            ".git",
            "test_",
            "_test.py",
            "tests/",
            ".venv",
            "build/",
            "dist/",
            ".eggs/",
            "*.egg-info/",
        ]

        return any(pattern in str(file_path) for pattern in skip_patterns)

    def analyze_codebase(self) -> list[RefinedIssue]:
        """Analyze entire codebase and return all issues."""
        self.issues = []

        python_files = list(self.root_path.rglob("*.py"))
        total_files = len(python_files)

        logger.info(f"Analyzing {total_files} Python files...")

        for i, py_file in enumerate(python_files, 1):
            if i % 100 == 0:
                logger.info(f"Progress: {i}/{total_files} files analyzed")

            file_issues = self.analyze_file(py_file)
            self.issues.extend(file_issues)

        # Sort by priority score
        self.issues.sort(key=lambda x: x.priority_score, reverse=True)

        return self.issues

    def generate_comprehensive_report(self) -> str:
        """Generate detailed analysis report."""
        if not self.issues:
            return "No issues found or analysis not run yet."

        # Group issues by category
        by_category = {}
        for issue in self.issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)

        # Group by severity
        by_severity = {}
        for issue in self.issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)

        # Auto-fixable statistics
        auto_fixable = [i for i in self.issues if i.auto_fixable]
        high_confidence_fixes = [i for i in auto_fixable if i.fix_confidence >= 0.8]

        report = []
        report.append("# 🔍 Comprehensive Code Quality Analysis Report")
        report.append("")
        report.append(f"**Total Issues Found**: {len(self.issues)}")
        report.append(
            f"**Auto-fixable Issues**: {len(auto_fixable)} ({len(auto_fixable)/len(self.issues)*100:.1f}%)"
        )
        report.append(f"**High-confidence Fixes**: {len(high_confidence_fixes)}")
        report.append("")

        # Summary by severity
        report.append("## 📊 Issues by Severity")
        report.append("")
        for severity in IssueSeverity:
            count = len(by_severity.get(severity, []))
            if count > 0:
                auto_count = len([i for i in by_severity[severity] if i.auto_fixable])
                report.append(
                    f"- **{severity.value.title()}**: {count} issues ({auto_count} auto-fixable)"
                )
        report.append("")

        # Top issues by category
        report.append("## 🎯 Issues by Category")
        report.append("")
        report.append("| Category | Count | Auto-fixable | Avg Priority | Top Tool |")
        report.append("|----------|-------|--------------|-------------|----------|")

        for category, issues in sorted(
            by_category.items(), key=lambda x: len(x[1]), reverse=True
        ):
            auto_count = len([i for i in issues if i.auto_fixable])
            avg_priority = sum(i.priority_score for i in issues) / len(issues)

            # Find most common tool
            tools = []
            for issue in issues:
                tools.extend(issue.fix_tools)
            top_tool = max(set(tools), key=tools.count) if tools else "manual"

            report.append(
                f"| {category.value} | {len(issues)} | {auto_count} | {avg_priority:.1f} | {top_tool} |"
            )

        report.append("")

        # High priority issues
        report.append("## 🚨 Top 10 Priority Issues")
        report.append("")

        for i, issue in enumerate(self.issues[:10], 1):
            report.append(f"### {i}. {issue.title}")
            report.append(f"**File**: `{issue.file_path}:{issue.line_number}`")
            report.append(
                f"**Severity**: {issue.severity.value} | **Priority**: {issue.priority_score}"
            )
            report.append(
                f"**Auto-fixable**: {'✅' if issue.auto_fixable else '❌'} | **Effort**: {issue.fix_effort_minutes}min"
            )
            if issue.fix_tools:
                report.append(f"**Tools**: {', '.join(issue.fix_tools)}")
            report.append(f"**Description**: {issue.description}")
            if issue.fix_suggestion:
                report.append(f"**Fix**: {issue.fix_suggestion}")
            report.append("")

        # Quick wins
        quick_wins = [
            i
            for i in auto_fixable
            if i.fix_effort_minutes <= 5 and i.fix_confidence >= 0.8
        ]
        if quick_wins:
            report.append(f"## ⚡ Quick Wins ({len(quick_wins)} issues)")
            report.append("")
            report.append(
                "Issues that can be fixed automatically with high confidence in under 5 minutes:"
            )
            report.append("")

            for issue in quick_wins[:20]:  # Top 20 quick wins
                report.append(
                    f"- **{issue.file_path}:{issue.line_number}** - {issue.title}"
                )
                report.append(
                    f"  Tools: {', '.join(issue.fix_tools)} | Effort: {issue.fix_effort_minutes}min"
                )

            if len(quick_wins) > 20:
                report.append(f"  ... and {len(quick_wins) - 20} more")

            report.append("")

        return "\n".join(report)


@click.command()
@click.option("--root", default="packages/", help="Root directory to analyze")
@click.option("--output", default="REFINED_ANALYSIS_REPORT.md", help="Output file")
@click.option("--category", multiple=True, help="Filter by specific categories")
@click.option("--severity", multiple=True, help="Filter by severity levels")
@click.option("--auto-fixable-only", is_flag=True, help="Show only auto-fixable issues")
@click.option("--min-priority", type=float, default=0.0, help="Minimum priority score")
def main(
    root: str,
    output: str,
    category: tuple[str],
    severity: tuple[str],
    auto_fixable_only: bool,
    min_priority: float,
):
    """Refined documentation and code quality analyzer."""
    analyzer = RefinedDocumentationAnalyzer(root)

    print("🔍 Analyzing codebase comprehensively...")
    issues = analyzer.analyze_codebase()

    # Apply filters
    if category:
        issues = [i for i in issues if i.category.value in category]

    if severity:
        issues = [i for i in issues if i.severity.value in severity]

    if auto_fixable_only:
        issues = [i for i in issues if i.auto_fixable]

    if min_priority > 0:
        issues = [i for i in issues if i.priority_score >= min_priority]

    print("\n📊 Analysis Complete:")
    print(f"Total issues found: {len(analyzer.issues)}")
    print(f"After filters: {len(issues)}")
    print(f"Auto-fixable: {len([i for i in issues if i.auto_fixable])}")
    print(f"High priority (>7.0): {len([i for i in issues if i.priority_score > 7.0])}")

    # Generate report
    report = analyzer.generate_comprehensive_report()

    with open(output, "w") as f:
        f.write(report)

    print(f"\n✅ Detailed report written to: {output}")


if __name__ == "__main__":
    main()
