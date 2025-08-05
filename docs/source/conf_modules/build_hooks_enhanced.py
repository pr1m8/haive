"""Enhanced build event hooks with structured error collection."""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
import time

logger = logging.getLogger("sphinx_config.hooks")

# Track build timing
build_start_time = None
phase_times = {}


def on_config_inited(app, config):
    """Called when config is initialized."""
    global build_start_time
    build_start_time = time.time()

    logger.info("\n" + "=" * 80)
    logger.info("🏗️  SPHINX BUILD STARTED")
    logger.info("=" * 80)
    logger.info(f"📅 Time: {datetime.now()}")
    logger.info(f"📁 Source: {app.srcdir}")
    logger.info(f"📁 Output: {app.outdir}")
    # Builder is not available yet in config-inited event
    logger.info("=" * 80 + "\n")


def on_builder_inited(app):
    """Called when builder is initialized."""
    logger.info(f"🔨 Builder initialized: {app.builder.name}")
    logger.debug(f"  Format: {app.builder.format}")
    logger.debug(
        f"  Supported image types: {
            getattr(
                app.builder,
                'supported_image_types',
                'N/A')}")


def on_env_get_outdated(app, env, added, changed, removed):
    """Called to get outdated docs."""
    total_changes = len(added) + len(changed) + len(removed)

    if total_changes > 0:
        logger.info("\n📊 Document changes detected:")
        logger.info(f"  ➕ Added: {len(added)} files")
        logger.info(f"  ✏️  Changed: {len(changed)} files")
        logger.info(f"  ➖ Removed: {len(removed)} files")

        if logger.isEnabledFor(logging.DEBUG):
            if added and len(added) <= 5:
                logger.debug(f"  Added files: {added}")
            elif added:
                logger.debug(f"  Added files (first 5): {added[:5]}...")
            if changed and len(changed) <= 5:
                logger.debug(f"  Changed files: {changed}")
            elif changed:
                logger.debug(f"  Changed files (first 5): {changed[:5]}...")


def on_source_read(app, docname, source):
    """Called when a source file is read."""
    logger.debug(f"📖 Reading: {docname}")


def on_doctree_resolved(app, doctree, docname):
    """Called when doctree is resolved."""
    logger.debug(f"🌳 Resolved doctree: {docname}")


def on_env_warning(app, node, msg):
    """Called when a warning is emitted."""
    logger.warning(
        f"⚠️  {msg}",
        extra={
            "category": "doctree_warning",
            "docname": getattr(node, "source", "unknown")
        },
    )


def on_build_finished(app, exception):
    """Enhanced build finished handler with structured report."""
    build_time = time.time() - build_start_time if build_start_time else 0

    # Try to import structured logging components
    try:
        from structured_logging import error_collector

        # Generate structured report
        report_dir = Path(app.srcdir) / "logs" / "build"
        report_dir.mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"build_report_{timestamp}.json"

        # Collect build statistics
        build_stats = {
            "builder": app.builder.name,
            "source_dir": str(app.srcdir),
            "output_dir": str(app.outdir),
            "success": exception is None,
            "exception": str(exception) if exception else None,
            "build_time_seconds": round(build_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Get error summary
        error_summary = error_collector.get_summary()

        # Load extension status if available
        extension_status = load_extension_status()

        # Combine into final report
        final_report = {
            "build_info": build_stats,
            "errors_and_warnings": error_summary,
            "extension_status": extension_status,
            "phase_timings": phase_times,
        }

        # Save report
        with open(report_file, "w") as f:
            json.dump(final_report, f, indent=2)

        # Print summary to console
        logger.info("\n" + "=" * 80)
        logger.info("📊 BUILD SUMMARY")
        logger.info("=" * 80)

        # Extension summary
        if extension_status:
            extension_status.get("categories", {})
            total_loaded = len(extension_status.get("loaded", []))
            total_failed = len(extension_status.get("failed", []))
            total_optional = len(extension_status.get("optional_missing", []))

            logger.info("\n🔌 Extensions:")
            logger.info(f"  ✅ Loaded: {total_loaded}")
            if total_optional > 0:
                logger.info(f"  ⚠️  Optional missing: {total_optional}")
            if total_failed > 0:
                logger.error(f"  ❌ Failed: {total_failed}")

        # Error/warning summary
        if error_summary["summary"]["total_errors"] > 0:
            logger.error(
                f"\n❌ Errors: {error_summary['summary']['total_errors']}")
            for category, errors in error_summary["errors"].items():
                logger.error(f"  - {category}: {len(errors)} errors")

        if error_summary["summary"]["total_warnings"] > 0:
            logger.warning(
                f"\n⚠️  Warnings: {error_summary['summary']['total_warnings']}"
            )
            for category, warnings in error_summary["warnings"].items():
                logger.warning(f"  - {category}: {len(warnings)} warnings")

        # Build result
        if exception:
            logger.error(f"\n🚫 Build FAILED with: {exception}")
        else:
            logger.info("\n✅ Build COMPLETED successfully!")

        logger.info(f"\n⏱️  Total build time: {build_time:.2f} seconds")
        logger.info(f"📄 Detailed report: {report_file}")

    except ImportError:
        # Fallback if structured logging not available
        logger.info("\n" + "=" * 80)
        if exception:
            logger.error(f"❌ BUILD FAILED: {exception}")
        else:
            logger.info("✅ BUILD SUCCESSFUL")
        logger.info(f"⏱️  Total time: {build_time:.2f} seconds")

    logger.info("=" * 80)


def load_extension_status():
    """Load extension status if available."""
    try:
        status_file = Path(
            __file__
        ).parent.parent / "logs" / "build" / "extension_status.json"
        if status_file.exists():
            with open(status_file) as f:
                return json.load(f)
    except Exception as e:
        logger.debug(f"Could not load extension status: {e}")
    return None


def setup(app):
    """Setup enhanced build hooks."""
    # Core build events
    app.connect("config-inited", on_config_inited)
    app.connect("builder-inited", on_builder_inited)
    app.connect("env-get-outdated", on_env_get_outdated)
    app.connect("build-finished", on_build_finished)

    # Optional detailed events (only in debug mode)
    if logger.isEnabledFor(logging.DEBUG):
        app.connect("source-read", on_source_read)
        app.connect("doctree-resolved", on_doctree_resolved)

    # Warning handler
    if hasattr(app, "connect"):
        try:
            app.connect("env-warning", on_env_warning)
        except BaseException:
            pass  # Not all Sphinx versions support this

    logger.info("🪝 Build hooks registered")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
