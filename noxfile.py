import os
import shutil
import subprocess
import webbrowser
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Any

import nox

DOCS_SOURCE = "docs/source"
DOCS_BUILD = "docs/_build"
CONF_DIR = DOCS_SOURCE
LOG_DIR = Path("logs/docs/build")


def get_log_path() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{timestamp}.log"


def get_debug_log_path() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{timestamp}_debug.log"


def analyze_sphinx_log(log_path: Path) -> Dict[str, Any]:
    """Analyze Sphinx log for errors and warnings with context."""
    with log_path.open(encoding="utf-8") as f:
        lines = f.readlines()
    
    results = {
        "warnings": [],
        "errors": [],
        "import_errors": [],
        "extension_errors": [],
        "autosummary_errors": [],
        "other_issues": [],
        "total_lines": len(lines)
    }
    
    # Analyze line by line with context
    for i, line in enumerate(lines):
        # Get context (3 lines before and after)
        context_start = max(0, i - 3)
        context_end = min(len(lines), i + 4)
        context = lines[context_start:context_end]
        
        if "WARNING" in line:
            results["warnings"].append({
                "line_number": i + 1,
                "message": line.strip(),
                "context": [l.strip() for l in context]
            })
            
            # Check for specific warning types
            if "Failed to import" in line:
                results["import_errors"].append({
                    "line_number": i + 1,
                    "message": line.strip(),
                    "module": extract_module_name(line),
                    "hints": extract_import_hints(lines, i)
                })
        
        elif "ERROR" in line or "error:" in line.lower():
            results["errors"].append({
                "line_number": i + 1,
                "message": line.strip(),
                "context": [l.strip() for l in context],
                "traceback": extract_traceback(lines, i)
            })
            
            if "Extension error" in line:
                results["extension_errors"].append({
                    "line_number": i + 1,
                    "message": line.strip(),
                    "extension": extract_extension_name(line)
                })
                
            if "autosummary" in line.lower():
                results["autosummary_errors"].append({
                    "line_number": i + 1,
                    "message": line.strip(),
                    "module": extract_module_from_autosummary_error(line)
                })
        
        elif "Exception" in line or "Traceback" in line:
            results["other_issues"].append({
                "line_number": i + 1,
                "message": line.strip(),
                "traceback": extract_traceback(lines, i)
            })
    
    return results


def extract_module_name(line: str) -> str:
    """Extract module name from import error line."""
    import re
    match = re.search(r"Failed to import (.+?)\.?$", line)
    if match:
        return match.group(1)
    return "unknown"


def extract_import_hints(lines: List[str], error_index: int) -> List[str]:
    """Extract import error hints from subsequent lines."""
    hints = []
    for i in range(error_index + 1, min(error_index + 10, len(lines))):
        if "* " in lines[i]:
            hints.append(lines[i].strip())
        elif lines[i].strip() and not lines[i].startswith(" "):
            break
    return hints


def extract_extension_name(line: str) -> str:
    """Extract extension name from error line."""
    import re
    match = re.search(r"\(([^)]+)\)", line)
    if match:
        return match.group(1)
    return "unknown"


def extract_module_from_autosummary_error(line: str) -> str:
    """Extract module name from autosummary error."""
    import re
    match = re.search(r"no module named (.+?)[\s)]", line.lower())
    if match:
        return match.group(1)
    return "unknown"


def extract_traceback(lines: List[str], start_index: int) -> List[str]:
    """Extract traceback from error location."""
    traceback_lines = []
    for i in range(start_index, min(start_index + 20, len(lines))):
        line = lines[i].strip()
        if line:
            traceback_lines.append(line)
        if "File" in line or "line" in line:
            continue
        if not line or (i > start_index + 1 and not line.startswith(" ")):
            break
    return traceback_lines


