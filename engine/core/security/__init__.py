from .security import get_password_hash, verify_password, create_jwt_token, verify_jwt_token, refresh_jwt_token, get_current_user
from .role.roles import role_manager, permission_required

def setup(app):
    pass  # Безопасность настраивается через зависимости