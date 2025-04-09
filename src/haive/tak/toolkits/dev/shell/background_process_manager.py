import psutil
import subprocess
import shlex
from typing import Dict, Any, List

class BackgroundProcessManager:
    """Manages long-running background processes."""
    
    def __init__(self):
        self.processes = {}

    def run_background(self, command: str) -> Dict[str, Any]:
        """Start a long-running command in the background."""
        try:
            cmd_args = shlex.split(command)
            process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes[process.pid] = process
            return {"success": True, "pid": process.pid, "message": f"✅ {command} is running in the background"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_running(self) -> List[Dict[str, Any]]:
        """List currently running background processes."""
        active_processes = []
        for pid, process in self.processes.items():
            if psutil.pid_exists(pid):
                active_processes.append({"pid": pid, "command": " ".join(process.args), "status": "running"})
        return active_processes

    def stop_process(self, pid: int) -> Dict[str, Any]:
        """Stop a specific background process."""
        try:
            if pid in self.processes:
                self.processes[pid].terminate()
                del self.processes[pid]
                return {"success": True, "message": f"✅ Process {pid} stopped"}
            return {"success": False, "error": f"❌ Process {pid} not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    def list_network_listeners(self):
        """List all processes listening on a network port."""
        listeners = []
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == "LISTEN":
                listeners.append({
                    "port": conn.laddr.port,
                    "process": psutil.Process(conn.pid).name() if conn.pid else "Unknown",
                    "pid": conn.pid
                })
        return listeners
# Example Usage:
bg_manager = BackgroundProcessManager()
print(bg_manager.run_background("npm run dev"))  # ✅ Starts background process
print(bg_manager.list_running())  # 🔍 Lists all running processes
print(bg_manager.stop_process(12345))  # ❌ Replace with real PID to stop
