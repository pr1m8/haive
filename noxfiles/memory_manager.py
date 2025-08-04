"""Memory management utilities for nox sessions.

This module provides intelligent memory management to prevent system
crashes during resource-intensive documentation builds.
"""
from __future__ import annotations

import gc
import time
from pathlib import Path

# Memory management imports
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class MemoryManager:
    """Intelligent memory management for documentation builds."""

    def __init__(self):
        # Memory thresholds
        self.memory_threshold_critical = 1 * 1024**3  # 1GB
        self.memory_threshold_low = 2 * 1024**3  # 2GB
        self.memory_threshold_moderate = 4 * 1024**3  # 4GB
        self.memory_threshold_high = 8 * 1024**3  # 8GB

    def get_available_memory(self):
        """Get available system memory in bytes."""
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().available
        return 8 * 1024**3  # Assume 8GB if psutil unavailable

    def get_memory_gb(self):
        """Get available memory in GB."""
        return self.get_available_memory() / (1024**3)

    def get_memory_percent(self):
        """Get percentage of memory available."""
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().percent
        return 50.0  # Assume 50% if psutil unavailable

    def calculate_parallel_jobs(self):
        """Calculate optimal number of parallel jobs based on available.

        memory.
        """
        available_memory = self.get_available_memory()

        if available_memory < self.memory_threshold_critical:
            return 1  # Single job only
        if available_memory < self.memory_threshold_low:
            return 2  # Minimal parallelism
        if available_memory < self.memory_threshold_moderate:
            return 4  # Moderate parallelism
        if available_memory < self.memory_threshold_high:
            return 6  # Good parallelism
        return "auto"  # Let Sphinx decide

    def check_memory_status(self, session):
        """Check current memory status and log it."""
        if not PSUTIL_AVAILABLE:
            session.log(
                "⚠️  psutil not available - memory monitoring disabled")
            return "unknown"

        available_gb = self.get_memory_gb()
        percent_used = self.get_memory_percent()

        session.log(
            f"💾 Memory: {
                available_gb:.1f}GB available ({
                100 -
                percent_used:.0f}% free)",
        )

        if available_gb < 1.0:
            session.log("🚨 CRITICAL: Less than 1GB memory available!")
            return "critical"
        if available_gb < 2.0:
            session.log("⚠️  WARNING: Low memory - build may be slow")
            return "low"
        if available_gb < 4.0:
            session.log("📊 Moderate memory available")
            return "moderate"
        session.log("✅ Plenty of memory available")
        return "good"

    def cleanup_memory(self, session):
        """Force garbage collection and cleanup."""
        session.log("🧹 Cleaning up memory...")
        gc.collect()

        # If on Linux/Unix, try to drop caches (requires sudo)
        if Path("/proc/sys/vm/drop_caches").exists():
            try:
                import subprocess

                subprocess.run(["sync"], check=False)
                # Note: This would require sudo permissions
            except BaseException:
                pass

    def monitor_build(self, session, operation_name):
        """Context manager to monitor memory during builds."""

        class MemoryMonitor:

            def __init__(self, mm, sess, op_name):
                self.memory_manager = mm
                self.session = sess
                self.operation = op_name
                self.start_memory = None
                self.start_time = None

            def __enter__(self):
                self.start_memory = self.memory_manager.get_available_memory()
                self.start_time = time.time()
                self.session.log(
                    f"🚀 Starting {
                        self.operation} with {
                        self.memory_manager.get_memory_gb():.1f}GB available", )
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                end_memory = self.memory_manager.get_available_memory()
                memory_used = (self.start_memory - end_memory) / (1024**3)
                elapsed = time.time() - self.start_time

                self.session.log(
                    f"✅ {self.operation} completed in {elapsed:.1f}s")
                self.session.log(f"💾 Memory used: {memory_used:.1f}GB")

                # Cleanup if memory is low
                if self.memory_manager.get_memory_gb() < 2.0:
                    self.memory_manager.cleanup_memory(self.session)

        return MemoryMonitor(self, session, operation_name)


# Global memory manager instance
memory_manager = MemoryManager()


def get_memory_safe_sphinx_args(session):
    """Get memory-safe Sphinx build arguments."""
    memory_status = memory_manager.check_memory_status(session)

    args = ["-b", "html"]

    # Adjust parallelism based on memory
    if memory_status == "critical":
        args.extend(["-j", "1"])  # Single job only
        session.log("⚠️  Using single job due to low memory")
    elif memory_status == "low":
        args.extend(["-j", "2"])  # Minimal parallelism
        session.log("⚠️  Using 2 parallel jobs due to low memory")
    elif memory_status == "moderate":
        args.extend(["-j", "4"])  # Moderate parallelism
    else:
        args.extend(["-j", "auto"])  # Let Sphinx decide

    # Always continue on errors
    args.append("--keep-going")

    return args
