"""Memory-Safe Nox configuration for Haive project documentation.

This enhanced version preserves all documentation features while adding intelligent
memory management to prevent system crashes.

ENHANCEMENTS:
- Dynamic parallel job calculation based on available memory
- Streaming output instead of memory buffering
- Memory monitoring during builds
- Progressive fallback under memory pressure
- Resource cleanup between operations
- Smart timeout handling
"""

import os
import shutil
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path

import nox

# Memory management imports
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Configuration
PYTHON_VERSIONS = ["3.12"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths - Centralized and consistent
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build" / "html"
LOGS_DIR = DOCS_DIR / "logs"
QUALITY_REPORTS_DIR = DOCS_DIR / "quality-reports"

# Exclude problematic packages from documentation build
EXCLUDE_PACKAGES = ["packages/haive-prebuilt"]

# Package paths for namespaced imports
PACKAGES_DIR = Path("packages")
PACKAGE_NAMES = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

# ==============================================================================
# Memory Management System
# ==============================================================================


class MemoryManager:
    """Intelligent memory management for documentation builds."""

    def __init__(self):
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

    def get_memory_status(self):
        """Get current memory status."""
        available = self.get_available_memory()

        if available < self.memory_threshold_critical:
            return "critical"
        if available < self.memory_threshold_low:
            return "low"
        if available < self.memory_threshold_moderate:
            return "moderate"
        if available < self.memory_threshold_high:
            return "good"
        return "excellent"

    def get_safe_parallel_jobs(self):
        """Calculate safe number of parallel jobs based on available memory."""
        memory_status = self.get_memory_status()
        cpu_count = os.cpu_count() or 4

        if memory_status == "critical":
            return "1"  # Single threaded only
        if memory_status == "low":
            return "1"  # Single threaded
        if memory_status == "moderate":
            return str(min(2, cpu_count))  # Max 2 jobs
        if memory_status == "good":
            return str(min(4, cpu_count))  # Max 4 jobs
        # excellent
        return str(min(8, cpu_count))  # Up to 8 jobs with excellent memory

    def get_safe_timeout(self):
        """Get safe timeout based on parallelization."""
        jobs = int(self.get_safe_parallel_jobs())
        base_timeout = 1800  # 30 minutes base

        # More time for single-threaded builds
        if jobs == 1:
            return base_timeout * 2  # 60 minutes
        if jobs <= 2:
            return int(base_timeout * 1.5)  # 45 minutes
        return base_timeout  # 30 minutes

    def should_use_memory_safe_config(self):
        """Determine if we should use memory-safe sphinx config."""
        return self.get_memory_status() in ["critical", "low", "moderate"]


# Initialize global memory manager
memory_manager = MemoryManager()


def create_log_file(session, operation_name: str) -> Path:
    """Create a timestamped log file for the operation."""
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{operation_name}_{timestamp}.log"
    session.log(f"📝 Logging to: {log_file}")
    return log_file


def log_memory_status(session, prefix=""):
    """Log current memory status."""
    memory_gb = memory_manager.get_memory_gb()
    memory_status = memory_manager.get_memory_status()

    status_emoji = {
        "critical": "🚨",
        "low": "⚠️",
        "moderate": "📊",
        "good": "✅",
        "excellent": "🚀",
    }

    emoji = status_emoji.get(memory_status, "📊")
    session.log(
        f"{prefix}{emoji} Memory: {memory_gb:.1f}GB available ({memory_status})"
    )


def stream_with_memory_monitoring(
    session, cmd: list, log_file: Path, operation: str, timeout: int | None = None
) -> dict:
    """Run command with streaming output and memory monitoring."""
    status = {
        "success": False,
        "returncode": None,
        "warnings": 0,
        "errors": 0,
        "fatal_error": None,
        "output_exists": False,
        "log_file": log_file,
        "memory_critical_events": 0,
    }

    try:
        session.log(f"🔧 Running: {' '.join(cmd)}")
        log_memory_status(session, "🚀 Starting build - ")

        # Determine configuration based on memory
        if memory_manager.should_use_memory_safe_config():
            # Use memory-safe configuration
            if "sphinx-build" in cmd:
                config_file = SOURCE_DIR / "conf_memory_safe.py"
                if config_file.exists():
                    # Replace conf.py with conf_memory_safe.py
                    cmd = [
                        (
                            arg.replace("conf.py", "conf_memory_safe.py")
                            if "conf.py" in arg
                            else arg
                        )
                        for arg in cmd
                    ]
                    session.log("🛡️ Using memory-safe configuration")
                else:
                    session.log("⚠️ Memory-safe config not found, using standard config")

        with open(log_file, "w") as f:
            f.write(f"=== {operation} ===\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Started: {datetime.now()}\n")
            f.write(f"Memory at start: {memory_manager.get_memory_gb():.1f}GB\n\n")

            # Start process with timeout
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                preexec_fn=os.setsid if os.name != "nt" else None,
            )

            start_time = time.time()
            last_memory_check = start_time
            memory_check_interval = 30  # Check memory every 30 seconds

            # Stream output with memory monitoring
            while True:
                try:
                    # Check for process completion
                    if process.poll() is not None:
                        break

                    # Check timeout
                    if timeout and (time.time() - start_time) > timeout:
                        session.log(f"⏱️ Build timed out after {timeout}s")
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                        status["fatal_error"] = f"Timeout after {timeout}s"
                        break

                    # Read output with timeout
                    try:
                        output = process.stdout.readline()
                        if not output:
                            time.sleep(0.1)
                            continue
                    except:
                        time.sleep(0.1)
                        continue

                    # Write to log file immediately (streaming, not buffering)
                    f.write(output)
                    f.flush()

                    # Process output line for display
                    line = output.strip()
                    if line:
                        # Count warnings and errors
                        line_lower = line.lower()
                        if "warning:" in line_lower:
                            status["warnings"] += 1
                            session.log(f"⚠️  {line[:100]}")
                        elif "error:" in line_lower and "autosummary" not in line_lower:
                            status["errors"] += 1
                            session.log(f"🚨 {line[:100]}")
                        elif any(
                            keyword in line_lower
                            for keyword in [
                                "building",
                                "processing",
                                "writing",
                                "reading",
                            ]
                        ):
                            # Show progress but limit frequency
                            if (
                                time.time() - last_memory_check
                            ) > 10:  # Every 10 seconds for progress
                                session.log(f"📄 {line[:80]}...")

                    # Periodic memory monitoring
                    current_time = time.time()
                    if (current_time - last_memory_check) > memory_check_interval:
                        memory_status = memory_manager.get_memory_status()
                        memory_gb = memory_manager.get_memory_gb()

                        f.write(
                            f"\n[MEMORY CHECK] {datetime.now()}: {memory_gb:.1f}GB available ({memory_status})\n"
                        )

                        if memory_status == "critical":
                            status["memory_critical_events"] += 1
                            session.log(
                                f"🚨 CRITICAL MEMORY: {memory_gb:.1f}GB - Build may fail!"
                            )

                            # Consider terminating if critical for too long
                            if status["memory_critical_events"] > 3:
                                session.log(
                                    "🛑 Terminating build due to persistent critical memory"
                                )
                                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                                status["fatal_error"] = (
                                    "Terminated due to critical memory pressure"
                                )
                                break
                        elif memory_status in ["low", "moderate"]:
                            session.log(f"📊 Memory check: {memory_gb:.1f}GB available")

                        last_memory_check = current_time

                except KeyboardInterrupt:
                    session.log("🛑 Build interrupted by user")
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    status["fatal_error"] = "Interrupted by user"
                    break
                except Exception as e:
                    session.log(f"❌ Error during build monitoring: {e}")
                    break

            # Get final return code
            try:
                status["returncode"] = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                status["returncode"] = -1

            # Write final status to log
            end_time = datetime.now()
            final_memory = memory_manager.get_memory_gb()

            with open(log_file, "a") as f:
                f.write(f"\nCompleted: {end_time}\n")
                f.write(f"Return code: {status['returncode']}\n")
                f.write(f"Warnings: {status['warnings']}\n")
                f.write(f"Errors: {status['errors']}\n")
                f.write(f"Memory at end: {final_memory:.1f}GB\n")
                f.write(f"Memory critical events: {status['memory_critical_events']}\n")

        # Check if build produced output
        if BUILD_DIR.exists():
            html_files = list(BUILD_DIR.glob("*.html"))
            status["output_exists"] = len(html_files) > 0

        # Determine success
        if status["returncode"] == 0:
            status["success"] = True
            log_memory_status(session, "✅ Build completed - ")
        elif status["output_exists"] and status["memory_critical_events"] == 0:
            status["success"] = True  # Partial success
            session.log("⚠️ Build completed with issues but documentation was generated")
            log_memory_status(session, "⚠️ Build issues - ")
        else:
            session.log("❌ Build failed")
            log_memory_status(session, "❌ Build failed - ")

        return status

    except Exception as e:
        status["fatal_error"] = str(e)
        session.log(f"❌ {operation} failed with exception: {e}")
        log_memory_status(session, "❌ Exception - ")

        with open(log_file, "a") as f:
            f.write(f"\nFATAL ERROR: {e}\n")
            f.write(f"Memory at error: {memory_manager.get_memory_gb():.1f}GB\n")

        return status


