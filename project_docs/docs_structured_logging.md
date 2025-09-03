# Structured Logging for Sphinx Documentation Build

## 🎯 Solutions

### 1. Fix sphinxcontrib-spelling

Add to your `pyproject.toml`:

```toml
[tool.poetry.group.docs.dependencies]
sphinxcontrib-spelling = "^8.0.1"
pyenchant = "^3.2.2"  # Required dependency
```

Then install:

```bash
poetry install --with docs
```

### 2. Structured Error/Warning Logging

## 📊 Enhanced Logging Configuration

### \_conf/logging_config.py (Enhanced Version)

```python
"""Enhanced logging configuration with structured output."""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

class StructuredFormatter(logging.Formatter):
    """Format logs as structured JSON for easy parsing."""

    def format(self, record):
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, 'category'):
            log_obj['category'] = record.category
        if hasattr(record, 'extension'):
            log_obj['extension'] = record.extension
        if hasattr(record, 'package'):
            log_obj['package'] = record.package

        return json.dumps(log_obj)

class BuildErrorCollector:
    """Collect and categorize build errors/warnings."""

    def __init__(self):
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.info = defaultdict(list)

    def add_error(self, category: str, message: str, details: Dict[str, Any] = None):
        """Add an error with category."""
        self.errors[category].append({
            'message': message,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat()
        })

    def add_warning(self, category: str, message: str, details: Dict[str, Any] = None):
        """Add a warning with category."""
        self.warnings[category].append({
            'message': message,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat()
        })

    def get_summary(self) -> Dict[str, Any]:
        """Get structured summary of all issues."""
        return {
            'summary': {
                'total_errors': sum(len(v) for v in self.errors.values()),
                'total_warnings': sum(len(v) for v in self.warnings.values()),
                'error_categories': list(self.errors.keys()),
                'warning_categories': list(self.warnings.keys()),
            },
            'errors': dict(self.errors),
            'warnings': dict(self.warnings),
            'generated_at': datetime.utcnow().isoformat()
        }

    def save_report(self, filepath: Path):
        """Save structured report to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.get_summary(), f, indent=2)

# Global error collector
error_collector = BuildErrorCollector()

class StructuredLogHandler(logging.Handler):
    """Handler that collects errors/warnings in structured format."""

    def emit(self, record):
        """Process log record and categorize."""
        if record.levelname == 'ERROR':
            category = getattr(record, 'category', 'general')
            error_collector.add_error(category, record.getMessage(), {
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            })
        elif record.levelname == 'WARNING':
            category = getattr(record, 'category', 'general')
            error_collector.add_warning(category, record.getMessage(), {
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            })

def setup_sphinx_logging():
    """Setup comprehensive logging with structured output."""

    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs" / "build"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Regular log file
    log_file = log_dir / f"sphinx_build_{timestamp}.log"

    # Structured JSON log file
    json_log_file = log_dir / f"sphinx_build_{timestamp}.json"

    # Configure root logger
    logger = logging.getLogger('sphinx_config')
    logger.setLevel(logging.DEBUG)

    # File handler - human readable
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # JSON file handler - structured
    json_handler = logging.FileHandler(json_log_file)
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(StructuredFormatter())

    # Console handler - pretty formatted
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter())

    # Structured collector handler
    structured_handler = StructuredLogHandler()
    structured_handler.setLevel(logging.WARNING)

    # Add all handlers
    logger.addHandler(file_handler)
    logger.addHandler(json_handler)
    logger.addHandler(console_handler)
    logger.addHandler(structured_handler)

    logger.info(f"📝 Logging to: {log_file}")
    logger.info(f"📊 Structured log: {json_log_file}")

    return logger

class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)
```

### \_conf/extensions.py (Enhanced with Structured Logging)

```python
"""Enhanced extensions configuration with structured error handling."""

import logging
logger = logging.getLogger('sphinx_config.extensions')

# Extension categories for better organization
EXTENSION_CATEGORIES = {
    'core': [
        "sphinx.ext.autodoc",
        "sphinx.ext.autosummary",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        "sphinx.ext.todo",
        "sphinx.ext.coverage",
    ],
    'enhancement': [
        "myst_parser",
        "sphinx_copybutton",
        "sphinx_togglebutton",
        "sphinx_design",
        "sphinxcontrib.mermaid",
    ],
    'quality': [
        "sphinxcontrib.spelling",
        "sphinx.ext.doctest",
        "sphinx.ext.duration",
    ],
    'api': [
        "autoapi.extension",
        "sphinx_autodoc_typehints",
    ],
    'custom': [
        "_extensions.haive_sphinx_ext",
        "_extensions.agent_docs",
        "_extensions.auto_module_discovery",
    ]
}

# Build extensions list with structured logging
extensions = []
extension_status = {'loaded': [], 'failed': [], 'optional_missing': []}

for category, ext_list in EXTENSION_CATEGORIES.items():
    logger.info(f"\n📦 Loading {category} extensions:")

    for ext_name in ext_list:
        try:
            if ext_name.startswith("_extensions"):
                __import__(ext_name)
            extensions.append(ext_name)
            logger.info(f"  ✅ {ext_name}")
            extension_status['loaded'].append({
                'name': ext_name,
                'category': category
            })
        except ImportError as e:
            # Check if it's optional
            optional_extensions = [
                'sphinxcontrib.spelling',
                'sphinx_design',
                'sphinxcontrib.mermaid'
            ]

            if ext_name in optional_extensions:
                logger.warning(
                    f"  ⚠️  {ext_name}: Optional extension not available",
                    extra={'category': 'missing_extension', 'extension': ext_name}
                )
                extension_status['optional_missing'].append({
                    'name': ext_name,
                    'category': category,
                    'error': str(e)
                })
            else:
                logger.error(
                    f"  ❌ {ext_name}: Required extension failed to load - {e}",
                    extra={'category': 'extension_error', 'extension': ext_name}
                )
                extension_status['failed'].append({
                    'name': ext_name,
                    'category': category,
                    'error': str(e)
                })

# Summary report
logger.info("\n📊 Extension Loading Summary:")
logger.info(f"  ✅ Loaded: {len(extension_status['loaded'])}")
logger.info(f"  ⚠️  Optional Missing: {len(extension_status['optional_missing'])}")
logger.info(f"  ❌ Failed: {len(extension_status['failed'])}")

# Save extension status for later analysis
import json
from pathlib import Path
status_file = Path(__file__).parent.parent / "logs" / "build" / "extension_status.json"
status_file.parent.mkdir(exist_ok=True, parents=True)
with open(status_file, 'w') as f:
    json.dump(extension_status, f, indent=2)
```

