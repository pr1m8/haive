#!/usr/bin/env python3
"""Universal Example Runner - Execute any agent example with streaming and visualization.

This module provides a unified interface to run any agent example across the Haive ecosystem,
regardless of agent type, architecture, or execution pattern. It handles streaming output,
visualization generation, and graceful error recovery.
"""

import asyncio
from dataclasses import dataclass, field
import importlib.util
import logging
from pathlib import Path
import sys
import time
import traceback
from typing import Any

from scripts.doc_utils.agent_analyzer import AgentAnalyzer, AgentArchitecture, AgentInfo

logger = logging.getLogger(__name__)


@dataclass
class ExecutionConfig:
    """Configuration for example execution."""

    max_output_size: int = 10_000_000  # 10MB max output
    chunk_size: int = 1024  # 1KB chunks for streaming
    enable_visualization: bool = True
    visualization_path: Path | None = None
    timeout_seconds: int = 300  # 5 minute timeout
    stream_output: bool = True
    save_full_output: bool = True
    output_file: Path | None = None


@dataclass
class ExecutionResult:
    """Result of example execution."""

    success: bool
    output: str = ""
    error: str | None = None
    execution_time: float = 0.0
    agent_info: AgentInfo | None = None
    visualization_path: Path | None = None
    output_file: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class OutputStreamer:
    """Handle streaming output with chunking and size limits."""

    def __init__(self, config: ExecutionConfig):
        self.config = config
        self.total_size = 0
        self.chunks: list[str] = []
        self.full_output_file: Path | None = None

    def add_chunk(self, chunk: str) -> bool:
        """Add a chunk of output.

        Args:
            chunk: Output chunk to add

        Returns:
            True if chunk was added, False if size limit exceeded
        """
        chunk_size = len(chunk.encode("utf-8"))

        if self.total_size + chunk_size > self.config.max_output_size:
            # Size limit exceeded, save to file
            if self.config.save_full_output and not self.full_output_file:
                self._save_to_file(chunk)
            return False

        self.chunks.append(chunk)
        self.total_size += chunk_size

        if self.config.stream_output:
            # Stream chunk to stdout
            pass

        return True

    def _save_to_file(self, final_chunk: str = ""):
        """Save full output to file when size limit is reached."""
        if not self.config.output_file:
            timestamp = int(time.time())
            self.full_output_file = Path(f"agent_output_{timestamp}.txt")
        else:
            self.full_output_file = self.config.output_file

        try:
            with open(self.full_output_file, "w", encoding="utf-8") as f:
                f.write("".join(self.chunks))
                if final_chunk:
                    f.write(final_chunk)

        except Exception as e:
            logger.exception(f"Failed to save output to file: {e}")

    def get_output(self) -> str:
        """Get the complete output."""
        return "".join(self.chunks)

    def finalize(self) -> Path | None:
        """Finalize output and return file path if output was saved to file."""
        if self.total_size > self.config.max_output_size:
            if not self.full_output_file:
                self._save_to_file()
            return self.full_output_file
        return None


