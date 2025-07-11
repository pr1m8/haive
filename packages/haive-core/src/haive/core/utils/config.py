import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Project directories
PROJECTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "projects")

# Document directories
DOCUMENTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "documents")

# Vectorstore directories
VECTORSTORE_DIR = os.path.join(os.path.dirname(BASE_DIR), "vectorstore")

# Data directories
CACHE_DIR = os.path.join(os.path.dirname(BASE_DIR), "lc_cache")
