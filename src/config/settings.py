import os
import sys

# Get the base directory of the `src` folder
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure `haive` is in the Python path
HAIVE_DIR = os.path.join(SRC_DIR, "haive")
if HAIVE_DIR not in sys.path:
    sys.path.append(HAIVE_DIR)

# Define key directories relative to `SRC_DIR`
PROJECTS_DIR = os.path.join(SRC_DIR, "projects")
DOCUMENTS_DIR = os.path.join(SRC_DIR, "documents")
VECTORSTORE_DIR = os.path.join(SRC_DIR, "vectorstore")
CACHE_DIR = os.path.join(SRC_DIR, "lc_cache")
AGENTS_DIR = os.path.join(HAIVE_DIR, "agents")  # Agents belong inside `haive`

# Ensure the `agents` directory exists (initialize it if missing)
os.makedirs(AGENTS_DIR, exist_ok=True)

# Ensure other directories exist
#for directory in [PROJECTS_DIR, DOCUMENTS_DIR, VECTORSTORE_DIR, CACHE_DIR]:
  #  os.makedirs(directory, exist_ok=True)

# Print paths for debugging
print(f"Source Directory: {SRC_DIR}")
print(f"Projects Directory: {PROJECTS_DIR}")
print(f"Documents Directory: {DOCUMENTS_DIR}")
print(f"Vectorstore Directory: {VECTORSTORE_DIR}")
print(f"Cache Directory: {CACHE_DIR}")
print(f"Agents Directory: {AGENTS_DIR}")
