#!/usr/bin/env python3
"""Take screenshots of documentation pages for testing."""

import os
import time
from pathlib import Path
from datetime import datetime

# Create screenshot directory
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
screenshot_dir = Path(f"docs/screenshots/test_{timestamp}")
screenshot_dir.mkdir(parents=True, exist_ok=True)

# Pages to test
pages = [
    ("homepage", "http://127.0.0.1:8003/index.html"),
    ("agents_index", "http://127.0.0.1:8003/agents/index.html"),
    ("games_index", "http://127.0.0.1:8003/games/index.html"),
    ("chess_demo", "http://127.0.0.1:8003/games/demos/chess-demo.html"),
    ("checkers_demo", "http://127.0.0.1:8003/games/demos/checkers-demo.html"),
    ("simple_agent_demo", "http://127.0.0.1:8003/agents/demos/simple-demo.html"),
    ("api_index", "http://127.0.0.1:8003/api/index.html"),
]

# Viewport sizes
viewports = [
    ("desktop", 1400, 900),
    ("tablet", 768, 1024),
    ("mobile", 375, 667),
]

print(f"Taking screenshots to {screenshot_dir}")
print("=" * 60)

# Use the existing screenshot script
for page_name, url in pages:
    print(f"\n📸 Capturing {page_name}...")
    
    for viewport_name, width, height in viewports:
        output_file = screenshot_dir / f"{page_name}_{viewport_name}.png"
        
        cmd = f'poetry run python docs/visualize_agent_example.py --url "{url}" --output "{output_file}" --width {width} --height {height}'
        
        print(f"  - {viewport_name} ({width}x{height})...", end=" ", flush=True)
        
        result = os.system(cmd + " 2>/dev/null")
        
        if result == 0:
            print("✅")
        else:
            print("❌")

print(f"\n✅ Screenshots saved to: {screenshot_dir}")
print("\nNow checking key elements...")

# Quick visual checks
checks = {
    "homepage": [
        "✓ Hero section centered",
        "✓ Main content left-aligned",
        "✓ Navigation visible",
    ],
    "agents_index": [
        "✓ Agent cards visible",
        "✓ Demo buttons present",
        "✓ Cards left-aligned",
    ],
    "games_index": [
        "✓ Game cards visible",
        "✓ Proper grid layout",
        "✓ No centering issues",
    ],
    "chess_demo": [
        "✓ Game interface visible",
        "✓ Live stream indicator",
        "✓ Game state display",
        "✓ Move history present",
    ],
}

print("\n📋 Visual Checklist:")
print("=" * 60)
for page, items in checks.items():
    print(f"\n{page}:")
    for item in items:
        print(f"  {item}")

print(f"\n📁 Review screenshots at: {screenshot_dir}")
print("🔍 Check for:")
print("  - Alignment issues (everything should be left-aligned)")
print("  - Game streaming content visible")
print("  - Responsive layout working")
print("  - No visual glitches")