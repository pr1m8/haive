"""Clean and organized noxfile for Haive project.

This noxfile imports all sessions from modular files in the noxfiles/
directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to Python path to import noxfiles package
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root.absolute()))

from noxfiles.session_docs import (
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
from noxfiles.session_docs_error_collector import (
    docs_phased_with_error_collection,
    review_errors,
)
from noxfiles.session_docs_examples import (
    docs_autobuild_no_examples,
    docs_compare_examples,
    docs_dev,
    docs_minimal_no_examples,
    docs_no_examples,
    docs_prod,
    docs_with_examples,
)
from noxfiles.session_docs_package import docs_multi, docs_package, docs_quick
from noxfiles.session_docs_phased import docs_phased, docs_phased_no_examples
from noxfiles.session_docs_modular import docs_fast_build
from noxfiles.session_docs_debug import docs_debug_enhanced, docs_minimal_test
from noxfiles.session_docs_testing import (
    docs_test_all,
    docs_test_docstrings,
    docs_test_examples,
    docs_test_metadata,
    docs_test_notebooks,
    docs_test_pipeline,
    docs_test_prose,
    docs_test_spelling,
)
from noxfiles.session_examples import (
    examples,
    examples_docs,
    examples_rag,
    examples_react,
    examples_simple,
    run_example,
    validate_examples,
)
from noxfiles.session_lint import format, lint, mypy, security
from noxfiles.session_test import test, test_integration, test_package, test_quick

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
    # Granular documentation testing
    "docs_compare_configs",
    "docs_compare_examples",
    "docs_coverage",
    # Aliases
    "docs_d",
    # Documentation analysis
    "docs_debug",
    "docs_dev",
    "docs_dev",
    "docs_dl",
    "docs_fast",
    "docs_fast_dev",
    "docs_full",
    "docs_history",
    "docs_linkcheck",
    "docs_live",
    "docs_logs",
    "docs_minimal_no_examples",
    "docs_multi",
    "docs_no_examples",
    # Package-specific documentation
    "docs_package",
    "docs_pdf",
    # Error collection and review
    "docs_phased",
    "docs_phased_no_examples",
    "docs_phased_with_error_collection",
    "docs_prod",
    "docs_quality",
    "docs_quick",
    "docs_quick_test",
    "docs_s",
    "docs_serve",
    # Documentation testing
    "docs_test_all",
    "docs_test_config",
    "docs_test_docstrings",
    "docs_test_examples",
    "docs_test_incremental",
    "docs_test_metadata",
    "docs_test_notebooks",
    "docs_test_package",
    "docs_test_pipeline",
    "docs_test_prose",
    "docs_test_spelling",
    "docs_with_examples",
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
    "review_errors",
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
        ],
    )

# Print help when running nox without arguments
if __name__ == "__main__":
    list_sessions()
