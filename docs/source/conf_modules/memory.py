"""Memory management for Sphinx configuration.

This module integrates the memory management capabilities from the noxfile system
into the Sphinx configuration to optimize documentation builds based on available memory.
"""

import gc
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Memory management imports
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Try to use rich for better UI, fall back to basic logging if not available
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (BarColumn, Progress, SpinnerColumn,
                               TaskProgressColumn, TextColumn)
    from rich.table import Table

    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    console = None
    RICH_AVAILABLE = False

logger = logging.getLogger(__name__)


class SphinxMemoryManager:
    """Memory-aware Sphinx configuration manager."""

    def __init__(self):
        # Memory thresholds in bytes
        self.memory_threshold_critical = 1 * 1024**3  # 1GB
        self.memory_threshold_low = 2 * 1024**3  # 2GB
        self.memory_threshold_moderate = 4 * 1024**3  # 4GB
        self.memory_threshold_high = 8 * 1024**3  # 8GB

        self.current_status = self._check_memory_status()

    def get_available_memory(self) -> int:
        """Get available system memory in bytes."""
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().available
        return 8 * 1024**3  # Assume 8GB if psutil unavailable

    def get_memory_gb(self) -> float:
        """Get available memory in GB."""
        return self.get_available_memory() / (1024**3)

    def get_memory_percent_used(self) -> float:
        """Get percentage of memory used."""
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().percent
        return 50.0  # Assume 50% if psutil unavailable

    def _check_memory_status(self) -> str:
        """Check current memory status."""
        if not PSUTIL_AVAILABLE:
            return "unknown"

        available_gb = self.get_memory_gb()

        if available_gb < 1.0:
            return "critical"
        elif available_gb < 2.0:
            return "low"
        elif available_gb < 4.0:
            return "moderate"
        else:
            return "good"

    def get_memory_info(self) -> Dict[str, Any]:
        """Get comprehensive memory information."""
        return {
            "available_gb": self.get_memory_gb(),
            "percent_used": self.get_memory_percent_used(),
            "status": self.current_status,
            "psutil_available": PSUTIL_AVAILABLE,
        }

    def display_memory_status(self):
        """Display current memory status with rich UI."""
        info = self.get_memory_info()

        if RICH_AVAILABLE and console:
            # Create memory status table
            table = Table(
                title="Memory Status", show_header=True, header_style="bold blue"
            )
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("Status", style="yellow")

            # Status emoji mapping
            status_emoji = {
                "critical": "🚨",
                "low": "⚠️ ",
                "moderate": "📊",
                "good": "✅",
                "unknown": "❓",
            }

            table.add_row(
                "Available Memory",
                f"{info['available_gb']:.1f} GB",
                f"{status_emoji.get(info['status'], '❓')} {info['status'].title()}",
            )

            table.add_row(
                "Memory Used",
                f"{info['percent_used']:.1f}%",
                "Good" if info["percent_used"] < 80 else "High",
            )

            table.add_row(
                "Monitoring",
                "psutil" if info["psutil_available"] else "basic",
                "✅ Active" if info["psutil_available"] else "⚠️  Limited",
            )

            console.print(table)

            # Display memory-based recommendations
            recommendations = self.get_memory_recommendations()
            if recommendations:
                console.print(
                    Panel.fit(
                        "\n".join([f"• {rec}" for rec in recommendations]),
                        title="💡 Memory Recommendations",
                        border_style="yellow",
                    )
                )
        else:
            # Fallback to simple logging
            logger.info(
                f"💾 Memory: {info['available_gb']:.1f}GB available ({100-info['percent_used']:.0f}% free)"
            )
            logger.info(f"📊 Status: {info['status'].title()}")

    def get_memory_recommendations(self) -> list:
        """Get memory-based recommendations."""
        recommendations = []

        if self.current_status == "critical":
            recommendations.extend(
                [
                    "Consider closing other applications",
                    "Use single-threaded builds only",
                    "Build smaller sections at a time",
                    "Consider upgrading system memory",
                ]
            )
        elif self.current_status == "low":
            recommendations.extend(
                [
                    "Use limited parallelism (2-4 workers)",
                    "Avoid building all formats simultaneously",
                    "Monitor memory usage during builds",
                ]
            )
        elif self.current_status == "moderate":
            recommendations.extend(
                [
                    "Good for most documentation builds",
                    "Can use moderate parallelism",
                    "Consider HTML-only builds for speed",
                ]
            )
        else:
            recommendations.extend(
                [
                    "Excellent memory availability",
                    "Can use full parallelism",
                    "Safe to build all formats simultaneously",
                ]
            )

        return recommendations

    def get_memory_safe_config(self) -> Dict[str, Any]:
        """Get memory-optimized Sphinx configuration."""
        config = {}

        # Base memory-safe settings
        config.update(
            {
                "keep_warnings": True,
                "warning_is_error": False,  # Don't fail on warnings in low memory
            }
        )

        # Memory-specific optimizations
        if self.current_status == "critical":
            config.update(
                {
                    "html_split_index": True,  # Split large indices
                    "html_compact_lists": True,  # More compact HTML
                    "autodoc_member_order": "bysource",  # Faster than alphabetical
                    "autosummary_generate": False,  # Disable to save memory
                }
            )
        elif self.current_status == "low":
            config.update(
                {
                    "html_split_index": True,
                    "autodoc_member_order": "bysource",
                    "autosummary_generate": True,
                    "autosummary_generate_overwrite": False,  # Don't regenerate existing
                }
            )
        else:
            config.update(
                {
                    "html_split_index": False,  # Keep unified index for better UX
                    "autosummary_generate": True,
                    "autosummary_generate_overwrite": True,
                }
            )

        # Extension-specific memory optimizations
        if self.current_status in ["critical", "low"]:
            # Disable memory-intensive extensions in low memory
            config["memory_disabled_extensions"] = [
                "sphinx_gallery.gen_gallery",  # Very memory intensive
                "sphinx_examples",  # Can be memory intensive
                "sphinxcontrib.versioning",  # Memory intensive for large docs
            ]

        return config

    def get_build_recommendations(self) -> Dict[str, Any]:
        """Get build-specific recommendations."""
        recommendations = {
            "parallel_jobs": self._calculate_parallel_jobs(),
            "build_formats": self._get_recommended_formats(),
            "memory_monitoring": PSUTIL_AVAILABLE,
        }

        return recommendations

    def _calculate_parallel_jobs(self) -> str:
        """Calculate optimal number of parallel jobs."""
        available_memory = self.get_available_memory()

        if available_memory < self.memory_threshold_critical:
            return "1"  # Single job only
        elif available_memory < self.memory_threshold_low:
            return "2"  # Minimal parallelism
        elif available_memory < self.memory_threshold_moderate:
            return "4"  # Moderate parallelism
        elif available_memory < self.memory_threshold_high:
            return "6"  # Good parallelism
        else:
            return "auto"  # Let Sphinx decide

    def _get_recommended_formats(self) -> list:
        """Get recommended build formats based on memory."""
        if self.current_status == "critical":
            return ["html"]  # HTML only
        elif self.current_status == "low":
            return ["html", "epub"]  # Light formats
        elif self.current_status == "moderate":
            return ["html", "epub", "pdf"]  # Most formats
        else:
            return ["html", "epub", "pdf", "man", "texinfo"]  # All formats

    def optimize_extensions_for_memory(self, extensions: list) -> list:
        """Filter extensions based on available memory."""
        if self.current_status not in ["critical", "low"]:
            return extensions  # Return all extensions if memory is good

        # Memory-intensive extensions to potentially disable
        memory_intensive = {
            "sphinx_gallery.gen_gallery": "Gallery generation is memory intensive",
            "sphinx_examples": "Example processing can use significant memory",
            "sphinxcontrib.versioning": "Version building requires extra memory",
            "sphinx_jupyterbook_latex": "LaTeX processing is memory intensive",
        }

        optimized_extensions = []
        disabled_extensions = []

        for ext in extensions:
            if ext in memory_intensive and self.current_status == "critical":
                disabled_extensions.append((ext, memory_intensive[ext]))
            else:
                optimized_extensions.append(ext)

        if disabled_extensions and RICH_AVAILABLE and console:
            console.print(
                Panel.fit(
                    "\n".join(
                        [f"• {ext}: {reason}" for ext, reason in disabled_extensions]
                    ),
                    title="⚠️  Extensions Disabled Due to Low Memory",
                    border_style="red",
                )
            )
        elif disabled_extensions:
            logger.warning(
                f"⚠️  Disabled {len(disabled_extensions)} extensions due to low memory"
            )

        return optimized_extensions

    def cleanup_memory(self):
        """Force garbage collection and cleanup."""
        if RICH_AVAILABLE and console:
            console.print("🧹 Cleaning up memory...")
        else:
            logger.info("🧹 Cleaning up memory...")

        gc.collect()

        # Update status after cleanup
        self.current_status = self._check_memory_status()