### \_conf/build_hooks.py (Enhanced Error Reporting)

```python
"""Enhanced build hooks with structured error collection."""

import logging
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger('sphinx_config.hooks')

def on_build_finished(app, exception):
    """Enhanced build finished handler with structured report."""
    from _conf.logging_config import error_collector

    # Generate structured report
    report_dir = Path(app.srcdir) / "logs" / "build"
    report_dir.mkdir(exist_ok=True, parents=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = report_dir / f"build_report_{timestamp}.json"

    # Collect build statistics
    build_stats = {
        'builder': app.builder.name,
        'source_dir': str(app.srcdir),
        'output_dir': str(app.outdir),
        'success': exception is None,
        'exception': str(exception) if exception else None,
        'timestamp': datetime.utcnow().isoformat()
    }

    # Get error summary
    error_summary = error_collector.get_summary()

    # Combine into final report
    final_report = {
        'build_info': build_stats,
        'errors_and_warnings': error_summary,
        'extension_status': load_extension_status()
    }

    # Save report
    with open(report_file, 'w') as f:
        json.dump(final_report, f, indent=2)

    # Print summary to console
    logger.info("\n" + "=" * 80)
    logger.info("📊 BUILD SUMMARY")
    logger.info("=" * 80)

    if error_summary['summary']['total_errors'] > 0:
        logger.error(f"❌ Errors: {error_summary['summary']['total_errors']}")
        for category, errors in error_summary['errors'].items():
            logger.error(f"  - {category}: {len(errors)} errors")

    if error_summary['summary']['total_warnings'] > 0:
        logger.warning(f"⚠️  Warnings: {error_summary['summary']['total_warnings']}")
        for category, warnings in error_summary['warnings'].items():
            logger.warning(f"  - {category}: {len(warnings)} warnings")

    if exception:
        logger.error(f"🚫 Build failed with: {exception}")
    else:
        logger.info("✅ Build completed successfully!")

    logger.info(f"\n📄 Detailed report saved to: {report_file}")
    logger.info("=" * 80)

def load_extension_status():
    """Load extension status if available."""
    try:
        status_file = Path(__file__).parent.parent / "logs" / "build" / "extension_status.json"
        if status_file.exists():
            with open(status_file) as f:
                return json.load(f)
    except:
        pass
    return None
```

## 📊 Example Structured Output

### Console Output (Pretty Formatted)

```
📦 Loading core extensions:
  ✅ sphinx.ext.autodoc
  ✅ sphinx.ext.napoleon

📦 Loading quality extensions:
  ⚠️  sphinxcontrib.spelling: Optional extension not available

📊 Extension Loading Summary:
  ✅ Loaded: 25
  ⚠️  Optional Missing: 3
  ❌ Failed: 0

================================================================================
📊 BUILD SUMMARY
================================================================================
⚠️  Warnings: 3
  - missing_extension: 3 warnings
✅ Build completed successfully!

📄 Detailed report saved to: logs/build/build_report_20250104_160522.json
================================================================================
```

### JSON Report Structure

```json
{
  "build_info": {
    "builder": "html",
    "source_dir": "/home/will/Projects/haive/docs/source",
    "output_dir": "/home/will/Projects/haive/docs/build/html",
    "success": true,
    "exception": null,
    "timestamp": "2025-01-04T16:05:22.123456"
  },
  "errors_and_warnings": {
    "summary": {
      "total_errors": 0,
      "total_warnings": 3,
      "error_categories": [],
      "warning_categories": ["missing_extension"]
    },
    "errors": {},
    "warnings": {
      "missing_extension": [
        {
          "message": "sphinxcontrib.spelling: Optional extension not available",
          "details": {
            "module": "extensions",
            "function": "load_extensions",
            "line": 45
          },
          "timestamp": "2025-01-04T16:05:20.123456"
        }
      ]
    }
  },
  "extension_status": {
    "loaded": [
      { "name": "sphinx.ext.autodoc", "category": "core" },
      { "name": "myst_parser", "category": "enhancement" }
    ],
    "optional_missing": [
      {
        "name": "sphinxcontrib.spelling",
        "category": "quality",
        "error": "No module named 'sphinxcontrib.spelling'"
      }
    ],
    "failed": []
  }
}
```

This gives you:

1. ✅ Solution for the missing sphinxcontrib-spelling
2. ✅ Structured logging with categories
3. ✅ JSON reports for programmatic analysis
4. ✅ Pretty console output with colors
5. ✅ Detailed error/warning tracking by category