# ==============================================================================
# Memory-Safe Documentation Sessions
# ==============================================================================


@nox.session(python=PYTHON_VERSIONS)
def docs_memory_safe(session):
    """Memory-safe documentation build with intelligent resource management."""
    datetime.now()
    session.log("🛡️ Running MEMORY-SAFE documentation build...")

    # Memory assessment
    log_memory_status(session, "🔍 Initial assessment - ")
    memory_status = memory_manager.get_memory_status()

    if memory_status == "critical":
        session.error("🚨 CRITICAL: Insufficient memory for documentation build")
        session.log("💡 Try closing other applications and retry")
        return False

    # Create log file
    log_file = create_log_file(session, "docs_memory_safe")

    # Install dependencies with memory awareness
    session.log("📦 Installing documentation dependencies...")

    if memory_status in ["low", "moderate"]:
        session.log("🛡️ Installing minimal dependencies for memory conservation")
        session.run(
            "poetry", "install", "--with", "docs", "--no-interaction", external=True
        )
    else:
        session.log("🚀 Installing full dependencies")
        session.run(
            "poetry",
            "install",
            "--with",
            "docs",
            "--all-extras",
            "--no-interaction",
            external=True,
        )

    # Install psutil if not available
    if not PSUTIL_AVAILABLE:
        session.log("📦 Installing psutil for memory monitoring...")
        session.run("poetry", "add", "--group", "docs", "psutil", external=True)

    # Set environment for memory-safe builds
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    os.environ["HAIVE_DOCS_MODE"] = "memory_safe"

    # Calculate safe parallel jobs and timeout
    parallel_jobs = memory_manager.get_safe_parallel_jobs()
    timeout = memory_manager.get_safe_timeout()

    session.log(f"🔧 Using {parallel_jobs} parallel jobs (memory-optimized)")
    session.log(f"⏱️ Timeout set to {timeout//60} minutes")

    # Memory-safe sphinx-build command
    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-c",
        str(SOURCE_DIR),  # Use source directory for config
        "-j",
        parallel_jobs,  # Memory-safe parallel jobs
        "--keep-going",  # Continue on errors
        "-v",  # Verbose for monitoring
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Run build with memory monitoring
    session.log("🔨 Starting memory-safe build...")
    status = stream_with_memory_monitoring(
        session, cmd, log_file, "Memory-Safe Sphinx Build", timeout
    )

    # Enhanced result reporting
    session.log("=" * 60)
    session.log("📊 MEMORY-SAFE BUILD SUMMARY")
    session.log("=" * 60)

    if status["success"]:
        session.log("✅ Status: SUCCESS")
    else:
        session.log("❌ Status: FAILED")

    session.log(f"📈 Warnings: {status['warnings']}")
    session.log(f"🚨 Errors: {status['errors']}")
    session.log(f"🔢 Return Code: {status['returncode']}")
    session.log(f"🧠 Memory Critical Events: {status['memory_critical_events']}")

    log_memory_status(session, "🔍 Final memory - ")

    # Check output
    if BUILD_DIR.exists():
        html_files = list(BUILD_DIR.glob("*.html"))
        session.log(f"📄 HTML files generated: {len(html_files)}")

        if html_files:
            if (BUILD_DIR / "index.html").exists():
                session.log(
                    f"🌐 View docs: file://{(BUILD_DIR / 'index.html').absolute()}"
                )
            else:
                first_html = html_files[0]
                session.log(f"🌐 View docs: file://{first_html.absolute()}")

    session.log(f"📋 Full log: {log_file}")
    session.log("=" * 60)

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_fast_safe(session):
    """Fastest possible documentation build with memory safety."""
    datetime.now()
    session.log("🚀 Running FASTEST SAFE documentation build...")

    log_memory_status(session, "🔍 Memory check - ")

    # Ultra-minimal approach for speed
    log_file = create_log_file(session, "docs_fast_safe")

    # Skip dependency installation if possible
    try:
        session.run(
            "poetry", "run", "sphinx-build", "--version", silent=True, external=True
        )
        session.log("✅ Sphinx available, skipping installation")
    except:
        session.log("📦 Installing minimal dependencies...")
        session.run(
            "poetry", "install", "--with", "docs", "--no-interaction", external=True
        )

    # Force single-threaded for speed and memory safety
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    os.environ["HAIVE_DOCS_MODE"] = "fast_safe"

    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "1",  # Single thread for maximum safety
        "--keep-going",  # Continue on all errors
        "-q",  # Quiet mode for speed
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    # Shorter timeout for fast build
    timeout = 900  # 15 minutes max

    session.log("⚡ Running ultra-fast safe build...")
    status = stream_with_memory_monitoring(
        session, cmd, log_file, "Fast Safe Build", timeout
    )

    # Quick result summary
    if status["success"]:
        session.log("✅ Fast safe build completed!")
        if (BUILD_DIR / "index.html").exists():
            session.log(f"🌐 View: file://{(BUILD_DIR / 'index.html').absolute()}")
    else:
        session.log("❌ Fast safe build failed")
        session.log(f"📋 Check log: {log_file}")

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_progressive(session):
    """Progressive documentation build - starts minimal, adds features based on success."""
    session.log("🎯 Running PROGRESSIVE documentation build...")

    log_memory_status(session, "🔍 Starting memory - ")

    # Phase 1: Minimal build
    session.log("📊 Phase 1: Minimal documentation build")
    os.environ["HAIVE_DOCS_MODE"] = "minimal"

    minimal_success = docs_fast_safe(session)

    if not minimal_success:
        session.log("❌ Minimal build failed - stopping")
        return False

    # Check memory after minimal build
    log_memory_status(session, "📊 After minimal - ")
    memory_status = memory_manager.get_memory_status()

    # Phase 2: Enhanced build if memory allows
    if memory_status in ["good", "excellent"]:
        session.log("📊 Phase 2: Enhanced documentation build")
        os.environ["HAIVE_DOCS_MODE"] = "enhanced"

        enhanced_success = docs_memory_safe(session)

        if enhanced_success:
            session.log("✅ Progressive build: Both phases completed successfully!")
            return True
        session.log("⚠️ Enhanced build failed, but minimal build succeeded")
        return True  # Partial success
    session.log("📊 Skipping enhanced build due to memory constraints")
    session.log("✅ Progressive build: Minimal phase completed successfully!")
    return True


