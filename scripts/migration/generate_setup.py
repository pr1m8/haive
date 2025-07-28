#!/usr/bin/env python3
# Generate setup.py from pyproject.toml

from pathlib import Path
import re
import sys

import toml


def generate_setup_py(pyproject_path):
    """Generate setup.py from pyproject.toml."""
    try:
        with open(pyproject_path) as f:
            config = toml.load(f)
    except Exception:
        return False

    # Extract information from pyproject.toml
    package_info = config.get("tool", {}).get("poetry", {})
    name = package_info.get("name", "unknown")
    version = package_info.get("version", "0.1.0")
    description = package_info.get("description", "")
    authors = package_info.get("authors", [])
    author = authors[0].split("<")[0].strip() if authors else ""
    author_email = (
        authors[0].split("<")[1].split(">")[0].strip()
        if authors and "<" in authors[0]
        else ""
    )

    # Extract dependencies
    dependencies = {}
    for dep_name, dep_version in package_info.get("dependencies", {}).items():
        if dep_name != "python" and not isinstance(dep_version, dict):
            # Convert ^1.2.3 to >=1.2.3,<2.0.0
            if isinstance(dep_version, str) and dep_version.startswith("^"):
                major, minor, patch = re.match(
                    r"\^(\d+)\.(\d+)\.(\d+)", dep_version
                ).groups()
                dependencies[dep_name] = (
                    f">={major}.{minor}.{patch},<{int(major) + 1}.0.0"
                )
            else:
                dependencies[dep_name] = dep_version

    # Check for system requirements
    system_reqs = []
    sys_req_path = Path(pyproject_path).parent / "system_requirements.txt"
    if sys_req_path.exists():
        with open(sys_req_path) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    system_reqs.append(line.strip())

    # Generate setup.py
    output_path = Path(pyproject_path).parent / "setup.py"

    with open(output_path, "w") as f:
        f.write(
            f"""from setuptools import setup, find_packages

setup(
    name="{name}",
    version="{version}",
    description="{description}",
    author="{author}",
    author_email="{author_email}",
    package_dir={{"": "src"}},
    packages=find_packages(where="src"),
    python_requires=">=3.12,<3.13",
    install_requires=[
"""
        )
        for dep_name, dep_version in dependencies.items():
            f.write(f'        "{dep_name}{dep_version}",\n')
        f.write(
            """    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
"""
        )
        if system_reqs:
            f.write(
                """    setup_requires=[
        "setuptools>=42",
        "wheel"
    ],
"""
            )
        f.write(
            """    include_package_data=True,
)
"""
        )

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    generate_setup_py(sys.argv[1])
