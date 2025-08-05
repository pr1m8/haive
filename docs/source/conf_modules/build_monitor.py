"""Enhanced build monitoring with real-time progress tracking."""

from __future__ import annotations

import time
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import logging

logger = logging.getLogger("sphinx_config.monitor")


class BuildStage:
    """Represents a build stage with timing and progress info."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.status = "pending"
        self.progress = 0
        self.total = 0
        self.current_item = ""
        self.metrics: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def start(self):
        """Start this stage."""
        self.start_time = time.time()
        self.status = "running"
    
    def update_progress(self, current: int, total: int, item: str = ""):
        """Update progress for this stage."""
        self.progress = current
        self.total = total
        self.current_item = item
    
    def complete(self, status: str = "success"):
        """Mark stage as complete."""
        self.end_time = time.time()
        self.status = status
    
    @property
    def duration(self) -> float:
        """Get duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return 0
    
    @property
    def progress_percent(self) -> float:
        """Get progress as percentage."""
        if self.total > 0:
            return (self.progress / self.total) * 100
        return 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "progress": self.progress,
            "total": self.total,
            "progress_percent": round(self.progress_percent, 1),
            "current_item": self.current_item,
            "duration": round(self.duration, 1),
            "metrics": self.metrics,
            "errors": len(self.errors),
            "warnings": len(self.warnings)
        }


class BuildMonitor:
    """Monitor and track Sphinx build progress with detailed metrics."""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Track stages
        self.stages: Dict[str, BuildStage] = {}
        self.current_stage: Optional[str] = None
        self.start_time = time.time()
        
        # Metrics
        self.file_counts = defaultdict(int)
        self.extension_metrics = defaultdict(int)
        self.module_metrics = defaultdict(int)
        
        # Live monitoring
        self.monitor_file = self.log_dir / f"build_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.update_thread = None
        self.stop_monitoring = False
        
        # Define expected stages
        self._define_stages()
    
    def _define_stages(self):
        """Define the expected build stages."""
        stage_definitions = [
            ("config_init", "Configuration Initialization"),
            ("extension_load", "Loading Extensions"),
            ("import_diagnostics", "Import Diagnostics"),
            ("autoapi_analysis", "AutoAPI Code Analysis"),
            ("source_read", "Reading Source Files"),
            ("doctree_build", "Building Document Trees"),
            ("doctree_resolve", "Resolving References"),
            ("write_output", "Writing Output Files"),
            ("copy_static", "Copying Static Files"),
            ("generate_indices", "Generating Indices"),
            ("finalize", "Finalizing Build")
        ]
        
        for name, desc in stage_definitions:
            self.stages[name] = BuildStage(name, desc)
    
    def start_stage(self, stage_name: str, total_items: int = 0):
        """Start a new build stage."""
        if stage_name in self.stages:
            stage = self.stages[stage_name]
            stage.start()
            stage.total = total_items
            self.current_stage = stage_name
            
            logger.info(f"\n{'='*60}")
            logger.info(f"🚀 STARTING: {stage.description}")
            if total_items > 0:
                logger.info(f"📊 Total items: {total_items}")
            logger.info(f"{'='*60}")
            
            self._update_monitor_file()
    
    def update_progress(self, current: int, item_name: str = ""):
        """Update progress for current stage."""
        if self.current_stage and self.current_stage in self.stages:
            stage = self.stages[self.current_stage]
            stage.update_progress(current, stage.total, item_name)
            
            # Log progress at intervals
            if current % 10 == 0 or current == stage.total:
                percent = stage.progress_percent
                logger.info(f"📈 Progress: {current}/{stage.total} ({percent:.1f}%) - {item_name}")
    
    def add_metric(self, metric_name: str, value: Any):
        """Add a metric to the current stage."""
        if self.current_stage and self.current_stage in self.stages:
            stage = self.stages[self.current_stage]
            stage.metrics[metric_name] = value
    
    def track_file(self, file_type: str, file_path: str = ""):
        """Track file processing."""
        self.file_counts[file_type] += 1
        
        # Update current stage progress if applicable
        if self.current_stage == "autoapi_analysis":
            self.update_progress(self.file_counts["python_files"], file_path)
        elif self.current_stage == "source_read":
            self.update_progress(self.file_counts["source_files"], file_path)
        elif self.current_stage == "write_output":
            self.update_progress(self.file_counts["html_files"], file_path)
    
    def complete_stage(self, stage_name: str = None, status: str = "success"):
        """Complete a build stage."""
        stage_name = stage_name or self.current_stage
        if stage_name and stage_name in self.stages:
            stage = self.stages[stage_name]
            stage.complete(status)
            
            # Log completion
            icon = "✅" if status == "success" else "❌"
            logger.info(f"{icon} COMPLETED: {stage.description}")
            logger.info(f"⏱️  Duration: {stage.duration:.1f}s")
            if stage.metrics:
                logger.info(f"📊 Metrics: {json.dumps(stage.metrics, indent=2)}")
            
            self._update_monitor_file()
    
    def add_error(self, error_msg: str):
        """Add error to current stage."""
        if self.current_stage and self.current_stage in self.stages:
            self.stages[self.current_stage].errors.append(error_msg)
            logger.error(f"❌ ERROR in {self.current_stage}: {error_msg}")
    
    def add_warning(self, warning_msg: str):
        """Add warning to current stage."""
        if self.current_stage and self.current_stage in self.stages:
            self.stages[self.current_stage].warnings.append(warning_msg)
            logger.warning(f"⚠️  WARNING in {self.current_stage}: {warning_msg}")
    
    def get_summary(self) -> dict:
        """Get build summary."""
        total_duration = time.time() - self.start_time
        
        # Calculate stage statistics
        completed_stages = [s for s in self.stages.values() if s.status in ["success", "failed"]]
        running_stages = [s for s in self.stages.values() if s.status == "running"]
        pending_stages = [s for s in self.stages.values() if s.status == "pending"]
        
        # File statistics
        total_files = sum(self.file_counts.values())
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_duration": round(total_duration, 1),
            "stages": {
                "total": len(self.stages),
                "completed": len(completed_stages),
                "running": len(running_stages),
                "pending": len(pending_stages)
            },
            "files": {
                "total": total_files,
                "by_type": dict(self.file_counts)
            },
            "current_stage": self.current_stage,
            "stage_details": {name: stage.to_dict() for name, stage in self.stages.items()}
        }
    
    def _update_monitor_file(self):
        """Update the monitor file with current status."""
        try:
            summary = self.get_summary()
            with open(self.monitor_file, 'w') as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            logger.debug(f"Failed to update monitor file: {e}")
    
    def start_live_monitoring(self, update_interval: float = 1.0):
        """Start live monitoring in background thread."""
        def monitor_loop():
            while not self.stop_monitoring:
                self._update_monitor_file()
                time.sleep(update_interval)
        
        self.update_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.update_thread.start()
        
        logger.info(f"📊 Live monitoring started: {self.monitor_file}")
    
    def stop_live_monitoring(self):
        """Stop live monitoring."""
        self.stop_monitoring = True
        if self.update_thread:
            self.update_thread.join(timeout=2)
        
        # Final update
        self._update_monitor_file()
        
        # Print final summary
        self.print_summary()
    
    def print_summary(self):
        """Print a visual summary of the build."""
        summary = self.get_summary()
        
        print("\n" + "="*80)
        print("📊 BUILD SUMMARY")
        print("="*80)
        print(f"Total Duration: {summary['total_duration']}s")
        print(f"Stages: {summary['stages']['completed']}/{summary['stages']['total']} completed")
        print(f"Files Processed: {summary['files']['total']}")
        
        print("\n📈 Stage Progress:")
        for name, stage in self.stages.items():
            status_icon = {
                "success": "✅",
                "failed": "❌",
                "running": "🔄",
                "pending": "⏳"
            }.get(stage.status, "❓")
            
            if stage.status in ["success", "failed"]:
                print(f"{status_icon} {stage.description:<40} {stage.duration:>6.1f}s")
            elif stage.status == "running":
                print(f"{status_icon} {stage.description:<40} {stage.progress_percent:>5.1f}%")
            else:
                print(f"{status_icon} {stage.description:<40} pending")
        
        print("\n📁 Files by Type:")
        for file_type, count in sorted(summary['files']['by_type'].items()):
            print(f"  {file_type}: {count}")
        
        print("="*80)


