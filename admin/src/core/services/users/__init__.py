"Este modelo cubre operaciones relacionadas con los usuarios."

from src.core.database import db
from src.core.Entities.user import User
from src.core.Entities.site import Site
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
    """Retorna una lista de usuarios aplicando filtros dinámicos, salvo los eliminados."""
    query = User.query.filter_by(eliminado=False)

    email = filtros.get("email") # filtro por email (texto parcial)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    # ---- Filtro por roles múltiples ----
    roles_ids = filtros.get("rol_id", [])
    if roles_ids:
        try:
            roles_ids = [int(r) for r in roles_ids if r.isdigit()]
            if roles_ids:
                query = query.join(User.roles).filter(Role.id.in_(roles_ids))
        except ValueError:
            pass

    activo = filtros.get("activo")# filtro por estado (activo)
    if activo:
        if activo == '1':
            query = query.filter(User.activo.is_(True))
        elif activo == '0':
            query = query.filter(User.activo.is_(False))

    order = filtros.get("order")
    if order == "fecha_asc":
        query = query.order_by(User.created_at.asc())
    elif order == "fecha_desc":
        query = query.order_by(User.created_at.desc())

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
    
    nuevo_usuario = User(
        email=user_data.get("email"),
        nombre=user_data.get("nombre"),
        username=user_data.get("username"),
        apellido=user_data.get("apellido"),
        contraseña_cifrada=bcrypt.generate_password_hash(user_data.get("contraseña")).decode('utf-8'),
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
    Retorna un usuario por su correo electrónico
    """
    user = User.query.filter_by(email=email, eliminado=False).first()
    return user

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
        
        db.session.commit()
        return usuario
    
def update_user_admin(user_id, user_data):
    """
    Modifica los datos de un usuario existente, incluyendo campos administrativos.
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
        
        if "rol_id" in user_data:
            roles_ids = user_data.get("rol_id", [])
            roles_ids = [int(r) for r in roles_ids if r]
            if roles_ids:
                roles = Role.query.filter(Role.id.in_(roles_ids)).all()
                usuario.roles = roles
            else:
                usuario.roles = []
        
        #si es admin no se puede desactivar
        if "is_active" in user_data:
            if usuario.is_admin and not user_data["is_active"]:
                raise ValueError("No se puede desactivar un usuario Administrador.")
            usuario.activo = bool(user_data["is_active"])
        
        db.session.commit()
        return usuario
    else:
        raise ValueError("Usuario no encontrado.")

def assign_roles_to_user(user_id, role_ids):
    """
    Asigna varios roles a un usuario.
    """
    usuario = User.query.get(user_id)
    if usuario:
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        if not roles:
            raise ValueError("Roles no encontrados.")
        usuario.roles = roles
        db.session.commit()
        return usuario
    else:
        raise ValueError("Usuario no encontrado.")


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


def add_favorite_site(user_id, site_id):
    """
    Agrega un sitio a la lista de favoritos del usuario.
    """
    user = get_user_by_id(user_id)
    site = Site.query.get(site_id)
    if user and site:
        if site not in user.favorites:
            user.favorites.append(site)
            db.session.commit()
            return True
    return False

def remove_favorite_site(user_id, site_id):
    """
    Remueve un sitio de la lista de favoritos del usuario.
    """
    user = get_username_by_email(user_id)
    site = Site.query.get(site_id)
    if user and site and site in user.favorites:
        user.favorites.remove(site)
        db.session.commit()
        return True
    return False


def is_favorite(user_id, site_id):
    """
    Verifica si un sitio es favorito para un usuario.
    """
    user = get_user_by_id(user_id)
    site = Site.query.get(site_id)
    if user and site:
        return site in user.favorites
    return False

def get_favorite_sites(user_id):
    """
    Obtiene la lista de sitios favoritos de un usuario.
    """
    user = get_user_by_id(user_id)
    if user:
        return user.favorites
    return []