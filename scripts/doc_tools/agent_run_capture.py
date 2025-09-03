#!/usr/bin/env python3
"""Agent Run Capture System for Documentation.

This module provides utilities for capturing agent execution outputs,
including logs, state transitions, and graph visualizations for
documentation.
"""
from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml
from pydantic import BaseModel
from pydantic import Field

# Ensure haive packages are in path
workspace_root = Path(__file__).resolve().parents[2]
packages_dir = workspace_root / 'packages'
for package in ['haive-core', 'haive-agents', 'haive-tools', 'haive-games']:
    package_path = packages_dir / package / 'src'
    if package_path.exists():
        sys.path.insert(0, str(package_path))


class AgentRunMetadata(BaseModel):
    """Metadata for an agent run."""

    run_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_name: str
    agent_type: str
    timestamp: datetime = Field(default_factory=datetime.now)
    duration: float = 0.0
    success: bool = True
    error: str | None = None
    input_data: dict[str, Any] = Field(default_factory=dict)
    output_data: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)


class AgentRunCapture(BaseModel):
    """Complete capture of an agent run."""

    metadata: AgentRunMetadata
    logs: list[dict[str, Any]] = Field(default_factory=list)
    state_transitions: list[dict[str, Any]] = Field(default_factory=list)
    messages: list[dict[str, Any]] = Field(default_factory=list)
    graph_visualizations: list[str] = Field(default_factory=list)
    performance_metrics: dict[str, Any] = Field(default_factory=dict)


class LogCapture(logging.Handler):
    """Custom logging handler to capture logs during agent execution."""

    def __init__(self):
        super().__init__()
        self.logs = []
        self.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        )

    def emit(self, record):
        """Capture log record."""
        self.logs.append(
            {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': self.format(record),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
            },
        )

    def clear(self):
        """Clear captured logs."""
        self.logs = []

    def get_logs(self):
        """Get captured logs."""
        return self.logs.copy()


