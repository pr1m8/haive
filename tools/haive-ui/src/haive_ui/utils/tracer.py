"""Lightweight tracer for capturing agent/game execution traces."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class TraceEvent:
    """Single event in a trace."""

    timestamp: str
    event_type: str  # "input", "output", "tool_call", "llm_call", "error", "game_move"
    agent_name: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0


@dataclass
class Trace:
    """Complete execution trace."""

    trace_id: str
    name: str
    started_at: str
    events: list[TraceEvent] = field(default_factory=list)
    status: str = "running"  # running, completed, error
    total_duration_ms: float = 0.0
    token_usage: dict[str, int] = field(default_factory=lambda: {"input": 0, "output": 0, "total": 0})

    def add_event(self, event_type: str, agent_name: str, content: str, **metadata):
        """Add an event to the trace."""
        self.events.append(TraceEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            agent_name=agent_name,
            content=content[:2000],  # Truncate very long content
            metadata=metadata,
        ))

    def complete(self, duration_ms: float):
        """Mark trace as completed."""
        self.status = "completed"
        self.total_duration_ms = duration_ms

    def error(self, error_msg: str):
        """Mark trace as errored."""
        self.status = "error"
        self.add_event("error", "system", error_msg)


class TraceCollector:
    """Collects and stores traces in session state."""

    def __init__(self):
        self.traces: list[Trace] = []
        self._current_trace: Trace | None = None
        self._start_time: float = 0

    def start_trace(self, name: str) -> Trace:
        """Start a new trace."""
        import uuid

        trace = Trace(
            trace_id=str(uuid.uuid4())[:8],
            name=name,
            started_at=datetime.now().isoformat(),
        )
        self._current_trace = trace
        self._start_time = time.time()
        self.traces.append(trace)
        return trace

    def log(self, event_type: str, agent_name: str, content: str, **metadata):
        """Log an event to the current trace."""
        if self._current_trace:
            elapsed = (time.time() - self._start_time) * 1000
            self._current_trace.add_event(event_type, agent_name, content, elapsed_ms=elapsed, **metadata)

    def end_trace(self, status: str = "completed"):
        """End the current trace."""
        if self._current_trace:
            duration = (time.time() - self._start_time) * 1000
            if status == "completed":
                self._current_trace.complete(duration)
            else:
                self._current_trace.status = status
                self._current_trace.total_duration_ms = duration
            self._current_trace = None

    @property
    def current(self) -> Trace | None:
        return self._current_trace

    def get_recent(self, n: int = 20) -> list[Trace]:
        return list(reversed(self.traces[-n:]))
