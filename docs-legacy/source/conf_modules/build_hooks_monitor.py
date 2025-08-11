"""Build hooks with integrated monitoring for detailed progress tracking."""

from __future__ import annotations

import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Any

from build_monitor import get_monitor, init_monitor

logger = logging.getLogger("sphinx_config.hooks.monitor")

# Track various metrics
_metrics = {
    "files_by_type": {},
    "extensions_loaded": set(),
    "warnings_by_type": {},
    "errors_by_type": {},
    "doctrees_built": set(),
    "html_files_written": set(),
    "static_files_copied": set(),
}


def on_config_inited(app, config):
    """Called when config is initialized."""
    monitor = get_monitor()
    if monitor:
        monitor.start_stage("config_init")
        monitor.add_metric("source_dir", str(app.srcdir))
        monitor.add_metric("output_dir", str(app.outdir))
        monitor.complete_stage("config_init")


def on_builder_inited(app):
    """Called when builder is initialized."""
    monitor = get_monitor()
    if monitor:
        monitor.start_stage("extension_load")
        monitor.add_metric("builder_name", app.builder.name)
        monitor.add_metric("builder_format", app.builder.format)

        # Count loaded extensions
        if hasattr(app, "extensions"):
            monitor.add_metric("extensions_count", len(app.extensions))

        monitor.complete_stage("extension_load")


def on_env_get_outdated(app, env, added, changed, removed):
    """Called to get outdated docs."""
    monitor = get_monitor()
    if monitor:
        total_docs = len(added) + len(changed)
        if total_docs > 0:
            monitor.start_stage("source_read", total_docs)
            monitor.add_metric("added_files", len(added))
            monitor.add_metric("changed_files", len(changed))
            monitor.add_metric("removed_files", len(removed))


def on_source_read(app, docname, source):
    """Called when a source file is read."""
    monitor = get_monitor()
    if monitor and monitor.current_stage == "source_read":
        monitor.track_file("source_files", docname)

        # Track file type
        file_ext = Path(docname).suffix
        _metrics["files_by_type"][file_ext] = _metrics["files_by_type"].get(file_ext, 0) + 1


def on_doctree_read(app, doctree):
    """Called when a doctree is read."""
    monitor = get_monitor()
    if monitor:
        if monitor.current_stage != "doctree_build":
            monitor.start_stage("doctree_build")
        monitor.track_file("doctrees", "")


def on_doctree_resolved(app, doctree, docname):
    """Called when doctree is resolved."""
    monitor = get_monitor()
    if monitor:
        if monitor.current_stage != "doctree_resolve":
            # Count total doctrees to resolve
            total_docs = len(app.env.found_docs) if hasattr(app.env, "found_docs") else 0
            monitor.start_stage("doctree_resolve", total_docs)

        _metrics["doctrees_built"].add(docname)
        monitor.track_file("doctrees_resolved", docname)


def on_html_page_context(app, pagename, templatename, context, doctree):
    """Called when HTML page context is created."""
    # Only process for HTML builder
    if not hasattr(app, "builder") or app.builder.name != "html":
        return

    monitor = get_monitor()
    if monitor:
        if monitor.current_stage != "write_output":
            # Estimate total pages
            total_pages = len(app.env.found_docs) if hasattr(app.env, "found_docs") else 0
            monitor.start_stage("write_output", total_pages)

        _metrics["html_files_written"].add(pagename)
        monitor.track_file("html_files", pagename)


def on_html_collect_pages(app):
    """Called to collect additional HTML pages to write."""
    # Only process for HTML builder
    if not hasattr(app, "builder") or app.builder.name != "html":
        return []

    monitor = get_monitor()
    if monitor and monitor.current_stage == "write_output":
        # This is where indices and search pages are generated
        monitor.add_metric("indices_generated", True)

    # Return empty list (no additional pages)
    return []


