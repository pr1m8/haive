#!/usr/bin/env python3
"""Comprehensive Documentation Quality Pipeline with Enhanced Logging."""

import asyncio
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("docs/logs/quality_pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class DocumentationQualityPipeline:
    """Enhanced documentation quality pipeline with comprehensive logging."""

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.cwd()
        self.docs_dir = self.base_dir / "docs"
        self.logs_dir = self.docs_dir / "logs"
        self.reports_dir = self.docs_dir / "quality-reports"

        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Track metrics
        self.metrics = {
            "start_time": None,
            "end_time": None,
            "duration": None,
            "stages": {},
            "errors": [],
            "warnings": [],
            "build_success": False,
            "pages_processed": 0,
            "html_files_generated": 0,
        }

    def log_stage_start(self, stage_name: str) -> str:
        """Log the start of a pipeline stage."""
        stage_id = f"{stage_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = time.time()

        self.metrics["stages"][stage_id] = {
            "name": stage_name,
            "start_time": start_time,
            "status": "running",
            "output": [],
            "errors": [],
            "warnings": [],
        }

        logger.info(f"🚀 Starting stage: {stage_name}")
        return stage_id

    def log_stage_end(self, stage_id: str, success: bool = True, output: str = ""):
        """Log the end of a pipeline stage."""
        if stage_id not in self.metrics["stages"]:
            logger.error(f"Unknown stage ID: {stage_id}")
            return

        stage = self.metrics["stages"][stage_id]
        stage["end_time"] = time.time()
        stage["duration"] = stage["end_time"] - stage["start_time"]
        stage["status"] = "success" if success else "failed"
        stage["output"].append(output)

        status_emoji = "✅" if success else "❌"
        logger.info(
            f"{status_emoji} Stage '{stage['name']}' completed in {stage['duration']:.2f}s"
        )

    def run_command(
        self, cmd: list[str], stage_id: str | None = None, timeout: int = 600
    ) -> tuple[bool, str, str]:
        """Run a command with enhanced logging."""
        cmd_str = " ".join(cmd)
        logger.info(f"🔧 Running: {cmd_str}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.base_dir,
                check=False,
            )

            success = result.returncode == 0

            if stage_id and stage_id in self.metrics["stages"]:
                self.metrics["stages"][stage_id]["output"].append(result.stdout)
                if result.stderr:
                    self.metrics["stages"][stage_id]["errors"].append(result.stderr)

            if not success:
                logger.error(f"❌ Command failed with return code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                self.metrics["errors"].append(
                    {
                        "command": cmd_str,
                        "error": result.stderr,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            logger.exception(f"⏰ Command timed out after {timeout}s")
            self.metrics["errors"].append(
                {
                    "command": cmd_str,
                    "error": f"Timeout after {timeout}s",
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return False, "", f"Timeout after {timeout}s"

        except Exception as e:
            logger.exception(f"💥 Exception running command: {e}")
            self.metrics["errors"].append(
                {
                    "command": cmd_str,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return False, "", str(e)

    async def check_extensions(self) -> bool:
        """Check if all Sphinx extensions are properly installed and configured."""
        stage_id = self.log_stage_start("extension_check")

        try:
            # Check extension imports
            test_script = """
import sys
import importlib

extensions_to_check = [
    "sphinx_tabs.tabs",
    "sphinx_gallery.gen_gallery",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "myst_parser"
]

failed_imports = []
for ext in extensions_to_check:
    try:
        importlib.import_module(ext)
        print(f"✓ {ext}")
    except ImportError as e:
        print(f"✗ {ext}: {e}")
        failed_imports.append(ext)

if failed_imports:
    print(f"FAILED_IMPORTS: {','.join(failed_imports)}")
    sys.exit(1)
else:
    print("ALL_EXTENSIONS_OK")
    sys.exit(0)
"""

            success, stdout, stderr = self.run_command(
                ["poetry", "run", "python", "-c", test_script], stage_id
            )

            if "FAILED_IMPORTS:" in stdout:
                failed = stdout.split("FAILED_IMPORTS: ")[1].strip().split(",")
                logger.error(f"Failed to import extensions: {failed}")
                self.log_stage_end(stage_id, False, f"Failed imports: {failed}")
                return False

            self.log_stage_end(stage_id, True, "All extensions import successfully")
            return True

        except Exception as e:
            logger.exception(f"Extension check failed: {e}")
            self.log_stage_end(stage_id, False, str(e))
            return False

    async def run_sphinx_build(self) -> bool:
        """Run Sphinx build with comprehensive monitoring."""
        stage_id = self.log_stage_start("sphinx_build")

        # Create build log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        build_log = self.logs_dir / f"sphinx_build_{timestamp}.log"

        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-j",
            "auto",
            "--keep-going",
            "-v",
            "-v",  # Double verbose
            str(self.docs_dir / "source"),
            str(self.docs_dir / "build" / "html"),
        ]

        logger.info(f"📝 Build log: {build_log}")

        try:
            # Run with streaming output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                cwd=self.base_dir,
            )

            pages_count = 0
            errors_count = 0
            warnings_count = 0

            with open(build_log, "w") as log_file:
                while True:
                    output = process.stdout.readline()
                    if output == "" and process.poll() is not None:
                        break

                    if output:
                        log_file.write(output)
                        log_file.flush()

                        # Track progress
                        if (
                            "reading sources" in output.lower()
                            or "writing output" in output.lower()
                        ):
                            pages_count += 1
                            if pages_count % 100 == 0:
                                logger.info(f"📄 Processed {pages_count} pages...")

                        if "ERROR" in output or "ImportError" in output:
                            errors_count += 1

                        if "WARNING" in output:
                            warnings_count += 1

                        # Show progress for key events
                        if any(
                            keyword in output.lower()
                            for keyword in ["building", "generating", "copying"]
                        ):
                            logger.debug(f"🔄 {output.strip()[:100]}...")

            return_code = process.wait()

            # Update metrics
            self.metrics["pages_processed"] = pages_count

            # Count generated HTML files
            html_dir = self.docs_dir / "build" / "html"
            if html_dir.exists():
                html_files = list(html_dir.glob("**/*.html"))
                self.metrics["html_files_generated"] = len(html_files)
                logger.info(f"📄 Generated {len(html_files)} HTML files")

            success = return_code == 0
            if success:
                logger.info("✅ Sphinx build completed successfully")
                logger.info(
                    f"📊 Pages: {pages_count}, Errors: {errors_count}, Warnings: {warnings_count}"
                )
            else:
                logger.error(f"❌ Sphinx build failed with return code {return_code}")

            self.log_stage_end(
                stage_id,
                success,
                f"Pages: {pages_count}, Errors: {errors_count}, Warnings: {warnings_count}",
            )
            return success

        except Exception as e:
            logger.exception(f"Sphinx build exception: {e}")
            self.log_stage_end(stage_id, False, str(e))
            return False

    async def analyze_build_results(self) -> dict:
        """Analyze build results and generate report."""
        stage_id = self.log_stage_start("result_analysis")

        try:
            # Find most recent build log
            build_logs = list(self.logs_dir.glob("sphinx_build_*.log"))
            if not build_logs:
                logger.warning("No build logs found")
                return {}

            latest_log = max(build_logs, key=lambda p: p.stat().st_mtime)
            logger.info(f"📊 Analyzing build log: {latest_log}")

            analysis = {
                "log_file": str(latest_log),
                "total_lines": 0,
                "errors": [],
                "warnings": [],
                "import_errors": [],
                "pages_by_package": {},
                "problematic_pages": [],
            }

            with open(latest_log) as f:
                lines = f.readlines()
                analysis["total_lines"] = len(lines)

                for i, line in enumerate(lines):
                    line = line.strip()

                    # Track errors
                    if "ERROR" in line or "ImportError" in line:
                        context_lines = lines[max(0, i - 2) : i + 3]
                        analysis["errors"].append(
                            {
                                "line_number": i + 1,
                                "error": line,
                                "context": [l.strip() for l in context_lines],
                            }
                        )

                        if "ImportError" in line or "cannot import" in line:
                            analysis["import_errors"].append(line)

                    # Track warnings
                    elif "WARNING" in line:
                        analysis["warnings"].append(
                            {"line_number": i + 1, "warning": line}
                        )

                    # Track pages by package
                    elif "reading sources" in line:
                        for package in [
                            "haive-core",
                            "haive-agents",
                            "haive-tools",
                            "haive-games",
                        ]:
                            if package in line:
                                analysis["pages_by_package"][package] = (
                                    analysis["pages_by_package"].get(package, 0) + 1
                                )

            # Find most problematic pages
            error_pages = {}
            for error in analysis["errors"]:
                for context_line in error["context"]:
                    if "reading sources" in context_line:
                        page = (
                            context_line.split("] ")[-1]
                            if "] " in context_line
                            else "unknown"
                        )
                        error_pages[page] = error_pages.get(page, 0) + 1

            analysis["problematic_pages"] = sorted(
                error_pages.items(), key=lambda x: x[1], reverse=True
            )[:10]

            # Save analysis report
            report_file = (
                self.reports_dir
                / f"build_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(report_file, "w") as f:
                json.dump(analysis, f, indent=2)

            logger.info(f"📋 Analysis saved to: {report_file}")
            logger.info(f"📊 Total errors: {len(analysis['errors'])}")
            logger.info(f"📊 Total warnings: {len(analysis['warnings'])}")
            logger.info(f"📊 Import errors: {len(analysis['import_errors'])}")

            self.log_stage_end(
                stage_id,
                True,
                f"Analysis complete: {len(analysis['errors'])} errors, {len(analysis['warnings'])} warnings",
            )
            return analysis

        except Exception as e:
            logger.exception(f"Build analysis failed: {e}")
            self.log_stage_end(stage_id, False, str(e))
            return {}

    async def run_full_pipeline(self) -> bool:
        """Run the complete documentation quality pipeline."""
        logger.info("🎯 Starting Documentation Quality Pipeline")
        self.metrics["start_time"] = time.time()

        try:
            # Stage 1: Check extensions
            if not await self.check_extensions():
                logger.error("❌ Extension check failed - aborting pipeline")
                return False

            # Stage 2: Run Sphinx build
            build_success = await self.run_sphinx_build()
            self.metrics["build_success"] = build_success

            # Stage 3: Analyze results (always run, even if build failed)
            await self.analyze_build_results()

            # Generate final report
            self.metrics["end_time"] = time.time()
            self.metrics["duration"] = (
                self.metrics["end_time"] - self.metrics["start_time"]
            )

            report_file = (
                self.reports_dir
                / f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(report_file, "w") as f:
                json.dump(self.metrics, f, indent=2)

            logger.info(f"🎯 Pipeline completed in {self.metrics['duration']:.2f}s")
            logger.info(f"📋 Full report: {report_file}")

            if build_success:
                logger.info("✅ Documentation build successful!")
                html_index = self.docs_dir / "build" / "html" / "index.html"
                if html_index.exists():
                    logger.info(f"🌐 View docs: file://{html_index.absolute()}")
            else:
                logger.error("❌ Documentation build failed - check logs for details")

            return build_success

        except Exception as e:
            logger.exception(f"💥 Pipeline failed with exception: {e}")
            self.metrics["errors"].append(
                {
                    "stage": "pipeline",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return False


async def main():
    """Main entry point."""
    pipeline = DocumentationQualityPipeline()
    success = await pipeline.run_full_pipeline()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
