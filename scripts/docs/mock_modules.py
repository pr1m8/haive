#!/usr/bin/env python3
"""
Script to create mock modules for documentation.
Place in docs/scripts/mock_modules.py
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set

def create_mock_module(module_path: Path, content: str = "") -> None:
    """Create a mock module file."""
    module_path.parent.mkdir(parents=True, exist_ok=True)
    if not module_path.exists():
        module_path.write_text(content or '"""Mock module for documentation."""\n')

def create_mock_structure():
    """Create mock module structure."""
    DOCS_DIR = Path("docs")
    MOCKS_DIR = DOCS_DIR / "_mocks" / "haive"
    
    # Base structure
    modules = {
        "agents": {
            "base.py": """
from typing import Any, Dict
class AgentArchitecture:
    \"\"\"Base class for all agents.\"\"\"
    pass

class AgentArchitectureConfig:
    \"\"\"Configuration for agents.\"\"\"
    pass
""",
            "__init__.py": "",
            "react_agent": {"__init__.py": "", "agent.py": "", "state.py": ""},
            "plan_and_execute": {"__init__.py": "", "agent.py": "", "state.py": ""},
            "tot": {"__init__.py": "", "agent.py": "", "state.py": ""},
            "self_discover": {"__init__.py": "", "agent.py": "", "state.py": ""},
        },
        "core": {
            "__init__.py": "",
            "aug_llm": {"__init__.py": "", "base.py": ""},
            "models": {"__init__.py": "", "llm": {"__init__.py": "", "base.py": ""}},
        },
        "flstaesr": {
            "__init__.py": "",
            "transform": {"__init__.py": "", "base.py": ""},
            "annotate": {"__init__.py": "", "base.py": ""},
        },
    }

    def create_module_structure(base_path: Path, structure: Dict):
        for name, content in structure.items():
            path = base_path / name
            if isinstance(content, dict):
                path.mkdir(parents=True, exist_ok=True)
                create_module_structure(path, content)
            else:
                create_mock_module(path, content)

    # Create mock structure
    create_module_structure(MOCKS_DIR, modules)
    
    # Add to Python path
    sys.path.insert(0, str(DOCS_DIR / "_mocks"))

if __name__ == "__main__":
    create_mock_structure()