# Global memory manager instance
sphinx_memory_manager = SphinxMemoryManager()


def get_memory_safe_sphinx_config(extensions: list) -> Dict[str, Any]:
    """Get complete memory-safe Sphinx configuration."""
    # Display current memory status
    sphinx_memory_manager.display_memory_status()

    # Get memory-optimized configuration
    config = sphinx_memory_manager.get_memory_safe_config()

    # Optimize extensions for available memory
    optimized_extensions = sphinx_memory_manager.optimize_extensions_for_memory(
        extensions
    )
    config["extensions"] = optimized_extensions

    # Add build recommendations
    build_recs = sphinx_memory_manager.get_build_recommendations()
    config["build_recommendations"] = build_recs

    return config


def monitor_sphinx_build(operation_name: str):
    """Context manager to monitor memory during Sphinx operations."""

    class SphinxMemoryMonitor:
        def __init__(self, op_name):
            self.operation = op_name
            self.start_memory = None
            self.start_time = None

        def __enter__(self):
            self.start_memory = sphinx_memory_manager.get_available_memory()
            self.start_time = time.time()

            if RICH_AVAILABLE and console:
                console.print(
                    f"🚀 Starting {self.operation} with {sphinx_memory_manager.get_memory_gb():.1f}GB available"
                )
            else:
                logger.info(
                    f"🚀 Starting {self.operation} with {sphinx_memory_manager.get_memory_gb():.1f}GB available"
                )

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            end_memory = sphinx_memory_manager.get_available_memory()
            memory_used = (self.start_memory - end_memory) / (1024**3)
            elapsed = time.time() - self.start_time

            if RICH_AVAILABLE and console:
                console.print(f"✅ {self.operation} completed in {elapsed:.1f}s")
                console.print(f"💾 Memory used: {memory_used:.1f}GB")
            else:
                logger.info(f"✅ {self.operation} completed in {elapsed:.1f}s")
                logger.info(f"💾 Memory used: {memory_used:.1f}GB")

            # Cleanup if memory is low
            if sphinx_memory_manager.get_memory_gb() < 2.0:
                sphinx_memory_manager.cleanup_memory()

    return SphinxMemoryMonitor(operation_name)
