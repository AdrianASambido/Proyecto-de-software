"Este modelo cubre operaciones relacionadas con los usuarios."

from src.core.database import db
from src.core.Entities.user import User


def list_users():
    """
    Retorna una lista de todos los usuarios.
    """
    users = User.query.all()
    return users

def list_users(filtros: dict):
    """
    Retorna una lista de usuarios aplicando filtros dinámicos.
    Filtros soportados:
      - email (texto parcial)
      - rol (selector)
      - activo (checkbox)
    """
    query = User.query

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

def add_user(user_data):
    """
    Agrega un nuevo usuario.
    """
    nuevo_usuario = User(
        nombre=user_data.get("nombre"),
        apellido=user_data.get("apellido"),
        email=user_data.get("email"),
        rol=user_data.get("rol"),
        activo=user_data.get("activo", True),
        contraseña_cifrada=user_data.get("contraseña_cifrada"),
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def buscar_usuario_por_email(email):
    """
    Busca un usuario por email.
    """
    usuario = User.query.filter_by(email=email).first()
    return usuario

def buscar_usuario_por_id(user_id):
    """
    Busca un usuario por ID.
    """
    usuario = User.query.get(user_id)
    return usuario

def borrar_usuario(user_id):
    """
    Se marca al usuario como eliminado
    """
    usuario = User.query.get(user_id)
    if usuario:
        usuario.eliminado = True
        db.session.commit()
        return True
    return False

def desactivar_cuenta(user_id):
    """
    Desactiva la cuenta de un usuario.
    """
    usuario = User.query.get(user_id)
    if usuario:
        usuario.activo = False
        db.session.commit()
        return True
    return False

def activar_cuenta(user_id):
    """
    Activa la cuenta de un usuario.
    """
    usuario = User.query.get(user_id)
    if usuario:
        usuario.activo = True
        db.session.commit()
        return True
    return False

def modificar_usuario(user_id, nuevos_datos):
    """
    Modifica los datos de un usuario existente, en caso de tener los campos habilitados.
    """
    usuario = User.query.get(user_id)
    if usuario:
        if "nombre" in nuevos_datos:
            usuario.nombre = nuevos_datos.get("nombre", usuario.nombre)
        if "apellido" in nuevos_datos:
            usuario.apellido = nuevos_datos.get("apellido", usuario.apellido)
        if "email" in nuevos_datos:
            usuario.email = nuevos_datos.get("email", usuario.email)
        if "rol" in nuevos_datos:
            usuario.rol = nuevos_datos.get("rol", usuario.rol)
        if "contraseña_cifrada" in nuevos_datos:
            usuario.contraseña_cifrada = nuevos_datos["contraseña_cifrada"]
        db.session.commit()
        return usuario
    return None