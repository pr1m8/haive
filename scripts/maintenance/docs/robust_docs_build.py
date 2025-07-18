#!/usr/bin/env python3
"""Robust documentation build with comprehensive error tracking and recovery."""

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
ERROR_TRACKING_FILE = LOGS_DIR / "error_tracking.json"


class DocumentationBuilder:
    def __init__(self):
        self.errors = {
            "syntax_errors": [],
            "import_errors": [],
            "directive_errors": [],
            "build_errors": [],
            "warnings": [],
            "fixed_errors": [],
        }
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "failed_files": 0,
            "warnings_count": 0,
            "errors_count": 0,
            "html_generated": 0,
        }
        self.log_file = None

    def setup_logging(self):
        """Setup logging infrastructure."""
        LOGS_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = LOGS_DIR / f"robust_build_{timestamp}.log"
        return self.log_file

    def log(self, message, level="INFO"):
        """Log message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        # Console output with color
        if level == "ERROR":
            pass}")
        elif level == "WARNING":
            passe}")
        elif level == "SUCCESS":
            pass")
        elif level == "INFO":
            pass}")
        else:
            pass

        # File output
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(log_entry + "\n")

    def fix_syntax_error(self, file_path, error_msg):
        """Attempt to fix common syntax errors."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content
            fixed = False

            # Fix empty except blocks
            if "expected an indented block after 'except'" in error_msg:
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if line.strip().startswith("except") and line.strip().endswith(":"):
                        if i + 1 < len(lines) and not lines[i + 1].strip():
                            indent = len(line) - len(line.lstrip()) + 4
                            lines.insert(i + 1, " " * indent + "pass")
                            fixed = True
                            break
                content = "\n".join(lines)

            # Fix empty for/while loops
            elif "expected an indented block" in error_msg and any(
                keyword in error_msg.lower()
                for keyword in ["for", "while", "if", "else", "elif", "def", "class"]
            ):
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if any(
                        stripped.startswith(kw + " ")
                        or stripped.startswith(kw + ":")
                        or stripped == kw + ":"
                        for kw in ["for", "while", "if", "else", "elif", "def", "class"]
                    ) and (
                        stripped.endswith(":")
                        and i + 1 < len(lines)
                        and not lines[i + 1].strip()
                    ):
                        indent = len(line) - len(line.lstrip()) + 4
                        lines.insert(i + 1, " " * indent + "pass")
                        fixed = True
                        break
                content = "\n".join(lines)

            if fixed and content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.errors["fixed_errors"].append(
                    {
                        "file": str(file_path),
                        "error": error_msg,
                        "fix": "Added 'pass' statement",
                    }
                )
                return True

        except Exception as e:
            self.log(f"Failed to fix {file_path}: {e}", "ERROR")
        return False

    def validate_python_files(self):
        """Validate all Python files and attempt fixes."""
        self.log("Starting Python file validation...", "INFO")

        for package_dir in Path("packages").glob("haive-*/src"):
            for py_file in package_dir.rglob("*.py"):
                self.stats["total_files"] += 1

                try:
                    # Try to compile the file
                    with open(py_file, "rb") as f:
                        compile(f.read(), str(py_file), "exec")
                    self.stats["processed_files"] += 1

                except SyntaxError as e:
                    error_info = {
                        "file": str(py_file),
                        "line": e.lineno,
                        "error": str(e.msg),
                        "text": e.text,
                    }

                    # Try to fix it
                    if self.fix_syntax_error(py_file, str(e)):
                        self.log(f"Fixed syntax error in {py_file}", "SUCCESS")
                        try:
                            with open(py_file, "rb") as f:
                                compile(f.read(), str(py_file), "exec")
                            self.stats["processed_files"] += 1
                        except:
                            self.errors["syntax_errors"].append(error_info)
                            self.stats["failed_files"] += 1
                    else:
                        self.errors["syntax_errors"].append(error_info)
                        self.stats["failed_files"] += 1

                except Exception as e:
                    self.errors["import_errors"].append(
                        {"file": str(py_file), "error": str(e)}
                    )
                    self.stats["failed_files"] += 1

        self.log(
            f"Validation complete: {self.stats['processed_files']}/{self.stats['total_files']} files valid",
            "INFO",
        )

    def run_sphinx_build(self):
        """Run Sphinx build with comprehensive error handling."""
        self.log("Starting Sphinx documentation build...", "INFO")

        # Clean build directory
        if BUILD_DIR.exists():
            shutil.rmtree(BUILD_DIR)
        BUILD_DIR.mkdir(parents=True, exist_ok=True)

        # Build command with all error handling flags
        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-E",  # Don't use saved environment
            "-a",  # Write all files
            "--keep-going",  # Continue on errors
            "-v",  # Verbose
            "-T",  # Show full traceback
            str(SOURCE_DIR),
            str(BUILD_DIR),
        ]

        env = os.environ.copy()
        env["PYTHONWARNINGS"] = "default"

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1,
            )

            # Process output line by line
            current_error = []
            in_traceback = False

            with open(self.log_file, "a") as log:
                for line in iter(process.stdout.readline, ""):
                    log.write(line)
                    log.flush()

                    line_lower = line.lower()

                    # Track warnings
                    if "warning:" in line_lower:
                        self.stats["warnings_count"] += 1
                        self.errors["warnings"].append(line.strip())
                        if len(self.errors["warnings"]) <= 10:  # Show first 10
                            self.log(line.strip(), "WARNING")

                    # Track errors
                    elif "error:" in line_lower or "exception" in line_lower:
                        self.stats["errors_count"] += 1
                        in_traceback = True
                        current_error = [line.strip()]
                        self.log(line.strip(), "ERROR")

                    # Collect traceback
                    elif in_traceback and ("Traceback" in line or line.startswith(" ")):
                        current_error.append(line.strip())

                    # End of traceback
                    elif in_traceback and current_error and not line.strip():
                        self.errors["build_errors"].append(
                            {
                                "error": (
                                    current_error[0]
                                    if current_error
                                    else "Unknown error"
                                ),
                                "traceback": "\n".join(current_error),
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                        in_traceback = False
                        current_error = []

                    # Progress indicators
                    elif "reading sources..." in line:
                        # Extract percentage if available
                        if "[" in line and "]" in line:
                            self.log(line.strip(), "PROGRESS")
                    elif "writing output..." in line:
                        self.log("Writing HTML files...", "INFO")
                    elif "build succeeded" in line:
                        self.log("Build completed successfully!", "SUCCESS")
                    elif "build finished with problems" in line:
                        self.log("Build completed with errors", "WARNING")

            process.wait()
            return process.returncode

        except Exception as e:
            self.log(f"Build process failed: {e}", "ERROR")
            self.errors["build_errors"].append(
                {
                    "error": "Build process exception",
                    "details": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
            return -1

    def check_output(self):
        """Check generated output."""
        self.log("Checking generated documentation...", "INFO")

        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("**/*.html"))
            self.stats["html_generated"] = len(html_files)

            if html_files:
                self.log(f"Generated {len(html_files)} HTML files", "SUCCESS")

                # Check for key files
                key_files = ["index.html", "genindex.html", "search.html"]
                for key_file in key_files:
                    if (BUILD_DIR / key_file).exists():
                        self.log(f"✓ {key_file} generated", "SUCCESS")
                    else:
                        self.log(f"✗ {key_file} missing", "WARNING")

                # Sample some generated files
                self.log("Sample generated files:", "INFO")
                for html_file in list(html_files)[:5]:
                    self.log(f"  - {html_file.relative_to(BUILD_DIR)}", "")
            else:
                self.log("No HTML files generated!", "ERROR")
        else:
            self.log("Build directory does not exist!", "ERROR")

    def save_error_tracking(self):
        """Save error tracking data."""
        tracking_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "errors": self.errors,
            "log_file": str(self.log_file),
        }

        with open(ERROR_TRACKING_FILE, "w") as f:
            json.dump(tracking_data, f, indent=2)

        self.log(f"Error tracking saved to {ERROR_TRACKING_FILE}", "INFO")

    def generate_report(self):
        """Generate final report."""

        # Summary

        # Errors breakdown
        if any(self.errors.values()):
            for error_type, errors in self.errors.items():
                if errors and error_type != "warnings":
                    for error in errors[:3]:  # Show first 3
                        if isinstance(error, dict):
                            pass
                        else:
                            pass
                    if len(errors) > 3:
                        pass

        # Success indicator
        if self.stats["html_generated"] > 0:
            if self.stats["errors_count"] == 0:
                pass!")
            else:
                passrs")
        else:
            pass")

        # Output location
        if self.stats["html_generated"] > 0:
            index_path = BUILD_DIR / "index.html"
            if index_path.exists():
                pass}")


    def build(self):
        """Main build process."""
        try:
            # Setup
            self.setup_logging()
            self.log("Starting robust documentation build", "INFO")
            self.log(f"Log file: {self.log_file}", "INFO")

            # Step 1: Validate Python files
            self.validate_python_files()

            # Step 2: Run Sphinx build
            self.run_sphinx_build()

            # Step 3: Check output
            self.check_output()

            # Step 4: Save tracking data
            self.save_error_tracking()

            # Step 5: Generate report
            self.generate_report()

            return 0 if self.stats["html_generated"] > 0 else 1

        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            self.errors["build_errors"].append(
                {
                    "error": "Unexpected build error",
                    "details": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
            self.save_error_tracking()
            self.generate_report()
            return 2


def main():
    """Main entry point."""

    builder = DocumentationBuilder()
    return builder.build()


if __name__ == "__main__":
    sys.exit(main())
