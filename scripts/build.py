from build_utils import check_system_requirements
import subprocess
import sys

def check_meson():
    try:
        subprocess.run(['meson', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: meson build system is not installed.")
        print("Please install meson using one of the following commands:")
        print("  - pip install meson")
        print("  - brew install meson  (on macOS)")
        sys.exit(1)

def build():
    check_system_requirements()
    check_meson()
    # The actual build will be handled by poetry and setuptools

if __name__ == "__main__":
    build() 