"""Clean and organized noxfile for Haive project.

This noxfile imports all sessions from modular files in the noxfiles/ directory.
"""

import sys
from pathlib import Path

# Add noxfiles to Python path to import session modules
noxfiles_dir = Path(__file__).parent / "noxfiles"
sys.path.insert(0, str(noxfiles_dir))

# Import all documentation sessions
from session_docs import (
    docs,
    docs_autobuild,
    docs_clean,
    docs_coverage,
    docs_debug,
    docs_fast,
    docs_full,
    docs_history,
    docs_linkcheck,
    docs_logs,
    docs_pdf,
    docs_quality,
    docs_serve,
)

# Import documentation testing sessions
from session_docs_testing import (
    docs_test_all,
    docs_test_docstrings,
    docs_test_examples,
    docs_test_metadata,
    docs_test_notebooks,
    docs_test_pipeline,
    docs_test_prose,
    docs_test_spelling,
)

# Import example sessions
from session_examples import (
    examples,
    examples_docs,
    examples_rag,
    examples_react,
    examples_simple,
    run_example,
    validate_examples,
)

# Import linting sessions
from session_lint import format, lint, mypy, security

# Import testing sessions
from session_test import test, test_integration, test_package, test_quick

# Import memory-aware sessions if available
try:
    from session_docs_memory import (
        docs_adaptive,
        docs_autobuild_memory,
        docs_fast_memory,
        docs_memory_safe,
        docs_monitor,
    )

    MEMORY_SESSIONS_AVAILABLE = True
except ImportError:
    MEMORY_SESSIONS_AVAILABLE = False

# Convenience aliases
docs_d = docs  # nox -s d
docs_s = docs_serve  # nox -s s
docs_dl = docs_autobuild  # nox -s dl


# Define session groups for easy execution
def list_sessions():
    """Print organized list of available sessions."""
    print(
        """
╔═══════════════════════════════════════════════════════════════════╗
║                    🚀 Haive Nox Sessions                          ║
╚═══════════════════════════════════════════════════════════════════╝

📚 Documentation Building
  nox -s docs           # Standard build with logging
  nox -s docs_fast      # Fast build (continues on errors)
  nox -s docs_full      # Full build with autosummary
  nox -s docs_clean     # Clean all build artifacts
  nox -s docs_serve     # Serve built docs (port 8003)
  nox -s docs_autobuild # Auto-rebuild on changes
  nox -s docs_pdf       # Generate PDF documentation

📊 Documentation Analysis
  nox -s docs_debug     # Analyze recent build logs
  nox -s docs_history   # Show build history
  nox -s docs_logs      # Manage build logs
  nox -s docs_quality   # Run quality checks
  nox -s docs_linkcheck # Check for broken links
  nox -s docs_coverage  # Check documentation coverage

🧪 Documentation Testing
  nox -s docs_test_all        # Run all doc tests
  nox -s docs_test_docstrings # Test docstring quality
  nox -s docs_test_examples   # Test code examples
  nox -s docs_test_notebooks  # Test Jupyter notebooks
  nox -s docs_test_spelling   # Spell checking
  nox -s docs_test_prose      # Prose quality
  nox -s docs_test_metadata   # Package metadata
  nox -s docs_test_pipeline   # Full quality pipeline

🔍 Code Quality
  nox -s lint      # Run all linters
  nox -s format    # Format code
  nox -s mypy      # Type checking
  nox -s security  # Security scan

🧪 Testing
  nox -s test                         # Run all tests
  nox -s test_quick                   # Quick test run
  nox -s test_package -- haive-agents # Test specific package
  nox -s test_integration             # Integration tests

🚀 Examples
  nox -s examples                        # Run all examples
  nox -s examples_simple                  # Run SimpleAgent examples
  nox -s examples_react                   # Run ReactAgent examples
  nox -s examples_rag                     # Run RAG agent examples
  nox -s examples_docs                    # Generate docs examples
  nox -s run_example -- simple_agent.py  # Run specific example
  nox -s validate_examples               # Validate examples

⚡ Quick Shortcuts
  nox -s d   # Build docs (alias for docs)
  nox -s s   # Serve docs (alias for docs_serve)
  nox -s dl  # Docs live (alias for docs_autobuild)
"""
    )

    if MEMORY_SESSIONS_AVAILABLE:
        print(
            """
🧠 Memory-Aware Sessions (Available)
  nox -s docs_monitor       # Check system resources
  nox -s docs_memory_safe   # Memory-safe build
  nox -s docs_adaptive      # Adaptive resource build
  nox -s docs_fast_memory   # Fast build with monitoring
  nox -s docs_autobuild_memory # Memory-aware autobuild
"""
        )


# Export sessions
__all__ = [
    # Documentation building
    "docs",
    "docs_fast",
    "docs_full",
    "docs_clean",
    "docs_serve",
    "docs_autobuild",
    "docs_pdf",
    # Documentation analysis
    "docs_debug",
    "docs_history",
    "docs_logs",
    "docs_quality",
    "docs_linkcheck",
    "docs_coverage",
    # Documentation testing
    "docs_test_all",
    "docs_test_docstrings",
    "docs_test_examples",
    "docs_test_notebooks",
    "docs_test_spelling",
    "docs_test_prose",
    "docs_test_metadata",
    "docs_test_pipeline",
    # Code quality
    "lint",
    "format",
    "mypy",
    "security",
    # Testing
    "test",
    "test_quick",
    "test_package",
    "test_integration",
    # Examples
    "examples",
    "examples_simple",
    "examples_react",
    "examples_rag",
    "examples_docs",
    "run_example",
    "validate_examples",
    # Aliases
    "docs_d",
    "docs_s",
    "docs_dl",
]

# Add memory sessions if available
if MEMORY_SESSIONS_AVAILABLE:
    __all__.extend(
        [
            "docs_monitor",
            "docs_memory_safe",
            "docs_adaptive",
            "docs_fast_memory",
            "docs_autobuild_memory",
        ]
    )

# Print help when running nox without arguments
if __name__ == "__main__":
    list_sessions()
