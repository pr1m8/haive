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
    docs_nitpicky,
    docs_pdf,
    docs_quality,
    docs_serve,
    docs_test,
)

# Import phased documentation sessions
from session_docs_phased import docs_diagnose, docs_phased, docs_validate

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

    if MEMORY_SESSIONS_AVAILABLE:
        pass


# Export sessions
__all__ = [
    # Documentation building
    "docs",
    "docs_autobuild",
    "docs_clean",
    "docs_coverage",
    # Aliases
    "docs_d",
    # Documentation analysis
    "docs_debug",
    "docs_dl",
    "docs_fast",
    "docs_full",
    "docs_history",
    "docs_linkcheck",
    "docs_logs",
    "docs_pdf",
    "docs_quality",
    "docs_s",
    "docs_serve",
    # Documentation testing
    "docs_test_all",
    "docs_test_docstrings",
    "docs_test_examples",
    "docs_test_metadata",
    "docs_test_notebooks",
    "docs_test_pipeline",
    "docs_test_prose",
    "docs_test_spelling",
    # Examples
    "examples",
    "examples_docs",
    "examples_rag",
    "examples_react",
    "examples_simple",
    "format",
    # Code quality
    "lint",
    "mypy",
    "run_example",
    "security",
    # Testing
    "test",
    "test_integration",
    "test_package",
    "test_quick",
    "validate_examples",
]

# Add memory sessions if available
if MEMORY_SESSIONS_AVAILABLE:
    __all__.extend(
        [
            "docs_adaptive",
            "docs_autobuild_memory",
            "docs_fast_memory",
            "docs_memory_safe",
            "docs_monitor",
        ]
    )

# Print help when running nox without arguments
if __name__ == "__main__":
    list_sessions()