class UniversalExampleRunner:
    """Universal runner for any agent example."""

    def __init__(self, project_root: Path | None = None):
        """Initialize the runner.

        Args:
            project_root: Root directory of the Haive project
        """
        self.analyzer = AgentAnalyzer(project_root)
        self.project_root = self.analyzer.project_root

    async def discover_all_examples(self) -> list[Path]:
        """Discover all example files across the project.

        Returns:
            List of example file paths
        """
        logger.info("Discovering all examples...")

        example_files = []

        # Discover through agent analysis
        agents = self.analyzer.discover_all_agents()
        for agent in agents:
            example_files.extend(agent.example_files)

        # Also scan for standalone example files
        for examples_dir in [
                self.project_root / "examples",
                self.project_root / "packages" / "haive-agents" / "examples",
                self.project_root / "packages" / "haive-core" / "examples",
                self.project_root / "packages" / "haive-games" / "examples",
                self.project_root / "packages" / "haive-mcp" / "examples",
                self.project_root / "packages" / "haive-tools" / "examples",
        ]:
            if examples_dir.exists():
                for example_file in examples_dir.rglob("*.py"):
                    if example_file not in example_files:
                        example_files.append(example_file)

        # Also find embedded examples
        for package_dir in (self.project_root / "packages").glob("haive-*"):
            if package_dir.is_dir():
                for example_file in package_dir.rglob("example*.py"):
                    if example_file not in example_files:
                        example_files.append(example_file)

        logger.info(f"Found {len(example_files)} example files")
        return list(set(example_files))  # Remove duplicates

    async def run_example(
        self,
        example_path: str | Path,
        config: ExecutionConfig | None = None,
    ) -> ExecutionResult:
        """Run a single example with full monitoring and streaming.

        Args:
            example_path: Path to the example file
            config: Execution configuration

        Returns:
            Execution result
        """
        if config is None:
            config = ExecutionConfig()

        example_path = Path(example_path)
        if not example_path.exists():
            return ExecutionResult(
                success=False,
                error=f"Example file not found: {example_path}",
            )

        logger.info(f"Running example: {example_path}")
        start_time = time.time()

        # Initialize output streamer
        streamer = OutputStreamer(config)

        try:
            # Detect associated agent if possible
            agent_info = await self._detect_agent_for_example(example_path)

            # Generate visualization if requested and possible
            visualization_path = None
            if config.enable_visualization and agent_info and agent_info.has_visualization:
                visualization_path = await self._generate_visualization(
                    agent_info,
                    config.visualization_path,
                )

            # Execute the example
            success, output, error = await self._execute_example_safely(
                example_path,
                streamer,
                config,
            )

            execution_time = time.time() - start_time

            # Finalize output
            output_file = streamer.finalize()

            return ExecutionResult(
                success=success,
                output=output,
                error=error,
                execution_time=execution_time,
                agent_info=agent_info,
                visualization_path=visualization_path,
                output_file=output_file,
                metadata={
                    "example_path": str(example_path),
                    "output_chunks": len(streamer.chunks),
                    "total_output_size": streamer.total_size,
                },
            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.exception(f"Failed to run example {example_path}: {e}")

            return ExecutionResult(
                success=False,
                error=str(e),
                execution_time=execution_time,
                metadata={
                    "example_path": str(example_path),
                    "exception_type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                },
            )

    async def _detect_agent_for_example(
            self, example_path: Path) -> AgentInfo | None:
        """Detect which agent is associated with an example.

        Args:
            example_path: Path to the example file

        Returns:
            AgentInfo if detected, None otherwise
        """
        try:
            # Look for agent.py in same directory
            example_dir = example_path.parent
            agent_file = example_dir / "agent.py"

            if agent_file.exists():
                return self.analyzer._analyze_agent_file(agent_file)

            # Look for agent files in parent directories
            current_dir = example_dir
            for _ in range(3):  # Look up to 3 levels up
                for agent_file in current_dir.glob("*agent*.py"):
                    if agent_file.stem != example_path.stem:  # Not the example itself
                        agent_info = self.analyzer._analyze_agent_file(
                            agent_file)
                        if agent_info:
                            return agent_info
                current_dir = current_dir.parent
                if current_dir == current_dir.parent:  # Reached root
                    break

            return None

        except Exception as e:
            logger.warning(f"Failed to detect agent for {example_path}: {e}")
            return None

    async def _generate_visualization(
        self,
        agent_info: AgentInfo,
        viz_path: Path | None = None,
    ) -> Path | None:
        """Generate visualization for an agent.

        Args:
            agent_info: Agent information
            viz_path: Optional path for visualization file

        Returns:
            Path to generated visualization or None if failed
        """
        if not agent_info.has_visualization:
            return None

        try:
            # Import the agent module
            spec = importlib.util.spec_from_file_location(
                agent_info.module_path,
                agent_info.file_path,
            )
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the agent class
            agent_class = getattr(module, agent_info.name, None)
            if not agent_class:
                return None

            # Create a basic instance (this might fail for complex agents)
            try:
                # Try creating with minimal config
                if agent_info.architecture == AgentArchitecture.HAIVE_AGENTS_MIXIN:
                    from haive.core.engine.aug_llm import AugLLMConfig

                    agent = agent_class(
                        name=f"viz_{agent_info.name.lower()}",
                        engine=AugLLMConfig(),
                    )
                else:
                    # Try with default constructor
                    agent = agent_class()

                # Generate visualization
                if viz_path is None:
                    timestamp = int(time.time())
                    viz_path = Path(
                        f"{agent_info.name.lower()}_visualization_{timestamp}.png",
                    )

                if hasattr(agent, "compile"):
                    agent.compile()

                if hasattr(agent, "visualize_graph"):
                    agent.visualize_graph(str(viz_path))
                    return viz_path

            except Exception as e:
                logger.warning(
                    f"Failed to create agent instance for visualization: {e}",
                )
                return None

        except Exception as e:
            logger.warning(
                f"Failed to generate visualization for {agent_info.name}: {e}",
            )
            return None

    async def _execute_example_safely(
        self,
        example_path: Path,
        streamer: OutputStreamer,
        config: ExecutionConfig,
    ) -> tuple[bool, str, str | None]:
        """Execute an example with safety measures and output streaming.

        Args:
            example_path: Path to the example file
            streamer: Output streamer
            config: Execution configuration

        Returns:
            Tuple of (success, output, error)
        """
        try:
            # First, try to detect execution pattern by reading the file
            with open(example_path, encoding="utf-8") as f:
                content = f.read()

            # Check if it's async
            is_async = ("asyncio.run" in content or "await " in content
                        or "async def main" in content)

            if is_async:
                return await self._execute_async_example(
                    example_path, streamer, config)
            return await self._execute_sync_example(example_path, streamer,
                                                    config)

        except Exception as e:
            error_msg = f"Execution failed: {e!s}\n{traceback.format_exc()}"
            streamer.add_chunk(f"ERROR: {error_msg}\n")
            return False, streamer.get_output(), error_msg

    async def _execute_async_example(
        self,
        example_path: Path,
        streamer: OutputStreamer,
        config: ExecutionConfig,
    ) -> tuple[bool, str, str | None]:
        """Execute an async example."""
        try:
            # Import and execute the module
            spec = importlib.util.spec_from_file_location(
                "example_module",
                example_path,
            )
            if not spec or not spec.loader:
                raise ImportError(f"Cannot load module from {example_path}")

            module = importlib.util.module_from_spec(spec)

            # Redirect stdout to capture output
            from contextlib import redirect_stdout
            import io

            captured_output = io.StringIO()

            with redirect_stdout(captured_output):
                # Execute the module
                spec.loader.exec_module(module)

                # If module has main function, run it
                if hasattr(module, "main"):
                    if asyncio.iscoroutinefunction(module.main):
                        await asyncio.wait_for(
                            module.main(),
                            timeout=config.timeout_seconds,
                        )
                    else:
                        module.main()

            # Stream the output
            output = captured_output.getvalue()
            for chunk in self._chunk_string(output, config.chunk_size):
                if not streamer.add_chunk(chunk):
                    break

            return True, streamer.get_output(), None

        except TimeoutError:
            error_msg = f"Example execution timed out after {
                config.timeout_seconds} seconds"
            streamer.add_chunk(f"TIMEOUT: {error_msg}\n")
            return False, streamer.get_output(), error_msg

        except Exception as e:
            error_msg = f"Async execution failed: {e!s}"
            streamer.add_chunk(f"ERROR: {error_msg}\n")
            return False, streamer.get_output(), error_msg

    async def _execute_sync_example(
        self,
        example_path: Path,
        streamer: OutputStreamer,
        config: ExecutionConfig,
    ) -> tuple[bool, str, str | None]:
        """Execute a sync example."""
        try:
            import asyncio

            # Run the example as a subprocess with timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                str(example_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=self.project_root,
            )

            # Stream output as it comes
            try:
                while True:
                    line = await asyncio.wait_for(
                        process.stdout.readline(),
                        timeout=config.timeout_seconds,
                    )
                    if not line:
                        break

                    chunk = line.decode("utf-8", errors="replace")
                    if not streamer.add_chunk(chunk):
                        # Output too large, terminate process
                        process.terminate()
                        break

                await process.wait()

                if process.returncode == 0:
                    return True, streamer.get_output(), None
                error_msg = f"Process exited with code {process.returncode}"
                return False, streamer.get_output(), error_msg

            except TimeoutError:
                process.terminate()
                error_msg = f"Process timed out after {config.timeout_seconds} seconds"
                streamer.add_chunk(f"TIMEOUT: {error_msg}\n")
                return False, streamer.get_output(), error_msg

        except Exception as e:
            error_msg = f"Sync execution failed: {e!s}"
            streamer.add_chunk(f"ERROR: {error_msg}\n")
            return False, streamer.get_output(), error_msg

    def _chunk_string(self, text: str, chunk_size: int) -> list[str]:
        """Split string into chunks of specified size.

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk

        Returns:
            List of text chunks
        """
        return [
            text[i:i + chunk_size] for i in range(0, len(text), chunk_size)
        ]

    async def run_multiple_examples(
        self,
        example_paths: list[str | Path],
        config: ExecutionConfig | None = None,
        max_concurrent: int = 3,
    ) -> list[ExecutionResult]:
        """Run multiple examples concurrently.

        Args:
            example_paths: List of example file paths
            config: Execution configuration
            max_concurrent: Maximum concurrent executions

        Returns:
            List of execution results
        """
        if config is None:
            config = ExecutionConfig()

        semaphore = asyncio.Semaphore(max_concurrent)

        async def run_with_semaphore(path):
            async with semaphore:
                return await self.run_example(path, config)

        tasks = [run_with_semaphore(path) for path in example_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def generate_example_report(self, results: list[ExecutionResult]) -> str:
        """Generate a report from multiple execution results.

        Args:
            results: List of execution results

        Returns:
            Formatted report
        """
        successful = sum(1 for result in results if result.success)
        failed = len(results) - successful

        report = [
            "# Example Execution Report",
            "",
            f"**Total Examples**: {len(results)}",
            f"**Successful**: {successful}",
            f"**Failed**: {failed}",
            f"**Success Rate**: {successful / len(results) * 100:.1f}%",
            "",
        ]

        if failed > 0:
            report.append("## Failed Examples")
            for result in results:
                if not result.success:
                    report.append(
                        f"- {result.metadata.get('example_path', 'Unknown')}: {result.error}",
                    )
            report.append("")

        # Execution time statistics
        times = [result.execution_time for result in results if result.success]
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)

            report.append("## Execution Time Statistics")
            report.append(f"- Average: {avg_time:.2f}s")
            report.append(f"- Maximum: {max_time:.2f}s")
            report.append(f"- Minimum: {min_time:.2f}s")
            report.append("")

        # Architecture breakdown
        arch_counts = {}
        for result in results:
            if result.agent_info:
                arch = result.agent_info.architecture.value
                arch_counts[arch] = arch_counts.get(arch, 0) + 1

        if arch_counts:
            report.append("## Architecture Distribution")
            for arch, count in arch_counts.items():
                report.append(f"- {arch}: {count} examples")

        return "\n".join(report)
