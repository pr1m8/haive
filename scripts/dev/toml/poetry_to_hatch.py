from __future__ import annotations

import tomlkit


def migrate_poetry_to_hatch(pyproject_path="pyproject.toml"):
    with open(pyproject_path) as f:
        config = tomlkit.parse(f.read())

    # Add Hatch build system
    config["build-system"] = {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }

    # Create Hatch environments from Poetry groups
    hatch_envs = {}

    if "tool" in config and "poetry" in config["tool"]:
        poetry_groups = config["tool"]["poetry"].get("group", {})

        for group_name, group_config in poetry_groups.items():
            if "dependencies" in group_config:
                deps = []
                for dep, version in group_config["dependencies"].items():
                    if isinstance(version, str):
                        deps.append(f"{dep}{version}")
                    elif isinstance(version, dict):
                        deps.append(f"{dep}>={version.get('version', '')}")

                hatch_envs[group_name] = {"dependencies": deps}

    # Add Hatch configuration
    if "tool" not in config:
        config["tool"] = {}
    config["tool"]["hatch"] = {"envs": hatch_envs}

    # Write back
    with open(pyproject_path, "w") as f:
        f.write(tomlkit.dumps(config))


# Usage
migrate_poetry_to_hatch()
