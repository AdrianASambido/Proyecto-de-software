"""
    Este controlador maneja las rutas relacionadas con las operaciones de usuarios
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for
from src.core import board_usuarios

bp = Blueprint("users", __name__, url_prefix=("/usuarios"))

@bp.get("/lista_usuarios")
def index():
    """Muestra la lista de usuarios.
    Renderiza la plantilla con la lista de usuarios.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 2

    filtros = request.args.to_dict()
    filtros.pop("page", None)
    filtros.pop("per_page", None)

    pagination = board_usuarios.list_users(filtros).paginate(page=page, per_page=per_page)
    return render_template("usuarios/tabla_usuarios.html",
                           items=pagination.items,
                           pagination=pagination,
                           filtros=filtros), 200

@bp.route("/agregar_usuario")
def add_user():
    if request.method=="POST":
        user_data = dict(request.form)
        board_usuarios.add_user(user_data)
        return redirect(url_for("users.index"))
    
    return render_template("usuarios/agregar_usuario.html"), 200

@bp.route("/editar_usuario/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    usuario = board_usuarios.buscar_usuario_por_id(user_id)
    if request.method == "POST":
        nuevos_datos = dict(request.form)
        board_usuarios.modificar_usuario(user_id, nuevos_datos)
        return redirect(url_for("users.index"))
    
    return render_template("usuarios/editar_usuario.html", user=usuario), 200