"""Nox configuration for Haive project.

Quick Commands:
--------------
    nox -s docs                 # Build docs with autosummary
    nox -s docs_fast            # Build docs without autosummary
    nox -s docs_serve           # Build and serve with auto-reload
    nox -s docs_clean           # Clean build artifacts
    nox -s docs_build           # Enhanced build with organized logs
    nox -s docs_health_check    # Check docs build health
    nox -s docs_analyze         # Analyze recent builds
    nox -s docs_serve_enhanced  # Enhanced server with monitoring
    nox -s docs_recover         # Recover from build failures
    nox -s lint                 # Run linters
    nox -s test                 # Run tests
    nox -s typecheck            # Run type checking
"""

import os
import shutil
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
LOGS_DIR = DOCS_DIR / "logs"
BUILD_REPORTS_DIR = DOCS_DIR / "build_reports"


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build documentation with full autosummary generation."""
    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Enable autosummary generation
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"

    # Build documentation
    session.log("Building documentation with autosummary...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    # Run fix script if it exists
    fix_script = Path("scripts/fix_autosummary_output.py")
    if fix_script.exists():
        session.log("Fixing autosummary output...")
        session.run("poetry", "run", "python", str(fix_script), external=True)

    session.log(f"✅ Documentation built in {BUILD_DIR / 'html'}")
    session.log(f"🌐 Open file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")


@nox.session(python=PYTHON_VERSIONS, name="docs_fast")
def docs_fast(session):
    """Build documentation quickly without autosummary generation."""
    # Install minimal dependencies
    session.run("poetry", "install", "--only", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Disable autosummary generation for speed
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"

    # Build documentation
    session.log("Building documentation (fast mode)...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",
        "-q",  # Quiet mode
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"✅ Fast build complete in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Build and serve documentation with auto-reload using sphinx-autobuild."""
    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    session.log("🔨 Building and serving documentation with auto-reload")
    session.log("🌐 Server at http://localhost:8000")

    # Simple sphinx-autobuild
    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port",
        "8000",
        external=True,
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Cleaned {BUILD_DIR}")

    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")

    # Clean doctrees
    doctrees = DOCS_DIR / "doctrees"
    if doctrees.exists():
        shutil.rmtree(doctrees)
        session.log(f"✅ Cleaned {doctrees}")

    session.log("✅ Documentation artifacts cleaned")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run code quality checks."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "ruff", "check", "packages/", external=True)
    session.run("poetry", "run", "black", "--check", "packages/", external=True)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run test suite."""
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("poetry", "run", "pytest", "-v", external=True)


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session):
    """Run type checking with mypy."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "mypy", "packages/", external=True)


@nox.session
def fix_autosummary(session):
    """Fix autosummary generated files."""
    scripts_dir = Path("scripts")

    # Run fix scripts
    fix_scripts = ["fix_generated_modules.py", "fix_autosummary_output.py"]

    for script in fix_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            session.log(f"Running {script}...")
            session.run("python", str(script_path), external=True)
        else:
            session.log(f"Script not found: {script}")

    session.log("✅ Autosummary fixes applied")


# Enhanced Documentation Build System
# ===================================

