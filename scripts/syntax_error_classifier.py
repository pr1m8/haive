#!/usr/bin/env python3
"""Classify and fix syntax errors in Python files with backup and rollback capability."""

import ast
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ErrorPattern:
    """Represents a pattern of syntax error."""

    category: str
    pattern: str
    description: str
    fix_strategy: str
    example: str
    regex: Optional[str] = None


@dataclass
class SyntaxErrorInfo:
    """Information about a syntax error."""

    file_path: Path
    line_number: int
    error_message: str
    line_content: str
    context_before: List[str]
    context_after: List[str]
    category: Optional[str] = None
    suggested_fix: Optional[str] = None


class SyntaxErrorClassifier:
    """Classify and manage syntax errors."""

    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(exist_ok=True)
        self.error_patterns = self._define_error_patterns()
        self.errors: Dict[str, List[SyntaxErrorInfo]] = {}
        self.fix_history: List[Dict] = []

    def _define_error_patterns(self) -> List[ErrorPattern]:
        """Define common error patterns."""
        return [
            ErrorPattern(
                category="incomplete_comparison",
                pattern="missing value after comparison operator",
                description="Comparison operator without right operand",
                fix_strategy="Add placeholder value or remove incomplete comparison",
                example="if x >=:",
                regex=r"(if|while|elif)\s+.*\s+(>=|<=|>|<|==|!=)\s*:",
            ),
            ErrorPattern(
                category="incomplete_assignment",
                pattern="missing value after assignment",
                description="Assignment operator without value",
                fix_strategy="Add default value or remove line",
                example="max_retries =",
                regex=r"^\s*\w+\s*=\s*$",
            ),
            ErrorPattern(
                category="unterminated_string",
                pattern="unterminated string literal",
                description="String not properly closed",
                fix_strategy="Close string or fix quotes",
                example='print("Hello!"!")',
                regex=r'["\'].*["\']["\']|["\'][^"\']*$',
            ),
            ErrorPattern(
                category="missing_block",
                pattern="expected an indented block",
                description="Missing code block after statement",
                fix_strategy="Add pass statement or implement block",
                example="if condition:\n# missing block",
                regex=r"(if|else|elif|for|while|def|class|try|except|finally)\s*.*:\s*$",
            ),
            ErrorPattern(
                category="typo_in_keyword",
                pattern="invalid syntax in control structure",
                description="Typo in for/if/while statement",
                fix_strategy="Fix keyword typo",
                example="for x i list:",
                regex=r"for\s+\w+\s+[^i][^n]\s+",
            ),
            ErrorPattern(
                category="incomplete_variable",
                pattern="incomplete variable name",
                description="Variable name cut off or typo",
                fix_strategy="Complete variable name",
                example="state.revision_coun",
                regex=r"\w+\.\w+[^a-zA-Z0-9_\s\)\]\}]",
            ),
            ErrorPattern(
                category="malformed_expression",
                pattern="malformed expression",
                description="Expression with syntax errors",
                fix_strategy="Fix expression syntax",
                example="sum(for x in list)",
                regex=None,
            ),
            ErrorPattern(
                category="unclosed_parenthesis",
                pattern="parenthesis was never closed",
                description="Missing closing parenthesis",
                fix_strategy="Add closing parenthesis",
                example="func(arg1, arg2",
                regex=r"\([^)]*$",
            ),
        ]

    def analyze_file(self, file_path: Path) -> Optional[SyntaxErrorInfo]:
        """Analyze a file for syntax errors."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            ast.parse(content)
            return None  # No syntax error
        except SyntaxError as e:
            lines = content.split("\n")
            line_idx = e.lineno - 1 if e.lineno else 0

            # Get context
            context_before = []
            context_after = []

            if line_idx > 0:
                context_before = lines[max(0, line_idx - 3) : line_idx]
            if line_idx < len(lines) - 1:
                context_after = lines[line_idx + 1 : min(len(lines), line_idx + 4)]

            error_info = SyntaxErrorInfo(
                file_path=file_path,
                line_number=e.lineno or 0,
                error_message=e.msg,
                line_content=lines[line_idx] if line_idx < len(lines) else "",
                context_before=context_before,
                context_after=context_after,
            )

            # Classify the error
            error_info.category = self._classify_error(error_info)
            error_info.suggested_fix = self._suggest_fix(error_info)

            return error_info
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None

    def _classify_error(self, error_info: SyntaxErrorInfo) -> str:
        """Classify the error based on patterns."""
        error_msg = error_info.error_message.lower()
        line = error_info.line_content.strip()

        # Check each pattern
        for pattern in self.error_patterns:
            # Check error message
            if pattern.pattern in error_msg:
                return pattern.category

            # Check regex if available
            if pattern.regex and re.search(pattern.regex, line):
                return pattern.category

        # Specific checks
        if "unterminated string" in error_msg:
            return "unterminated_string"
        elif "expected an indented block" in error_msg:
            return "missing_block"
        elif ">=" in line and line.strip().endswith(":"):
            return "incomplete_comparison"
        elif "=" in line and line.strip().endswith("="):
            return "incomplete_assignment"
        elif "was never closed" in error_msg:
            return "unclosed_parenthesis"

        return "unknown"

    def _suggest_fix(self, error_info: SyntaxErrorInfo) -> Optional[str]:
        """Suggest a fix for the error."""
        line = error_info.line_content
        category = error_info.category

        if category == "incomplete_comparison":
            # Add a placeholder value
            if ">=" in line:
                return line.replace(">=:", ">= 0:")
            elif "<=" in line:
                return line.replace("<=:", "<= 0:")
            elif ">" in line and line.strip().endswith(">"):
                return line.replace(">", "> 0")
            elif "<" in line and line.strip().endswith("<"):
                return line.replace("<", "< 0")

        elif category == "incomplete_assignment":
            # Add a default value
            if line.strip().endswith("="):
                indent = len(line) - len(line.lstrip())
                var_name = line.strip()[:-1].strip()
                return line.rstrip() + " 0  # TODO: Add proper value"

        elif category == "unterminated_string":
            # Try to fix string
            # Count quotes
            single_quotes = line.count("'")
            double_quotes = line.count('"')

            if double_quotes % 2 != 0:
                # Odd number of double quotes
                if line.rstrip().endswith('"'):
                    return line
                else:
                    return line.rstrip() + '"'
            elif single_quotes % 2 != 0:
                # Odd number of single quotes
                if line.rstrip().endswith("'"):
                    return line
                else:
                    return line.rstrip() + "'"

        elif category == "missing_block":
            # Add pass statement
            indent = len(line) - len(line.lstrip())
            return line + "\n" + " " * (indent + 4) + "pass  # TODO: Implement"

        elif category == "typo_in_keyword":
            # Fix common typos
            if " i[" in line or ' i["' in line:
                return line.replace(" i[", " in [")
            elif " i " in line and "for " in line:
                return re.sub(r"\s+i\s+", " in ", line)

        elif category == "incomplete_variable":
            # Try to complete variable names
            match = re.search(r"(\w+)\.(\w+?)(?=[^a-zA-Z0-9_]|$)", line)
            if match:
                obj, attr = match.groups()
                # Common completions
                if attr.endswith("coun"):
                    return line.replace(f"{obj}.{attr}", f"{obj}.{attr}t")
                elif attr.endswith("statu"):
                    return line.replace(f"{obj}.{attr}", f"{obj}.{attr}s")

        return None

    def backup_file(self, file_path: Path) -> Path:
        """Create a backup of the file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        relative_path = file_path.relative_to(
            Path("/home/will/Projects/haive/backend/haive")
        )
        backup_path = (
            self.backup_dir / f"{relative_path.stem}_{timestamp}{relative_path.suffix}"
        )
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path

    def apply_fix(
        self, error_info: SyntaxErrorInfo, custom_fix: Optional[str] = None
    ) -> bool:
        """Apply a fix to the file."""
        if not error_info.suggested_fix and not custom_fix:
            return False

        # Backup first
        backup_path = self.backup_file(error_info.file_path)

        try:
            with open(error_info.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Apply fix
            line_idx = error_info.line_number - 1
            if line_idx < len(lines):
                original_line = lines[line_idx]
                fixed_line = custom_fix if custom_fix else error_info.suggested_fix

                # Handle multiline fixes
                if "\n" in fixed_line and not fixed_line.endswith("\n"):
                    fixed_line += "\n"

                lines[line_idx] = fixed_line

                # Write back
                with open(error_info.file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                # Record fix
                self.fix_history.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "file": str(error_info.file_path),
                        "line": error_info.line_number,
                        "original": original_line.strip(),
                        "fixed": fixed_line.strip(),
                        "category": error_info.category,
                        "backup": str(backup_path),
                    }
                )

                # Verify fix
                if self.analyze_file(error_info.file_path) is None:
                    return True
                else:
                    # Rollback if still has errors
                    shutil.copy2(backup_path, error_info.file_path)
                    return False

        except Exception as e:
            print(f"Error applying fix: {e}")
            # Rollback
            shutil.copy2(backup_path, error_info.file_path)
            return False

    def rollback_fix(self, file_path: Path) -> bool:
        """Rollback the last fix for a file."""
        # Find last fix for this file
        for fix in reversed(self.fix_history):
            if fix["file"] == str(file_path):
                backup_path = Path(fix["backup"])
                if backup_path.exists():
                    shutil.copy2(backup_path, file_path)
                    return True
        return False

    def scan_directory(self, directory: Path, limit: int = 100) -> None:
        """Scan directory for syntax errors."""
        count = 0
        for pattern in ["*/src/**/*.py", "*/examples/**/*.py", "*/tests/**/*.py"]:
            for file_path in directory.glob(pattern):
                if ".venv" in str(file_path) or "site-packages" in str(file_path):
                    continue

                error_info = self.analyze_file(file_path)
                if error_info:
                    category = error_info.category
                    if category not in self.errors:
                        self.errors[category] = []
                    self.errors[category].append(error_info)
                    count += 1
                    if count >= limit:
                        return

    def generate_report(self) -> str:
        """Generate a detailed report of errors."""
        lines = ["# Syntax Error Classification Report\n"]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Summary
        lines.append("## Summary\n")
        total_errors = sum(len(errors) for errors in self.errors.values())
        lines.append(f"Total errors found: {total_errors}\n")
        lines.append("\n### By Category:\n")

        for category, errors in sorted(self.errors.items()):
            lines.append(f"- **{category}**: {len(errors)} errors\n")

        # Detailed examples
        lines.append("\n## Examples by Category\n")

        for pattern in self.error_patterns:
            category = pattern.category
            if category in self.errors:
                errors = self.errors[category]
                lines.append(f"\n### {category.replace('_', ' ').title()}\n")
                lines.append(f"**Pattern**: {pattern.pattern}\n")
                lines.append(f"**Description**: {pattern.description}\n")
                lines.append(f"**Fix Strategy**: {pattern.fix_strategy}\n")
                lines.append(f"**Example**: `{pattern.example}`\n")
                lines.append(f"\n**Found {len(errors)} instances:**\n")

                # Show up to 3 examples
                for error in errors[:3]:
                    rel_path = error.file_path.relative_to(
                        Path("/home/will/Projects/haive/backend/haive")
                    )
                    lines.append(f"\n📄 `{rel_path}` (Line {error.line_number})\n")
                    lines.append("```python\n")

                    # Show context
                    for i, line in enumerate(error.context_before):
                        lines.append(
                            f"{error.line_number - len(error.context_before) + i}: {line}\n"
                        )

                    lines.append(f">>> {error.line_number}: {error.line_content}\n")

                    if error.suggested_fix:
                        lines.append(f"FIX: {error.suggested_fix}\n")

                    lines.append("```\n")

                if len(errors) > 3:
                    lines.append(f"\n... and {len(errors) - 3} more\n")

        return "".join(lines)

    def save_fix_history(self, path: Path) -> None:
        """Save fix history to JSON file."""
        with open(path, "w") as f:
            json.dump(self.fix_history, f, indent=2)

    def load_fix_history(self, path: Path) -> None:
        """Load fix history from JSON file."""
        if path.exists():
            with open(path, "r") as f:
                self.fix_history = json.load(f)
