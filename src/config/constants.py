import os
import sys

# Determine the absolute path to the root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
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
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")  # New resources directory
GRAPH_IMAGES_DIR = os.path.join(RESOURCES_DIR, "graph_images")  # Store graph images here
EMBEDDINGS_CACHE_DIR = os.path.join(RESOURCES_DIR, "embeddings_cache")  # Store embeddings cache here

# Ensure the necessary directories exist
for directory in [AGENTS_DIR, PROJECTS_DIR, DOCUMENTS_DIR, VECTORSTORE_DIR, CACHE_DIR, GRAPH_IMAGES_DIR]:
    os.makedirs(directory, exist_ok=True)

# Print paths for debugging
#print(f"Root Directory: {ROOT_DIR}")
#print(f"Source Directory: {SRC_DIR}")
#print(f"Projects Directory: {PROJECTS_DIR}")
#print(f"Documents Directory: {DOCUMENTS_DIR}")
#print(f"Vectorstore Directory: {VECTORSTORE_DIR}")
#print(f"Cache Directory: {CACHE_DIR}")
#print(f"Agents Directory: {AGENTS_DIR}")
#print(f"Resources Directory: {RESOURCES_DIR}")
#print(f"Graph Images Directory: {GRAPH_IMAGES_DIR}")
