import subprocess
import shlex
from pydantic import BaseModel, Field
from typing import Dict, Any
from src.haive.tak.toolkits.dev.permission import PermissionsManager
from pathlib import Path
class CommandExecutionResult(BaseModel):
    """Represents the result of a shell command execution."""
    
    success: bool = Field(..., description="Indicates if the command executed successfully")
    command: str = Field(..., description="Executed command")
    stdout: str = Field(default="", description="Command standard output")
    stderr: str = Field(default="", description="Command standard error")
    exit_code: int = Field(..., description="Exit code of the command")
    error: str = Field(default="", description="Error message (if any)")

class SecureShellExecutor:
    """Shell command executor with enforced security restrictions using Pydantic."""

    def __init__(self):
        self.permissions_manager = PermissionsManager()

    def _extract_paths(self, command: str):
        """Extract file paths from the command arguments."""
        args = shlex.split(command)
        return [arg for arg in args if Path(arg).exists()]

    def run(self, command: str, timeout: int = 30) -> CommandExecutionResult:
        """Execute a command with security enforcement."""
        paths = self._extract_paths(command)

        for path in paths:
            if self.permissions_manager.is_restricted(path):
                return CommandExecutionResult(
                    success=False, command=command, error=f"🚫 Access denied to {path}", exit_code=1
                )
            if "rm" in command or "mv" in command or "cp" in command:
                if not self.permissions_manager.is_write_allowed(path):
                    return CommandExecutionResult(
                        success=False, command=command, error=f"🚫 Write access denied to {path}", exit_code=1
                    )
            if "cat" in command or "less" in command:
                if not self.permissions_manager.is_read_allowed(path):
                    return CommandExecutionResult(
                        success=False, command=command, error=f"🚫 Read access denied to {path}", exit_code=1
                    )

        try:
            result = subprocess.run(
                shlex.split(command), text=True, capture_output=True, timeout=timeout, check=True
            )
            return CommandExecutionResult(
                success=True, command=command, stdout=result.stdout.strip(), stderr=result.stderr.strip(), exit_code=result.returncode
            )
        except subprocess.CalledProcessError as e:
            return CommandExecutionResult(
                success=False, command=command, stderr=e.stderr.strip(), exit_code=e.returncode, error="Command failed"
            )