# Global monitor instance
_monitor: Optional[BuildMonitor] = None


def get_monitor() -> Optional[BuildMonitor]:
    """Get the global monitor instance."""
    return _monitor


def init_monitor(log_dir: Path) -> BuildMonitor:
    """Initialize the global monitor."""
    global _monitor
    _monitor = BuildMonitor(log_dir)
    _monitor.start_live_monitoring()
    return _monitor


def track_sphinx_event(event_name: str, *args, **kwargs):
    """Track Sphinx events in the monitor."""
    monitor = get_monitor()
    if not monitor:
        return
    
    # Map Sphinx events to our stages
    event_mapping = {
        "config-inited": ("config_init", "complete"),
        "builder-inited": ("extension_load", "complete"),
        "env-get-outdated": ("source_read", "start"),
        "env-before-read-docs": ("source_read", "start"),
        "env-updated": ("source_read", "complete"),
        "doctree-resolved": ("doctree_resolve", "progress"),
        "html-page-context": ("write_output", "progress"),
        "build-finished": ("finalize", "complete")
    }
    
    if event_name in event_mapping:
        stage_name, action = event_mapping[event_name]
        
        if action == "start":
            monitor.start_stage(stage_name)
        elif action == "complete":
            monitor.complete_stage(stage_name)
        elif action == "progress":
            # Extract file info if available
            if args and hasattr(args[0], 'docname'):
                monitor.update_progress(monitor.file_counts["doctrees"], args[0].docname)


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """Create a text progress bar."""
    if total == 0:
        return "[" + " " * width + "]"
    
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{total} ({percent*100:.1f}%)"