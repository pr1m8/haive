import subprocess
import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOCS_DIR = "docs"
BUILD_DIR = "docs/_build/html"
PORT = 8000
IGNORE_DIR = os.path.join(DOCS_DIR, "_build")
EXIT_FLAG = False  # Global flag to exit the script safely

class DocsEventHandler(FileSystemEventHandler):
    """Handles file changes and triggers incremental Sphinx rebuilds."""

    def on_modified(self, event):
        """Trigger an incremental rebuild when an .rst or .py file is modified."""
        if EXIT_FLAG:  # Stop rebuilds if exiting
            return
        
        # Ignore changes inside _build directory to prevent infinite loops
        if IGNORE_DIR in event.src_path:
            return
        
        if event.src_path.endswith(".rst") or event.src_path.endswith(".py"):
            print(f"🔄 Detected change in {event.src_path}. Rebuilding docs...")
            rebuild_incrementally()

def regenerate_api_docs():
    """Runs Sphinx apidoc to regenerate API documentation when Python files change."""
    print("📄 Generating API docs...")
    subprocess.run(["poetry", "run", "sphinx-apidoc", "-o", "docs/agents", "src/haive/agents"], check=True)
    subprocess.run(["poetry", "run", "sphinx-apidoc", "-o", "docs/core", "src/haive/core"], check=True)
    subprocess.run(["poetry", "run", "sphinx-apidoc", "-o", "docs/flstaesr", "src/haive/flstaesr"], check=True)

def rebuild_incrementally():
    """Runs an incremental Sphinx build (avoids full clean)."""
    if not Path(BUILD_DIR).exists():
        print("⚠️ No HTML build found! Performing full rebuild...")
        full_rebuild()
    else:
        subprocess.run(["poetry", "run", "sphinx-build", "-b", "html", "-d", "docs/_build/doctrees", DOCS_DIR, BUILD_DIR], check=True)
        print("✅ Docs updated.")

def full_rebuild():
    """Runs a full clean and rebuild."""
    subprocess.run(["poetry", "run", "make", "-C", DOCS_DIR, "clean"], check=True)
    regenerate_api_docs()  # Ensure API docs are generated
    subprocess.run(["poetry", "run", "make", "-C", DOCS_DIR, "html"], check=True)
    print("✅ Full rebuild completed.")

def serve_docs():
    """Starts a local HTTP server in the background (if not already running)."""
    if not is_server_running():
        print(f"📢 Serving docs at http://localhost:{PORT}/")
        subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", BUILD_DIR])

def is_server_running():
    """Check if the docs server is already running."""
    try:
        import requests
        response = requests.get(f"http://localhost:{PORT}")
        return response.status_code == 200
    except:
        return False

def watch_docs():
    """Watches the docs folder for changes and triggers incremental rebuilds."""
    global EXIT_FLAG
    event_handler = DocsEventHandler()
    observer = Observer()
    observer.schedule(event_handler, DOCS_DIR, recursive=True)
    observer.schedule(event_handler, "src/haive", recursive=True)  # Watch for code changes
    observer.start()

    print(f"👀 Watching for changes in {DOCS_DIR} & src/haive (excluding {IGNORE_DIR})...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n❌ Exiting... Cleaning up watchers.")
        EXIT_FLAG = True  # Stop further rebuilds
        observer.stop()
    observer.join()

def main():
    """Runs the full documentation process: build, serve, and watch."""
    if not Path(BUILD_DIR).exists():
        print("🛠 Running initial full build...")
        full_rebuild()
    
    serve_docs()  # Start server
    watch_docs()  # Start file watcher

if __name__ == "__main__":
    main()
