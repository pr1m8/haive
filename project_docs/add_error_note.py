#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys

if len(sys.argv) < 3:
    print("Usage: python add_error_note.py <error_id> <note>")
    sys.exit(1)

error_id = sys.argv[1]
note = " ".join(sys.argv[2:])
state_file = "error_analysis/todo_state.json"

# Load state
with open(state_file) as f:
    state = json.load(f)

# Add note
state["notes"][error_id] = note

# Save state
with open(state_file, "w") as f:
    json.dump(state, f, indent=2)

print(f"📝 Added note to {error_id}")

# Regenerate index

subprocess.run([sys.executable, "create_error_todo_index.py"], check=False)
