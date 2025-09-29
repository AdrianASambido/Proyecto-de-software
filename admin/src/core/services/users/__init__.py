"Este modelo cubre operaciones relacionadas con los usuarios."

from src.core.database import db
from src.core.Entities.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def list_users():
    """
    Retorna una lista de todos los usuarios menos los eliminados
    """
    users = User.query.filter_by(eliminado=False).all()
    return users

def get_user_by_email(email):
    """
    Retorna un usuario por su correo electrónico
    """
    user = User.query.filter_by(email=email, eliminado=False).first()
    return user

def delete_user(user_id):
    """
    Marca un usuario como eliminado en lugar de borrarlo físicamente.
    """
    user = User.query.get(user_id)
    if user and not user.eliminado:
        user.eliminado = True
        db.session.commit()
        return user
    else:
        raise ValueError("Usuario no encontrado.")

def add_user(user_data):
    """
    Agrega un nuevo usuario.
    """
    nuevo_usuario = User(
        email=user_data.get("email"),
        nombre=user_data.get("nombre"),
        username=user_data.get("username"),
        apellido=user_data.get("apellido"),
        contraseña_cifrada=bcrypt.generate_password_hash(user_data.get("contraseña")).decode('utf-8'),
        rol_id=user_data.get("rol_id"),
    )

    #Revisa si el usuario ya existe
    usuario_existente = User.query.filter_by(email=nuevo_usuario.email).first()
    if usuario_existente:
        raise ValueError("El usuario con este correo ya existe.")
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario
