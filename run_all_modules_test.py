#!/usr/bin/env python3
"""Test All Module Examples - Record which ones work and which fail.
==============================================================

This script tests all module examples and creates a report of successes/failures.
"""

import asyncio
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path

from tqdm.asyncio import tqdm

from scripts.doc_utils.example_runner import ExecutionConfig, UniversalExampleRunner

# Suppress verbose logging during testing
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class ModuleTestRunner:
    """Test runner for all module examples."""

    def __init__(self):
        self.runner = UniversalExampleRunner()

        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"data/runs/{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results = {
            "timestamp": datetime.now().isoformat(),
            "output_dir": str(self.output_dir),
            "successes": [],
            "failures": [],
            "summary": {},
        }

    def discover_module_examples(self):
        """Discover module examples (simplified version)."""
        modules = {}

        # Agent modules
        agent_base = self.runner.project_root / "packages/haive-agents/src/haive/agents"
        for example_file in agent_base.rglob("example.py"):
            relative_path = example_file.relative_to(agent_base)
            module_path_parts = relative_path.parts[:-1]
            if module_path_parts:
                module_name = "/".join(module_path_parts)
                modules[module_name] = {
                    "type": "agent",
                    "example_file": example_file,
                    "module_dir": example_file.parent,
                }

        # Game modules
        games_base = self.runner.project_root / "packages/haive-games/src/haive/games"
        for example_file in games_base.rglob("example.py"):
            relative_path = example_file.relative_to(games_base)
            module_path_parts = relative_path.parts[:-1]
            if module_path_parts:
                game_name = "/".join(module_path_parts)
                modules[game_name] = {
                    "type": "game",
                    "example_file": example_file,
                    "module_dir": example_file.parent,
                }

        return modules

    async def test_module(self, module_name, module_info, pbar=None):
        """Test a single module with better error capture and organized output."""
        if pbar:
            pbar.set_description(f"Testing {module_name}")

        # Create module-specific output directory
        safe_name = module_name.replace("/", "_").replace(" ", "_")
        module_dir = self.output_dir / safe_name
        module_dir.mkdir(exist_ok=True)

        # Config with visualization and organized output
        viz_path = module_dir / f"{safe_name}_graph.png"
        config = ExecutionConfig(
            timeout_seconds=45,  # 45 seconds max
            enable_visualization=True,  # Enable viz for organized output
            visualization_path=viz_path,
            stream_output=False,  # No output during testing
            save_full_output=True,  # Save outputs to capture errors
            output_file=module_dir / f"{safe_name}_output.txt",
            max_output_size=100000,  # 100KB limit for error capture
        )

        try:
            result = await self.runner.run_example(module_info["example_file"], config)

            if result.success:
                # Save state history if available
                state_file = module_dir / f"{safe_name}_state.json"
                if hasattr(result, "agent_info") and result.agent_info:
                    try:
                        # Try to get state info from agent
                        state_info = {
                            "module": module_name,
                            "execution_time": result.execution_time,
                            "agent_info": (
                                {
                                    "name": result.agent_info.name,
                                    "architecture": result.agent_info.architecture.value,
                                    "has_visualization": result.agent_info.has_visualization,
                                }
                                if result.agent_info
                                else None
                            ),
                            "output_preview": (
                                result.output[:500] if result.output else "No output"
                            ),
                        }
                        with open(state_file, "w") as f:
                            json.dump(state_info, f, indent=2)
                    except Exception as e:
                        logger.warning(f"Could not save state for {module_name}: {e}")

                self.results["successes"].append(
                    {
                        "module": module_name,
                        "type": module_info["type"],
                        "execution_time": result.execution_time,
                        "file": str(
                            module_info["example_file"].relative_to(
                                self.runner.project_root
                            )
                        ),
                        "output_dir": str(module_dir),
                        "has_visualization": viz_path.exists(),
                        "output_preview": (
                            result.output[:200] if result.output else "No output"
                        ),
                    }
                )

                if pbar:
                    pbar.write(f"✅ {module_name} - {result.execution_time:.1f}s")
                return True
            # Capture both error and output for better debugging
            error_info = result.error if result.error else "Unknown error"
            output_info = (
                result.output[-500:] if result.output else "No output"
            )  # Last 500 chars

            # Try to extract meaningful error from output
            if "Error:" in output_info:
                error_lines = [
                    line.strip()
                    for line in output_info.split("\n")
                    if "Error:" in line
                    or "Traceback" in line
                    or "ImportError" in line
                    or "ModuleNotFoundError" in line
                ]
                if error_lines:
                    error_info = error_lines[-1]  # Get last error line

            # Save error info to module directory
            error_file = module_dir / f"{safe_name}_error.txt"
            with open(error_file, "w") as f:
                f.write(f"Module: {module_name}\n")
                f.write(f"Error: {error_info}\n\n")
                f.write(f"Output tail:\n{output_info}\n")

            self.results["failures"].append(
                {
                    "module": module_name,
                    "type": module_info["type"],
                    "error": error_info[:300],
                    "output_tail": output_info[:300],
                    "output_dir": str(module_dir),
                    "file": str(
                        module_info["example_file"].relative_to(
                            self.runner.project_root
                        )
                    ),
                }
            )

            if pbar:
                pbar.write(f"❌ {module_name} - {error_info[:60]}...")
            return False

        except Exception as e:
            import traceback

            error_detail = f"Exception: {e!s}"
            traceback_info = traceback.format_exc()

            # Save exception info to module directory
            exception_file = module_dir / f"{safe_name}_exception.txt"
            with open(exception_file, "w") as f:
                f.write(f"Module: {module_name}\n")
                f.write(f"Exception: {error_detail}\n\n")
                f.write(f"Traceback:\n{traceback_info}\n")

            self.results["failures"].append(
                {
                    "module": module_name,
                    "type": module_info["type"],
                    "error": error_detail[:300],
                    "traceback": traceback_info[:500],
                    "output_dir": str(module_dir),
                    "file": str(
                        module_info["example_file"].relative_to(
                            self.runner.project_root
                        )
                    ),
                }
            )

            if pbar:
                pbar.write(f"❌ {module_name} - Exception: {str(e)[:60]}...")
            return False

    async def test_all_modules(self):
        """Test all modules and generate report."""

        # Discover modules
        modules = self.discover_module_examples()

        # Test each module with progress bar
        total = len(modules)

        # Create progress bar
        pbar = tqdm(total=total, desc="Testing modules", unit="module")

        try:
            for module_name, module_info in modules.items():
                await self.test_module(module_name, module_info, pbar)
                pbar.update(1)
        finally:
            pbar.close()

        # Generate summary
        success_count = len(self.results["successes"])
        failure_count = len(self.results["failures"])

        self.results["summary"] = {
            "total_modules": total,
            "successful": success_count,
            "failed": failure_count,
            "success_rate": (
                f"{success_count / total * 100:.1f}%" if total > 0 else "0%"
            ),
        }

        # Show summary

        # Show working modules by type
        agent_successes = [s for s in self.results["successes"] if s["type"] == "agent"]
        game_successes = [s for s in self.results["successes"] if s["type"] == "game"]

        if agent_successes:
            for success in sorted(agent_successes, key=lambda x: x["module"]):
                pass")

        if game_successes:
            for success in sorted(game_successes, key=lambda x: x["module"]):
                pass")

        # Show failed modules
        agent_failures = [f for f in self.results["failures"] if f["type"] == "agent"]
        game_failures = [f for f in self.results["failures"] if f["type"] == "game"]

        if agent_failures:
            for failure in sorted(agent_failures, key=lambda x: x["module"]):
                if "output_tail" in failure and failure["output_tail"] != "No output":
                    # Extract key error info from output
                    output = failure["output_tail"]
                    if "ImportError:" in output:
                        import_error = [
                            line.strip()
                            for line in output.split("\n")
                            if "ImportError:" in line
                        ]
                        if import_error:
                            pass
                    elif "ModuleNotFoundError:" in output:
                        module_error = [
                            line.strip()
                            for line in output.split("\n")
                            if "ModuleNotFoundError:" in line
                        ]
                        if module_error:
                            pass

        if game_failures:
            for failure in sorted(game_failures, key=lambda x: x["module"]):
                if "output_tail" in failure and failure["output_tail"] != "No output":
                    output = failure["output_tail"]
                    if "ImportError:" in output:
                        import_error = [
                            line.strip()
                            for line in output.split("\n")
                            if "ImportError:" in line
                        ]
                        if import_error:
                            pass
                    elif "ModuleNotFoundError:" in output:
                        module_error = [
                            line.strip()
                            for line in output.split("\n")
                            if "ModuleNotFoundError:" in line
                        ]
                        if module_error:
                            pass

        # Save detailed report to output directory
        report_file = self.output_dir / "test_report.json"
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Create summary README
        readme_file = self.output_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write("# Module Test Results\n\n")
            f.write(f"**Generated**: {self.results['timestamp']}\n")
            f.write(f"**Total Modules**: {total}\n")
            f.write(f"**Successful**: {success_count}\n")
            f.write(f"**Failed**: {failure_count}\n")
            f.write(f"**Success Rate**: {self.results['summary']['success_rate']}\n\n")

            f.write("## Directory Structure\n\n")
            f.write("Each module has its own directory containing:\n")
            f.write(
                f"- `{'{module}'}_graph.png` - Agent workflow visualization (if successful)\n"
            )
            f.write(
                f"- `{'{module}'}_state.json` - Agent state and execution info (if successful)\n"
            )
            f.write(f"- `{'{module}'}_output.txt` - Full execution output\n")
            f.write(f"- `{'{module}'}_error.txt` - Error details (if failed)\n")
            f.write(
                f"- `{'{module}'}_exception.txt` - Exception traceback (if crashed)\n\n"
            )

            if agent_successes:
                f.write(f"## ✅ Working Agent Modules ({len(agent_successes)})\n\n")
                for success in sorted(agent_successes, key=lambda x: x["module"]):
                    viz_icon = "🎨" if success.get("has_visualization") else ""
                    f.write(
                        f"- {viz_icon} **{success['module']}** ({success['execution_time']:.1f}s)\n"
                    )
                f.write("\n")

            if game_successes:
                f.write(f"## 🎮 Working Game Modules ({len(game_successes)})\n\n")
                for success in sorted(game_successes, key=lambda x: x["module"]):
                    viz_icon = "🎨" if success.get("has_visualization") else ""
                    f.write(
                        f"- {viz_icon} **{success['module']}** ({success['execution_time']:.1f}s)\n"
                    )
                f.write("\n")


        return self.results


async def main():
    """Main execution."""
    runner = ModuleTestRunner()
    await runner.test_all_modules()


if __name__ == "__main__":
    asyncio.run(main())
