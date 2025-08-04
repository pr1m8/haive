"""Clean and organized noxfile for Haive project.

This noxfile imports all sessions from modular files in the noxfiles/
directory.
"""

from __future__ import annotations

from pathlib import Path
import sys

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
from session_docs_error_collector import (
    docs_phased_with_error_collection,
    review_errors,
)
from session_docs_examples import (
    docs_autobuild_no_examples,
    docs_compare_examples,
    docs_dev,
    docs_minimal_no_examples,
    docs_no_examples,
    docs_prod,
    docs_with_examples,
)
from session_docs_package import (
    docs_multi,
    docs_package,
    docs_quick,
)
from session_docs_phased import (
    docs_phased_no_examples, )
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
from session_examples import (
    examples,
    examples_docs,
    examples_rag,
    examples_react,
    examples_simple,
    run_example,
    validate_examples,
)
from session_lint import format, lint, mypy, security
from session_test import test, test_integration, test_package, test_quick

# Add noxfiles to Python path to import session modules
noxfiles_dir = Path(__file__).parent / "noxfiles"
sys.path.insert(0, str(noxfiles_dir))

# Import all documentation sessions

# Import error collection sessions

# Import example-aware documentation sessions

# Import modular documentation build sessions

# Import package-specific documentation sessions

# Import phased documentation sessions

# Import documentation testing sessions

# Import example sessions

# Import linting sessions

# Import testing sessions

# Import granular documentation testing sessions (temporarily disabled due to file corruption)
# from session_docs_granular import (
#     docs_compare_configs,
#     docs_dev,
#     docs_quick_test,
#     docs_test_config,
#     docs_test_incremental,
#     docs_test_package,

# Import memory-aware sessions if available
try:
    pass

    MEMORY_SESSIONS_AVAILABLE = True
except ImportError:
    MEMORY_SESSIONS_AVAILABLE = False

# Convenience aliases
docs_d = docs  # nox -s d
docs_s = docs_serve  # nox -s s
docs_dl = docs_autobuild  # nox -s dl

# Example-aware aliases
docs_fast_dev = docs_no_examples  # nox -s docs_fast_dev (no examples)
docs_live = docs_autobuild_no_examples  # nox -s docs_live (auto-build without examples)


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
    "docs_autobuild_no_examples",
    "docs_clean",
    "docs_compare_examples",
    "docs_coverage",
    "docs_dev",
    "docs_minimal_no_examples",
    "docs_no_examples",
    "docs_prod",
    "docs_with_examples",
    # Aliases
    "docs_d",
    "docs_fast_dev",
    "docs_live",
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
    # Granular documentation testing
    "docs_compare_configs",
    "docs_dev",
    "docs_quick_test",
    "docs_test_config",
    "docs_test_incremental",
    "docs_test_package",
    # Package-specific documentation
    "docs_package",
    "docs_quick",
    "docs_multi",
    # Error collection and review
    "docs_phased_no_examples",
    "docs_phased_with_error_collection",
    "review_errors",
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
    __all__.extend([
        "docs_adaptive",
        "docs_autobuild_memory",
        "docs_fast_memory",
        "docs_memory_safe",
        "docs_monitor",
    ], )

# Print help when running nox without arguments
if __name__ == "__main__":
    list_sessions()
