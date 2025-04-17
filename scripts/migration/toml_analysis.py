import toml
from pathlib import Path

# Locate the root pyproject.toml
pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
pyproject = toml.load(pyproject_path)

poetry = pyproject.get("tool", {}).get("poetry", {})

top_level_deps = poetry.get("dependencies", {})
group_deps = poetry.get("group", {})
extras = poetry.get("extras", {})
sources = poetry.get("source", [])

import toml
from pathlib import Path

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

print("\n🧱 [tool.poetry.dependencies]")
for dep, version in top_level_deps.items():
    if dep.lower() != "python":
        print(f"  - {dep}: {version}")
        top_level_count += 1

print("\n📦 [tool.poetry.group.<name>.dependencies]")
for group_name, group in group_deps.items():
    deps = group.get("dependencies", {})
    print(f"\n  🔸 {group_name}")
    for dep, version in deps.items():
        print(f"    - {dep}: {version}")
        group_dep_set.add(dep)

print("\n🧩 [tool.poetry.extras]")
for extra, deps in extras.items():
    print(f"  - {extra}: {deps}")

print("\n🌐 [[tool.poetry.source]]")
for src in sources:
    name = src.get("name")
    url = src.get("url")
    priority = src.get("priority")
    print(f"  - {name} → {url} (priority: {priority})")

# Summary
print("\n📊 Summary")
print(f"🔹 Total top-level dependencies: {top_level_count}")
print(f"🔸 Total unique group dependencies: {len(group_dep_set)}")
print(f"🧩 Total extras defined: {len(extras)}")
print(f"🌐 Total sources listed: {len(sources)}")

# Optional: compare overlap
overlap = set(top_level_deps.keys()) & group_dep_set
overlap.discard("python")
if overlap:
    print(f"⚠️ Overlapping deps (in both top-level and groups): {sorted(overlap)}")

print("\n🧱 [tool.poetry.dependencies]")
for dep, version in poetry.get("dependencies", {}).items():
    if dep != "python":
        print(f"  - {dep}: {version}")

print("\n📦 [tool.poetry.group.<name>.dependencies]")
for group_name, group in poetry.get("group", {}).items():
    deps = group.get("dependencies", {})
    print(f"\n  🔸 {group_name}")
    for dep, version in deps.items():
        print(f"    - {dep}: {version}")

print("\n🧩 [tool.poetry.extras]")
for extra, deps in poetry.get("extras", {}).items():
    print(f"  - {extra}: {deps}")

print("\n🌐 [[tool.poetry.source]]")
sources = poetry.get("source", [])
for src in sources:
    name = src.get("name")
    url = src.get("url")
    priority = src.get("priority")
    print(f"  - {name} → {url} (priority: {priority})")
