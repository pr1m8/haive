#!/usr/bin/env python3
"""Run a monitored documentation build with real-time progress tracking."""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up environment
os.chdir(project_root)


def run_monitor():
    """Run the monitor in a separate thread."""
    time.sleep(2)  # Give build time to start
    subprocess.run(
        [
            sys.executable,
            'scripts/monitor_docs_build.py',
            '--simple',  # Use simple mode for cleaner output
        ],
    )


def main():
    """Run the monitored build."""
    print('🚀 Starting monitored documentation build...')
    print('=' * 80)

    # Start monitor in background
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()

    # Run the build with nox
    print('\n📦 Running nox -s docs_phased...')
    print('=' * 80)

    result = subprocess.run(
        ['nox', '-s', 'docs_phased'], capture_output=False, text=True,
    )

    print('\n' + '=' * 80)
    if result.returncode == 0:
        print('✅ Build completed successfully!')

        # Check for HTML files
        html_dir = project_root / 'docs' / 'build' / 'html'
        if html_dir.exists():
            html_files = list(html_dir.rglob('*.html'))
            print(f"\n📄 HTML files generated: {len(html_files)}")
            if html_files:
                print('\nSample files:')
                for f in html_files[:10]:
                    print(f"  - {f.relative_to(html_dir)}")
                if len(html_files) > 10:
                    print(f"  ... and {len(html_files) - 10} more")
        else:
            print('\n❌ No HTML output directory found!')
    else:
        print(f"❌ Build failed with return code: {result.returncode}")

    # Give monitor time to finish
    time.sleep(2)

    # Find and display latest monitor file
    log_dir = project_root / 'docs' / 'logs' / 'build'
    if log_dir.exists():
        monitor_files = sorted(
            log_dir.glob('build_monitor_*.json'), key=lambda f: f.stat().st_mtime,
        )
        if monitor_files:
            print(f"\n📊 Monitor report: {monitor_files[-1]}")


if __name__ == '__main__':
    main()