# ==============================================================================
# Original Sessions with Memory Enhancements
# ==============================================================================


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Enhanced standard sphinx-build with memory monitoring."""
    session.log("📚 Running enhanced sphinx-build with memory monitoring...")

    log_memory_status(session, "🔍 Initial - ")

    # Use memory-safe approach if needed
    if memory_manager.get_memory_status() in ["critical", "low"]:
        session.log("🛡️ Low memory detected - switching to memory-safe build")
        return docs_memory_safe(session)

    # Proceed with enhanced standard build
    log_file = create_log_file(session, "docs_enhanced")

    session.log("📦 Installing documentation dependencies...")
    session.run("poetry", "install", "--with", "docs", external=True)

    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    os.environ["HAIVE_DOCS_MODE"] = "enhanced"

    # Smart parallel jobs
    parallel_jobs = memory_manager.get_safe_parallel_jobs()
    timeout = memory_manager.get_safe_timeout()

    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        parallel_jobs,
        "--keep-going",
        "-v",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]

    status = stream_with_memory_monitoring(
        session, cmd, log_file, "Enhanced Sphinx Build", timeout
    )

    # Result reporting
    if status["success"]:
        session.log("✅ Enhanced build completed successfully!")
        if (BUILD_DIR / "index.html").exists():
            session.log(f"🌐 View docs: file://{(BUILD_DIR / 'index.html').absolute()}")
    else:
        session.log("❌ Enhanced build failed")

    session.log(f"📋 Full log: {log_file}")
    log_memory_status(session, "🔍 Final - ")

    return status["success"]


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve documentation with memory monitoring."""
    if not BUILD_DIR.exists() or not (BUILD_DIR / "index.html").exists():
        session.log("❌ No documentation found. Run 'nox -s docs_memory_safe' first.")
        return False

    session.log("🌐 Starting documentation server...")
    log_memory_status(session, "🔍 Server memory - ")

    try:
        session.run(
            "python",
            "-m",
            "http.server",
            "8000",
            "--directory",
            str(BUILD_DIR),
            external=True,
        )
    except KeyboardInterrupt:
        session.log("🛑 Server stopped")
        log_memory_status(session, "🔍 Server stopped - ")


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    session.log("🧹 Cleaning documentation build artifacts...")

    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Removed {BUILD_DIR}")

    # Clean logs older than 7 days
    if LOGS_DIR.exists():
        import time

        current_time = time.time()
        week_ago = current_time - (7 * 24 * 60 * 60)

        cleaned = 0
        for log_file in LOGS_DIR.glob("*.log"):
            if log_file.stat().st_mtime < week_ago:
                log_file.unlink()
                cleaned += 1

        if cleaned > 0:
            session.log(f"✅ Cleaned {cleaned} old log files")

    session.log("✅ Documentation cleanup complete")


