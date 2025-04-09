from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict
from pathlib import Path
import json

class RolePermissions(BaseModel):
    """Defines permissions for a specific role."""
    read: List[Path] = Field(default=["/home"], description="Paths allowed for reading")
    write: List[Path] = Field(default=[], description="Paths allowed for writing")
    execute: List[str] = Field(default=[], description="Commands allowed for execution")

class RBACConfig(BaseModel):
    """Defines role-based access control settings."""
    roles: Dict[str, RolePermissions] = Field(
        default={
            "admin": RolePermissions(read=["/"], write=["/etc", "/var"], execute=["*"]),
            "developer": RolePermissions(read=["/home/dev"], write=["/home/dev/projects"], execute=["python", "gcc"]),
            "guest": RolePermissions(read=["/home/guest"], write=[], execute=[])
        },
        description="Role-based access control settings"
    )

    def can_read(self, role: str, path: str) -> bool:
        return any(Path(path).resolve().startswith(p) for p in self.roles.get(role, RolePermissions()).read)

    def can_write(self, role: str, path: str) -> bool:
        return any(Path(path).resolve().startswith(p) for p in self.roles.get(role, RolePermissions()).write)

    def can_execute(self, role: str, command: str) -> bool:
        allowed_commands = self.roles.get(role, RolePermissions()).execute
        return "*" in allowed_commands or command in allowed_commands

    def save_config(self, path: str = ".rbac_config.json"):
        """Save RBAC settings to a file."""
        with open(path, "w") as f:
            json.dump(self.model_dump(), f, indent=4)

    @classmethod
    def load_config(cls, path: str = ".rbac_config.json"):
        """Load RBAC settings from a file."""
        with open(path, "r") as f:
            return cls(**json.load(f))

# Example Usage:
rbac = RBACConfig()
rbac.save_config()
print(rbac.can_execute("developer", "gcc"))  # ✅ True
print(rbac.can_write("guest", "/home/guest"))  # ❌ False
