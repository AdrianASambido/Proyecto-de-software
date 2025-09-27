"Este modelo cubre operaciones relacionadas con los usuarios."

from src.core.database import db
from src.core.Entities.user import User


def list_users():
    """
    Retorna una lista de todos los usuarios.
    """
    users = User.query.all()
    return users


def add_user(user_data):
    """
    Agrega un nuevo usuario.
    """
    nuevo_usuario = User(
        email=user_data.get("email"),
        nombre=user_data.get("nombre"),
        username=user_data.get("username"),
        apellido=user_data.get("apellido"),
        contraseña_cifrada=user_data.get("contraseña_cifrada"),
        rol_id=user_data.get("rol_id"),
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario
