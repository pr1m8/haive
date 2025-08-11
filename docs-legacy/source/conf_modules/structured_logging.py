"""Enhanced logging configuration with structured output for Sphinx builds."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import json
import logging
from pathlib import Path
import sys
from typing import Any


class StructuredFormatter(logging.Formatter):
    """Format logs as structured JSON for easy parsing."""

    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "category"):
            log_obj["category"] = record.category
        if hasattr(record, "extension"):
            log_obj["extension"] = record.extension
        if hasattr(record, "package"):
            log_obj["package"] = record.package

        return json.dumps(log_obj)


class BuildErrorCollector:
    """Collect and categorize build errors/warnings."""

    def __init__(self):
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.info = defaultdict(list)

    def add_error(self, category: str, message: str, details: dict[str, Any] = None):
        """Add an error with category."""
        self.errors[category].append(
            {
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def add_warning(self, category: str, message: str, details: dict[str, Any] = None):
        """Add a warning with category."""
        self.warnings[category].append(
            {
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def get_summary(self) -> dict[str, Any]:
        """Get structured summary of all issues."""
        return {
            "summary": {
                "total_errors": sum(len(v) for v in self.errors.values()),
                "total_warnings": sum(len(v) for v in self.warnings.values()),
                "error_categories": list(self.errors.keys()),
                "warning_categories": list(self.warnings.keys()),
            },
            "errors": dict(self.errors),
            "warnings": dict(self.warnings),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def save_report(self, filepath: Path):
        """Save structured report to JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.get_summary(), f, indent=2)


# Global error collector
error_collector = BuildErrorCollector()


class StructuredLogHandler(logging.Handler):
    """Handler that collects errors/warnings in structured format."""

    def emit(self, record):
        """Process log record and categorize."""
        if record.levelname == "ERROR":
            category = getattr(record, "category", "general")
            error_collector.add_error(
                category,
                record.getMessage(),
                {
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno,
                },
            )
        elif record.levelname == "WARNING":
            category = getattr(record, "category", "general")
            error_collector.add_warning(
                category,
                record.getMessage(),
                {
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno,
                },
            )


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        # Format with color
        levelname = record.levelname
        record.levelname = f"{log_color}{levelname}{self.RESET}"
        formatted = super().format(record)
        # Reset levelname
        record.levelname = levelname
        return formatted


def setup_sphinx_logging():
    """Setup comprehensive logging with structured output."""

    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs" / "build"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Regular log file
    log_file = log_dir / f"sphinx_build_{timestamp}.log"

    # Structured JSON log file
    json_log_file = log_dir / f"sphinx_build_{timestamp}.json"

    # Configure root logger
    logger = logging.getLogger("sphinx_config")
    logger.setLevel(logging.DEBUG)

    # File handler - human readable
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    file_handler.setFormatter(file_formatter)

    # JSON file handler - structured
    json_handler = logging.FileHandler(json_log_file)
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(StructuredFormatter())

    # Console handler - pretty formatted
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

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


def get_error_summary():
    """Get current error summary."""
    return error_collector.get_summary()


def save_build_report(build_dir: Path = None):
    """Save final build report."""
    if build_dir is None:
        build_dir = Path(__file__).parent.parent / "logs" / "build"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = build_dir / f"build_report_{timestamp}.json"
    error_collector.save_report(report_file)
    return report_file
