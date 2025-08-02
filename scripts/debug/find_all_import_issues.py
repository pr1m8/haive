#!/usr/bin/env python3
"""
Import Issue Analysis Script for Haive Framework

This script systematically finds all import issues in the codebase using multiple approaches:
1. Direct import testing
2. AST parsing for import analysis
3. Missing module detection
4. Relative import issues

Usage:
    poetry run python scripts/debug/find_all_import_issues.py
"""

import ast
import importlib
import importlib.util
import os
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
packages_root = project_root / "packages"


class ImportAnalyzer:
    def __init__(self):
        self.failed_imports = {}
        self.missing_modules = set()
        self.relative_import_issues = []
        self.circular_imports = []
        self.external_dependencies = set()
        self.analyzed_files = 0

    def analyze_all_packages(self):
        """Analyze all packages for import issues."""
        print("🔍 Analyzing Import Issues in Haive Framework")
        print("=" * 60)

        # Find all Python files
        python_files = []
        for package_dir in packages_root.glob("haive-*"):
            if package_dir.is_dir():
                src_dir = package_dir / "src"
                if src_dir.exists():
                    python_files.extend(src_dir.rglob("*.py"))

        print(f"📁 Found {len(python_files)} Python files to analyze")

        # Analyze each file
        for file_path in python_files:
            self.analyze_file(file_path)
            self.analyzed_files += 1

        # Generate report
        self.generate_report()

    def analyze_file(self, file_path: Path):
        """Analyze a single Python file for import issues."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                self.failed_imports[str(file_path)] = f"SyntaxError: {e}"
                return

            # Extract imports
            imports = self.extract_imports(tree)

            # Check each import
            for import_info in imports:
                self.check_import(file_path, import_info)

        except Exception as e:
            self.failed_imports[str(file_path)] = f"FileError: {e}"

    def extract_imports(self, tree: ast.AST) -> List[Dict]:
        """Extract all import statements from AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "import",
                            "module": alias.name,
                            "names": [alias.name],
                            "level": 0,
                            "line": node.lineno,
                        }
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names] if node.names else []
                imports.append(
                    {
                        "type": "from",
                        "module": module,
                        "names": names,
                        "level": node.level,
                        "line": node.lineno,
                    }
                )

        return imports

    def check_import(self, file_path: Path, import_info: Dict):
        """Check if an import statement works."""
        module_name = import_info["module"]
        import_type = import_info["type"]
        level = import_info["level"]
        line = import_info["line"]

        # Skip empty modules (from . import ...)
        if not module_name and level > 0:
            return

        # Check for relative imports
        if level > 0:
            self.check_relative_import(file_path, import_info)
            return

        # Try to import the module
        try:
            if import_type == "import":
                importlib.import_module(module_name)
            else:  # from X import Y
                if module_name:
                    mod = importlib.import_module(module_name)
                    # Check if specific names exist
                    for name in import_info["names"]:
                        if name != "*" and not hasattr(mod, name):
                            self.record_import_issue(
                                file_path,
                                line,
                                f"'{name}' not found in module '{module_name}'",
                            )
                else:
                    # from . import ... (handled in relative imports)
                    pass
        except ImportError as e:
            self.record_import_issue(file_path, line, str(e))

            # Categorize the issue
            if "No module named" in str(e):
                self.missing_modules.add(module_name)

            # Check if it's an external dependency
            if any(
                ext in module_name
                for ext in ["google", "openai", "anthropic", "langchain"]
            ):
                self.external_dependencies.add(module_name)

    def check_relative_import(self, file_path: Path, import_info: Dict):
        """Check relative import issues."""
        level = import_info["level"]
        module_name = import_info["module"]
        line = import_info["line"]

        # Calculate the expected module path
        try:
            # Get the file's module path
            relative_to_packages = file_path.relative_to(packages_root)
            parts = list(relative_to_packages.parts)

            # Remove 'src' and file extension
            if "src" in parts:
                src_index = parts.index("src")
                parts = parts[src_index + 1 :]
            parts[-1] = parts[-1].replace(".py", "")

            # Calculate relative path
            if level > len(parts) - 1:
                self.relative_import_issues.append(
                    {
                        "file": str(file_path),
                        "line": line,
                        "issue": f"Relative import level {level} too high for module depth {len(parts) - 1}",
                        "import": f"{'.' * level}{module_name}",
                    }
                )

        except Exception as e:
            self.relative_import_issues.append(
                {
                    "file": str(file_path),
                    "line": line,
                    "issue": f"Cannot resolve relative import: {e}",
                    "import": f"{'.' * level}{module_name}",
                }
            )

    def record_import_issue(self, file_path: Path, line: int, issue: str):
        """Record an import issue."""
        key = str(file_path)
        if key not in self.failed_imports:
            self.failed_imports[key] = []
        if isinstance(self.failed_imports[key], str):
            self.failed_imports[key] = [self.failed_imports[key]]
        self.failed_imports[key].append(f"Line {line}: {issue}")

    def generate_report(self):
        """Generate comprehensive import analysis report."""
        print(f"\n📊 IMPORT ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Files analyzed: {self.analyzed_files}")
        print(f"Files with issues: {len(self.failed_imports)}")
        print(f"Missing modules: {len(self.missing_modules)}")
        print(f"Relative import issues: {len(self.relative_import_issues)}")
        print(f"External dependencies: {len(self.external_dependencies)}")

        # Most problematic modules
        print(f"\n🚨 MISSING CORE MODULES (TOP 10)")
        print("-" * 40)
        missing_sorted = sorted(self.missing_modules)[:10]
        for i, module in enumerate(missing_sorted, 1):
            print(f"{i:2d}. {module}")

        # Relative import issues
        if self.relative_import_issues:
            print(f"\n⚠️  RELATIVE IMPORT ISSUES")
            print("-" * 40)
            for issue in self.relative_import_issues[:10]:  # Top 10
                rel_file = Path(issue["file"]).relative_to(project_root)
                print(f"📄 {rel_file}:{issue['line']}")
                print(f"   {issue['issue']}")
                print(f"   Import: {issue['import']}")
                print()

        # External dependencies
        if self.external_dependencies:
            print(f"\n📦 EXTERNAL DEPENDENCIES NEEDED")
            print("-" * 40)
            for dep in sorted(self.external_dependencies):
                print(f"   {dep}")

        # Detailed file issues (top 20)
        print(f"\n📋 DETAILED IMPORT ISSUES (TOP 20)")
        print("-" * 40)
        sorted_files = sorted(
            self.failed_imports.items(),
            key=lambda x: len(x[1]) if isinstance(x[1], list) else 1,
            reverse=True,
        )

        for file_path, issues in sorted_files[:20]:
            rel_path = Path(file_path).relative_to(project_root)
            print(f"\n📄 {rel_path}")

            if isinstance(issues, list):
                for issue in issues[:5]:  # Top 5 issues per file
                    print(f"   ❌ {issue}")
                if len(issues) > 5:
                    print(f"   ... and {len(issues) - 5} more issues")
            else:
                print(f"   ❌ {issues}")

        # Summary recommendations
        print(f"\n🎯 RECOMMENDATIONS")
        print("-" * 40)
        print("1. Install missing external dependencies:")
        for dep in sorted(self.external_dependencies)[:5]:
            print(f"   poetry add {dep.split('.')[0]}")

        print("\n2. Fix relative import issues:")
        print("   - Use absolute imports: from haive.package.module import X")
        print("   - Check module structure and __init__.py files")

        print("\n3. Create missing core modules:")
        core_missing = [m for m in self.missing_modules if m.startswith("haive.core")][
            :5
        ]
        for module in core_missing:
            print(f"   - {module}")

        print(f"\n4. Priority fixes (most impactful):")
        print("   - Fix relative imports (blocks AST parsing)")
        print("   - Add missing __init__.py files")
        print("   - Install google-search-results")
        print("   - Fix Pydantic v2 validators")


def main():
    """Main analysis function."""
    analyzer = ImportAnalyzer()
    analyzer.analyze_all_packages()

    # Also suggest tools for automated fixing
    print(f"\n🛠️  RECOMMENDED TOOLS FOR FIXING")
    print("-" * 40)
    print("1. deptry - Find missing dependencies:")
    print("   pip install deptry && deptry .")
    print("\n2. findimports - Analyze import structure:")
    print("   pip install findimports && findimports packages/")
    print("\n3. pylint - Check for undefined variables:")
    print("   poetry run pylint -E packages/ | grep undefined-variable")
    print("\n4. isort - Fix import ordering:")
    print("   poetry run isort packages/")


if __name__ == "__main__":
    main()
