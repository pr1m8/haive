#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python mark_error_fixed.py <error_id>")
    sys.exit(1)

error_id = sys.argv[1]
state_file = "error_analysis/todo_state.json"

# Load state
with open(state_file) as f:
    state = json.load(f)

# Update state
if error_id not in state["fixed"]:
    state["fixed"].append(error_id)
    # Remove from other states
    if error_id in state["in_progress"]:
        state["in_progress"].remove(error_id)
    if error_id in state["wont_fix"]:
        state["wont_fix"].remove(error_id)

# Save state
with open(state_file, "w") as f:
    json.dump(state, f, indent=2)

print(f"✅ Marked {error_id} as fixed")

# Regenerate index

subprocess.run([sys.executable, "create_error_todo_index.py"], check=False)
