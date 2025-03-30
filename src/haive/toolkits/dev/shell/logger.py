import datetime

class ExecutionLogger:
    """Logs command execution details for audit trail."""

    LOG_FILE = Path.home() / ".secure_shell_log.json"

    @classmethod
    def log(cls, role: str, command: str, result: Dict[str, Any]):
        """Log command execution details."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "role": role,
            "command": command,
            "success": result["success"],
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "exit_code": result.get("exit_code", ""),
            "error": result.get("error", ""),
        }

        existing_logs = []
        if cls.LOG_FILE.exists():
            with open(cls.LOG_FILE, "r") as f:
                existing_logs = json.load(f)

        existing_logs.append(log_entry)
        with open(cls.LOG_FILE, "w") as f:
            json.dump(existing_logs, f, indent=4)

# Example Usage:
executor = SecureShellExecutor(role="admin")
result = executor.run("ls -lah")
ExecutionLogger.log("admin", "ls -lah", result)
