"""
    Este controlador maneja las rutas relacionadas con las operaciones de usuarios
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from src.core.services import users as board_users
from src.core.formularios import RegistrationForm, EditUserForm, EditUserAdminForm
from src.core.auth import login_required, permission_required
bp = Blueprint("users", __name__, url_prefix=("/usuarios"))




@bp.get("/lista_usuarios")
@login_required
@permission_required("user_index")
def index():
    """Muestra la lista de usuarios.
    Renderiza la plantilla con la lista de usuarios.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 2

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    pagination = board_users.list_users(filtros).paginate(page=page, per_page=per_page)
    return render_template("usuarios/tabla_usuarios.html",
                           items=pagination.items,
                           pagination=pagination,
                           filtros=filtros), 200


@bp.route("/agregar_usuario", methods=["GET", "POST"])
@login_required
@permission_required("user_create")
def add_user():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_data = {
            "nombre": form.nombre.data,
            "apellido": form.apellido.data,
            "username": form.username.data,
            "email": form.email.data,
            "contraseña": form.contraseña.data,  # el servicio se encarga de encriptar
            "rol_id": form.rol_id.data,
        }
        board_users.add_user(user_data)
        flash("Usuario agregado exitosamente.", "success")
        return redirect(url_for("users.index"))
    else:
        print(form.errors)
    
    return render_template("usuarios/agregar_usuario.html", form=form), 200

@bp.route("/editar_usuario/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    usuario = board_users.get_user_by_id(user_id)
    form = EditUserForm(obj=usuario, original_email=usuario.email)
    if form.validate_on_submit():
        nuevos_datos = form.data
        print("Se consiguieron los datos nuevos")
        board_users.update_user(user_id, nuevos_datos)
        print("Se guardaron los datos nuevos")
        return redirect(url_for("users.index"))
    else:
        print(form.errors)
    
    return render_template("usuarios/editar_usuario.html", user=usuario, form=form), 200

@bp.post("/eliminar_usuario/<int:user_id>")
@login_required
@permission_required("user_destroy")
def delete_user(user_id):

    if not board_users.get_user_by_id(user_id):
        flash("Usuario no encontrado.", "error")

    board_users.delete_user(user_id)
    flash("Usuario eliminado exitosamente.", "success")
    return redirect(url_for("users.index"))

@bp.route("editar_usuario_admin/<int:user_id>", methods=["GET", "POST"])
@login_required
@permission_required("user_update")
def edit_user_admin(user_id):
    usuario = board_users.get_user_by_id(user_id)
    form = EditUserAdminForm(obj=usuario, original_email=usuario.email)
    if form.validate_on_submit():
        nuevos_datos = form.data
        print("Se consiguieron los datos nuevos")
        board_users.update_user(user_id, nuevos_datos)
        print("Se guardaron los datos nuevos")
        return redirect(url_for("users.index"))
    else:
        print(form.errors)
    
    return render_template("usuarios/editar_usuario_admin.html", user=usuario, form=form), 200
