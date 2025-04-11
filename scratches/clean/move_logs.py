import os
import shutil
from pathlib import Path

def move_logs_to_root_log_folder(root_dir='.'):
    root = Path(root_dir).resolve()
    log_dir = root / 'logs'
    log_dir.mkdir(exist_ok=True)

    for path in root.rglob('*.log'):
        # Skip logs already in the log dir
        if log_dir in path.parents:
            continue

        target = log_dir / path.name
        # Rename if conflict
        counter = 1
        while target.exists():
            target = log_dir / f"{path.stem}_{counter}{path.suffix}"
            counter += 1

        print(f"Moving {path} -> {target}")
        shutil.move(str(path), target)

    print("✅ Done.")

if __name__ == "__main__":
    move_logs_to_root_log_folder()
