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
        nombre=user_data.get("nombre"),
        apellido=user_data.get("apellido"),
        email=user_data.get("email"),
        rol_id=user_data.get("rol"),
        activo=user_data.get("activo", True),
        contraseña_cifrada=user_data.get("contraseña_cifrada"),
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

    
