from pathlib import Path

import toml

# Locate the root pyproject.toml
pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
pyproject = toml.load(pyproject_path)

poetry = pyproject.get("tool", {}).get("poetry", {})

top_level_deps = poetry.get("dependencies", {})
group_deps = poetry.get("group", {})
extras = poetry.get("extras", {})
sources = poetry.get("source", [])

from pathlib import Path

import toml

# Locate the root pyproject.toml
pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
pyproject = toml.load(pyproject_path)
poetry = pyproject.get("tool", {}).get("poetry", {})

top_level_deps = poetry.get("dependencies", {})
group_deps = poetry.get("group", {})
extras = poetry.get("extras", {})
sources = poetry.get("source", [])

# Track counts
top_level_count = 0
group_dep_set = set()

for dep, version in top_level_deps.items():
    if dep.lower() != "python":
        top_level_count += 1

for group_name, group in group_deps.items():
    deps = group.get("dependencies", {})
    for dep, version in deps.items():
        group_dep_set.add(dep)

for extra, deps in extras.items():
    pass

for src in sources:
    name = src.get("name")
    url = src.get("url")
    priority = src.get("priority")

# Summary

# Optional: compare overlap
overlap = set(top_level_deps.keys()) & group_dep_set
overlap.discard("python")
if overlap:
    pass
for dep, version in poetry.get("dependencies", {}).items():
    if dep != "python":
        pass

for group_name, group in poetry.get("group", {}).items():
    deps = group.get("dependencies", {})
    for dep, version in deps.items():
        pass

for extra, deps in poetry.get("extras", {}).items():
    pass

sources = poetry.get("source", [])
for src in sources:
    name = src.get("name")
    url = src.get("url")
    priority = src.get("priority")
