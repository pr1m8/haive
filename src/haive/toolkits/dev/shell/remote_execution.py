import paramiko

class RemoteExecutor:
    """Securely execute commands on a remote machine via SSH."""

    def __init__(self, hostname: str, username: str, key_path: str):
        self.hostname = hostname
        self.username = username
        self.key_path = key_path
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """Establish SSH connection."""
        self.client.connect(self.hostname, username=self.username, key_filename=self.key_path)

    def run_remote(self, command: str):
        """Execute a command remotely."""
        stdin, stdout, stderr = self.client.exec_command(command)
        return {
            "stdout": stdout.read().decode().strip(),
            "stderr": stderr.read().decode().strip()
        }

    def close(self):
        """Close SSH connection."""
        self.client.close()

# Example Usage:
remote_executor = RemoteExecutor("192.168.1.100", "user", "~/.ssh/id_rsa")
remote_executor.connect()
print(remote_executor.run_remote("uname -a"))
remote_executor.close()