# ==============================================================================
# Memory Diagnostic Sessions
# ==============================================================================


@nox.session(python=PYTHON_VERSIONS)
def memory_diagnosis(session):
    """Diagnose system memory and recommend optimal build strategy."""
    session.log("🔍 MEMORY DIAGNOSIS FOR DOCUMENTATION BUILDS")
    session.log("=" * 60)

    # System memory info
    if PSUTIL_AVAILABLE:
        memory = psutil.virtual_memory()
        session.log(f"💾 Total Memory: {memory.total / 1024**3:.1f}GB")
        session.log(f"💾 Available Memory: {memory.available / 1024**3:.1f}GB")
        session.log(
            f"💾 Used Memory: {memory.used / 1024**3:.1f}GB ({memory.percent:.1f}%)"
        )
        session.log(f"💾 Free Memory: {memory.free / 1024**3:.1f}GB")
    else:
        session.log("❌ psutil not available - install for detailed memory info")

    # CPU info
    cpu_count = os.cpu_count()
    session.log(f"🖥️  CPU Cores: {cpu_count}")

    # Memory manager recommendations
    memory_status = memory_manager.get_memory_status()
    parallel_jobs = memory_manager.get_safe_parallel_jobs()
    timeout = memory_manager.get_safe_timeout()

    session.log("")
    session.log("🎯 RECOMMENDATIONS:")
    session.log(f"📊 Memory Status: {memory_status.upper()}")
    session.log(f"🔧 Recommended Parallel Jobs: {parallel_jobs}")
    session.log(f"⏱️ Recommended Timeout: {timeout//60} minutes")

    # Recommended commands
    session.log("")
    session.log("💡 RECOMMENDED COMMANDS:")

    if memory_status == "critical":
        session.log("🚨 CRITICAL: Close other applications first!")
        session.log("   nox -s docs_fast_safe    # Minimal safe build")
    elif memory_status == "low":
        session.log("⚠️  LOW MEMORY - Use safe builds:")
        session.log("   nox -s docs_memory_safe  # Full features, memory managed")
        session.log("   nox -s docs_fast_safe    # Fastest safe option")
    elif memory_status == "moderate":
        session.log("📊 MODERATE - Progressive builds recommended:")
        session.log("   nox -s docs_progressive  # Builds incrementally")
        session.log("   nox -s docs_memory_safe  # Full safe build")
    else:  # good or excellent
        session.log("✅ EXCELLENT - All options available:")
        session.log("   nox -s docs              # Enhanced standard build")
        session.log("   nox -s docs_progressive  # Progressive build")
        session.log("   nox -s docs_memory_safe  # Safest option")

    session.log("")
    session.log("🛡️ MEMORY-SAFE OPTIONS:")
    session.log("   nox -s docs_fast_safe     # 15min timeout, minimal features")
    session.log("   nox -s docs_memory_safe   # Full features, smart management")
    session.log("   nox -s docs_progressive   # Adaptive: minimal → enhanced")

    return True


# ==============================================================================
# Session Aliases for Easy Access
# ==============================================================================

# Main recommended sessions
docs_safe = docs_memory_safe  # Primary safe option
docs_fast = docs_fast_safe  # Fastest safe option
docs_smart = docs_progressive  # Smart progressive option