def create_build_folder(base_name: str) -> Path:
    """Create a timestamped build folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    build_folder = BUILD_REPORTS_DIR / f"{base_name}_{timestamp}"
    build_folder.mkdir(parents=True, exist_ok=True)
    return build_folder


def parse_sphinx_output(output: str) -> Dict[str, List[str]]:
    """Parse Sphinx output to separate warnings, errors, and info."""
    lines = output.split('\n')
    
    warnings = []
    errors = []
    info = []
    
    for line in lines:
        line_lower = line.lower()
        if 'warning:' in line_lower:
            warnings.append(line)
        elif 'error:' in line_lower or 'failed' in line_lower:
            errors.append(line)
        elif line.strip() and not line.startswith('Running Sphinx'):
            info.append(line)
    
    return {
        'warnings': warnings,
        'errors': errors,
        'info': info
    }


def run_sphinx_with_logging(session, source_dir: Path, build_dir: Path, 
                           build_folder: Path, extra_args: List[str] = None) -> Tuple[int, Dict[str, List[str]]]:
    """Run Sphinx build with comprehensive logging and error handling."""
    extra_args = extra_args or []
    
    # Prepare command
    cmd = [
        "poetry", "run", "sphinx-build",
        "-b", "html",
        "-j", "auto",
        *extra_args,
        str(source_dir),
        str(build_dir)
    ]
    
    # Create log files
    stdout_log = build_folder / "stdout.log"
    stderr_log = build_folder / "stderr.log"
    full_log = build_folder / "full_build.log"
    
    session.log(f"📝 Logs will be saved to: {build_folder}")
    
    # Pre-build checks
    if not source_dir.exists():
        error_msg = f"Source directory does not exist: {source_dir}"
        (build_folder / "fatal_error.log").write_text(error_msg)
        return 1, {'warnings': [], 'errors': [error_msg], 'info': []}
    
    conf_py = source_dir / "conf.py"
    if not conf_py.exists():
        error_msg = f"conf.py not found in {source_dir}"
        (build_folder / "fatal_error.log").write_text(error_msg)
        return 1, {'warnings': [], 'errors': [error_msg], 'info': []}
    
    # Run command with logging
    try:
        session.log(f"🔧 Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=Path.cwd()
        )
        
        # Write logs
        stdout_log.write_text(result.stdout or "")
        stderr_log.write_text(result.stderr or "")
        
        # Combine outputs
        full_output = f"STDOUT:\n{result.stdout or ''}\n\nSTDERR:\n{result.stderr or ''}"
        full_log.write_text(full_output)
        
        # Parse output
        parsed = parse_sphinx_output(full_output)
        
        # Write parsed logs
        if parsed['warnings']:
            (build_folder / "warnings.log").write_text('\n'.join(parsed['warnings']))
        if parsed['errors']:
            (build_folder / "errors.log").write_text('\n'.join(parsed['errors']))
        if parsed['info']:
            (build_folder / "info.log").write_text('\n'.join(parsed['info']))
        
        return result.returncode, parsed
        
    except subprocess.TimeoutExpired:
        error_msg = "Sphinx build timed out after 10 minutes"
        (build_folder / "fatal_error.log").write_text(error_msg)
        return 1, {'warnings': [], 'errors': [error_msg], 'info': []}
    except Exception as e:
        error_msg = f"Failed to run Sphinx: {e}"
        (build_folder / "fatal_error.log").write_text(error_msg)
        return 1, {'warnings': [], 'errors': [error_msg], 'info': []}


def create_build_summary(build_folder: Path, returncode: int, 
                        parsed_output: Dict[str, List[str]], 
                        build_type: str) -> None:
    """Create a build summary report."""
    summary = {
        'build_type': build_type,
        'timestamp': datetime.now().isoformat(),
        'success': returncode == 0,
        'return_code': returncode,
        'warnings_count': len(parsed_output['warnings']),
        'errors_count': len(parsed_output['errors']),
        'info_count': len(parsed_output['info']),
        'files_created': [
            str(f.relative_to(build_folder)) for f in build_folder.glob("*.log")
        ]
    }
    
    # Write JSON summary
    (build_folder / "build_summary.json").write_text(
        json.dumps(summary, indent=2)
    )
    
    # Write human-readable summary
    summary_text = f"""Build Summary
=============

Build Type: {build_type}
Timestamp: {summary['timestamp']}
Success: {'✅' if summary['success'] else '❌'}
Return Code: {returncode}

Counts:
- Warnings: {summary['warnings_count']}
- Errors: {summary['errors_count']}
- Info messages: {summary['info_count']}

