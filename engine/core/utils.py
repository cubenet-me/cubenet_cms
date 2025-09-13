# engine/core/utils.py
import random, string
import json
from pathlib import Path

# Генерация случайной строки
def generate_random_string(length: int = 12) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Роли
ROLE_FILE = Path(__file__).parent / "role.json"

def load_roles():
    with open(ROLE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("roles", {})

# Загружаем роли один раз
roles = load_roles()
ADMIN_ROLE = roles.get("admin")
USER_ROLE = roles.get("user")
MODERATOR_ROLE = roles.get("moderator")