def on_copy_static_files(app, exception):
    """Called after static files are copied."""
    monitor = get_monitor()
    if monitor:
        if not exception:
            monitor.start_stage("copy_static")

            # Count static files
            static_dir = Path(app.outdir) / "_static"
            if static_dir.exists():
                static_files = list(static_dir.rglob("*"))
                monitor.add_metric("static_files_count", len(static_files))

                # Track by type
                static_by_type = {}
                for f in static_files:
                    if f.is_file():
                        ext = f.suffix or "no_extension"
                        static_by_type[ext] = static_by_type.get(ext, 0) + 1
                monitor.add_metric("static_by_type", static_by_type)

            monitor.complete_stage("copy_static")


def on_build_finished(app, exception):
    """Called when build is finished."""
    monitor = get_monitor()
    if monitor:
        # Complete any running stages
        if monitor.current_stage:
            status = "failed" if exception else "success"
            monitor.complete_stage(monitor.current_stage, status)

        # Start and complete finalize stage
        monitor.start_stage("finalize")

        # Add final metrics
        monitor.add_metric("total_doctrees", len(_metrics["doctrees_built"]))
        monitor.add_metric("total_html_files", len(_metrics["html_files_written"]))
        monitor.add_metric("files_by_type", dict(_metrics["files_by_type"]))

        # Count actual HTML files in output
        html_dir = Path(app.outdir)
        if html_dir.exists():
            actual_html_files = list(html_dir.rglob("*.html"))
            monitor.add_metric("actual_html_files", len(actual_html_files))

            # Sample some files
            if actual_html_files:
                monitor.add_metric(
                    "sample_html_files",
                    [str(f.relative_to(html_dir)) for f in actual_html_files[:10]],
                )

        # Complete finalize
        status = "failed" if exception else "success"
        if exception:
            monitor.add_error(str(exception))

        monitor.complete_stage("finalize", status)

        # Stop monitoring and print summary
        monitor.stop_live_monitoring()


def on_warning_emitted(app, warning):
    """Called when a warning is emitted."""
    monitor = get_monitor()
    if monitor:
        monitor.add_warning(str(warning))

        # Categorize warning
        warning_str = str(warning)
        if "docstring" in warning_str:
            category = "docstring"
        elif "reference" in warning_str:
            category = "reference"
        elif "toctree" in warning_str:
            category = "toctree"
        else:
            category = "other"

        _metrics["warnings_by_type"][category] = _metrics["warnings_by_type"].get(category, 0) + 1


def on_env_updated(app, env):
    """Called when environment is updated."""
    monitor = get_monitor()
    if monitor and monitor.current_stage == "source_read":
        monitor.complete_stage("source_read")

        # Add environment metrics
        if hasattr(env, "found_docs"):
            monitor.add_metric("total_documents", len(env.found_docs))
        if hasattr(env, "dependencies"):
            monitor.add_metric("total_dependencies", len(env.dependencies))


def on_autoapi_skip_member(app, what, name, obj, skip, options):
    """Called by AutoAPI when deciding to skip a member."""
    # Track what's being processed
    monitor = get_monitor()
    if monitor and monitor.current_stage != "autoapi_analysis":
        # We're now in AutoAPI analysis phase
        monitor.complete_stage(
            "import_diagnostics"
        ) if monitor.current_stage == "import_diagnostics" else None
        monitor.start_stage("autoapi_analysis")

    return skip


def setup(app):
    """Setup monitoring hooks."""
    # Initialize monitor
    log_dir = Path(app.srcdir) / "logs" / "build"
    init_monitor(log_dir)

    logger.info("📊 Build monitoring initialized")

    # Core events
    app.connect("config-inited", on_config_inited)
    app.connect("builder-inited", on_builder_inited)
    app.connect("env-get-outdated", on_env_get_outdated)
    app.connect("build-finished", on_build_finished)

    # Document processing events
    app.connect("source-read", on_source_read)
    app.connect("doctree-resolved", on_doctree_resolved)
    app.connect("env-updated", on_env_updated)

    # HTML builder events - will be checked at runtime
    app.connect("html-page-context", on_html_page_context)
    app.connect("html-collect-pages", on_html_collect_pages)

    # AutoAPI events
    app.connect("autoapi-skip-member", on_autoapi_skip_member)

    # Warning tracking
    if hasattr(app, "connect"):
        try:
            app.connect("warning-emitted", on_warning_emitted)
        except:
            pass

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
