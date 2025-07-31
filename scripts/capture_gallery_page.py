"""Quick script to capture the gallery page for visualization testing."""

import os
import subprocess
import time

# Use gnome-screenshot to capture the page

time.sleep(5)

# Create screenshots directory
os.makedirs("docs/screenshots", exist_ok=True)

# Take screenshot
subprocess.run(
    [
        "gnome-screenshot",
        "-f",
        "docs/screenshots/gallery_page_current.png",
        "-w",  # Window capture
    ],
    check=False,
)