def print_analysis_report(session: nox.Session, analysis: Dict[str, Any], log_path: Path):
    """Print a detailed analysis report."""
    session.log("\n" + "="*80)
    session.log(f"📊 SPHINX BUILD ANALYSIS REPORT")
    session.log(f"📝 Log file: {log_path}")
    session.log(f"📏 Total lines in log: {analysis['total_lines']}")
    session.log("="*80 + "\n")
    
    # Import Errors
    if analysis["import_errors"]:
        session.log(f"\n🚫 IMPORT ERRORS ({len(analysis['import_errors'])} found):")
        session.log("-" * 60)
        for i, err in enumerate(analysis["import_errors"][:10], 1):
            session.log(f"\n{i}. Module: {err['module']}")
            session.log(f"   Line {err['line_number']}: {err['message']}")
            if err['hints']:
                session.log("   Hints:")
                for hint in err['hints']:
                    session.log(f"     {hint}")
    
    # Extension Errors
    if analysis["extension_errors"]:
        session.log(f"\n🔌 EXTENSION ERRORS ({len(analysis['extension_errors'])} found):")
        session.log("-" * 60)
        for err in analysis["extension_errors"]:
            session.log(f"Extension: {err['extension']}")
            session.log(f"Line {err['line_number']}: {err['message']}")
    
    # Autosummary Errors
    if analysis["autosummary_errors"]:
        session.log(f"\n📑 AUTOSUMMARY ERRORS ({len(analysis['autosummary_errors'])} found):")
        session.log("-" * 60)
        for err in analysis["autosummary_errors"][:5]:
            session.log(f"Module: {err['module']}")
            session.log(f"Line {err['line_number']}: {err['message']}")
    
    # General Errors
    other_errors = [e for e in analysis["errors"] 
                    if e not in analysis["extension_errors"] 
                    and e not in analysis["autosummary_errors"]]
    if other_errors:
        session.log(f"\n❌ OTHER ERRORS ({len(other_errors)} found):")
        session.log("-" * 60)
        for err in other_errors[:5]:
            session.log(f"\nLine {err['line_number']}: {err['message']}")
            if err.get('traceback'):
                session.log("Traceback:")
                for line in err['traceback'][:10]:
                    session.log(f"  {line}")
    
    # Summary
    session.log("\n" + "="*80)
    session.log("📈 SUMMARY:")
    session.log(f"  - Total Warnings: {len(analysis['warnings'])}")
    session.log(f"  - Total Errors: {len(analysis['errors'])}")
    session.log(f"  - Import Errors: {len(analysis['import_errors'])}")
    session.log(f"  - Extension Errors: {len(analysis['extension_errors'])}")
    session.log(f"  - Autosummary Errors: {len(analysis['autosummary_errors'])}")
    session.log("="*80 + "\n")


@nox.session(name="docs")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation with detailed debugging."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")
    
    log_path = get_log_path()
    debug_log_path = get_debug_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    session.log(f"🛠️  Building docs...")
    session.log(f"📝 Main log: {log_path}")
    session.log(f"🔍 Debug log: {debug_log_path}")
    
    # Set environment variables for better debugging
    env = os.environ.copy()
    env.update({
        "PYTHONWARNINGS": "default",  # Show all warnings
        "SPHINX_DEBUG": "1",          # Enable Sphinx debug mode
        "PYTHONUNBUFFERED": "1",      # Unbuffered output
    })
    
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b", "html",
        "-c", CONF_DIR,
        "-v",  # Verbose
        "-E",  # Don't use cached environment
        "-T",  # Show full traceback on error
        "--keep-going",  # Continue on errors
        "-w", str(log_path),  # Write warnings to log
        DOCS_SOURCE,
        DOCS_BUILD,
    ]
    
    session.log(f"🚀 Running command: {' '.join(cmd)}")
    
    # Run with both stdout and stderr captured
    with debug_log_path.open("w", encoding="utf-8") as debug_file:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            bufsize=1,  # Line buffered
        )
        
        # Stream output in real-time
        session.log("\n📋 Live Output:")
        session.log("-" * 60)
        
        output_lines = []
        for line in process.stdout:
            line = line.rstrip()
            output_lines.append(line)
            debug_file.write(line + "\n")
            debug_file.flush()
            
            # Show important lines in real-time
            if any(keyword in line for keyword in ["WARNING", "ERROR", "Failed", "Exception"]):
                session.log(f"  ⚠️  {line}")
        
        process.wait()
        return_code = process.returncode
    
    # Analyze the log
    session.log("\n🔍 Analyzing build output...")
    analysis = analyze_sphinx_log(log_path)
    
    # Print detailed analysis
    print_analysis_report(session, analysis, log_path)
    
    # Determine success/failure
    if return_code == 0:
        session.log("✅ Sphinx build completed (but may have warnings)")
    else:
        session.log(f"❌ Sphinx build failed with return code {return_code}")
    
    # Provide actionable suggestions
    if analysis["import_errors"]:
        session.log("\n💡 SUGGESTIONS FOR IMPORT ERRORS:")
        session.log("1. Add modules to autodoc_mock_imports in conf.py")
        session.log("2. Check if all packages are properly installed")
        session.log("3. Verify sys.path includes all package directories")
        session.log("4. Consider using autosummary_mock_imports")
    
    if analysis["autosummary_errors"]:
        session.log("\n💡 SUGGESTIONS FOR AUTOSUMMARY ERRORS:")
        session.log("1. Use :recursive: cautiously - it may try to import everything")
        session.log("2. Be explicit about which modules to document")
        session.log("3. Add problematic modules to autosummary_mock_imports")
    
    session.log(f"\n📚 Docs output: {DOCS_BUILD}/index.html")
    session.log(f"📊 Full analysis saved to: {log_path}")
    session.log(f"🔍 Debug output saved to: {debug_log_path}")


