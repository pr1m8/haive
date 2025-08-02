#!/usr/bin/env python3
"""
Documentation Build Diagnostics Report Generator
Date: August 1, 2025
Purpose: Comprehensive analysis of Sphinx documentation build issues
"""

import importlib
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "source"))

# Import the diagnostics module
from conf_modules.import_diagnostics import (
    diagnose_imports,
    find_all_python_modules,
    get_autodoc_mock_imports_from_diagnosis,
)


def analyze_import_issues():
    """Analyze all import issues in the project."""
    logger.info("Starting import analysis...")

    # AutoAPI directories
    autoapi_dirs = [
        "../../packages/haive-core/src",
        "../../packages/haive-agents/src",
        "../../packages/haive-tools/src",
        "../../packages/haive-games/src",
        "../../packages/haive-dataflow/src",
        "../../packages/haive-mcp/src",
        "../../packages/haive-prebuilt/src",
    ]

    # Convert to absolute paths
    source_dir = PROJECT_ROOT / "docs" / "source"
    absolute_dirs = []
    for dir_path in autoapi_dirs:
        abs_path = (source_dir / dir_path).resolve()
        if abs_path.exists():
            absolute_dirs.append(str(abs_path))

    # Run import diagnostics
    mock_imports = get_autodoc_mock_imports_from_diagnosis(
        autoapi_dirs, str(source_dir)
    )

    return mock_imports


def run_sphinx_diagnostic_build():
    """Run a minimal Sphinx build to collect all warnings and errors."""
    logger.info("Running Sphinx diagnostic build...")

    build_dir = PROJECT_ROOT / "docs" / "build" / "diagnostic"
    source_dir = PROJECT_ROOT / "docs" / "source"

    # Run sphinx-build with nitpicky mode
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-n",  # Nitpicky mode
        "-b",
        "gettext",  # Use gettext builder for fast analysis
        str(source_dir),
        str(build_dir),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.returncode,
    }


def parse_sphinx_warnings(output: str):
    """Parse Sphinx output to categorize warnings and errors."""
    issues = {
        "missing_references": [],
        "type_hint_issues": [],
        "import_errors": [],
        "cross_reference_issues": [],
        "autodoc_issues": [],
        "other_warnings": [],
    }

    lines = output.split("\n")

    for line in lines:
        if "WARNING:" in line:
            if "missing-reference" in line:
                # Extract the missing reference
                if "pending_xref" in line:
                    # Type hint reference
                    if any(
                        t in line
                        for t in [
                            "'str'",
                            "'int'",
                            "'bool'",
                            "'float'",
                            "'list'",
                            "'dict'",
                        ]
                    ):
                        issues["type_hint_issues"].append(line)
                    else:
                        issues["missing_references"].append(line)
                else:
                    issues["missing_references"].append(line)
            elif "ImportError" in line:
                issues["import_errors"].append(line)
            elif "autodoc" in line:
                issues["autodoc_issues"].append(line)
            elif "cross-reference" in line or "xref" in line:
                issues["cross_reference_issues"].append(line)
            else:
                issues["other_warnings"].append(line)

    return issues


def generate_report(mock_imports, sphinx_output):
    """Generate comprehensive documentation report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Parse Sphinx warnings
    issues = parse_sphinx_warnings(sphinx_output["stderr"] + sphinx_output["stdout"])

    # Count unique type issues
    type_counts = {}
    for issue in issues["type_hint_issues"]:
        for type_name in [
            "str",
            "int",
            "bool",
            "float",
            "list",
            "dict",
            "Any",
            "Optional",
            "List",
            "Dict",
        ]:
            if f"'{type_name}'" in issue:
                type_counts[type_name] = type_counts.get(type_name, 0) + 1

    report = f"""# Documentation Build Issues Report
Generated: {timestamp}
Date: August 1, 2025

## Executive Summary

This report documents all issues found during the Sphinx documentation build process for the Haive project.

### Issue Categories:
- **Import Errors**: {len(mock_imports)} modules need to be mocked
- **Type Hint References**: {len(issues["type_hint_issues"])} unresolved type references
- **Missing References**: {len(issues["missing_references"])} missing cross-references
- **Cross-Reference Issues**: {len(issues["cross_reference_issues"])} ambiguous or broken cross-references
- **Autodoc Issues**: {len(issues["autodoc_issues"])} autodoc-related problems
- **Other Warnings**: {len(issues["other_warnings"])} miscellaneous warnings

