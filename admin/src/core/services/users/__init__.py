"Este modelo cubre operaciones relacionadas con los usuarios."

from src.core.database import db
from src.core.Entities.user import User
from src.core.Entities.role import Role
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def list_users():
    """
    Retorna una lista de todos los usuarios menos los eliminados
    """
    users = User.query.filter_by(eliminado=False).all()
    return users

def list_users(filtros: dict):
    """
    Retorna una lista de usuarios aplicando filtros dinámicos, salvo los eliminados
    Filtros soportados:
      - email (texto parcial)
      - rol (selector)
      - activo (checkbox)
    """
    query = User.query.filter_by(eliminado=False)

    email = filtros.get("email")
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    rol = filtros.get("role")
    if rol:
        query = query.filter(User.rol_id == rol)

    activo = filtros.get("activo")
    if activo:
        query = query.filter(User.activo == True)

    return query

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
    # Obtener el rol por ID o nombre
    rol_id = user_data.get("rol_id")
    if not rol_id:
        # Si no se proporciona rol_id, buscar por nombre
        rol_name = user_data.get("rol_id", "Editor")  # Default a Editor
        rol = Role.query.filter_by(name=rol_name).first()
        rol_id = rol.id if rol else 2  # Default a Editor (ID 2)
    
    nuevo_usuario = User(
        email=user_data.get("email"),
        nombre=user_data.get("nombre"),
        username=user_data.get("username"),
        apellido=user_data.get("apellido"),
        contraseña_cifrada=bcrypt.generate_password_hash(user_data.get("contraseña")).decode('utf-8'),
        rol_id=int(rol_id),
    )

    #Revisa si el usuario ya existe
    usuario_existente = User.query.filter_by(email=nuevo_usuario.email).first()
    if usuario_existente:
        raise ValueError("El usuario con este correo ya existe.")
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def get_user_by_id(user_id):
    """
    Retorna un usuario por su ID.
    """
    return User.query.get(user_id)


def get_username_by_email(email):
    """
    Retorna el nombre de usuario por su correo electrónico
    """
    user = User.query.filter_by(email=email, eliminado=False).first()
    return user.username if user else None


def get_user_by_email(email):
    """
    Retorna un usuario por su correo electrónico.
    """
    return User.query.filter_by(email=email, eliminado=False).first()

def update_user(user_id, user_data):
    """
    Modifica los datos de un usuario existente, en caso de tener los campos habilitados.
    """
    usuario = User.query.get(user_id)
    if usuario:
        if "nombre" in user_data and user_data["nombre"] and user_data["nombre"] != usuario.nombre:
            usuario.nombre = user_data["nombre"]
        if "apellido" in user_data and user_data["apellido"] and user_data["apellido"] != usuario.apellido:
            usuario.apellido = user_data["apellido"]
        if "email" in user_data and user_data["email"] and user_data["email"] != usuario.email:
            usuario.email = user_data["email"]
        if "username" in user_data and user_data["username"] and user_data["username"] != usuario.username:
            usuario.username = user_data["username"]
        if "contraseña" in user_data and user_data["contraseña"] and user_data["contraseña"] != usuario.contraseña_cifrada:
            usuario.contraseña_cifrada = bcrypt.generate_password_hash(user_data["contraseña"]).decode('utf-8')
        if "rol_id" in user_data and user_data["rol_id"]:
            usuario.rol_id = int(user_data["rol_id"])
        
        db.session.commit()
        return usuario

def assign_role_to_user(user_id, role_id):
    """
    Asigna un rol a un usuario.
    """
    usuario = get_user_by_id(user_id)
    rol = Role.query.get(role_id)
    
    if usuario and rol:
        usuario.rol_id = role_id
        db.session.commit()
        return True
    return False


def block_user(user_id):
    """
    Bloquea un usuario.
    """
    usuario = get_user_by_id(user_id)
    if usuario and usuario.can_be_blocked():
        usuario.block()
        db.session.commit()
        return True
    return False


def unblock_user(user_id):
    """
    Desbloquea un usuario.
    """
    usuario = get_user_by_id(user_id)
    if usuario:
        usuario.unblock()
        db.session.commit()
        return True
    return False

def get_users_by_role(role_id):
    """
    Obtiene todos los usuarios con un rol específico.
    """
    return User.query.filter_by(rol_id=role_id).all()


def get_active_users():
    """
    Obtiene todos los usuarios activos.
    """
    return User.query.filter_by(activo=True).all()


def get_blocked_users():
    """
    Obtiene todos los usuarios bloqueados.
    """
    return User.query.filter_by(bloqueado=True).all()