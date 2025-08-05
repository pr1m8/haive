#!/usr/bin/env python3
"""Enhanced documentation build with comprehensive error handling and extension
utilization."""

import ast
import json
import os
import shutil
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Configuration
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build" / "html"
LOGS_DIR = DOCS_DIR / "logs"
ERROR_REPORT_DIR = DOCS_DIR / "error_reports"

# Extensions we're using
EXTENSIONS = {
    "autoapi.extension": "Automatic API documentation",
    "sphinx.ext.napoleon": "Google/NumPy docstring support",
    "sphinx.ext.viewcode": "Source code links",
    "sphinx.ext.linkcode": "GitHub source links",
    "sphinx.ext.intersphinx": "Cross-project references",
    "sphinx.ext.autosummary": "Summary tables",
    "sphinx.ext.autodoc": "Autodoc support",
    "sphinx_design": "Cards, grids, badges, dropdowns",
    "sphinx_tabs": "Tabbed content sections",
    "sphinx_inline_tabs": "Inline tabbed content",
    "sphinx_togglebutton": "Collapsible sections",
    "sphinx_copybutton": "Copy code buttons",
    "sphinx_exec_directive": "Execute Python code in docs",
    "myst_parser": "Markdown support",
    "sphinxcontrib.mermaid": "Mermaid diagrams",
    "sphinxcontrib.youtube": "YouTube video embedding",
    "sphinx_sitemap": "SEO sitemap generation",
    "sphinxcontrib.openapi": "OpenAPI/Swagger docs",
    "sphinxcontrib.httpdomain": "HTTP API documentation",
    "sphinxext.opengraph": "Open Graph metadata",
    "sphinx_autodoc_typehints": "Beautiful type hints",
}


def ensure_directories():
    """Ensure all required directories exist."""
    LOGS_DIR.mkdir(exist_ok=True)
    ERROR_REPORT_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)


def create_log_file(operation_name: str) -> Path:
    """Create a timestamped log file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return LOGS_DIR / f"{operation_name}_{timestamp}.log"


def create_error_report(error_type: str, details: dict) -> Path:
    """Create a detailed error report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = ERROR_REPORT_DIR / f"error_{error_type}_{timestamp}.json"

    report = {
        "timestamp": timestamp,
        "error_type": error_type,
        "details": details,
        "environment": {
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "path": sys.path[:5],  # First 5 paths
        },
    }

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)

    return report_file