## 1. Import Issues

### Modules Requiring Mocking
The following external modules could not be imported and need to be mocked:

```python
autodoc_mock_imports = {json.dumps(sorted(mock_imports), indent=4)}
```

## 2. Type Hint Reference Issues

### Summary of Unresolved Type References:
{chr(10).join([f"- `{t}`: {count} occurrences" for t, count in sorted(type_counts.items())])}

### Root Cause:
Sphinx is unable to resolve basic Python type hints. This is because:
1. The `sphinx_autodoc_typehints` extension is currently disabled in the configuration
2. Intersphinx mapping for Python built-ins may not be properly configured
3. Type aliases are not being properly resolved

### Recommended Fix:
1. Re-enable `sphinx_autodoc_typehints` with proper configuration
2. Add `nitpick_ignore` entries for basic Python types
3. Configure `python_use_unqualified_type_names = True`

## 3. Missing References

### Common Missing References:
- `Document` - from langchain_core.documents
- `SecretStr` - from pydantic
- `BaseMessage`, `HumanMessage`, `AIMessage` - from langchain_core.messages
- Various internal module references

### Sample Missing References:
```
{chr(10).join(issues["missing_references"][:10])}
```

## 4. Cross-Reference Issues

### Ambiguous References:
These occur when multiple modules export the same name:

{chr(10).join(issues["cross_reference_issues"][:10])}

## 5. Proposed Solutions

### 5.1 Fix Type Hint References

Add to `conf.py`:

```python
# Configure nitpicky mode to ignore basic types
nitpicky = True
nitpick_ignore = [
    ("py:class", "str"),
    ("py:class", "int"),
    ("py:class", "bool"),
    ("py:class", "float"),
    ("py:class", "list"),
    ("py:class", "dict"),
    ("py:class", "Any"),
    ("py:class", "Optional"),
    ("py:class", "List"),
    ("py:class", "Dict"),
    # Add more as needed
]

# Enable Python domain configuration
python_use_unqualified_type_names = True
```

### 5.2 Fix Import Issues

Update `autodoc_mock_imports` in `conf.py` with all modules listed in section 1.

### 5.3 Fix Cross-References

1. Use fully qualified names in docstrings
2. Add explicit module prefixes where ambiguous
3. Use `:py:obj:` role with full paths

### 5.4 Configure sphinx-autodoc-typehints

In `extension_configs.py`, change:

```python
"autodoc_typehints": "none"  # Current setting
```

To:

```python
"autodoc_typehints": "description"  # Show in descriptions
"simplify_optional_unions": True
"typehints_use_signature": True
```

## 6. Testing Recommendations

1. Run phased build without `-W` flag initially
2. Fix issues incrementally by category
3. Add fixed issues to `nitpick_ignore` as needed
4. Re-enable strict mode once major issues are resolved

## 7. Files to Modify

1. `/docs/source/conf.py` - Main configuration
2. `/docs/source/conf_modules/extension_configs.py` - Extension settings
3. `/noxfiles/session_docs_phased.py` - Build process

---
Report generated by: scripts/documentation_diagnostics.py
"""

    return report


def main():
    """Run full diagnostics and generate report."""
    logger.info("Running documentation diagnostics...")

    # Get import issues
    mock_imports = analyze_import_issues()

    # Run Sphinx diagnostic build
    sphinx_output = run_sphinx_diagnostic_build()

    # Generate report
    report = generate_report(mock_imports, sphinx_output)

    # Save report
    report_path = PROJECT_ROOT / "project_docs" / "documentation_issues_2025_08_01.md"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w") as f:
        f.write(report)

    logger.info(f"Report saved to: {report_path}")

    # Also print summary
    print("\n=== DOCUMENTATION DIAGNOSTICS SUMMARY ===")
    print(f"Mock imports needed: {len(mock_imports)}")
    print(f"Report location: {report_path}")
    print("\nRun 'cat {report_path}' to view the full report")


if __name__ == "__main__":
    main()