Log Files:
{chr(10).join(f'- {f}' for f in summary['files_created'])}
"""
    
    (build_folder / "SUMMARY.md").write_text(summary_text)


@nox.session(python=PYTHON_VERSIONS)
def docs_build(session):
    """Enhanced documentation build with organized logging and error analysis."""
    session.log("🏗️  Starting enhanced documentation build...")
    
    # Setup directories
    BUILD_REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Create build folder
    build_folder = create_build_folder("docs_build")
    session.log(f"📁 Build folder: {build_folder}")
    
    # Install dependencies
    session.log("📦 Installing dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log("🧹 Cleaned previous build")
    
    # Enable autosummary generation
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"
    
    # Run Sphinx with logging
    session.log("🔨 Building documentation...")
    returncode, parsed_output = run_sphinx_with_logging(
        session, 
        SOURCE_DIR, 
        BUILD_DIR / "html",
        build_folder,
        ["--keep-going"]  # Continue on errors
    )
    
    # Create summary
    create_build_summary(build_folder, returncode, parsed_output, "full_build")
    
    # Report results
    session.log("\n" + "="*60)
    session.log("📊 BUILD RESULTS")
    session.log("="*60)
    
    if returncode == 0:
        session.log("✅ Build completed successfully!")
    else:
        session.log("❌ Build failed!")
    
    session.log(f"📈 Warnings: {len(parsed_output['warnings'])}")
    session.log(f"🚨 Errors: {len(parsed_output['errors'])}")
    session.log(f"📝 Info messages: {len(parsed_output['info'])}")
    session.log(f"📁 Logs saved to: {build_folder}")
    
    # Show top errors/warnings
    if parsed_output['errors']:
        session.log("\n🚨 Top Errors:")
        for error in parsed_output['errors'][:5]:
            session.log(f"  - {error[:100]}...")
    
    if parsed_output['warnings']:
        session.log("\n⚠️  Top Warnings:")
        for warning in parsed_output['warnings'][:5]:
            session.log(f"  - {warning[:100]}...")
    
    # Final paths
    if returncode == 0:
        session.log(f"\n🌐 Documentation: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}")
    session.log(f"📋 Full report: {build_folder / 'SUMMARY.md'}")
    
    return returncode


@nox.session(python=PYTHON_VERSIONS)
def docs_analyze(session):
    """Analyze recent documentation builds and provide insights."""
    session.log("📊 Analyzing documentation builds...")
    
    if not BUILD_REPORTS_DIR.exists():
        session.log("❌ No build reports found. Run 'nox -s docs_build' first.")
        return
    
    # Find recent builds
    build_dirs = sorted([d for d in BUILD_REPORTS_DIR.iterdir() if d.is_dir()], 
                       key=lambda x: x.name, reverse=True)
    
    if not build_dirs:
        session.log("❌ No build reports found.")
        return
    
    session.log(f"📈 Found {len(build_dirs)} build reports")
    
    # Analyze recent builds
    for i, build_dir in enumerate(build_dirs[:5]):
        summary_file = build_dir / "build_summary.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            
            status = "✅" if summary['success'] else "❌"
            session.log(f"{status} {build_dir.name}: {summary['warnings_count']}W, {summary['errors_count']}E")
        else:
            session.log(f"❓ {build_dir.name}: No summary found")
    
    # Show latest build details
    latest_build = build_dirs[0]
    session.log(f"\n📋 Latest Build Details: {latest_build.name}")
    session.log("-" * 50)
    
    summary_md = latest_build / "SUMMARY.md"
    if summary_md.exists():
        session.log(summary_md.read_text())
    
    session.log(f"\n📁 Full logs: {latest_build}")


@nox.session(python=PYTHON_VERSIONS)
def docs_health_check(session):
    """Check documentation build health and dependencies."""
    session.log("🔍 Running documentation health check...")
    
    # Check Python environment
    session.log("🐍 Checking Python environment...")
    session.run("python", "--version", external=True)
    
    # Check if poetry is available
    session.log("📦 Checking Poetry...")
    session.run("poetry", "--version", external=True)
    
    # Install dependencies
    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Check Sphinx version
    session.log("📚 Checking Sphinx...")
    session.run("poetry", "run", "sphinx-build", "--version", external=True)
    
    # Check critical directories
    session.log("📁 Checking documentation structure...")
    critical_paths = [
        DOCS_DIR,
        SOURCE_DIR,
        SOURCE_DIR / "conf.py",
        SOURCE_DIR / "index.rst",
    ]
    
    for path in critical_paths:
        if path.exists():
            session.log(f"✅ {path}")
        else:
            session.log(f"❌ Missing: {path}")
    
    # Check package imports
    session.log("📦 Checking package imports...")
    test_imports = [
        "haive.core",
        "haive.agents",
        "haive.tools",
        "haive.games",
    ]
    
    for module in test_imports:
        try:
            session.run("poetry", "run", "python", "-c", f"import {module}; print(f'✅ {module}')", external=True)
        except Exception as e:
            session.log(f"❌ Failed to import {module}: {e}")
    
    # Quick build test
    session.log("🔨 Running quick build test...")
    build_folder = create_build_folder("health_check")
    returncode, parsed_output = run_sphinx_with_logging(
        session, 
        SOURCE_DIR, 
        BUILD_DIR / "html",
        build_folder,
        ["-q", "--keep-going"]
    )
    
    if returncode == 0:
        session.log("✅ Documentation build is healthy!")
    else:
        session.log("❌ Documentation build has issues:")
        session.log(f"🚨 Errors: {len(parsed_output['errors'])}")
        session.log(f"⚠️  Warnings: {len(parsed_output['warnings'])}")
        session.log(f"📁 Detailed logs: {build_folder}")
    
    return returncode


@nox.session(python=PYTHON_VERSIONS)
def docs_serve_enhanced(session):
    """Enhanced documentation server with build monitoring."""
    session.log("🚀 Starting enhanced documentation server...")
    
    # First, do a build to check status
    session.log("🔍 Checking current build status...")
    build_folder = create_build_folder("serve_check")
    
    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Quick build check
    returncode, parsed_output = run_sphinx_with_logging(
        session, 
        SOURCE_DIR, 
        BUILD_DIR / "html",
        build_folder,
        ["-q"]  # Quiet mode
    )
    
    if returncode != 0:
        session.log("⚠️  Build has issues. Starting server anyway...")
        session.log(f"📁 Build logs: {build_folder}")
    
    # Start server
    session.log("🌐 Starting server at http://localhost:8000")
    session.log("📝 Auto-reload enabled - changes will trigger rebuilds")
    
    session.run(
        "poetry", "run", "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port", "8000",
        "--host", "0.0.0.0",
        "--watch", "../packages",  # Watch package changes
        "--ignore", "*.pyc",
        "--ignore", "*.pyo",
        "--ignore", "*~",
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_recover(session):
    """Recover from documentation build failures with systematic fixes."""
    session.log("🔧 Starting documentation recovery process...")
    
    # Step 1: Clean everything
    session.log("🧹 Step 1: Deep clean...")
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Remove all build artifacts
    cleanup_dirs = [
        BUILD_DIR,
        DOCS_DIR / "doctrees",
        SOURCE_DIR / "api" / "generated",
        Path(".pytest_cache"),
        Path("__pycache__"),
    ]
    
    for dir_path in cleanup_dirs:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            session.log(f"✅ Cleaned {dir_path}")
    
    # Step 2: Check Python path and imports
    session.log("🐍 Step 2: Checking Python environment...")
    session.run("poetry", "run", "python", "-c", "import sys; print('Python path:'); [print(p) for p in sys.path]", external=True)
    
    # Step 3: Test critical imports
    session.log("📦 Step 3: Testing critical imports...")
    critical_imports = [
        "import haive.core",
        "import haive.agents",
        "import haive.tools",
        "import haive.games",
    ]
    
    for import_test in critical_imports:
        try:
            session.run("poetry", "run", "python", "-c", import_test, external=True)
            session.log(f"✅ {import_test}")
        except Exception as e:
            session.log(f"❌ {import_test} failed: {e}")
    
    # Step 4: Regenerate API documentation
    session.log("📚 Step 4: Regenerating API documentation...")
    try:
        session.run("poetry", "run", "sphinx-apidoc", 
                   "-f", "-o", str(SOURCE_DIR / "api"), 
                   "packages/", external=True)
        session.log("✅ API documentation regenerated")
    except Exception as e:
        session.log(f"⚠️  API doc generation failed: {e}")
    
    # Step 5: Try minimal build
    session.log("🔨 Step 5: Attempting minimal build...")
    build_folder = create_build_folder("recovery")
    
    # Try without autosummary first
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    
    returncode, parsed_output = run_sphinx_with_logging(
        session, 
        SOURCE_DIR, 
        BUILD_DIR / "html",
        build_folder,
        ["-E", "-a", "--keep-going"]  # Fresh build, all files, continue on errors
    )
    
    # Step 6: Report results
    session.log("\n" + "="*60)
    session.log("🔧 RECOVERY RESULTS")
    session.log("="*60)
    
    if returncode == 0:
        session.log("✅ Recovery successful! Documentation build is working.")
        session.log(f"🌐 Documentation: file://{(BUILD_DIR / 'html' / 'index.html').absolute()}")
    else:
        session.log("❌ Recovery partially successful but issues remain:")
        session.log(f"🚨 Errors: {len(parsed_output['errors'])}")
        session.log(f"⚠️  Warnings: {len(parsed_output['warnings'])}")
        
        # Show top errors
        if parsed_output['errors']:
            session.log("\n🚨 Top Errors to Fix:")
            for error in parsed_output['errors'][:3]:
                session.log(f"  - {error}")
        
        session.log(f"\n📁 Full recovery logs: {build_folder}")
    
    return returncode