def check_python_syntax(file_path: Path) -> tuple[bool, str]:
    """Check Python file syntax using AST."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def fix_common_syntax_errors(file_path: Path) -> bool:
    """Attempt to fix common syntax errors."""
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        modified = False
        for i, line in enumerate(lines):
            # Fix empty except blocks
            if line.strip().startswith("except") and line.strip().endswith(":"):
                if i + 1 < len(lines) and not lines[i + 1].strip():
                    lines[i + 1] = "    pass\n"
                    modified = True

            # Fix empty for/while loops
            if (
                line.strip().startswith(("for ", "while "))
                and line.strip().endswith(":")
                and i + 1 < len(lines)
                and not lines[i + 1].strip()
            ):
                lines[i + 1] = "    pass\n"
                modified = True

            # Fix empty if/else blocks
            if (
                line.strip().startswith(("if ", "else", "elif "))
                and line.strip().endswith(":")
                and i + 1 < len(lines)
                and not lines[i + 1].strip()
            ):
                lines[i + 1] = "    pass\n"
                modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
        return False
    except Exception:
        return False


def pre_build_validation() -> dict:
    """Validate all Python files before building."""
    results = {
        "total_files": 0,
        "syntax_errors": [],
        "fixed_errors": [],
        "warnings": [],
    }

    # Find all Python files in source directories
    for package_dir in Path("packages").glob("haive-*/src"):
        for py_file in package_dir.rglob("*.py"):
            results["total_files"] += 1

            # Check syntax
            valid, error = check_python_syntax(py_file)
            if not valid:
                # Try to fix common errors
                if fix_common_syntax_errors(py_file):
                    # Re-check after fix
                    valid, new_error = check_python_syntax(py_file)
                    if valid:
                        results["fixed_errors"].append(
                            {"file": str(py_file), "original_error": error},
                        )
                    else:
                        results["syntax_errors"].append(
                            {"file": str(py_file), "error": new_error},
                        )
                else:
                    results["syntax_errors"].append(
                        {"file": str(py_file), "error": error},
                    )

    # Report results

    if results["syntax_errors"]:
        for _err in results["syntax_errors"][:5]:  # Show first 5
            pass
        if len(results["syntax_errors"]) > 5:
            pass

    return results


def check_extension_compatibility() -> dict:
    """Check if all configured extensions are properly available."""
    results = {"available": [], "missing": [], "warnings": []}

    for ext, description in EXTENSIONS.items():
        try:
            # Try to import the extension
            module_name = ext.rsplit(".", 1)[0] if "." in ext else ext

            __import__(module_name)
            results["available"].append(ext)
        except ImportError as e:
            results["missing"].append(
                {"extension": ext, "description": description, "error": str(e)},
            )

    if results["missing"]:
        pass

    return results


def run_sphinx_build_enhanced(log_file: Path) -> dict:
    """Run Sphinx build with enhanced error handling."""
    status = {
        "success": False,
        "warnings": 0,
        "errors": 0,
        "output_exists": False,
        "error_details": [],
    }

    # Enhanced Sphinx command with all features
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",  # HTML builder
        "-E",  # Don't use cached environment
        "-a",  # Write all files
        "--keep-going",  # Continue despite errors
        "-v",  # Verbose
        "-W",
        "--keep-going",  # Treat warnings as errors but continue
        "-T",  # Show full traceback
        "-j",
        "auto",  # Parallel build
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Set enhanced environment
    env = os.environ.copy()
    env.update(
        {
            "SPHINX_AUTOSUMMARY_GENERATE": "true",
            "SPHINX_VERBOSE": "true",
            "HAIVE_DOCS_MODE": "enhanced",
            "PYTHONWARNINGS": "default",  # Show Python warnings
        },
    )

    try:
        # Run build process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            bufsize=1,
        )

        with open(log_file, "w") as f:
            f.write("Enhanced Sphinx Build Log\n")
            f.write(f"Started: {datetime.now()}\n")
            f.write(f"Command: {' '.join(cmd)}\n\n")

            # Process output line by line
            for line in iter(process.stdout.readline, ""):
                f.write(line)
                f.flush()

                # Analyze output
                line_lower = line.lower()
                if "warning:" in line_lower:
                    status["warnings"] += 1
                elif "error:" in line_lower:
                    status["errors"] += 1
                    status["error_details"].append(line.strip())
                elif "exception" in line_lower or "traceback" in line_lower:
                    status["error_details"].append(line.strip())
                elif "writing output..." in line_lower:
                    pass
                elif "build succeeded" in line_lower:
                    status["success"] = True

        status["returncode"] = process.wait()

        # Check for output even if build had errors
        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("**/*.html"))
            status["output_exists"] = len(html_files) > 0
            status["html_count"] = len(html_files)

    except Exception as e:
        status["error_details"].append(f"Build process error: {e!s}")
        traceback.print_exc()

    return status


def generate_build_report(
    validation_results: dict,
    extension_results: dict,
    build_status: dict,
    log_file: Path,
) -> Path:
    """Generate comprehensive build report."""
    report_file = (
        ERROR_REPORT_DIR / f"build_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

    with open(report_file, "w") as f:
        f.write("# Haive Documentation Build Report\n\n")
        f.write(f"**Generated**: {datetime.now()}\n\n")

        # Summary
        f.write("## Summary\n\n")
        if build_status["success"]:
            f.write("✅ **Build Status**: SUCCESS\n")
        elif build_status["output_exists"]:
            f.write("⚠️  **Build Status**: PARTIAL SUCCESS (with errors)\n")
        else:
            f.write("❌ **Build Status**: FAILED\n")

        f.write(f"- Files validated: {validation_results['total_files']}\n")
        f.write(f"- Syntax errors fixed: {len(validation_results['fixed_errors'])}\n")
        f.write(f"- Remaining errors: {len(validation_results['syntax_errors'])}\n")
        f.write(f"- Build warnings: {build_status['warnings']}\n")
        f.write(f"- Build errors: {build_status['errors']}\n")
        if "html_count" in build_status:
            f.write(f"- HTML files generated: {build_status['html_count']}\n")

        # Extension Status
        f.write("\n## Extension Status\n\n")
        f.write(f"### Available ({len(extension_results['available'])})\n\n")
        for ext in extension_results["available"]:
            f.write(f"- ✅ {ext}: {EXTENSIONS.get(ext, 'N/A')}\n")

        if extension_results["missing"]:
            f.write(f"\n### Missing ({len(extension_results['missing'])})\n\n")
            for item in extension_results["missing"]:
                f.write(f"- ❌ {item['extension']}: {item['description']}\n")

        # Validation Issues
        if validation_results["syntax_errors"]:
            f.write("\n## Syntax Errors\n\n")
            for err in validation_results["syntax_errors"]:
                f.write(f"### {err['file']}\n")
                f.write(f"```\n{err['error']}\n```\n\n")

        # Build Errors
        if build_status["error_details"]:
            f.write("\n## Build Errors\n\n")
            for error in build_status["error_details"][:10]:  # First 10
                f.write(f"- {error}\n")

        # Recommendations
        f.write("\n## Recommendations\n\n")
        if validation_results["syntax_errors"]:
            f.write("1. Fix remaining syntax errors in Python files\n")
        if extension_results["missing"]:
            f.write("2. Install missing extensions or update configuration\n")
        if build_status["warnings"] > 50:
            f.write("3. Address documentation warnings to improve quality\n")

        f.write(f"\n**Full log**: {log_file}\n")

    return report_file


def main():
    """Main enhanced documentation build process."""
    # Ensure directories exist
    ensure_directories()

    # Create log file
    log_file = create_log_file("enhanced_docs_build")

    # Pre-build validation
    validation_results = pre_build_validation()

    # Check extensions
    extension_results = check_extension_compatibility()

    # Clean build directory for fresh start
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Run enhanced build
    build_status = run_sphinx_build_enhanced(log_file)

    # Generate comprehensive report
    generate_build_report(validation_results, extension_results, build_status, log_file)

    # Final summary

    if build_status["success"] or build_status["output_exists"]:
        pass
    else:
        pass

    if BUILD_DIR.exists() and list(BUILD_DIR.glob("*.html")):
        index_path = BUILD_DIR / "index.html"
        if index_path.exists():
            pass

    # Return appropriate exit code
    if build_status["success"]:
        return 0
    if build_status["output_exists"]:
        return 1  # Partial success
    return 2  # Failed


if __name__ == "__main__":
    sys.exit(main())
