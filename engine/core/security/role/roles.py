# engine/core/security/role/roles.py
import json
from pathlib import Path
from fastapi import Depends, HTTPException

ROLE_FILE = Path(__file__).parent / "roles.json"

class RoleManager:
    def __init__(self, role_file: Path = ROLE_FILE):
        self.role_file = role_file
        self.roles = self.load_roles()

    def load_roles(self):
        if not self.role_file.exists():
            return {}
        with open(self.role_file, "r", encoding="utf-8") as f:
            return json.load(f).get("roles", {})

    def get_permission_value(self, role_name: str) -> int:
        role = self.roles.get(role_name)
        if not role:
            return 0
        return role.get("permissions", 0)

role_manager = RoleManager()

def permission_required(level: int):
    def dependency(role: str = "user"):
        role_perms = role_manager.get_permission_value(role)
        if role_perms < level:
            raise HTTPException(status_code=403, detail="Permission denied")
    return Depends(dependency)