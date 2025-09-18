from .config import settings
from .utils import generate_random_string, load_roles, roles, ADMIN_ROLE, USER_ROLE, MODERATOR_ROLE

def setup(app):
    pass  # Конфигурация загружается автоматически через импорт settings