class AgentRunner:
    """Runner for capturing agent execution for documentation.

    This class handles:
    - Setting up logging capture
    - Running agents with monitoring
    - Capturing state transitions
    - Saving outputs in structured format
    - Generating graph visualizations
    """

    def __init__(self, output_dir: str | Path | None = None):
        """Initialize the runner."""
        if output_dir is None:
            output_dir = workspace_root / 'docs' / 'resources' / 'agent_runs'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set up log capture
        self.log_capture = LogCapture()
        self.original_handlers = []

    def _setup_logging(self):
        """Set up logging to capture agent execution logs."""
        # Get root logger
        root_logger = logging.getLogger()

        # Save original handlers
        self.original_handlers = root_logger.handlers.copy()

        # Add our capture handler
        root_logger.addHandler(self.log_capture)

        # Also capture haive-specific loggers
        for logger_name in ['haive', 'langchain', 'langgraph']:
            logger = logging.getLogger(logger_name)
            logger.addHandler(self.log_capture)
            logger.setLevel(logging.DEBUG)

    def _restore_logging(self):
        """Restore original logging configuration."""
        root_logger = logging.getLogger()
        root_logger.removeHandler(self.log_capture)

        for logger_name in ['haive', 'langchain', 'langgraph']:
            logger = logging.getLogger(logger_name)
            logger.removeHandler(self.log_capture)

    async def run_agent_async(
        self,
        agent,
        input_data: dict[str, Any],
        config: dict[str, Any] | None = None,
        capture_graph: bool = True,
    ) -> AgentRunCapture:
        """Run an agent asynchronously and capture output."""
        # Create metadata
        metadata = AgentRunMetadata(
            agent_name=getattr(agent, 'name', agent.__class__.__name__),
            agent_type=agent.__class__.__name__,
            input_data=input_data,
            config=config or {},
        )

        # Create capture object
        capture = AgentRunCapture(metadata=metadata)

        # Set up logging
        self.log_capture.clear()
        self._setup_logging()

        # Record start time
        start_time = time.time()

        try:
            # Run the agent
            if hasattr(agent, 'ainvoke'):
                result = await agent.ainvoke(input_data, config)
            else:
                # Fall back to sync invoke in async context
                result = await asyncio.to_thread(agent.invoke, input_data, config)

            # Record success
            metadata.success = True
            metadata.output_data = (
                result if isinstance(result, dict) else {'result': result}
            )

        except Exception as e:
            # Record failure
            metadata.success = False
            metadata.error = str(e)
            logging.error(f"Agent execution failed: {e}", exc_info=True)
            raise

        finally:
            # Record duration
            metadata.duration = time.time() - start_time

            # Capture logs
            capture.logs = self.log_capture.get_logs()

            # Restore logging
            self._restore_logging()

            # Capture graph visualization if available
            if capture_graph and hasattr(agent, 'visualize_graph'):
                try:
                    graph_path = self._capture_graph(agent, metadata.run_id)
                    if graph_path:
                        capture.graph_visualizations.append(str(graph_path))
                except Exception as e:
                    logging.warning(f"Failed to capture graph: {e}")

            # Extract state transitions from logs
            capture.state_transitions = self._extract_state_transitions(capture.logs)

            # Extract messages
            capture.messages = self._extract_messages(capture.logs)

            # Calculate performance metrics
            capture.performance_metrics = self._calculate_metrics(capture)

        return capture

    def run_agent(
        self,
        agent,
        input_data: dict[str, Any],
        config: dict[str, Any] | None = None,
        capture_graph: bool = True,
    ) -> AgentRunCapture:
        """Run an agent synchronously and capture output."""
        # Create async event loop if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.run_agent_async(agent, input_data, config, capture_graph),
        )

    def _capture_graph(self, agent, run_id: str) -> Path | None:
        """Capture agent graph visualization."""
        try:
            # Import visualization utilities
            from haive.core.utils.visualize_graph_utils import visualize_graph

            # Generate graph
            graph_dir = self.output_dir / 'graphs'
            graph_dir.mkdir(exist_ok=True)

            graph_path = graph_dir / f"{run_id}.png"

            # Get the graph from agent
            if hasattr(agent, '_app') and agent._app:
                graph = agent._app
            elif hasattr(agent, 'graph'):
                graph = agent.graph
            else:
                return None

            # Visualize and save
            visualize_graph(graph, output_path=str(graph_path))
            return graph_path

        except Exception as e:
            logging.warning(f"Failed to visualize graph: {e}")
            return None

    def _extract_state_transitions(self, logs: list[dict]) -> list[dict]:
        """Extract state transitions from logs."""
        transitions = []

        for log in logs:
            message = log.get('message', '')

            # Look for state transition patterns
            if any(
                pattern in message
                for pattern in [
                    'State update',
                    'STATE UPDATE',
                    'Transitioning to',
                    'state:',
                    'State:',
                    'New state:',
                    'Updated state:',
                ]
            ):
                transitions.append(
                    {
                        'timestamp': log['timestamp'],
                        'message': message,
                        'type': 'state_change',
                    },
                )

        return transitions

    def _extract_messages(self, logs: list[dict]) -> list[dict]:
        """Extract agent messages from logs."""
        messages = []

        for log in logs:
            message = log.get('message', '')

            # Look for message patterns
            if any(
                pattern in message
                for pattern in [
                    'Message:',
                    'message:',
                    'AIMessage',
                    'HumanMessage',
                    'ToolMessage',
                    'SystemMessage',
                ]
            ):
                messages.append(
                    {
                        'timestamp': log['timestamp'],
                        'content': message,
                        'type': 'message',
                    },
                )

        return messages

    def _calculate_metrics(self, capture: AgentRunCapture) -> dict[str, Any]:
        """Calculate performance metrics from capture."""
        return {
            'total_logs': len(capture.logs),
            'error_logs': len([l for l in capture.logs if l['level'] == 'ERROR']),
            'warning_logs': len([l for l in capture.logs if l['level'] == 'WARNING']),
            'state_transitions': len(capture.state_transitions),
            'messages': len(capture.messages),
            'duration_seconds': capture.metadata.duration,
        }

    def save_capture(self, capture: AgentRunCapture, format: str = 'yaml') -> Path:
        """Save capture to file."""
        filename = f"{capture.metadata.agent_name}_{capture.metadata.run_id}"

        if format == 'yaml':
            output_path = self.output_dir / f"{filename}.yaml"
            with open(output_path, 'w') as f:
                yaml.dump(capture.model_dump(), f, default_flow_style=False)
        else:
            output_path = self.output_dir / f"{filename}.json"
            with open(output_path, 'w') as f:
                json.dump(capture.model_dump(), f, indent=2, default=str)

        return output_path

    def create_rst_snippet(self, capture: AgentRunCapture) -> str:
        """Create RST snippet for embedding in documentation."""
        rst = f"""
.. _agent-run-{capture.metadata.run_id}:

{capture.metadata.agent_name} Run Output
{"=" * (len(capture.metadata.agent_name) + 11)}

.. container:: agent-run-output
   :data-paginated: true
   :data-page-size: 50

   .. container:: run-header

      **Agent:** {capture.metadata.agent_name}

      **Type:** {capture.metadata.agent_type}

      **Timestamp:** {capture.metadata.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

      **Duration:** {capture.metadata.duration:.2f}s

      **Status:** {"✅ Success" if capture.metadata.success else "❌ Failed"}

   .. container:: run-content

      .. code-block:: text

"""

        # Add log content
        for log in capture.logs[:100]:  # First 100 logs
            rst += f"         [{log['timestamp']}] {log['level']}: {log['message']}\n"

        if len(capture.logs) > 100:
            rst += f"\n         ... and {len(capture.logs) - 100} more logs\n"

        # Add graph visualization if available
        if capture.graph_visualizations:
            rst += f"""

.. container:: agent-graph

   .. image:: {capture.graph_visualizations[0]}
      :alt: Agent Graph Visualization
      :align: center
"""

        return rst


def capture_example_agents():
    """Capture runs for example agents."""
    runner = AgentRunner()

    # Import some example agents
    try:
        from haive.agents.react import ReactAgent
        from haive.agents.simple import SimpleAgent

        # Example captures
        agents_to_capture = [
            (SimpleAgent(name='SimpleExample'), {'messages': ['Hello, how are you?']}),
            (ReactAgent(name='ReactExample'), {'messages': ['What is 2+2?']}),
        ]

        for agent, input_data in agents_to_capture:
            try:
                capture = runner.run_agent(agent, input_data)

                # Save capture
                output_path = runner.save_capture(capture)

                # Generate RST
                rst_path = output_path.with_suffix('.rst')
                with open(rst_path, 'w') as f:
                    f.write(runner.create_rst_snippet(capture))

            except Exception:
                pass

    except ImportError:
        pass


if __name__ == '__main__':
    # Run example captures
    capture_example_agents()
