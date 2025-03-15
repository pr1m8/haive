import subprocess
import sys
import os
from pathlib import Path

def check_system_requirements():
    requirements = {
        'git': 'git --version',
        'meson': 'meson --version',
        'cmake': 'cmake --version'
    }
    
    missing = []
    for req, cmd in requirements.items():
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(req)
    
    if missing:
        print(f"Missing required system dependencies: {', '.join(missing)}")
        print("\nPlease install the missing dependencies:")
        print("On macOS:")
        print("    brew install " + " ".join(missing))
        print("On Ubuntu/Debian:")
        print("    sudo apt-get install " + " ".join(missing))
        sys.exit(1) 