@nox.session(name="docs-live")
def live_docs(session: nox.Session) -> None:
    """Start live-reloading Sphinx server with enhanced debugging."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")
    
    session.log("🔴 Starting live documentation server with debugging enabled...")
    
    env = os.environ.copy()
    env.update({
        "PYTHONWARNINGS": "default",
        "SPHINX_DEBUG": "1",
        "PYTHONUNBUFFERED": "1",
    })
    
    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        DOCS_SOURCE,
        DOCS_BUILD,
        "--host", "0.0.0.0",
        "--port", "8001",
        "--open-browser",
        "--watch", "README.md",
        "--ignore", DOCS_BUILD,
        "-v",  # Verbose
        "-E",  # Don't use cached environment
        "--keep-going",  # Continue on errors
        env=env
    )


@nox.session(name="view-docs")
def view_docs(session: nox.Session) -> None:
    """Open the built documentation in the default web browser."""
    index_path = Path(DOCS_BUILD) / "index.html"
    if not index_path.exists():
        session.error(f"{index_path} not found. Run `nox -s docs` first.")
    webbrowser.open(index_path.resolve().as_uri())
    session.log(f"📖 Opened docs at: {index_path}")


@nox.session(name="docs-debug")
def debug_imports(session: nox.Session) -> None:
    """Debug import issues by testing imports directly."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")
    
    session.log("🔍 Testing imports directly...")
    
    # Test importing each package
    packages = ["haive.core", "haive.agents", "haive.tools", "haive.games", "haive.dataflow", "haive.prebuilt"]
    
    for package in packages:
        session.log(f"\n📦 Testing import: {package}")
        try:
            session.run(
                "python", "-c", 
                f"import sys; sys.path.extend(['{DOCS_SOURCE}', 'packages/haive-core/src', 'packages/haive-agents/src', 'packages/haive-tools/src', 'packages/haive-games/src', 'packages/haive-dataflow/src', 'packages/haive-prebuilt/src']); import {package}; print(f'✅ Successfully imported {package}')",
                external=True
            )
        except Exception as e:
            session.log(f"❌ Failed to import {package}: {e}")
            # Try to get more details
            session.run(
                "python", "-c",
                f"import traceback; import sys; sys.path.extend(['{DOCS_SOURCE}', 'packages/haive-core/src', 'packages/haive-agents/src', 'packages/haive-tools/src', 'packages/haive-games/src', 'packages/haive-dataflow/src', 'packages/haive-prebuilt/src']); exec('try:\\n    import {package}\\nexcept Exception as e:\\n    traceback.print_exc()')",
                external=True
            )