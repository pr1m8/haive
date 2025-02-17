import importlib
import pkgutil
import os
import sys
import subprocess
from pathlib import Path

# Import paths dynamically from haive's settings
try:
    from haive.config.settings import AGENTS_DIR
except ImportError:
    print("Error: Could not import settings from haive.config. Ensure `haive` is in your PYTHONPATH.")
    sys.exit(1)

# Ensure `agents/` exists
Path(AGENTS_DIR).mkdir(parents=True, exist_ok=True)

def load_agents():
    """Dynamically discover and import all agent modules."""
    agents = {}

    if not os.path.exists(AGENTS_DIR):
        print(f"Warning: Agents directory {AGENTS_DIR} does not exist.")
        return agents

    for _, module_name, is_pkg in pkgutil.iter_modules([AGENTS_DIR]):
        if is_pkg:  # Ensure we are only importing sub-packages
            module_path = f"haive.agents.{module_name}"
            try:
                module = importlib.import_module(module_path)
                agents[module_name] = module
                print(f"✅ Loaded agent: {module_name}")
            except Exception as e:
                print(f"⚠️ Error loading {module_name}: {e}")

    return agents

def install_agent(repo_url: str):
    """Clones and installs an agent submodule dynamically into `agents/`."""
    if not repo_url.startswith("http"):
        print("⚠️ Error: Invalid repository URL. Must start with 'http' or 'https'.")
        return

    agent_name = repo_url.split("/")[-1].replace(".git", "")
    agent_path = os.path.join(AGENTS_DIR, agent_name)

    if os.path.exists(agent_path):
        print(f"⚠️ Agent {agent_name} already exists at {agent_path}.")
        return

    print(f"🔄 Cloning {repo_url} into {agent_path}...")
    try:
        subprocess.run(["git", "clone", repo_url, agent_path], check=True)
        print(f"✅ Successfully installed agent: {agent_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install agent {agent_name}: {e}")

def remove_agent(agent_name: str):
    """Removes an installed agent from `agents/`."""
    agent_path = os.path.join(AGENTS_DIR, agent_name)

    if not os.path.exists(agent_path):
        print(f"⚠️ Agent {agent_name} does not exist at {agent_path}.")
        return

    print(f"🗑 Removing agent: {agent_name}...")
    try:
        subprocess.run(["rm", "-rf", agent_path], check=True)
        print(f"✅ Successfully removed agent: {agent_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to remove agent {agent_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "load":
            loaded_agents = load_agents()
            print(f"📜 Available agents: {list(loaded_agents.keys())}")

        elif command == "install":
            if len(sys.argv) > 2:
                install_agent(sys.argv[2])
            else:
                print("Usage: python cli.py install <repo_url>")

        elif command == "remove":
            if len(sys.argv) > 2:
                remove_agent(sys.argv[2])
            else:
                print("Usage: python cli.py remove <agent_name>")

        else:
            print("⚠️ Unknown command. Usage: python cli.py [load|install <repo_url>|remove <agent_name>]")
    else:
        print("Usage: python cli.py [load|install <repo_url>|remove <agent_name>]")
