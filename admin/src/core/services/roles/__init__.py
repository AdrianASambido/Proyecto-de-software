"""
Servicio para manejo de roles y permisos
"""

from src.core.database import db
from src.core.Entities.role import Role
from src.core.Entities.permission import Permission


def list_roles():
    """
    Retorna una lista de todos los roles.
    """
    roles = Role.query.all()
    return roles


def get_role_by_id(role_id):
    """
    Obtiene un rol por su ID.
    """
    return Role.query.get(role_id)


def get_role_by_name(name):
    """
    Obtiene un rol por su nombre.
    """
    return Role.query.filter_by(name=name).first()


def create_role(role_data):
    """
    Crea un nuevo rol.
    """
    nuevo_rol = Role(
        name=role_data.get("name"),
        description=role_data.get("description")
    )
    
    db.session.add(nuevo_rol)
    db.session.commit()
    return nuevo_rol


def update_role(role_id, role_data):
    """
    Actualiza un rol existente.
    """
    rol = get_role_by_id(role_id)
    if rol:
        rol.name = role_data.get("name", rol.name)
        rol.description = role_data.get("description", rol.description)
        db.session.commit()
    return rol


def delete_role(role_id):
    """
    Elimina un rol.
    """
    rol = get_role_by_id(role_id)
    if rol:
        db.session.delete(rol)
        db.session.commit()
        return True
    return False


def assign_permission_to_role(role_id, permission_id):
    """
    Asigna un permiso a un rol.
    """
    rol = get_role_by_id(role_id)
    permiso = get_permission_by_id(permission_id)
    
    if rol and permiso:
        rol.add_permission(permiso)
        db.session.commit()
        return True
    return False


def remove_permission_from_role(role_id, permission_id):
    """
    Remueve un permiso de un rol.
    """
    rol = get_role_by_id(role_id)
    permiso = get_permission_by_id(permission_id)
    
    if rol and permiso:
        rol.remove_permission(permiso)
        db.session.commit()
        return True
    return False


def list_permissions():
    """
    Retorna una lista de todos los permisos.
    """
    permissions = Permission.query.all()
    return permissions


def get_permission_by_id(permission_id):
    """
    Obtiene un permiso por su ID.
    """
    return Permission.query.get(permission_id)


def get_permission_by_name(name):
    """
    Obtiene un permiso por su nombre.
    """
    return Permission.query.filter_by(name=name).first()


def create_permission(permission_data):
    """
    Crea un nuevo permiso.
    """
    nuevo_permiso = Permission(
        name=permission_data.get("name"),
        description=permission_data.get("description"),
        module=permission_data.get("module"),
        action=permission_data.get("action")
    )
    
    db.session.add(nuevo_permiso)
    db.session.commit()
    return nuevo_permiso


def get_permissions_by_module(module):
    """
    Obtiene todos los permisos de un módulo específico.
    """
    return Permission.query.filter_by(module=module).all()


def get_role_permissions(role_id):
    """
    Obtiene todos los permisos de un rol.
    """
    rol = get_role_by_id(role_id)
    if rol:
        return rol.permissions
    return []
