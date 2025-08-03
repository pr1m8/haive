#!/usr/bin/env python3
"""
Build Performance Test Suite
Benchmarks documentation build performance and identifies bottlenecks.
"""

import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path

import psutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class BuildPerformanceTester:
    """Test documentation build performance and identify bottlenecks."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.source_dir = docs_dir / "source"
        self.build_dir = docs_dir / "build"

        self.results = {
            "build_times": {},
            "memory_usage": {},
            "file_counts": {},
            "bottlenecks": [],
            "recommendations": [],
        }

    def test_all(self):
        """Run all build performance tests."""
        print("⚡ Build Performance Test Suite\n")

        self.analyze_source_structure()
        self.test_clean_build()
        self.test_incremental_build()
        self.test_api_generation()
        self.test_different_builders()
        self.identify_bottlenecks()

        self.print_report()

    def analyze_source_structure(self):
        """Analyze source structure impact on build performance."""
        print("1️⃣ Analyzing source structure...")

        # Count different file types
        file_counts = defaultdict(int)
        total_size = 0

        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                file_counts[suffix] += 1
                total_size += file_path.stat().st_size

        self.results["file_counts"] = dict(file_counts)
        self.results["total_size_mb"] = round(total_size / (1024 * 1024), 2)

        print(f"   📄 RST files: {file_counts.get('.rst', 0)}")
        print(f"   🎨 CSS files: {file_counts.get('.css', 0)}")
        print(
            f"   📸 Image files: {file_counts.get('.png', 0) + file_counts.get('.jpg', 0)}"
        )
        print(f"   📦 Archive files: {file_counts.get('.zip', 0)}")
        print(f"   📊 Total size: {self.results['total_size_mb']} MB")

        # Check for performance-impacting patterns
        if file_counts.get(".zip", 0) > 50:
            self.results["bottlenecks"].append(
                {
                    "type": "excessive_archives",
                    "count": file_counts[".zip"],
                    "impact": "high",
                    "description": "Large number of ZIP files may slow builds",
                }
            )

        if file_counts.get(".css", 0) > 30:
            self.results["bottlenecks"].append(
                {
                    "type": "css_fragmentation",
                    "count": file_counts[".css"],
                    "impact": "medium",
                    "description": "Many CSS files increase processing time",
                }
            )

    def test_clean_build(self):
        """Test clean build performance."""
        print("\n2️⃣ Testing clean build performance...")

        # Clean build directory
        if self.build_dir.exists():
            import shutil

            shutil.rmtree(self.build_dir)

        # Test different build configurations
        build_configs = [
            ("full_build", []),
            ("no_autoapi", ["-D", "autoapi_generate_api_docs=0"]),
            (
                "minimal",
                [
                    "-D",
                    "autoapi_generate_api_docs=0",
                    "-D",
                    "autodoc_generate_api_docs=0",
                ],
            ),
        ]

        for config_name, extra_args in build_configs:
            print(f"   🔨 Testing {config_name}...")

            build_time, memory_peak = self.run_build_with_monitoring(extra_args)

            self.results["build_times"][config_name] = {
                "time_seconds": build_time,
                "memory_peak_mb": memory_peak,
                "extra_args": extra_args,
            }

            print(f"      ⏱️  Time: {build_time:.1f}s, Memory: {memory_peak:.1f}MB")

    def test_incremental_build(self):
        """Test incremental build performance."""
        print("\n3️⃣ Testing incremental build performance...")

        # Ensure we have a built version
        if not (self.build_dir / "html" / "index.html").exists():
            print("   Building initial version for incremental test...")
            self.run_build_with_monitoring([])

        # Test incremental builds
        incremental_tests = [
            ("no_changes", lambda: None),
            ("rst_change", self.modify_rst_file),
            ("css_change", self.modify_css_file),
            ("config_change", self.modify_config_file),
        ]

        for test_name, modification_func in incremental_tests:
            print(f"   📝 Testing {test_name}...")

            # Apply modification
            modification_func()

            # Measure incremental build
            build_time, memory_peak = self.run_build_with_monitoring([])

            self.results["build_times"][f"incremental_{test_name}"] = {
                "time_seconds": build_time,
                "memory_peak_mb": memory_peak,
            }

            print(f"      ⏱️  Time: {build_time:.1f}s, Memory: {memory_peak:.1f}MB")

    def test_api_generation(self):
        """Test API generation performance impact."""
        print("\n4️⃣ Testing API generation impact...")

        # Count potential API files
        api_file_count = 0
        for packages_dir in [project_root / "packages"]:
            if packages_dir.exists():
                py_files = list(packages_dir.rglob("*.py"))
                api_file_count += len(py_files)

        print(f"   📦 Python files for API generation: {api_file_count}")

        if api_file_count > 0:
            # Test with and without API generation
            with_api_time, with_api_memory = self.run_build_with_monitoring([])
            without_api_time, without_api_memory = self.run_build_with_monitoring(
                ["-D", "autoapi_generate_api_docs=0"]
            )

            api_overhead = with_api_time - without_api_time
            memory_overhead = with_api_memory - without_api_memory

            self.results["api_generation"] = {
                "files_processed": api_file_count,
                "time_overhead": api_overhead,
                "memory_overhead": memory_overhead,
                "overhead_per_file": (
                    api_overhead / api_file_count if api_file_count > 0 else 0
                ),
            }

            print(
                f"   ⏱️  API generation overhead: {api_overhead:.1f}s ({api_overhead/with_api_time*100:.1f}%)"
            )
            print(f"   🧠 Memory overhead: {memory_overhead:.1f}MB")

    def test_different_builders(self):
        """Test different Sphinx builders."""
        print("\n5️⃣ Testing different builders...")

        builders = ["html", "dirhtml", "singlehtml"]

        for builder in builders:
            print(f"   🏗️  Testing {builder} builder...")

            try:
                build_time, memory_peak = self.run_build_with_monitoring(
                    ["-b", builder]
                )

                self.results["build_times"][f"builder_{builder}"] = {
                    "time_seconds": build_time,
                    "memory_peak_mb": memory_peak,
                }

                print(f"      ⏱️  Time: {build_time:.1f}s, Memory: {memory_peak:.1f}MB")

            except Exception as e:
                print(f"      ❌ Failed: {e}")

    def identify_bottlenecks(self):
        """Identify performance bottlenecks."""
        print("\n6️⃣ Identifying bottlenecks...")

        build_times = self.results["build_times"]

        # Identify slowest operations
        if "full_build" in build_times and "no_autoapi" in build_times:
            full_time = build_times["full_build"]["time_seconds"]
            no_api_time = build_times["no_autoapi"]["time_seconds"]

            if full_time > no_api_time * 2:
                self.results["bottlenecks"].append(
                    {
                        "type": "autoapi_slowdown",
                        "impact": "high",
                        "full_time": full_time,
                        "no_api_time": no_api_time,
                        "description": "AutoAPI generation is a major bottleneck",
                    }
                )

        # Check memory usage
        memory_usage = [build["memory_peak_mb"] for build in build_times.values()]
        if memory_usage and max(memory_usage) > 1000:  # More than 1GB
            self.results["bottlenecks"].append(
                {
                    "type": "high_memory_usage",
                    "impact": "medium",
                    "peak_memory": max(memory_usage),
                    "description": "Build requires significant memory",
                }
            )

        # Check for slow incremental builds
        incremental_times = [
            build["time_seconds"]
            for name, build in build_times.items()
            if name.startswith("incremental_")
        ]

        if incremental_times and max(incremental_times) > 30:  # More than 30 seconds
            self.results["bottlenecks"].append(
                {
                    "type": "slow_incremental_builds",
                    "impact": "medium",
                    "max_incremental_time": max(incremental_times),
                    "description": "Incremental builds are slower than expected",
                }
            )

    @contextmanager
    def monitor_process(self):
        """Monitor build process resource usage."""
        process = psutil.Process()
        start_time = time.time()
        peak_memory = 0

        try:
            yield
        finally:
            end_time = time.time()
            try:
                current_memory = process.memory_info().rss / (1024 * 1024)  # MB
                peak_memory = max(peak_memory, current_memory)
            except:
                pass

        return end_time - start_time, peak_memory

    def run_build_with_monitoring(self, extra_args):
        """Run Sphinx build with resource monitoring."""
        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(self.source_dir),
            str(self.build_dir / "html"),
            "-q",  # Quiet mode for performance
        ] + extra_args

        start_time = time.time()
        start_memory = psutil.virtual_memory().used / (1024 * 1024)

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=project_root
            )

            if result.returncode != 0:
                print(f"      ⚠️  Build warning/error: {result.stderr[:200]}...")

        except Exception as e:
            print(f"      ❌ Build failed: {e}")
            return 999.0, 0.0  # Return high time to indicate failure

        end_time = time.time()
        end_memory = psutil.virtual_memory().used / (1024 * 1024)

        build_time = end_time - start_time
        memory_delta = end_memory - start_memory

        return build_time, max(0, memory_delta)

    def modify_rst_file(self):
        """Modify an RST file for incremental build testing."""
        index_file = self.source_dir / "index.rst"
        if index_file.exists():
            with open(index_file, "a") as f:
                f.write(f"\n.. comment:: Test modification {time.time()}")

    def modify_css_file(self):
        """Modify a CSS file for incremental build testing."""
        css_files = list(self.source_dir.rglob("*.css"))
        if css_files:
            css_file = css_files[0]
            with open(css_file, "a") as f:
                f.write(f"\n/* Test modification {time.time()} */")

    def modify_config_file(self):
        """Modify config for incremental build testing."""
        # This is a no-op for now to avoid breaking builds
        pass

    def print_report(self):
        """Print comprehensive build performance report."""
        print("\n" + "=" * 60)
        print("📊 BUILD PERFORMANCE REPORT")
        print("=" * 60)

        # File structure impact
        print(f"\n📁 SOURCE STRUCTURE:")
        print(f"   Total files: {sum(self.results['file_counts'].values())}")
        print(f"   Total size: {self.results['total_size_mb']} MB")

        for file_type, count in sorted(self.results["file_counts"].items()):
            if count > 0:
                print(f"   {file_type}: {count}")

        # Build time analysis
        if self.results["build_times"]:
            print(f"\n⏱️  BUILD TIMES:")

            sorted_builds = sorted(
                self.results["build_times"].items(), key=lambda x: x[1]["time_seconds"]
            )

            for build_name, build_data in sorted_builds:
                time_s = build_data["time_seconds"]
                memory_mb = build_data["memory_peak_mb"]
                print(f"   {build_name}: {time_s:.1f}s, {memory_mb:.1f}MB")

        # API generation impact
        if "api_generation" in self.results:
            api_data = self.results["api_generation"]
            print(f"\n🔧 API GENERATION IMPACT:")
            print(f"   Files processed: {api_data['files_processed']}")
            print(f"   Time overhead: {api_data['time_overhead']:.1f}s")
            print(f"   Time per file: {api_data['overhead_per_file']:.3f}s")
            print(f"   Memory overhead: {api_data['memory_overhead']:.1f}MB")

        # Bottlenecks
        if self.results["bottlenecks"]:
            print(f"\n🚫 BOTTLENECKS IDENTIFIED:")

            for bottleneck in self.results["bottlenecks"]:
                impact_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                emoji = impact_emoji.get(bottleneck["impact"], "⚪")

                print(
                    f"\n   {emoji} {bottleneck['type']} ({bottleneck['impact']} impact)"
                )
                print(f"      {bottleneck['description']}")

                # Add specific metrics
                if "count" in bottleneck:
                    print(f"      Count: {bottleneck['count']}")
                if "full_time" in bottleneck:
                    print(f"      Full build: {bottleneck['full_time']:.1f}s")
                    print(f"      Without API: {bottleneck['no_api_time']:.1f}s")

        # Performance recommendations
        print(f"\n💡 PERFORMANCE RECOMMENDATIONS:")

        # Base recommendations on findings
        if any(b["type"] == "excessive_archives" for b in self.results["bottlenecks"]):
            print("   1. 🗂️  Remove or archive ZIP files from source directory")

        if any(b["type"] == "autoapi_slowdown" for b in self.results["bottlenecks"]):
            print("   2. 🔧 Consider selective API generation or caching")

        if any(b["type"] == "css_fragmentation" for b in self.results["bottlenecks"]):
            print("   3. 🎨 Consolidate CSS files to reduce processing overhead")

        if any(b["type"] == "high_memory_usage" for b in self.results["bottlenecks"]):
            print("   4. 🧠 Consider build environment with more memory")

        if self.results["file_counts"].get(".rst", 0) > 100:
            print("   5. 📝 Consider breaking large RST files into smaller modules")

        # Build optimization suggestions
        build_times = self.results["build_times"]
        if (
            "full_build" in build_times
            and build_times["full_build"]["time_seconds"] > 60
        ):
            print("   6. ⚡ Use parallel builds: sphinx-build -j auto")
            print("   7. 🚀 Enable incremental builds for development")

        # Memory optimization
        memory_values = [b["memory_peak_mb"] for b in build_times.values()]
        if memory_values and max(memory_values) > 500:
            print("   8. 💾 Consider memory-efficient build configurations")

        # Summary statistics
        if build_times:
            fastest = min(build_times.values(), key=lambda x: x["time_seconds"])
            slowest = max(build_times.values(), key=lambda x: x["time_seconds"])

            print(f"\n📈 SUMMARY:")
            print(f"   Fastest build: {fastest['time_seconds']:.1f}s")
            print(f"   Slowest build: {slowest['time_seconds']:.1f}s")
            print(
                f"   Speed difference: {slowest['time_seconds']/fastest['time_seconds']:.1f}x"
            )


def main():
    """Run build performance tests."""
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        return 1

    tester = BuildPerformanceTester(docs_dir)
    tester.test_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
