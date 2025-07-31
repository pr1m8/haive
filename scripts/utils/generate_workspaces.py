import json
from pathlib import Path

# === Config ===
ROOT = Path("/home/will/Projects/haive/backend/haive")
WORKSPACE_DIR = ROOT / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# Dependency graph
DEPS = {
    "haive-core": [],
    "haive-tools": ["haive-core"],
    "haive-agents": ["haive-core", "haive-tools"],
    "haive-games": ["haive-core", "haive-agents"],
    "haive-prebuilt": ["haive-core", "haive-agents", "haive-tools"],
    "haive-dataflow": [
        "haive-core",
        "haive-agents",
        "haive-games",
        "haive-prebuilt",
        "haive-tools",
    ],
}


def generate_workspace(name, dependencies):
    # Compose list of folder paths relative to ROOT
    folders = [{"name": "root", "path": "."}]
    all_names = list(dict.fromkeys([*dependencies, name]))  # dedupe, preserve order
    folders += [{"name": n, "path": f"./packages/{n}"} for n in all_names]

    # Shared settings
    settings = {
        "python.defaultInterpreterPath": "${workspaceFolder:root}/.venv/bin/python",
        "python.analysis.extraPaths": [
            f"${{workspaceFolder:{n}}}/src" for n in all_names
        ],
        "python.envFile": "${workspaceFolder:root}/.env",
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["packages/"],
        "editor.formatOnSave": True,
        "python.analysis.typeCheckingMode": "basic",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "terminal.integrated.cwd": "${workspaceFolder:root}",
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/*.pyo": True,
            "**/.mypy_cache": True,
            "**/.pytest_cache": True,
        },
    }

    workspace_data = {
        "folders": folders,
        "settings": settings,
        "launch": {"configurations": [], "compounds": []},
        "extensions": {
            "recommendations": ["ms-python.python", "ms-python.vscode-pylance"]
        },
    }

    out_file = WORKSPACE_DIR / f"{name}.code-workspace"
    out_file.write_text(json.dumps(workspace_data, indent=2))


def main():
    for name, deps in DEPS.items():
        generate_workspace(name, deps)


if __name__ == "__main__":
    main()
