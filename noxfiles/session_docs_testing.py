"""Documentation testing sessions from original noxfile."""

from datetime import datetime
import json
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
QUALITY_REPORTS_DIR = DOCS_DIR / "quality-reports"
PACKAGES_DIR = Path("packages")
PACKAGE_NAMES = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

# Ensure directories exist
QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_all(session):
    """Run ALL documentation tests - comprehensive quality check."""
    session.log("🚀 Running comprehensive documentation testing suite...")

    results = {}

    # Run all test sessions
    test_sessions = [
        "docs_test_docstrings",
        "docs_test_examples",
        "docs_test_notebooks",
        "docs_test_spelling",
        "docs_test_prose",
        "docs_test_metadata",
    ]

    for test_session in test_sessions:
        session.log(f"\n{'=' * 60}")
        session.log(f"Running: {test_session}")
        session.log(f"{'=' * 60}")

        try:
            session.notify(test_session)
            results[test_session] = "✅ PASSED"
        except Exception as e:
            results[test_session] = f"❌ FAILED: {e}"

    # Generate summary report
    session.log("\n" + "=" * 60)
    session.log("📊 COMPREHENSIVE TEST SUMMARY")
    session.log("=" * 60)

    for test_name, result in results.items():
        session.log(f"{result} {test_name}")

    # Save results
    report_file = (
        QUALITY_REPORTS_DIR /
        f"comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)

    session.log(f"\n📋 Full report saved to: {report_file}")


@nox.session(python=PYTHON_VERSIONS)
def docs_test_docstrings(session):
    """Test docstring coverage and quality with multiple tools."""
    session.log("📊 Testing docstring coverage and quality...")

    # Install dependencies
    session.run("poetry", "install", "--with", "dev", external=True)

    results = {}

    # 1. Interrogate - Docstring coverage
    session.log("\n🔍 Running interrogate (docstring coverage)...")
    try:
        session.run(
            "poetry",
            "run",
            "interrogate",
            "-vv",
            "packages/",
            "--generate-badge",
            "docs/badges/",
            "--fail-under",
            "80",
            "--exclude",
            "packages/haive-prebuilt",
            external=True,
        )
        results["interrogate"] = {"status": "passed", "coverage": ">80%"}
        session.log("✅ Interrogate: Good docstring coverage")
    except Exception as e:
        results["interrogate"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Interrogate: Low coverage - {e}")

    # 2. Darglint - Docstring/function matching
    session.log("\n🔍 Running darglint (docstring consistency)...")
    try:
        session.run(
            "bash",
            "-c",
            "find packages/ -name '*.py' -not -path 'packages/haive-prebuilt/*' | xargs poetry run darglint -v 2",
            external=True,
        )
        results["darglint"] = {"status": "passed"}
        session.log("✅ Darglint: Docstrings match functions")
    except Exception as e:
        results["darglint"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Darglint: Inconsistencies found - {e}")

    # 3. Pydocstyle - Google style compliance
    session.log("\n🔍 Running pydocstyle (Google style)...")
    try:
        session.run(
            "poetry",
            "run",
            "pydocstyle",
            "packages/",
            "--convention=google",
            "--match-dir='^(?!haive-prebuilt).*'",
            external=True,
        )
        results["pydocstyle"] = {"status": "passed"}
        session.log("✅ Pydocstyle: Google style compliant")
    except Exception as e:
        results["pydocstyle"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Pydocstyle: Style violations - {e}")

    # 4. docstr-coverage - Detailed coverage report
    session.log("\n🔍 Running docstr-coverage...")
    try:
        for package in PACKAGE_NAMES:
            if package != "haive-prebuilt":
                package_path = PACKAGES_DIR / package
                if package_path.exists():
                    session.run(
                        "poetry",
                        "run",
                        "docstr-coverage",
                        str(package_path),
                        "--failunder",
                        "70",
                        external=True,
                    )
        results["docstr-coverage"] = {"status": "passed", "coverage": ">70%"}
        session.log("✅ docstr-coverage: Good coverage")
    except Exception as e:
        results["docstr-coverage"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ docstr-coverage: Low coverage - {e}")

    _generate_quality_report(session, "docstring_quality", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_examples(session):
    """Test code examples in documentation with pytest-doctestplus."""
    session.log("🧪 Testing code examples in documentation...")

    # Install dependencies
    session.run("poetry", "install", "--with", "dev,docs", external=True)

    # Set Python path for namespaced imports
    import os

    for package in PACKAGE_NAMES:
        src_path = PACKAGES_DIR / package / "src"
        if src_path.exists():
            os.environ[
                "PYTHONPATH"] = f"{src_path}:{os.environ.get('PYTHONPATH', '')}"

    results = {}

    # 1. Test Python docstrings with doctestplus
    session.log("\n🔍 Testing Python docstrings...")
    try:
        session.run(
            "poetry",
            "run",
            "pytest",
            "--doctest-plus",
            "--doctest-modules",
            "--doctest-continue-on-failure",
            "--ignore=packages/haive-prebuilt",
            "packages/",
            "-v",
            external=True,
        )
        results["python_doctests"] = {"status": "passed"}
        session.log("✅ Python doctests passed")
    except Exception as e:
        results["python_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Python doctests failed - {e}")

    # 2. Test RST documentation
    session.log("\n🔍 Testing RST documentation...")
    try:
        session.run(
            "poetry",
            "run",
            "pytest",
            "--doctest-plus",
            "--doctest-rst",
            "docs/",
            "-v",
            external=True,
        )
        results["rst_doctests"] = {"status": "passed"}
        session.log("✅ RST doctests passed")
    except Exception as e:
        results["rst_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ RST doctests failed - {e}")

    # 3. Test Markdown documentation
    session.log("\n🔍 Testing Markdown documentation...")
    try:
        session.run(
            "poetry",
            "run",
            "pytest",
            "--markdown-docs",
            "README.md",
            "project_docs/",
            "-v",
            external=True,
        )
        results["markdown_doctests"] = {"status": "passed"}
        session.log("✅ Markdown doctests passed")
    except Exception as e:
        results["markdown_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Markdown doctests failed - {e}")

    # 4. Test with sphinx doctest extension
    session.log("\n🔍 Testing with Sphinx doctest...")
    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "doctest",
            str(SOURCE_DIR),
            str(DOCS_DIR / "build" / "doctest"),
            external=True,
        )
        results["sphinx_doctests"] = {"status": "passed"}
        session.log("✅ Sphinx doctests passed")
    except Exception as e:
        results["sphinx_doctests"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Sphinx doctests failed - {e}")

    _generate_quality_report(session, "example_testing", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_notebooks(session):
    """Test Jupyter notebooks in documentation."""
    session.log("📓 Testing Jupyter notebooks...")

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    results = {}

    # Find all notebooks
    notebooks = list(Path(".").rglob("*.ipynb"))
    session.log(f"Found {len(notebooks)} notebooks to test")

    # Test each notebook
    for notebook in notebooks:
        session.log(f"\n📓 Testing: {notebook}")
        try:
            session.run(
                "poetry",
                "run",
                "pytest",
                "--nbval",
                str(notebook),
                external=True,
            )
            results[str(notebook)] = {"status": "passed"}
            session.log(f"✅ {notebook.name} passed")
        except Exception as e:
            results[str(notebook)] = {"status": "failed", "error": str(e)}
            session.log(f"❌ {notebook.name} failed - {e}")

    _generate_quality_report(session, "notebook_testing", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_spelling(session):
    """Advanced spell checking with multiple tools."""
    session.log("🔤 Running advanced spell checking...")

    # Install dependencies
    session.run("poetry", "install", "--with", "dev", external=True)

    results = {}

    # 1. Codespell
    session.log("\n🔍 Running codespell...")
    try:
        session.run(
            "poetry",
            "run",
            "codespell",
            ".",
            "--skip=.git,*.pyc,*.png,*.jpg,.venv,poetry.lock,*.min.js,*.min.css",
            "--ignore-words-list=haive,nd,crate",
            external=True,
        )
        results["codespell"] = {"status": "passed"}
        session.log("✅ Codespell: No spelling errors")
    except Exception as e:
        results["codespell"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Codespell: Spelling errors found - {e}")

    # 2. Pyspelling (if config exists)
    pyspelling_config = Path(".pyspelling.yml")
    if pyspelling_config.exists():
        session.log("\n🔍 Running pyspelling...")
        try:
            session.run("poetry", "run", "pyspelling", external=True)
            results["pyspelling"] = {"status": "passed"}
            session.log("✅ Pyspelling: No spelling errors")
        except Exception as e:
            results["pyspelling"] = {"status": "failed", "error": str(e)}
            session.log(f"❌ Pyspelling: Spelling errors found - {e}")
    else:
        session.log("⚠️ Pyspelling config not found, creating default...")
        pyspelling_config.write_text(
            """
matrix:
- name: Python
  sources:
  - 'packages/**/*.py'
  aspell:
    lang: en
  pipeline:
  - pyspelling.filters.python:
      comments: true
      docstrings: true

- name: Markdown
  sources:
  - '**/*.md'
  aspell:
    lang: en
  pipeline:
  - pyspelling.filters.markdown:
""", )

    _generate_quality_report(session, "spelling_check", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_prose(session):
    """Test prose quality with proselint and vale."""
    session.log("✍️ Testing prose quality...")

    # Install dependencies
    session.run("poetry", "install", "--with", "dev", external=True)

    results = {}

    # 1. Proselint
    session.log("\n🔍 Running proselint...")
    try:
        session.run(
            "poetry",
            "run",
            "proselint",
            "README.md",
            "docs/",
            "project_docs/",
            external=True,
        )
        results["proselint"] = {"status": "passed"}
        session.log("✅ Proselint: Good prose quality")
    except Exception as e:
        results["proselint"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Proselint: Prose issues found - {e}")

    # 2. Vale (if config exists)
    vale_config = Path(".vale.ini")
    if vale_config.exists():
        session.log("\n🔍 Running vale...")
        try:
            session.run("poetry",
                        "run",
                        "vale",
                        "README.md",
                        "docs/",
                        external=True)
            results["vale"] = {"status": "passed"}
            session.log("✅ Vale: Good prose quality")
        except Exception as e:
            results["vale"] = {"status": "failed", "error": str(e)}
            session.log(f"❌ Vale: Prose issues found - {e}")
    else:
        session.log("⚠️ Vale config not found, skipping")
        results["vale"] = {"status": "skipped", "reason": "No .vale.ini"}

    _generate_quality_report(session, "prose_quality", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_metadata(session):
    """Check package metadata with pytest-checkdocs."""
    session.log("📦 Checking package metadata...")

    # Install dependencies
    session.run("poetry", "install", "--with", "dev", external=True)

    results = {}

    # 1. pytest-checkdocs
    session.log("\n🔍 Running pytest-checkdocs...")
    try:
        session.run("poetry",
                    "run",
                    "pytest",
                    "--checkdocs",
                    "-v",
                    external=True)
        results["checkdocs"] = {"status": "passed"}
        session.log("✅ Package metadata is valid")
    except Exception as e:
        results["checkdocs"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Metadata issues found - {e}")

    # 2. Pyroma
    session.log("\n🔍 Running pyroma...")
    try:
        session.run("poetry", "run", "pyroma", ".", external=True)
        results["pyroma"] = {"status": "passed"}
        session.log("✅ Package quality is good")
    except Exception as e:
        results["pyroma"] = {"status": "failed", "error": str(e)}
        session.log(f"❌ Package quality issues - {e}")

    _generate_quality_report(session, "metadata_check", results)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_pipeline(session):
    """Run the full documentation quality pipeline."""
    session.log("🚀 Running full documentation quality pipeline...")

    # This runs our custom Python pipeline script
    session.run("poetry", "install", "--with", "dev,docs", external=True)

    pipeline_script = Path("scripts/doc_quality_pipeline.py")
    if pipeline_script.exists():
        session.run(
            "poetry",
            "run",
            "python",
            str(pipeline_script),
            "-v",
            "-o",
            str(
                QUALITY_REPORTS_DIR /
                f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", ),
            external=True,
        )
    else:
        session.log(
            "⚠️ Pipeline script not found at scripts/doc_quality_pipeline.py")


def _generate_quality_report(session, test_name: str, results: dict):
    """Generate a quality report for a test session."""
    # Create report
    report = {
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total":
            len(results),
            "passed":
            sum(1 for r in results.values() if r.get("status") == "passed"),
            "failed":
            sum(1 for r in results.values() if r.get("status") == "failed"),
            "skipped":
            sum(1 for r in results.values() if r.get("status") == "skipped"),
        },
    }

    # Save report
    report_file = (
        QUALITY_REPORTS_DIR /
        f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    # Display summary
    session.log("\n" + "=" * 60)
    session.log(f"📊 {test_name.upper()} SUMMARY")
    session.log("=" * 60)
    session.log(f"Total tests: {report['summary']['total']}")
    session.log(f"✅ Passed: {report['summary']['passed']}")
    session.log(f"❌ Failed: {report['summary']['failed']}")
    session.log(f"⏭️ Skipped: {report['summary']['skipped']}")
    session.log(f"📋 Report saved to: {report_file}")

    return report["summary"]["failed"] == 0
