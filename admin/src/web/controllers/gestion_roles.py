"""
    Este controlador maneja las rutas relacionadas con la gestión de roles y permisos
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.core.services import roles
from src.core.services import users
from src.core.auth import admin_required, permission_required

bp = Blueprint("gestion_roles", __name__, url_prefix="/gestion-roles")


@bp.get("/")
@admin_required
def index():
    """Lista todos los roles"""
    roles_list = roles.list_roles()
    return render_template("administration/roles.html", roles=roles_list), 200


@bp.get("/roles")
@admin_required
def list_roles():
    """Lista todos los roles"""
    roles_list = roles.list_roles()
    return render_template("administration/roles.html", roles=roles_list), 200


@bp.get("/roles/<int:role_id>")
@admin_required
def show_role(role_id):
    """Muestra los detalles de un rol específico"""
    role = roles.get_role_by_id(role_id)
    if not role:
        flash("Rol no encontrado", "error")
        return redirect(url_for("gestion_roles.index"))
    
    role_permissions = roles.get_role_permissions(role_id)
    all_permissions = roles.list_permissions()
    
    return render_template("administration/role_detail.html", 
                         role=role, 
                         role_permissions=role_permissions,
                         all_permissions=all_permissions), 200


@bp.get("/usuarios")
@admin_required
def list_users():
    """Lista todos los usuarios para gestión de roles"""
    users_list = users.list_users()
    roles_list = roles.list_roles()
    return render_template("administration/users_roles.html", 
                         users=users_list, 
                         roles=roles_list), 200


@bp.post("/usuarios/<int:user_id>/asignar-rol")
@permission_required("user_update")
def assign_role_to_user(user_id):
    """Asigna un rol a un usuario"""
    role_id = request.form.get("role_id")
    
    if not role_id:
        flash("Debe seleccionar un rol", "error")
        return redirect(url_for("gestion_roles.list_users"))
    
    success = users.assign_role_to_user(user_id, int(role_id))
    
    if success:
        flash("Rol asignado correctamente", "success")
    else:
        flash("Error al asignar el rol", "error")
    
    return redirect(url_for("gestion_roles.list_users"))


@bp.post("/usuarios/<int:user_id>/bloquear")
@permission_required("user_update")
def block_user(user_id):
    """Bloquea un usuario"""
    success = users.block_user(user_id)
    
    if success:
        flash("Usuario bloqueado correctamente", "success")
    else:
        flash("No se puede bloquear este usuario (es administrador)", "error")
    
    return redirect(url_for("gestion_roles.list_users"))


@bp.post("/usuarios/<int:user_id>/desbloquear")
@permission_required("user_update")
def unblock_user(user_id):
    """Desbloquea un usuario"""
    success = users.unblock_user(user_id)
    
    if success:
        flash("Usuario desbloqueado correctamente", "success")
    else:
        flash("Error al desbloquear el usuario", "error")
    
    return redirect(url_for("gestion_roles.list_users"))


@bp.post("/roles/<int:role_id>/permisos/<int:permission_id>/asignar")
@admin_required
def assign_permission_to_role(role_id, permission_id):
    """Asigna un permiso a un rol"""
    success = roles.assign_permission_to_role(role_id, permission_id)
    
    if success:
        flash("Permiso asignado correctamente", "success")
    else:
        flash("Error al asignar el permiso", "error")
    
    return redirect(url_for("gestion_roles.show_role", role_id=role_id))


@bp.post("/roles/<int:role_id>/permisos/<int:permission_id>/remover")
@admin_required
def remove_permission_from_role(role_id, permission_id):
    """Remueve un permiso de un rol"""
    success = roles.remove_permission_from_role(role_id, permission_id)
    
    if success:
        flash("Permiso removido correctamente", "success")
    else:
        flash("Error al remover el permiso", "error")
    
    return redirect(url_for("gestion_roles.show_role", role_id=role_id))


@bp.get("/permisos")
@admin_required
def list_permissions():
    """Lista todos los permisos"""
    permissions = roles.list_permissions()
    return render_template("administration/permissions.html", permissions=permissions), 200


@bp.get("/api/roles")
def api_roles():
    """API endpoint para obtener roles (para AJAX)"""
    roles_list = roles.list_roles()
    return jsonify([{"id": role.id, "name": role.name} for role in roles_list])


@bp.get("/api/usuarios/<int:user_id>/rol")
def api_user_role(user_id):
    """API endpoint para obtener el rol de un usuario"""
    user = users.get_user_by_id(user_id)
    if user and user.role:
        return jsonify({"role_id": user.role.id, "role_name": user.role.name})
    return jsonify({"error": "Usuario no encontrado"}), 404
